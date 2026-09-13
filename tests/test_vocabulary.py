import unittest

from scriptorium.metrics import analyze_deterministic_metrics
from scriptorium.vocabulary import (
    VOCABULARY_PROFILE,
    analyze_vocabulary,
    dictionary_lexemes_sha256,
    mean_unique_dictionary_words,
    normalize_dictionary_lexemes,
    normalize_lexeme,
    rolling_unique_dictionary_counts,
    vocabulary_lexemes,
)


class VocabularyTests(unittest.TestCase):
    def test_lexical_identity_is_nfc_text_token_plus_casefold(self):
        lexemes = vocabulary_lexemes(
            "Кот кот КОТ Ёж е\u0308ж рок-н-ролл РОК-Н-РОЛЛ"
        )

        self.assertEqual(
            lexemes,
            ("кот", "кот", "кот", "ёж", "ёж", "рок-н-ролл", "рок-н-ролл"),
        )
        self.assertEqual(normalize_lexeme("е\u0308ж"), "ёж")

    def test_unique_words_work_without_dictionary_dependency(self):
        result = analyze_vocabulary("Кот кот Пёс дракон")

        self.assertEqual(result["profile"], VOCABULARY_PROFILE)
        self.assertEqual(result["unique_words"], 3)
        self.assertIsNone(result["dictionary_dependency"])
        self.assertIsNone(result["active_dictionary"])
        self.assertIsNone(result["active_nondictionary"])
        self.assertIsNone(result["uasz_3000"])
        self.assertIsNone(result["uasz_10000"])
        self.assertIsNone(result["uasz_100000"])

    def test_dictionary_arguments_are_an_all_or_nothing_dependency(self):
        with self.assertRaisesRegex(ValueError, "requires dictionary_words"):
            analyze_vocabulary("Кот", dictionary_profile="test-v1")
        with self.assertRaisesRegex(ValueError, "require a non-empty"):
            analyze_vocabulary("Кот", dictionary_words=["кот"])
        with self.assertRaisesRegex(ValueError, "require a non-empty"):
            analyze_vocabulary("Кот", dictionary_words=["кот"], dictionary_profile="  ")

    def test_dictionary_partition_and_digest_are_reproducible(self):
        dictionary = normalize_dictionary_lexemes(["ПЁС", "кот", "КОТ", "  "])
        result = analyze_vocabulary(
            "Кот кот Пёс дракон",
            dictionary_words=["ПЁС", "кот", "КОТ", "  "],
            dictionary_profile="test-dictionary-v1",
        )

        self.assertEqual(result["unique_words"], 3)
        self.assertEqual(result["active_dictionary"], 2)
        self.assertEqual(result["active_nondictionary"], 1)
        self.assertEqual(
            result["dictionary_dependency"],
            {
                "profile": "test-dictionary-v1",
                "normalized_lexemes_sha256": dictionary_lexemes_sha256(dictionary),
                "lexeme_count": 2,
            },
        )
        self.assertEqual(
            dictionary_lexemes_sha256(dictionary),
            dictionary_lexemes_sha256(reversed(sorted(dictionary))),
        )

    def test_dictionary_unicode_composition_has_one_identity_and_digest(self):
        composed = normalize_dictionary_lexemes(["ёж"])
        decomposed = normalize_dictionary_lexemes(["е\u0308ж"])

        self.assertEqual(composed, decomposed)
        self.assertEqual(dictionary_lexemes_sha256(composed), dictionary_lexemes_sha256(decomposed))

    def test_decomposed_dictionary_lexeme_matches_equivalent_text_token(self):
        result = analyze_vocabulary(
            "Ёж волк",
            dictionary_words=["е\u0308ж"],
            dictionary_profile="unicode-test-v1",
        )

        self.assertEqual(result["unique_words"], 2)
        self.assertEqual(result["active_dictionary"], 1)
        self.assertEqual(result["active_nondictionary"], 1)

    def test_rolling_windows_advance_one_token_without_rebuilding_sets(self):
        lexemes = ("a", "b", "c", "c")
        dictionary = frozenset({"a", "b", "c"})

        self.assertEqual(
            rolling_unique_dictionary_counts(lexemes, 2, dictionary),
            (2, 2, 1),
        )
        self.assertAlmostEqual(
            mean_unique_dictionary_words(lexemes, 2, dictionary),
            5 / 3,
        )

    def test_window_edges_require_a_complete_window(self):
        dictionary = frozenset({"a", "b", "c"})

        self.assertEqual(
            rolling_unique_dictionary_counts(("a", "a", "b"), 3, dictionary),
            (2,),
        )
        self.assertEqual(
            rolling_unique_dictionary_counts(("a", "b"), 3, dictionary),
            (),
        )
        self.assertIsNone(
            mean_unique_dictionary_words(("a", "b"), 3, dictionary)
        )
        with self.assertRaisesRegex(ValueError, "positive"):
            rolling_unique_dictionary_counts(("a",), 0, dictionary)

    def test_metric_artifact_records_dictionary_dependency_and_uasz_3000(self):
        text = " ".join(("а", "б") * 1500)
        artifact = analyze_deterministic_metrics(
            text,
            dictionary_words=["а", "б"],
            dictionary_profile="tiny-test-v1",
        )
        metrics = artifact["metrics"]
        dependency = artifact["dependencies"]["vocabulary_dictionary"]

        self.assertEqual(metrics["fantlab.vocabulary.unique_words"]["value"], 2)
        self.assertEqual(metrics["fantlab.vocabulary.active_dictionary"]["value"], 2)
        self.assertEqual(metrics["fantlab.vocabulary.active_nondictionary"]["value"], 0)
        self.assertEqual(metrics["fantlab.vocabulary.uasz_3000"]["value"], 2.0)
        self.assertIsNone(metrics["fantlab.vocabulary.uasz_10000"]["value"])
        self.assertEqual(dependency["profile"], "tiny-test-v1")
        self.assertEqual(dependency["lexeme_count"], 2)
        self.assertRegex(dependency["normalized_lexemes_sha256"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
