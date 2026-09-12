import unittest

from scriptorium.text import (
    NORMALIZATION_PROFILE,
    TextSpan,
    normalize_text,
    sentence_spans,
    word_tokens,
)


class NormalizeTextTests(unittest.TestCase):
    def test_profile_is_versioned(self):
        self.assertEqual(NORMALIZATION_PROFILE, "scriptorium-text-v1")

    def test_normalizes_newlines_and_unicode_composition(self):
        decomposed = "е\u0308\r\nстрока\rфинал"
        self.assertEqual(normalize_text(decomposed), "ё\nстрока\nфинал")

    def test_preserves_non_newline_whitespace_and_punctuation(self):
        text = "  слово\t— слово  "
        self.assertEqual(normalize_text(text), text)

    def test_rejects_non_string_input(self):
        with self.assertRaises(TypeError):
            normalize_text(b"text")


class WordTokenTests(unittest.TestCase):
    def test_cyrillic_mixed_tokens_and_exact_offsets(self):
        text = "Ёжик, по-настоящему 2026 и rock’n’roll."
        self.assertEqual(
            word_tokens(text),
            (
                TextSpan("Ёжик", 0, 4),
                TextSpan("по-настоящему", 6, 19),
                TextSpan("2026", 20, 24),
                TextSpan("и", 25, 26),
                TextSpan("rock’n’roll", 27, 38),
            ),
        )

    def test_underscore_splits_candidate_tokens(self):
        self.assertEqual(
            word_tokens("два_слова"),
            (TextSpan("два", 0, 3), TextSpan("слова", 4, 9)),
        )

    def test_offsets_reference_normalized_text(self):
        text = "е\u0308\r\nтест"
        normalized = normalize_text(text)
        tokens = word_tokens(text)
        self.assertEqual(tokens, (TextSpan("ё", 0, 1), TextSpan("тест", 2, 6)))
        for token in tokens:
            self.assertEqual(normalized[token.start:token.end], token.text)


class SentenceSpanTests(unittest.TestCase):
    def test_mixed_terminators_closing_quote_ellipsis_and_tail(self):
        text = "  «Привет!»  Как дела?.. Хорошо\nПоследняя"
        self.assertEqual(
            sentence_spans(text),
            (
                TextSpan("«Привет!»", 2, 11),
                TextSpan("Как дела?..", 13, 24),
                TextSpan("Хорошо\nПоследняя", 25, 41),
            ),
        )

    def test_end_of_text_terminator_is_included(self):
        self.assertEqual(
            sentence_spans("Раз? Да!"),
            (TextSpan("Раз?", 0, 4), TextSpan("Да!", 5, 8)),
        )

    def test_blank_input_has_no_sentences(self):
        self.assertEqual(sentence_spans(" \n\t "), ())

    def test_repeated_execution_is_deterministic(self):
        text = "Первое. Второе?.. Третье"
        self.assertEqual(sentence_spans(text), sentence_spans(text))
        self.assertEqual(word_tokens(text), word_tokens(text))


if __name__ == "__main__":
    unittest.main()
