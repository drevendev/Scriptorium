import contextlib
import io
import hashlib
import copy
import json
from pathlib import Path
import tempfile
import unittest

import scriptorium.frozen_diagnostic_report as report


def artifact():
    return {
        "artifact_version": "scriptorium-frozen-diagnostic-v1",
        "benchmark_id": "fantlab-work1-2022-09-19",
        "candidate_id": "fixture-work",
        "evidence": {
            "hosted_run_id": 123,
            "python_version": "3.13.15",
            "scriptorium_revision": "abc123",
            "reference_path": "benchmarks/fantlab/work1.json",
            "source_manifest_path": "corpus/candidates/source-edition-traces/work.revisions.json",
            "replay_integrity": "passed",
            "chapter_count": 2,
            "raw_sha256": "a" * 64,
            "normalized_sha256": "b" * 64,
            "source_text_committed": False,
            "source_text_uploaded": False,
        },
        "epistemic_status": {
            "status": "diagnostic_only",
            "fantlab_source_edition_match": "unknown",
            "m2_parity_admissible": False,
            "m2_source_matched_progress": "0/5",
            "reason": "Source edition is not established.",
        },
        "metrics": {
            "fantlab.general.characters": {
                "expected": 10,
                "actual": 12,
                "raw_delta": 2,
                "result": "unresolved",
            },
            "fantlab.vocabulary.active_dictionary": {
                "expected": 5,
                "actual": None,
                "raw_delta": None,
                "result": "not_run",
            },
            "fantlab.punctuation.question.per_1000_words": {
                "expected": 1.25,
                "actual": 1.0,
                "raw_delta": -0.25,
                "result": "unresolved",
            },
        },
        "omitted_metric_families": {
            "pos": "Provider execution not available."
        },
        "observations": [
            "A visible difference is diagnostic only.",
        ],
    }


class FrozenDiagnosticReportTests(unittest.TestCase):
    def test_summary_keeps_missing_and_results_distinct(self):
        self.assertEqual(
            report.summarize(artifact()),
            {
                "metric_count": 3,
                "actual_count": 2,
                "missing_actual_count": 1,
                "unresolved_count": 2,
                "not_run_count": 1,
            },
        )

    def test_raw_delta_is_rechecked(self):
        bad = artifact()
        bad["metrics"]["fantlab.general.characters"]["raw_delta"] = 3
        with self.assertRaisesRegex(report.FrozenDiagnosticReportError, "raw_delta"):
            report.validate_artifact(bad)

    def test_missing_actual_cannot_have_delta(self):
        bad = artifact()
        bad["metrics"]["fantlab.vocabulary.active_dictionary"]["raw_delta"] = 0
        with self.assertRaisesRegex(report.FrozenDiagnosticReportError, "without actual"):
            report.validate_artifact(bad)

    def test_not_run_cannot_have_actual(self):
        bad = artifact()
        row = bad["metrics"]["fantlab.vocabulary.active_dictionary"]
        row["actual"] = 5
        row["raw_delta"] = 0
        with self.assertRaisesRegex(report.FrozenDiagnosticReportError, "not_run"):
            report.validate_artifact(bad)

    def test_pass_or_fail_is_rejected_for_source_unmatched_artifact(self):
        for result in ("pass", "fail"):
            bad = artifact()
            bad["metrics"]["fantlab.general.characters"]["result"] = result
            with self.subTest(result=result):
                with self.assertRaisesRegex(report.FrozenDiagnosticReportError, "overclaim"):
                    report.validate_artifact(bad)

    def test_source_text_flags_fail_closed(self):
        for key in ("source_text_committed", "source_text_uploaded"):
            bad = artifact()
            bad["evidence"][key] = True
            with self.subTest(key=key):
                with self.assertRaises(report.FrozenDiagnosticReportError):
                    report.validate_artifact(bad)

    def test_source_edition_and_m2_must_remain_open(self):
        bad = artifact()
        bad["epistemic_status"]["fantlab_source_edition_match"] = "exact"
        with self.assertRaisesRegex(report.FrozenDiagnosticReportError, "source edition"):
            report.validate_artifact(bad)
        bad = artifact()
        bad["epistemic_status"]["m2_parity_admissible"] = True
        with self.assertRaisesRegex(report.FrozenDiagnosticReportError, "M2 parity"):
            report.validate_artifact(bad)

    def test_html_groups_metric_families_and_preserves_unknown_as_dash(self):
        rendered = report.render_html(artifact(), title="Example")
        self.assertIn("<h2>General</h2>", rendered)
        self.assertIn("<h2>Vocabulary</h2>", rendered)
        self.assertIn("<h2>Punctuation</h2>", rendered)
        self.assertIn("—", rendered)
        self.assertIn("not_run", rendered)

    def test_html_escapes_artifact_controlled_text(self):
        value = artifact()
        value["observations"] = ["<script>alert(1)</script>"]
        rendered = report.render_html(value, title="<img src=x onerror=alert(2)>")
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("&lt;img", rendered)
        self.assertNotIn("<script", rendered.lower())
        self.assertNotIn("<img", rendered.lower())

    def test_html_is_offline_accessible_and_has_no_remote_assets(self):
        rendered = report.render_html(artifact())
        self.assertNotIn("<link", rendered.lower())
        self.assertNotIn("<script", rendered.lower())
        self.assertIn('scope="row"', rendered)
        self.assertIn(":focus-visible", rendered)
        self.assertIn("prefers-reduced-motion", rendered)

    def test_same_artifact_renders_byte_identically(self):
        value = artifact()
        self.assertEqual(
            report.render_html(value),
            report.render_html(copy.deepcopy(value)),
        )

    def test_non_finite_values_fail_closed(self):
        bad = artifact()
        bad["metrics"]["fantlab.general.characters"]["actual"] = float("nan")
        with self.assertRaisesRegex(report.FrozenDiagnosticReportError, "finite"):
            report.validate_artifact(bad)

    def test_cli_is_create_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "diagnostic.json"
            output = root / "report.html"
            source.write_text(json.dumps(artifact()), encoding="utf-8")
            self.assertEqual(
                report.main([str(source), "--output", str(output)]),
                0,
            )
            self.assertIn("<!doctype html>", output.read_text(encoding="utf-8"))
            with self.assertRaises(SystemExit):
                report.main([str(source), "--output", str(output)])


    def test_canonical_repository_diagnostic_is_unchanged_and_readable(self):
        source = Path(__file__).resolve().parents[1] / "benchmarks/fantlab/work270306-wikisource-diagnostic.json"
        raw = source.read_bytes()
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        self.assertEqual(sha, "0d5e420abb45e2b9e178df75a479ab7cdd5a4150")
        value = json.loads(raw)
        self.assertEqual(report.summarize(value), {
            "metric_count": 28, "actual_count": 23, "missing_actual_count": 5,
            "unresolved_count": 26, "not_run_count": 2,
        })
        rendered = report.render_html(value)
        self.assertEqual(rendered.count('scope="row"'), 28)
        self.assertIn("1,705,605", rendered)
        self.assertIn("0/5", rendered)
        self.assertIn(value["evidence"]["normalized_sha256"], rendered)

    def test_generic_title_comes_from_candidate_not_anna(self):
        rendered = report.render_html(artifact())
        self.assertIn("fixture-work", rendered)
        self.assertNotIn("Anna Karenina", rendered)

    def test_bad_status_type_has_controlled_error(self):
        value = artifact()
        value["metrics"]["fantlab.general.characters"]["result"] = []
        with self.assertRaises(report.FrozenDiagnosticReportError):
            report.validate_artifact(value)

    def test_huge_numeric_value_has_controlled_error(self):
        value = artifact()
        value["metrics"]["fantlab.general.characters"]["expected"] = 10 ** 1000
        with self.assertRaises(report.FrozenDiagnosticReportError):
            report.validate_artifact(value)

    def test_large_integer_delta_does_not_lose_precision(self):
        value = artifact()
        row = value["metrics"]["fantlab.general.characters"]
        row.update(expected=2 ** 53, actual=2 ** 53 + 1, raw_delta=1)
        report.validate_artifact(value)
        self.assertIn("9,007,199,254,740,993", report.render_html(value))
        row["raw_delta"] = 0
        with self.assertRaises(report.FrozenDiagnosticReportError):
            report.validate_artifact(value)

    def test_tiny_nonzero_delta_does_not_display_as_zero(self):
        self.assertEqual(report._signed(1e-10), "+1e-10")
        self.assertEqual(report._signed(-1e-10), "-1e-10")

    def test_noncanonical_reference_paths_fail_closed(self):
        for path in ("../secret.json", "a/../b.json", "C:/secret.json",
                     "C:\\secret.json", "a//b.json", "a/./b.json", " a/b.json"):
            value = artifact()
            value["evidence"]["reference_path"] = path
            with self.subTest(path=path):
                with self.assertRaises(report.FrozenDiagnosticReportError):
                    report.validate_artifact(value)

    def test_cli_rejects_duplicate_keys_without_creating_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, output = root / "input.json", root / "out.html"
            source.write_text('{"artifact_version": "bad", "artifact_version": "other"}', encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()) as errors:
                with self.assertRaises(SystemExit) as raised:
                    report.main([str(source), "--output", str(output)])
            self.assertEqual(raised.exception.code, 2)
            self.assertIn("duplicate JSON key", errors.getvalue())
            self.assertFalse(output.exists())

    def test_invalid_artifact_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, output = root / "input.json", root / "out.html"
            source.write_text("{}", encoding="utf-8")
            output.write_text("last valid report", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    report.main([str(source), "--output", str(output)])
            self.assertEqual(output.read_text(encoding="utf-8"), "last valid report")

    def test_table_keyboard_access_units_and_historical_boundary(self):
        rendered = report.render_html(artifact())
        self.assertIn('href="#metrics"', rendered)
        self.assertIn('id="metrics"', rendered)
        self.assertIn('tabindex="0" role="region"', rendered)
        self.assertIn('<caption>', rendered)
        self.assertIn('scope="col"', rendered)
        self.assertIn("events / 1,000 words", rendered)
        self.assertIn("Historical snapshot, not a new analyzer run", rendered)
        self.assertIn("Missing is not zero", rendered)


if __name__ == "__main__":
    unittest.main()
