"""Imported-mean regressions using the actual canonical Reader, without stubs."""
from __future__ import annotations
import copy
from pathlib import Path
import tempfile
import json
import unittest
from scriptorium import compare
from scriptorium.analyze import build_local_analysis

class MeanIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.left = build_local_analysis('Вечер. — Мы читаем книгу, — сказал он.\nТихо светит лампа.'.encode())
        self.right = build_local_analysis('Утро пришло. Открой окно!'.encode())

    def test_impossible_legacy_fixture_is_rejected(self):
        forged = copy.deepcopy(self.right)
        forged['metrics']['fantlab.general.mean_word_length_chars']['value'] = 100000
        with self.assertRaises(compare.CompareError):
            compare.validate_report(forged)

    def test_real_analyzer_reports_pass(self):
        compare.validate_report(self.left)
        compare.validate_report(self.right)
        self.assertEqual(len(compare.build_comparison(self.left, self.right)['metrics']), 29)

    def test_positive_word_mean_must_be_available(self):
        self.assertGreater(self.left['metrics']['fantlab.general.words']['value'], 0)
        self.left['metrics']['fantlab.general.mean_word_length_chars']['value'] = None
        with self.assertRaises(compare.CompareError):
            compare.validate_report(self.left)

    def test_impossible_word_length_is_rejected(self):
        self.left['metrics']['fantlab.general.mean_word_length_chars']['value'] = 100000
        with self.assertRaises(compare.CompareError):
            compare.validate_report(self.left)

    def test_nonempty_mean_cannot_be_zero(self):
        for key in ('fantlab.general.mean_word_length_chars', 'fantlab.general.mean_sentence_length_chars'):
            with self.subTest(key=key):
                bad = copy.deepcopy(self.left)
                bad['metrics'][key]['value'] = 0
                with self.assertRaises(compare.CompareError):
                    compare.validate_report(bad)

    def test_positive_sentence_mean_must_be_available(self):
        self.assertGreater(self.left['metrics']['scriptorium.general.sentences']['value'], 0)
        self.left['metrics']['fantlab.general.mean_sentence_length_chars']['value'] = None
        with self.assertRaises(compare.CompareError):
            compare.validate_report(self.left)

    def test_impossible_sentence_length_is_rejected(self):
        self.left['metrics']['fantlab.general.mean_sentence_length_chars']['value'] = 100000
        with self.assertRaises(compare.CompareError):
            compare.validate_report(self.left)

    def test_imported_json_rejects_forged_mean(self):
        self.left['metrics']['fantlab.general.mean_word_length_chars']['value'] = 100000
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'analysis.json'
            path.write_text(json.dumps(self.left, ensure_ascii=False), encoding='utf-8')
            with self.assertRaises(compare.CompareError):
                compare.load_report(path)

    def test_zero_denominator_means_undefined(self):
        empty = build_local_analysis(b'')
        compare.validate_report(empty)
        for name in ('fantlab.general.mean_word_length_chars', 'fantlab.general.mean_sentence_length_chars'):
            bad = copy.deepcopy(empty)
            bad['metrics'][name]['value'] = 0
            with self.assertRaises(compare.CompareError):
                compare.validate_report(bad)

if __name__ == '__main__':
    unittest.main()
