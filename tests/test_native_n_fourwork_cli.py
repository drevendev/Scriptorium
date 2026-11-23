"""Acceptance for offline four-work N comparison, with pinned byte privacy gates."""
import contextlib
import csv
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium import cli
from scriptorium.native_n_fourwork_cli import (
    EXTRA_RECEIPTS, build_fourwork_report, main, render_fourwork_report,
)
from scriptorium.native_n_evidence import RETAINED_PATH
from scriptorium.native_n_crosswork_cli import RESURRECTION_PATH

ROOT = Path(__file__).resolve().parents[1]
INPUTS = (RETAINED_PATH, RESURRECTION_PATH) + tuple(Path(x[1]) for x in EXTRA_RECEIPTS)


class NativeFourWorkCLITests(unittest.TestCase):
    def test_four_real_work_counts_percentages_and_provenance(self):
        doc = build_fourwork_report(ROOT)
        self.assertEqual(doc["schema_version"], "scriptorium-native-n-fourwork-offline-v1")
        self.assertEqual(doc["status"], "diagnostic_only")
        self.assertFalse(doc["source_text_included"])
        self.assertFalse(doc["m2_parity_admissible"])
        self.assertEqual(
            [(x["key"], x["word_tokens"], x["counts"]["n_only"]) for x in doc["works"]],
            [("anna", 269358, 55081), ("resurrection", 136129, 31708),
             ("grin", 55778, 12724), ("road", 65072, 17352)],
        )
        for row in doc["works"]:
            self.assertEqual(row["counts"]["n_only"] + row["counts"]["n_mixed"],
                             row["counts"]["any_n"])
            for metric in ("n_only", "n_mixed", "any_n"):
                self.assertAlmostEqual(
                    row["percent_of_word_tokens"][metric],
                    row["counts"][metric] / row["word_tokens"] * 100,
                )
            self.assertEqual(len(row["normalized_sha256"]), 64)
            self.assertEqual(len(row["runtime_analysis_sha256"]), 64)
            self.assertIn("/actions/runs/", row["native_workflow"])
        d = doc["same_author_percentage_point_deltas"]["grin_road_minus_waves"]
        self.assertAlmostEqual(d["n_only"],
            100 * 17352 / 65072 - 100 * 12724 / 55778)

    def test_cli_formats_and_create_only(self):
        report = build_fourwork_report(ROOT)
        serialized = render_fourwork_report(report, "json")
        self.assertEqual(json.loads(serialized), report)
        markdown = render_fourwork_report(report, "markdown")
        self.assertIn("четыре книги", markdown)
        self.assertIn("M2: 0/5", markdown)
        self.assertIn("Дорога в никуда", markdown)
        self.assertIn("Бегущая по волнам", markdown)
        self.assertIn("Воскресение − Анна Каренина", markdown)
        rows = list(csv.DictReader(StringIO(render_fourwork_report(report, "csv"))))
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[-1]["candidate_id"], "grin-road-nowhere-ru")
        self.assertEqual(rows[-1]["measure_id"], "any_n")
        for record in rows:
            self.assertEqual(record["evidence_status"], "diagnostic_only")
            self.assertEqual(len(record["normalized_sha256"]), 64)
        for output in (serialized, markdown, render_fourwork_report(report, "csv")):
            self.assertNotIn('"source_text":', output)
            self.assertNotIn('"normalized_text":', output)
            self.assertNotIn("private manuscript", output)
        with self.assertRaises(ValueError):
            render_fourwork_report(report, "html")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "four.csv"
            with contextlib.redirect_stdout(StringIO()):
                self.assertEqual(cli.main(["n-four", "--root", str(ROOT),
                                           "--format", "csv", "--output", str(output)]), 0)
            before = output.read_bytes()
            with contextlib.redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit) as error:
                    main(["--root", str(ROOT), "--output", str(output)])
            self.assertEqual(error.exception.code, 2)
            self.assertEqual(output.read_bytes(), before)

    def test_fail_closed_on_byte_drift_source_leaks_and_missing_receipts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "assets").mkdir()
            for path in INPUTS:
                (root / path).write_bytes((ROOT / path).read_bytes())
            self.assertEqual(build_fourwork_report(root), build_fourwork_report(ROOT))
            for path in INPUTS:
                baseline = (root / path).read_bytes()
                for changed in (
                    baseline + b"\n",
                    baseline.replace(b'"source_text_included": false',
                                     b'"source_text_included": true', 1),
                    baseline + b'"normalized_text": "private manuscript"',
                ):
                    (root / path).write_bytes(changed)
                    with self.subTest(file=path, changed=changed[-40:]):
                        with self.assertRaises((OSError, ValueError)):
                            build_fourwork_report(root)
                (root / path).write_bytes(baseline)
            extra = Path(EXTRA_RECEIPTS[1][1])
            (root / extra).unlink()
            with self.assertRaises((OSError, ValueError)):
                build_fourwork_report(root)


if __name__ == "__main__":
    unittest.main()
