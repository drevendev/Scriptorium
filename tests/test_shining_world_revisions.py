import unittest

from scriptorium.shining_world_revisions import (
    CANDIDATE_ID,
    MANIFEST_VERSION,
    PART_CHAPTER_COUNTS,
    build_manifest,
    expected_chapters,
    replay_manifest,
    validate_manifest,
)


class ShiningWorldRevisionTests(unittest.TestCase):
    @staticmethod
    def _fetcher(chapters):
        rows = tuple(chapters)
        return {
            str(row["title"]): {
                "revision_id": 6_000_000 + int(row["ordinal"]),
                "timestamp": f"2024-01-{((int(row['ordinal']) - 1) % 28) + 1:02d}T12:34:56Z",
                "mediawiki_sha1": f"{int(row['ordinal']):040x}",
                "wikitext": "transient source prose is deliberately ignored",
            }
            for row in rows
        }

    def test_expected_chapters_are_exact_three_part_contract(self):
        chapters = expected_chapters()
        self.assertEqual(len(chapters), 34)
        self.assertEqual(PART_CHAPTER_COUNTS, (16, 11, 7))
        self.assertEqual(
            chapters[0]["title"],
            "Блистающий мир (Грин)/Часть I/Глава I",
        )
        self.assertEqual(
            chapters[15]["title"],
            "Блистающий мир (Грин)/Часть I/Глава XVI",
        )
        self.assertEqual(
            chapters[16]["title"],
            "Блистающий мир (Грин)/Часть II/Глава I",
        )
        self.assertEqual(
            chapters[-1]["title"],
            "Блистающий мир (Грин)/Часть III/Глава VII",
        )

    def test_build_manifest_is_source_free_and_valid(self):
        manifest = build_manifest(fetcher=self._fetcher)
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["candidate_id"], CANDIDATE_ID)
        self.assertEqual(len(manifest["chapters"]), 34)
        self.assertEqual(
            manifest["capture_scope"],
            {
                "chapter_revision_inventory_frozen": True,
                "literary_body_extraction_frozen": False,
                "composite_identity_frozen": False,
                "source_text_committed": False,
            },
        )
        serialized = repr(manifest)
        self.assertNotIn("transient source prose", serialized)
        self.assertNotIn("wikitext", serialized)
        self.assertEqual(len(validate_manifest(manifest)), 34)

    def test_build_manifest_fails_closed_on_inventory_or_identity_drift(self):
        def missing_last(chapters):
            records = self._fetcher(chapters)
            records.pop(str(expected_chapters()[-1]["title"]))
            return records

        with self.assertRaisesRegex(ValueError, "chapter inventory mismatch"):
            build_manifest(fetcher=missing_last)

        def duplicate_revision(chapters):
            records = self._fetcher(chapters)
            titles = list(records)
            records[titles[1]]["revision_id"] = records[titles[0]]["revision_id"]
            return records

        with self.assertRaisesRegex(ValueError, "duplicate revision id"):
            build_manifest(fetcher=duplicate_revision)

    def test_validate_manifest_fails_closed_on_chapter_order_drift(self):
        manifest = build_manifest(fetcher=self._fetcher)
        manifest["chapters"][0]["title"] = "wrong title"
        with self.assertRaisesRegex(ValueError, "chapter identity drift"):
            validate_manifest(manifest)

    def test_replay_verifies_exact_inventory_without_returning_prose(self):
        manifest = build_manifest(fetcher=self._fetcher)

        def replay_fetcher(identities):
            rows = tuple(identities)
            self.assertEqual(len(rows), 34)
            self.assertEqual(rows[0]["revision_id"], 6_000_001)
            return {str(row["title"]): "source prose" for row in rows}

        receipt = replay_manifest(manifest, fetcher=replay_fetcher)
        self.assertEqual(
            receipt,
            {
                "verified": True,
                "candidate_id": CANDIDATE_ID,
                "chapter_count": 34,
                "source_text_committed": False,
            },
        )
        self.assertNotIn("source prose", repr(receipt))


if __name__ == "__main__":
    unittest.main()
