"""Retained native pylem N ambiguity is inspectable, create-only and not parity."""
from __future__ import annotations

import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.cli import main

ROOT = Path(__file__).resolve().parents[1]


class NativeNRetainedCliTests(unittest.TestCase):
    def invoke(self, *args: str) -> str:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["n-evidence", "--root", str(ROOT), *args]), 0)
        return output.getvalue()

    def test_exact_native_witness_never_claims_m2_or_recovers_n(self):
        data = json.loads(self.invoke("--format", "json"))
        self.assertEqual(data["schema_version"], "scriptorium-native-n-cli-evidence-v1")
        self.assertEqual(data["m2_source_matched_progress"], "0/5")
        self.assertEqual(data["measurement"], "retained_native_pylem_0.0.18_not_rerun")
        self.assertEqual(data["witness"]["evidence"]["pylem_version"], "0.0.18")
        self.assertEqual(data["witness"]["counts"], {
            "word_count": 269358, "sentence_count": 21228,
            "baseline_defined": 117554, "n_only": 55081,
            "n_mixed_excluded": 19670, "conditional_defined": 172635,
        })
        self.assertEqual([pair["max"] for pair in data["witness"]["bigram_bounds"]],
                         [9992, 8402, 8402, 9992])
        self.assertEqual(data["witness"]["bucket_bounds"],
                         {"noun": [0, 55081], "cardinal": [0, 55081]})
        self.assertFalse(data["witness"]["m2_parity_admissible"])
        self.assertFalse(data["witness"]["source_text_included"])
        self.assertFalse(data["witness"]["boundary"]["production_pos_mapping_changed"])
        self.assertNotIn("normalized_text", data)

    def test_markdown_and_csv_preserve_conditional_not_observed(self):
        markdown = self.invoke()
        self.assertIn("N-mixed tokens stay excluded", markdown)
        self.assertIn("8402", markdown)
        self.assertIn("40825478901", markdown)
        self.assertIn("M2: 0/5", markdown)
        rows = list(csv.DictReader(io.StringIO(self.invoke("--format", "csv"))))
        self.assertEqual(len(rows), 22)
        pair = next(row for row in rows if row["category"] == "bigram"
                    and row["measure"] == "noun->cardinal")
        self.assertEqual((pair["observed"], pair["conditional_min"],
                          pair["conditional_max"], pair["evidence_status"]),
                         ("", "0", "8402", "CONDITIONAL_N_ONLY"))
        self.assertNotIn("PASS", {row["evidence_status"] for row in rows})
        self.assertTrue(all(row["observed"] == "" for row in rows
                            if row["evidence_status"] == "CONDITIONAL_N_ONLY"))

    def test_create_only_and_private_path_redaction(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "PRIVATE-n.csv"
            self.assertEqual(main(["n-evidence", "--root", str(ROOT),
                                   "--format", "csv", "--output", str(target)]), 0)
            original = target.read_bytes()
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as caught:
                main(["n-evidence", "--root", str(ROOT), "--output", str(target)])
            self.assertEqual(caught.exception.code, 2)
            self.assertEqual(target.read_bytes(), original)
            self.assertIn("already exists", stderr.getvalue())
            self.assertNotIn(folder, stderr.getvalue())

    def test_invalid_evidence_is_rejected_without_leaking_paths(self):
        original = ROOT / "assets/n-uncertainty-anna.json"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "assets").mkdir()
            target = root / "assets/n-uncertainty-anna.json"
            doc = json.loads(original.read_text(encoding="utf-8"))
            for path, value in [
                (("m2_parity_admissible",), True),
                (("counts", "n_only"), True),
                (("boundary", "fantlab_homonym_selection"), "reproduced"),
                (("bucket_bounds", "noun"), [0, 1]),
            ]:
                with self.subTest(path=path):
                    forged = json.loads(json.dumps(doc))
                    cursor = forged
                    for key in path[:-1]:
                        cursor = cursor[key]
                    cursor[path[-1]] = value
                    target.write_text(json.dumps(forged), encoding="utf-8")
                    stderr = io.StringIO()
                    with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as caught:
                        main(["n-evidence", "--root", str(root), "--format", "json"])
                    self.assertEqual(caught.exception.code, 2)
                    self.assertIn("evidence invalid", stderr.getvalue())
                    self.assertNotIn(folder, stderr.getvalue())
            target.write_text('{"schema_version":"x","schema_version":"y"}', encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main(["n-evidence", "--root", str(root)])

    def test_help_and_missing_root(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--help"]), 0)
        self.assertIn("n-evidence", output.getvalue())
        with tempfile.TemporaryDirectory() as folder:
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
                main(["n-evidence", "--root", str(Path(folder) / "missing")])
            self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
