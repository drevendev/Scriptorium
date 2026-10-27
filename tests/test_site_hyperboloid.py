"""Pin-sensitive regression tests for the full generated Reader Hyperboloid route."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import site_hyperboloid as page
from scriptorium.site_renderer import build_site

ROOT = Path(__file__).resolve().parents[1]


class HyperboloidReaderTests(unittest.TestCase):
    def test_pinned_source_free_measurements_render_with_explicit_unknowns(self):
        result = page.build(ROOT)
        body = result["body"]
        self.assertEqual(body.count('<tr><th scope="row"><code>'), 29)
        self.assertIn("499,066 characters", body)
        self.assertIn("71,921 words", body)
        self.assertIn("24 измеренных показателя", body)
        self.assertIn("5 показателей NOT_RUN", body)
        self.assertIn("M2 parity: 0/5", body)
        self.assertIn("Wikisource revision 5014458", body)
        self.assertIn("measurements.csv", body)
        self.assertNotIn("<script", body)
        self.assertIn("diagnostic_source_unmatched", result["csv"])
        exported = json.loads(result["json"])
        self.assertFalse(exported["source_text_committed"])
        self.assertFalse(exported["m2_parity_admissible"])
        self.assertEqual(len(exported["metric_rows"]), 29)
        self.assertEqual(sum(r["actual"] is not None for r in exported["metric_rows"]), 24)
        self.assertEqual(sum(r["actual"] is None for r in exported["metric_rows"]), 5)
        self.assertEqual(sum(r["reference"] is not None for r in exported["metric_rows"]), 2)
        self.assertEqual(page.build(ROOT), result)

    def test_fail_closed_if_receipt_is_altered_even_when_numeric(self):
        data, raw = page._read_pinned(ROOT)
        modified = copy.deepcopy(data)
        modified["metric_rows"][0]["actual"] += 1
        with patch.object(page, "_read_pinned", return_value=(modified, raw)):
            # A plausible-but-altered observation still fails exact evidence pin.
            # The on-disk blob digest is an independent publication gate.
            with self.assertRaisesRegex(page.HyperboloidBuildError, "source/CI/parity|measurement"):
                # Exact row values are checked at pinned-blob read time, so test
                # a field that the semantic validator independently pins.
                modified["source_body_characters"] = 499067
                page.build(ROOT)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / page.ARTIFACT_PATH
            path.parent.mkdir(parents=True)
            path.write_bytes(raw.replace(b'"m2_parity_admissible": false',
                                         b'"m2_parity_admissible": true'))
            with self.assertRaisesRegex(page.HyperboloidBuildError, "blob digest changed"):
                page.build(Path(directory))

    def test_fail_closed_on_scientific_status_and_missing_values(self):
        data, raw = page._read_pinned(ROOT)
        for mutation, expected_error in (
            (lambda d: d.__setitem__("m2_parity_admissible", True),
             "source/CI/parity"),
            (lambda d: d["metric_rows"][0].__setitem__("reference", 0),
             "reference"),
            (lambda d: d["metric_rows"][0].__setitem__("status", "parity_pass"),
             "measurement"),
            (lambda d: d["metric_rows"][0].__setitem__("actual", float("nan")),
             "measurement"),
            (lambda d: next(r for r in d["metric_rows"] if r["id"] ==
                            "fantlab.vocabulary.active_dictionary").__setitem__(
                                "actual", 0),
             "dictionary-unbound"),
        ):
            modified = copy.deepcopy(data)
            mutation(modified)
            with self.subTest(expected_error=expected_error):
                with patch.object(page, "_read_pinned", return_value=(modified, raw)):
                    with self.assertRaisesRegex(page.HyperboloidBuildError, expected_error):
                        page.build(ROOT)

    def test_manifest_integration_downloads_and_receipt(self):
        manifest = json.loads((ROOT / "site" / "publication-manifest.json").read_text("utf-8"))
        entries = [e for e in manifest["entries"] if e["entry_id"] == page.EXPECTED_ENTRY["entry_id"]]
        self.assertEqual(len(entries), 1)
        page.validate_entry(entries[0])
        with self.assertRaisesRegex(page.HyperboloidBuildError, "registration"):
            page.validate_entry({**entries[0], "m2_parity_admissible": True})
        build_root = ROOT / "build"
        build_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="test-hyperboloid-", dir=build_root) as temp:
            output = Path(temp) / "site"
            receipt = build_site(ROOT, output)
            target = output / "works" / page.SLUG
            self.assertTrue((target / "index.html").is_file())
            self.assertTrue((target / "measurements.json").is_file())
            self.assertTrue((target / "measurements.csv").is_file())
            self.assertIn("Гиперболоид", (target / "index.html").read_text("utf-8"))
            homepage = (output / "index.html").read_text("utf-8")
            self.assertIn(f'works/{page.SLUG}/', homepage)
            export = json.loads((target / "measurements.json").read_text("utf-8"))
            self.assertEqual(export["original_ci_artifact_json_sha256"], page.CI_JSON_SHA256)
            row = next(r for r in receipt["entries"]
                       if r["entry_id"] == page.EXPECTED_ENTRY["entry_id"])
            self.assertEqual(row["retained_git_blob_sha1"], page.ARTIFACT_GIT_BLOB_SHA1)
            self.assertEqual(row["route"], f"works/{page.SLUG}/")


if __name__ == "__main__":
    unittest.main()
