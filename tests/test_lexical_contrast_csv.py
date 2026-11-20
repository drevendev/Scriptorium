"""Source-free CSV lexical-contrast contract and installed CLI regressions."""
from __future__ import annotations

import contextlib
import csv
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from scriptorium import cli
from scriptorium.lexical_contrast import build_lexical_contrast, render_lexical_contrast


def sample(left="кот " * 8 + "пёс " * 2, right="пёс " * 9 + "кот", **kwargs):
    return build_lexical_contrast(
        left, right, left_edition_id="edition-left",
        right_edition_id="edition-right", **kwargs
    )


def rows(report):
    rendered = render_lexical_contrast(report, "csv")
    parsed = csv.DictReader(StringIO(rendered))
    assert parsed.fieldnames == ["section", "field", "value", "unit"]
    records = {(r["section"], r["field"]): r for r in parsed}
    assert len(records) == len(list(csv.DictReader(StringIO(rendered))))
    return rendered, records


class LexicalContrastCsvTests(unittest.TestCase):
    def test_numeric_units_and_source_identity_are_replayable_without_words(self):
        report = sample()
        rendered, data = rows(report)
        self.assertEqual(data["comparison", "status"]["value"], "COMPARABLE")
        self.assertEqual(data["comparison", "public_release_ready"]["value"], "false")
        self.assertEqual(data["left", "edition_id"]["value"], "edition-left")
        self.assertEqual(data["right", "edition_id"]["value"], "edition-right")
        self.assertEqual(data["left", "normalized_sha256"]["value"],
                         report["left"]["normalized_sha256"])
        self.assertEqual(data["left", "source_text_embedded"]["value"], "false")
        self.assertEqual(data["aggregate", "eligible_form_count"]["value"], "2")
        self.assertEqual(data["aggregate", "eligible_form_count"]["unit"], "forms")
        self.assertEqual(data["aggregate", "left_dominant_token_share_percent"]["unit"],
                         "% of left tokens")
        self.assertEqual(data["aggregate", "jensen_shannon_divergence_bits"]["unit"], "bits (0-1)")
        self.assertIn("private", rendered.lower())
        self.assertNotIn("кот", rendered)
        self.assertNotIn("пёс", rendered)

    def test_token_ratio_csv_is_typed_and_old_v1_artifacts_remain_readable(self):
        report = sample("кот " * 10, "а б " * 10)
        _, data = rows(report)
        self.assertEqual(data["comparison", "length_imbalance_warning"]["value"], "false")
        self.assertEqual(data["comparison", "word_token_ratio_max_over_min"]["value"], "2.0")
        self.assertEqual(data["comparison", "word_token_ratio_max_over_min"]["unit"], "ratio")
        self.assertEqual(data["comparison", "word_token_imbalance_warning"]["value"], "true")
        _, unavailable = rows(sample("", "кот"))
        self.assertEqual(unavailable["comparison", "word_token_ratio_max_over_min"]["value"], "UNKNOWN")
        legacy = {key: value for key, value in report.items()
                  if key not in ("word_token_ratio_max_over_min", "word_token_imbalance_warning")}
        _, old = rows(legacy)
        self.assertNotIn(("comparison", "word_token_ratio_max_over_min"), old)
        with self.assertRaises(ValueError):
            rows({**legacy, "word_token_ratio_max_over_min": 2})
        with self.assertRaises(ValueError):
            rows({**report, "word_token_imbalance_warning": False})

    def test_unavailable_is_not_zero_and_true_zero_is_preserved(self):
        _, empty = rows(sample("", "кот"))
        self.assertEqual(empty["comparison", "status"]["value"], "NOT_RUN_EMPTY")
        for (section, key), row in empty.items():
            if section == "aggregate":
                self.assertEqual(row["value"], "NOT_RUN", key)
        _, identical = rows(sample("кот " * 6, "КОТ " * 6))
        self.assertEqual(identical["aggregate", "jensen_shannon_divergence_bits"]["value"], "0.0")
        self.assertEqual(identical["aggregate", "left_dominant_form_count"]["value"], "0")

    def test_untrusted_labels_are_quoted_and_formula_neutralized(self):
        report = sample(left_translator="=2+2,evil", right_translator="@SUM(1)")
        rendered, data = rows(report)
        self.assertEqual(data["left", "translator"]["value"], "'=2+2,evil")
        self.assertEqual(data["right", "translator"]["value"], "'@SUM(1)")
        self.assertIn('"\'=2+2,evil"', rendered)
        self.assertEqual(data["left", "metadata_verified"]["value"], "false")
        self.assertEqual(data["right", "original_work_id"]["value"], "UNKNOWN")

    def test_bad_schema_incomplete_rows_and_numeric_spoofs_fail_closed(self):
        original = sample()
        for report in (
            {**original, "schema_version": "forged"},
            {**original, "aggregate": {}},
            {**original, "aggregate": {**original["aggregate"],
                                      "jensen_shannon_divergence_bits": float("nan")}},
            {**original, "aggregate": {**original["aggregate"],
                                      "eligible_form_count": "5"}},
            {**original, "aggregate": {**original["aggregate"],
                                      "left_dominant_token_share_percent": 101}},
            {**original, "left": {"edition_id": "a"}},
        ):
            with self.subTest(report=report.get("schema_version")):
                with self.assertRaises(ValueError):
                    render_lexical_contrast(report, "csv")

    def test_cli_offline_csv_and_create_only_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            left, right, destination = (root / n for n in ("left.txt", "right.txt", "contrast.csv"))
            left.write_text("кот " * 8 + "пёс " * 2, encoding="utf-8")
            right.write_text("пёс " * 9 + "кот", encoding="utf-8")
            args = ["distinctives", str(left), str(right), "--left-edition", "edition-left",
                    "--right-edition", "edition-right", "--format", "csv", "--output", str(destination)]
            with contextlib.redirect_stdout(StringIO()):
                self.assertEqual(cli.main(args), 0)
            csv_text = destination.read_text(encoding="utf-8")
            self.assertEqual(rows(sample())[0], csv_text)
            with contextlib.redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                cli.main(args)
            self.assertEqual(destination.read_text(encoding="utf-8"), csv_text)


if __name__ == "__main__":
    unittest.main()
