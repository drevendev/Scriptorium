"""Conservative source-free preflight for 185 pinned Paris 1927 Page revisions.

This is a *candidate* projection, not a ProofreadPage render: Page header/footer,
page joins and historic parent transclusion semantics remain unproven. No prose is
serialized or written, including on provider failures.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import re
import sys
from typing import Callable, Mapping

from .white_guard_paris_manifest import CSV_SHA256, load_rows
from .white_guard_page_identities import EXPECTED_RANGES
from .white_guard_revisions import SOURCE_FAMILY_1927, canonical_json_text
from .wikisource_replay import fetch_pinned_chapter_revisions

SCHEMA_VERSION = "scriptorium-white-guard-paris-body-preflight-v1"
EXTRACTION_PROFILE = "scriptorium-proofreadpage-conservative-page-v1-candidate"
MAX_PAGE_CHARACTERS = 200_000
# Only literal, balanced noinclude regions at the outside of a Page are removed.
# Wiki styling, external links and line-start structures must not become prose metrics.
_NOINCLUDE = re.compile(r"<noinclude>.*?</noinclude\s*>", re.I | re.S)
_UNSAFE = re.compile(
    r"<|>|\{\{|\}\}|\[\[|\]\]|\[(?:[a-z][a-z0-9+.-]*:|//)|'{2,}|^\s*(?:={1,6}\s|[|!]{1,2})"
    r"|^[ \t]*(?:[*#:;]|-{4,})", re.I | re.M
)


def candidate_page_body(source: str) -> tuple[str, str | None]:
    """Return bounded, conservative plain-text candidate or a fixed failure code.

    Unlike a MediaWiki render this deliberately refuses templates and inline HTML,
    including section markers, rather than silently losing or fabricating text.
    """
    if not isinstance(source, str):
        raise ValueError("invalid pinned Page response")
    if len(source) > MAX_PAGE_CHARACTERS:
        return "OVERSIZED_PAGE", None
    if not source:
        return "EMPTY_PAGE", None
    text = source
    # Boundary-only noinclude wrappers, never content in the literary middle.
    removed = 0
    while True:
        stripped = text.lstrip()
        match = _NOINCLUDE.match(stripped)
        if match is None:
            break
        removed += 1
        text = stripped[match.end():]
        if removed > 3:
            return "UNSUPPORTED_PAGE_MARKUP", None
    while True:
        stripped = text.rstrip()
        matches = list(_NOINCLUDE.finditer(stripped))
        if not matches or matches[-1].end() != len(stripped):
            break
        removed += 1
        text = stripped[:matches[-1].start()]
        if removed > 3:
            return "UNSUPPORTED_PAGE_MARKUP", None
    if "<noinclude" in text.lower() or "</noinclude" in text.lower():
        return "UNSUPPORTED_PAGE_MARKUP", None
    body = text.strip()
    if not body:
        return "EMPTY_PAGE", None
    if _UNSAFE.search(body):
        return "UNSUPPORTED_PAGE_MARKUP", None
    return "CANDIDATE_ONLY", body


def build_preflight(
    *,
    loader: Callable[[], tuple[dict[str, object], ...]] = load_rows,
    fetcher: Callable[..., Mapping[str, str]] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Replay all immutable oldids; only release metadata after complete provider read.

    Real fetcher checks exact oldid, page ID, timestamp and MediaWiki SHA-1 before
    this routine sees raw text. Provider/identity errors abort with no receipt.
    """
    rows = loader()
    if len(rows) != 185 or [r["page_number"] for r in rows] != list(range(5, 190)):
        raise ValueError("invalid Paris Page inventory")
    identities = tuple({k: r[k] for k in (
        "title", "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1"
    )} for r in rows)
    sources = fetcher(identities)
    if not isinstance(sources, Mapping) or set(sources) != {r["title"] for r in rows}:
        raise ValueError("incomplete pinned Page contents")
    pages = []
    chapter_bodies: dict[int, list[str]] = {i: [] for i in range(1, 12)}
    failed_chapters: set[int] = set()
    for row in rows:
        source = sources[row["title"]]
        try:
            status, body = candidate_page_body(source)
        except Exception:
            status, body = "UNCLASSIFIED_ERROR", None
        entry = {"page_number": row["page_number"], "chapter": row["chapter"],
                 "revision_id": row["revision_id"], "status": status,
                 "candidate_characters_including_spaces": len(body) if body is not None else None,
                 "candidate_sha256": sha256(body.encode("utf-8")).hexdigest() if body is not None else None}
        pages.append(entry)
        if body is None:
            failed_chapters.add(row["chapter"])
        else:
            chapter_bodies[row["chapter"]].append(body)
    chapters = []
    for chapter, (first, last) in enumerate(EXPECTED_RANGES, start=1):
        complete = chapter not in failed_chapters and len(chapter_bodies[chapter]) == last - first + 1
        composite = "\n".join(chapter_bodies[chapter]) if complete else None
        chapters.append({"chapter": chapter, "first_page": first, "last_page": last,
                         "candidate_page_count": len(chapter_bodies[chapter]),
                         "status": "CANDIDATE_ONLY" if complete else "INCOMPLETE",
                         "candidate_characters_including_spaces": len(composite) if composite is not None else None,
                         "candidate_sha256": sha256(composite.encode("utf-8")).hexdigest() if composite is not None else None})
    return {"schema_version": SCHEMA_VERSION, "extraction_profile": EXTRACTION_PROFILE,
            "source_family_id": SOURCE_FAMILY_1927, "page_manifest_sha256": CSV_SHA256,
            "provider_replay": "VERIFIED_IDENTITIES" if fetcher is fetch_pinned_chapter_revisions else "INJECTED_FIXTURE",
            "page_count": len(rows), "candidate_page_count": sum(p["status"] == "CANDIDATE_ONLY" for p in pages),
            "chapter_count": len(chapters), "candidate_chapter_count": sum(c["status"] == "CANDIDATE_ONLY" for c in chapters),
            "pages": pages, "chapters": chapters,
            "historical_transclusion_proven": False, "single_edition_body_frozen": False,
            "fantlab_input_identity": "unknown", "m2_parity_admissible": False,
            "source_text_committed": False}


def main(argv: list[str] | None = None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    try:
        receipt = build_preflight()
    except Exception:
        print("Pinned Paris Page body preflight failed; no receipt issued.", file=sys.stderr)
        return 2
    print(canonical_json_text(receipt), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
