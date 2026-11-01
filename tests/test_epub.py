"""Original, synthetic EPUB fixtures: reading order and fail-closed archive semantics."""
from __future__ import annotations

from contextlib import redirect_stderr
from hashlib import sha256
from io import BytesIO, StringIO
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

from scriptorium import epub

CONTAINER = b'''<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="OPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'''
OPF = b'''<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid"><manifest><item id="a" href="chapter-1.xhtml" media-type="application/xhtml+xml"/><item id="b" href="chapter-2.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="a"/><itemref idref="b"/></spine></package>'''
CH1 = '''<html xmlns="http://www.w3.org/1999/xhtml"><head><script>EXCLUDE PRIVATE SCRIPT</script></head><body><h1>Привет, мир!</h1><p>Первый <em>текст</em>.</p><script>EXCLUDE SCRIPT</script></body></html>'''.encode()
CH2 = '''<html xmlns="http://www.w3.org/1999/xhtml"><body><p>Вторая глава.</p><p>Последняя строка.</p></body></html>'''.encode()


def book(*, opf=OPF, chapter1=CH1, chapter2=CH2, extras=(), missing=()):
    files = [("mimetype", b"application/epub+zip", ZIP_STORED),
             ("META-INF/container.xml", CONTAINER, ZIP_DEFLATED),
             ("OPS/package.opf", opf, ZIP_DEFLATED),
             ("OPS/chapter-2.xhtml", chapter2, ZIP_DEFLATED),
             ("OPS/chapter-1.xhtml", chapter1, ZIP_DEFLATED), *extras]
    data = BytesIO()
    with ZipFile(data, "w") as archive:
        for path, content, compression in files:
            if path not in missing:
                archive.writestr(path, content, compress_type=compression)
    return data.getvalue()


class EpubIngestionTests(unittest.TestCase):
    def test_original_unicode_xhtml_spine_order_and_identity(self):
        archive = book()
        text, receipt = epub.extract_epub(archive)
        self.assertIn("Привет, мир!", text.decode())
        self.assertIn("Первый текст.", text.decode())
        self.assertLess(text.index("Первый".encode()), text.index("Вторая".encode()))
        self.assertNotIn(b"EXCLUDE", text)
        self.assertEqual(receipt["archive_sha256"], sha256(archive).hexdigest())
        self.assertEqual(receipt["extracted_body_sha256"], sha256(text).hexdigest())
        self.assertEqual(receipt["spine_documents"], 2)
        self.assertFalse(receipt["source_text_embedded"])
        self.assertEqual(epub.extract_epub(archive), (text, receipt))

    def test_archive_variation_preserves_body_identity(self):
        original = book()
        modified = book(extras=[("OPS/unreferenced.jpg", b"FAKE IMAGE", ZIP_STORED)])
        a, ar = epub.extract_epub(original)
        b, br = epub.extract_epub(modified)
        self.assertEqual(a, b)
        self.assertNotEqual(ar["archive_sha256"], br["archive_sha256"])
        self.assertEqual(ar["extracted_body_sha256"], br["extracted_body_sha256"])

    def test_missing_spine_and_invalid_container_fail(self):
        for archive in (book(missing={"OPS/chapter-1.xhtml"}),
                        book(opf=OPF.replace(b'idref="a"', b'idref="gone"')),
                        book(opf=OPF.replace(b"<spine>", b"<foo>")),
                        book(missing={"META-INF/container.xml"}),
                        book(chapter1=b"<invalid"),
                        book(chapter1=b"<!DOCTYPE html><html />"),
                        book(chapter1='<!DOCTYPE html><html />'.encode("utf-16")),
                        book(chapter1=CH1.replace(b"<body>", b"<nothing>")),
                        b"not a zip"):
            with self.subTest(archive=sha256(archive).hexdigest()[:12]):
                with self.assertRaises(epub.EpubError):
                    epub.extract_epub(archive)

    def test_malicious_paths_ambiguity_and_limits_fail(self):
        for archive in (
            book(extras=[("../outside.xhtml", b"BAD", ZIP_STORED)]),
            book(extras=[("OPS/chapter-1.xhtml", b"DUPLICATE", ZIP_STORED)]),
            book(extras=[("OPS/chapter-1.xhtml/", b"ALIAS", ZIP_STORED)]),
            book(extras=[("OPS/evil\\name", b"BAD", ZIP_STORED)]),
            book(extras=[("META-INF/encryption.xml", b"<encryption/>", ZIP_STORED)]),
            book(extras=[("OPS/really-compressible.xhtml", b"a" * 100_000, ZIP_DEFLATED)]),
            book(opf=OPF.replace(b"chapter-1.xhtml", b"../chapter-1.xhtml")),
            book(opf=OPF.replace(b"chapter-1.xhtml", b"https://bad.site/chapter.xhtml")),
        ):
            with self.subTest(archive=sha256(archive).hexdigest()[:12]):
                with self.assertRaises(epub.EpubError):
                    epub.extract_epub(archive)
        old = epub.MAX_ARCHIVE_BYTES
        try:
            epub.MAX_ARCHIVE_BYTES = 12
            with self.assertRaises(epub.EpubError):
                epub.extract_epub(book())
        finally:
            epub.MAX_ARCHIVE_BYTES = old

    def test_dual_output_preflight_blocks_partial_results_from_known_collisions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "book.epub"
            source.write_bytes(book())
            report = root / "report.json"
            provenance = root / "identity.json"
            provenance.write_text("existing receipt", encoding="utf-8")
            args = ["--output", str(report), "--provenance-output", str(provenance)]
            with redirect_stderr(StringIO()) as err:
                with self.assertRaises(SystemExit):
                    epub.main([str(source), *args])
            self.assertIn("already exists", err.getvalue())
            self.assertNotIn(str(provenance), err.getvalue())
            self.assertFalse(report.exists())
            self.assertEqual(provenance.read_text(encoding="utf-8"), "existing receipt")

            provenance.unlink()
            (root / "subdir").mkdir()
            alias = root / "subdir" / ".." / "report.json"
            with redirect_stderr(StringIO()) as err:
                with self.assertRaises(SystemExit):
                    epub.main([str(source), "--output", str(report),
                               "--provenance-output", str(alias)])
            self.assertIn("must differ", err.getvalue())
            self.assertFalse(report.exists())

            # A dangling symlink is occupied, despite Path.exists() == False.
            provenance.symlink_to(root / "missing-target.json")
            with redirect_stderr(StringIO()) as err:
                with self.assertRaises(SystemExit):
                    epub.main([str(source), *args])
            self.assertIn("already exists", err.getvalue())
            self.assertFalse(report.exists())
            self.assertTrue(provenance.is_symlink())

    def test_real_reader_cli_private_json_html_provenance_and_no_clobber(self):
        from scriptorium import cli
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "my.epub").write_bytes(book())
            report = root / "report.json"
            receipt = root / "source.json"
            self.assertEqual(cli.main(["epub", str(root / "my.epub"), "--output", str(report),
                                       "--provenance-output", str(receipt)]), 0)
            analysis = json.loads(report.read_text(encoding="utf-8"))
            provenance = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(analysis["schema_version"], "scriptorium-local-analysis-v1")
            self.assertEqual(len(analysis["metrics"]), 29)
            self.assertEqual(provenance["extracted_body_sha256"], analysis["source"]["raw_sha256"])
            self.assertEqual(provenance["normalized_sha256"], analysis["source"]["normalized_sha256"])
            self.assertNotIn("Первый текст", report.read_text(encoding="utf-8"))
            self.assertNotIn("Первый текст", receipt.read_text(encoding="utf-8"))
            with self.assertRaises(SystemExit):
                cli.main(["epub", str(root / "my.epub"), "--output", str(report)])
            self.assertEqual(json.loads(report.read_text(encoding="utf-8")), analysis)
            self.assertEqual(cli.main(["epub", str(root / "my.epub"), "--format", "html",
                                       "--output", str(root / "report.html")]), 0)
            self.assertEqual(cli.main(["epub", str(root / "my.epub"), "--format", "csv",
                                       "--output", str(root / "report.csv")]), 0)
            self.assertIn("At a glance", (root / "report.html").read_text(encoding="utf-8"))
            self.assertIn("metric_id", (root / "report.csv").read_text(encoding="utf-8"))


    def test_markdown_epub_matches_canonical_renderer_and_preserves_privacy(self):
        from scriptorium import cli
        from scriptorium.analyze import build_local_analysis, render_markdown
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive = book()
            epub_file = root / "private.epub"
            epub_file.write_bytes(archive)
            report = root / "analysis.md"
            receipt = root / "source-identity.json"
            title = "Private | [Draft] <script>"
            args = ["epub", str(epub_file), "--format", "markdown", "--title", title,
                    "--output", str(report), "--provenance-output", str(receipt)]
            self.assertEqual(cli.main(args), 0)
            body, witness = epub.extract_epub(archive)
            expected = render_markdown(build_local_analysis(body), title=title)
            actual = report.read_text(encoding="utf-8")
            self.assertEqual(actual, expected)
            self.assertIn("## Dialogue", actual)
            self.assertIn("NOT** verified FantLab parity", actual)
            self.assertIn(r"Private \| \[Draft\] &lt;script&gt;", actual)
            self.assertNotIn("<script>", actual)
            self.assertNotIn("Привет, мир!", actual)
            self.assertNotIn("Первый текст", actual)
            provenance = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(provenance["archive_sha256"], witness["archive_sha256"])
            self.assertEqual(provenance["extracted_body_sha256"], witness["extracted_body_sha256"])
            self.assertEqual(provenance["normalized_sha256"], build_local_analysis(body)["source"]["normalized_sha256"])
            with redirect_stderr(StringIO()) as error:
                with self.assertRaises(SystemExit):
                    cli.main(args)
            self.assertIn("already exists", error.getvalue())
            self.assertNotIn(str(report), error.getvalue())
            self.assertEqual(report.read_text(encoding="utf-8"), actual)


if __name__ == "__main__":
    unittest.main()
