"""Source-free structural probing helpers for the Klim Samgin freeze.

The probe reports markup/dependency inventory only. Source prose remains transient in
process memory. This intentionally fails closed rather than pretending that a parent
revision freezes unversioned Wikisource transclusions.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Mapping, Sequence

from .single_page_body import fetch_pinned_wikitext
from .single_page_revision import _api_query, validate_manifest as validate_revision_manifest


_TEMPLATE_NAME_RE = re.compile(r"\{\{\s*([^|{}\n]+)")
_HTML_TAG_NAME_RE = re.compile(r"<\/?\s*([A-Za-z][A-Za-z0-9]*)\b")
_HEADING_RE = re.compile(r"(?m)^(={2,6})\s*.*?\s*\1\s*$")
_CATEGORY_RE = re.compile(r"(?mi)^\s*\[\[\s*(?:Категория|Category)\s*:")
_LST_TARGET_RE = re.compile(r"\{\{\s*#lst\s*:\s*([^|{}\n]+)\|", re.IGNORECASE)


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def probe_revision_shape(revision_manifest: Mapping[str, object]) -> dict[str, object]:
    """Return source-free markup inventory for an already-pinned exact revision."""

    validate_revision_manifest(revision_manifest)
    source_identity = revision_manifest.get("source_identity")
    assert isinstance(source_identity, dict)
    title = source_identity.get("title")
    revision_id = source_identity.get("revision_id")
    if not isinstance(title, str) or not isinstance(revision_id, int):
        raise ValueError("revision manifest source identity incomplete")

    observed = fetch_pinned_wikitext(title=title, revision_id=revision_id)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient source prose missing")
    if observed != source_identity:
        differing = sorted(
            key for key in set(observed) | set(source_identity)
            if observed.get(key) != source_identity.get(key)
        )
        raise ValueError(f"pinned revision identity drift before probe: {differing}")

    templates = Counter(match.group(1).strip() for match in _TEMPLATE_NAME_RE.finditer(wikitext))
    html_tags = Counter(match.group(1).lower() for match in _HTML_TAG_NAME_RE.finditer(wikitext))
    heading_levels = Counter(len(match.group(1)) for match in _HEADING_RE.finditer(wikitext))
    lst_targets = sorted(set(match.group(1).strip() for match in _LST_TARGET_RE.finditer(wikitext)))
    nonempty_lines = [line.strip() for line in wikitext.splitlines() if line.strip()]

    def line_class(line: str) -> str:
        if line.startswith("{{"):
            return "template"
        if line.startswith("[[") and ":" in line:
            return "wikilink_or_category"
        if re.match(r"^={2,6}", line):
            return "heading"
        if line.startswith("<"):
            return "html"
        return "content_or_markup"

    return {
        "probe_version": "scriptorium-klim-samgin-shape-probe-v2",
        "candidate_id": revision_manifest["candidate_id"],
        "revision_id": revision_id,
        "wikitext_character_count": len(wikitext),
        "line_count": len(wikitext.splitlines()),
        "nonempty_line_count": len(nonempty_lines),
        "template_names": dict(sorted(templates.items())),
        "lst_transclusion_targets": lst_targets,
        "html_tag_names": dict(sorted(html_tags.items())),
        "heading_level_counts": {str(level): count for level, count in sorted(heading_levels.items())},
        "category_link_count": len(_CATEGORY_RE.findall(wikitext)),
        "table_start_count": wikitext.count("{|"),
        "table_end_count": wikitext.count("|}"),
        "noinclude_open_count": len(re.findall(r"<noinclude\b", wikitext, re.IGNORECASE)),
        "noinclude_close_count": len(re.findall(r"</noinclude\s*>", wikitext, re.IGNORECASE)),
        "ref_open_count": len(re.findall(r"<ref\b", wikitext, re.IGNORECASE)),
        "first_nonempty_line_class": line_class(nonempty_lines[0]) if nonempty_lines else "empty",
        "last_nonempty_line_class": line_class(nonempty_lines[-1]) if nonempty_lines else "empty",
        "source_text_included": False,
    }


def resolve_current_revision_identity(title: str) -> dict[str, object]:
    """Resolve one dependency to a source-free current revision identity."""

    payload = _api_query({
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
        "redirects": "0",
    })
    query_obj = payload.get("query")
    pages = query_obj.get("pages") if isinstance(query_obj, dict) else None
    if not isinstance(pages, list) or len(pages) != 1:
        raise ValueError("expected exactly one dependency page")
    page = pages[0]
    if not isinstance(page, dict) or page.get("title") != title or page.get("missing") is True:
        raise ValueError("dependency title missing or drifted")
    revisions = page.get("revisions")
    if not isinstance(revisions, list) or len(revisions) != 1:
        raise ValueError("expected exactly one dependency revision")
    revision = revisions[0]
    slots = revision.get("slots") if isinstance(revision, dict) else None
    main = slots.get("main") if isinstance(slots, dict) else None
    wikitext = main.get("content") if isinstance(main, dict) else None
    if not isinstance(wikitext, str):
        raise ValueError("dependency wikitext missing")
    raw = wikitext.encode("utf-8")
    return {
        "title": title,
        "page_id": page.get("pageid"),
        "revision_id": revision.get("revid"),
        "revision_timestamp": revision.get("timestamp"),
        "mediawiki_sha1": revision.get("sha1"),
        "wikitext_character_count": len(wikitext),
        "wikitext_utf8_byte_count": len(raw),
        "wikitext_sha256": sha256(raw).hexdigest(),
        "source_text_included": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Probe pinned Klim Samgin source shape without emitting source prose.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision-manifest", type=Path)
    group.add_argument("--resolve-title")
    args = parser.parse_args(argv)
    if args.revision_manifest is not None:
        result = probe_revision_shape(_load_json(args.revision_manifest))
        prefix = "SCRIPTORIUM_KLIM_SHAPE="
    else:
        result = resolve_current_revision_identity(str(args.resolve_title))
        prefix = "SCRIPTORIUM_KLIM_DEPENDENCY="
    print(prefix + json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
