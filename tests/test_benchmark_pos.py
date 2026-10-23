"""Cross-artifact FantLab POS joins: positive and negative source-free regressions."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.benchmark import build_comparison, main
from scriptorium.benchmark_pos import build_pos_comparisons, strict_json, validate_pos_artifact
from scriptorium.morphology import FANTLAB_POS_BUCKETS, analyze_pos_metrics

ROOT = Path(__file__).resolve().parents[1]
REF = (ROOT / "benchmarks/fantlab/work488.json").read_text(encoding="utf-8")
TEXT = "Красный бежит. Тихий спит."
ROWS = [["A"], ["V"], ["A"], ["N"]]


def run_fixture(pos=None):
    if pos is None:
        pos = analyze_pos_metrics(TEXT, ROWS, runtime_profile="test-aot-sidecar")
    return build_comparison(REF, TEXT.encode("utf-8"), scriptorium_revision="test", pos_artifact=pos)


class FantLabPosJoinTests(unittest.TestCase):
    def setUp(self):
        self.pos = analyze_pos_metrics(TEXT, ROWS, runtime_profile="test-aot-sidecar")

    def test_40_rows_are_diagnostic_without_claimed_pos_parity(self):
        output = run_fixture(self.pos)
        rows = {key: value for key, value in output["metrics"].items() if key.startswith("fantlab.pos.")}
        self.assertEqual(len(rows), 40)
        self.assertTrue(all(value["comparison"]["result"] in ("unresolved", "not_run") for value in rows.values()))
        self.assertEqual(rows["fantlab.pos.undefined.count"]["actual"]["raw_value"], 1)
        self.assertEqual(rows["fantlab.pos.buckets.adjective.count"]["actual"]["raw_value"], 2)
        self.assertEqual(rows["fantlab.pos.buckets.pronoun_noun.count"]["actual"]["raw_value"], 0)
        self.assertEqual(rows["fantlab.pos.service_words.count"]["expected"]["numeric_value"], 14410)
        self.assertIsNone(rows["fantlab.pos.service_words.count"]["actual"]["raw_value"])
        self.assertEqual(rows["fantlab.pos.service_words.count"]["comparison"]["result"], "unresolved")
        self.assertEqual(rows["fantlab.pos.buckets.pronoun_predicative.percent_of_defined"]["expected"]["display_text"], "0.0")
        self.assertEqual(output["analyzer"]["morphology_provider"], "test-aot-sidecar")
        self.assertEqual(len(output["analyzer"]["morphology_version"].split("@sha256:")[-1]), 64)
        self.assertNotIn("Красный", json.dumps(output, ensure_ascii=False))
        self.assertFalse(any(value["comparison"]["result"] == "pass" for value in rows.values()))

    def test_reference_categories_need_not_partition_fantlab_defined_words(self):
        ref = json.loads(REF)
        self.assertGreater(sum(v["count"] for v in ref["expected"]["pos"].values()), ref["expected"]["defined_pos_words"])
        self.assertEqual(len([k for k in run_fixture()["metrics"] if k.startswith("fantlab.pos.")]), 40)

    def test_default_benchmark_remains_unchanged_without_pos_artifact(self):
        old = build_comparison(REF, TEXT.encode("utf-8"), scriptorium_revision="test")
        self.assertFalse(any(k.startswith("fantlab.pos.") for k in old["metrics"]))
        self.assertNotIn("morphology_provider", old["analyzer"])

    def test_denies_forged_cross_text_and_counts_and_mapping_profile(self):
        mutations = [
            ("normalized_sha256", "0" * 64),
            ("mapping_contract", "fake-compatible-v1"),
            ("profile", "not-scriptorium-pos"),
            ("compatibility_status", "reproduced"),
        ]
        for key, value in mutations:
            candidate = copy.deepcopy(self.pos)
            candidate[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "POS"):
                run_fixture(candidate)
        for key in ("word_count", "sentence_count"):
            candidate = copy.deepcopy(self.pos)
            candidate["input"][key] += 1
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "POS"):
                run_fixture(candidate)

    def test_rejects_false_zero_service_words(self):
        candidate = copy.deepcopy(self.pos)
        candidate["metrics"]["service_words"]["count"] = 0
        with self.assertRaisesRegex(ValueError, "service-word"):
            run_fixture(candidate)

    def test_rejects_bucket_accounting_or_rate_corruption(self):
        candidate = copy.deepcopy(self.pos)
        candidate["metrics"]["buckets"]["verb"]["count"] += 1
        with self.assertRaises(ValueError):
            run_fixture(candidate)
        candidate = copy.deepcopy(self.pos)
        candidate["metrics"]["buckets"]["adjective"]["percent_of_defined"] = 99.0
        with self.assertRaisesRegex(ValueError, "denominator"):
            run_fixture(candidate)
        candidate = copy.deepcopy(self.pos)
        candidate["metrics"]["defined"]["count"] = True
        with self.assertRaisesRegex(ValueError, "finite number"):
            run_fixture(candidate)

    def test_rejects_wrong_matrix_bucket_or_position_shape(self):
        for layer in ("bigrams", "positions"):
            candidate = copy.deepcopy(self.pos)
            next(iter(candidate["metrics"][layer].values())).pop("adjective")
            with self.subTest(layer=layer), self.assertRaises(ValueError):
                run_fixture(candidate)
        candidate = copy.deepcopy(self.pos)
        candidate["metrics"]["positions"].pop("20")
        with self.assertRaises(ValueError):
            run_fixture(candidate)
        candidate = copy.deepcopy(self.pos)
        candidate["metrics"]["bigrams"]["adjective"]["verb"]["raw_count"] = 99
        with self.assertRaises(ValueError):
            run_fixture(candidate)
        candidate = copy.deepcopy(self.pos)
        candidate["metrics"]["positions"]["1"]["adjective"]["raw_count"] = 99
        with self.assertRaises(ValueError):
            run_fixture(candidate)

    def test_duplicate_keys_and_nonfinite_json_fail_closed(self):
        for doc in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            with self.subTest(doc=doc), self.assertRaises(ValueError):
                strict_json(doc)

    def test_reference_forgery_and_missing_bucket_fail(self):
        altered = json.loads(REF)
        altered["expected"]["defined_pos_words"] += 1
        with self.assertRaisesRegex(ValueError, "partition"):
            build_pos_comparisons(altered, strict_json(REF), self.pos,
                                  normalized_sha256=self.pos["normalized_sha256"],
                                  word_count=4, sentence_count=2)
        altered = json.loads(REF)
        altered["expected"]["pos"].pop("noun")
        with self.assertRaisesRegex(ValueError, "FantLab POS buckets"):
            build_pos_comparisons(altered, strict_json(REF), self.pos,
                                  normalized_sha256=self.pos["normalized_sha256"],
                                  word_count=4, sentence_count=2)

    def test_zero_word_artifact_valid_if_all_denominators_null(self):
        pos = analyze_pos_metrics("", [], runtime_profile="test-aot-sidecar")
        validate_pos_artifact(pos, normalized_sha256=pos["normalized_sha256"], word_count=0, sentence_count=0)
        pos["metrics"]["bigrams"]["noun"]["adjective"]["per_1000_words"] = 0.0
        with self.assertRaisesRegex(ValueError, "null"):
            validate_pos_artifact(pos, normalized_sha256=pos["normalized_sha256"], word_count=0, sentence_count=0)

    def test_real_cli_accepts_pos_artifact_and_preserves_reference_lexemes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference, manuscript, pos_file, output = [root / name for name in ("reference.json", "source.txt", "pos.json", "result.json")]
            reference.write_text(REF, encoding="utf-8")
            manuscript.write_text(TEXT, encoding="utf-8")
            pos_file.write_text(json.dumps(self.pos, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(main(["--reference", str(reference), "--text", str(manuscript),
                                   "--scriptorium-revision", "fixture", "--pos-metrics", str(pos_file),
                                   "--output", str(output)]), 0)
            artifact = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(len([k for k in artifact["metrics"] if k.startswith("fantlab.pos.")]), 40)
            self.assertEqual(artifact["metrics"]["fantlab.punctuation.question.per_1000_words"]["expected"]["display_text"], "10.30")
            pos_file.write_text('{"schema_version":"fake","schema_version":"fake"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                main(["--reference", str(reference), "--text", str(manuscript),
                      "--scriptorium-revision", "fixture", "--pos-metrics", str(pos_file)])


if __name__ == "__main__":
    unittest.main()
