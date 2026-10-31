"""Installed CLI entry point: evidence is source-free and scientifically labelled."""
from __future__ import annotations

import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.cli import main

ROOT = Path(__file__).resolve().parents[1]


class RetainedEvidenceCliTests(unittest.TestCase):
    def invoke(self, *arguments: str) -> str:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["evidence", "--root", str(ROOT), *arguments]), 0)
        return output.getvalue()

    def test_json_exposes_real_field_deltas_without_claiming_parity(self):
        report = json.loads(self.invoke("--format", "json"))
        self.assertEqual(report["works_reported"], 5)
        self.assertEqual(report["retained_metric_rows"], 171)
        self.assertEqual(report["m2_source_matched_pass_count"], 0)
        self.assertEqual(len(report["supplemental_diagnostics"]), 1)
        for entry in report["entries"] + report["supplemental_diagnostics"]:
            self.assertEqual(entry["exact_fantlab_input_identity"], "UNKNOWN")
            for row in entry["metric_rows"]:
                self.assertNotIn(row["result"], ("PASS", "FAIL", "pass", "fail"))
        self.assertNotIn("source_text", report)

    def test_csv_exposes_missing_as_unknown_not_numeric_zero(self):
        rows = list(csv.DictReader(io.StringIO(self.invoke("--format", "csv"))))
        self.assertEqual(len(rows), 171)
        self.assertTrue(all(row["source_match"] == "UNKNOWN" for row in rows))
        self.assertTrue(any(row["status"] == "NOT_RUN" and row["actual"] == ""
                            for row in rows))
        anna = next(row for row in rows if row["candidate_id"] == "tolstoy-anna-karenina-ru"
                    and row["metric_id"] == "fantlab.general.characters")
        self.assertEqual((anna["expected"], anna["actual"], anna["delta"]),
                         ("1692647", "1705605", "12958"))

    def test_output_create_only_and_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "PRIVATE-evidence.json"
            self.assertEqual(main(["evidence", "--root", str(ROOT), "--format", "json",
                                   "--output", str(destination)]), 0)
            before = destination.read_bytes()
            self.assertEqual(json.loads(before)["m2_source_matched_pass_count"], 0)
            error = io.StringIO()
            with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as caught:
                main(["evidence", "--root", str(ROOT), "--format", "csv",
                      "--output", str(destination)])
            self.assertEqual(caught.exception.code, 2)
            self.assertEqual(destination.read_bytes(), before)
            self.assertIn("already exists", error.getvalue())
            self.assertNotIn(directory, error.getvalue())

    def test_help_and_invalid_format(self):
        self.assertIn("evidence", self.invoke_help())
        error = io.StringIO()
        with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as caught:
            main(["evidence", "--format", "not-a-format"])
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("invalid choice", error.getvalue())

    @staticmethod
    def invoke_help() -> str:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            assert main(["--help"]) == 0
        return output.getvalue()


if __name__ == "__main__":
    unittest.main()
