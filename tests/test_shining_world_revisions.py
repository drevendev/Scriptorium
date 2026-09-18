import unittest

from scriptorium.shining_world_revisions import (
    CANDIDATE_ID,
    MANIFEST_VERSION,
    PART_CHAPTER_COUNTS,
    build_manifest,
    expected_chapters,
    fetch_chapter_inventory,
    replay_manifest,
    validate_manifest,
)


class ShiningWorldRevisionTests(unittest.TestCase):
    @staticmethod
    def _fetcher(chapters):
        rows = tuple(chapters)
        return {
            str(row["title"]): {
                "status": "present",
                "revision_id": 6_000_000 + int(row["ordinal"]),
                "revision_timestamp": f"2024-01-{((int(row['ordinal']) - 1) % 28) + 1:02d}T12:34:56Z",
                "mediawiki_sha1": f"{int(row['ordinal']):040x}",
            }
            for row in rows
        }

    @staticmethod
    def _missing_last(chapters):
        records = ShiningWorldRevisionTests._fetcher(chapters)
        title = str(expected_chapters()[-1]["title"])
        records[title] = {"status": "missing"}
        return records

    def test_expected_chapters_are_exact_three_part_contract(self):
        chapters = expected_chapters()
        self.assertEqual(len(chapters), 34)
        self.assertEqual(PART_CHAPTER_COUNTS, (16, 11, 7))
        self.assertEqual(chapters[0]["title"], "Блистающий мир (Грин)/Часть I/Глава I")
        self.assertEqual(chapters[15]["title"], "Блистающий мир (Грин)/Часть I/Глава XVI")
        self.assertEqual(chapters[16]["title"], "Блистающий мир (Грин)/Часть II/Глава I")
        self.assertEqual(chapters[-1]["title"], "Блистающий мир (Грин)/Часть III/Глава VII")

    def test_probe_records_red_links_without_requesting_source_prose(self):
        chapters = expected_chapters()[:2]
        seen_params = {}

        def query(params):
            seen_params.update(params)
            return {"query": {"pages": [
                {"title": chapters[0]["title"], "revisions": [{"revid": 123, "timestamp": "2024-01-01T00:00:00Z", "sha1": "1" * 40}]},
                {"title": chapters[1]["title"], "missing": True},
            ]}}

        records = fetch_chapter_inventory(chapters, query=query)
        self.assertEqual(seen_params["rvprop"], "ids|timestamp|sha1")
        self.assertNotIn("content", seen_params["rvprop"])
        self.assertNotIn("rvslots", seen_params)
        self.assertEqual(records[str(chapters[0]["title"])]["status"], "present")
        self.assertEqual(records[str(chapters[1]["title"])], {"status": "missing"})

    def test_build_manifest_is_source_free_when_inventory_is_complete(self):
        manifest = build_manifest(fetcher=self._fetcher)
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["candidate_id"], CANDIDATE_ID)
        self.assertEqual(len(manifest["chapters"]), 34)
        self.assertEqual(manifest["inventory_summary"]["missing_chapter_count"], 0)
        self.assertTrue(manifest["capture_scope"]["complete_chapter_revision_inventory_frozen"])
        serialized = repr(manifest)
        self.assertNotIn("wikitext", serialized)
        self.assertNotIn("source prose", serialized)
        self.assertEqual(len(validate_manifest(manifest)), 34)

    def test_missing_advertised_chapter_is_preserved_as_a_blocker(self):
        manifest = build_manifest(fetcher=self._missing_last)
        self.assertEqual(manifest["inventory_summary"]["present_chapter_count"], 33)
        self.assertEqual(manifest["inventory_summary"]["missing_chapter_count"], 1)
        self.assertEqual(manifest["inventory_summary"]["missing_titles"], ["Блистающий мир (Грин)/Часть III/Глава VII"])
        self.assertFalse(manifest["capture_scope"]["complete_chapter_revision_inventory_frozen"])
        identities = validate_manifest(manifest)
        self.assertEqual(len(identities), 33)
        self.assertNotIn("revision_id", manifest["chapters"][-1])

    def test_build_manifest_fails_closed_on_query_or_identity_drift(self):
        def omitted_title(chapters):
            records = self._fetcher(chapters)
            records.pop(str(expected_chapters()[-1]["title"]))
            return records
        with self.assertRaisesRegex(ValueError, "chapter inventory mismatch"):
            build_manifest(fetcher=omitted_title)

        def duplicate_revision(chapters):
            records = self._fetcher(chapters)
            titles = list(records)
            records[titles[1]]["revision_id"] = records[titles[0]]["revision_id"]
            return records
        with self.assertRaisesRegex(ValueError, "duplicate revision id"):
            build_manifest(fetcher=duplicate_revision)

    def test_validate_manifest_fails_closed_on_chapter_order_drift(self):
        manifest = build_manifest(fetcher=self._missing_last)
        manifest["chapters"][0]["title"] = "wrong title"
        with self.assertRaisesRegex(ValueError, "chapter identity drift"):
            validate_manifest(manifest)

    def test_replay_verifies_present_revisions_without_returning_prose(self):
        manifest = build_manifest(fetcher=self._missing_last)

        def replay_fetcher(identities):
            rows = tuple(identities)
            self.assertEqual(len(rows), 33)
            self.assertEqual(rows[0]["revision_id"], 6_000_001)
            return {str(row["title"]): "source prose" for row in rows}

        receipt = replay_manifest(manifest, fetcher=replay_fetcher)
        self.assertEqual(receipt, {
            "verified": True,
            "candidate_id": CANDIDATE_ID,
            "verified_present_chapter_count": 33,
            "missing_advertised_chapter_count": 1,
            "complete_chapter_revision_inventory_frozen": False,
            "source_text_committed": False,
        })
        self.assertNotIn("source prose", repr(receipt))


if __name__ == "__main__":
    unittest.main()
