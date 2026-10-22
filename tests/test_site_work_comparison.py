"""Positive/negative tests on real pinned, source-free derived evidence."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

from scriptorium import site_work_comparison as subject

REPO = Path(__file__).resolve().parents[1]


class FrozenComparisonPublicationTests(unittest.TestCase):
    def test_real_pinned_build_and_exact_metric_units(self):
        rendered = subject.build(REPO)
        data = json.loads(rendered["json"])
        self.assertEqual(len(data["measurements"]), 10)
        self.assertEqual(data["scientific_boundary"]["m2_weight"], 0)
        self.assertFalse(data["scientific_boundary"]["m2_parity_admissible"])
        self.assertEqual(data["works"][0]["characters_including_spaces"], 363819)
        self.assertEqual(data["works"][1]["characters_including_spaces"], 1095467)
        self.assertEqual(data["works"][1]["author_or_translator"],
                         "Jules Verne · Alexandra Beketova translation")
        metrics = {row["metric_id"]: row for row in data["measurements"]}
        self.assertEqual(metrics["fantlab.dialogue.share_percent"]["difference_unit"], "percentage points")
        self.assertEqual(metrics["fantlab.general.words"]["difference_unit"], "words")
        self.assertIn("right_minus_left", rendered["json"])

    def test_links_accessibility_and_no_scripts(self):
        page = subject.build(REPO)["html"]
        for piece in ("href='../../'", "href='measurements.json'",
                      "href='measurements.csv'", "href='#main'", "<table>",
                      "No manuscript text"):
            self.assertIn(piece, page)
        self.assertNotIn("<script", page)

    def test_replay_and_input_digests(self):
        first = subject.build(REPO)
        self.assertEqual(first, subject.build(REPO))
        self.assertEqual(len(first["input_artifacts"]), 2)
        for row in first["input_artifacts"]:
            self.assertEqual(hashlib.sha256((REPO / row["path"]).read_bytes()).hexdigest(), row["sha256"])
        self.assertIn("fantlab.general.words", first["csv"])

    def test_strict_manifest_registration(self):
        subject.validate_entry(copy.deepcopy(subject.EXPECTED_ENTRY))
        for key, value in (("kind", "work_showcase"), ("compatibility_claim", "reproduced"),
                           ("corpus_admissibility", "admissible"), ("source_text_included", True),
                           ("artifact_paths", ["corpus/candidates/diagnostics/other.json"])):
            with self.subTest(key=key):
                modified = copy.deepcopy(subject.EXPECTED_ENTRY)
                modified[key] = value
                with self.assertRaises(subject.ComparisonBuildError):
                    subject.validate_entry(modified)
        with self.assertRaises(subject.ComparisonBuildError):
            subject.validate_entry({**subject.EXPECTED_ENTRY, "surprise": "new"})

    def test_tampering_rejected_without_private_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for rel in subject.SOURCE_PATHS:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPO / rel, path)
            self.assertTrue(subject.build(root)["json"])
            tampered = root / subject.SOURCE_PATHS[0]
            tampered.write_bytes(tampered.read_bytes() + b" ")
            with self.assertRaises(subject.ComparisonBuildError) as raised:
                subject.build(root)
            self.assertNotIn(directory, str(raised.exception))

    @unittest.skipUnless(hasattr(os, "mkfifo"), "requires FIFO support")
    def test_nonblocking_source_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for rel in subject.SOURCE_PATHS:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPO / rel, path)
            fifo = root / subject.SOURCE_PATHS[0]
            fifo.unlink()
            os.mkfifo(fifo)
            with self.assertRaises(subject.ComparisonBuildError):
                subject.build(root)


if __name__ == "__main__":
    unittest.main()
