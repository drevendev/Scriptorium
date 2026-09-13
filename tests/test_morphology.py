import unittest

from scriptorium.morphology import (
    FANTLAB_POS_BUCKETS,
    MAX_POSITION,
    POS_MAPPING_CONTRACT,
    POS_PROFILE,
    POS_SCHEMA_VERSION,
    analyze_pos_metrics,
    resolve_runtime_pos,
)
from scriptorium.text import NORMALIZATION_PROFILE


class MorphologyMetricTests(unittest.TestCase):
    def test_resolution_is_conservative(self):
        self.assertEqual(resolve_runtime_pos(["A"]), "adjective")
        self.assertEqual(resolve_runtime_pos(["A", "A"]), "adjective")
        self.assertIsNone(resolve_runtime_pos([]))
        self.assertIsNone(resolve_runtime_pos(["A", "V"]))
        self.assertIsNone(resolve_runtime_pos(["N"]))
        self.assertIsNone(resolve_runtime_pos(["POSL"]))
        self.assertIsNone(resolve_runtime_pos(["UNKNOWN"]))
        with self.assertRaises(TypeError):
            resolve_runtime_pos(["A", 3])

    def test_empty_input_keeps_undefined_rates_null(self):
        artifact = analyze_pos_metrics("", [], runtime_profile="fixture")
        self.assertEqual(artifact["input"], {"word_count": 0, "sentence_count": 0})
        self.assertEqual(artifact["metrics"]["defined"]["count"], 0)
        self.assertEqual(artifact["metrics"]["undefined"]["count"], 0)
        self.assertIsNone(artifact["metrics"]["defined"]["percent_of_words"])
        self.assertIsNone(
            artifact["metrics"]["bigrams"]["adjective"]["verb"]["per_1000_words"]
        )
        self.assertIsNone(artifact["metrics"]["positions"]["1"]["verb"]["percent"])

    def test_distribution_counts_only_consensus_direct_mappings(self):
        artifact = analyze_pos_metrics(
            "Красный бежит быстро спорно число после.",
            [["A"], ["V", "V"], ["ADV"], ["A", "V"], ["N"], ["POSL"]],
            runtime_profile="fixture",
        )
        metrics = artifact["metrics"]
        self.assertEqual(metrics["defined"]["count"], 3)
        self.assertEqual(metrics["undefined"]["count"], 3)
        self.assertEqual(metrics["defined"]["percent_of_words"], 50.0)
        self.assertEqual(metrics["buckets"]["adjective"]["count"], 1)
        self.assertEqual(metrics["buckets"]["verb"]["count"], 1)
        self.assertEqual(metrics["buckets"]["adverb"]["count"], 1)
        self.assertAlmostEqual(
            metrics["buckets"]["adjective"]["percent_of_defined"], 100 / 3
        )
        self.assertIsNone(metrics["service_words"]["count"])
        self.assertEqual(metrics["service_words"]["status"], "unresolved")

    def test_bigrams_are_sentence_bounded_and_use_total_words_denominator(self):
        artifact = analyze_pos_metrics(
            "Красный бежит. Тихий спит.",
            [["A"], ["V"], ["A"], ["V"]],
            runtime_profile="fixture",
        )
        bigrams = artifact["metrics"]["bigrams"]
        self.assertEqual(bigrams["adjective"]["verb"]["raw_count"], 2)
        self.assertEqual(bigrams["adjective"]["verb"]["per_1000_words"], 500.0)
        self.assertEqual(bigrams["verb"]["adjective"]["raw_count"], 0)
        self.assertEqual(bigrams["verb"]["adjective"]["per_1000_words"], 0.0)

    def test_unresolved_token_breaks_bigram(self):
        artifact = analyze_pos_metrics(
            "Красный число спит.",
            [["A"], ["N"], ["V"]],
            runtime_profile="fixture",
        )
        bigrams = artifact["metrics"]["bigrams"]
        self.assertEqual(bigrams["adjective"]["verb"]["raw_count"], 0)

    def test_position_probability_uses_all_sentences_as_denominator(self):
        artifact = analyze_pos_metrics(
            "Красный. Тихий спит.",
            [["A"], ["A"], ["V"]],
            runtime_profile="fixture",
        )
        positions = artifact["metrics"]["positions"]
        self.assertEqual(positions["1"]["adjective"]["raw_count"], 2)
        self.assertEqual(positions["1"]["adjective"]["percent"], 100.0)
        self.assertEqual(positions["2"]["verb"]["raw_count"], 1)
        self.assertEqual(positions["2"]["verb"]["percent"], 50.0)
        self.assertEqual(positions["3"]["verb"]["percent"], 0.0)

    def test_positions_stop_at_twenty(self):
        text = " ".join(f"слово{i}" for i in range(21)) + "."
        artifact = analyze_pos_metrics(text, [["A"]] * 21, runtime_profile="fixture")
        positions = artifact["metrics"]["positions"]
        self.assertEqual(len(positions), MAX_POSITION)
        self.assertEqual(positions["20"]["adjective"]["percent"], 100.0)
        self.assertNotIn("21", positions)

    def test_alignment_and_runtime_profile_are_required(self):
        with self.assertRaises(ValueError):
            analyze_pos_metrics("одно два", [["A"]], runtime_profile="fixture")
        with self.assertRaises(ValueError):
            analyze_pos_metrics("", [], runtime_profile="  ")

    def test_artifact_identity_and_matrix_shape_are_deterministic(self):
        first = analyze_pos_metrics(
            "Красный бежит.", [["A"], ["V"]], runtime_profile="fixture"
        )
        second = analyze_pos_metrics(
            "Красный бежит.", [["A"], ["V"]], runtime_profile="fixture"
        )
        self.assertEqual(first, second)
        self.assertEqual(first["schema_version"], POS_SCHEMA_VERSION)
        self.assertEqual(first["profile"], POS_PROFILE)
        self.assertEqual(first["text_profile"], NORMALIZATION_PROFILE)
        self.assertEqual(first["mapping_contract"], POS_MAPPING_CONTRACT)
        self.assertEqual(tuple(first["metrics"]["buckets"]), FANTLAB_POS_BUCKETS)
        self.assertEqual(len(first["metrics"]["bigrams"]), 17)
        self.assertTrue(
            all(len(row) == 17 for row in first["metrics"]["bigrams"].values())
        )

    def test_text_identity_distinguishes_segmentation_with_same_runtime_matrix(self):
        candidates = [["A"], ["V"], ["A"], ["V"]]
        first = analyze_pos_metrics("А Б. В Г.", candidates, runtime_profile="fixture")
        second = analyze_pos_metrics("А. Б В Г.", candidates, runtime_profile="fixture")

        self.assertEqual(first["runtime_analysis_sha256"], second["runtime_analysis_sha256"])
        self.assertEqual(first["input"], {"word_count": 4, "sentence_count": 2})
        self.assertEqual(second["input"], first["input"])
        self.assertEqual(first["text_profile"], NORMALIZATION_PROFILE)
        self.assertEqual(second["text_profile"], NORMALIZATION_PROFILE)
        self.assertNotEqual(first["normalized_sha256"], second["normalized_sha256"])
        self.assertEqual(first["metrics"]["bigrams"]["adjective"]["verb"]["raw_count"], 2)
        self.assertEqual(second["metrics"]["bigrams"]["adjective"]["verb"]["raw_count"], 1)
        self.assertEqual(second["metrics"]["bigrams"]["verb"]["adjective"]["raw_count"], 1)


if __name__ == "__main__":
    unittest.main()
