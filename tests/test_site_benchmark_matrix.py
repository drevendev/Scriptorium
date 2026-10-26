"""Regression tests for the source-free public FantLab evidence page."""
import copy
import hashlib
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from scriptorium import site_benchmark_matrix as page


ROOT = Path(__file__).resolve().parents[1]


class FantLabEvidencePageTests(unittest.TestCase):
    def test_registered_real_report_is_source_free_and_explicit(self):
        registration = json.loads(
            (ROOT / "site/publication-manifest.json").read_text(encoding="utf-8")
        )
        entry = next(e for e in registration["entries"] if e.get("kind") == "benchmark_matrix")
        page.validate_entry(entry)
        published = page.build(ROOT)
        content = published["body"]
        self.assertEqual(content.count('class="source-row"'), 5)
        self.assertEqual(content.count('class="metric-row" data-metric-family='), 28)
        self.assertEqual(content.count('class="wave-metric-row"'), 27)
        self.assertEqual(content.count('class="silver-metric-row"'), 29)
        self.assertIn('aria-label="Silver Dove diagnostic fields"', content)
        self.assertIn('id="silver-metric-rows"', content)
        self.assertIn('href="#silver-title">Explore Silver Dove', content)
        self.assertIn('only two FantLab reference counts', content)
        self.assertIn('Silver Dove: 29 retained Scriptorium fields', content)
        self.assertEqual(content.count('data-metric-family="punctuation"'), 56)
        self.assertEqual(content.count('id="wave-metric-rows"'), 1)
        self.assertIn('id="wave-metric-filters"', content)
        self.assertIn('aria-controls="wave-metric-rows"', content)
        self.assertIn("Running on Waves: 27 retained diagnostic rows", content)
        self.assertIn('aria-label="Running on Waves metric differences"', content)
        self.assertEqual(content.count('class="cross-metric-row" data-metric-family='), 20)
        self.assertIn('aria-label="Two-work normalized diagnostic comparison"', content)
        self.assertIn('id="shared-scroll"', content)
        self.assertIn("Compare measured rates across two works", content)
        self.assertIn("Running on Waves minus Anna Karenina", content)
        self.assertIn("denominator compatibility and rounding remain unverified", content)
        self.assertIn("Missing measurements are omitted here, not replaced with zero", content)
        self.assertIn("four dictionary-dependent metrics not run", content)
        self.assertIn("360987</td><td>363819</td><td>2832", content)
        # Five sources, 55 individual metrics, 20 cross-work rows, four summaries.
        self.assertEqual(content.count('scope="row"'), 113)
        self.assertEqual(content.count('<span lang="ru">'), 104)
        self.assertIn('<nav id="metric-families" aria-label="Metric families">', content)
        for family, count in (("dialogue", 4), ("general", 4),
                              ("punctuation", 14), ("vocabulary", 6)):
            anchor_state = "not_run" if family == "vocabulary" else "measured"
            self.assertIn(
                f'<a href="#metric-family-{family}">{family.title()} ({count})</a>',
                content,
            )
            self.assertIn(
                f'data-metric-family="{family}" data-metric-state="{anchor_state}" '
                f'id="metric-family-{family}" tabindex="-1">',
                content,
            )
        # Four family jump targets plus the family-filter control ID.
        self.assertEqual(content.count('id="metric-family-'), 5)
        self.assertEqual(content.count('class="coverage-row"'), 4)
        self.assertIn('Measurement availability by family', content)
        self.assertIn('Vocabulary</a></th><td>1</td><td>2</td><td>3</td><td>6</td>', content)
        self.assertIn('Dialogue</a></th><td>4</td><td>0</td><td>0</td><td>4</td>', content)
        self.assertIn('General</a></th><td>4</td><td>0</td><td>0</td><td>4</td>', content)
        self.assertIn('Punctuation</a></th><td>14</td><td>0</td><td>0</td><td>14</td>', content)
        self.assertEqual(content.count('aria-label="Metric-family measurement coverage"'), 1)
        self.assertIn('<span lang="ru">Длина текста, знаков</span>', content)
        self.assertIn('<code>fantlab.general.characters</code>', content)
        self.assertIn('<th scope="col">Metric ID</th><th scope="col">Unit</th>', content)
        self.assertEqual(content.count('occurrences / 1,000 word tokens</td>'), 56)
        self.assertIn('mean unique forms / 3,000-token window</td>', content)
        self.assertIn('mean unique forms / 10,000-token window</td>', content)
        self.assertIn('mean unique forms / 100,000-token window</td>', content)
        self.assertIn('Percentage-value differences are in percentage points', content)
        self.assertIn('characters including spaces</td>', content)
        self.assertIn("Input identity unverified", content)
        self.assertIn("Actual value unavailable", content)
        self.assertIn("UNRESOLVED_SOURCE", content)
        self.assertIn("M2: 0/5", content)
        self.assertIn("Three works have retained metric observations", content)
        self.assertIn("Frozen:</strong> 1,705,605", content)
        self.assertIn("FantLab displayed:</strong> 1,692,647", content)
        self.assertIn("Δ:</strong> +12,958", content)
        self.assertIn("Relative drift:</strong> +0.77%", content)
        self.assertEqual(content.count("Relative drift:</strong>"), 5)
        self.assertIn("rounded to two decimal places", content)
        self.assertEqual(content.count("Public-domain source ↗"), 5)
        self.assertIn("NOT_RUN", content)
        self.assertIn("UNKNOWN", content)
        self.assertIn('aria-describedby="metrics-scroll"', content)
        self.assertIn('<script src="../../assets/metric-filter.js" defer></script>', content)
        self.assertIn('<script src="../../assets/shared-metric-filter.js" defer></script>', content)
        self.assertEqual(content.count("<script"), 2)
        self.assertEqual(content.count('data-metric-state="measured"'), 70)
        self.assertEqual(content.count('data-metric-state="not_run"'), 11)
        self.assertEqual(content.count('data-metric-state="unavailable"'), 3)
        self.assertIn('id="metric-filters"', content)
        self.assertIn('id="retained-metric-rows"', content)
        self.assertNotIn("source prose", content)
        self.assertEqual(json.loads(published["json"])["m2_source_matched_pass_count"], 0)
        self.assertIn("12958", published["csv"])
        self.assertIn("14075", published["csv"])
        self.assertIn("MEASURED_NO_REFERENCE", published["json"])
        self.assertIn('href="readiness.json" download', content)
        self.assertIn('href="readiness.csv" download', content)
        source_report = json.loads(published["readiness_json"])
        self.assertEqual(source_report["works_reported"], 5)
        self.assertEqual(source_report["m2_source_matched_pass_count"], 0)
        self.assertEqual(len(source_report["entries"]), 5)
        for entry in source_report["entries"]:
            self.assertEqual(len(entry["source"]["raw_sha256"]), 64)
            self.assertEqual(len(entry["source"]["normalized_sha256"]), 64)
            self.assertEqual(entry["exact_fantlab_input_identity"], "UNKNOWN")
        self.assertEqual(
            published["readiness_json"],
            page.benchmark_readiness.render_report(page.benchmark_readiness.build_readiness(ROOT), "json"),
        )
        self.assertEqual(
            published["readiness_csv"],
            page.benchmark_readiness.render_report(page.benchmark_readiness.build_readiness(ROOT), "csv"),
        )
        self.assertEqual(page.build(ROOT), published)


    def test_silver_dove_unknowns_are_not_parity_and_invalid_rows_fail_closed(self):
        real = page.matrix.build_metric_matrix(ROOT)
        for row in real["entries"][2]["metric_rows"]:
            if row["expected"] is None:
                self.assertIsNone(row["actual_minus_expected"])
        content = page.build(ROOT)["body"]
        self.assertIn("26 further FantLab-shaped references are UNKNOWN", content)
        self.assertIn(
            "N/A (extension)</td><td>6219</td><td>N/A (extension)</td>"
            "<td>Scriptorium extension; no FantLab counterpart", content
        )
        self.assertNotIn("other 27 reference values", content)
        changed = copy.deepcopy(real)
        target = changed["entries"][2]["metric_rows"][0]
        target["expected"] = 0
        with patch.object(page.matrix, "build_metric_matrix", return_value=changed):
            with self.assertRaisesRegex(ValueError, "fabricated"):
                page.build(ROOT)
        changed = copy.deepcopy(real)
        changed["entries"][2]["metric_rows"][28]["comparison_kind"] = "DIAGNOSTIC_ONLY"
        with patch.object(page.matrix, "build_metric_matrix", return_value=changed):
            with self.assertRaisesRegex(ValueError, "extension classification"):
                page.build(ROOT)

    def test_metric_units_match_all_versioned_retained_fields(self):
        self.assertEqual(set(page._VALUE_UNITS), set(page._METRIC_PRESENTATION))
        self.assertEqual(len(page._VALUE_UNITS), 28)
        self.assertEqual(page._VALUE_UNITS["fantlab.dialogue.share_percent"], "%")
        self.assertEqual(page._VALUE_UNITS["fantlab.vocabulary.unique_words"],
                         "unique word forms")
        self.assertNotIn("fantlab.future.unverified", page._VALUE_UNITS)
        self.assertTrue(all(unit and isinstance(unit, str)
                            for unit in page._VALUE_UNITS.values()))

    def test_canonical_site_packages_source_provenance_with_receipt_hashes(self):
        from scriptorium.site_renderer import build_site

        build_dir = ROOT / "build"
        build_dir.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="test-source-evidence-", dir=build_dir) as temporary:
            destination = Path(temporary) / "site"
            receipt = build_site(ROOT, destination)
            published = page.build(ROOT)
            evidence = destination / "evidence" / "fantlab"
            from scriptorium.site_metric_filter import FILTER_JS
            self.assertEqual((destination / "assets" / "metric-filter.js").read_text(encoding="utf-8"), FILTER_JS)
            from scriptorium.site_shared_metric_filter import JS as SHARED_FILTER_JS
            self.assertEqual((destination / "assets" / "shared-metric-filter.js").read_text(encoding="utf-8"), SHARED_FILTER_JS)
            for name, key in (("readiness.json", "readiness_json"),
                              ("readiness.csv", "readiness_csv"),
                              ("shared-rates.json", "shared_json"),
                              ("shared-rates.csv", "shared_csv")):
                self.assertEqual((evidence / name).read_text(encoding="utf-8"), published[key])
            row = next(item for item in receipt["entries"]
                       if item["entry_id"] == page.EXPECTED_ENTRY["entry_id"])
            for label, key in (("readiness_json_sha256", "readiness_json"),
                               ("readiness_csv_sha256", "readiness_csv"),
                               ("shared_json_sha256", "shared_json"),
                               ("shared_csv_sha256", "shared_csv")):
                self.assertEqual(row[label], hashlib.sha256(published[key].encode("utf-8")).hexdigest())
            self.assertEqual((evidence / "metrics.json").read_text(encoding="utf-8"), published["json"])
            self.assertEqual((evidence / "metrics.csv").read_text(encoding="utf-8"), published["csv"])

    def test_signed_relative_drift_rounding_and_invalid_denominator(self):
        self.assertEqual(page._relative_character_delta(12_958, 1_692_647), "+0.77%")
        self.assertEqual(page._relative_character_delta(-100, 1_000), "-10.00%")
        self.assertEqual(page._relative_character_delta(100, 1_000), "+10.00%")
        self.assertEqual(page._relative_character_delta(0, 1_000), "0.00%")
        self.assertEqual(page._relative_character_delta(-1, 1_000_000), "-0.00%")
        for delta, denominator in ((1, 0), (True, 100), (1, True)):
            with self.subTest(delta=delta, denominator=denominator):
                with self.assertRaisesRegex(ValueError, "relative character-count"):
                    page._relative_character_delta(delta, denominator)

    def test_source_readiness_mismatch_and_unsafe_links_fail_closed(self):
        metric_report = page.matrix.build_metric_matrix(ROOT)
        readiness = page.benchmark_readiness.build_readiness(ROOT)

        def attempt(mutate):
            altered = copy.deepcopy(readiness)
            mutate(altered)
            with patch.object(page.matrix, "build_metric_matrix", return_value=metric_report):
                with patch.object(page.benchmark_readiness, "build_readiness", return_value=altered):
                    return page.build(ROOT)

        with self.assertRaisesRegex(ValueError, "source readiness and metric matrix disagree"):
            attempt(lambda r: r["entries"][0]["source"].__setitem__("raw_sha256", "f" * 64))
        with self.assertRaisesRegex(ValueError, "invalid source readiness diagnostic"):
            attempt(lambda r: r["entries"][0]["character_count_diagnostic"].__setitem__("actual_minus_expected", 0))
        with self.assertRaisesRegex(ValueError, "source readiness and metric matrix disagree"):
            attempt(lambda r: r["entries"][0]["fantlab"].__setitem__("reference_url", "https://fantlab.ru/work1/lp"))
        with self.assertRaisesRegex(ValueError, "unsafe public source URL"):
            attempt(lambda r: r["entries"][0]["source"].__setitem__("url", "javascript:alert(1)"))
        escaped = attempt(lambda r: r["entries"][0]["source"].__setitem__("edition", "<script>x</script>"))
        self.assertIn("&lt;script&gt;x&lt;/script&gt;", escaped["body"])
        self.assertNotIn("<script>x</script>", escaped["body"])

    def test_coverage_rejects_inconsistent_retained_measurement_count(self):
        real = page.matrix.build_metric_matrix(ROOT)
        changed = copy.deepcopy(real)
        row = next(r for r in changed["entries"][0]["metric_rows"] if r["actual"] is not None)
        row["actual"] = None
        row["actual_minus_expected"] = None
        row["result"] = "NOT_RUN"
        with patch.object(page.matrix, "build_metric_matrix", return_value=changed):
            with self.assertRaisesRegex(ValueError, "metric-family coverage disagrees"):
                page.build(ROOT)

    def test_undeclared_status_upgrade_fails_closed(self):
        entry = dict(page.EXPECTED_ENTRY)
        entry["benchmark_admissibility"] = "admissible"
        with self.assertRaisesRegex(ValueError, "registration"):
            page.validate_entry(entry)
        entry = dict(page.EXPECTED_ENTRY)
        entry["source_text_included"] = True
        with self.assertRaisesRegex(ValueError, "registration"):
            page.validate_entry(entry)

    def test_report_cannot_promote_parity_or_fabricate_missing_runs(self):
        real = page.matrix.build_metric_matrix(ROOT)
        changed = copy.deepcopy(real)
        changed["m2_source_matched_pass_count"] = 1
        with patch.object(page.matrix, "build_metric_matrix", return_value=changed):
            with self.assertRaisesRegex(ValueError, "publication gate"):
                page.build(ROOT)
        changed = copy.deepcopy(real)
        absent = next(e for e in changed["entries"] if e["metric_evidence"] == "NOT_RUN")
        absent["metric_rows"] = [{"metric_id": "invented"}]
        with patch.object(page.matrix, "build_metric_matrix", return_value=changed):
            with self.assertRaisesRegex(ValueError, "fabricated rows"):
                page.build(ROOT)

    def test_no_unrecognized_metric_or_scientific_status_in_public_html(self):
        real = page.matrix.build_metric_matrix(ROOT)
        changed = copy.deepcopy(real)
        changed["entries"][0]["metric_rows"][0]["result"] = "PASS"
        with patch.object(page.matrix, "build_metric_matrix", return_value=changed):
            with self.assertRaisesRegex(ValueError, "scientific status"):
                page.build(ROOT)
        changed = copy.deepcopy(real)
        changed["entries"][0]["metric_rows"][0]["metric_id"] = "unrecognized.id"
        with patch.object(page.matrix, "build_metric_matrix", return_value=changed):
            with self.assertRaisesRegex(ValueError, "unrecognized FantLab metric"):
                page.build(ROOT)

    def test_escaping_and_reference_url_validation(self):
        real = page.matrix.build_metric_matrix(ROOT)
        changed = copy.deepcopy(real)
        changed["entries"][0]["title"] = '<img src=x onerror=alert(1)>'
        with patch.object(page.matrix, "build_metric_matrix", return_value=changed):
            rendered = page.build(ROOT)["body"]
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", rendered)
        self.assertNotIn("<img", rendered)
        changed = copy.deepcopy(real)
        changed["entries"][0]["reference_url"] = "javascript:alert(1)"
        with patch.object(page.matrix, "build_metric_matrix", return_value=changed):
            with self.assertRaisesRegex(ValueError, "unsafe FantLab reference"):
                page.build(ROOT)


    def test_cross_work_rates_have_precise_signed_deltas_not_parity(self):
        from decimal import Decimal

        report = page.matrix.build_metric_matrix(ROOT)
        anna = next(e for e in report["entries"] if e["candidate_id"] == "tolstoy-anna-karenina-ru")
        waves = next(e for e in report["entries"] if e["candidate_id"] == "grin-running-on-waves-ru")
        rows = page._shared_normalized_rows(anna["metric_rows"], waves["metric_rows"])
        self.assertEqual(len(rows), 20)
        ids = {row["metric_id"] for row in rows}
        self.assertEqual(len(ids), len(rows))
        self.assertNotIn("fantlab.general.characters", ids)
        self.assertNotIn("fantlab.general.words", ids)
        self.assertNotIn("fantlab.vocabulary.unique_words", ids)
        self.assertNotIn("fantlab.vocabulary.uasz_3000", ids)
        self.assertIn("fantlab.dialogue.share_percent", ids)
        self.assertIn("fantlab.punctuation.dash.per_1000_words", ids)
        self.assertEqual(len([r for r in rows if r["family"] == "Punctuation"]), 14)
        for row in rows:
            self.assertEqual(
                Decimal(row["right_minus_left"]),
                Decimal(str(row["right"])) - Decimal(str(row["left"])),
            )
            self.assertEqual(
                row["difference_unit"],
                "percentage points" if row["unit"] == "%" else row["unit"],
            )
        self.assertEqual(
            page.build(ROOT)["json"],
            page.matrix.render_metric_matrix(report, "json"),
        )

    def test_cross_work_comparison_refuses_fabricated_numeric_states(self):
        metric_id = "fantlab.dialogue.share_percent"
        a = {"metric_id": metric_id, "actual": 12.5, "result": "UNRESOLVED_SOURCE"}
        b = {"metric_id": metric_id, "actual": 13.0, "result": "UNRESOLVED_SOURCE"}
        rows = page._shared_normalized_rows([a], [b])
        self.assertEqual(rows[0]["right_minus_left"], "+0.5")
        self.assertEqual(rows[0]["difference_unit"], "percentage points")
        self.assertEqual(page._shared_normalized_rows([a], [
            {**b, "actual": None, "result": "NOT_RUN"},
        ]), [])
        with self.assertRaisesRegex(ValueError, "duplicate cross-work"):
            page._shared_normalized_rows([a, a], [b])
        with self.assertRaisesRegex(ValueError, "promoted to parity"):
            page._shared_normalized_rows([a], [{**b, "result": "PASS"}])
        with self.assertRaisesRegex(ValueError, "invalid cross-work numeric"):
            page._shared_normalized_rows([a], [{**b, "actual": True}])
        with self.assertRaisesRegex(ValueError, "non-finite cross-work"):
            page._shared_normalized_rows([a], [{**b, "actual": float("nan")}])


    def test_shared_rate_exports_are_deterministic_and_scientifically_limited(self):
        import csv
        from decimal import Decimal
        from io import StringIO

        rendered = page.build(ROOT)
        doc = json.loads(rendered["shared_json"])
        self.assertEqual(doc["schema_version"], "scriptorium-shared-rate-comparison-v1")
        self.assertEqual(doc["evidence_class"], "diagnostic_source_unmatched")
        self.assertEqual(doc["comparison_direction"], "running_on_waves_minus_anna_karenina")
        self.assertFalse(doc["m2_parity_admissible"])
        self.assertEqual(doc["m2_weight"], 0)
        self.assertEqual([work["fantlab_input_identity"] for work in doc["works"]],
                         ["UNKNOWN", "UNKNOWN"])
        self.assertEqual([work["candidate_id"] for work in doc["works"]],
                         ["tolstoy-anna-karenina-ru", "grin-running-on-waves-ru"])
        self.assertTrue(all(len(work["frozen_raw_sha256"]) == 64 for work in doc["works"]))
        self.assertEqual(len(doc["measurements"]), 20)
        self.assertEqual(len({row["metric_id"] for row in doc["measurements"]}), 20)
        for row in doc["measurements"]:
            self.assertEqual(Decimal(row["right_minus_left"]),
                             Decimal(str(row["right"])) - Decimal(str(row["left"])))
            self.assertEqual(row["difference_unit"],
                             "percentage points" if row["unit"] == "%" else row["unit"])
        self.assertTrue(all(row["metric_id"] not in {
            "fantlab.general.characters", "fantlab.general.words",
            "fantlab.vocabulary.unique_words",
        } for row in doc["measurements"]))
        csv_rows = list(csv.DictReader(StringIO(rendered["shared_csv"])))
        self.assertEqual(len(csv_rows), 20)
        self.assertEqual([row["metric_id"] for row in csv_rows],
                         [row["metric_id"] for row in doc["measurements"]])
        self.assertTrue(all(row["fantlab_input_identity"] == "UNKNOWN"
                            and row["evidence_class"] == "diagnostic_source_unmatched"
                            for row in csv_rows))
        for csv_row in csv_rows:
            for side, work in (("left", doc["works"][0]), ("right", doc["works"][1])):
                self.assertEqual(csv_row[f"{side}_fantlab_reference_url"],
                                 work["fantlab_reference_url"])
                self.assertEqual(csv_row[f"{side}_fantlab_reference_date"],
                                 work["fantlab_reference_date"])
            self.assertEqual(csv_row["schema_version"], doc["schema_version"])
            self.assertEqual(csv_row["m2_parity_admissible"], "false")
            self.assertEqual(csv_row["m2_weight"], "0")
        self.assertEqual(rendered["shared_json"], page.build(ROOT)["shared_json"])
        self.assertIn('href="shared-rates.json" download', rendered["body"])
        self.assertIn('href="shared-rates.csv" download', rendered["body"])
        self.assertNotIn("SECRET SOURCE PROSE", rendered["shared_json"])

    def test_shared_rate_export_refuses_duplicate_or_upgraded_identity(self):
        report = page.matrix.build_metric_matrix(ROOT)
        anna = next(e for e in report["entries"] if e["candidate_id"] == "tolstoy-anna-karenina-ru")
        wave = next(e for e in report["entries"] if e["candidate_id"] == "grin-running-on-waves-ru")
        rows = page._shared_normalized_rows(anna["metric_rows"], wave["metric_rows"])
        with self.assertRaisesRegex(ValueError, "twenty distinct"):
            page._shared_rate_exports(rows + [rows[0]], anna, wave)
        altered = dict(anna, exact_fantlab_input_identity="EXACT")
        with self.assertRaisesRegex(ValueError, "proven FantLab input identity"):
            page._shared_rate_exports(rows, altered, wave)


if __name__ == "__main__":
    unittest.main()
