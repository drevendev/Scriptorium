"""Regression tests for the retained, source-free field-by-field metric matrix."""
import copy
import csv
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import benchmark_metric_matrix as matrix

ROOT = Path(__file__).resolve().parents[1]


class RetainedMetricMatrixTests(unittest.TestCase):
    def test_real_five_work_report_has_two_retained_diagnostics(self):
        report = matrix.build_metric_matrix(ROOT)
        self.assertEqual(report["schema_version"], matrix.SCHEMA_VERSION)
        self.assertEqual(report["works_reported"], 5)
        self.assertEqual(report["works_with_retained_metric_diagnostics"], 2)
        self.assertEqual(report["retained_metric_rows"], 55)
        self.assertEqual(report["m2_source_matched_pass_count"], 0)
        self.assertEqual([e["metric_evidence"] for e in report["entries"]],
                         ["RETAINED_DIAGNOSTIC"] + ["NOT_RUN"] * 3 + ["RETAINED_DIAGNOSTIC"])
        self.assertEqual(report["entries"][0]["metric_rows_with_actual"], 23)
        self.assertEqual(report["entries"][0]["metric_rows_without_actual"], 5)
        anna = report["entries"][0]
        chars = next(r for r in anna["metric_rows"] if r["metric_id"] == "fantlab.general.characters")
        self.assertEqual((chars["expected"], chars["actual"], chars["actual_minus_expected"]),
                         (1692647, 1705605, 12958))
        self.assertEqual(chars["result"], "UNRESOLVED_SOURCE")
        self.assertTrue(all(e["exact_fantlab_input_identity"] == "UNKNOWN"
                            for e in report["entries"]))
        self.assertEqual([e["metric_rows"] for e in report["entries"][1:4]], [[], [], []])

    def test_formats_are_stable_and_do_not_turn_not_run_into_zero(self):
        report = matrix.build_metric_matrix(ROOT)
        for kind in ("json", "csv", "markdown"):
            self.assertEqual(matrix.render_metric_matrix(report, kind),
                             matrix.render_metric_matrix(matrix.build_metric_matrix(ROOT), kind))
        self.assertEqual(json.loads(matrix.render_metric_matrix(report, "json")),
                         report)
        rows = list(csv.DictReader(StringIO(matrix.render_metric_matrix(report, "csv"))))
        self.assertEqual(len(rows), 58)
        self.assertEqual(sum(r["status"] == "NOT_RUN" for r in rows), 9)
        # Two Anna and four Running on Waves dictionary rows are NOT_RUN; three other works have no metric artifacts.
        absent = [r for r in rows if not r["metric_id"]]
        self.assertEqual(len(absent), 3)
        self.assertTrue(all(r["expected"] == r["actual"] == r["delta"] == "" for r in absent))
        self.assertIn("M2: 0/5", matrix.render_metric_matrix(report, "markdown"))
        self.assertIn("12958", matrix.render_metric_matrix(report, "csv"))

    def _mutate(self, path, mutate):
        original = matrix._load

        def substituted(root, relative):
            document = original(root, relative)
            if relative == path:
                document = copy.deepcopy(document)
                mutate(document)
            return document

        with patch.object(matrix, "_load", side_effect=substituted):
            return matrix.build_metric_matrix(ROOT)

    def test_rejects_dishonest_source_match_or_parity(self):
        with self.assertRaisesRegex(ValueError, "source identity"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["epistemic_status"].__setitem__("fantlab_source_edition_match", "exact"))
        with self.assertRaisesRegex(ValueError, "parity admissibility"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["epistemic_status"].__setitem__("m2_parity_admissible", True))

    def test_rejects_swapped_witness_and_reference(self):
        with self.assertRaisesRegex(ValueError, "raw frozen witness"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["evidence"].__setitem__("raw_sha256", "f" * 64))
        with self.assertRaisesRegex(ValueError, "reference URL"):
            self._mutate(matrix.REFERENCE,
                         lambda d: d["reference"].__setitem__("url", "https://fantlab.ru/work1/lp"))

    def test_rejects_expected_delta_or_status_tampering(self):
        metric = "fantlab.general.characters"
        with self.assertRaisesRegex(ValueError, "expected"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["metrics"][metric].__setitem__("expected", 1))
        with self.assertRaisesRegex(ValueError, "integer metric delta"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["metrics"][metric].__setitem__("raw_delta", 0))
        with self.assertRaisesRegex(ValueError, "may not pass"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["metrics"][metric].__setitem__("result", "pass"))
        with self.assertRaisesRegex(ValueError, "metric IDs"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["metrics"].pop(metric))
        with self.assertRaisesRegex(ValueError, "unknown metric state"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["metrics"]["fantlab.vocabulary.active_dictionary"].__setitem__("raw_delta", 0))

    def test_rejects_nearby_float_delta_and_actual_forgery(self):
        metric = "fantlab.general.mean_word_length_chars"

        def corrupt_delta(doc):
            doc["metrics"][metric]["raw_delta"] += 1e-11

        def corrupt_actual(doc):
            doc["metrics"][metric]["actual"] += 1e-11

        # Both perturbations were previously swallowed by the 1e-10 isclose
        # tolerance, even though the retained artifact encodes exact deltas.
        for change in (corrupt_delta, corrupt_actual):
            with self.subTest(change=change.__name__):
                with self.assertRaisesRegex(ValueError, "floating metric delta"):
                    self._mutate(matrix.DIAGNOSTIC, change)


    def test_running_on_waves_reuses_frozen_measurements_without_parity(self):
        report = matrix.build_metric_matrix(ROOT)
        wave = report["entries"][-1]
        self.assertEqual(wave["candidate_id"], "grin-running-on-waves-ru")
        self.assertEqual(wave["metric_evidence"], "RETAINED_DIAGNOSTIC")
        self.assertEqual((len(wave["metric_rows"]), wave["metric_rows_with_actual"],
                          wave["metric_rows_without_actual"]), (27, 23, 4))
        chars = next(r for r in wave["metric_rows"]
                     if r["metric_id"] == "fantlab.general.characters")
        words = next(r for r in wave["metric_rows"]
                     if r["metric_id"] == "fantlab.general.words")
        self.assertEqual((chars["expected"], chars["actual"], chars["actual_minus_expected"]),
                         (360987, 363819, 2832))
        self.assertEqual((words["expected"], words["actual"], words["actual_minus_expected"]),
                         (52985, 55778, 2793))
        self.assertEqual(wave["exact_fantlab_input_identity"], "UNKNOWN")
        self.assertEqual(report["m2_source_matched_pass_count"], 0)
        self.assertTrue(all(r["comparison_kind"] == "DIAGNOSTIC_ONLY"
                            and r["display_rounding_evidence"] == "UNKNOWN"
                            and r["result"] in ("NOT_RUN", "UNRESOLVED_SOURCE")
                            for r in wave["metric_rows"]))

    def test_running_on_waves_rejects_forged_source_or_metric_evidence(self):
        def corrupt_reference(doc):
            doc["metrics"][0]["fantlab_display_value"] = "360986"

        def corrupt_decimal_delta(doc):
            doc["metrics"][2]["delta_against_fantlab_display"] = "0"

        def corrupt_source(doc):
            doc["body_identity"]["raw_sha256"] = "f" * 64

        def corrupt_parity(doc):
            doc["gates"]["m2_parity_admissible"] = True

        for change, message in (
            (corrupt_reference, "displayed reference"),
            (corrupt_decimal_delta, "decimal metric delta"),
            (corrupt_source, "raw witness"),
            (corrupt_parity, "M2 and source gates"),
        ):
            with self.subTest(change=change.__name__):
                with self.assertRaisesRegex(ValueError, message):
                    self._mutate(matrix._RUNNING_DIAGNOSTIC, change)

    def test_nonfinite_metric_values_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "numeric metric"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["metrics"]["fantlab.general.words"].__setitem__("actual", float("nan")))

    def test_public_guides_do_not_hide_retained_waves_measurements(self):
        """Public evidence counts must agree with the canonical retained matrix."""
        report = matrix.build_metric_matrix(ROOT)
        self.assertEqual(report["works_with_retained_metric_diagnostics"], 2)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        method = (ROOT / "docs/BENCHMARK_METRIC_MATRIX.md").read_text(encoding="utf-8")
        readiness = (ROOT / "docs/BENCHMARK_READINESS.md").read_text(encoding="utf-8")
        self.assertIn(f"**{report['retained_metric_rows']} field-level diagnostic rows**", readme)
        self.assertIn("**two works with retained measurements**", readme)
        self.assertIn("the remaining **three** frozen works", readme)
        self.assertIn("**independent search/filter controls for both books**", readme)
        self.assertIn("**two independent**", method)
        self.assertIn("the three works without retained diagnostics", method)
        self.assertIn("all 55 rows after filtering", method)
        self.assertIn("**not a global evidence verdict**", readiness)
        self.assertNotIn("Filters affect Anna only", method)
        self.assertNotIn("all four other works remain", method)
        self.assertNotIn("marks the other four works", readme)

    def test_cli_creates_report_but_cannot_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "metrics.csv"
            self.assertEqual(matrix.main(["--root", str(ROOT), "--format", "csv", "--output", str(destination)]), 0)
            first = destination.read_bytes()
            with patch("sys.stderr", new_callable=StringIO) as err:
                with self.assertRaises(SystemExit):
                    matrix.main(["--root", str(ROOT), "--format", "csv", "--output", str(destination)])
            self.assertEqual(destination.read_bytes(), first)
            self.assertIn("already exists", err.getvalue())
            self.assertNotIn(str(destination), err.getvalue())


if __name__ == "__main__":
    unittest.main()
