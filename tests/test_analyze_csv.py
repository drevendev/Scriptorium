"""CSV export regressions exercised against the exact PR #270 metric core."""
from __future__ import annotations

import contextlib
import copy
import csv
from hashlib import sha256
import io
from pathlib import Path
import tempfile
import unittest

from scriptorium.analyze import build_local_analysis, main, render_csv


TEXT = "Кот, кот!\n— Здравствуйте? — спросил он.\nДругая строка."


def table(artifact):
    return list(csv.DictReader(io.StringIO(render_csv(artifact))))


class AnalysisCsvTests(unittest.TestCase):
    def test_all_29_real_engine_metrics_are_present_with_stable_ids(self):
        artifact = build_local_analysis(TEXT.encode("utf-8"))
        rows = table(artifact)
        self.assertEqual(len(rows), 29)
        self.assertEqual([r["metric_id"] for r in rows], sorted(artifact["metrics"]))
        self.assertEqual(len(rows[0]), 18)
        self.assertEqual({r["status"] for r in rows}, {"inferred", "extension"})

    def test_values_and_raw_counts_exactly_match_the_real_engine(self):
        artifact = build_local_analysis(TEXT.encode("utf-8"))
        for row in table(artifact):
            metric = artifact["metrics"][row["metric_id"]]
            expected = "" if metric["value"] is None else str(metric["value"])
            self.assertEqual(row["value"], expected)
            self.assertEqual(row["raw_count"], "" if metric.get("raw_count") is None else str(metric["raw_count"]))

    def test_unavailable_remains_blank_not_zero(self):
        artifact = build_local_analysis(b"")
        rows = table(artifact)
        unavailable = [r for r in rows if artifact["metrics"][r["metric_id"]]["value"] is None]
        self.assertTrue(unavailable)
        self.assertTrue(all(r["value"] == "" for r in unavailable))

    def test_reproducible_source_and_profile_identity_on_every_row(self):
        data = TEXT.encode("utf-8")
        artifact = build_local_analysis(data)
        rows = table(artifact)
        for row in rows:
            self.assertEqual(row["raw_sha256"], sha256(data).hexdigest())
            self.assertEqual(row["normalized_sha256"], artifact["source"]["normalized_sha256"])
            self.assertEqual(row["metric_contract_id"], artifact["metric_contract_id"])
            self.assertEqual(row["csv_schema_version"], "scriptorium-local-analysis-csv-v1")
            for key in ("normalization", "metrics", "dialogue", "vocabulary", "punctuation"):
                self.assertEqual(row[f"{key}_profile"], artifact["analyzer"]["profiles"][key])
            self.assertEqual(row["dictionary_profile"], "")
        self.assertEqual(render_csv(artifact), render_csv(build_local_analysis(data)))

    def test_no_source_text_or_dictionary_lexemes_are_exported(self):
        artifact = build_local_analysis(
            "Кот дракон-единорог".encode("utf-8"),
            dictionary_words=["дракон-единорог"], dictionary_profile="demo-v1",
        )
        result = render_csv(artifact)
        self.assertNotIn("Кот", result)
        self.assertNotIn("дракон-единорог", result)
        self.assertEqual(table(artifact)[0]["dictionary_profile"], "demo-v1")
        self.assertEqual(table(artifact)[0]["dictionary_sha256"], artifact["analyzer"]["dependencies"]["vocabulary_dictionary"]["normalized_lexemes_sha256"])

    def test_rejects_spreadsheet_formulas_from_user_controlled_profiles(self):
        for malicious in ('=HYPERLINK("https://invalid.example")', '+SUM(1,2)', '-cmd', '@SUM(1,2)', '\t=1+1'):
            with self.subTest(malicious=malicious):
                artifact = build_local_analysis(TEXT.encode("utf-8"), dictionary_words=["кот"], dictionary_profile=malicious)
                value = table(artifact)[0]["dictionary_profile"]
                self.assertTrue(value.startswith("'"), value)
                self.assertEqual(value[1:], malicious.strip())

    def test_arbitrary_precision_float_not_truncated_in_csv(self):
        artifact = build_local_analysis(TEXT.encode("utf-8"))
        artifact["metrics"]["fantlab.general.mean_word_length_chars"]["value"] = 5.142857142857143
        rows = {r["metric_id"]: r for r in table(artifact)}
        self.assertEqual(rows["fantlab.general.mean_word_length_chars"]["value"], "5.142857142857143")

    def test_inconsistent_types_and_nonfinite_values_fail_closed(self):
        original = build_local_analysis(TEXT.encode("utf-8"))
        for invalid in (True, float("inf"), float("nan"), "=1+1"):
            with self.subTest(value=str(invalid)):
                artifact = copy.deepcopy(original)
                artifact["metrics"]["fantlab.general.words"]["value"] = invalid
                with self.assertRaises(ValueError):
                    render_csv(artifact)
        artifact = copy.deepcopy(original)
        artifact["metrics"]["fantlab.general.words"]["compatibility_status"] = "reproduced"
        with self.assertRaises(ValueError):
            render_csv(artifact)
        artifact = copy.deepcopy(original)
        artifact["source"]["source_text_embedded"] = True
        with self.assertRaises(ValueError):
            render_csv(artifact)

    def test_missing_provenance_is_not_silently_exported(self):
        original = build_local_analysis(TEXT.encode("utf-8"))
        for obj_path in (("source", "raw_sha256"), ("source", "normalized_sha256"),
                         ("analyzer", "profiles", "metrics")):
            with self.subTest(path=obj_path):
                artifact = copy.deepcopy(original)
                parent = artifact
                for key in obj_path[:-1]:
                    parent = parent[key]
                parent[obj_path[-1]] = None
                with self.assertRaises(ValueError):
                    render_csv(artifact)

    def test_cli_writes_csv_create_only_and_preserves_source_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "manuscript.txt"
            output = root / "analysis.csv"
            source.write_text(TEXT, encoding="utf-8")
            self.assertEqual(main([str(source), "--format", "csv", "--output", str(output)]), 0)
            with output.open(encoding="utf-8", newline="") as stream:
                self.assertEqual(len(list(csv.DictReader(stream))), 29)
            before = output.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main([str(source), "--format", "csv", "--output", str(output)])
            self.assertEqual(output.read_bytes(), before)
            manuscript_before = source.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main([str(source), "--format", "csv", "--output", str(source)])
            self.assertEqual(source.read_bytes(), manuscript_before)
            alias = root / "source-alias.csv"
            alias.symlink_to(source)
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main([str(source), "--format", "csv", "--output", str(alias)])
            self.assertEqual(source.read_bytes(), manuscript_before)

    def test_cli_stdout_matches_serialized_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "input.txt"
            source.write_text(TEXT, encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()) as stream:
                self.assertEqual(main([str(source), "--format", "csv"]), 0)
            self.assertEqual(stream.getvalue(), render_csv(build_local_analysis(source.read_bytes())))


if __name__ == "__main__":
    unittest.main()
