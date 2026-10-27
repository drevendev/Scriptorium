"""Regression and publication gates for the pinned Beketova translation route."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import site_beketova as page
from scriptorium import full_work_gallery as gallery
from scriptorium.site_renderer import build_site

ROOT = Path(__file__).resolve().parents[1]


class BeketovaMeasuredReaderTests(unittest.TestCase):
    def test_eleven_measured_translation_fields_are_real_and_deterministic(self):
        result = page.build(ROOT)
        self.assertEqual(result, page.build(ROOT))
        body = result["body"]
        data = json.loads(result["json"])
        self.assertEqual(body.count('<tr><th scope="row"><code>'), 11)
        self.assertIn("Бекетовой", body)
        self.assertIn("M2", body)
        self.assertIn("0/5", body)
        self.assertIn("5304880", body)
        self.assertIn("measurements.csv", body)
        self.assertEqual(data["translator"], "Alexandra A. Beketova")
        self.assertEqual(data["analysis_language"], "ru")
        self.assertEqual(data["original_language"], "fr")
        self.assertIs(data["source_text_committed"], False)
        self.assertIs(data["m2_parity_admissible"], False)
        self.assertIs(data["fantlab_comparison_performed"], False)
        self.assertEqual(data["fantlab_source_edition_match"], "unknown")
        self.assertEqual(data["retained_git_blob_sha1"], page.ARTIFACT_GIT_BLOB_SHA1)
        self.assertEqual(len(data["metrics"]), 11)
        self.assertEqual(len(result["csv"].splitlines()), 12)
        self.assertTrue(all(row["fantlab_reference"] is None for row in data["metrics"]))
        vals = {row["metric_id"]: row["value"] for row in data["metrics"]}
        self.assertEqual(vals["fantlab.general.characters"], 1_095_467)
        self.assertEqual(vals["fantlab.general.words"], 158_881)
        self.assertEqual(vals["scriptorium.general.sentences"], 14_568)
        self.assertEqual(
            next(row for row in data["metrics"] if row["metric_id"] ==
                 "scriptorium.general.sentences")["compatibility_status"],
            "extension",
        )

    def test_fails_closed_on_tampered_artifact_and_false_parity_claim(self):
        source = ROOT / page.ARTIFACT_PATH
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / page.ARTIFACT_PATH
            target.parent.mkdir(parents=True)
            target.write_bytes(source.read_bytes().replace(b'"m2_weight": 0',
                                                        b'"m2_weight": 1'))
            with self.assertRaisesRegex(page.BeketovaBuildError, "invalid"):
                page.build(Path(temp))
        with self.assertRaisesRegex(page.BeketovaBuildError, "registration"):
            page.validate_entry({**page.EXPECTED_ENTRY, "compatibility_claim": "reproduced"})
        valid = gallery._load(ROOT, 1)
        for mutation in (
            lambda r: r["values"].__setitem__("scriptorium.general.sentences", 0),
            lambda r: r["values"].__setitem__("fantlab.general.words", 999),
            lambda r: r["values"].__setitem__("fantlab.general.characters", float("nan")),
            lambda r: r.__setitem__("profiles", ("unknown",) * 5),
        ):
            wrong = copy.deepcopy(valid)
            mutation(wrong)
            with self.subTest(mutation=mutation):
                with patch.object(gallery, "_load", return_value=wrong):
                    with self.assertRaisesRegex(page.BeketovaBuildError, "drifted"):
                        page.build(ROOT)

    def test_generated_reader_route_and_source_free_exports(self):
        manifest = json.loads((ROOT / "site/publication-manifest.json").read_text("utf-8"))
        matching = [e for e in manifest["entries"]
                    if e["entry_id"] == page.EXPECTED_ENTRY["entry_id"]]
        self.assertEqual(matching, [page.EXPECTED_ENTRY])
        page.validate_entry(matching[0])
        build_root = ROOT / "build"
        build_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="test-beketova-reader-", dir=build_root) as tmp:
            output = Path(tmp) / "site"
            receipt = build_site(ROOT, output)
            target = output / "works" / page.SLUG
            self.assertTrue((target / "index.html").is_file())
            self.assertTrue((target / "measurements.json").is_file())
            self.assertTrue((target / "measurements.csv").is_file())
            homepage = (output / "index.html").read_text("utf-8")
            self.assertIn(f'works/{page.SLUG}/', homepage)
            self.assertIn("Бекетовой", (target / "index.html").read_text("utf-8"))
            exported = json.loads((target / "measurements.json").read_text("utf-8"))
            self.assertEqual(exported["schema_version"], page.REPORT_PROFILE)
            entry = next(row for row in receipt["entries"]
                         if row["entry_id"] == page.EXPECTED_ENTRY["entry_id"])
            self.assertEqual(entry["retained_git_blob_sha1"], page.ARTIFACT_GIT_BLOB_SHA1)
            self.assertEqual(entry["route"], f"works/{page.SLUG}/")


if __name__ == "__main__":
    unittest.main()
