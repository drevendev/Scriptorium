"""Four-fold author rhythm stress test; never promote to accepted M3."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from scriptorium import cli, voice_profile, voice_holdout

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/evidence-snapshot.json"
PREVIEW = ROOT / "assets/voice-preview.json"


class FourBookHoldoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = SOURCE.read_bytes()
        cls.preview = voice_profile.build_preview(
            json.loads(raw), source_blob_sha1=voice_profile._git_blob_sha(raw)
        )

    def test_four_distinct_folds_without_book_leakage(self):
        data = voice_holdout.build_holdout(self.preview)
        self.assertEqual(data["schema_version"], voice_holdout.VERSION)
        self.assertEqual(data["source_snapshot_git_blob_sha1"],
                         self.preview["source_snapshot_git_blob_sha1"])
        self.assertEqual(len(data["method"]["features"]), 8)
        self.assertEqual(data["summary"], {
            "total_folds": 4, "nearer_to_labelled_author": 1,
            "nearer_to_other_author": 3, "ties": 0,
        })
        self.assertEqual([f["held_out_work_key"] for f in data["folds"]],
                         ["waves", "road", "anna", "resurrection"])
        for fold in data["folds"]:
            self.assertEqual(sum(map(len, fold["training_work_keys"].values())), 3)
            self.assertEqual(sorted(map(len, fold["training_work_keys"].values())), [1, 2])
            for work_keys in fold["training_work_keys"].values():
                self.assertNotIn(fold["held_out_work_key"], work_keys)
            for d in fold["relative_distances"].values():
                self.assertGreaterEqual(d, 0)
                self.assertLessEqual(d, 2)
        # Explicit scientific negatives: a held-out book is often nearer another author.
        self.assertEqual(data["folds"][0]["nearest_author_id"], "tolstoy")
        self.assertEqual(data["folds"][1]["nearest_author_id"], "tolstoy")
        self.assertEqual(data["folds"][2]["nearest_author_id"], "grin")
        self.assertEqual(data["folds"][3]["nearest_author_id"], "tolstoy")
        self.assertAlmostEqual(data["folds"][0]["relative_distances"]["tolstoy"], .115350, places=6)
        self.assertFalse(data["scientific_boundary"]["m3_accepted"])
        self.assertFalse(data["scientific_boundary"]["independent_external_validation"])

    def test_same_pinned_inputs_same_json_and_human_report(self):
        a = voice_holdout.build_holdout(self.preview)
        b = voice_holdout.build_holdout(self.preview)
        self.assertEqual(voice_profile.render_json(a), voice_profile.render_json(b))
        report = voice_holdout.render_markdown(a)
        self.assertIn("1 из 4", report)
        self.assertIn("М3 остаётся открыт", report)
        self.assertIn("не является вероятностью", report)
        self.assertEqual(report.count("| Бегущая по волнам"), 1)

    def test_negative_incomplete_or_forged_source_boundaries(self):
        for mutate in (
            lambda x: x["scientific_boundary"].__setitem__("m3_accepted", True),
            lambda x: x["scientific_boundary"].__setitem__("m2_source_matched", 1),
            lambda x: x.__setitem__("source_snapshot_git_blob_sha1", "invalid"),
            lambda x: x["authors"][0]["works"][0].__setitem__("word_weight", 0),
            lambda x: x["authors"][0]["works"][0].__setitem__("source_sha256", "0" * 64),
            lambda x: x["authors"][0]["metrics"][0]["per_work"][0].__setitem__("value", -1),
            lambda x: x["authors"][0]["metrics"][1].__setitem__("id", "wrong"),
        ):
            broken = deepcopy(self.preview)
            mutate(broken)
            with self.assertRaises(ValueError):
                voice_holdout.build_holdout(broken)

    def test_voice_entrypoint_holdout_json_and_markdown(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(cli.main(["voice", "--holdout"]), 0)
        self.assertEqual(json.loads(output.getvalue()),
                         voice_holdout.build_holdout(self.preview))
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(cli.main(["voice", "--holdout", "--format", "markdown"]), 0)
        self.assertEqual(output.getvalue(), voice_holdout.render_markdown(
            voice_holdout.build_holdout(self.preview)
        ))
        self.assertEqual(
            json.loads(PREVIEW.read_text(encoding="utf-8")),
            self.preview,
            "original preview must remain byte-contract-compatible"
        )

    def test_fail_closed_on_bundled_tamper_and_reject_check_mix(self):
        stderr, stdout = StringIO(), StringIO()
        with patch.object(voice_profile, "_PACKAGED_SOURCE_BLOB_SHA1", "0" * 40):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as rejected:
                    cli.main(["voice", "--holdout"])
        self.assertEqual(rejected.exception.code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("unable to verify", stderr.getvalue())
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit) as mixed:
                cli.main(["voice", "--holdout", "--check", str(PREVIEW)])
        self.assertEqual(mixed.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
