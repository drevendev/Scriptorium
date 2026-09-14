import json
from pathlib import Path
import unittest

from scriptorium.dialogue import DIALOGUE_PROFILE
from scriptorium.metrics import (
    METRIC_PROFILE,
    PUNCTUATION_KEYS,
    PUNCTUATION_PROFILE,
    SCHEMA_VERSION,
    analyze_deterministic_metrics,
    punctuation_counts,
)
from scriptorium.vocabulary import VOCABULARY_PROFILE


class DeterministicMetricTests(unittest.TestCase):
    def test_general_metrics_use_text_model_and_explicit_statuses(self):
        artifact = analyze_deterministic_metrics("Кот спит. Пёс идёт!")
        metrics = artifact["metrics"]

        self.assertEqual(metrics["fantlab.general.characters"]["value"], 19)
        self.assertEqual(metrics["fantlab.general.words"]["value"], 4)
        self.assertEqual(metrics["scriptorium.general.sentences"]["value"], 2)
        self.assertEqual(
            metrics["fantlab.general.mean_word_length_chars"]["value"],
            (3 + 4 + 3 + 4) / 4,
        )
        self.assertEqual(
            metrics["fantlab.general.mean_sentence_length_chars"]["value"],
            (9 + 9) / 2,
        )
        self.assertEqual(metrics["fantlab.vocabulary.unique_words"]["value"], 4)
        self.assertIsNone(metrics["fantlab.vocabulary.active_dictionary"]["value"])
        self.assertEqual(
            metrics["fantlab.general.characters"]["compatibility_status"], "inferred"
        )
        self.assertEqual(
            metrics["scriptorium.general.sentences"]["compatibility_status"], "extension"
        )

    def test_empty_text_preserves_zero_counts_and_undefined_rates(self):
        artifact = analyze_deterministic_metrics("")
        metrics = artifact["metrics"]

        self.assertEqual(metrics["fantlab.general.characters"]["value"], 0)
        self.assertEqual(metrics["fantlab.general.words"]["value"], 0)
        self.assertEqual(metrics["scriptorium.general.sentences"]["value"], 0)
        self.assertEqual(metrics["fantlab.vocabulary.unique_words"]["value"], 0)
        self.assertIsNone(metrics["fantlab.general.mean_word_length_chars"]["value"])
        self.assertIsNone(metrics["fantlab.general.mean_sentence_length_chars"]["value"])
        self.assertIsNone(metrics["fantlab.vocabulary.active_dictionary"]["value"])
        self.assertIsNone(metrics["fantlab.vocabulary.uasz_3000"]["value"])
        self.assertIsNone(artifact["dependencies"]["vocabulary_dictionary"])
        for key in PUNCTUATION_KEYS:
            row = metrics[f"fantlab.punctuation.{key}.per_1000_words"]
            self.assertEqual(row["raw_count"], 0)
            self.assertIsNone(row["value"])

    def test_punctuation_compounds_are_non_overlapping(self):
        counts = punctuation_counts(
            'а?! б!.. в?.. г... д!!! е… — ж, (з) «и»: "к"; л.'
        )

        expected = {key: 0 for key in PUNCTUATION_KEYS}
        expected.update(
            {
                "question_exclamation": 1,
                "exclamation_ellipsis": 1,
                "question_ellipsis": 1,
                "ellipsis": 2,
                "triple_exclamation": 1,
                "dash": 1,
                "comma": 1,
                "parentheses": 1,
                "quote": 4,
                "colon": 1,
                "semicolon": 1,
                "period": 1,
            }
        )
        self.assertEqual(counts, expected)

    def test_lexical_ascii_hyphens_are_not_dash_events(self):
        counts = punctuation_counts("кто-то 12-34 кто - то ‐ ‑ ‒ – —")

        # ASCII hyphens retained inside current text-v1 word tokens are lexical
        # connectors for punctuation-v2. A spaced ASCII hyphen and every supported
        # Unicode dash-family glyph remain punctuation candidates.
        self.assertEqual(counts["dash"], 7)

        artifact = analyze_deterministic_metrics("кто-то кто - то")
        dash = artifact["metrics"]["fantlab.punctuation.dash.per_1000_words"]
        self.assertEqual(dash["raw_count"], 1)
        self.assertAlmostEqual(dash["value"], 1000 / 3)

    def test_punctuation_rates_keep_raw_counts_for_diagnostics(self):
        metrics = analyze_deterministic_metrics("раз, два, три.")["metrics"]

        comma = metrics["fantlab.punctuation.comma.per_1000_words"]
        period = metrics["fantlab.punctuation.period.per_1000_words"]
        self.assertEqual(comma["raw_count"], 2)
        self.assertAlmostEqual(comma["value"], 2000 / 3)
        self.assertEqual(period["raw_count"], 1)
        self.assertAlmostEqual(period["value"], 1000 / 3)

    def test_profiles_and_digest_are_deterministic(self):
        first = analyze_deterministic_metrics("е\u0308\r\nТест.")
        second = analyze_deterministic_metrics("е\u0308\r\nТест.")

        self.assertEqual(first, second)
        self.assertEqual(first["schema_version"], SCHEMA_VERSION)
        self.assertEqual(first["profiles"]["metrics"], METRIC_PROFILE)
        self.assertEqual(first["profiles"]["dialogue"], DIALOGUE_PROFILE)
        self.assertEqual(first["profiles"]["vocabulary"], VOCABULARY_PROFILE)
        self.assertEqual(first["profiles"]["punctuation"], PUNCTUATION_PROFILE)
        self.assertIsNone(first["dependencies"]["vocabulary_dictionary"])
        self.assertEqual(
            first["normalized_sha256"],
            "852e7a3dce82ea35581c89365ace4ea9e3dd22d754dd37f127c37de62392c349",
        )

    def test_schema_is_valid_json_and_names_same_profile(self):
        schema_path = Path(__file__).parents[1] / "schemas" / f"{SCHEMA_VERSION}.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        self.assertEqual(
            schema["properties"]["schema_version"]["const"],
            SCHEMA_VERSION,
        )
        self.assertEqual(
            schema["properties"]["profiles"]["properties"]["metrics"]["const"],
            METRIC_PROFILE,
        )
        self.assertEqual(
            schema["properties"]["profiles"]["properties"]["dialogue"]["const"],
            DIALOGUE_PROFILE,
        )
        self.assertEqual(
            schema["properties"]["profiles"]["properties"]["vocabulary"]["const"],
            VOCABULARY_PROFILE,
        )
        self.assertEqual(
            schema["properties"]["profiles"]["properties"]["punctuation"]["const"],
            PUNCTUATION_PROFILE,
        )
        self.assertEqual(len(schema["properties"]["metrics"]["required"]), 29)
        self.assertFalse(schema["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
