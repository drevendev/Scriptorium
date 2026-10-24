"""Regression tests for the source-free public FantLab evidence page."""
import copy
import json
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
        self.assertEqual(content.count('class="metric-row"'), 28)
        self.assertEqual(content.count('scope="row"'), 33)
        self.assertEqual(content.count('<span lang="ru">'), 28)
        self.assertIn('<nav aria-label="Metric families">', content)
        for family, count in (("dialogue", 4), ("general", 4),
                              ("punctuation", 14), ("vocabulary", 6)):
            self.assertIn(
                f'<a href="#metric-family-{family}">{family.title()} ({count})</a>',
                content,
            )
            self.assertIn(
                f'<tr class="metric-row" id="metric-family-{family}" tabindex="-1">',
                content,
            )
        self.assertEqual(content.count('id="metric-family-'), 4)
        self.assertIn('<span lang="ru">Длина текста, знаков</span>', content)
        self.assertIn('<code>fantlab.general.characters</code>', content)
        self.assertIn("Input identity unverified", content)
        self.assertIn("Actual value unavailable", content)
        self.assertIn("UNRESOLVED_SOURCE", content)
        self.assertIn("M2: 0/5", content)
        self.assertIn("NOT_RUN", content)
        self.assertIn("UNKNOWN", content)
        self.assertIn('aria-describedby="metrics-scroll"', content)
        self.assertNotIn("<script", content)
        self.assertNotIn("source prose", content)
        self.assertEqual(json.loads(published["json"])["m2_source_matched_pass_count"], 0)
        self.assertIn("12958", published["csv"])
        self.assertEqual(page.build(ROOT), published)

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


if __name__ == "__main__":
    unittest.main()
