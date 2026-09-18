from __future__ import annotations

import unittest

from scriptorium.klim_samgin_literary_body import (
    COMPOSITE_SEPARATOR,
    _extract_part_literary_body,
    _plain_poem_value,
    _raw_template_spans,
)
from scriptorium.mediawiki_poemx1_content import _parameter_two_value
from scriptorium.mediawiki_template_invocation import find_template_invocations


class KlimSamginLiteraryBodyTests(unittest.TestCase):
    def test_raw_scaffold_span_accepts_cyrillic_named_arguments(self) -> None:
        source = "{{Жизнь Клима Самгина|ЧАСТЬ=1|ПРЕДЫДУЩИЙ=0}}\nПроза"
        spans = _raw_template_spans(source, "Жизнь Клима Самгина")
        self.assertEqual(spans, [(0, source.index("\n"))])

    def test_plain_poem_replacement_revalidates_exact_parameter_two(self) -> None:
        source = "A {{poemx1||Первая строка\nВторая строка}} B"
        observed = find_template_invocations(source, template_name="poemx1")[0]
        _, identity = _parameter_two_value(source, observed)
        value = _plain_poem_value(
            source,
            observed,
            expected_invocation_sha256=observed["invocation_sha256"],
            expected_parameter_2_sha256=identity["sha256"],
        )
        self.assertEqual(value, "Первая строка\nВторая строка")

    def test_plain_poem_replacement_fails_on_identity_drift(self) -> None:
        source = "{{poemx1||Текст}}"
        observed = find_template_invocations(source, template_name="poemx1")[0]
        with self.assertRaisesRegex(ValueError, "parameter-2 identity drift"):
            _plain_poem_value(
                source,
                observed,
                expected_invocation_sha256=observed["invocation_sha256"],
                expected_parameter_2_sha256="0" * 64,
            )

    def test_candidate_scaffold_extraction_preserves_visible_literary_text(self) -> None:
        source = (
            "{{Жизнь Клима Самгина|ЧАСТЬ=1}}\n"
            "=== I ===\n"
            "<center>Грегер и {{Ко}}</center>\n\n"
            "Обычный [[Текст|видимый текст]].<ref>служебная сноска</ref>\n\n"
            "Буквально <nowiki>[[не ссылка]]</nowiki>.\n"
            "[[Категория:Жизнь Клима Самгина (Горький)]]\n"
        )
        source = source.replace(
            "<center>",
            "=== II ===\n=== III ===\n=== IV ===\n=== V ===\n<center>",
        )
        body, surface = _extract_part_literary_body(
            source,
            part=1,
            expected_parent_category_count=1,
        )
        self.assertIn("Грегер и Ко", body)
        self.assertIn("видимый текст", body)
        self.assertIn("[[не ссылка]]", body)
        self.assertNotIn("служебная сноска", body)
        self.assertNotIn("Категория:", body)
        self.assertNotIn("Жизнь Клима Самгина|", body)
        self.assertEqual(surface["heading_count_preserved"], 5)
        self.assertEqual(surface["nowiki_pair_count_preserved"], 1)

    def test_unsupported_template_fails_closed(self) -> None:
        source = (
            "{{Жизнь Клима Самгина}}\n"
            "=== I ===\n=== II ===\n=== III ===\n=== IV ===\n=== V ===\n"
            "Грегер и {{Ко}}. Проза {{Неизвестный}}\n"
            "[[Категория:Жизнь Клима Самгина (Горький)]]"
        )
        with self.assertRaisesRegex(ValueError, "unsupported template syntax"):
            _extract_part_literary_body(source, part=1, expected_parent_category_count=1)

    def test_composition_separator_is_two_newlines(self) -> None:
        self.assertEqual(COMPOSITE_SEPARATOR, "\n\n")
        self.assertEqual(
            COMPOSITE_SEPARATOR.join(["A", "B", "C", "D"]),
            "A\n\nB\n\nC\n\nD",
        )


if __name__ == "__main__":
    unittest.main()
