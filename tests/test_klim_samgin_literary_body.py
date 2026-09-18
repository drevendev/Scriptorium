from __future__ import annotations

import unittest

from scriptorium.klim_samgin_literary_body import (
    COMPOSITION_SEPARATOR,
    _identity,
    _protect_encoded_angle_spans,
    _protect_literal_line_openers,
    _protect_nowiki,
    _replace_named_template,
    _replace_spans,
    _restore_tokens,
    _strip_trailing_category,
)
from scriptorium.text import NORMALIZATION_PROFILE


class KlimSamginLiteraryBodyHelpersTests(unittest.TestCase):
    def test_replace_spans_applies_original_offsets_right_to_left(self) -> None:
        source = "alpha {{x}} beta {{y}} omega"
        observed = _replace_spans(
            source,
            [(6, 11, "ONE"), (17, 22, "TWO")],
        )
        self.assertEqual(observed, "alpha ONE beta TWO omega")

    def test_replace_spans_rejects_overlap(self) -> None:
        with self.assertRaisesRegex(ValueError, "overlapping"):
            _replace_spans("abcdefghij", [(1, 6, "x"), (5, 9, "y")])

    def test_named_template_replacement_is_balanced(self) -> None:
        source = "left {{Ко}} right"
        self.assertEqual(
            _replace_named_template(source, "Ко", expected=1, replacement="Ко"),
            "left Ко right",
        )

    def test_ko_arguments_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "arguments"):
            _replace_named_template("{{Ко|unexpected}}", "Ко", expected=1, replacement="Ко")

    def test_nowiki_is_protected_from_later_markup_interpretation(self) -> None:
        source, protected = _protect_nowiki(
            "before <nowiki>''[[literal]]''</nowiki> after",
            expected_tag_count=2,
        )
        self.assertNotIn("[[literal]]", source)
        self.assertEqual(len(protected), 1)
        self.assertEqual(
            _restore_tokens(source, protected, label="nowiki"),
            "before <nowiki>''[[literal]]''</nowiki> after".replace("<nowiki>", "").replace("</nowiki>", ""),
        )

    def test_multiline_nowiki_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "multiline"):
            _protect_nowiki("<nowiki>a\nb</nowiki>", expected_tag_count=2)

    def test_entity_encoded_angle_literal_is_protected_as_visible_text(self) -> None:
        source, protected = _protect_encoded_angle_spans("before &lt;слово&gt; after")
        self.assertNotIn("&lt;", source)
        self.assertEqual(len(protected), 1)
        self.assertEqual(_restore_tokens(source, protected, label="encoded-angle"), "before <слово> after")
        untouched, protected_tag = _protect_encoded_angle_spans("&lt;ref&gt;")
        self.assertEqual(untouched, "&lt;ref&gt;")
        self.assertEqual(protected_tag, [])

    def test_literal_line_openers_are_protected_but_table_delimiters_fail(self) -> None:
        source, protected = _protect_literal_line_openers("plain\n| literal\n! emphatic")
        self.assertNotIn("\n|", source)
        self.assertNotIn("\n!", source)
        self.assertEqual(len(protected), 2)
        self.assertEqual(
            _restore_tokens(source, protected, label="line-opener"),
            "plain\n| literal\n! emphatic",
        )
        for table in ("{| class=x\n| cell\n|}", "|-\ncell", "|}\n"):
            with self.assertRaisesRegex(ValueError, "table delimiter"):
                _protect_literal_line_openers(table)

    def test_trailing_category_is_removed_only_at_tail(self) -> None:
        source = "literary\n\n[[Категория:Example]]\n"
        self.assertEqual(_strip_trailing_category(source, expected_count=1), "literary")
        with self.assertRaisesRegex(ValueError, "after trailing"):
            _strip_trailing_category(
                "literary\n[[Категория:Example]]\nnot-tail\n",
                expected_count=1,
            )

    def test_identity_uses_public_normalization_profile(self) -> None:
        value = "one\r\ntwo"
        identity = _identity(value)
        self.assertEqual(identity["normalization_profile"], NORMALIZATION_PROFILE)
        self.assertEqual(identity["character_count_including_spaces"], len(value))
        self.assertEqual(len(identity["raw_sha256"]), 64)
        self.assertEqual(len(identity["normalized_sha256"]), 64)

    def test_composition_separator_is_explicit_two_newlines(self) -> None:
        self.assertEqual(COMPOSITION_SEPARATOR, "\n\n")


if __name__ == "__main__":
    unittest.main()
