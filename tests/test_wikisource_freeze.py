import unittest

from scriptorium.wikisource_freeze import (
    PART_CHAPTER_COUNTS,
    expected_chapters,
    extract_transcription_body,
    roman,
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

    def test_extracts_only_text_body_and_normalizes_wiki_markup(self):
        source = '''<noinclude>metadata</noinclude>
<div class="text">
{{СодержаниеБН}}
Первая
строка с {{lang|it|dolce vita}} и [[Цель|меткой]].<ref>Сноска.</ref>

Второй абзац с [https://example.invalid подписью] и ''курсивом''.
</div>
=== Примечания ===
<references />'''
        self.assertEqual(
            extract_transcription_body(source),
            "Первая строка с dolce vita и меткой.\n\n"
            "Второй абзац с подписью и курсивом.",
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


if __name__ == "__main__":
    unittest.main()
