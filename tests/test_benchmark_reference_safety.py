"""Reject ambiguous expected values before any literary-text computation."""
import unittest
from unittest.mock import patch

from scriptorium.benchmark import build_comparison


class BenchmarkReferenceSafetyTests(unittest.TestCase):
    def test_duplicate_keys_are_rejected_without_pos(self):
        for raw in (
            '{"benchmark_id":"one","benchmark_id":"two","expected":{"characters":1}}',
            '{"benchmark_id":"test","expected":{"characters":99,"characters":1}}',
        ):
            with self.subTest(raw=raw), patch('scriptorium.benchmark.analyze_deterministic_metrics') as analyze:
                with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
                    build_comparison(raw, b'A', scriptorium_revision='synthetic')
                analyze.assert_not_called()

    def test_invalid_numbers_are_rejected_before_analysis(self):
        for key, token in (
            ('characters', 'true'), ('words', 'false'), ('characters', '1.0'),
            ('words', '-1'), ('mean_word_length_characters', 'true'),
            ('mean_word_length_characters', 'NaN'), ('mean_word_length_characters', 'Infinity'),
            ('mean_word_length_characters', '-Infinity'), ('mean_word_length_characters', '1e999'),
            ('mean_word_length_characters', '"1.25"'), ('words', 'null'),
        ):
            raw = '{"benchmark_id":"test","expected":{"' + key + '":' + token + '}}'
            with self.subTest(key=key, token=token), patch('scriptorium.benchmark.analyze_deterministic_metrics') as analyze:
                with self.assertRaises(ValueError):
                    build_comparison(raw, b'A', scriptorium_revision='synthetic')
                analyze.assert_not_called()

    def test_valid_counts_and_decimal_lexemes_are_preserved(self):
        raw = ('{"benchmark_id":"test","reference":{},"expected":'
               '{"characters":1,"words":1,"mean_word_length_characters":1.0000}}')
        result = build_comparison(raw, b'A', scriptorium_revision='synthetic',
                                  edition_match='exact', edition_label='Synthetic',
                                  source_reference='https://example.invalid/synthetic',
                                  legal_basis='Original synthetic fixture')
        self.assertEqual(result['metrics']['fantlab.general.characters']['comparison']['result'], 'pass')
        row = result['metrics']['fantlab.general.mean_word_length_chars']
        self.assertEqual(row['expected']['display_text'], '1.0000')
        self.assertEqual(row['comparison']['result'], 'unresolved')


if __name__ == '__main__':
    unittest.main()
