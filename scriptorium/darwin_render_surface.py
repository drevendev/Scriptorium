"""Audit the exact Darwin/Rachinsky Page-wikitext surface without persisting prose.

The audit is intentionally one step before a renderer. It re-fetches only the 388
already-pinned literary Page revisions, verifies their frozen identities, and records
source-free markup construct shapes. Template arguments, wikitext, rendered prose,
OCR and scan bytes never enter the durable manifest.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, Sequence

from .darwin_body_contract import literary_page_sequences
from .darwin_page_freeze import CAPTURE_BATCH_SIZE, CANDIDATE_ID, _api_query
from .darwin_page_shards import load_sharded_manifest

AUDIT_VERSION = "scriptorium-darwin-render-surface-audit-v1"
PROFILE_STATUS = "surface_inventory_frozen_renderer_unfrozen"
EXPECTED_LITERARY_PAGE_COUNT = 388

_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_NOINCLUDE_BLOCK_RE = re.compile(
    r"<noinclude\b[^>]*>.*?</noinclude\s*>", re.IGNORECASE | re.DOTALL
)
_NOINCLUDE_EMPTY_RE = re.compile(r"<noinclude\b[^>]*/\s*>", re.IGNORECASE)
_NOINCLUDE_TOKEN_RE = re.compile(r"</?noinclude\b", re.IGNORECASE)
_TAG_RE = re.compile(r"<\s*(/?)\s*([A-Za-z][A-Za-z0-9:-]*)\b([^>]*)>", re.DOTALL)
_LITERAL_BLOCK_RE = re.compile(
    r"<(nowiki|pre|source|syntaxhighlight|math)\b[^>]*>.*?</\1\s*>",
    re.IGNORECASE | re.DOTALL,
)
_EXTERNAL_LINK_RE = re.compile(r"(?<!\[)\[(?:https?:)?//[^\]\s]+(?:\s+[^\]]*)?\]")
_HEADING_RE = re.compile(r"(?m)^\s*={2,6}[^\n]*={2,6}\s*$")
_TABLE_OPEN_RE = re.compile(r"(?m)^\s*\{\|")
_TABLE_CLOSE_RE = re.compile(r"(?m)^\s*\|\}")


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _strip_nontranscluded_regions(wikitext: str) -> tuple[str, int, int]:
    """Remove comments/noinclude blocks while proving noinclude markup is balanced."""

    comments = len(_COMMENT_RE.findall(wikitext))
    text = _COMMENT_RE.sub("", wikitext)
    noinclude_blocks = len(_NOINCLUDE_BLOCK_RE.findall(text))
    text = _NOINCLUDE_BLOCK_RE.sub("", text)
    text = _NOINCLUDE_EMPTY_RE.sub("", text)
    if _NOINCLUDE_TOKEN_RE.search(text):
        raise ValueError("unbalanced noinclude markup in pinned Page wikitext")
    return text, comments, noinclude_blocks


def _mask_literal_blocks(text: str) -> str:
    """Mask literal-tag payloads so braces inside them are not mistaken for templates."""

    return _LITERAL_BLOCK_RE.sub(lambda match: " " * len(match.group(0)), text)


def _split_top_level(inner: str) -> list[str]:
    """Split a template invocation on top-level pipes only."""

    parts: list[str] = []
    start = 0
    template_depth = 0
    link_depth = 0
    index = 0
    while index < len(inner):
        pair = inner[index : index + 2]
        if pair == "{{":
            template_depth += 1
            index += 2
            continue
        if pair == "}}":
            if template_depth == 0:
                raise ValueError("unbalanced nested template close")
            template_depth -= 1
            index += 2
            continue
        if pair == "[[":
            link_depth += 1
            index += 2
            continue
        if pair == "]]":
            if link_depth == 0:
                raise ValueError("unbalanced wikilink close inside template")
            link_depth -= 1
            index += 2
            continue
        if inner[index] == "|" and template_depth == 0 and link_depth == 0:
            parts.append(inner[start:index])
            start = index + 1
        index += 1
    if template_depth or link_depth:
        raise ValueError("unbalanced nested construct inside template")
    parts.append(inner[start:])
    return parts


def _has_top_level_equals(field: str) -> bool:
    template_depth = 0
    link_depth = 0
    index = 0
    while index < len(field):
        pair = field[index : index + 2]
        if pair == "{{":
            template_depth += 1
            index += 2
            continue
        if pair == "}}" and template_depth:
            template_depth -= 1
            index += 2
            continue
        if pair == "[[":
            link_depth += 1
            index += 2
            continue
        if pair == "]]" and link_depth:
            link_depth -= 1
            index += 2
            continue
        if field[index] == "=" and template_depth == 0 and link_depth == 0:
            return bool(field[:index].strip())
        index += 1
    return False


def _template_shapes(text: str) -> list[tuple[str, int, int]]:
    """Return template name + positional/named arities, never argument values."""

    if "{{{" in text or "}}}" in text:
        raise ValueError("template-parameter braces are unsupported in Page audit")
    stack: list[int] = []
    invocations: list[str] = []
    index = 0
    while index < len(text):
        pair = text[index : index + 2]
        if pair == "{{":
            stack.append(index)
            index += 2
            continue
        if pair == "}}":
            if not stack:
                raise ValueError("unbalanced template close in Page wikitext")
            start = stack.pop()
            invocations.append(text[start + 2 : index])
            index += 2
            continue
        index += 1
    if stack:
        raise ValueError("unbalanced template open in Page wikitext")

    shapes: list[tuple[str, int, int]] = []
    for inner in invocations:
        fields = _split_top_level(inner)
        name = re.sub(r"\s+", " ", fields[0].strip())
        if not name or len(name) > 120 or any(ch in name for ch in "{}\n\r"):
            raise ValueError("dynamic/invalid template name in Page wikitext")
        positional = 0
        named = 0
        for field in fields[1:]:
            if _has_top_level_equals(field):
                named += 1
            else:
                positional += 1
        shapes.append((name, positional, named))
    return shapes


def audit_wikitext(wikitext: str) -> dict[str, object]:
    """Build a lexical-value-free construct summary for one exact Page revision."""

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    raw_tags: Counter[str] = Counter()
    tag_kinds: Counter[tuple[str, str]] = Counter()
    for match in _TAG_RE.finditer(wikitext):
        name = match.group(2).lower()
        suffix = match.group(3).rstrip()
        kind = "close" if match.group(1) else ("self_closing" if suffix.endswith("/") else "open")
        raw_tags[name] += 1
        tag_kinds[(name, kind)] += 1

    transcluded, comment_count, noinclude_block_count = _strip_nontranscluded_regions(wikitext)
    masked = _mask_literal_blocks(transcluded)
    shapes = _template_shapes(masked)
    template_counter = Counter(shapes)

    wikilink_open = masked.count("[[")
    wikilink_close = masked.count("]]" )
    if wikilink_open != wikilink_close:
        raise ValueError("unbalanced wikilink markup in Page wikitext")

    summary = {
        "comment_count": comment_count,
        "noinclude_block_count": noinclude_block_count,
        "template_shapes": [
            {"name": name, "positional": positional, "named": named, "count": count}
            for (name, positional, named), count in sorted(template_counter.items())
        ],
        "tag_shapes": [
            {"name": name, "kind": kind, "count": count}
            for (name, kind), count in sorted(tag_kinds.items())
        ],
        "wikilink_count": wikilink_open,
        "external_link_count": len(_EXTERNAL_LINK_RE.findall(masked)),
        "heading_count": len(_HEADING_RE.findall(masked)),
        "table_open_count": len(_TABLE_OPEN_RE.findall(masked)),
        "table_close_count": len(_TABLE_CLOSE_RE.findall(masked)),
    }
    summary["surface_signature_sha256"] = _sha256_text(_canonical_json(summary))
    return summary


def fetch_pinned_literary_wikitext(
    rows: Iterable[Mapping[str, object]],
    *,
    query: Callable[[Mapping[str, str]], dict[str, object]] = _api_query,
) -> dict[int, str]:
    """Fetch exact pinned literary revisions and return content transiently in memory."""

    expected = tuple(rows)
    fetched: dict[int, str] = {}
    for offset in range(0, len(expected), CAPTURE_BATCH_SIZE):
        batch = expected[offset : offset + CAPTURE_BATCH_SIZE]
        ids = [int(row["revision_id"]) for row in batch]
        by_id = {int(row["revision_id"]): row for row in batch}
        payload = query({
            "action": "query",
            "prop": "revisions",
            "revids": "|".join(str(item) for item in ids),
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
        })
        query_obj = payload.get("query")
        pages = query_obj.get("pages") if isinstance(query_obj, dict) else None
        if not isinstance(pages, list):
            raise ValueError("MediaWiki content replay response missing pages")
        for page in pages:
            if not isinstance(page, dict):
                raise ValueError("unexpected MediaWiki content replay page")
            title = page.get("title")
            revisions = page.get("revisions")
            if not isinstance(title, str) or not isinstance(revisions, list) or len(revisions) != 1:
                raise ValueError("unexpected MediaWiki content replay shape")
            revision = revisions[0]
            if not isinstance(revision, dict):
                raise ValueError("unexpected MediaWiki content revision")
            revid = revision.get("revid")
            if not isinstance(revid, int) or revid not in by_id or revid in fetched:
                raise ValueError(f"unexpected/duplicate pinned revision ID: {revid!r}")
            expected_row = by_id[revid]
            if (
                title != expected_row["title"]
                or revision.get("timestamp") != expected_row["timestamp"]
                or revision.get("sha1") != expected_row["mediawiki_sha1"]
            ):
                raise ValueError(f"pinned Page identity drift before markup audit: {revid}")
            slots = revision.get("slots")
            main = slots.get("main") if isinstance(slots, dict) else None
            content = main.get("content") if isinstance(main, dict) else None
            if not isinstance(content, str):
                raise ValueError(f"missing exact Page wikitext for revision {revid}")
            fetched[revid] = content
    if set(fetched) != {int(row["revision_id"]) for row in expected}:
        raise ValueError("literary Page content replay inventory mismatch")
    return fetched


def build_audit_manifest(
    index_path: Path,
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[int, str]] = fetch_pinned_literary_wikitext,
) -> dict[str, object]:
    rows = load_sharded_manifest(index_path)
    literary = set(literary_page_sequences())
    selected = tuple(row for row in rows if int(row["page_sequence"]) in literary)
    if len(selected) != EXPECTED_LITERARY_PAGE_COUNT:
        raise ValueError("expected exactly 388 frozen literary Page identities")
    fetched = fetcher(selected)

    templates: Counter[tuple[str, int, int]] = Counter()
    tags: Counter[tuple[str, str]] = Counter()
    totals: Counter[str] = Counter()
    page_receipts: list[dict[str, object]] = []
    for row in selected:
        revid = int(row["revision_id"])
        wikitext = fetched[revid]
        summary = audit_wikitext(wikitext)
        for item in summary["template_shapes"]:
            assert isinstance(item, dict)
            templates[(str(item["name"]), int(item["positional"]), int(item["named"]))] += int(item["count"])
        for item in summary["tag_shapes"]:
            assert isinstance(item, dict)
            tags[(str(item["name"]), str(item["kind"]))] += int(item["count"])
        for key in (
            "comment_count", "noinclude_block_count", "wikilink_count", "external_link_count",
            "heading_count", "table_open_count", "table_close_count",
        ):
            totals[key] += int(summary[key])
        page_receipts.append({
            "page_sequence": int(row["page_sequence"]),
            "revision_id": revid,
            "mediawiki_sha1": row["mediawiki_sha1"],
            "wikitext_sha256": _sha256_text(wikitext),
            "surface_signature_sha256": summary["surface_signature_sha256"],
            "template_invocation_count": sum(int(item["count"]) for item in summary["template_shapes"]),
            "tag_token_count": sum(int(item["count"]) for item in summary["tag_shapes"]),
        })

    manifest: dict[str, object] = {
        "audit_version": AUDIT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "status": PROFILE_STATUS,
        "source_revision_index_sha256": sha256(index_path.read_bytes()).hexdigest(),
        "literary_dependency_count": len(selected),
        "identity_replay_match": True,
        "source_text_included": False,
        "template_shapes": [
            {"name": name, "positional": positional, "named": named, "count": count}
            for (name, positional, named), count in sorted(templates.items())
        ],
        "tag_shapes": [
            {"name": name, "kind": kind, "count": count}
            for (name, kind), count in sorted(tags.items())
        ],
        "construct_totals": dict(sorted(totals.items())),
        "page_surface_receipts": page_receipts,
        "rendering_profile_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    manifest["audit_sha256"] = _sha256_text(_canonical_json(manifest))
    return manifest


def validate_audit_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("audit_version") != AUDIT_VERSION or manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin rendering-surface audit identity drift")
    if manifest.get("status") != PROFILE_STATUS:
        raise ValueError("Darwin rendering-surface audit status drift")
    if manifest.get("literary_dependency_count") != EXPECTED_LITERARY_PAGE_COUNT:
        raise ValueError("Darwin rendering-surface audit page count drift")
    if manifest.get("identity_replay_match") is not True or manifest.get("source_text_included") is not False:
        raise ValueError("Darwin rendering-surface source boundary drift")
    for key in (
        "rendering_profile_frozen", "literary_body_count_and_digests_frozen", "minimum_300k_proved",
        "admitted_for_calibration", "diagnostic_ready", "m2_parity_admissible",
    ):
        if manifest.get(key) is not False:
            raise ValueError(f"{key} must remain false in rendering-surface audit")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")
    pages = manifest.get("page_surface_receipts")
    if not isinstance(pages, list) or len(pages) != EXPECTED_LITERARY_PAGE_COUNT:
        raise ValueError("rendering-surface audit must contain 388 source-free Page receipts")
    forbidden = {"wikitext", "content", "text", "prose", "body", "template_arguments", "snippet"}
    serialized_keys: set[str] = set()
    stack: list[object] = [manifest]
    while stack:
        value = stack.pop()
        if isinstance(value, Mapping):
            for key, child in value.items():
                serialized_keys.add(str(key).lower())
                stack.append(child)
        elif isinstance(value, list):
            stack.extend(value)
    if forbidden.intersection(serialized_keys):
        raise ValueError("source payload key leaked into rendering-surface audit")
    expected_digest = manifest.get("audit_sha256")
    unsigned = dict(manifest)
    unsigned.pop("audit_sha256", None)
    if expected_digest != _sha256_text(_canonical_json(unsigned)):
        raise ValueError("rendering-surface audit digest drift")


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = build_audit_manifest(args.index)
    validate_audit_manifest(manifest)
    _write_json(args.output, manifest)
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
