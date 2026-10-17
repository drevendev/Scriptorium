"""Regression tests for the source-free gallery preview."""
from __future__ import annotations
import csv
from io import StringIO
import json
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from scriptorium import full_work_gallery as gallery

class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = Path(__file__).resolve().parents[1]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for spec in gallery.SOURCES:
            filename = spec[0] + '.json'
            p = Path('corpus/candidates/diagnostics') / filename
            (self.root / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.original / p, self.root / p)

    def _mutate(self, index, change):
        spec = list(gallery.SOURCES[index])
        p = self.root / 'corpus/candidates/diagnostics' / (spec[0]+'.json')
        doc = json.loads(p.read_text())
        change(doc)
        raw = (json.dumps(doc, ensure_ascii=False, indent=2) + '\n').encode()
        p.write_bytes(raw)
        blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        all_specs = list(gallery.SOURCES)
        spec[1] = blob
        all_specs[index] = tuple(spec)
        return tuple(all_specs)

    def test_verified_sizes(self):
        a,b = gallery.load_gallery(self.root)
        self.assertEqual((a['body'],b['body']), (363819,1095467))
        self.assertEqual((a['values']['fantlab.dialogue.share_percent'],b['values']['fantlab.dialogue.share_percent']), (35.88986183443132,32.4738652575157))

    def test_html_and_csv(self):
        records = gallery.load_gallery(self.root)
        page = gallery.render_html(records)
        self.assertEqual(page.count("<tr><th scope='row'>"),10)
        self.assertEqual(page.count("<li><h3>"),7)
        self.assertIn('M2 0/5',page)
        self.assertIn('prefers-reduced-motion',page)
        self.assertIn('tabindex=\'0\'',page)
        self.assertNotIn('<script',page)
        rows = list(csv.DictReader(StringIO(gallery.render_csv(records))))
        self.assertEqual(len(rows),20)
        self.assertEqual(rows[0]['value'],'363819')

    def test_deterministic(self):
        self.assertEqual(gallery.render_html(gallery.load_gallery(self.root)),gallery.render_html(gallery.load_gallery(self.root)))
        self.assertEqual(gallery.render_csv(gallery.load_gallery(self.root)),gallery.render_csv(gallery.load_gallery(self.root)))

    def test_raw_byte_mutation_fails(self):
        p = self.root / 'corpus/candidates/diagnostics/grin-running-on-waves-ru.json'
        p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaisesRegex(gallery.GalleryError,'checksum'):
            gallery.load_gallery(self.root)

    def test_symlink_no_follow(self):
        p = self.root / 'corpus/candidates/diagnostics/grin-running-on-waves-ru.json'
        p.unlink()
        outside = self.root / 'secret.txt'
        outside.write_text('secret')
        p.symlink_to(outside)
        with self.assertRaises(gallery.GalleryError):
            gallery.load_gallery(self.root)

    def test_fifo_no_hang(self):
        p = self.root / 'corpus/candidates/diagnostics/grin-running-on-waves-ru.json'
        p.unlink()
        if not hasattr(os,'mkfifo'):
            self.skipTest('no mkfifo')
        os.mkfifo(p)
        with self.assertRaises(gallery.GalleryError):
            gallery.load_gallery(self.root)

    def test_status_promotion_rejected(self):
        modified = self._mutate(0,lambda d:d['gates'].update(m2_weight=1))
        with patch.object(gallery,'SOURCES',modified),self.assertRaisesRegex(gallery.GalleryError,'scientific'):
            gallery.load_gallery(self.root)

    def test_translation_rejected(self):
        modified = self._mutate(1,lambda d:d.update(translation_identity='different translator'))
        with patch.object(gallery,'SOURCES',modified),self.assertRaisesRegex(gallery.GalleryError,'translation'):
            gallery.load_gallery(self.root)

    def test_missing_metric_rejected(self):
        modified = self._mutate(1,lambda d:d['metrics'].pop())
        with patch.object(gallery,'SOURCES',modified),self.assertRaisesRegex(gallery.GalleryError,'shared measurement'):
            gallery.load_gallery(self.root)

    def test_duplicate_metric_rejected(self):
        modified = self._mutate(1,lambda d:d['metrics'].append(d['metrics'][0]))
        with patch.object(gallery,'SOURCES',modified),self.assertRaisesRegex(gallery.GalleryError,'duplicate metric'):
            gallery.load_gallery(self.root)

    def test_nonfinite_rejected(self):
        modified = self._mutate(1,lambda d:d['metrics'][0].update(value=float('inf')))
        with patch.object(gallery,'SOURCES',modified),self.assertRaises(gallery.GalleryError):
            gallery.load_gallery(self.root)

if __name__ == '__main__':
    unittest.main()
