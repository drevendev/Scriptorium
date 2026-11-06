"""Source-unmatched word-density regression: arithmetic, safety and CLI."""
from __future__ import annotations

import contextlib
import copy
import csv
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium import cli, word_gap
from scriptorium.benchmark_metric_matrix import build_metric_matrix

ROOT = Path(__file__).resolve().parents[1]


class WordGapTests(unittest.TestCase):
    def _simple(self):
        return {
            "m2_source_matched_pass_count": 0,
            "entries": [{
                "candidate_id": "synthetic", "title": "A | B",
                "exact_fantlab_input_identity": "UNKNOWN",
                "metric_rows": [
                    {"metric_id": "fantlab.general.characters", "expected": 1000,
                     "actual": 1200, "actual_minus_expected": 200, "result": "UNRESOLVED_SOURCE"},
                    {"metric_id": "fantlab.general.words", "expected": 100,
                     "actual": 144, "actual_minus_expected": 44, "result": "UNRESOLVED_SOURCE"},
                ],
            }],
            "supplemental_diagnostics": [],
        }

    def test_real_frozen_anna_quantifies_unexplained_word_gap(self):
        diagnostic = word_gap.build_word_density_diagnostic(build_metric_matrix(ROOT))
        self.assertEqual(diagnostic["schema_version"], word_gap.SCHEMA_VERSION)
        self.assertEqual(diagnostic["m2_source_matched_pass_count"], 0)
        self.assertEqual(len(diagnostic["entries"]), 6)
        anna = next(e for e in diagnostic["entries"] if e["candidate_id"] == "tolstoy-anna-karenina-ru")
        self.assertEqual((anna["raw_character_gap"], anna["raw_word_gap"]), (12958, 16083))
        self.assertEqual(anna["fantlab_words_per_1000_characters"], "149.632499")
        self.assertEqual(anna["scriptorium_words_per_1000_characters"], "157.925194")
        self.assertEqual(anna["density_gap_per_1000_characters"], "8.292695")
        self.assertEqual(anna["length_adjusted_word_residual"], "14144.062082")
        self.assertEqual(anna["status"], "DIAGNOSTIC_ONLY")
        for kind in ("json", "markdown", "csv"):
            self.assertEqual(word_gap.render_word_density_diagnostic(diagnostic, kind),
                             word_gap.render_word_density_diagnostic(
                                 word_gap.build_word_density_diagnostic(build_metric_matrix(ROOT)), kind))
        self.assertIn("not", diagnostic["note"].lower())
        self.assertIn("M2: 0/5", word_gap.render_word_density_diagnostic(diagnostic, "markdown"))
        self.assertEqual(json.loads(word_gap.render_word_density_diagnostic(diagnostic, "json")), diagnostic)

    def test_synthetic_length_adjustment_and_missing_are_explicit(self):
        report = self._simple()
        report["supplemental_diagnostics"].append({
            "candidate_id": "missing", "title": "Unmeasured",
            "exact_fantlab_input_identity": "UNKNOWN", "metric_rows": [],
        })
        rows = word_gap.build_word_density_diagnostic(report)["entries"]
        self.assertEqual(rows[0]["raw_word_gap"], 44)
        self.assertEqual(rows[0]["density_gap_per_1000_characters"], "20.000000")
        self.assertEqual(rows[0]["length_adjusted_word_residual"], "24.000000")
        self.assertEqual(rows[1]["status"], "NOT_RUN")
        self.assertIsNone(rows[1]["density_gap_per_1000_characters"])
        rendered = word_gap.render_word_density_diagnostic(
            word_gap.build_word_density_diagnostic(report), "markdown"
        )
        self.assertIn("A \\| B", rendered)
        self.assertIn("NOT_RUN", rendered)
        csv_rows = list(csv.DictReader(StringIO(word_gap.render_word_density_diagnostic(
            word_gap.build_word_density_diagnostic(report), "csv"
        ))))
        self.assertEqual(csv_rows[1]["density_gap_per_1000_characters"], "")

    def test_rejects_tampering_and_parity_inference(self):
        for mutation in ("boolean", "negative", "delta", "source", "parity", "duplicate", "zero"):
            with self.subTest(mutation=mutation):
                report = copy.deepcopy(self._simple())
                row = report["entries"][0]["metric_rows"][1]
                if mutation == "boolean":
                    row["actual"] = True
                elif mutation == "negative":
                    row["expected"] = -1
                elif mutation == "delta":
                    row["actual_minus_expected"] += 1
                elif mutation == "source":
                    report["entries"][0]["exact_fantlab_input_identity"] = "MATCHED"
                elif mutation == "parity":
                    report["m2_source_matched_pass_count"] = 1
                elif mutation == "duplicate":
                    report["entries"][0]["metric_rows"].append(copy.deepcopy(row))
                elif mutation == "zero":
                    report["entries"][0]["metric_rows"][0]["expected"] = 0
                    report["entries"][0]["metric_rows"][0]["actual_minus_expected"] = 1200
                with self.assertRaises(ValueError):
                    word_gap.build_word_density_diagnostic(report)

    def test_cli_export_create_only(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / "word-gap.json"
            self.assertEqual(cli.main(["word-gap", "--root", str(ROOT), "--format", "json",
                                       "--output", str(out)]), 0)
            self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["m2_source_matched_pass_count"], 0)
            with self.assertRaises(SystemExit):
                cli.main(["word-gap", "--root", str(ROOT), "--output", str(out)])
