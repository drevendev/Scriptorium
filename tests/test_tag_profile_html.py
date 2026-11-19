"""Offline tag visualisation: source-free, accessible and fail-closed."""
from copy import deepcopy
from io import StringIO
from pathlib import Path
import contextlib
import json
import tempfile
import unittest

from scriptorium.tag_profile import FEATURES, VERSION, main
from scriptorium.tag_profile_html import render_tag_profiles_html


def report():
    works = [{"key": "a", "candidate_id": "candidate-a", "edition_id": "edition-a",
              "source_sha256": "a" * 64, "rights_basis": "public_domain",
              "rights_evidence_url": "https://example.org/rights/a",
              "tag_authority": "documented_source", "tag_evidence_url": "https://example.org/tags/a"},
             {"key": "b", "candidate_id": "candidate-b", "edition_id": "edition-b",
              "source_sha256": "b" * 64, "rights_basis": "public_domain",
              "rights_evidence_url": "https://example.org/rights/b",
              "tag_authority": "human_curator", "tag_evidence_url": "https://example.org/tags/b"}]
    def metric_rows(n):
        return [{"id": key, "unit": unit, "observed_count": n if i == 0 else 0,
                 "missing_count": 0 if i == 0 else n,
                 "mean_per_work": 4.7 if i == 0 and n else None,
                 "population_stddev_between_works": 0.5 if i == 0 and n > 1 else None,
                 "minimum": 4.2 if i == 0 and n else None,
                 "maximum": 5.2 if i == 0 and n > 1 else (4.7 if i == 0 and n else None)}
                for i, (key, unit) in enumerate(FEATURES.items())]
    tags = [{"tag_id": "historical", "label": "Historical fiction", "confirmed_work_count": 2,
             "sample_warning": "DESCRIPTIVE_ONLY", "works": works, "metrics": metric_rows(2)},
            {"tag_id": "science", "label": "Science", "confirmed_work_count": 0,
             "sample_warning": "NO_CONFIRMED_WORKS", "works": [], "metrics": metric_rows(0)}]
    return {"schema_version": VERSION, "taxonomy_version": "curation-v1",
            "source_snapshot_sha256": "f" * 64, "source_metric_profiles": {"metrics": "v1"},
            "aggregation": "unweighted", "scientific_boundary": {
                "class": "private_curator_declared_descriptive_extension",
                "public_release_ready": False, "rights_independently_verified": False,
                "fantlab_parity": False, "m2_source_matched": 0, "no_source_text": True},
            "tags": tags}


class TagProfileHtmlTests(unittest.TestCase):
    def test_real_numerics_missing_and_no_data_are_distinct(self):
        html = render_tag_profiles_html(report())
        self.assertIn("4.7", html)
        self.assertIn("4.2–5.2", html)
        self.assertIn("2 / 0", html)
        self.assertIn("0 / 2", html)
        self.assertIn("No confirmed editions", html)
        self.assertIn("NOT_RUN", html)
        self.assertIn('scope="row"', html)
        self.assertIn('scope="col"', html)
        self.assertIn('tabindex="0"', html)
        self.assertIn('@media print', html)
        self.assertIn("default-src 'none'", html)
        self.assertNotIn('<script', html.lower())
        self.assertNotIn('<a ', html.lower())
        self.assertNotIn('http-equiv="refresh"', html.lower())
        self.assertEqual(html, render_tag_profiles_html(report()))

    def test_html_escaping_and_source_free(self):
        r = report()
        r["tags"][0]["label"] = '<img src=x onerror=alert(1)>'
        r["taxonomy_version"] = 'curation<script>alert(1)</script>'
        r["tags"][0]["works"][0]["edition_id"] = 'edition</li><script>bad()</script>'
        html = render_tag_profiles_html(r)
        self.assertIn('&lt;img src=x onerror=alert(1)&gt;', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>', html)
        self.assertNotIn('<img ', html)
        self.assertNotIn('PRIVATE MANUSCRIPT', html)

    def test_rejects_false_scientific_gate_and_corrupt_numbers(self):
        r = report()
        r["scientific_boundary"]["public_release_ready"] = True
        with self.assertRaisesRegex(ValueError, "boundary"):
            render_tag_profiles_html(r)
        r = report()
        r["tags"][0]["metrics"][0]["missing_count"] = 1
        with self.assertRaisesRegex(ValueError, "missingness"):
            render_tag_profiles_html(r)
        r = report()
        r["tags"][0]["metrics"][0]["mean_per_work"] = float('nan')
        with self.assertRaisesRegex(ValueError, "range"):
            render_tag_profiles_html(r)
        r = report()
        r["tags"][0]["metrics"][0]["unit"] = "%"
        with self.assertRaisesRegex(ValueError, "unit"):
            render_tag_profiles_html(r)
        r = report()
        r["tags"][1]["metrics"][0]["mean_per_work"] = 0
        with self.assertRaisesRegex(ValueError, "unobserved"):
            render_tag_profiles_html(r)
        r = report()
        r["tags"][0]["works"][0]["source_sha256"] = "unknown"
        with self.assertRaisesRegex(ValueError, "hash"):
            render_tag_profiles_html(r)

    def test_metric_specific_bars_show_real_means_zero_and_missing(self):
        r = report()
        # Same metric across tags shares one scale; different metrics never mix units.
        r["tags"][0]["metrics"][2].update(
            observed_count=2, missing_count=0, mean_per_work=25.0,
            minimum=0.0, maximum=50.0, population_stddev_between_works=25.0)
        r["tags"][0]["metrics"][3].update(
            observed_count=2, missing_count=0, mean_per_work=0.0,
            minimum=0.0, maximum=0.0, population_stddev_between_works=0.0)
        html = render_tag_profiles_html(r)
        self.assertEqual(html.count('class="metric-chart"'), 5)
        self.assertIn("Fixed domain 0–100 %", html)
        self.assertIn("highest observed tag mean", html)
        self.assertIn("all observed means are zero", html)
        self.assertIn("NOT_RUN for every tag", html)
        self.assertIn('style="width:100.00%"', html)  # 4.7 character mean vs observed maximum
        self.assertIn('style="width:25.00%"', html)   # 25% on fixed 0..100 domain
        self.assertIn('style="width:0.00%"', html)    # measured zero is not missing
        self.assertIn('aria-hidden="true"', html)  # decorative bars; exact table/labels remain
        self.assertIn("0.0 per 1000 words · 2 observed / 0 missing", html)
        self.assertIn("NOT_RUN · 0 observed / 0 missing", html)
        self.assertNotIn("<script", html.lower())

    def test_chart_escapes_hostile_labels_without_untrusted_styles(self):
        r = report()
        r["tags"][0]["label"] = '<svg onload="alert(1)">'
        html = render_tag_profiles_html(r)
        self.assertNotIn("<svg", html)
        self.assertIn('&lt;svg onload=&quot;alert(1)&quot;&gt;', html)
        self.assertEqual(html.count('style="width:'), 1)
        self.assertEqual(html.count('class="metric-chart"'), len(FEATURES))


    def test_cli_html_is_create_only_and_json_remains_default(self):
        # Synthetic curation only. No actual book/tag admission is implied.
        snap = {"schema": "scriptorium-ru-reader-v2", "scientific_claim": "DIAGNOSTIC_ONLY",
                "fantlab_input_identity": "UNKNOWN", "counts": {"m2_source_matched": 0},
                "comparability": {"m2_parity_admissible": False},
                "books": [{"key": "a", "candidate_id": "work-a", "edition_id": "edition-a",
                           "source_sha256": "a" * 64, "language": "ru", "translator": None,
                           "text_status": "measured", "profiles": {"metrics": "scriptorium-metrics-v4"},
                           "metrics": [{"id": "fantlab.general.characters", "actual": 350000,
                                        "status": "measured", "kind": "candidate"}]}]}
        cur = {"schema": "scriptorium-tag-curation-v1", "taxonomy_version": "curated-tags-v1",
               "tags": [{"id": "historical", "label": "Historical fiction"}],
               "editions": [{"key": "a", "candidate_id": "work-a", "edition_id": "edition-a",
                             "source_sha256": "a" * 64, "language": "ru", "translator": None,
                             "rights": {"basis": "public_domain", "evidence_url": "https://example.org/rights/a", "reviewed": True},
                             "annotations": [{"tag_id": "historical", "authority": "documented_source",
                                              "certainty": "confirmed", "evidence_url": "https://example.org/tag/a"}]}]}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            snapshot, curation, output = root / 'snapshot.json', root / 'curation.json', root / 'profile.html'
            snapshot.write_text(json.dumps(snap), encoding='utf-8')
            curation.write_text(json.dumps(cur), encoding='utf-8')
            args = ['--snapshot', str(snapshot), '--curation', str(curation)]
            with contextlib.redirect_stdout(StringIO()) as stream:
                self.assertEqual(main(args), 0)
            self.assertIn('"schema_version": "scriptorium-tag-profile-preview-v1"', stream.getvalue())
            self.assertEqual(main(args + ['--format', 'html', '--output', str(output)]), 0)
            self.assertIn('<h1>Private curated tag profiles</h1>', output.read_text(encoding='utf-8'))
            with contextlib.redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit) as exc:
                    main(args + ['--format', 'html', '--output', str(output)])
            self.assertEqual(exc.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
