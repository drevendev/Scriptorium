"""Pinned, source-free native N collision comparison across two full works."""
import copy
import json
from pathlib import Path
import unittest

from scriptorium.native_n_crosswork import compare_pinned_native_n

ROOT = Path(__file__).resolve().parents[1]


def fixtures():
    anna = json.loads((ROOT / "assets/n-uncertainty-anna.json").read_text(encoding="utf-8"))
    resurrection = json.loads((ROOT / "assets/n-uncertainty-resurrection-summary.json").read_text(encoding="utf-8"))
    return anna, resurrection


class NativeNCrossworkTests(unittest.TestCase):
    def test_exact_source_free_difference(self):
        anna, resurrection = fixtures()
        delta = compare_pinned_native_n(anna, resurrection)
        self.assertEqual(delta["unit"], "percentage_points_of_word_tokens")
        self.assertAlmostEqual(delta["anna_n_only_percent"], 55081 / 269358 * 100)
        self.assertAlmostEqual(delta["resurrection_n_only_percent"], 31708 / 136129 * 100)
        self.assertAlmostEqual(delta["resurrection_minus_anna_pp"], 2.8436186218769173)
        self.assertEqual(resurrection["counts"]["n_mixed_excluded"], 9555)
        self.assertFalse(delta["m2_parity_admissible"])
        self.assertFalse(resurrection["source_text_included"])
        self.assertNotIn("normalized_text", json.dumps(resurrection))

    def test_forged_native_receipts_fail_closed(self):
        anna, resurrection = fixtures()
        cases = (
            ("counts", "n_only", 31709),
            ("counts", "n_only", 31708.0),
            ("counts", "word_count", True),
            ("evidence", "artifact_id", 14429917083.0),
            ("evidence", "run_id", 44309635723.0),
            ("evidence", "artifact_json_sha256", "0" * 64),
            ("evidence", "normalized_sha256", "0" * 64),
            ("evidence", "head_sha", "0" * 40),
            ("provider", "version", "0.0.19"),
            (None, "source_text_included", True),
            (None, "m2_parity_admissible", True),
        )
        for group, key, invalid in cases:
            with self.subTest(group=group, key=key):
                fake = copy.deepcopy(resurrection)
                (fake[group] if group else fake)[key] = invalid
                with self.assertRaises(ValueError):
                    compare_pinned_native_n(anna, fake)
        forged = copy.deepcopy(anna)
        forged["counts"]["n_only"] += 1
        with self.assertRaises(ValueError):
            compare_pinned_native_n(forged, resurrection)
        forged = copy.deepcopy(resurrection)
        forged["source_text"] = "private manuscript"
        with self.assertRaises(ValueError):
            compare_pinned_native_n(anna, forged)

    def test_reader_rows_remain_bound_to_native_counts(self):
        anna, resurrection = fixtures()
        summary = compare_pinned_native_n(anna, resurrection)
        page = (ROOT / "n-uncertainty.html").read_text(encoding="utf-8")
        self.assertIn('id="n-two-work-table"', page)
        self.assertIn('href="./assets/n-uncertainty-resurrection-summary.json"', page)
        self.assertIn("actions/runs/44309635723", page)
        for key, label, count, denom, mixed in (
            ("anna", "Анна Каренина", 55081, 269358, 19670),
            ("resurrection", "Воскресение", 31708, 136129, 9555),
        ):
            ratio = summary["anna_n_only_percent" if key == "anna" else "resurrection_n_only_percent"]
            row = (f'<tr data-n-crosswork="{key}"><th scope="row">{label}</th>'
                   f'<td>{count:,}</td><td>{denom:,}</td>'
                   f'<td>{ratio:.2f}%</td><td>{mixed:,}</td></tr>')
            self.assertIn(row.replace(",", " ").replace(".", ","), page)
        self.assertIn("2,84 процентного пункта", page)
        self.assertIn("не является проверкой выбора омонимов", page)
        self.assertIn("M2: 0/5", page)
        self.assertNotIn("normalized_text", page)
        changed = page.replace("2,84 процентного пункта", "2,85 процентного пункта", 1)
        self.assertNotIn("2,84 процентного пункта", changed)


if __name__ == "__main__":
    unittest.main()
