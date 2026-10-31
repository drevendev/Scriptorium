"""Private Reader comparison contract and CLI end-to-end regressions."""
from __future__ import annotations

import contextlib
import copy
import csv
from decimal import Decimal
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scriptorium import cli
from scriptorium.analyze import build_local_analysis
from scriptorium import compare


LEFT = "Кот спит. Кот и пёс гуляют!\n— Да? — сказал пёс."
RIGHT = "Кот, кот, кот!\n— А? — ответил он."


class LocalComparisonTests(unittest.TestCase):
    def setUp(self):
        self.a = build_local_analysis(LEFT.encode("utf-8"))
        self.b = build_local_analysis(RIGHT.encode("utf-8"))

    def test_complete_29_metric_contract_and_decimal_differences(self):
        value = compare.build_comparison(self.a, self.b)
        self.assertEqual(value["schema_version"], "scriptorium-private-comparison-v1")
        self.assertEqual(len(value["metrics"]), 29)
        self.assertEqual({r["metric_id"] for r in value["metrics"]}, set(self.a["metrics"]))
        rows = {r["metric_id"]: r for r in value["metrics"]}
        count = rows["fantlab.general.words"]
        self.assertEqual(count["difference"], str(self.b["metrics"]["fantlab.general.words"]["value"] - self.a["metrics"]["fantlab.general.words"]["value"]))
        self.assertEqual(count["difference_unit"], "words")
        share = rows["fantlab.dialogue.share_percent"]
        self.assertEqual(share["difference_unit"], "percentage_points")
        self.assertEqual(share["difference"], str(Decimal(repr(self.b["metrics"]["fantlab.dialogue.share_percent"]["value"])) - Decimal(repr(self.a["metrics"]["fantlab.dialogue.share_percent"]["value"]))))
        self.assertTrue(any(r["comparison_status"] == "unavailable" for r in value["metrics"]))
        self.assertEqual(value["scientific_boundary"].count("M2 0/5"), 1)

    def test_float_lexemes_produce_exact_decimal_difference(self):
        self.a["metrics"]["fantlab.general.mean_word_length_chars"]["value"] = Decimal("1.0000000000000003")
        self.b["metrics"]["fantlab.general.mean_word_length_chars"]["value"] = Decimal("1.0000000000000004")
        value = compare.build_comparison(self.a, self.b)
        row = next(r for r in value["metrics"] if r["metric_id"] == "fantlab.general.mean_word_length_chars")
        self.assertEqual(row["difference"], "1E-16")
        self.assertEqual(row["left"], "1.0000000000000003")

    def test_long_json_decimal_lexemes_do_not_round_difference(self):
        # Both are accepted by the 72-character JSON literal gate. A normal
        # Decimal subtraction at default context precision silently loses
        # the 29th+ significant digit, violating exact decimal deltas.
        cases = (
            ("2.123456789012345678901234567890", "2.111111111111111111111111111111",
             "-0.012345677901234567790123456779"),
            ("4.0000000000000000000000000000000000000001",
             "3.0000000000000000000000000000000000000002",
             "-0.9999999999999999999999999999999999999999"),
        )
        for first, second, expected in cases:
            with self.subTest(first=first, second=second):
                left = copy.deepcopy(self.a)
                right = copy.deepcopy(self.b)
                metric = "fantlab.general.mean_word_length_chars"
                left["metrics"][metric]["value"] = Decimal(first)
                right["metrics"][metric]["value"] = Decimal(second)
                row = next(r for r in compare.build_comparison(left, right)["metrics"]
                           if r["metric_id"] == metric)
                self.assertEqual(row["difference"], expected)
                self.assertEqual(row["difference_unit"], "characters/word")

    def test_imported_mean_length_and_presence_match_source_budget(self):
        # The actual engine produces mandatory means when a word/sentence
        # denominator is nonzero. Their character budget cannot exceed the
        # normalized source. Zero-length inputs keep the mean unavailable.
        accepted = self.a
        compare.validate_report(accepted)
        for metric_id in (
            "fantlab.general.mean_word_length_chars",
            "fantlab.general.mean_sentence_length_chars",
        ):
            with self.subTest(metric_id=metric_id):
                for bad_value in (None, 0, self.a["source"]["normalized_character_count"] + 1000):
                    invalid = copy.deepcopy(self.a)
                    invalid["metrics"][metric_id]["value"] = bad_value
                    with self.assertRaises(compare.CompareError):
                        compare.validate_report(invalid)
        empty = build_local_analysis(b"")
        for metric_id in (
            "fantlab.general.mean_word_length_chars",
            "fantlab.general.mean_sentence_length_chars",
        ):
            self.assertIsNone(empty["metrics"][metric_id]["value"])
            compare.validate_report(empty)
            invalid = copy.deepcopy(empty)
            invalid["metrics"][metric_id]["value"] = 0
            with self.assertRaises(compare.CompareError):
                compare.validate_report(invalid)

    def test_changed_dictionary_cannot_hide_same_text_dialogue_drift(self):
        # Both are genuine Reader artifacts from identical bytes. Their only
        # declared analysis dependency change is the optional lexicon.
        left = self.a
        right = build_local_analysis(
            LEFT.encode("utf-8"), dictionary_words=["кот"],
            dictionary_profile="test-lexicon-v1",
        )
        self.assertEqual(left["source"]["normalized_sha256"], right["source"]["normalized_sha256"])
        self.assertEqual(left["analyzer"]["profiles"], right["analyzer"]["profiles"])
        compare.validate_report(right)
        rows = {r["metric_id"]: r for r in compare.build_comparison(left, right)["metrics"]}
        self.assertEqual(rows["fantlab.vocabulary.active_dictionary"]["comparison_status"], "incomparable")
        self.assertEqual(rows["fantlab.general.words"]["difference"], "0")
        right["metrics"]["fantlab.dialogue.share_percent"]["value"] += 1
        compare.validate_report(right)
        with self.assertRaises(compare.CompareError):
            compare.build_comparison(left, right)

    def test_changed_dictionary_cannot_hide_same_text_punctuation_drift(self):
        left = self.a
        right = build_local_analysis(
            LEFT.encode("utf-8"), dictionary_words=["кот"],
            dictionary_profile="test-lexicon-v1",
        )
        row = right["metrics"]["fantlab.punctuation.dash.per_1000_words"]
        row["raw_count"] += 1
        words = right["metrics"]["fantlab.general.words"]["value"]
        row["value"] = row["raw_count"] * 1000.0 / words
        compare.validate_report(right)
        with self.assertRaises(compare.CompareError):
            compare.build_comparison(left, right)

    def test_mismatched_algorithm_prevents_all_deltas(self):
        self.b["analyzer"]["profiles"]["metrics"] = "future-metrics-v99"
        value = compare.build_comparison(self.a, self.b)
        self.assertTrue(all(r["comparison_status"] == "incomparable" and r["difference"] is None for r in value["metrics"]))

    def test_dictionary_mismatch_only_blocks_dependent_rows(self):
        left = build_local_analysis(LEFT.encode(), dictionary_words=["кот"], dictionary_profile="same-dictionary-label")
        right = build_local_analysis(RIGHT.encode(), dictionary_words=["пёс"], dictionary_profile="same-dictionary-label")
        rows = {r["metric_id"]: r for r in compare.build_comparison(left, right)["metrics"]}
        self.assertEqual(rows["fantlab.vocabulary.active_dictionary"]["comparison_status"], "incomparable")
        self.assertIsNone(rows["fantlab.vocabulary.active_dictionary"]["difference"])
        self.assertEqual(rows["fantlab.general.words"]["comparison_status"], "comparable")
        self.assertEqual(rows["fantlab.vocabulary.unique_words"]["comparison_status"], "comparable")

    def test_identical_normalized_input_must_have_deterministic_metrics(self):
        left = build_local_analysis(LEFT.encode("utf-8"))
        same = copy.deepcopy(left)
        compare.build_comparison(left, same)
        same["metrics"]["fantlab.dialogue.share_percent"]["value"] += 1.0
        compare.validate_report(same)
        with self.assertRaisesRegex(compare.CompareError, "contradictory measurements"):
            compare.build_comparison(left, same)

    def test_changed_revision_label_cannot_hide_same_method_contradiction(self):
        # Revision is provenance, not a substitute for a versioned algorithm
        # or dictionary profile.  With identical normalized source and declared
        # method a different commit label must not produce a fabricated delta.
        left = build_local_analysis(LEFT.encode("utf-8"), scriptorium_revision="first-commit")
        right = copy.deepcopy(left)
        right["analyzer"]["scriptorium_revision"] = "later-commit"
        compare.build_comparison(left, right)  # different label; same values OK
        right["metrics"]["fantlab.dialogue.share_percent"]["value"] += 1.0
        compare.validate_report(right)  # a single report cannot prove this violation
        with self.assertRaisesRegex(compare.CompareError, "contradictory measurements"):
            compare.build_comparison(left, right)

    def test_identical_normalized_input_cannot_have_different_punctuation_counts(self):
        left = build_local_analysis(LEFT.encode("utf-8"))
        same = copy.deepcopy(left)
        row = same["metrics"]["fantlab.punctuation.comma.per_1000_words"]
        row["raw_count"] += 1
        row["value"] = row["raw_count"] * 1000.0 / same["metrics"]["fantlab.general.words"]["value"]
        compare.validate_report(same)
        with self.assertRaises(compare.CompareError):
            compare.build_comparison(left, same)

    def test_equal_normalized_text_with_different_raw_newlines_is_allowed(self):
        lf = build_local_analysis(LEFT.encode("utf-8"))
        crlf = build_local_analysis(LEFT.replace("\n", "\r\n").encode("utf-8"))
        self.assertNotEqual(lf["source"]["raw_sha256"], crlf["source"]["raw_sha256"])
        self.assertEqual(lf["source"]["normalized_sha256"], crlf["source"]["normalized_sha256"])
        compare.build_comparison(lf, crlf)

    def test_equal_raw_digest_cannot_have_inconsistent_source_metadata(self):
        left = build_local_analysis(LEFT.encode("utf-8"))
        changed_bytes = copy.deepcopy(left)
        changed_bytes["source"]["byte_count"] += 1
        compare.validate_report(changed_bytes)
        with self.assertRaises(compare.CompareError):
            compare.build_comparison(left, changed_bytes)
        changed_normalized = copy.deepcopy(left)
        changed_normalized["source"]["normalized_sha256"] = "0" * 64
        compare.validate_report(changed_normalized)
        with self.assertRaises(compare.CompareError):
            compare.build_comparison(left, changed_normalized)

    def test_changed_method_does_not_claim_same_deterministic_measures(self):
        left = build_local_analysis(LEFT.encode("utf-8"))
        different = copy.deepcopy(left)
        different["analyzer"]["profiles"]["punctuation"] = "candidate-v99"
        different["metrics"]["fantlab.dialogue.share_percent"]["value"] += 1.0
        result = compare.build_comparison(left, different)
        self.assertTrue(all(row["comparison_status"] == "incomparable" for row in result["metrics"]))

    def test_schema_unit_source_and_numeric_mutations_rejected(self):
        edits = (
            lambda d: d["metrics"]["fantlab.dialogue.share_percent"].update(unit="ratio"),
            lambda d: d["metrics"]["fantlab.general.words"].update(value=True),
            lambda d: d["metrics"]["fantlab.general.words"].update(value=1.0),
            lambda d: d["metrics"]["fantlab.dialogue.share_percent"].update(value=101),
            lambda d: d["metrics"].pop("fantlab.general.words"),
            lambda d: d["source"].update(source_text_embedded=True),
            lambda d: d["source"].update(normalized_sha256="missing"),
            lambda d: d["source"].update(normalized_character_count=1),
            lambda d: d.update(manuscript=LEFT),
            lambda d: d["analyzer"]["profiles"].update(dialogue=None),
            lambda d: d["representativeness"].update(meets_calibration_threshold=True),
            lambda d: d["metrics"]["fantlab.punctuation.comma.per_1000_words"].update(raw_count=-1),
        )
        for edit in edits:
            with self.subTest(edit=str(edit)):
                artifact = copy.deepcopy(self.a)
                edit(artifact)
                with self.assertRaises(compare.CompareError):
                    compare.build_comparison(artifact, self.b)

    def test_mandatory_count_contract_rejects_null_and_impossible_counts(self):
        # Imported reports are untrusted declarations.  The actual analyzer
        # *always* emits these counts, even for the empty input.  None is only
        # allowed for genuinely undefined optional derived statistics.
        required = (
            "fantlab.general.words",
            "scriptorium.general.sentences",
            "fantlab.vocabulary.unique_words",
        )
        for metric_id in required:
            with self.subTest(metric_id=metric_id):
                poisoned = copy.deepcopy(self.a)
                poisoned["metrics"][metric_id]["value"] = None
                with self.assertRaises(compare.CompareError):
                    compare.build_comparison(poisoned, self.b)
        for metric_id in ("scriptorium.general.sentences", "fantlab.general.words"):
            with self.subTest(impossible_count=metric_id):
                poisoned = copy.deepcopy(self.a)
                poisoned["metrics"][metric_id]["value"] = (
                    poisoned["source"]["normalized_character_count"] + 1
                )
                with self.assertRaises(compare.CompareError):
                    compare.build_comparison(poisoned, self.b)
        # Genuine undefined metrics remain representable and comparable as
        # unavailable, rather than being silently synthesized as zero.
        result = compare.build_comparison(self.a, self.b)
        self.assertTrue(any(r["comparison_status"] == "unavailable" for r in result["metrics"]))

    def test_derived_punctuation_rate_integrity_is_enforced(self):
        # The canonical metrics-v4 engine derives all 14 rates using
        # raw_count * 1000.0 / words.  A schema-valid JSON report with a
        # different claimed denominator/rate cannot produce a trustworthy
        # comparison, even if its source digest fields look well formed.
        key = "fantlab.punctuation.comma.per_1000_words"
        baseline = self.a["metrics"][key]
        self.assertIsNotNone(baseline["value"])
        altered = copy.deepcopy(self.a)
        altered["metrics"][key]["value"] = baseline["value"] + 1.0
        with self.assertRaises(compare.CompareError):
            compare.build_comparison(altered, self.b)

        too_many = copy.deepcopy(self.a)
        count = too_many["source"]["normalized_character_count"] + 1
        too_many["metrics"][key]["raw_count"] = count
        words = too_many["metrics"]["fantlab.general.words"]["value"]
        too_many["metrics"][key]["value"] = count * 1000.0 / words
        with self.assertRaises(compare.CompareError):
            compare.build_comparison(too_many, self.b)

        missing = copy.deepcopy(self.a)
        missing["metrics"][key]["value"] = None
        with self.assertRaises(compare.CompareError):
            compare.build_comparison(missing, self.b)

    def test_dictionary_partition_and_window_integrity(self):
        valid = build_local_analysis(
            LEFT.encode("utf-8"), dictionary_words=["кот", "пёс"],
            dictionary_profile="tested-lexemes-v1",
        )
        compare.validate_report(valid)
        dictionary_key = "fantlab.vocabulary.active_dictionary"
        no_count = copy.deepcopy(valid)
        no_count["metrics"][dictionary_key]["value"] = None
        with self.assertRaises(compare.CompareError):
            compare.validate_report(no_count)

        wrong_partition = copy.deepcopy(valid)
        wrong_partition["metrics"][dictionary_key]["value"] += 1
        with self.assertRaises(compare.CompareError):
            compare.validate_report(wrong_partition)

        unexpected_window = copy.deepcopy(valid)
        unexpected_window["metrics"]["fantlab.vocabulary.uasz_3000"]["value"] = 0.0
        with self.assertRaises(compare.CompareError):
            compare.validate_report(unexpected_window)

        enough_words = build_local_analysis(
            ("Кот " * 3000).encode("utf-8"), dictionary_words=["кот"],
            dictionary_profile="tested-lexemes-v1",
        )
        self.assertIsNotNone(enough_words["metrics"]["fantlab.vocabulary.uasz_3000"]["value"])
        compare.validate_report(enough_words)
        contradictory = copy.deepcopy(enough_words)
        contradictory["metrics"]["fantlab.vocabulary.uasz_3000"]["value"] = None
        with self.assertRaises(compare.CompareError):
            compare.validate_report(contradictory)

    def test_punctuation_rates_are_unavailable_without_words(self):
        punctuation_only = build_local_analysis("?! ... —".encode("utf-8"))
        self.assertEqual(punctuation_only["metrics"]["fantlab.general.words"]["value"], 0)
        compare.validate_report(punctuation_only)
        with self.assertRaises(compare.CompareError):
            bad = copy.deepcopy(punctuation_only)
            bad["metrics"]["fantlab.punctuation.question.per_1000_words"]["value"] = 0.0
            compare.validate_report(bad)

    def test_private_html_csv_and_json_are_deterministic(self):
        result = compare.build_comparison(self.a, self.b)
        html = compare.render_html(result, title="My <a> Books")
        self.assertIn("My &lt;a&gt; Books", html)
        self.assertEqual(html.count("<th scope='row'>"), 29)
        self.assertIn("<caption>", html)
        self.assertIn("prefers-reduced-motion", html)
        self.assertNotIn(LEFT, html)
        self.assertNotIn("<script", html)
        exported = compare.render_json(result)
        self.assertEqual(exported, compare.render_json(result))
        self.assertEqual(json.loads(exported)["metrics"], result["metrics"])
        rows = list(csv.DictReader(io.StringIO(compare.render_csv(result))))
        self.assertEqual(len(rows), 29)
        self.assertEqual(rows[0]["left_sha256"], self.a["source"]["raw_sha256"])

    def test_signed_numeric_csv_difference_remains_numeric(self):
        result = compare.build_comparison(self.a, self.b)
        target = next(row for row in result["metrics"] if row["metric_id"] == "fantlab.general.words")
        self.assertTrue(target["difference"].startswith("-"), target["difference"])
        rows = list(csv.DictReader(io.StringIO(compare.render_csv(result))))
        exported = next(row for row in rows if row["metric_id"] == "fantlab.general.words")
        self.assertEqual(exported["difference"], target["difference"])
        self.assertFalse(exported["difference"].startswith("'"))

    def test_markdown_comparison_preserves_complete_source_free_evidence(self):
        compared = compare.build_comparison(self.a, self.b)
        title = "Notes <script>alert(1)</script> | `test`"
        report = compare.render_markdown(compared, title=title)
        self.assertEqual(report, compare.render_markdown(compared, title=title))
        self.assertIn("&lt;script&gt;", report)
        self.assertIn(r"\|", report)
        self.assertNotIn("<script>", report)
        self.assertNotIn(LEFT, report)
        self.assertNotIn(RIGHT, report)
        self.assertIn(self.a["source"]["raw_sha256"], report)
        self.assertIn(self.b["source"]["normalized_sha256"], report)
        self.assertIn("M2 0/5", report)
        self.assertIn("right minus left", report)
        self.assertIn("percentage", report)
        metrics_section = report.split("## All 29 measured fields\n", 1)[1]
        metric_lines = [line for line in metrics_section.splitlines()
                        if line.startswith("| ") and not line.startswith(("| Metric", "| :--"))]
        self.assertEqual(len(metric_lines), 29)
        self.assertIn("Unavailable", report)
        self.assertIn("inferred", report)

    def test_markdown_distinguishes_zero_unavailable_and_incompatible(self):
        same = compare.render_markdown(compare.build_comparison(self.a, self.a))
        words = next(line for line in same.splitlines()
                     if "| fantlab.general.words |" in line)
        self.assertIn("| 0 |", words)
        missing = next(line for line in same.splitlines()
                       if "| fantlab.vocabulary.uasz_3000 |" in line)
        self.assertIn("Unavailable", missing)
        incompatible = copy.deepcopy(self.b)
        incompatible["analyzer"]["profiles"]["metrics"] = "future-metrics-v99"
        report = compare.render_markdown(compare.build_comparison(self.a, incompatible))
        self.assertIn("Not comparable", report)
        self.assertNotIn("| 0 |", next(line for line in report.splitlines()
                         if "| fantlab.general.words |" in line))

    def test_markdown_rejects_forged_status_and_metric_registry(self):
        valid = compare.build_comparison(self.a, self.b)
        mutations = (
            lambda data: data.update(scientific_boundary="FantLab parity proven"),
            lambda data: data["metrics"].pop(),
            lambda data: data["metrics"][0].update(comparison_status="passed"),
            lambda data: data["metrics"][0].update(metric_id="<img src=x>"),
            lambda data: data["metrics"][0].update(difference="0") if
                data["metrics"][0]["comparison_status"] != "comparable" else
                data["metrics"][0].update(difference=None),
        )
        for mutate in mutations:
            with self.subTest(mutation=str(mutate)):
                forged = copy.deepcopy(valid)
                mutate(forged)
                with self.assertRaises(compare.CompareError):
                    compare.render_markdown(forged)

    def test_private_reader_cli_real_analyze_to_compare_all_formats(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left, right = root / "private-A.txt", root / "private-B.txt"
            left.write_text(LEFT, encoding="utf-8")
            right.write_text(RIGHT, encoding="utf-8")
            for source, output in ((left, root / "A.json"), (right, root / "B.json")):
                self.assertEqual(cli.main(["analyze", str(source), "--output", str(output)]), 0)
            for format_ in ("json", "html", "csv", "markdown"):
                output = root / ("comparison." + format_)
                self.assertEqual(cli.main(["compare", str(root / "A.json"), str(root / "B.json"),
                                           "--format", format_, "--output", str(output)]), 0)
                content = output.read_text(encoding="utf-8")
                self.assertNotIn(LEFT, content)
                self.assertNotIn(RIGHT, content)
                self.assertIn(self.a["source"]["raw_sha256"], content)
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    cli.main(["compare", str(root / "A.json"), str(root / "B.json"),
                              "--format", format_, "--output", str(output)])
                self.assertEqual(output.read_text(encoding="utf-8"), content)

    def test_adversarial_json_duplicate_key_nan_and_oversized_exponent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.json"
            valid = json.dumps(self.a, ensure_ascii=False)
            for poisoned in (
                valid.replace('"schema_version":', '"schema_version": "duplicate", "schema_version":', 1),
                valid.replace('"value": 0', '"value": NaN', 1),
                valid.replace('"value": 0', '"value": 1e999999', 1),
                valid.replace('"value": 0', '"value": 1000000000000000000000000', 1),
            ):
                with self.subTest(payload=poisoned[:50]):
                    source.write_text(poisoned, encoding="utf-8")
                    with self.assertRaises(compare.CompareError):
                        compare.load_report(source)

    def test_path_private_error_and_symlink_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "PRIVATE-INVALID-JSON"
            good = root / "good.json"
            target = root / "original-output.csv"
            source.write_text("{bad", encoding="utf-8")
            good.write_text(json.dumps(self.b), encoding="utf-8")
            target.write_text("preserve me", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as exc:
                cli.main(["compare", str(source), str(good), "--format", "csv", "--output", str(target)])
            self.assertEqual(exc.exception.code, 2)
            self.assertNotIn(str(source), stderr.getvalue())
            self.assertNotIn("PRIVATE", stderr.getvalue())
            self.assertEqual(target.read_text(encoding="utf-8"), "preserve me")
            alias = root / "symlink.json"
            try:
                alias.symlink_to(good)
            except (OSError, NotImplementedError):
                self.skipTest("no symlink support")
            with self.assertRaises(Exception):
                compare.load_report(alias)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO is POSIX-specific")
    def test_fifo_rejected_without_hanging(self):
        with tempfile.TemporaryDirectory() as tmp:
            fifo = Path(tmp) / "private-input.fifo"
            os.mkfifo(fifo)
            cmd = [sys.executable, "-m", "scriptorium", "compare", str(fifo), str(fifo)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(tmp, result.stderr)


if __name__ == "__main__":
    unittest.main()
