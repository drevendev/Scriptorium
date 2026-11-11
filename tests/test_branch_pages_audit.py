"""Regression gates for branch Pages routes (not a claim of live verification)."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scriptorium.branch_pages_audit import ReaderLinkError, audit_site


ROOT = Path(__file__).resolve().parents[1]


class BranchPagesAuditTests(unittest.TestCase):
    def test_real_reader_links_assets_and_fragments_resolve(self):
        pages, links = audit_site(ROOT)
        self.assertEqual(pages, 5)
        self.assertGreaterEqual(links, 40)

    def _run(self, html, *, voice=None, files=()):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "index.html").write_text(html, encoding="utf-8")
            pages = ("index.html",)
            if voice is not None:
                (root / "voice").mkdir()
                (root / "voice" / "index.html").write_text(voice, encoding="utf-8")
                pages += ("voice/index.html",)
            for path in files:
                dest = root / path
                dest.parent.mkdir(exist_ok=True, parents=True)
                dest.write_text("data\n", encoding="utf-8")
            return audit_site(root, pages=pages, required=())

    def test_nested_voice_and_download_are_reachable(self):
        pages, references = self._run(
            '<html><main id="books"></main><a href="voice/">Voice</a></html>',
            voice='<a href="../#books">Books</a><a href="folds.csv">CSV</a>',
            files=("voice/folds.csv",),
        )
        self.assertEqual((pages, references), (2, 3))

    def test_missing_download_fails_instead_of_claiming_complete_site(self):
        with self.assertRaisesRegex(ReaderLinkError, "missing/empty"):
            self._run('<a href="voice/folds.csv">Download</a>')

    def test_local_fragment_typo_fails(self):
        with self.assertRaisesRegex(ReaderLinkError, "broken Reader fragment"):
            self._run('<main id="books"></main><a href="#book">Broken</a>')

    def test_encoded_parent_escape_fails(self):
        with self.assertRaisesRegex(ReaderLinkError, "escapes publication root"):
            self._run('<a href="%2e%2e/private.txt">Unsafe</a>')

    def test_duplicate_ids_fail(self):
        with self.assertRaisesRegex(ReaderLinkError, "duplicate fragment IDs"):
            self._run('<h2 id="books"></h2><h3 id="books"></h3>')

    def test_javascript_url_fails(self):
        with self.assertRaisesRegex(ReaderLinkError, "unsafe Reader URL"):
            self._run('<a href="javascript:alert(1)">Unsafe</a>')


if __name__ == "__main__":
    unittest.main()
