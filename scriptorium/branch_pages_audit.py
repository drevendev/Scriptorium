"""Fail-closed, offline link acceptance for the branch-published Russian Reader.

GitHub-managed Pages publishes master/(root); the separately generated build/site
artifact is NOT its publication tree. Check root HTML, source-free downloads and
local fragment targets before claiming that the Reader navigation is functional.
This does not attempt to verify live HTTP, appearance or deployment settings.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import posixpath
from urllib.parse import unquote, urlsplit

PAGES = (
    "index.html",
    "metrics.html",
    "word-density.html",
    "n-uncertainty.html",
    "voice/index.html",
)
REQUIRED_ASSETS = (
    "assets/pages-reader.css",
    "assets/pages-reader.js",
    "assets/evidence-snapshot.json",
    "assets/voice-preview.json",
    "assets/scriptorium-ru-measured-metrics.csv",
    "assets/n-uncertainty-anna.json",
    "voice/holdout-three.csv",
)


class ReaderLinkError(ValueError):
    """A branch Pages route, asset, or local fragment is broken or unsafe."""


class _Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.identifiers: set[str] = set()
        self.duplicates: set[str] = set()
        self.duplicate_attributes: set[str] = set()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # Browsers retain the FIRST duplicate attribute; dict(attrs) keeps the
        # LAST. Without this guard a broken/unsafe first href could be hidden
        # from the offline audit by appending a valid second href.
        seen: set[str] = set()
        for name, _ in attrs:
            if name in {"href", "src", "id"}:
                if name in seen:
                    self.duplicate_attributes.add(name)
                seen.add(name)
        attr = dict(attrs)
        identifier = attr.get("id")
        if identifier:
            if identifier in self.identifiers:
                self.duplicates.add(identifier)
            self.identifiers.add(identifier)
        key = "href" if tag in {"a", "link"} else "src" if tag in {"script", "img", "source"} else None
        if key and attr.get(key) is not None:
            self.references.append(attr[key] or "")


def audit_site(
    root: Path,
    *,
    pages: tuple[str, ...] = PAGES,
    required: tuple[str, ...] = REQUIRED_ASSETS,
) -> tuple[int, int]:
    """Return (HTML documents, internal references); reject broken/unsafe links."""
    root = Path(root).resolve()
    documents: dict[str, _Document] = {}

    def source(path: str) -> Path:
        file = root / path
        if file.absolute() != file.resolve(strict=False):
            raise ReaderLinkError(f"symlink in published path: {path}")
        if root not in file.parents or not file.is_file() or not file.stat().st_size:
            raise ReaderLinkError(f"missing/empty branch Pages file: {path}")
        return file

    def document(path: str) -> _Document:
        if path not in documents:
            file = source(path)
            try:
                markup = file.read_text(encoding="utf-8")
            except UnicodeError as exc:
                raise ReaderLinkError(f"invalid UTF-8 HTML: {path}") from exc
            parser = _Document()
            parser.feed(markup)
            parser.close()
            if parser.duplicate_attributes:
                raise ReaderLinkError(
                    f"duplicate audited HTML attributes in {path}: {sorted(parser.duplicate_attributes)}"
                )
            if parser.duplicates:
                raise ReaderLinkError(f"duplicate fragment IDs in {path}: {sorted(parser.duplicates)}")
            documents[path] = parser
        return documents[path]

    for required_file in required:
        source(required_file)
    for page in pages:
        document(page)

    internal = 0
    for page in pages:
        for reference in document(page).references:
            if not reference:
                raise ReaderLinkError(f"empty local URL in {page}")
            url = urlsplit(reference)
            if url.scheme in {"https", "http", "mailto", "tel"} or reference.startswith("//"):
                continue
            if url.scheme or url.netloc or "\\" in reference or url.path.startswith("/"):
                raise ReaderLinkError(f"unsafe Reader URL in {page}: {reference}")
            path = unquote(url.path)
            if "\\" in path or "\x00" in path:
                raise ReaderLinkError(f"unsafe Reader path in {page}: {reference}")
            target = (
                posixpath.normpath(posixpath.join(posixpath.dirname(page), path))
                if path else page
            )
            if target in {"", "."} or path.endswith("/"):
                target = posixpath.join("" if target == "." else target, "index.html")
            if target == ".." or target.startswith("../") or target.startswith("/"):
                raise ReaderLinkError(f"Reader URL escapes publication root in {page}: {reference}")
            source(target)
            internal += 1
            if url.fragment and target.endswith(".html"):
                identifier = unquote(url.fragment)
                if identifier not in document(target).identifiers:
                    raise ReaderLinkError(f"broken Reader fragment {page} -> {reference}")
    return len(pages), internal


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args(argv)
    pages, links = audit_site(Path(args.repo_root))
    print(f"Branch Pages root OK: {pages} pages, {links} local references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
