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
    def test_real_five_work_report_has_four_retained_diagnostics(self):
        report = matrix.build_metric_matrix(ROOT)
        self.assertEqual(report["schema_version"], matrix.SCHEMA_VERSION)
        self.assertEqual(report["works_reported"], 5)
        self.assertEqual(report["works_with_retained_metric_diagnostics"], 4)
        self.assertEqual(report["retained_metric_rows"], 142)
        self.assertEqual(report["supplemental_retained_metric_rows"], 29)
        self.assertEqual(report["m2_source_matched_pass_count"], 0)
        self.assertEqual([e["metric_evidence"] for e in report["entries"]],
                         ["RETAINED_DIAGNOSTIC", "RETAINED_DIAGNOSTIC", "RETAINED_DIAGNOSTIC",
                          "NOT_RUN", "RETAINED_DIAGNOSTIC"])
        self.assertEqual(report["entries"][0]["metric_rows_with_actual"], 23)
        self.assertEqual(report["entries"][0]["metric_rows_without_actual"], 5)
        anna = report["entries"][0]
        chars = next(r for r in anna["metric_rows"] if r["metric_id"] == "fantlab.general.characters")
        self.assertEqual((chars["expected"], chars["actual"], chars["actual_minus_expected"]),
                         (1692647, 1705605, 12958))
        self.assertEqual(chars["result"], "UNRESOLVED_SOURCE")
        self.assertTrue(all(e["exact_fantlab_input_identity"] == "UNKNOWN"
                            for e in report["entries"]))
        self.assertEqual(report["entries"][3]["metric_rows"], [])
        silver = report["entries"][2]
        self.assertEqual((len(silver["metric_rows"]), silver["metric_rows_with_actual"],
                          silver["metric_rows_without_actual"]), (29, 24, 5))
        self.assertEqual(silver["metric_evidence"], "RETAINED_DIAGNOSTIC")
        self.assertEqual(silver["exact_fantlab_input_identity"], "UNKNOWN")
        self.assertEqual(len([r for r in silver["metric_rows"] if r["expected"] is not None]), 2)
        self.assertEqual([r["expected"] for r in silver["metric_rows"] if r["expected"] is not None],
                         [549050, 83369])

    def test_formats_are_stable_and_do_not_turn_not_run_into_zero(self):
        report = matrix.build_metric_matrix(ROOT)
        for kind in ("json", "csv", "markdown"):
            self.assertEqual(matrix.render_metric_matrix(report, kind),
                             matrix.render_metric_matrix(matrix.build_metric_matrix(ROOT), kind))
        self.assertEqual(json.loads(matrix.render_metric_matrix(report, "json")),
                         report)
        rows = list(csv.DictReader(StringIO(matrix.render_metric_matrix(report, "csv"))))
        self.assertEqual(len(rows), 143)
        self.assertEqual(sum(r["status"] == "NOT_RUN" for r in rows), 22)
        # Core missing rows plus five Resurrection unbound metrics; one absent work remains NOT_RUN.
        absent = [r for r in rows if not r["metric_id"]]
        self.assertEqual(len(absent), 1)
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


    def test_silver_dove_pinned_ci_receipt_rejects_forgery(self):
        from scriptorium import silver_dove_retained as silver
        from scriptorium.benchmark_readiness import build_readiness
        witness = next(item for item in build_readiness(ROOT)["entries"]
                       if item["candidate_id"] == silver.CANDIDATE_ID)
        rows = silver.verify(ROOT, witness)
        self.assertEqual((len(rows), sum(r["actual"] is not None for r in rows)), (29, 24))
        self.assertEqual(sum(r["expected"] is not None for r in rows), 2)
        self.assertEqual(next(r for r in rows if r["metric_id"] == "fantlab.general.characters")
                         ["actual_minus_expected"], 14075)
        self.assertEqual(next(r for r in rows if r["metric_id"] == "fantlab.general.words")
                         ["actual_minus_expected"], 4867)
        self.assertEqual(next(r for r in rows if r["metric_id"] == "scriptorium.general.sentences")
                         ["comparison_kind"], "EXTENSION_ONLY")
        self.assertEqual([r["result"] for r in rows].count("MEASURED_NO_REFERENCE"), 22)
        self.assertTrue(all(r["expected"] is None and r["actual_minus_expected"] is None
                            for r in rows if r["result"] == "MEASURED_NO_REFERENCE"))
        original = silver._load
        for change, message in (
            (lambda d: d["gates"].__setitem__("m2_parity_admissible", True), "M2 gate"),
            (lambda d: d["body_identity"].__setitem__("raw_sha256", "f" * 64), "frozen source identity"),
            (lambda d: d["metric_rows"][0].__setitem__("fantlab_display", "35"), "reference field"),
            (lambda d: d["metric_rows"][0].__setitem__("actual_minus_fantlab_display", 0), "unknown reference delta"),
            (lambda d: d["metric_rows"][4].__setitem__("actual_minus_fantlab_display", 0), "integer reference delta"),
            (lambda d: d["metric_rows"][22].__setitem__("actual", 0), "unbound dictionary state"),
            (lambda d: d["metric_rows"][28].__setitem__("compatibility_status", "reproduced"), "compatibility status"),
        ):
            def injected(root, relative):
                document = copy.deepcopy(original(root, relative))
                change(document)
                return document
            with self.subTest(change=message), patch.object(silver, "_load", side_effect=injected):
                with self.assertRaisesRegex(ValueError, message):
                    silver.verify(ROOT, witness)

    def test_karamazov_pinned_ci_receipt_rejects_forgery(self):
        from scriptorium import karamazov_retained as karamazov
        from scriptorium.benchmark_readiness import build_readiness
        witness = next(item for item in build_readiness(ROOT)["entries"]
                       if item["candidate_id"] == karamazov.CANDIDATE_ID)
        rows = karamazov.verify(ROOT, witness)
        self.assertEqual((len(rows), sum(r["actual"] is not None for r in rows)), (29, 24))
        self.assertEqual(sum(r["expected"] is not None for r in rows), 2)
        self.assertEqual(next(r for r in rows if r["metric_id"] == "fantlab.general.characters")
                         ["actual_minus_expected"], 3244)
        self.assertEqual(next(r for r in rows if r["metric_id"] == "fantlab.general.words")
                         ["actual_minus_expected"], 10588)
        self.assertEqual(next(r for r in rows if r["metric_id"] == "scriptorium.general.sentences")
                         ["comparison_kind"], "EXTENSION_ONLY")
        self.assertEqual([r["result"] for r in rows].count("MEASURED_NO_REFERENCE"), 22)
        self.assertTrue(all(r["expected"] is None and r["actual_minus_expected"] is None
                            for r in rows if r["result"] == "MEASURED_NO_REFERENCE"))
        original = karamazov._load
        for change, message in (
            (lambda d: d["gates"].__setitem__("m2_parity_admissible", True), "M2 gate"),
            (lambda d: d["body_identity"].__setitem__("raw_sha256", "f" * 64), "frozen source identity"),
            (lambda d: d["metric_rows"][0].__setitem__("fantlab_display", "35"), "reference field"),
            (lambda d: d["metric_rows"][0].__setitem__("actual_minus_fantlab_display", 0), "unknown reference delta"),
            (lambda d: d["metric_rows"][4].__setitem__("actual_minus_fantlab_display", 0), "integer reference delta"),
            (lambda d: d["metric_rows"][22].__setitem__("actual", 0), "unbound dictionary state"),
            (lambda d: d["metric_rows"][28].__setitem__("compatibility_status", "reproduced"), "compatibility status"),
        ):
            def injected(root, relative):
                document = copy.deepcopy(original(root, relative))
                change(document)
                return document
            with self.subTest(change=message), patch.object(karamazov, "_load", side_effect=injected):
                with self.assertRaisesRegex(ValueError, message):
                    karamazov.verify(ROOT, witness)

    def test_resurrection_is_supplemental_and_retains_two_only_fantlab_references(self):
        report = matrix.build_metric_matrix(ROOT)
        self.assertEqual(report["works_reported"], 5)
        self.assertEqual(report["works_with_retained_metric_diagnostics"], 4)
        self.assertEqual(len(report["entries"]), 5)
        extra, = report["supplemental_diagnostics"]
        self.assertEqual(extra["candidate_id"], "tolstoy-resurrection-ru")
        self.assertEqual(extra["m2_candidate_scope"], "SUPPLEMENTAL_NOT_SOURCE_MATCHED")
        self.assertEqual(extra["exact_fantlab_input_identity"], "UNKNOWN")
        self.assertEqual(extra["source_witness_sha256"],
                         "2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0")
        self.assertEqual((len(extra["metric_rows"]), extra["metric_rows_with_actual"],
                          extra["metric_rows_without_actual"]), (29, 24, 5))
        rows = {row["metric_id"]: row for row in extra["metric_rows"]}
        self.assertEqual((rows["fantlab.general.characters"]["expected"],
                          rows["fantlab.general.characters"]["actual"],
                          rows["fantlab.general.characters"]["actual_minus_expected"]),
                         (881244, 890835, 9591))
        self.assertEqual((rows["fantlab.general.words"]["expected"],
                          rows["fantlab.general.words"]["actual_minus_expected"]),
                         (126457, 9672))
        self.assertEqual(sum(row["expected"] is not None for row in rows.values()), 2)
        self.assertEqual(rows["scriptorium.general.sentences"]["comparison_kind"],
                         "EXTENSION_ONLY")
        self.assertTrue(all(row["comparison_kind"] != "EXTENSION_ONLY"
                            or row["expected"] is None for row in rows.values()))
        self.assertTrue(all(row["result"] != "PASS" for row in rows.values()))
        self.assertEqual(report["m2_source_matched_pass_count"], 0)
        self.assertIn("Resurrection is a sixth supplemental diagnostic",
                      matrix.render_metric_matrix(report, "markdown"))
        self.assertIn("tolstoy-resurrection-ru", matrix.render_metric_matrix(report, "csv"))

    def test_resurrection_tampering_fails_before_publication(self):
        from scriptorium import resurrection_retained as retained
        original = retained._load

        for field, mutate, failure in (
            ("ref", lambda d: d["fantlab"]["public_display_references_retained"]
             .__setitem__("fantlab.general.characters", "881243"), "dated unmatched FantLab reference"),
            ("gate", lambda d: d["gates"].__setitem__("m2_parity_admissible", True),
             "unchanged M2 gate"),
            ("source", lambda d: d["body_identity"].__setitem__("raw_sha256", "f" * 64),
             "frozen source identity"),
            ("status", lambda d: d["metric_rows"][4].__setitem__("result", "PASS"),
             "unmatched reference status"),
            ("delta", lambda d: d["metric_rows"][4].__setitem__(
                "actual_minus_fantlab_display", 0), "integer reference delta"),
            ("unknown", lambda d: d["metric_rows"][22].__setitem__("actual", 0),
             "unbound dictionary state"),
        ):
            def changed(root, relative):
                value = original(root, relative)
                if relative == retained.ARTIFACT_PATH:
                    value = copy.deepcopy(value)
                    mutate(value)
                return value

            with self.subTest(field=field), patch.object(retained, "_load", side_effect=changed):
                with self.assertRaisesRegex(ValueError, failure):
                    retained.verify(ROOT)

    def test_nonfinite_metric_values_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "numeric metric"):
            self._mutate(matrix.DIAGNOSTIC,
                         lambda d: d["metrics"]["fantlab.general.words"].__setitem__("actual", float("nan")))

    def test_public_guides_do_not_hide_retained_waves_measurements(self):
        """Public evidence counts must agree with the canonical retained matrix."""
        report = matrix.build_metric_matrix(ROOT)
        self.assertEqual(report["works_with_retained_metric_diagnostics"], 4)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        method = (ROOT / "docs/BENCHMARK_METRIC_MATRIX.md").read_text(encoding="utf-8")
        readiness = (ROOT / "docs/BENCHMARK_READINESS.md").read_text(encoding="utf-8")
        self.assertIn(f"**{report['retained_metric_rows']} field-level diagnostic/extension rows**", readme)
        self.assertIn("**four works with retained measurements**", readme)
        self.assertIn("The remaining **one** frozen work", readme)
        self.assertIn("**independent search/filter controls for both books**", readme)
        self.assertIn("**two independent**", method)
        self.assertIn("the one work without retained diagnostics", method)
        self.assertIn("all 142 rows in exports", method)
        self.assertIn("**not a global evidence verdict**", readiness)
        self.assertIn(f"already validates {report['retained_metric_rows']}\n", readiness)
        self.assertIn("**26 reference values are UNKNOWN**", method)
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
