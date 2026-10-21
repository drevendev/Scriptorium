"""Private-path leak regression for the installable Workbench single-text CLI."""
from __future__ import annotations
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium import analyze


class LocalCliErrorPrivacyTests(unittest.TestCase):
    def rejected(self, args, forbidden):
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors), self.assertRaises(SystemExit) as caught:
            analyze.main(args)
        self.assertEqual(caught.exception.code, 2)
        message = errors.getvalue()
        for phrase in forbidden:
            self.assertNotIn(phrase, message)
        return message

    def test_existing_output_preserved_and_paths_private(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manuscript = root / 'PRIVATE-manuscript.txt'
            report = root / 'PRIVATE-report.html'
            manuscript.write_text('Кот идёт. Пёс спит.', encoding='utf-8')
            report.write_bytes(b'OLD REPORT')
            error = self.rejected([str(manuscript), '--format', 'html', '--output', str(report)],
                                  [directory, manuscript.name, report.name])
            self.assertIn('already exists', error)
            self.assertEqual(report.read_bytes(), b'OLD REPORT')

    def test_missing_manuscript_is_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            manuscript = Path(directory) / 'PRIVATE-secret-work.txt'
            error = self.rejected([str(manuscript)], [directory, manuscript.name])
            self.assertIn('regular file', error)

    def test_private_invalid_utf8_manuscript(self):
        with tempfile.TemporaryDirectory() as directory:
            manuscript = Path(directory) / 'PRIVATE-secret-work.txt'
            manuscript.write_bytes(b'\xff')
            error = self.rejected([str(manuscript)], [directory, manuscript.name])
            self.assertIn('manuscript must be UTF-8', error)

    def test_private_dictionary_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manuscript = root / 'PRIVATE-secret-work.txt'
            dictionary = root / 'PRIVATE-words.txt'
            manuscript.write_text('Кот идёт.', encoding='utf-8')
            dictionary.write_bytes(b'\xff')
            error = self.rejected([str(manuscript), '--dictionary', str(dictionary),
                                   '--dictionary-profile', 'local-v1'],
                                  [directory, manuscript.name, dictionary.name])
            self.assertIn('dictionary must be UTF-8', error)

    def test_dictionary_and_manuscript_regular_file_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manuscript = root / 'PRIVATE-manuscript.txt'
            dictionary = root / 'PRIVATE-words.txt'
            manuscript.write_text('Кот идёт.', encoding='utf-8')
            dictionary.mkdir()
            error = self.rejected([str(manuscript), '--dictionary', str(dictionary),
                                   '--dictionary-profile', 'local-v1'],
                                  [directory, manuscript.name, dictionary.name])
            self.assertIn('regular file', error)

    def test_engine_exception_does_not_leak_original_text(self):
        with tempfile.TemporaryDirectory() as directory:
            manuscript = Path(directory) / 'PRIVATE-secret-work.txt'
            manuscript.write_text('Кот идёт.', encoding='utf-8')
            with patch.object(analyze, 'analyze_deterministic_metrics',
                              side_effect=ValueError('PRIVATE-ENGINE-AND-DICTIONARY')):
                error = self.rejected([str(manuscript)],
                                      [directory, manuscript.name, 'PRIVATE-ENGINE-AND-DICTIONARY'])
            self.assertIn('unable to analyze', error)

    def test_unexpected_write_error_does_not_leak_output_path(self):
        with tempfile.TemporaryDirectory() as directory:
            manuscript = Path(directory) / 'PRIVATE-secret-work.txt'
            report = Path(directory) / 'PRIVATE-report.json'
            manuscript.write_text('Кот идёт.', encoding='utf-8')
            with patch.object(analyze, '_write_new',
                              side_effect=OSError('PRIVATE-report.json: access denied')):
                error = self.rejected([str(manuscript), '--output', str(report)],
                                      [directory, manuscript.name, report.name, 'access denied'])
            self.assertIn('unable to analyze', error)
            self.assertFalse(report.exists())

    def test_successful_json_and_html_still_work(self):
        with tempfile.TemporaryDirectory() as directory:
            manuscript = Path(directory) / 'work.txt'
            manuscript.write_text('Кот идёт. Пёс спит.', encoding='utf-8')
            for kind in ['json', 'html', 'csv']:
                report = Path(directory) / f'{kind}.txt'
                self.assertEqual(analyze.main([str(manuscript), '--format', kind,
                                               '--output', str(report)]), 0)
                self.assertTrue(report.stat().st_size > 0)


if __name__ == '__main__':
    unittest.main()
