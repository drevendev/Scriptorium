"""Audit Darwin/Rachinsky Page-wikitext constructs without persisting source prose.

This is deliberately a prerequisite to rendering: exact pinned literary Page revisions
are replayed transiently, identity-checked, and reduced to source-free construct shapes
and digests. Wikitext, template arguments, rendered prose, OCR, and scan bytes are never
serialized.
"""

from __future__ import annotations

import argparse
from collections import Counter
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
_NOINCLUDE_BLOCK_RE = re.compile(r"<noinclude\b[^>]*>.*?</noinclude\s*>", re.I | re.S)
_NOINCLUDE_EMPTY_RE = re.compile(r"<noinclude\b[^>]*/\s*>", re.I)
_NOINCLUDE_TOKEN_RE = re.compile(r"</?noinclude\b", re.I)
_TAG_RE = re.compile(r"<\s*(/?)\s*([A-Za-z][A-Za-z0-9:-]*)\b([^>]*)>", re.S)
_LITERAL_BLOCK_RE = re.compile(
    r"<(nowiki|pre|source|syntaxhighlight|math)\b[^>]*>.*?</\1\s*>", re.I | re.S
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
    comments = len(_COMMENT_RE.findall(wikitext))
    text = _COMMENT_RE.sub("", wikitext)
    noinclude_blocks = len(_NOINCLUDE_BLOCK_RE.findall(text))
    text = _NOINCLUDE_BLOCK_RE.sub("", text)
    text = _NOINCLUDE_EMPTY_RE.sub("", text)
    if _NOINCLUDE_TOKEN_RE.search(text):
        raise ValueError("unbalanced noinclude markup in pinned Page wikitext")
    return text, comments, noinclude_blocks


def _mask_literal_blocks(text: str) -> str:
    return _LITERAL_BLOCK_RE.sub(lambda match: " " * len(match.group(0)), text)


def _scan_curly_constructs(text: str) -> tuple[list[str], int]:
    """Return raw template inners plus count of triple-brace parameter constructs.

    Long runs of closing braces are parsed by the current stack type, so nested
    `{{outer|{{inner}}}}` is not misclassified as a triple-brace parameter.
    """

    stack: list[tuple[str, int]] = []
    templates: list[str] = []
    parameter_count = 0
    index = 0
    while index < len(text):
        if text.startswith("{{{", index):
            stack.append(("parameter", index))
            index += 3
            continue
        if text.startswith("{{", index):
            stack.append(("template", index))
            index += 2
            continue
        if stack and stack[-1][0] == "parameter" and text.startswith("}}}", index):
            stack.pop()
            parameter_count += 1
            index += 3
            continue
        if text.startswith("}}", index):
            if not stack or stack[-1][0] != "template":
                raise ValueError("unbalanced template close in Page wikitext")
            _, start = stack.pop()
            templates.append(text[start + 2 : index])
            index += 2
            continue
        index += 1
    if stack:
        raise ValueError(f"unbalanced curly construct in Page wikitext: {stack[-1][0]}")
    return templates, parameter_count


def _split_top_level(inner: str) -> list[str]:
    parts: list[str] = []
    start = 0
    template_depth = parameter_depth = link_depth = 0
    index = 0
    while index < len(inner):
        if inner.startswith("{{{", index):
            parameter_depth += 1
            index += 3
            continue
        if inner.startswith("{{", index):
            template_depth += 1
            index += 2
            continue
        if parameter_depth and inner.startswith("}}}", index):
            parameter_depth -= 1
            index += 3
            continue
        if template_depth and inner.startswith("}}", index):
            template_depth -= 1
            index += 2
            continue
        if inner.startswith("[[", index):
            link_depth += 1
            index += 2
            continue
        if inner.startswith("]]", index):
            if not link_depth:
                raise ValueError("unbalanced wikilink close inside template")
            link_depth -= 1
            index += 2
            continue
        if inner[index] == "|" and not (template_depth or parameter_depth or link_depth):
            parts.append(inner[start:index])
            start = index + 1
        index += 1
    if template_depth or parameter_depth or link_depth:
        raise ValueError("unbalanced nested construct inside template")
    parts.append(inner[start:])
    return parts


def _has_top_level_equals(field: str) -> bool:
    template_depth = parameter_depth = link_depth = 0
    index = 0
    while index < len(field):
        if field.startswith("{{{", index):
            parameter_depth += 1
            index += 3
            continue
        if field.startswith("{{", index):
            template_depth += 1
            index += 2
            continue
        if parameter_depth and field.startswith("}}}", index):
            parameter_depth -= 1
            index += 3
            continue
        if template_depth and field.startswith("}}", index):
            template_depth -= 1
            index += 2
            continue
        if field.startswith("[[", index):
            link_depth += 1
            index += 2
            continue
        if link_depth and field.startswith("]]", index):
            link_depth -= 1
            index += 2
            continue
        if field[index] == "=" and not (template_depth or parameter_depth or link_depth):
            return bool(field[:index].strip())
        index += 1
    return False


def _template_shapes(text: str) -> tuple[list[tuple[str, int, int]], int]:
    invocations, parameter_count = _scan_curly_constructs(text)
    shapes: list[tuple[str, int, int]] = []
    for inner in invocations:
        fields = _split_top_level(inner)
        raw_name = re.sub(r"\s+", " ", fields[0].strip())
        if not raw_name or len(raw_name) > 120 or "\n" in raw_name or "\r" in raw_name:
            raise ValueError("invalid template name in Page wikitext")
        name = "<dynamic>" if "{" in raw_name or "}" in raw_name else raw_name
        positional = sum(not _has_top_level_equals(field) for field in fields[1:])
        named = len(fields) - 1 - positional
        shapes.append((name, positional, named))
    return shapes, parameter_count


def audit_wikitext(wikitext: str) -> dict[str, object]:
    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    tag_kinds: Counter[tuple[str, str]] = Counter()
    for match in _TAG_RE.finditer(wikitext):
        name = match.group(2).lower()
        suffix = match.group(3).rstrip()
        kind = "close" if match.group(1) else ("self_closing" if suffix.endswith("/") else "open")
        tag_kinds[(name, kind)] += 1

    transcluded, comments, noinclude_blocks = _strip_nontranscluded_regions(wikitext)
    masked = _mask_literal_blocks(transcluded)
    shapes, parameter_count = _template_shapes(masked)
    templates = Counter(shapes)
    wikilink_open = masked.count("[[")
    if wikilink_open != masked.count("]]" ):
        raise ValueError("unbalanced wikilink markup in Page wikitext")

    summary: dict[str, object] = {
        "comment_count": comments,
        "noinclude_block_count": noinclude_blocks,
        "template_parameter_count": parameter_count,
        "template_shapes": [
            {"name": name, "positional": positional, "named": named, "count": count}
            for (name, positional, named), count in sorted(templates.items())
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
    expected = tuple(rows)
    fetched: dict[int, str] = {}
    for offset in range(0, len(expected), CAPTURE_BATCH_SIZE):
        batch = expected[offset : offset + CAPTURE_BATCH_SIZE]
        ids = [int(row["revision_id"]) for row in batch]
        by_id = {int(row["revision_id"]): row for row in batch}
        payload = query({
            "action": "query", "prop": "revisions", "revids": "|".join(map(str, ids)),
            "rvprop": "ids|timestamp|sha1|content", "rvslots": "main",
        })
        query_obj = payload.get("query")
        pages = query_obj.get("pages") if isinstance(query_obj, dict) else None
        if not isinstance(pages, list):
            raise ValueError("MediaWiki content replay response missing pages")
        for page in pages:
            if not isinstance(page, dict):
                raise ValueError("unexpected MediaWiki content replay page")
            revisions = page.get("revisions")
            if not isinstance(revisions, list) or len(revisions) != 1:
                raise ValueError("unexpected MediaWiki content replay shape")
            revision = revisions[0]
            if not isinstance(revision, dict):
                raise ValueError("unexpected MediaWiki content revision")
            revid = revision.get("revid")
            if not isinstance(revid, int) or revid not in by_id or revid in fetched:
                raise ValueError(f"unexpected/duplicate pinned revision ID: {revid!r}")
            row = by_id[revid]
            if (
                page.get("title") != row["title"]
                or revision.get("timestamp") != row["timestamp"]
                or revision.get("sha1") != row["mediawiki_sha1"]
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
        try:
            summary = audit_wikitext(wikitext)
        except ValueError as exc:
            raise ValueError(f"Page {row['page_sequence']} revision {revid}: {exc}") from exc
        for item in summary["template_shapes"]:
            templates[(str(item["name"]), int(item["positional"]), int(item["named"]))] += int(item["count"])
        for item in summary["tag_shapes"]:
            tags[(str(item["name"]), str(item["kind"]))] += int(item["count"])
        for key in (
            "comment_count", "noinclude_block_count", "template_parameter_count", "wikilink_count",
            "external_link_count", "heading_count", "table_open_count", "table_close_count",
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
    if manifest.get("status") != PROFILE_STATUS or manifest.get("literary_dependency_count") != 388:
        raise ValueError("Darwin rendering-surface audit status/count drift")
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
    if not isinstance(pages, list) or len(pages) != 388:
        raise ValueError("rendering-surface audit must contain 388 source-free Page receipts")
    forbidden = {"wikitext", "content", "text", "prose", "body", "template_arguments", "snippet"}
    keys: set[str] = set()
    stack: list[object] = [manifest]
    while stack:
        value = stack.pop()
        if isinstance(value, Mapping):
            for key, child in value.items():
                keys.add(str(key).lower())
                stack.append(child)
        elif isinstance(value, list):
            stack.extend(value)
    if forbidden.intersection(keys):
        raise ValueError("source payload key leaked into rendering-surface audit")
    expected = manifest.get("audit_sha256")
    unsigned = dict(manifest)
    unsigned.pop("audit_sha256", None)
    if expected != _sha256_text(_canonical_json(unsigned)):
        raise ValueError("rendering-surface audit digest drift")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = build_audit_manifest(args.index)
    validate_audit_manifest(manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
