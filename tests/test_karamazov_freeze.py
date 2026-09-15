import copy
from hashlib import sha256
import unittest

from scriptorium.karamazov_freeze import (
    BOOK_CHAPTER_COUNTS,
    EXTRACTION_PROFILE,
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
        self.assertEqual(segments[1]["title"], "Братья Карамазовы (Достоевский)/От автора")
        self.assertEqual(segments[-1]["title"], "Братья Карамазовы (Достоевский)/Эпилог/III")
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
            "Посвящается Анне Григорьевне Достоевской\n\n"
            "Строка эпиграфа.\n\nИсточник эпиграфа",
        )

    def test_extractor_accepts_observed_poem1_shapes_and_numeric_indent_only(self):
        source = """{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}
<onlyinclude>Перед вставкой.
{{Poem1||<poem>
Первая строка
{{indent|3}}Вторая строка
</poem>|}}
Середина.
{{poem1||Короткая строка без poem-тега.|}}
После вставки.</onlyinclude>
"""
        self.assertEqual(
            extract_karamazov_body(source, kind="book_chapter"),
            "Перед вставкой. Первая строка Вторая строка "
            "Середина. Короткая строка без poem-тега. После вставки.",
        )

        titled = source.replace("{{Poem1||<poem>", "{{Poem1|Заголовок|<poem>", 1)
        with self.assertRaisesRegex(ValueError, "unsupported Poem1 argument shape"):
            extract_karamazov_body(titled, kind="book_chapter")

        nested = source.replace(
            "{{poem1||Короткая строка без poem-тега.|}}",
            "{{poem1||Текст {{lang|ru|вложенный}}.|}}",
        )
        with self.assertRaisesRegex(ValueError, "nested template"):
            extract_karamazov_body(nested, kind="book_chapter")

        textual_indent = source.replace("{{indent|3}}", "{{indent|ступень}}", 1)
        with self.assertRaisesRegex(ValueError, "unsupported Poem1 Indent argument shape"):
            extract_karamazov_body(textual_indent, kind="book_chapter")

        inline_indent = source.replace("{{indent|3}}Вторая", "префикс {{indent|3}}Вторая", 1)
        with self.assertRaisesRegex(ValueError, "must be at line start"):
            extract_karamazov_body(inline_indent, kind="book_chapter")

        malformed = source.replace("</poem>|}}", "|}}", 1)
        with self.assertRaisesRegex(ValueError, "malformed Poem1 poem-tag shape"):
            extract_karamazov_body(malformed, kind="book_chapter")

    def test_extractor_renders_only_unambiguous_long_form_typo_corrections(self):
        source = """{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}
<onlyinclude>До исправления.
{{Опечатка|ошыбка|ошибка|О1}}
После исправления.</onlyinclude>
"""
        self.assertEqual(
            extract_karamazov_body(source, kind="book_chapter"),
            "До исправления. ошибка После исправления.",
        )

        short = source.replace("{{Опечатка|ошыбка|ошибка|О1}}", "{{Опечатка|ошибка|О1}}")
        with self.assertRaisesRegex(ValueError, "unsupported Wikisource typo argument shape"):
            extract_karamazov_body(short, kind="book_chapter")

        unknown_class = source.replace("|О1}}", "|комментарий}}")
        with self.assertRaisesRegex(ValueError, "unsupported Wikisource typo correction class"):
            extract_karamazov_body(unknown_class, kind="book_chapter")

        nested = source.replace("|ошибка|О1}}", "|{{lang|ru|ошибка}}|О1}}")
        with self.assertRaisesRegex(ValueError, "nested template inside Wikisource typo"):
            extract_karamazov_body(nested, kind="book_chapter")

        linked = source.replace("|ошибка|О1}}", "|[[Ошибка|ошибка]]|О1}}")
        with self.assertRaisesRegex(ValueError, "wikilink inside Wikisource typo"):
            extract_karamazov_body(linked, kind="book_chapter")

    def test_wikisource_editor_notes_are_excluded_with_nested_markup(self):
        source = """{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}
<onlyinclude>Авторский текст до.
{{Примечание ВТ|Редакторский комментарий {{lang-fr|texte}}.}}
Авторский текст после.
{{Примечания ВТ}}</onlyinclude>
"""
        self.assertEqual(
            extract_karamazov_body(source, kind="book_chapter"),
            "Авторский текст до.\n\nАвторский текст после.",
        )

        malformed = source.replace("{{Примечание ВТ|Редакторский", "{{Примечание ВТ}} Редакторский")
        with self.assertRaisesRegex(ValueError, "missing its note argument"):
            extract_karamazov_body(malformed, kind="book_chapter")

    def test_observed_literary_subheadings_preserve_text_and_other_levels_fail_closed(self):
        source = """{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}
<onlyinclude>Начало.
===== ''Подраздел [[Цель|видимая цель]]'' =====
Текст после первого заголовка.
====== Второй подраздел ======
Конец.</onlyinclude>
"""
        self.assertEqual(
            extract_karamazov_body(source, kind="book_chapter"),
            "Начало.\n\nПодраздел видимая цель\n\n"
            "Текст после первого заголовка.\n\nВторой подраздел\n\nКонец.",
        )

        unsupported = source.replace("===== ''Подраздел", "==== ''Подраздел", 1).replace(
            "цель]]'' =====", "цель]]'' ====", 1
        )
        with self.assertRaisesRegex(ValueError, "unsupported literary heading level"):
            extract_karamazov_body(unsupported, kind="book_chapter")

    def test_extractor_handles_onlyinclude_and_styled_indent(self):
        preface = """{{Отексте|АВТОР=[[Фёдор Михайлович Достоевский]]}}
== От автора ==
<onlyinclude>Первый абзац.

Второй абзац.</onlyinclude>
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
<div class='indent' style='text-align:justify'>Первый абзац.

Второй абзац.</div>
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
        self.assertEqual(manifest["composition"]["extraction_profile"], EXTRACTION_PROFILE)
        self.assertEqual(EXTRACTION_PROFILE, "scriptorium-wikisource-karamazov-body-v6")
        self.assertIs(manifest["composition"]["navigation_wrappers_included"], False)
        self.assertIs(manifest["composition"]["wikisource_editor_notes_included"], False)
        self.assertIs(
            manifest["composition"]["wikisource_typo_corrections_render_corrected_text"], True
        )
        self.assertEqual(manifest["composition"]["literary_heading_levels_preserved_as_text"], [5, 6])
        self.assertIs(manifest["composition"]["poem_indent_templates_stripped_as_formatting"], True)
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

    def test_replay_fails_closed_on_inventory_extraction_and_composite_drift(self):
        records = self._synthetic_records()
        manifest = build_manifest(fetcher=lambda segments: records)
        replay_records = {title: record["wikitext"] for title, record in records.items()}

        changed = copy.deepcopy(manifest)
        changed["source_identity_encoding"]["source_segment_count"] = 97
        with self.assertRaisesRegex(ValueError, "source-segment count drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["composition"]["extraction_profile"] = "older-profile"
        with self.assertRaisesRegex(ValueError, "extraction profile"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["composition"]["wikisource_editor_notes_included"] = True
        with self.assertRaisesRegex(ValueError, "editor-note boundary drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["composition"]["wikisource_typo_corrections_render_corrected_text"] = False
        with self.assertRaisesRegex(ValueError, "typo-correction boundary drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["composition"]["literary_heading_levels_preserved_as_text"] = [6]
        with self.assertRaisesRegex(ValueError, "literary-heading boundary drift"):
            replay_manifest(changed, fetcher=lambda identities: replay_records)

        changed = copy.deepcopy(manifest)
        changed["composition"]["poem_indent_templates_stripped_as_formatting"] = False
        with self.assertRaisesRegex(ValueError, "Indent-formatting boundary drift"):
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
