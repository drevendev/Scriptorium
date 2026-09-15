import copy
from hashlib import sha256
import unittest

from scriptorium.karamazov_freeze import (
    BOOK_CHAPTER_COUNTS,
    MANIFEST_VERSION,
    SOURCE_SEGMENT_COUNT,
    SOURCE_WORK_INDEX_REVISION_ID,
    build_manifest,
    expected_segments,
    extract_index_front_matter,
    extract_karamazov_body,
    replay_manifest,
)


class KaramazovFreezeTests(unittest.TestCase):
    def _synthetic_records(self):
        records = {}
        for row in expected_segments():
            if row["kind"] == "front_matter":
                wikitext = """{{Отексте
|АВТОР=[[Фёдор Михайлович Достоевский]]
|ИСТОЧНИК={{книга|заглавие=Собрание сочинений}}
}}__NOEDITSECTION__
{{right|''Посвящается Анне Григорьевне Достоевской''}}
{{эпиграф2|Строка эпиграфа.|Источник эпиграфа|60}}
== Оглавление ==
* [[Навигационная ссылка]]
"""
                revision_id = SOURCE_WORK_INDEX_REVISION_ID
            elif row["kind"] == "author_preface":
                body = ("От автора. " + "слово " * 600).strip()
                wikitext = (
                    "{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}\n"
                    "== От автора ==\n"
                    f"<onlyinclude>{body}</onlyinclude>\n"
                    "[[Категория:Братья Карамазовы (Достоевский)]]"
                )
                revision_id = 8_000_000 + row["ordinal"]
            else:
                body = (f"Сегмент {row['ordinal']}. " + "слово " * 600).strip()
                wikitext = (
                    "{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}"
                    "__NOTOC____NOEDITSECTION__\n"
                    "<center>''Заголовок''</center>\n"
                    f"== {row['ordinal']} ==\n"
                    f"<div class='indent' style='text-align:justify'>{body}</div>"
                )
                revision_id = 8_000_000 + row["ordinal"]
            records[row["title"]] = {
                "revision_id": revision_id,
                "timestamp": f"2026-01-{((row['ordinal'] - 1) % 28) + 1:02d}T00:00:00Z",
                "mediawiki_sha1": sha256(f"mw-{row['ordinal']}".encode()).hexdigest()[:40],
                "wikitext": wikitext,
            }
        return records

    def test_expected_inventory_is_exactly_98_text_bearing_segments(self):
        segments = expected_segments()
        self.assertEqual(BOOK_CHAPTER_COUNTS, (5, 8, 11, 7, 7, 3, 4, 8, 9, 7, 10, 14))
        self.assertEqual(sum(BOOK_CHAPTER_COUNTS), 93)
        self.assertEqual(SOURCE_SEGMENT_COUNT, 98)
        self.assertEqual(len(segments), 98)
        self.assertEqual(len({row["title"] for row in segments}), 98)
        self.assertEqual(segments[0]["title"], "Братья Карамазовы (Достоевский)")
        self.assertEqual(segments[0]["kind"], "front_matter")
        self.assertEqual(
            segments[1]["title"], "Братья Карамазовы (Достоевский)/От автора"
        )
        self.assertEqual(
            segments[-1]["title"], "Братья Карамазовы (Достоевский)/Эпилог/III"
        )
        titles = {row["title"] for row in segments}
        self.assertNotIn("Братья Карамазовы (Достоевский)/Книга первая", titles)
        self.assertNotIn("Братья Карамазовы (Достоевский)/Эпилог", titles)

    def test_index_front_matter_handles_nested_source_template_and_stops_before_toc(self):
        source = """{{Отексте
|АВТОР=[[Фёдор Михайлович Достоевский]]
|ИСТОЧНИК={{книга|заглавие=Собрание сочинений|том=9-10}}
}}__NOEDITSECTION__
{{right|''Посвящается Анне Григорьевне Достоевской''}}
{{эпиграф2|Строка эпиграфа.|Источник эпиграфа|60}}
== Оглавление ==
* [[Братья Карамазовы (Достоевский)/От автора|От автора]]
"""
        self.assertEqual(
            extract_index_front_matter(source),
            "Посвящается Анне Григорьевне Достоевской\n\nСтрока эпиграфа.\n\nИсточник эпиграфа",
        )

    def test_extractor_handles_onlyinclude_and_styled_indent_shapes(self):
        preface = """{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}
== От автора ==
<onlyinclude>Первый абзац.\n\nВторой абзац.</onlyinclude>
[[Категория:Братья Карамазовы (Достоевский)]]
"""
        self.assertEqual(
            extract_karamazov_body(preface, kind="author_preface"),
            "Первый абзац.\n\nВторой абзац.",
        )

        styled = """{{Отексте|ЧАСТЬ=Эпилог}}
__NOTOC____NOEDITSECTION__
<center>''Эпилог''</center>
== I ==
<div class='indent' style='text-align:justify'>Первый абзац.\n\nВторой абзац.</div>
"""
        self.assertEqual(
            extract_karamazov_body(styled, kind="epilogue_chapter"),
            "Первый абзац.\n\nВторой абзац.",
        )

    def test_manifest_is_source_free_and_replay_uses_exact_source_identities(self):
        records = self._synthetic_records()
        manifest = build_manifest(fetcher=lambda segments: records)
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["candidate_id"], "dostoevsky-brothers-karamazov-ru")
        self.assertEqual(
            manifest["composition"]["extraction_profile"],
            "scriptorium-wikisource-karamazov-body-v1",
        )
        self.assertIs(manifest["composition"]["navigation_wrappers_included"], False)
        self.assertIs(manifest["composition"]["source_text_committed"], False)
        self.assertGreaterEqual(
            manifest["composite_identity"]["character_count_including_spaces"], 300_000
        )

        encoding = manifest["source_identity_encoding"]
        self.assertEqual(encoding["source_segment_count"], 98)
        self.assertEqual(len(encoding["revision_ids"]), 98)
        self.assertEqual(len(encoding["revision_timestamps"]), 98)
        self.assertEqual(len(encoding["mediawiki_sha1_hex_concat"]), 98 * 40)
        forbidden = {"body", "content", "prose", "source_text", "text", "wikitext"}
        self.assertTrue(forbidden.isdisjoint(manifest))
        self.assertTrue(forbidden.isdisjoint(encoding))

        replay_records = {title: record["wikitext"] for title, record in records.items()}
        observed_identities = []

        def replay_fetcher(identities):
            observed_identities.extend(identities)
            return replay_records

        receipt = replay_manifest(manifest, fetcher=replay_fetcher)
        self.assertEqual(len(observed_identities), 98)
        first = observed_identities[0]
        source = records[first["title"]]
        self.assertEqual(first["revision_id"], source["revision_id"])
        self.assertEqual(first["revision_timestamp"], source["timestamp"])
        self.assertEqual(first["mediawiki_sha1"], source["mediawiki_sha1"])
        self.assertEqual(receipt["source_segment_count"], 98)
        self.assertIs(receipt["source_text_included"], False)
        self.assertIs(receipt["diagnostic_comparison_admissible"], False)
        self.assertEqual(receipt["fantlab_source_edition_match"], "unknown")
        self.assertIs(receipt["m2_parity_admissible"], False)
        self.assertEqual(receipt["composite_identity"], manifest["composite_identity"])

    def test_replay_fails_closed_on_inventory_and_composite_contract_drift(self):
        records = self._synthetic_records()
        manifest = build_manifest(fetcher=lambda segments: records)
        replay_records = {title: record["wikitext"] for title, record in records.items()}

        changed = copy.deepcopy(manifest)
        changed["source_identity_encoding"]["source_segment_count"] = 97
        with self.assertRaisesRegex(ValueError, "source-segment count drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["source_identity_encoding"]["mediawiki_sha1_hex_concat"] = "0"
        with self.assertRaisesRegex(ValueError, "mediawiki_sha1 length"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["source_identity_encoding"]["revision_ids"][0] += 1
        with self.assertRaisesRegex(ValueError, "work-index revision drift"):
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
