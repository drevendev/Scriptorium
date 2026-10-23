"""Installed-wheel, out-of-checkout EPUB -> Reader reports smoke (synthetic text)."""
from __future__ import annotations

import csv
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


def fixture() -> bytes:
    container = ('<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OPS/content.opf" '
                 'media-type="application/oebps-package+xml"/></rootfiles></container>')
    opf = ('<package xmlns="http://www.idpf.org/2007/opf" version="3.0">'
           '<manifest><item id="a" href="a.xhtml" media-type="application/xhtml+xml"/>'
           '<item id="b" href="b.xhtml" media-type="application/xhtml+xml"/></manifest>'
           '<spine><itemref idref="a"/><itemref idref="b"/></spine></package>')
    body_a = ('<html xmlns="http://www.w3.org/1999/xhtml"><body>'
              '<p>Первый текст. Кот спит.</p></body></html>')
    body_b = ('<html xmlns="http://www.w3.org/1999/xhtml"><body>'
              '<p>Вторая глава. Пёс идёт.</p></body></html>')
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr("mimetype", b"application/epub+zip", compress_type=ZIP_STORED)
        archive.writestr("META-INF/container.xml", container, compress_type=ZIP_DEFLATED)
        archive.writestr("OPS/content.opf", opf, compress_type=ZIP_DEFLATED)
        archive.writestr("OPS/b.xhtml", body_b, compress_type=ZIP_DEFLATED)
        archive.writestr("OPS/a.xhtml", body_a, compress_type=ZIP_DEFLATED)
    return buffer.getvalue()


def main() -> None:
    checkout = Path(sys.argv[1]).resolve()
    assert not Path.cwd().resolve().is_relative_to(checkout)
    import scriptorium
    assert not Path(scriptorium.__file__).resolve().is_relative_to(checkout)
    cli = Path(sys.executable).parent / "scriptorium"
    assert cli.is_file(), "installed console script required"

    with tempfile.TemporaryDirectory(prefix="scriptorium-epub-smoke-") as private:
        folder = Path(private)
        archive = fixture()
        epub = folder / "private.epub"
        epub.write_bytes(archive)

        def run(*args: str, success: bool = True):
            proc = subprocess.run([str(cli), "epub", str(epub), *args],
                                  cwd=folder, capture_output=True, text=True, timeout=30)
            assert (proc.returncode == 0) == success, proc.stderr
            assert str(folder) not in proc.stderr
            return proc

        report = folder / "report.json"
        identity = folder / "identity.json"
        run("--output", str(report), "--provenance-output", str(identity))
        analysis = json.loads(report.read_text(encoding="utf-8"))
        receipt = json.loads(identity.read_text(encoding="utf-8"))
        assert analysis["schema_version"] == "scriptorium-local-analysis-v1"
        assert len(analysis["metrics"]) == 29
        assert receipt["archive_sha256"] == sha256(archive).hexdigest()
        assert receipt["extracted_body_sha256"] == analysis["source"]["raw_sha256"]
        assert receipt["normalized_sha256"] == analysis["source"]["normalized_sha256"]
        assert receipt["spine_documents"] == 2
        assert not receipt["source_text_embedded"]
        for artifact in (report, identity):
            text = artifact.read_text(encoding="utf-8")
            assert "Первый текст" not in text and "Вторая глава" not in text

        html = folder / "report.html"
        csv = folder / "report.csv"
        run("--format", "html", "--output", str(html))
        run("--format", "csv", "--output", str(csv))
        assert "At a glance" in html.read_text(encoding="utf-8")
        assert len(list(csv_rows(csv))) == 29

        # The EPUB-produced JSON must be consumed unchanged by Reader compare.
        comparison = folder / "comparison.json"
        proc = subprocess.run([str(cli), "compare", str(report), str(report),
                               "--output", str(comparison)], cwd=folder,
                              capture_output=True, text=True, timeout=30)
        assert proc.returncode == 0, proc.stderr
        assert len(json.loads(comparison.read_text(encoding="utf-8"))["metrics"]) == 29
        old = report.read_bytes()
        run("--output", str(report), success=False)
        assert report.read_bytes() == old
        epub.write_bytes(b"not an epub")
        bad = folder / "bad.json"
        run("--output", str(bad), success=False)
        assert not bad.exists()
    print("Installed EPUB Reader PASS: original 2-chapter EPUB, 29 metrics, "
          "JSON/HTML/CSV, source hashes, compare, invalid input and create-only output")


def csv_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as stream:
        yield from csv.DictReader(stream)


if __name__ == "__main__":
    main()
