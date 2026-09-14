import copy
from hashlib import sha256
import unittest

from scriptorium.resurrection_freeze import (
    MANIFEST_VERSION,
    PART_CHAPTER_COUNTS,
    build_manifest,
    expected_chapters,
    extract_resurrection_body,
    replay_manifest,
)


class ResurrectionFreezeTests(unittest.TestCase):
    def _synthetic_records(self):
        records = {}
        for row in expected_chapters():
            body = (f"Глава {row['ordinal']}. " + "слово " * 420).strip()
            wikitext = f'<div class="text">{body}</div>'
            records[row["title"]] = {
                "revision_id": 7_000_000 + row["ordinal"],
                "timestamp": f"2026-01-{((row['ordinal'] - 1) % 28) + 1:02d}T00:00:00Z",
                "mediawiki_sha1": sha256(f"mw-{row['ordinal']}".encode()).hexdigest()[:40],
                "wikitext": wikitext,
            }
        return records

    def test_expected_inventory_is_exactly_129_unique_chapters(self):
        chapters = expected_chapters()
        self.assertEqual(PART_CHAPTER_COUNTS, (59, 42, 28))
        self.assertEqual(len(chapters), 129)
        self.assertEqual(len({row["title"] for row in chapters}), 129)
        self.assertEqual(
            chapters[0]["title"],
            "Воскресение (Толстой)/Часть I/Глава I",
        )
        self.assertEqual(
            chapters[-1]["title"],
            "Воскресение (Толстой)/Часть III/Глава XXVIII",
        )

    def test_extractor_handles_observed_plain_and_multi_div_page_shapes(self):
        plain = """{{Отексте
|АВТОР=[[Лев Николаевич Толстой]]
|НАЗВАНИЕ=[[Воскресение (Толстой)|Воскресение]]
|ЧАСТЬ= Часть первая. Глава II
}}
__NOEDITSECTION__
=== II ===
Первый абзац.

Второй абзац.
[[Категория:Воскресение (Толстой)|1_02]]
"""
        self.assertEqual(
            extract_resurrection_body(plain),
            "Первый абзац.\n\nВторой абзац.",
        )

        multi = """{{Отексте|ЧАСТЬ=Часть первая. Глава I}}
{| | <div class="indent">Эпиграф.</div> |}
=== I ===
<div class="indent">Первый абзац.\n\nВторой абзац.</div>
[[Категория:Воскресение (Толстой)|1_01]]
"""
        self.assertEqual(
            extract_resurrection_body(multi),
            "Эпиграф.\n\nПервый абзац.\n\nВторой абзац.",
        )

    def test_manifest_is_source_free_and_replay_uses_exact_source_identities(self):
        records = self._synthetic_records()
        manifest = build_manifest(fetcher=lambda chapters: records)
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["candidate_id"], "tolstoy-resurrection-ru")
        self.assertNotIn("chapters", manifest)
        self.assertIs(manifest["composition"]["source_text_committed"], False)
        self.assertGreaterEqual(
            manifest["composite_identity"]["character_count_including_spaces"],
            300_000,
        )

        encoding = manifest["chapter_identity_encoding"]
        self.assertEqual(encoding["chapter_count"], 129)
        self.assertEqual(len(encoding["revision_ids"]), 129)
        self.assertEqual(len(encoding["revision_timestamps"]), 129)
        self.assertEqual(len(encoding["mediawiki_sha1_hex_concat"]), 129 * 40)
        forbidden = {"body", "content", "prose", "source_text", "text", "wikitext"}
        self.assertTrue(forbidden.isdisjoint(manifest))
        self.assertTrue(forbidden.isdisjoint(encoding))

        replay_records = {title: record["wikitext"] for title, record in records.items()}
        observed_identities = []

        def replay_fetcher(identities):
            observed_identities.extend(identities)
            return replay_records

        receipt = replay_manifest(manifest, fetcher=replay_fetcher)
        self.assertEqual(len(observed_identities), 129)
        first = observed_identities[0]
        source = records[first["title"]]
        self.assertEqual(first["revision_id"], source["revision_id"])
        self.assertEqual(first["revision_timestamp"], source["timestamp"])
        self.assertEqual(first["mediawiki_sha1"], source["mediawiki_sha1"])
        self.assertEqual(receipt["chapter_count"], 129)
        self.assertIs(receipt["source_text_included"], False)
        self.assertEqual(receipt["fantlab_source_edition_match"], "unknown")
        self.assertIs(receipt["m2_parity_admissible"], False)
        self.assertEqual(receipt["composite_identity"], manifest["composite_identity"])

    def test_replay_fails_closed_on_source_and_composite_contract_drift(self):
        records = self._synthetic_records()
        manifest = build_manifest(fetcher=lambda chapters: records)
        replay_records = {title: record["wikitext"] for title, record in records.items()}

        changed = copy.deepcopy(manifest)
        changed["chapter_identity_encoding"]["chapter_count"] = 128
        with self.assertRaisesRegex(ValueError, "packed chapter count drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["chapter_identity_encoding"]["mediawiki_sha1_hex_concat"] = "0"
        with self.assertRaisesRegex(ValueError, "mediawiki_sha1 length"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["composite_identity"]["raw_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "raw_sha256"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["composition"]["source_text_committed"] = True
        with self.assertRaisesRegex(ValueError, "source-text boundary drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)


if __name__ == "__main__":
    unittest.main()
