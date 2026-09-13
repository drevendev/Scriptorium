import base64
import json
from pathlib import Path
import re
import unittest

from scriptorium.wikisource_freeze import (
    PART_CHAPTER_COUNTS,
    expected_chapters,
    extract_transcription_body,
    roman,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
REVISION_MANIFEST = (
    REPO_ROOT
    / "corpus"
    / "candidates"
    / "source-edition-traces"
    / "tolstoy-anna-karenina-ru.revisions.json"
)


class WikisourceFreezeTests(unittest.TestCase):
    def test_expected_inventory_is_exactly_239_unique_chapters(self):
        chapters = expected_chapters()
        self.assertEqual(PART_CHAPTER_COUNTS, (34, 35, 32, 23, 33, 32, 31, 19))
        self.assertEqual(len(chapters), 239)
        self.assertEqual(len({row["title"] for row in chapters}), 239)
        self.assertEqual(
            chapters[0]["title"],
            "Анна Каренина (Толстой)/Часть I/Глава I",
        )
        self.assertEqual(
            chapters[-1]["title"],
            "Анна Каренина (Толстой)/Часть VIII/Глава XIX",
        )

    def test_roman_contract(self):
        self.assertEqual(roman(1), "I")
        self.assertEqual(roman(4), "IV")
        self.assertEqual(roman(8), "VIII")
        self.assertEqual(roman(34), "XXXIV")
        with self.assertRaises(ValueError):
            roman(0)

    def test_extracts_observed_text_indent_and_inline_template_variants(self):
        source = '''<noinclude>metadata</noinclude>
<div class="indent">
{{СодержаниеБН}}
Первая
строка с {{lang|it|dolce vita}} и [[Цель|меткой]].<ref>Сноска.</ref>

Второй абзац с [https://example.invalid подписью] и ''курсивом''. {{poemx1|| {{lang|de|Himmlisch}}|}}
{{right|А. Каренин.}}
<center>{{Razr|Конец}}</center>
=== Примечания ===
<references />
</div>
<noinclude>navigation</noinclude>'''
        self.assertEqual(
            extract_transcription_body(source),
            "Первая строка с dolce vita и меткой.\n\n"
            "Второй абзац с подписью и курсивом. Himmlisch А. Каренин. Конец",
        )

    def test_unknown_template_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported template"):
            extract_transcription_body(
                '<div class="text">Текст {{Неизвестный|аргумент}}.</div>'
            )

    def test_missing_or_multiple_text_bodies_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            extract_transcription_body("Текст без контейнера")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            extract_transcription_body(
                '<div class="text">Один.</div><div class="text">Два.</div>'
            )

    def test_committed_revision_manifest_is_complete_source_free_and_decodable(self):
        manifest = json.loads(REVISION_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(
            set(manifest),
            {
                "bibliographic_source",
                "candidate_id",
                "chapter_identity_encoding",
                "composite_identity",
                "composition",
                "legal_basis",
                "manifest_version",
                "provider",
                "source_work_index_revision_id",
                "source_work_url",
            },
        )
        self.assertEqual(
            manifest["manifest_version"],
            "scriptorium-source-revision-packed-manifest-v1",
        )
        self.assertEqual(manifest["candidate_id"], "tolstoy-anna-karenina-ru")
        self.assertEqual(manifest["composition"]["part_chapter_counts"], list(PART_CHAPTER_COUNTS))
        self.assertIs(manifest["composition"]["source_text_committed"], False)

        identities = manifest["chapter_identity_encoding"]
        revision_ids = identities["revision_ids"]
        offsets = identities["revision_timestamp_offsets_seconds"]
        self.assertEqual(len(revision_ids), 239)
        self.assertEqual(len(set(revision_ids)), 239)
        self.assertEqual(len(offsets), 239)
        self.assertEqual(revision_ids[0], 4929732)
        self.assertEqual(revision_ids[10], 4929741)
        self.assertEqual(revision_ids[-1], 4929969)

        width = identities["mediawiki_sha1_base64_no_padding_fixed_width"]
        packed = identities["mediawiki_sha1_base64_no_padding_concat"]
        self.assertEqual(width, 27)
        self.assertEqual(len(packed), width * 239)
        for offset in range(0, len(packed), width):
            digest = base64.b64decode(packed[offset : offset + width] + "=")
            self.assertEqual(len(digest), 20)

        composite = manifest["composite_identity"]
        self.assertEqual(composite["chapter_count"], 239)
        self.assertGreaterEqual(composite["character_count_including_spaces"], 300_000)
        self.assertEqual(composite["character_count_including_spaces"], 1_705_605)
        self.assertEqual(composite["normalized_character_count_including_spaces"], 1_705_605)
        self.assertEqual(composite["normalization_profile"], "scriptorium-text-v1")
        for key in ("raw_sha256", "normalized_sha256"):
            self.assertRegex(composite[key], re.compile(r"^[0-9a-f]{64}$"))
            self.assertEqual(
                composite[key],
                "1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205",
            )

        forbidden_payload_keys = {"body", "content", "prose", "source_text", "text", "wikitext"}
        self.assertTrue(forbidden_payload_keys.isdisjoint(manifest))
        self.assertTrue(forbidden_payload_keys.isdisjoint(identities))
        self.assertTrue(forbidden_payload_keys.isdisjoint(composite))


if __name__ == "__main__":
    unittest.main()
