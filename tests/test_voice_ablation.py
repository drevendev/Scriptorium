"""Pinned four-work feature-removal sensitivity, not M3 validation."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from scriptorium import cli, voice_ablation, voice_holdout, voice_profile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/evidence-snapshot.json"


class FeatureAblationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = SOURCE.read_bytes()
        cls.preview = voice_profile.build_preview(
            json.loads(raw), source_blob_sha1=voice_profile._git_blob_sha(raw)
        )

    def test_all_eight_feature_removals_preserve_no_leakage_and_pins(self):
        result = voice_ablation.build_ablation(self.preview)
        self.assertEqual(result["schema_version"], voice_ablation.VERSION)
        self.assertEqual(result["source_snapshot_git_blob_sha1"],
                         self.preview["source_snapshot_git_blob_sha1"])
        baseline = voice_holdout.build_holdout(self.preview)
        self.assertEqual(result["baseline_summary"], baseline["summary"])
        self.assertEqual(result["baseline_summary"]["nearer_to_labelled_author"], 1)
        self.assertEqual(len(result["ablations"]), 8)
        self.assertEqual(
            [x["summary"]["nearer_to_labelled_author"] for x in result["ablations"]],
            [1, 1, 1, 1, 1, 1, 2, 1],
        )
        self.assertEqual(
            [x["summary"]["changed_nearest"] for x in result["ablations"]],
            [0, 0, 0, 0, 0, 0, 1, 0],
        )
        for ablation in result["ablations"]:
            self.assertEqual(len(ablation["retained_features"]), 7)
            self.assertNotIn(ablation["omitted_feature_id"], ablation["retained_features"])
            self.assertEqual(len(ablation["folds"]), 4)
            summary = ablation["summary"]
            self.assertEqual(sum(summary[key] for key in (
                "nearer_to_labelled_author", "nearer_to_other_author", "ties"
            )), 4)
            for fold, reference in zip(ablation["folds"], baseline["folds"]):
                self.assertEqual(fold["held_out_work_key"], reference["held_out_work_key"])
                for author_id in ("grin", "tolstoy"):
                    self.assertGreaterEqual(fold["relative_distances"][author_id], 0)
                    self.assertLessEqual(fold["relative_distances"][author_id], 2)
        removed_questions = result["ablations"][6]
        self.assertEqual(removed_questions["omitted_feature_id"],
                         "fantlab.punctuation.question.per_1000_words")
        self.assertEqual(removed_questions["folds"][1]["held_out_work_key"], "road")
        self.assertEqual(removed_questions["folds"][1]["nearest_author_id"], "grin")
        self.assertTrue(removed_questions["folds"][1]["nearest_changed_from_eight_features"])
        self.assertFalse(result["scientific_boundary"]["m3_accepted"])

    def test_deterministic_human_report_and_json(self):
        a = voice_ablation.build_ablation(self.preview)
        b = voice_ablation.build_ablation(self.preview)
        self.assertEqual(voice_profile.render_json(a), voice_profile.render_json(b))
        report = voice_ablation.render_markdown(a)
        self.assertIn("1 из 4", report)
        self.assertIn("2 из 4", report)
        self.assertIn("подгонку", report)
        self.assertIn("M2: 0/5; M3: открыт", report)
        self.assertEqual(report.count("| Запятые |"), 1)
        self.assertEqual(report.count("| Тире |"), 1)

    def test_rejects_forged_pins_and_scientific_boundaries(self):
        for mutate in (
            lambda p: p["scientific_boundary"].__setitem__("m3_accepted", True),
            lambda p: p["scientific_boundary"].__setitem__("m2_source_matched", 1),
            lambda p: p["authors"][0]["works"][0].__setitem__("source_sha256", "0" * 64),
            lambda p: p["authors"][1]["metrics"][0]["per_work"][0].__setitem__("value", -1),
            lambda p: p["authors"][0]["metrics"][0].__setitem__("id", "forged"),
        ):
            damaged = deepcopy(self.preview)
            mutate(damaged)
            with self.assertRaises(ValueError):
                voice_ablation.build_ablation(damaged)
        damaged_result = voice_ablation.build_ablation(self.preview)
        damaged_result["scientific_boundary"]["m3_accepted"] = True
        with self.assertRaises(ValueError):
            voice_ablation.render_markdown(damaged_result)

    def test_cli_json_markdown_and_invalid_flag_combinations(self):
        expected = voice_ablation.build_ablation(self.preview)
        stdout = StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(cli.main(["voice", "--ablate"]), 0)
        self.assertEqual(json.loads(stdout.getvalue()), expected)
        with redirect_stdout(stdout := StringIO()):
            self.assertEqual(cli.main(["voice", "--ablate", "--format", "markdown"]), 0)
        self.assertEqual(stdout.getvalue(), voice_ablation.render_markdown(expected))
        for options in (
            ["--ablate", "--holdout"],
            ["--ablate", "--check", str(ROOT / "assets/voice-preview.json")],
        ):
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as rejected:
                cli.main(["voice", *options])
            self.assertEqual(rejected.exception.code, 2)

    def test_bundled_resource_integrity_is_still_mandatory(self):
        output, errors = StringIO(), StringIO()
        with patch.object(voice_profile, "_PACKAGED_SOURCE_BLOB_SHA1", "0" * 40):
            with redirect_stdout(output), redirect_stderr(errors):
                with self.assertRaises(SystemExit) as rejected:
                    cli.main(["voice", "--ablate"])
        self.assertEqual(rejected.exception.code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("unable to verify", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
