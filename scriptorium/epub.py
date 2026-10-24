"""Bounded, local-only EPUB 2/3 XHTML-spine ingestion for Scriptorium Reader.

No archive member is written to disk, no network resources are fetched and no
container markup is executed. The output is a versioned UTF-8 text projection;
container identity is separately recorded rather than pretending it is a TXT.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import posixpath
import re
import stat
import sys
import unicodedata
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZIP_DEFLATED, ZIP_STORED, ZipFile

EXTRACTION_PROFILE = "scriptorium-epub-spine-xhtml-v1"
PROVENANCE_SCHEMA = "scriptorium-private-epub-provenance-v1"
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
MAX_MEMBER_BYTES = 16 * 1024 * 1024
MAX_TOTAL_EXPANDED = 64 * 1024 * 1024
MAX_BODY_BYTES = 32 * 1024 * 1024
MAX_MEMBERS = 256
MAX_CHAPTERS = 128
_OPF_NS = "{http://www.idpf.org/2007/opf}"
_CONTAINER_NS = "{urn:oasis:names:tc:opendocument:xmlns:container}"
_XHTML_NS = "{http://www.w3.org/1999/xhtml}"
_SKIP = frozenset({"head", "style", "script", "nav", "svg", "math", "iframe", "object", "audio", "video", "noscript", "form"})
_BLOCK = frozenset({"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "li", "ul", "ol", "blockquote", "br", "hr", "table", "tr", "td", "th", "pre"})


class EpubError(ValueError):
    """Controlled, path-free rejection of an untrusted ebook."""


def _safe_name(name: str) -> str:
    if (not name or len(name) > 512 or "\\" in name or "\x00" in name
            or unicodedata.normalize("NFC", name) != name or name.startswith("/")):
        raise EpubError("unsupported archive member path")
    parts = name.removesuffix("/").split("/")
    if len(parts) > 12 or any(not part or part in (".", "..") or ":" in part
                              or any(ord(c) < 32 for c in part) for part in parts):
        raise EpubError("unsafe archive member path")
    return name


def _load_xml(raw: bytes, label: str) -> ET.Element:
    try:
        decoded = raw.decode("utf-8-sig")
    except UnicodeError as exc:
        raise EpubError(f"invalid {label} UTF-8 XML") from exc
    if "\x00" in decoded or re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", decoded, re.I):
        raise EpubError(f"{label} declares unsupported XML entities or encoding")
    try:
        return ET.fromstring(decoded)
    except (ET.ParseError, UnicodeError, ValueError) as exc:
        raise EpubError(f"invalid {label} XML") from exc


def _archive_members(archive: ZipFile) -> dict[str, object]:
    infos = archive.infolist()
    if not 1 <= len(infos) <= MAX_MEMBERS:
        raise EpubError("EPUB has too many archive members")
    if infos[0].filename != "mimetype" or infos[0].compress_type != ZIP_STORED:
        raise EpubError("EPUB mimetype must be the first, uncompressed member")
    seen = {}
    canonical_names = set()
    expanded = 0
    for info in infos:
        name = _safe_name(info.filename)
        canonical = name.removesuffix("/")
        if canonical in canonical_names:
            raise EpubError("duplicate or ambiguous EPUB archive member")
        canonical_names.add(canonical)
        seen[name] = info
        mode = stat.S_IFMT(info.external_attr >> 16)
        if mode not in (0, stat.S_IFREG, stat.S_IFDIR):
            raise EpubError("EPUB contains an unsafe archive member type")
        if info.flag_bits & 1 or info.compress_type not in (ZIP_STORED, ZIP_DEFLATED):
            raise EpubError("encrypted or unsupported EPUB member")
        if info.file_size > MAX_MEMBER_BYTES or info.file_size < 0 or info.compress_size < 0:
            raise EpubError("EPUB member exceeds decompression limits")
        if info.file_size and info.file_size > max(1, info.compress_size) * 150:
            raise EpubError("EPUB member exceeds compression-ratio limit")
        expanded += info.file_size
        if expanded > MAX_TOTAL_EXPANDED:
            raise EpubError("EPUB exceeds total expanded-byte limit")
    return seen


def _read_member(archive: ZipFile, members: dict, path: str, limit: int) -> bytes:
    member = members.get(path)
    if member is None or member.is_dir() or member.file_size > limit:
        raise EpubError("required EPUB document missing or oversized")
    try:
        with archive.open(member) as reader:
            raw = reader.read(limit + 1)
    except (BadZipFile, OSError, RuntimeError, ValueError) as exc:
        raise EpubError("unreadable EPUB document") from exc
    if len(raw) != member.file_size or len(raw) > limit:
        raise EpubError("EPUB document size mismatch")
    return raw


def _resolved_member(opf_path: str, href: str) -> str:
    if not isinstance(href, str) or len(href) > 512:
        raise EpubError("invalid EPUB spine href")
    parts = urlsplit(href)
    if parts.scheme or parts.netloc or parts.query or parts.fragment:
        raise EpubError("remote or fragment EPUB spine href is unsupported")
    try:
        decoded = unquote(parts.path, encoding="utf-8", errors="strict")
    except UnicodeError as exc:
        raise EpubError("invalid encoded EPUB spine href") from exc
    _safe_name(decoded)
    return _safe_name(posixpath.join(posixpath.dirname(opf_path), decoded))


def _spine_paths(archive: ZipFile, members: dict) -> list[str]:
    container = _load_xml(_read_member(archive, members, "META-INF/container.xml", 64 * 1024), "container")
    if container.tag != _CONTAINER_NS + "container":
        raise EpubError("unsupported EPUB container namespace")
    rootfiles = container.findall("./" + _CONTAINER_NS + "rootfiles/" + _CONTAINER_NS + "rootfile")
    if len(rootfiles) != 1 or rootfiles[0].get("media-type") != "application/oebps-package+xml":
        raise EpubError("EPUB requires one OPF package rootfile")
    opf_path = _safe_name(rootfiles[0].get("full-path") or "")
    package = _load_xml(_read_member(archive, members, opf_path, 2 * 1024 * 1024), "OPF")
    if package.tag != _OPF_NS + "package" or package.get("version", "").split(".")[0] not in ("2", "3"):
        raise EpubError("unsupported EPUB package version")
    manifest = package.find(_OPF_NS + "manifest")
    spine = package.find(_OPF_NS + "spine")
    if manifest is None or spine is None:
        raise EpubError("EPUB manifest or spine missing")
    items = {}
    targets = set()
    for item in manifest.findall(_OPF_NS + "item"):
        ident, href = item.get("id"), item.get("href")
        if not ident or ident in items or not href:
            raise EpubError("duplicate or missing EPUB manifest item")
        target = _resolved_member(opf_path, href)
        if target in targets:
            raise EpubError("ambiguous EPUB manifest targets")
        targets.add(target)
        items[ident] = (target, item.get("media-type"))
    paths = []
    seen_spine = set()
    for ref in spine.findall(_OPF_NS + "itemref"):
        ident = ref.get("idref")
        if ident not in items or ident in seen_spine:
            raise EpubError("missing or duplicate EPUB spine item")
        seen_spine.add(ident)
        if ref.get("linear", "yes") == "no":
            continue
        if ref.get("linear", "yes") != "yes" or items[ident][1] != "application/xhtml+xml":
            raise EpubError("EPUB spine must use linear XHTML documents")
        paths.append(items[ident][0])
    if not 1 <= len(paths) <= MAX_CHAPTERS:
        raise EpubError("EPUB spine must contain 1–128 linear XHTML chapters")
    return paths


def _chapter_text(root: ET.Element) -> str:
    if root.tag != _XHTML_NS + "html":
        raise EpubError("EPUB chapter must be XHTML")
    body = root.find(_XHTML_NS + "body")
    if body is None:
        raise EpubError("EPUB XHTML body missing")
    parts = []

    def visit(node: ET.Element) -> None:
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in _SKIP:
            return
        block = tag in _BLOCK
        if block:
            parts.append("\n")
        if node.text:
            parts.append(node.text)
        for child in node:
            visit(child)
            if child.tail:
                parts.append(child.tail)
        if block:
            parts.append("\n")

    visit(body)
    collapsed = "\n".join(" ".join(line.split()) for line in "".join(parts).splitlines())
    return re.sub(r"\n{3,}", "\n\n", collapsed).strip()


def extract_epub(archive_bytes: bytes) -> tuple[bytes, dict[str, object]]:
    """Return spine-ordered UTF-8 text and source-free, archive/body digests."""
    if not isinstance(archive_bytes, bytes) or len(archive_bytes) > MAX_ARCHIVE_BYTES:
        raise EpubError("EPUB exceeds archive-byte limit")
    try:
        with ZipFile(BytesIO(archive_bytes)) as archive:
            members = _archive_members(archive)
            if "META-INF/encryption.xml" in members:
                raise EpubError("encrypted EPUB resources are unsupported")
            if _read_member(archive, members, "mimetype", 128) != b"application/epub+zip":
                raise EpubError("invalid EPUB mimetype")
            paths = _spine_paths(archive, members)
            chapters = []
            for path in paths:
                chapter = _load_xml(_read_member(archive, members, path, MAX_MEMBER_BYTES), "XHTML")
                text = _chapter_text(chapter)
                if text:
                    chapters.append(text)
            if not chapters:
                raise EpubError("EPUB spine has no readable body text")
    except (BadZipFile, OSError, RuntimeError, EOFError) as exc:
        raise EpubError("invalid or unreadable EPUB archive") from exc
    body = "\n\n".join(chapters).encode("utf-8")
    if len(body) > MAX_BODY_BYTES:
        raise EpubError("extracted EPUB body exceeds analysis limit")
    provenance = {
        "schema_version": PROVENANCE_SCHEMA,
        "extraction_profile": EXTRACTION_PROFILE,
        "archive_sha256": sha256(archive_bytes).hexdigest(),
        "archive_bytes": len(archive_bytes),
        "extracted_body_sha256": sha256(body).hexdigest(),
        "extracted_body_bytes": len(body),
        "spine_documents": len(paths),
        "readable_chapters": len(chapters),
        "source_text_embedded": False,
    }
    return body, provenance


def main(argv: list[str] | None = None) -> int:
    from .analyze import (LocalInputError, _read_bounded_regular_file, _write_new,
                          build_local_analysis, render_csv, render_html)
    parser = argparse.ArgumentParser(description="Analyze a local unencrypted XHTML EPUB; no uploads or DRM bypass.")
    parser.add_argument("epub", type=Path)
    parser.add_argument("--format", choices=("json", "html", "csv"), default="json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--provenance-output", type=Path,
                        help="separate create-only JSON containing archive/body/normalized identities")
    parser.add_argument("--title", help="title for the local HTML report")
    args = parser.parse_args(argv)
    try:
        if args.output is not None and args.provenance_output is not None:
            # An existing sidecar used to fail after the report had been created.
            # Catch known collisions before either create-only write. This is a
            # preflight, not a cross-file transaction: concurrent changes and
            # late I/O failures can still leave the first completed output.
            if args.output.resolve() == args.provenance_output.resolve():
                parser.error("report and provenance destinations must differ")
            if os.path.lexists(args.output) or os.path.lexists(args.provenance_output):
                parser.error("report or provenance already exists; no files were overwritten")
        raw = _read_bounded_regular_file(args.epub, MAX_ARCHIVE_BYTES, "EPUB")
        body, provenance = extract_epub(raw)
        analysis = build_local_analysis(body)
        provenance["normalized_sha256"] = analysis["source"]["normalized_sha256"]
        provenance["analysis_schema"] = analysis["schema_version"]
        if args.format == "json":
            rendered = json.dumps(analysis, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        elif args.format == "html":
            rendered = render_html(analysis, title=args.title)
        else:
            rendered = render_csv(analysis)
        if args.output is None:
            print(rendered, end="")
        else:
            _write_new(args.output, rendered)
        if args.provenance_output is not None:
            _write_new(args.provenance_output,
                       json.dumps(provenance, sort_keys=True, indent=2) + "\n")
    except FileExistsError:
        parser.error("report or provenance already exists; no files were overwritten")
    except (EpubError, LocalInputError) as exc:
        parser.error(str(exc))
    except (UnicodeError, ValueError, TypeError, OSError, RecursionError, OverflowError):
        parser.error("EPUB analysis failed or a private output could not be created")
    return 0


if __name__ == "__main__":
    sys.exit(main())
