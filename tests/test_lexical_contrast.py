"""Executable source-free lexical-extension regressions (no book text fixtures)."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium import cli
from scriptorium.lexical_contrast import (
    PROFILE, build_lexical_contrast, render_lexical_contrast,
)


def contrast(left: str, right: str, **kwargs):
    return build_lexical_contrast(
        left, right, left_edition_id="edition-left",
        right_edition_id="edition-right", **kwargs
    )


class LexicalContrastTests(unittest.TestCase):
    def test_opposing_dominant_forms_and_no_word_leakage(self):
        left = "кот " * 8 + "пёс " * 2
        right = "КОТ " + "пёс " * 9
        result = contrast(left, right)
        self.assertEqual(result["profile"], PROFILE)
        self.assertEqual(result["status"], "COMPARABLE")
        self.assertEqual(result["compatibility_status"], "extension")
        self.assertEqual(result["aggregate"]["eligible_form_count"], 2)
        self.assertEqual(result["aggregate"]["left_dominant_form_count"], 1)
        self.assertEqual(result["aggregate"]["right_dominant_form_count"], 1)
        self.assertEqual(result["aggregate"]["balanced_form_count"], 0)
        self.assertEqual(result["aggregate"]["left_dominant_token_share_percent"], 80.0)
        self.assertEqual(result["aggregate"]["right_dominant_token_share_percent"], 90.0)
        self.assertFalse(result["public_release_ready"])
        self.assertEqual(result["corpus_admission"], "NOT_VERIFIED")
        serialized = render_lexical_contrast(result)
        for forbidden in ("кот", "пёс", "КОТ"):
            self.assertNotIn(forbidden, serialized)
        self.assertNotIn(left.strip(), render_lexical_contrast(result, "markdown"))
        self.assertIsNone(result["method"]["dictionary_dependency"])

    def test_identical_normalized_text_has_exact_zero_divergence(self):
        result = contrast("Ёж и ёж.", "Ёж и ёж.")
        self.assertEqual(result["status"], "IDENTICAL_NORMALIZED_TEXT")
        self.assertEqual(result["aggregate"]["jensen_shannon_divergence_bits"], 0)
        self.assertEqual(result["aggregate"]["left_dominant_form_count"], 0)
        self.assertEqual(result["aggregate"]["right_dominant_form_count"], 0)
        self.assertEqual(result["left"]["normalized_sha256"], result["right"]["normalized_sha256"])

    def test_equal_distribution_different_lengths_has_zero_empirical_js(self):
        result = contrast("кот " * 5 + "пёс " * 5, "кот " * 50 + "пёс " * 50)
        self.assertEqual(result["status"], "COMPARABLE")
        self.assertEqual(result["aggregate"]["jensen_shannon_divergence_bits"], 0)
        self.assertEqual(result["aggregate"]["balanced_form_count"], 2)
        self.assertTrue(result["length_imbalance_warning"])
        self.assertEqual(result["length_ratio_max_over_min"], 10)

    def test_disjoint_vocabulary_has_one_bit_divergence(self):
        result = contrast("кот " * 5, "пёс " * 5)
        self.assertEqual(result["aggregate"]["jensen_shannon_divergence_bits"], 1)
        self.assertEqual(result["aggregate"]["left_dominant_form_count"], 1)
        self.assertEqual(result["aggregate"]["right_dominant_form_count"], 1)

    def test_rare_forms_removed_from_dominance_but_not_js(self):
        result = contrast("кот " * 4, "пёс " * 4)
        self.assertEqual(result["aggregate"]["eligible_form_count"], 0)
        self.assertEqual(result["aggregate"]["excluded_rare_form_count"], 2)
        self.assertEqual(result["aggregate"]["jensen_shannon_divergence_bits"], 1)
        self.assertEqual(result["aggregate"]["left_dominant_token_share_percent"], 0)

    def test_empty_and_zero_word_text_returns_not_run_not_zero(self):
        for a, b in (("", "кот"), ("...", "кот"), ("кот", " ")):
            with self.subTest(a=a, b=b):
                result = contrast(a, b)
                self.assertEqual(result["status"], "NOT_RUN_EMPTY")
                self.assertIsNone(result["aggregate"])

    def test_language_and_original_work_mismatches_fail_closed(self):
        lang = contrast("кот " * 10, "пёс " * 10, right_language="en")
        self.assertEqual(lang["status"], "INCOMPARABLE_LANGUAGE")
        self.assertIsNone(lang["aggregate"])
        lineage = contrast("кот " * 10, "пёс " * 10,
                           left_original_work_id="book-a", right_original_work_id="book-b",
                           translation_pair=True)
        self.assertEqual(lineage["status"], "INCOMPARABLE_TRANSLATION_LINEAGE")
        self.assertIsNone(lineage["aggregate"])
        absent = contrast("кот", "пёс", translation_pair=True)
        self.assertEqual(absent["status"], "INCOMPARABLE_TRANSLATION_LINEAGE")
        accepted = contrast("кот " * 6, "пёс " * 6,
                            left_original_work_id="same-work",
                            right_original_work_id="same-work",
                            left_translator="Translator A",
                            right_translator="Translator B",
                            translation_pair=True)
        self.assertEqual(accepted["status"], "COMPARABLE")
        self.assertEqual(accepted["left"]["translator"], "Translator A")

    def test_same_edition_cannot_have_conflicting_text(self):
        with self.assertRaisesRegex(ValueError, "one edition"):
            build_lexical_contrast("кот", "пёс", left_edition_id="same",
                                   right_edition_id="same")
        same = build_lexical_contrast("кот", "кот", left_edition_id="same",
                                      right_edition_id="same")
        self.assertEqual(same["status"], "IDENTICAL_NORMALIZED_TEXT")

    def test_unicode_normalization_and_casefold_are_shared_with_vocabulary(self):
        value = contrast("Ёж " * 6, "е\u0308ж " * 6)
        self.assertEqual(value["status"], "COMPARABLE")
        # Different case is preserved by normalized source hashing, while the
        # vocabulary contrast itself uses casefolded NFC lexical identities.
        self.assertEqual(value["aggregate"]["jensen_shannon_divergence_bits"], 0)

    def test_bounded_unverified_fixture_not_corpus_admission(self):
        short = contrast("кот", "пёс")
        self.assertFalse(short["left"]["meets_300000_character_floor"])
        self.assertEqual(short["corpus_admission"], "NOT_VERIFIED")
        threshold = contrast("кот " * 75001, "пёс " * 75001)
        self.assertTrue(threshold["left"]["meets_300000_character_floor"])
        self.assertTrue(threshold["right"]["meets_300000_character_floor"])
        self.assertFalse(threshold["public_release_ready"])

    def test_invalid_metadata_and_nontext_rejected(self):
        for options in ({"left_language": "zz-raw"}, {"left_original_work_id": "bad id"},
                        {"left_translator": "bad\nactor"}):
            with self.subTest(options=options):
                with self.assertRaises(ValueError):
                    contrast("кот", "пёс", **options)
        with self.assertRaises(ValueError):
            contrast(None, "кот")
        with self.assertRaises(ValueError):
            contrast("кот", "пёс", translation_pair="yes")

    def test_private_html_report_escapes_metadata_and_never_embeds_source_words(self):
        result = contrast("кот " * 8 + "пёс " * 2, "пёс " * 9 + "кот",
                          left_translator="<script>alert(1)</script>")
        html = render_lexical_contrast(result, "html")
        self.assertIn("<!doctype html>", html)
        self.assertIn('lang="en"', html)
        self.assertIn("Content-Security-Policy", html)
        self.assertIn('scope="col"', html)
        self.assertIn("Jensen–Shannon divergence", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("<script>", html)
        self.assertNotIn("кот", html)
        self.assertNotIn("пёс", html)
        self.assertIn("nonrepresentative private preview", html)
        self.assertIn("NOT_VERIFIED", html)
        self.assertIn("False", html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)

        unavailable = contrast("кот", "...")
        missing = render_lexical_contrast(unavailable, "html")
        self.assertIn("NOT_RUN_EMPTY", missing)
        self.assertIn("NOT_RUN / INCOMPARABLE", missing)
        self.assertNotIn("0</td><td>bits", missing)
        unbalanced = contrast("кот " * 5, "пёс " * 50)
        self.assertIn("lengths differ by at least 2", render_lexical_contrast(unbalanced, "html"))
        with self.assertRaises(ValueError):
            render_lexical_contrast({"schema_version": "wrong"}, "html")
        with self.assertRaises(ValueError):
            render_lexical_contrast({**result, "aggregate": {}}, "html")

    def test_cli_local_json_markdown_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first, second = root / "left.txt", root / "right.txt"
            first.write_text("кот " * 8 + "пёс " * 2, encoding="utf-8")
            second.write_text("пёс " * 9 + "кот", encoding="utf-8")
            output = root / "summary.json"
            args = ["distinctives", str(first), str(second),
                    "--left-edition", "frozen-left", "--right-edition", "frozen-right",
                    "--output", str(output)]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(args), 0)
            artifact = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(artifact["status"], "COMPARABLE")
            self.assertNotIn("кот", output.read_text(encoding="utf-8"))
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                cli.main(args)
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(cli.main(args[:-2] + ["--format", "markdown"]), 0)
            self.assertIn("Jensen–Shannon", stdout.getvalue())
            self.assertIn("not FantLab parity", stdout.getvalue())
            html_path = root / "private-contrast.html"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(args[:-2] + ["--format", "html",
                                                      "--output", str(html_path)]), 0)
            html = html_path.read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", html)
            self.assertIn("COMPARABLE", html)
            self.assertNotIn("кот", html)
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                cli.main(args[:-2] + ["--format", "html", "--output", str(html_path)])



if __name__ == "__main__":
    unittest.main()
