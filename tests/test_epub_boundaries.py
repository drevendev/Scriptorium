"""Original synthetic archives exercise the actual EPUB parser, without stubs."""
from hashlib import sha256
from io import BytesIO
import unittest
from unittest.mock import patch
from urllib.parse import quote
from xml.sax.saxutils import quoteattr
from zipfile import ZipFile, ZIP_STORED

from scriptorium import epub


def make_epub(*, href="chapter.xhtml", member="OPS/chapter.xhtml", body=None,
              extras=(), href_xml=None, version="3.0"):
    """Small deterministic original EPUB; href_xml permits XML character refs."""
    if body is None:
        body = '<p>Alpha <em>beta</em>.</p><p>Gamma delta.</p>'
    ref = quoteattr(href) if href_xml is None else '"' + href_xml + '"'
    package = (f'<package xmlns="http://www.idpf.org/2007/opf" version="{version}">'
               f'<manifest><item id="c" href={ref} media-type="application/xhtml+xml"/>'
               '</manifest><spine><itemref idref="c"/></spine></package>').encode()
    container = (b'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 b'<rootfiles><rootfile full-path="OPS/package.opf" '
                 b'media-type="application/oebps-package+xml"/></rootfiles></container>')
    chapter = ('<html xmlns="http://www.w3.org/1999/xhtml"><body>' + body +
               '</body></html>').encode()
    stream = BytesIO()
    with ZipFile(stream, "w", compression=ZIP_STORED) as archive:
        for name, content in [
            ("mimetype", b"application/epub+zip"),
            ("META-INF/container.xml", container),
            ("OPS/package.opf", package), (member, chapter), *extras,
        ]:
            archive.writestr(name, content)
    return stream.getvalue()


class EpubBoundaryTests(unittest.TestCase):
    def reject(self, href):
        with self.assertRaises(epub.EpubError) as failure:
            epub._resolved_member("OPS/package.opf", href)
        self.assertNotIn("PRIVATE", str(failure.exception))

    def test_raw_controls_and_spaces_rejected_before_urlsplit(self):
        for code in [*range(33), 127]:
            for href in (chr(code) + "PRIVATE.xhtml", "PRI" + chr(code) + "VATE.xhtml"):
                with self.subTest(code=code, href=repr(href)):
                    self.reject(href)

    def test_malformed_percent_triplets_rejected(self):
        for suffix in ("%", "%0", "%GG", "%2G", "%G2", "%%20", "%１２", "%é0"):
            with self.subTest(suffix=suffix):
                self.reject("PRIVATE" + suffix + ".xhtml")

    def test_valid_encoding_decoded_exactly_once(self):
        for href, expected in (
            ("chapter%20one.xhtml", "chapter one.xhtml"),
            ("%D0%B3%D0%BB%D0%B0%D0%B2%D0%B0.xhtml", "глава.xhtml"),
            ("%d0%b3.xhtml", "г.xhtml"),
            ("глава.xhtml", "глава.xhtml"),
            ("chapter%25.xhtml", "chapter%.xhtml"),
            ("chapter%25GG.xhtml", "chapter%GG.xhtml"),
            ("chapter%252f.xhtml", "chapter%2f.xhtml"),
            ("chapter%23%3F.xhtml", "chapter#?.xhtml"),
        ):
            with self.subTest(href=href):
                self.assertEqual(epub._resolved_member("OPS/package.opf", href), "OPS/" + expected)

    def test_empty_url_components_and_bad_authority_fail_controlled(self):
        for href in ("PRIVATE.xhtml?", "PRIVATE.xhtml#", "PRIVATE.xhtml?#",
                     "//[PRIVATE", "http://[PRIVATE", "//PRIVATE/x", "https://PRIVATE/x"):
            with self.subTest(href=href):
                self.reject(href)

    def test_existing_unsafe_and_invalid_utf8_references_stay_rejected(self):
        for href in ("../PRIVATE.xhtml", "%2e%2e/PRIVATE.xhtml", "/PRIVATE.xhtml",
                     "PRIVATE%00.xhtml", "PRIVATE%7F.xhtml", "PRIVATE%5c.xhtml",
                     "PRIVATE%FF.xhtml", "PRIVATE%C0%AF.xhtml", "PRIVATE%ED%A0%80.xhtml",
                     "PRIVATE%3A.xhtml", "e\u0301-PRIVATE.xhtml", "PRIVATE" * 100, ""):
            with self.subTest(href=href):
                self.reject(href)
        for href in (None, 12, b"PRIVATE.xhtml"):
            with self.subTest(href=href):
                self.reject(href)

    def test_xml_character_reference_cannot_silently_alias_a_chapter(self):
        for ref in ("chap&#9;ter.xhtml", "chap&#10;ter.xhtml", "chap&#13;ter.xhtml",
                    "&#32;chapter.xhtml", "chapter.xhtml?", "chapter.xhtml#"):
            with self.subTest(ref=ref):
                with self.assertRaises(epub.EpubError):
                    epub.extract_epub(make_epub(href_xml=ref))

    def test_real_archive_rejects_malformed_percent_even_when_member_exists(self):
        for name in ("chapter%GG.xhtml", "chapter%.xhtml", "chapter%2.xhtml"):
            with self.subTest(name=name):
                with self.assertRaises(epub.EpubError):
                    epub.extract_epub(make_epub(href=name, member="OPS/" + name))

    def test_real_encoded_members_keep_body_and_provenance_contract(self):
        for version in ("2.0", "3.0"):
            for name in ("chapter one.xhtml", "глава.xhtml", "chapter%.xhtml",
                         "chapter%GG.xhtml", "chapter%2f.xhtml", "chapter#?.xhtml"):
                with self.subTest(version=version, name=name):
                    raw = make_epub(href=quote(name), member="OPS/" + name, version=version)
                    body, receipt = epub.extract_epub(raw)
                    self.assertEqual(body, b"Alpha beta.\n\nGamma delta.")
                    self.assertEqual(receipt["archive_sha256"], sha256(raw).hexdigest())
                    self.assertEqual(receipt["extracted_body_sha256"], sha256(body).hexdigest())
                    self.assertEqual(receipt["extraction_profile"], "scriptorium-epub-spine-xhtml-v1")
                    self.assertFalse(receipt["source_text_embedded"])
                    self.assertEqual(epub.extract_epub(raw), (body, receipt))

    def test_original_nul_member_is_rejected_even_when_unreferenced(self):
        raw = make_epub(extras=[("OPS/PRIVATE_Xnote", b"unused")])
        self.assertEqual(raw.count(b"OPS/PRIVATE_Xnote"), 2)
        raw = raw.replace(b"OPS/PRIVATE_Xnote", b"OPS/PRIVATE_\x00note")
        with ZipFile(BytesIO(raw)) as archive:
            info = archive.infolist()[-1]
            self.assertNotEqual(info.orig_filename, info.filename)
        with self.assertRaises(epub.EpubError) as failure:
            epub.extract_epub(raw)
        self.assertNotIn("PRIVATE", str(failure.exception))

    def test_valid_directory_and_unused_unicode_names_still_work(self):
        raw = make_epub(extras=[("OPS/images/", b""), ("OPS/images/рисунок", b"unused")])
        self.assertEqual(epub.extract_epub(raw)[0], b"Alpha beta.\n\nGamma delta.")

    def test_depth_limit_inclusive_and_one_over_rejected(self):
        with patch.object(epub, "MAX_XML_DEPTH", 8, create=True):
            epub._load_xml(b"<x>" * 8 + b"</x>" * 8, "XHTML")
            with self.assertRaisesRegex(epub.EpubError, "XML structure limits"):
                epub._load_xml(b"<x>" * 9 + b"</x>" * 9, "XHTML")

    def test_element_limit_inclusive_and_one_over_rejected(self):
        with patch.object(epub, "MAX_XML_ELEMENTS", 10, create=True):
            self.assertEqual(len(epub._load_xml(b"<x>" + b"<y/>" * 9 + b"</x>", "OPF")), 9)
            with self.assertRaisesRegex(epub.EpubError, "XML structure limits"):
                epub._load_xml(b"<x>" + b"<y/>" * 10 + b"</x>", "OPF")

    def test_shape_accounting_across_chunks_preserves_text_and_tails(self):
        xml = b'<x>begin<y a="value">middle</y>tail<z/>end</x>'
        with patch.object(epub, "_XML_CHUNK_CHARS", 3, create=True):
            root = epub._load_xml(xml, "XHTML")
            self.assertEqual("".join(root.itertext()), "beginmiddletailend")
            with patch.object(epub, "MAX_XML_ELEMENTS", 2, create=True):
                with self.assertRaises(epub.EpubError):
                    epub._load_xml(xml, "XHTML")

    def test_malformed_xml_and_entities_stay_rejected(self):
        for xml in (b"", b"<x>", b"<x/><y/>", b"<x>&unknown;</x>", b"\xff",
                    b'<!DOCTYPE x [<!ENTITY e "data">]><x>&e;</x>'):
            with self.subTest(xml=xml):
                with self.assertRaises(epub.EpubError):
                    epub._load_xml(xml, "OPF")

    def test_deep_real_chapter_fails_before_python_recursion_limit(self):
        raw = make_epub(body="<div>" * 127 + "Original." + "</div>" * 127)
        with self.assertRaisesRegex(epub.EpubError, "XML structure limits"):
            epub.extract_epub(raw)

    def test_body_limit_counts_utf8_bytes_not_characters(self):
        raw = make_epub(body="<p>Кот.</p><p>Пёс.</p>")
        expected = "Кот.\n\nПёс.".encode()
        with patch.object(epub, "MAX_BODY_BYTES", len(expected)):
            self.assertEqual(epub.extract_epub(raw)[0], expected)
        with patch.object(epub, "MAX_BODY_BYTES", len(expected) - 1):
            with self.assertRaisesRegex(epub.EpubError, "body exceeds"):
                epub.extract_epub(raw)

    def test_cross_chapter_separator_is_counted_before_reading_further(self):
        source = make_epub(body="<p>A.</p>")
        target = BytesIO()
        with ZipFile(BytesIO(source)) as old, ZipFile(target, "w", compression=ZIP_STORED) as new:
            for info in old.infolist():
                raw = old.read(info)
                if info.filename == "OPS/package.opf":
                    raw = raw.replace(b"</manifest>",
                        b'<item id="d" href="second.xhtml" media-type="application/xhtml+xml"/></manifest>')
                    raw = raw.replace(b"</spine>", b'<itemref idref="d"/></spine>')
                new.writestr(info, raw)
            new.writestr("OPS/second.xhtml",
                b'<html xmlns="http://www.w3.org/1999/xhtml"><body><p>B.</p></body></html>')
        raw = target.getvalue()
        with patch.object(epub, "MAX_BODY_BYTES", 6):
            self.assertEqual(epub.extract_epub(raw)[0], b"A.\n\nB.")
        with patch.object(epub, "MAX_BODY_BYTES", 5):
            with self.assertRaisesRegex(epub.EpubError, "body exceeds"):
                epub.extract_epub(raw)


class EpubBoundaryCliTests(unittest.TestCase):
    """Run against the real installed analyzer in the package CI smoke too."""

    def test_invalid_archives_never_create_reports_or_expose_private_paths(self):
        from contextlib import redirect_stderr, redirect_stdout
        from io import StringIO
        from pathlib import Path
        import tempfile
        from scriptorium import cli

        nul = make_epub(extras=[("OPS/PRIVATE_Xnote", b"unused")]).replace(
            b"OPS/PRIVATE_Xnote", b"OPS/PRIVATE_\x00note")
        archives = (
            make_epub(href_xml="chap&#9;ter.xhtml"),
            make_epub(href="chapter%GG.xhtml", member="OPS/chapter%GG.xhtml"),
            make_epub(href="//[PRIVATE"),
            make_epub(body="<div>" * 127 + "Original." + "</div>" * 127),
            nul,
        )
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, report, sidecar = (root / name for name in
                                      ("PRIVATE-book.epub", "report.json", "identity.json"))
            for index, raw in enumerate(archives):
                source.write_bytes(raw)
                out, err = StringIO(), StringIO()
                with self.subTest(index=index), redirect_stdout(out), redirect_stderr(err):
                    with self.assertRaises(SystemExit) as failure:
                        cli.main(["epub", str(source), "--output", str(report),
                                  "--provenance-output", str(sidecar)])
                    self.assertEqual(failure.exception.code, 2)
                self.assertFalse(report.exists())
                self.assertFalse(sidecar.exists())
                self.assertEqual(out.getvalue(), "")
                self.assertNotIn(folder, err.getvalue())
                self.assertNotIn("PRIVATE", err.getvalue())
                self.assertNotIn("Traceback", err.getvalue())

    def test_valid_encoded_names_use_real_analyzer_in_all_report_formats(self):
        from pathlib import Path
        import json
        import tempfile
        from scriptorium import cli
        from scriptorium.analyze import build_local_analysis

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "PRIVATE-book.epub"
            raw = make_epub(href="chapter%20%252f.xhtml", member="OPS/chapter %2f.xhtml")
            source.write_bytes(raw)
            body, witness = epub.extract_epub(raw)
            expected = build_local_analysis(body)
            for fmt in ("json", "html", "csv", "markdown"):
                report, sidecar = root / ("report." + fmt), root / (fmt + "-identity.json")
                with self.subTest(format=fmt):
                    self.assertEqual(cli.main(["epub", str(source), "--format", fmt,
                                               "--output", str(report),
                                               "--provenance-output", str(sidecar)]), 0)
                    text = report.read_text(encoding="utf-8")
                    self.assertTrue(text)
                    self.assertNotIn("Alpha beta.", text)
                    self.assertNotIn(folder, text)
                    identity = json.loads(sidecar.read_text(encoding="utf-8"))
                    self.assertEqual(identity["archive_sha256"], witness["archive_sha256"])
                    self.assertEqual(identity["extracted_body_sha256"], expected["source"]["raw_sha256"])
                    if fmt == "json":
                        self.assertEqual(json.loads(text), expected)


if __name__ == "__main__":
    unittest.main()
