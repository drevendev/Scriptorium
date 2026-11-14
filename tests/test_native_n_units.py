"""Pure arithmetic regressions for source-free native N conditional rates."""
from __future__ import annotations

import unittest
from scriptorium.native_n_units import normalized_n_bounds


class NativeNUnitTests(unittest.TestCase):
    def example(self):
        return {
            "counts": {"word_count": 100, "sentence_count": 20, "conditional_defined": 50},
            "bucket_bounds": {"noun": [0, 10], "cardinal": [0, 10]},
            "bigram_bounds": [{"first": "noun", "second": "cardinal",
                               "min": 1, "max": 5, "independent_edge_upper": 7}],
            "sentence_position_bounds": [{"position": 1, "min": 2, "max": 5}],
            "native_controls": {
                "noun_examples": {"token_count": 3, "n_only": 3},
                "cardinal_examples": {"token_count": 3, "n_only": 2},
                "other_pos_controls": {"token_count": 3, "n_only": 0},
            },
        }

    def test_denominators_and_conditional_intervals(self):
        result = normalized_n_bounds(self.example())
        self.assertEqual(result["denominators"], {
            "word_tokens": 100, "all_sentences": 20, "conditionally_defined_tokens": 50,
        })
        self.assertEqual(result["bucket_percent_of_conditional_defined"]["noun"], [0.0, 20.0])
        self.assertEqual(result["bigram_per_1000_word_tokens"], [{
            "first": "noun", "second": "cardinal", "min": 10.0,
            "max": 50.0, "independent_edge_upper": 70.0,
        }])
        self.assertEqual(result["sentence_position_percent_of_all_sentences"], [
            {"position": 1, "min": 10.0, "max": 25.0},
        ])
        self.assertIn("not_observed", result["status"])
        self.assertEqual(result["schema_version"], "scriptorium-native-n-conditional-units-v2")
        self.assertEqual(result["native_control_n_only_percent_of_annotated_examples"], {
            "noun_examples": 100.0,
            "cardinal_examples": 200 / 3,
            "other_pos_controls": 0.0,
        })

    def test_invalid_denominators_fail_closed(self):
        for key, value in (("word_count", 0), ("word_count", True),
                           ("word_count", 100.0), ("sentence_count", 0),
                           ("conditionally_defined", 0)):
            witness = self.example()
            field = "conditional_defined" if key == "conditionally_defined" else key
            witness["counts"][field] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                normalized_n_bounds(witness)

    def test_noninteger_and_negative_counts_fail_closed(self):
        for value in (True, -1, 2.5):
            witness = self.example()
            witness["bigram_bounds"][0]["max"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalized_n_bounds(witness)

    def test_small_native_controls_are_not_false_precision_or_accuracy(self):
        example = self.example()
        example["native_controls"]["noun_examples"] = {"token_count": 0, "n_only": 0}
        self.assertIsNone(normalized_n_bounds(example)[
            "native_control_n_only_percent_of_annotated_examples"]["noun_examples"])
        for tested, observed in ((True, 1), (3, True), (-1, 0), (2, 3), (2.0, 1), (1, -1)):
            example = self.example()
            example["native_controls"]["noun_examples"] = {
                "token_count": tested, "n_only": observed}
            with self.subTest(tested=tested, observed=observed), self.assertRaises(ValueError):
                normalized_n_bounds(example)
        example = self.example()
        del example["native_controls"]["other_pos_controls"]
        with self.assertRaises(ValueError):
            normalized_n_bounds(example)


if __name__ == "__main__":
    unittest.main()
