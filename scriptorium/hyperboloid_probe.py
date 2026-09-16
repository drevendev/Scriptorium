"""Emit source-free structural metadata for the pinned Hyperboloid wikitext."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
import re

from .hyperboloid_freeze import REVISION_ID, TITLE, fetch_pinned_wikitext


_TEMPLATE_NAME_RE = re.compile(r"\{\{\s*([^|{}\n]+)")
_TAG_RE = re.compile(r"</?\s*([A-Za-z][A-Za-z0-9:-]*)\b")
_HEADING_RE = re.compile(r"^(={2,6})\s*.*?\s*\1\s*$")
_CATEGORY_RE = re.compile(r"^\s*\[\[\s*Категория\s*:", re.IGNORECASE)
_TEMPLATE_ONLY_RE = re.compile(r"^\s*\{\{.*\}\}\s*$")
_SUP_U_RE = re.compile(r"<sup>\s*<u>(.*?)</u>\s*</sup>", re.IGNORECASE | re.DOTALL)


def _inner_shape(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return "empty"
    if stripped.isdecimal():
        return "digits_only"
    if all(not ch.isalnum() for ch in stripped):
        return "punctuation_only"
    if any(ch.isalpha() for ch in stripped):
        return "contains_letters"
    return "other"


def build_probe(wikitext: str) -> dict[str, object]:
    """Describe markup shape without returning literary/source prose."""

    lines = wikitext.splitlines()
    line_kinds: Counter[str] = Counter()
    heading_levels: Counter[str] = Counter()
    for line in lines:
        stripped = line.strip()
        if not stripped:
            line_kinds["blank"] += 1
            continue
        heading = _HEADING_RE.fullmatch(stripped)
        if heading:
            line_kinds["heading"] += 1
            heading_levels[str(len(heading.group(1)))] += 1
        elif _CATEGORY_RE.match(stripped):
            line_kinds["category"] += 1
        elif _TEMPLATE_ONLY_RE.fullmatch(stripped):
            line_kinds["template_only"] += 1
        elif stripped.startswith("<"):
            line_kinds["html_prefixed"] += 1
        else:
            line_kinds["other_nonblank"] += 1

    template_names = Counter(
        re.sub(r"\s+", " ", match.group(1).strip()).casefold()
        for match in _TEMPLATE_NAME_RE.finditer(wikitext)
    )
    tag_names = Counter(match.group(1).casefold() for match in _TAG_RE.finditer(wikitext))
    sup_u_values = [match.group(1) for match in _SUP_U_RE.finditer(wikitext)]
    encoded = wikitext.encode("utf-8")
    prefix = encoded[:256]
    suffix = encoded[-256:] if len(encoded) >= 256 else encoded
    return {
        "probe_version": "scriptorium-hyperboloid-structure-probe-v2",
        "revision_id": REVISION_ID,
        "wikitext_character_count": len(wikitext),
        "wikitext_utf8_byte_count": len(encoded),
        "line_count": len(lines),
        "line_kinds": dict(sorted(line_kinds.items())),
        "heading_levels": dict(sorted(heading_levels.items())),
        "template_names": dict(sorted(template_names.items())),
        "html_tag_names": dict(sorted(tag_names.items())),
        "sup_u_pairs": {
            "count": len(sup_u_values),
            "inner_shapes": dict(sorted(Counter(_inner_shape(value) for value in sup_u_values).items())),
            "inner_lengths": sorted(Counter(len(value.strip()) for value in sup_u_values).items()),
        },
        "markup_counts": {
            "text_div_open_count": len(re.findall(r'<div\b[^>]*\bclass=["\'][^"\']*\btext\b', wikitext, re.IGNORECASE)),
            "indent_div_open_count": len(re.findall(r'<div\b[^>]*\bclass=["\'][^"\']*\bindent\b', wikitext, re.IGNORECASE)),
            "noinclude_open_count": len(re.findall(r'<noinclude\b', wikitext, re.IGNORECASE)),
            "onlyinclude_open_count": len(re.findall(r'<onlyinclude\b', wikitext, re.IGNORECASE)),
            "poem_open_count": len(re.findall(r'<poem\b', wikitext, re.IGNORECASE)),
            "table_open_count": len(re.findall(r'(?m)^\s*\{\|', wikitext)),
            "wikilink_open_count": wikitext.count("[["),
            "category_link_count": len(re.findall(r'\[\[\s*Категория\s*:', wikitext, re.IGNORECASE)),
            "bold_or_italic_marker_count": wikitext.count("''"),
            "html_comment_open_count": wikitext.count("<!--"),
            "br_tag_count": len(re.findall(r'<br\s*/?>', wikitext, re.IGNORECASE)),
        },
        "boundary_hashes": {
            "first_256_utf8_sha256": sha256(prefix).hexdigest(),
            "last_256_utf8_sha256": sha256(suffix).hexdigest(),
        },
        "source_text_included": False,
    }


def main() -> int:
    observed = fetch_pinned_wikitext(title=TITLE, revision_id=REVISION_ID)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient wikitext missing")
    print(json.dumps(build_probe(wikitext), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
