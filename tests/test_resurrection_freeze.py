import copy
from hashlib import sha256
import unittest

from scriptorium.resurrection_freeze import (
    PACKED_MANIFEST_VERSION,
    PART_CHAPTER_COUNTS,
    build_manifest,
    expected_chapters,
    extract_resurrection_body,
    pack_manifest,
    replay_manifest,
    unpack_manifest,
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

    def test_packed_manifest_is_source_free_and_round_trips_every_identity(self):
        records = self._synthetic_records()
        expanded = build_manifest(fetcher=lambda chapters: records)
        packed = pack_manifest(expanded)
        self.assertEqual(packed["manifest_version"], PACKED_MANIFEST_VERSION)
        self.assertEqual(packed["candidate_id"], "tolstoy-resurrection-ru")
        self.assertNotIn("chapters", packed)
        encoding = packed["chapter_identity_encoding"]
        self.assertEqual(encoding["chapter_count"], 129)
        self.assertEqual(len(encoding["revision_ids"]), 129)
        self.assertEqual(len(encoding["revision_timestamps"]), 129)
        self.assertEqual(len(encoding["mediawiki_sha1_hex_concat"]), 129 * 40)
        self.assertEqual(len(encoding["wikitext_sha256_hex_concat"]), 129 * 64)
        self.assertEqual(len(encoding["extracted_sha256_hex_concat"]), 129 * 64)
        self.assertEqual(len(encoding["extracted_character_counts"]), 129)
        self.assertIs(packed["composition"]["source_text_committed"], False)
        self.assertGreaterEqual(
            packed["composite_identity"]["character_count_including_spaces"],
            300_000,
        )
        forbidden = {"body", "content", "prose", "source_text", "text", "wikitext"}
        self.assertTrue(forbidden.isdisjoint(packed))
        self.assertTrue(forbidden.isdisjoint(encoding))

        round_tripped = unpack_manifest(packed)
        self.assertEqual(round_tripped, expanded)
        replay_records = {title: record["wikitext"] for title, record in records.items()}
        receipt = replay_manifest(packed, fetcher=lambda identities: replay_records)
        self.assertEqual(receipt["chapter_count"], 129)
        self.assertIs(receipt["source_text_included"], False)
        self.assertEqual(receipt["fantlab_source_edition_match"], "unknown")
        self.assertIs(receipt["m2_parity_admissible"], False)
        self.assertEqual(receipt["composite_identity"], expanded["composite_identity"])

        changed = copy.deepcopy(packed)
        digest = changed["chapter_identity_encoding"]["extracted_sha256_hex_concat"]
        changed["chapter_identity_encoding"]["extracted_sha256_hex_concat"] = (
            digest[: 50 * 64] + "0" * 64 + digest[51 * 64 :]
        )
        with self.assertRaisesRegex(ValueError, "extracted SHA-256 drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

    def test_replay_fails_closed_on_contract_drift(self):
        records = self._synthetic_records()
        expanded = build_manifest(fetcher=lambda chapters: records)
        packed = pack_manifest(expanded)
        replay_records = {title: record["wikitext"] for title, record in records.items()}

        changed = copy.deepcopy(packed)
        changed["chapter_identity_encoding"]["chapter_count"] = 128
        with self.assertRaisesRegex(ValueError, "packed chapter count drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(packed)
        changed["composite_identity"]["raw_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "raw_sha256"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(packed)
        changed["composition"]["source_text_committed"] = True
        with self.assertRaisesRegex(ValueError, "source-text boundary drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)


if __name__ == "__main__":
    unittest.main()
