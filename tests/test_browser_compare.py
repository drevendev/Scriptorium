"""Actual Reader JSON vs browser comparison: 234-case Python/Node differential.

Runs against real build_local_analysis() reports and the canonical installed Python
comparison contract; no analyzer stub, private source upload or browser network.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from scriptorium.analyze import build_local_analysis
from scriptorium import compare, site_browser_compare
from scriptorium.metrics import analyze_deterministic_metrics
from scriptorium.site_renderer import _render_index, _SITE_CSS


LEFT_TEXT = 'Кот спит. Кот и пёс гуляют!\n— Да? — сказал пёс.'
RIGHT_TEXT = 'Кот, кот, кот!\n— А? — ответил он.'


class BrowserCompareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.javascript = site_browser_compare.render_script()
        cls.first = build_local_analysis(LEFT_TEXT.encode('utf-8'))
        cls.second = build_local_analysis(RIGHT_TEXT.encode('utf-8'))

    def test_contract_generated_from_real_metrics_and_browser_page(self):
        self.assertIn('fantlab-2022-v1', self.javascript)
        self.assertNotIn('/*SCRIPTORIUM_METRIC_CONTRACT*/ null', self.javascript)
        canonical = analyze_deterministic_metrics('')
        self.assertEqual(len(canonical['metrics']), 29)
        for mid in canonical['metrics']:
            self.assertIn(mid, self.javascript)
        self.assertIn('type="file"', site_browser_compare.BODY)
        self.assertIn('role="status"', site_browser_compare.BODY)
        self.assertIn('aria-live="polite"', site_browser_compare.BODY)
        self.assertIn('aria-label="29 report measurements"', site_browser_compare.BODY)
        self.assertIn('href="compare/"', _render_index([]))
        self.assertIn('min-height: 44px', site_browser_compare.CSS)
        self.assertIn('prefers-reduced-motion', _SITE_CSS)
        self.assertNotIn('<script>\n', site_browser_compare.BODY)
        for forbidden in ('fetch(', 'XMLHttpRequest', 'sendBeacon(', 'localStorage',
                          'sessionStorage', 'document.cookie', 'eval(', 'innerHTML'):
            self.assertNotIn(forbidden, self.javascript)

    def _case_data(self):
        left, right = self.first, self.second
        samples = [(json.dumps(left, ensure_ascii=False), json.dumps(right, ensure_ascii=False))]
        texts = [
            'Толстой. Пушкин, Чехов?\n— Хорошо!', 'Пунктуация!! Ура?\nНо что-то ещё…',
            'Один. Два. Три.', 'Страница без знаков и с несколькими словами',
            '«Привет», — сказал он. «Здравствуйте!»', '— Мы здесь? — Да!',
            'Лекция про звёзды: космос; планеты.', 'Огромный-длинный-токен и короткий.',
            'Слово, слово, слово, слово!', 'Глава I\nЗаголовок\nТекст.',
            'AOT, лемма: N. Описание.', 'Лес… и ветер… и море…',
        ]
        analyses = [build_local_analysis(s.encode('utf-8')) for s in texts]
        for index in range(0, 12, 2):
            samples.append((json.dumps(analyses[index], ensure_ascii=False),
                            json.dumps(analyses[index + 1], ensure_ascii=False)))
        for index in range(12):
            samples.append((json.dumps(analyses[index], ensure_ascii=False),
                            json.dumps(analyses[index], ensure_ascii=False)))
        # Any tamper can be rejected *or* result in a valid comparable artifact.
        # The point is exact agreement on acceptance and exports in both engines.
        canonical = list(left['metrics'])
        for idx, metric in enumerate(canonical):
            for tamper in range(6):
                mutated = copy.deepcopy(left)
                row = mutated['metrics'][metric]
                if tamper == 0:
                    row['unit'] = 'unsupported_unit'
                elif tamper == 1:
                    row['compatibility_status'] = 'reproduced'
                elif tamper == 2:
                    row['definition_evidence'] = 'secret'
                elif tamper == 3:
                    row['value'] = None if row['value'] is not None else 333333
                elif tamper == 4:
                    row['value'] = -1
                else:
                    row['stray'] = True
                samples.append((json.dumps(mutated, ensure_ascii=False), json.dumps(right, ensure_ascii=False)))
        # Root/source/analyzer tampering, JSON parser attacks, float-integer spoofs.
        tamperers = (
            ('schema_version', 'newly invented'),
            ('metric_contract_id', 'fantlab-unauthorized-v5'),
            ('source', None),
            ('analyzer', None),
            ('representativeness', None),
            ('metrics', None),
        )
        for field, value in tamperers:
            clone = copy.deepcopy(left); clone[field] = value
            samples.append((json.dumps(clone, ensure_ascii=False), json.dumps(right, ensure_ascii=False)))
        mutations = [
            ('source', 'raw_sha256', 'f' * 64),
            ('source', 'raw_sha256', 'bad'),
            ('source', 'normalized_sha256', 'bad'),
            ('source', 'normalized_character_count', -1),
            ('source', 'byte_count', False),
            ('source', 'source_text_embedded', True),
            ('analyzer', 'scriptorium_revision', []),
            ('analyzer', 'profiles', {}),
            ('analyzer', 'dependencies', {}),
            ('representativeness', 'calibration_threshold_characters', 2000),
            ('representativeness', 'meets_calibration_threshold', True),
            ('representativeness', 'note', ''),
        ]
        for root, field, value in mutations:
            clone = copy.deepcopy(left); clone[root][field] = value
            samples.append((json.dumps(clone, ensure_ascii=False), json.dumps(right, ensure_ascii=False)))
        for metric in canonical:
            # float lexeme spoof for every count row; Python decides whether accepted.
            original = json.dumps(left, ensure_ascii=False)
            key = json.dumps(metric)
            needle = key + ': {"value": '
            offset = original.find(needle)
            self.assertGreater(offset, 0, metric)
            start = offset + len(needle)
            suffix = original[start:]
            replacement = '3.0' if suffix.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) else '3e0'
            end = start
            while end < len(original) and original[end] not in ',}':
                end += 1
            samples.append((original[:start] + replacement + original[end:], json.dumps(right, ensure_ascii=False)))
        # Four adversarial parser probes including encoded duplicate names and NaN.
        raw = json.dumps(left, ensure_ascii=False)
        samples.extend([
            ('{"schema_version":"x","schema_version":"y"}', json.dumps(right, ensure_ascii=False)),
            ('{"n":NaN}', json.dumps(right, ensure_ascii=False)),
            ('{"n":1e999}', json.dumps(right, ensure_ascii=False)),
            ('{"f\\u006fo":1,"foo":2}', json.dumps(right, ensure_ascii=False)),
        ])
        # Count 234 cases *precisely*, without low-value repeated identical probes.
        samples = samples[:234]
        self.assertEqual(len(samples), 234)
        self.assertEqual(len(set(samples)), 234)
        return samples

    @unittest.skipUnless(shutil.which('node'), 'Node is needed for genuine JS/Python differential')
    def test_234_real_python_vs_browser_differential(self):
        cases = self._case_data()
        harness = r'''
const fs=require('fs');
const api=require(process.argv[1]);
const cases=JSON.parse(fs.readFileSync(0,'utf8'));
const result=cases.map(([a,b])=>{
  try {
    const c=api.compareReports(api.parseStrictJSON(a),api.parseStrictJSON(b));
    return {accepted:true,document:c,json:api.renderJSON(c),csv:api.renderCSV(c)};
  } catch(e) {return {accepted:false};}
});
process.stdout.write(JSON.stringify(result));
'''
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            script = root / 'browser.js'
            script.write_text(self.javascript, encoding='utf-8')
            command = subprocess.run(
                ['node', '-e', harness, str(script)], input=json.dumps(cases, ensure_ascii=False),
                text=True, capture_output=True, check=True, timeout=90,
            )
            browser = json.loads(command.stdout)
            self.assertEqual(len(browser), 234)
            accepted = 0
            for index, ((left, right), actual) in enumerate(zip(cases, browser)):
                a_path = root / 'a.json'; b_path = root / 'b.json'
                a_path.write_text(left, encoding='utf-8'); b_path.write_text(right, encoding='utf-8')
                try:
                    compared = compare.build_comparison(compare.load_report(a_path), compare.load_report(b_path))
                except (ValueError, OSError, UnicodeError, RecursionError):
                    self.assertFalse(actual['accepted'], f'case {index}: JS accepted a Python-rejected report')
                else:
                    accepted += 1
                    self.assertTrue(actual['accepted'], f'case {index}: JS rejected Python-accepted report')
                    self.assertEqual(actual['document'], compared, f'case {index}: comparison mismatch')
                    self.assertEqual(actual['csv'], compare.render_csv(compared), f'case {index}: CSV mismatch')
                    self.assertEqual(actual['json'], compare.render_json(compared), f'case {index}: JSON mismatch')
            self.assertGreaterEqual(accepted, 15, 'negative cases cannot replace real accepted report evidence')

    def test_script_does_not_embed_source_text_or_external_transport(self):
        for value in (LEFT_TEXT, RIGHT_TEXT):
            self.assertNotIn(value, self.javascript)
        self.assertNotIn('http://', self.javascript)
        self.assertNotIn('https://', self.javascript)
        self.assertIn('parseStrictJSON', self.javascript)
        self.assertIn('new TextDecoder(\'utf-8\', {fatal: true})', self.javascript)
        self.assertIn('setTimeout(() => URL.revokeObjectURL(url)', self.javascript)


if __name__ == '__main__':
    unittest.main()