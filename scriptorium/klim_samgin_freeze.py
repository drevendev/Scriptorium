"""Source-free structural probing helpers for the Klim Samgin freeze.

The probe reports markup/dependency inventory only. Source prose remains transient in
process memory. This intentionally exposes unversioned transclusion dependencies before
a literary-body freeze can be claimed.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
from typing import Mapping, Sequence

from .single_page_body import fetch_pinned_wikitext
from .single_page_revision import validate_manifest as validate_revision_manifest


_TEMPLATE_NAME_RE = re.compile(r"\{\{\s*([^|{}\n]+)")
_HTML_TAG_NAME_RE = re.compile(r"<\/?\s*([A-Za-z][A-Za-z0-9]*)\b")
_HEADING_RE = re.compile(r"(?m)^(={2,6})\s*.*?\s*\1\s*$")
_CATEGORY_RE = re.compile(r"(?mi)^\s*\[\[\s*(?:Категория|Category)\s*:")
_LST_TARGET_RE = re.compile(
    r"\{\{\s*#lst\s*:\s*([^|{}\n]+?)(?=\||\}\})",
    re.IGNORECASE,
)


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def probe_revision_shape(revision_manifest: Mapping[str, object]) -> dict[str, object]:
    """Return source-free markup/dependency inventory for one pinned revision."""

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
            key
            for key in set(observed) | set(source_identity)
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
        "heading_level_counts": {
            str(level): count for level, count in sorted(heading_levels.items())
        },
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Probe pinned Klim Samgin source shape without emitting source prose."
    )
    parser.add_argument("--revision-manifest", type=Path, required=True)
    args = parser.parse_args(argv)
    result = probe_revision_shape(_load_json(args.revision_manifest))
    print(
        "SCRIPTORIUM_KLIM_SHAPE="
        + json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
