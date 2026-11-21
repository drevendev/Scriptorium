"""Offline two-work native N CLI: source-bound positive and negative regressions."""
from __future__ import annotations

import contextlib
import csv
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium import cli
from scriptorium.native_n_crosswork_cli import (
    RESURRECTION_PATH, SCHEMA, build_crosswork_report, main,
    render_crosswork_report,
)

ROOT = Path(__file__).resolve().parents[1]
ANNA_PATH = Path("assets/n-uncertainty-anna.json")


class NativeNCrossworkOfflineTests(unittest.TestCase):
    def test_exact_observed_three_way_comparison(self):
        report = build_crosswork_report(ROOT)
        self.assertEqual(report["schema_version"], SCHEMA)
        self.assertEqual(report["status"], "diagnostic_only")
        self.assertFalse(report["source_text_included"])
        self.assertFalse(report["m2_parity_admissible"])
        self.assertEqual([x["measure_id"] for x in report["rows"]],
                         ["n_only", "n_mixed", "any_n"])
        self.assertEqual([x["word_tokens"] for x in report["works"]],
                         [269358, 136129])
        self.assertEqual([x["anna_count"] for x in report["rows"]],
                         [55081, 19670, 74751])
        self.assertEqual([x["resurrection_count"] for x in report["rows"]],
                         [31708, 9555, 41263])
        for row in report["rows"]:
            self.assertAlmostEqual(
                row["anna_percent_of_word_tokens"],
                row["anna_count"] / 269358 * 100,
            )
            self.assertAlmostEqual(
                row["resurrection_percent_of_word_tokens"],
                row["resurrection_count"] / 136129 * 100,
            )
            self.assertAlmostEqual(
                row["resurrection_minus_anna_percentage_points"],
                (row["resurrection_count"] / 136129
                 - row["anna_count"] / 269358) * 100,
            )
        self.assertEqual(report, build_crosswork_report(ROOT))
        self.assertEqual(report["works"][0]["normalized_sha256"],
                         "1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205")
        self.assertEqual(report["works"][1]["normalized_sha256"],
                         "2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0")

    def test_all_three_output_formats_are_source_free_and_labeled(self):
        report = build_crosswork_report(ROOT)
        json_text = render_crosswork_report(report, "json")
        self.assertEqual(json.loads(json_text), report)
        self.assertIn('"source_text_included": false', json_text)
        self.assertNotIn("normalized_text", json_text)
        markdown = render_crosswork_report(report, "markdown")
        self.assertIn("Анна Каренина", markdown)
        self.assertIn("Воскресение", markdown)
        self.assertIn("M2: 0/5", markdown)
        self.assertIn("не точность распознавания", markdown)
        self.assertIn("+2.84", markdown)
        self.assertIn("+2.56", markdown)
        self.assertIn("actions/runs/44309635723", markdown)
        csv_text = render_crosswork_report(report, "csv")
        rows = list(csv.DictReader(StringIO(csv_text)))
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2]["measure_id"], "any_n")
        self.assertEqual(rows[2]["anna_count"], "74751")
        self.assertEqual(rows[2]["resurrection_count"], "41263")
        self.assertEqual(rows[1]["status"], "diagnostic_only")
        for text in (json_text, markdown, csv_text):
            self.assertNotIn("private manuscript", text)
            self.assertNotIn("normalized_text", text)
        with self.assertRaises(ValueError):
            render_crosswork_report(report, "html")

    def test_witness_byte_drift_and_source_injection_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "assets").mkdir()
            for path in (ANNA_PATH, RESURRECTION_PATH):
                (root / path).write_bytes((ROOT / path).read_bytes())
            self.assertEqual(build_crosswork_report(root),
                             build_crosswork_report(ROOT))
            resurrection_path = root / RESURRECTION_PATH
            original = resurrection_path.read_bytes()
            for changed in (
                original.replace(b'31708', b'31709', 1),
                original + b'\n',
                original.replace(b'"source_text_included": false',
                                 b'"source_text_included": false, "source_text": "private manuscript"', 1),
                original.replace(b'"word_count": 136129',
                                 b'"word_count": 136129, "word_count": 136129', 1),
            ):
                self.assertNotEqual(changed, original)
                resurrection_path.write_bytes(changed)
                with self.assertRaises(ValueError):
                    build_crosswork_report(root)
            resurrection_path.write_bytes(original)
            anna_path = root / ANNA_PATH
            anna_path.write_bytes(anna_path.read_bytes() + b'\n')
            with self.assertRaises(ValueError):
                build_crosswork_report(root)
            anna_path.unlink()
            with self.assertRaises((ValueError, OSError)):
                build_crosswork_report(root)

    def test_command_dispatch_and_create_only_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "native-pair.csv"
            buffer = StringIO()
            with contextlib.redirect_stdout(buffer):
                self.assertEqual(cli.main(["n-compare", "--root", str(ROOT),
                                           "--format", "csv", "--output", str(target)]), 0)
            self.assertEqual(buffer.getvalue(), "")
            original = target.read_text(encoding="utf-8")
            self.assertEqual(len(list(csv.DictReader(StringIO(original)))), 3)
            with contextlib.redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    main(["--root", str(ROOT), "--format", "json",
                          "--output", str(target)])
            self.assertEqual(raised.exception.code, 2)
            self.assertEqual(target.read_text(encoding="utf-8"), original)
            printed = StringIO()
            with contextlib.redirect_stdout(printed):
                self.assertEqual(main(["--root", str(ROOT), "--format", "json"]), 0)
            self.assertEqual(json.loads(printed.getvalue()), build_crosswork_report(ROOT))

    def test_missing_or_symlinked_input_is_rejected_without_prose(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "assets").mkdir()
            (root / ANNA_PATH).write_bytes((ROOT / ANNA_PATH).read_bytes())
            with self.assertRaises((ValueError, OSError)):
                build_crosswork_report(root)
            (root / RESURRECTION_PATH).symlink_to(ROOT / RESURRECTION_PATH)
            with self.assertRaises((ValueError, OSError)):
                build_crosswork_report(root)
            with contextlib.redirect_stderr(StringIO()) as errors:
                with self.assertRaises(SystemExit) as raised:
                    main(["--root", str(root)])
            self.assertEqual(raised.exception.code, 2)
            self.assertIn("pinned native N receipts invalid", errors.getvalue())
            self.assertNotIn("private manuscript", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
