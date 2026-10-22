"""Canonical gallery route, downloads, manifest and last-valid-site checks."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scriptorium.site_renderer import PublicationBuildError, build_site
from scriptorium.site_work_comparison import EXPECTED_ENTRY, SOURCE_PATHS

REPO = Path(__file__).resolve().parents[1]


class CanonicalTwoWorkRouteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "site").mkdir()
        for rel in SOURCE_PATHS:
            dest = self.root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / rel, dest)
        self.destination = self.root / "build/site"
        self.entry = copy.deepcopy(EXPECTED_ENTRY)
        self.write_manifest()

    def write_manifest(self):
        doc = {
            "schema_version": "scriptorium-publication-manifest-v1",
            "generated_from": {"repository": "drevendev/Scriptorium", "branch": "master"},
            "deployment": {"publication_source": "github_actions", "generated_output_committed": False},
            "entries": [self.entry],
        }
        (self.root / "site/publication-manifest.json").write_text(
            json.dumps(doc, ensure_ascii=False), encoding="utf-8",
        )

    def snapshot(self):
        return {
            p.relative_to(self.destination).as_posix(): p.read_bytes()
            for p in self.destination.rglob("*") if p.is_file()
        }

    def test_real_route_homepage_and_deterministic_exports(self):
        receipt = build_site(self.root, self.destination)
        first = self.snapshot()
        build_site(self.root, self.destination)
        self.assertEqual(first, self.snapshot())
        self.assertIn("works/two-full-work-differences/", (self.destination / "index.html").read_text())
        page_path = self.destination / "works/two-full-work-differences/index.html"
        self.assertTrue(page_path.exists())
        page = page_path.read_text()
        for link in ("href='../../'", "measurements.json", "measurements.csv"):
            self.assertIn(link, page)
        data = json.loads((page_path.parent / "measurements.json").read_text())
        self.assertEqual(len(data["measurements"]), 10)
        self.assertFalse(data["scientific_boundary"]["m2_parity_admissible"])
        self.assertEqual(receipt["entries"][0]["artifact_paths"][0]["path"], SOURCE_PATHS[0])

    def test_no_implicit_discovery_or_parity_upgrade(self):
        self.entry["kind"] = "unlisted_kind"
        self.write_manifest()
        with self.assertRaises(PublicationBuildError):
            build_site(self.root, self.destination)
        self.assertFalse(self.destination.exists())
        self.entry = copy.deepcopy(EXPECTED_ENTRY)
        self.entry["compatibility_claim"] = "reproduced"
        self.write_manifest()
        with self.assertRaises(PublicationBuildError):
            build_site(self.root, self.destination)

    def test_changed_frozen_json_preserves_previous_site(self):
        build_site(self.root, self.destination)
        original = self.snapshot()
        path = self.root / SOURCE_PATHS[1]
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaises(PublicationBuildError):
            build_site(self.root, self.destination)
        self.assertEqual(original, self.snapshot())


if __name__ == "__main__":
    unittest.main()
