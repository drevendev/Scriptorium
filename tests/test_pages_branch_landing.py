"""The GitHub Pages master/root entrypoint must display only real retained diagnostics.

The existing Python Reader builds its complete site into build/site. The GitHub-managed
branch publisher instead sees the repository root, so the root landing must carry a
safe, source-free data snapshot and working local CSS/JS. Any source drift is a test
failure, not a reason to fabricate or silently refresh parity evidence.
"""
from __future__ import annotations

from hashlib import sha1
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "index.html"
SNAPSHOT = ROOT / "assets/evidence-snapshot.json"
CSS = ROOT / "assets/pages-reader.css"
JS = ROOT / "assets/pages-reader.js"
SOURCE = (
    ("anna", "benchmarks/fantlab/work270306-wikisource-diagnostic.json", 28, 23),
    ("waves", "corpus/candidates/diagnostics/grin-running-on-waves-ru.json", 27, 23),
    ("silver", "corpus/candidates/diagnostics/bely-silver-dove-ru.json", 29, 24),
    ("karamazov", "corpus/candidates/diagnostics/dostoevsky-brothers-karamazov-ru.json", 29, 24),
)


class Links(HTMLParser):
    def __init__(self, html: str):
        super().__init__()
        self.links = []
        self.scripts = []
        self.headers = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        meta = dict(attrs)
        if tag == "a":
            self.links.append(meta.get("href"))
        if tag == "script":
            self.scripts.append(meta)
        if tag == "h1":
            self.headers.append(meta)


class BranchPagesLandingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = SITE.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")
        cls.js = JS.read_text(encoding="utf-8")
        cls.data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))

    def test_branch_root_has_real_static_entrypoint_and_navigation(self):
        html = self.html
        links = Links(html)
        self.assertEqual(len(links.headers), 1)
        self.assertIn('href="./assets/pages-reader.css"', html)
        self.assertIn('src="./assets/pages-reader.js"', html)
        self.assertIn('id="chart-series"', html)
        self.assertIn('id="measurement-rows"', html)
        self.assertIn('id="table-status" aria-live="polite"', html)
        self.assertIn('type="search"', html)
        self.assertIn('tabindex="0" role="region"', html)
        self.assertIn('<noscript>', html)
        self.assertIn('M2: 0 / 5', html)
        for anchor in ('#books', '#measurements', '#method'):
            self.assertIn(anchor, links.links)
        for script in links.scripts:
            self.assertEqual(script.get('src'), './assets/pages-reader.js')
            self.assertNotIn('integrity', script)  # same-origin checked-in source
        self.assertNotIn('https://fonts.', html)
        self.assertNotIn('http://', html)
        self.assertNotIn('upload a manuscript here', html.lower())

    def test_numeric_json_is_exact_canonical_source_free_evidence(self):
        data = self.data
        self.assertEqual(
            {k:data[k] for k in ('schema','scientific_claim','fantlab_input_identity')},
            {'schema':'scriptorium-branch-pages-derived-v1',
             'scientific_claim':'DIAGNOSTIC_ONLY',
             'fantlab_input_identity':'UNKNOWN'},
        )
        self.assertEqual(data['produced_from'],
                         'master:f8479c7fbe540e279b6fd66e44fba78df5d2dfd0')
        self.assertEqual(data['counts'],{
            'work_count':4,'measured_works':4,'expected_corpus_works':5,
            'metrics_total':113,'numeric_total':94,'unavailable_total':19,
            'm2_source_matched':0,
        })
        self.assertEqual([b['key'] for b in data['books']], [x[0] for x in SOURCE])
        for book, (key, path, count, measured) in zip(data['books'], SOURCE):
            with self.subTest(key=key):
                raw = (ROOT/path).read_bytes()
                original = json.loads(raw)
                github_blob = sha1(
                    b'blob '+str(len(raw)).encode('ascii')+b'\0'+raw
                ).hexdigest()
                self.assertEqual(book['blob_sha1'], github_blob)
                self.assertEqual(book['candidate_id'], original['candidate_id'])
                self.assertEqual(book['key'], key)
                self.assertEqual(book['evidence_url'],
                                 'https://github.com/drevendev/Scriptorium/blob/master/'+path)
                self.assertTrue(book['fantlab_url'].startswith('https://fantlab.ru/work'))
                self.assertEqual(len(book['metrics']), count)
                self.assertEqual(book['measured'], measured)
                self.assertEqual(book['unavailable'], count-measured)
                self.assertEqual(len({r['id'] for r in book['metrics']}), count)
                if key == 'anna':
                    self.assertIs(original['epistemic_status']['m2_parity_admissible'],False)
                    self.assertIs(original['evidence']['source_text_committed'],False)
                    self.assertEqual(book['source_sha256'],original['evidence']['raw_sha256'])
                    raw_rows = dict(original['metrics'])
                else:
                    self.assertIs(original['gates']['m2_parity_admissible'],False)
                    self.assertIs(original['source_text_committed'],False)
                    self.assertEqual(book['source_sha256'],original['body_identity']['raw_sha256'])
                    rows = original['metric_rows'] if 'metric_rows' in original else original['metrics']
                    raw_rows = {row['metric_id']:row for row in rows}
                for row in book['metrics']:
                    item = raw_rows[row['id']]
                    actual = item.get('scriptorium_raw_value',item.get('actual'))
                    reference = item.get('fantlab_display_value',
                                 item.get('fantlab_display',item.get('expected')))
                    expected = None if reference is None else float(reference)
                    if row['kind'] == 'extension':
                        self.assertTrue(row['id'].startswith('scriptorium.'))
                        self.assertIsNone(row['reference'])
                    elif expected is not None:
                        self.assertEqual(float(row['reference']),expected)
                    else:
                        self.assertIsNone(row['reference'])
                    self.assertEqual(row['actual'],actual)
                    self.assertEqual(row['status']=='measured',actual is not None)

    def test_existing_pages_build_and_usable_private_fallback(self):
        self.assertIn('type="search"', self.html)
        self.assertIn('github.com/drevendev/Scriptorium',self.html)
        self.assertIn('scriptorium analyze manuscript.txt --format html',self.html)
        self.assertIn('https://github.com/drevendev/Scriptorium/blob/master/docs/READER_PREVIEW.md',self.html)
        self.assertIn('No uploaded manuscripts',self.html)
        self.assertIn('an offline Python library and CLI', self.html)
        workflow=(ROOT/'.github/workflows/pages.yml').read_text(encoding='utf-8')
        for path in ('index.html','assets/**'):
            self.assertGreaterEqual(workflow.count('"'+path+'"'),2)
        self.assertIn("vars.SCRIPTORIUM_PAGES_DEPLOY_ENABLED == 'true'",workflow)
        self.assertIn('master',workflow)

    def test_keyboard_motion_print_and_network_privacy(self):
        self.assertIn('.skip-link:focus',self.css)
        self.assertIn(':focus-visible',self.css)
        self.assertIn('min-height:44px',self.css)
        self.assertIn('@media(max-width:480px)',self.css)
        self.assertIn('@media(prefers-reduced-motion:reduce)',self.css)
        self.assertIn('@media print',self.css)
        self.assertIn('@media(forced-colors:active)',self.css)
        self.assertIn('credentials:"omit"',self.js)
        self.assertIn('assets/evidence-snapshot.json',self.js)
        self.assertIn('textContent',self.js)
        self.assertIn('replaceChildren',self.js)
        self.assertNotIn('innerHTML',self.js)
        for forbidden in ('localStorage','sendBeacon','XMLHttpRequest','https://fonts.',
                          'eval(', 'document.cookie'):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden,self.js)

if __name__=='__main__':
    unittest.main()
