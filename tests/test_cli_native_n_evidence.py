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
from scriptorium.native_n_html import render_native_n_html

ROOT = Path(__file__).resolve().parents[1]


class NativeNRetainedCliTests(unittest.TestCase):
    def invoke(self, *args: str) -> str:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["n-evidence", "--root", str(ROOT), *args]), 0)
        return output.getvalue()

    def test_exact_native_witness_never_claims_m2_or_recovers_n(self):
        data = json.loads(self.invoke("--format", "json"))
        self.assertEqual(data["schema_version"], "scriptorium-native-n-cli-evidence-v4")
        self.assertEqual(data["m2_source_matched_progress"], "0/5")
        self.assertEqual(data["measurement"], "retained_native_pylem_0.0.18_not_rerun")
        self.assertEqual(data["witness"]["evidence"]["pylem_version"], "0.0.18")
        self.assertAlmostEqual(data["rates"]["n_mixed_excluded_percent_of_words"],
                               19670 * 100 / 269358)
        self.assertAlmostEqual(data["rates"]["n_candidate_percent_of_words"],
                               74751 * 100 / 269358)
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
        units = data["conditional_units"]
        self.assertEqual(units["status"], "conditional_n_only_not_observed_pos_or_fantlab_parity")
        self.assertEqual(units["denominators"], {
            "word_tokens": 269358, "all_sentences": 21228,
            "conditionally_defined_tokens": 172635,
        })
        self.assertEqual(units["schema_version"], "scriptorium-native-n-conditional-units-v2")
        self.assertEqual(units["native_control_n_only_percent_of_annotated_examples"], {
            "noun_examples": 100.0,
            "cardinal_examples": 200 / 3,
            "other_pos_controls": 0.0,
        })
        self.assertAlmostEqual(units["bucket_percent_of_conditional_defined"]["noun"][1],
                               55081 * 100 / 172635)
        self.assertAlmostEqual(units["bigram_per_1000_word_tokens"][1]["max"],
                               8402 * 1000 / 269358)
        self.assertAlmostEqual(units["sentence_position_percent_of_all_sentences"][0]["max"],
                               2787 * 100 / 21228)
        self.assertNotIn("normalized_text", data)

    def test_markdown_and_csv_preserve_conditional_not_observed(self):
        markdown = self.invoke()
        self.assertIn("N-mixed tokens stay excluded", markdown)
        self.assertIn("Excluded N-mixed: **19670 (7.30% of words)**", markdown)
        self.assertIn("Any N candidate: **74751 (27.75% of words)**", markdown)
        self.assertIn("mixed rows remain unassigned", markdown)
        self.assertIn("8402", markdown)
        self.assertIn("40825478901", markdown)
        self.assertIn("M2: 0/5", markdown)
        self.assertIn("Min / 1,000 words", markdown)
        self.assertIn("Independent-edge upper / 1,000 words", markdown)
        self.assertIn("the independent-edge upper is a looser bound", markdown)
        self.assertIn(
            f"| noun → cardinal | 0 | 8402 | 9992 | 0.000000 | "
            f"{8402 * 1000 / 269358:.6f} | {9992 * 1000 / 269358:.6f} |",
            markdown,
        )
        self.assertIn("NOT FantLab rounding", markdown)
        self.assertIn("not classifier accuracy or corpus rates", markdown)
        self.assertIn("| cardinal_examples | 2 | 3 | 66.666667% |", markdown)
        rows = list(csv.DictReader(io.StringIO(self.invoke("--format", "csv"))))
        self.assertEqual(len(rows), 27)
        derived_rates = {row["measure"]: row for row in rows if row["category"] == "rate"}
        self.assertEqual(derived_rates["n_mixed_excluded_percent_of_words"]["observed"],
                         f"{19670 * 100 / 269358:.6f}")
        self.assertEqual(derived_rates["n_candidate_percent_of_words"]["observed"],
                         f"{74751 * 100 / 269358:.6f}")
        self.assertTrue(all(derived_rates[k]["evidence_status"] == "DERIVED_NATIVE"
                            for k in ("n_mixed_excluded_percent_of_words",
                                      "n_candidate_percent_of_words")))
        cardinal_rate = next(row for row in rows if row["category"] == "native_control_rate"
                             and row["measure"] == "cardinal_examples_n_only_percent")
        self.assertEqual(cardinal_rate["observed"], "66.666667")
        self.assertEqual(cardinal_rate["unit"], "percent_of_annotated_examples")
        self.assertEqual(cardinal_rate["evidence_status"], "DERIVED_NATIVE")
        self.assertEqual(cardinal_rate["conditional_max"], "")
        pair = next(row for row in rows if row["category"] == "bigram"
                    and row["measure"] == "noun->cardinal")
        self.assertEqual((pair["observed"], pair["conditional_min"],
                          pair["conditional_max"], pair["evidence_status"]),
                         ("", "0", "8402", "CONDITIONAL_N_ONLY"))
        self.assertEqual(pair["independent_edge_upper_raw"], "9992")
        self.assertEqual(pair["conditional_max_normalized"], f"{8402 * 1000 / 269358:.6f}")
        self.assertEqual(pair["independent_edge_upper_normalized"], f"{9992 * 1000 / 269358:.6f}")
        self.assertEqual(pair["normalized_unit"], "per_1000_word_tokens")
        first_position = next(row for row in rows
                              if row["category"] == "sentence_position" and row["measure"] == "1")
        self.assertEqual(first_position["conditional_max_normalized"],
                         f"{2787 * 100 / 21228:.6f}")
        self.assertEqual(first_position["normalized_unit"], "percent_of_all_sentences")
        self.assertNotIn("PASS", {row["evidence_status"] for row in rows})
        self.assertEqual({row["candidate_id"] for row in rows}, {"tolstoy-anna-karenina-ru"})
        self.assertEqual({row["pylem_version"] for row in rows}, {"0.0.18"})
        self.assertEqual({row["runtime_analysis_sha256"] for row in rows},
                         {"00cb365eeb6e187362cb1cb54acc6718c230791df18013702907dfee6446d69d"})
        conditional_defined = next(row for row in rows if row["measure"] == "conditional_defined")
        self.assertEqual((conditional_defined["observed"], conditional_defined["evidence_status"]),
                         ("172635", "DERIVED_CONDITIONAL"))
        self.assertTrue(all(row["observed"] == "" for row in rows
                            if row["evidence_status"] == "CONDITIONAL_N_ONLY"))

    def test_html_is_accessible_source_free_and_safe_to_print(self):
        page = self.invoke("--format", "html")
        self.assertTrue(page.startswith("<!doctype html>"))
        self.assertIn('lang="ru"', page)
        self.assertIn('<caption>Условные интервалы POS-биграмм</caption>', page)
        self.assertIn('role="region" tabindex="0"', page)
        self.assertIn("55", page)
        self.assertIn("19670", page)
        self.assertIn("8402", page)
        self.assertIn("9992", page)
        self.assertIn("только диагностика".lower(), page.lower())
        self.assertIn("0/5", page)
        self.assertIn("на 1000 слов-токенов", page)
        self.assertIn("@media print", page)
        self.assertNotIn("<script", page.lower())
        self.assertNotIn('<link rel="stylesheet"', page.lower())
        self.assertNotIn("normalized_text", page)
        report = json.loads(self.invoke("--format", "json"))
        report["witness"]["work"]["title"] = '<img src=x onerror="alert(1)">'
        escaped = render_native_n_html(report)
        self.assertNotIn("<img", escaped)
        self.assertIn("&lt;img", escaped)

    def test_html_create_only_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "native-n.html"
            self.assertEqual(main(["n-evidence", "--root", str(ROOT),
                                   "--format", "html", "--output", str(path)]), 0)
            first = path.read_bytes()
            self.assertTrue(first.startswith(b"<!doctype html>"))
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main(["n-evidence", "--root", str(ROOT),
                      "--format", "html", "--output", str(path)])
            self.assertEqual(path.read_bytes(), first)

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
                (("bigram_bounds", 1, "max"), 8300),  # schema-valid but not the frozen native witness
                (("bigram_bounds", 1, "independent_edge_upper"), 9991),
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
