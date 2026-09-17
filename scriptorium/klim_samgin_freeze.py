"""Freeze source-free #lst selection semantics for the Klim Samgin source graph.

The retained Part 2 revision delegates one labeled section to a separately pinned
Wikisource dependency. This module verifies both immutable revision identities, resolves
that one #lst invocation at the wikitext-selection layer, and persists only offsets,
counts and digests. It deliberately does not claim that MediaWiki rendering or the final
literary-body extraction is frozen.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .single_page_body import fetch_pinned_wikitext
from .single_page_revision import validate_manifest as validate_revision_manifest


PART2_CANDIDATE_ID = "gorky-klim-samgin-ru-part-2"
DEPENDENCY_CANDIDATE_ID = "gorky-klim-samgin-ru-part-2-part2"
DEPENDENCY_TITLE = "Жизнь Клима Самгина (Горький)/Часть 2/part2"
LST_CONTRACT_VERSION = "scriptorium-klim-samgin-lst-contract-v1"
LST_SELECTION_PROFILE = "scriptorium-klim-samgin-part2-lst-selection-v1"

_TEMPLATE_NAME_RE = re.compile(r"\{\{\s*([^|{}\n]+)")
_HTML_TAG_NAME_RE = re.compile(r"</?\s*([A-Za-z][A-Za-z0-9]*)\b")
_HEADING_RE = re.compile(r"(?m)^(={2,6})\s*.*?\s*\1\s*$")
_CATEGORY_RE = re.compile(r"(?mi)^\s*\[\[\s*(?:Категория|Category)\s*:")
_LST_TARGET_RE = re.compile(
    r"\{\{\s*#lst\s*:\s*([^|{}\n]+?)(?=\||\}\})",
    re.IGNORECASE,
)
_LST_PREFIX_RE = re.compile(r"\{\{\s*#lst\s*:", re.IGNORECASE)
_LST_CALL_RE = re.compile(
    r"\{\{\s*#lst\s*:\s*"
    r"(?P<target>[^|{}]+?)\s*\|\s*"
    r"(?P<section>[^|{}]+?)\s*"
    r"(?P<range>\|[^{}]*?)?"
    r"\}\}",
    re.IGNORECASE,
)
_SECTION_PREFIX_RE = re.compile(r"<section\b", re.IGNORECASE)
_SECTION_MARKER_RE = re.compile(
    r"<section\s+(?P<kind>begin|end)\s*=\s*"
    r"(?:\"(?P<double>[^\"]+)\"|'(?P<single>[^']+)'|(?P<bare>[^\s/>]+))"
    r"\s*/\s*>",
    re.IGNORECASE,
)


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _source_free_identity(text: str) -> dict[str, object]:
    raw = text.encode("utf-8")
    return {
        "character_count": len(text),
        "utf8_byte_count": len(raw),
        "sha256": sha256(raw).hexdigest(),
    }


def _verified_wikitext(
    revision_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]],
) -> str:
    validate_revision_manifest(revision_manifest)
    source_identity = revision_manifest.get("source_identity")
    assert isinstance(source_identity, dict)
    title = source_identity.get("title")
    revision_id = source_identity.get("revision_id")
    if not isinstance(title, str) or not isinstance(revision_id, int):
        raise ValueError("revision manifest source identity incomplete")

    observed = fetcher(title=title, revision_id=revision_id)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient source prose missing")
    if observed != source_identity:
        differing = sorted(
            key
            for key in set(observed) | set(source_identity)
            if observed.get(key) != source_identity.get(key)
        )
        raise ValueError(f"pinned revision identity drift before #lst resolution: {differing}")
    return wikitext


def parse_single_lst_invocation(wikitext: str) -> dict[str, object]:
    """Parse exactly one simple #lst call and reject range or unsupported syntax."""

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    matches = tuple(_LST_CALL_RE.finditer(wikitext))
    prefix_count = len(tuple(_LST_PREFIX_RE.finditer(wikitext)))
    if prefix_count != len(matches):
        raise ValueError("unsupported #lst invocation syntax")
    if len(matches) != 1:
        raise ValueError(f"expected exactly one #lst invocation, observed {len(matches)}")
    match = matches[0]
    target = match.group("target").strip()
    section = match.group("section").strip()
    range_arg = match.group("range")
    if not target or not section:
        raise ValueError("#lst target and section label must be non-empty")
    if range_arg is not None:
        raise ValueError("Klim Samgin #lst range syntax is not supported by this frozen profile")
    return {
        "target_title": target,
        "section_label": section,
        "parent_start_offset": match.start(),
        "parent_end_offset": match.end(),
    }


def _section_markers(wikitext: str) -> list[dict[str, object]]:
    matches = tuple(_SECTION_MARKER_RE.finditer(wikitext))
    prefix_count = len(tuple(_SECTION_PREFIX_RE.finditer(wikitext)))
    if prefix_count != len(matches):
        raise ValueError("unsupported labeled-section marker syntax")
    markers: list[dict[str, object]] = []
    for match in matches:
        label = match.group("double") or match.group("single") or match.group("bare")
        if not isinstance(label, str) or not label:
            raise ValueError("empty labeled-section name")
        markers.append(
            {
                "kind": match.group("kind").casefold(),
                "label": label,
                "start_offset": match.start(),
                "end_offset": match.end(),
            }
        )
    return markers


def select_labeled_sections(wikitext: str, section_label: str) -> dict[str, object]:
    """Select all same-label #lst spans in source order, source-free in its result."""

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    if not isinstance(section_label, str) or not section_label:
        raise ValueError("section_label must be non-empty")
    markers = _section_markers(wikitext)
    selected = [marker for marker in markers if marker["label"] == section_label]
    if not selected:
        raise ValueError(f"dependency has no markers for #lst section {section_label!r}")

    open_marker: dict[str, object] | None = None
    segments: list[dict[str, object]] = []
    segment_texts: list[str] = []
    for marker in selected:
        kind = marker["kind"]
        if kind == "begin":
            if open_marker is not None:
                raise ValueError("overlapping same-label section begins are unsupported")
            open_marker = marker
            continue
        if open_marker is None:
            raise ValueError("labeled-section end appears before matching begin")
        start = int(open_marker["end_offset"])
        end = int(marker["start_offset"])
        if end < start:
            raise ValueError("labeled-section offsets are reversed")
        text = wikitext[start:end]
        identity = _source_free_identity(text)
        segments.append(
            {
                "ordinal": len(segments) + 1,
                "start_offset": start,
                "end_offset": end,
                **identity,
            }
        )
        segment_texts.append(text)
        open_marker = None
    if open_marker is not None:
        raise ValueError("labeled-section begin has no matching end")

    selected_wikitext = "".join(segment_texts)
    if not selected_wikitext:
        raise ValueError("selected #lst dependency wikitext is empty")
    return {
        "total_section_marker_count": len(markers),
        "selected_label_marker_count": len(selected),
        "selected_segment_count": len(segments),
        "segments": segments,
        "selection_identity": _source_free_identity(selected_wikitext),
        "_selected_wikitext": selected_wikitext,
    }


def _source_revision_projection(manifest: Mapping[str, object]) -> dict[str, object]:
    identity = manifest.get("source_identity")
    assert isinstance(identity, dict)
    return {
        key: identity[key]
        for key in (
            "title",
            "page_id",
            "revision_id",
            "revision_timestamp",
            "mediawiki_sha1",
            "wikitext_sha256",
        )
    }


def build_lst_contract(
    parent_revision_manifest: Mapping[str, object],
    dependency_revision_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    """Freeze the exact Part 2 #lst selection and placement without source prose."""

    validate_revision_manifest(parent_revision_manifest)
    validate_revision_manifest(dependency_revision_manifest)
    if parent_revision_manifest.get("candidate_id") != PART2_CANDIDATE_ID:
        raise ValueError("unexpected Klim Samgin Part 2 candidate")
    if dependency_revision_manifest.get("candidate_id") != DEPENDENCY_CANDIDATE_ID:
        raise ValueError("unexpected Klim Samgin Part 2 dependency candidate")
    dependency_identity = dependency_revision_manifest.get("source_identity")
    assert isinstance(dependency_identity, dict)
    if dependency_identity.get("title") != DEPENDENCY_TITLE:
        raise ValueError("unexpected Klim Samgin #lst dependency title")

    parent_wikitext = _verified_wikitext(parent_revision_manifest, fetcher=fetcher)
    dependency_wikitext = _verified_wikitext(dependency_revision_manifest, fetcher=fetcher)
    invocation = parse_single_lst_invocation(parent_wikitext)
    if invocation["target_title"] != DEPENDENCY_TITLE:
        raise ValueError("Part 2 #lst target does not match the pinned dependency")

    selection = select_labeled_sections(
        dependency_wikitext,
        str(invocation["section_label"]),
    )
    selected_wikitext = selection.pop("_selected_wikitext")
    assert isinstance(selected_wikitext, str)
    if _LST_PREFIX_RE.search(dependency_wikitext):
        raise ValueError("nested #lst dependency requires an explicit additional source-graph pin")

    start = int(invocation["parent_start_offset"])
    end = int(invocation["parent_end_offset"])
    resolved_parent = parent_wikitext[:start] + selected_wikitext + parent_wikitext[end:]

    return {
        "contract_version": LST_CONTRACT_VERSION,
        "candidate_id": "gorky-klim-samgin-ru",
        "selection_profile": LST_SELECTION_PROFILE,
        "parent_revision": _source_revision_projection(parent_revision_manifest),
        "dependency_revision": _source_revision_projection(dependency_revision_manifest),
        "invocation": {
            **invocation,
            "range_end_label": None,
            "placement_semantics": "replace_exact_parent_invocation_with_all_matching_dependency_sections_in_source_order_without_added_separator",
        },
        "dependency_selection": selection,
        "resolved_parent_wikitext_identity": _source_free_identity(resolved_parent),
        "capture_scope": {
            "lst_labeled_section_selection_frozen": True,
            "lst_parent_placement_frozen": True,
            "resolved_part2_wikitext_identity_frozen": True,
            "literary_body_extraction_frozen": False,
            "composite_literary_body_identity_frozen": False,
            "source_text_committed": False,
        },
        "semantics_evidence": {
            "authority": "MediaWiki Labeled Section Transclusion documentation",
            "rule": "a simple #lst call includes every same-name labeled section; no range argument is used by this frozen invocation",
            "reference": "https://www.mediawiki.org/wiki/Extension:Labeled_Section_Transclusion/en",
        },
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "gate_ready": False,
        "m2_parity_admissible": False,
    }


def validate_lst_contract(
    contract: Mapping[str, object],
    *,
    parent_revision_manifest: Mapping[str, object] | None = None,
    dependency_revision_manifest: Mapping[str, object] | None = None,
) -> None:
    if contract.get("contract_version") != LST_CONTRACT_VERSION:
        raise ValueError("unsupported Klim Samgin #lst contract version")
    if contract.get("candidate_id") != "gorky-klim-samgin-ru":
        raise ValueError("unexpected Klim Samgin #lst contract candidate")
    if contract.get("selection_profile") != LST_SELECTION_PROFILE:
        raise ValueError("Klim Samgin #lst selection profile drift")
    invocation = contract.get("invocation")
    if not isinstance(invocation, dict):
        raise ValueError("Klim Samgin #lst invocation contract missing")
    if invocation.get("target_title") != DEPENDENCY_TITLE:
        raise ValueError("Klim Samgin #lst target drift")
    if not isinstance(invocation.get("section_label"), str) or not invocation["section_label"]:
        raise ValueError("Klim Samgin #lst section label missing")
    if invocation.get("range_end_label") is not None:
        raise ValueError("Klim Samgin frozen #lst invocation must not use a range")
    for key in ("parent_start_offset", "parent_end_offset"):
        if not isinstance(invocation.get(key), int) or int(invocation[key]) < 0:
            raise ValueError(f"invalid Klim Samgin #lst {key}")
    if int(invocation["parent_end_offset"]) <= int(invocation["parent_start_offset"]):
        raise ValueError("invalid Klim Samgin #lst parent placement")
    if invocation.get("placement_semantics") != (
        "replace_exact_parent_invocation_with_all_matching_dependency_sections_in_source_order_without_added_separator"
    ):
        raise ValueError("Klim Samgin #lst placement semantics drift")

    selection = contract.get("dependency_selection")
    if not isinstance(selection, dict):
        raise ValueError("Klim Samgin dependency selection missing")
    segments = selection.get("segments")
    if not isinstance(segments, list) or not segments:
        raise ValueError("Klim Samgin #lst selected segments missing")
    if selection.get("selected_segment_count") != len(segments):
        raise ValueError("Klim Samgin #lst selected-segment count drift")
    if selection.get("selected_label_marker_count") != len(segments) * 2:
        raise ValueError("Klim Samgin #lst marker-pair count drift")
    previous_end = -1
    for ordinal, segment in enumerate(segments, start=1):
        if not isinstance(segment, dict) or segment.get("ordinal") != ordinal:
            raise ValueError("Klim Samgin #lst segment order drift")
        start = segment.get("start_offset")
        end = segment.get("end_offset")
        if not isinstance(start, int) or not isinstance(end, int) or start < previous_end or end < start:
            raise ValueError("Klim Samgin #lst segment offsets invalid")
        for key in ("character_count", "utf8_byte_count"):
            if not isinstance(segment.get(key), int) or int(segment[key]) < 0:
                raise ValueError(f"invalid Klim Samgin #lst segment {key}")
        digest = segment.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError("invalid Klim Samgin #lst segment SHA-256")
        previous_end = end
    identity = selection.get("selection_identity")
    if not isinstance(identity, dict):
        raise ValueError("Klim Samgin selection_identity missing")
    for key in ("character_count", "utf8_byte_count"):
        if not isinstance(identity.get(key), int) or int(identity[key]) <= 0:
            raise ValueError(f"invalid Klim Samgin selection_identity {key}")
    digest = identity.get("sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ValueError("invalid Klim Samgin selection_identity SHA-256")
    resolved = contract.get("resolved_parent_wikitext_identity")
    if not isinstance(resolved, dict):
        raise ValueError("Klim Samgin resolved Part 2 identity missing")
    for key in ("character_count", "utf8_byte_count"):
        if not isinstance(resolved.get(key), int) or int(resolved[key]) <= 0:
            raise ValueError(f"invalid Klim Samgin resolved Part 2 {key}")
    if not isinstance(resolved.get("sha256"), str) or len(str(resolved["sha256"])) != 64:
        raise ValueError("invalid Klim Samgin resolved Part 2 SHA-256")

    expected_scope = {
        "lst_labeled_section_selection_frozen": True,
        "lst_parent_placement_frozen": True,
        "resolved_part2_wikitext_identity_frozen": True,
        "literary_body_extraction_frozen": False,
        "composite_literary_body_identity_frozen": False,
        "source_text_committed": False,
    }
    if contract.get("capture_scope") != expected_scope:
        raise ValueError("Klim Samgin #lst capture scope drift")
    if contract.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source identity must remain unknown")
    if contract.get("diagnostic_ready") is not False:
        raise ValueError("Klim Samgin body diagnostic must remain disabled")
    if contract.get("gate_ready") is not False:
        raise ValueError("Klim Samgin gate readiness must remain false")
    if contract.get("m2_parity_admissible") is not False:
        raise ValueError("Klim Samgin #lst freezing cannot advance M2")

    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(contract):
        raise ValueError("source prose leaked into Klim Samgin #lst contract")

    if parent_revision_manifest is not None:
        validate_revision_manifest(parent_revision_manifest)
        if contract.get("parent_revision") != _source_revision_projection(parent_revision_manifest):
            raise ValueError("Klim Samgin #lst parent revision identity drift")
    if dependency_revision_manifest is not None:
        validate_revision_manifest(dependency_revision_manifest)
        if contract.get("dependency_revision") != _source_revision_projection(dependency_revision_manifest):
            raise ValueError("Klim Samgin #lst dependency revision identity drift")


def replay_lst_contract(
    parent_revision_manifest: Mapping[str, object],
    dependency_revision_manifest: Mapping[str, object],
    contract: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    validate_lst_contract(
        contract,
        parent_revision_manifest=parent_revision_manifest,
        dependency_revision_manifest=dependency_revision_manifest,
    )
    observed = build_lst_contract(
        parent_revision_manifest,
        dependency_revision_manifest,
        fetcher=fetcher,
    )
    if observed != contract:
        raise ValueError("pinned Klim Samgin #lst selection/placement identity drift")
    selection = contract["dependency_selection"]
    resolved = contract["resolved_parent_wikitext_identity"]
    assert isinstance(selection, dict) and isinstance(resolved, dict)
    selection_identity = selection["selection_identity"]
    assert isinstance(selection_identity, dict)
    return {
        "receipt_version": "scriptorium-klim-samgin-lst-replay-v1",
        "candidate_id": contract["candidate_id"],
        "selection_profile": LST_SELECTION_PROFILE,
        "selected_segment_count": selection["selected_segment_count"],
        "selection_sha256": selection_identity["sha256"],
        "resolved_part2_wikitext_sha256": resolved["sha256"],
        "verified": True,
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def probe_revision_shape(revision_manifest: Mapping[str, object]) -> dict[str, object]:
    """Return source-free markup/dependency inventory for one pinned revision."""

    wikitext = _verified_wikitext(revision_manifest, fetcher=fetch_pinned_wikitext)
    source_identity = revision_manifest.get("source_identity")
    assert isinstance(source_identity, dict)
    revision_id = source_identity["revision_id"]

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
        description="Probe or freeze the pinned Klim Samgin source graph without emitting source prose."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    probe = subparsers.add_parser("probe")
    probe.add_argument("--revision-manifest", type=Path, required=True)

    capture = subparsers.add_parser("capture-lst")
    capture.add_argument("--parent-revision-manifest", type=Path, required=True)
    capture.add_argument("--dependency-revision-manifest", type=Path, required=True)
    capture.add_argument("--output", type=Path, required=True)

    replay = subparsers.add_parser("replay-lst")
    replay.add_argument("--parent-revision-manifest", type=Path, required=True)
    replay.add_argument("--dependency-revision-manifest", type=Path, required=True)
    replay.add_argument("--contract", type=Path, required=True)
    replay.add_argument("--receipt", type=Path)

    args = parser.parse_args(argv)
    if args.command == "probe":
        result = probe_revision_shape(_load_json(args.revision_manifest))
        print(
            "SCRIPTORIUM_KLIM_SHAPE="
            + json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        )
        return 0

    parent = _load_json(args.parent_revision_manifest)
    dependency = _load_json(args.dependency_revision_manifest)
    if args.command == "capture-lst":
        contract = build_lst_contract(parent, dependency)
        validate_lst_contract(
            contract,
            parent_revision_manifest=parent,
            dependency_revision_manifest=dependency,
        )
        _write_json(args.output, contract)
        return 0

    contract = _load_json(args.contract)
    receipt = replay_lst_contract(parent, dependency, contract)
    if args.receipt is not None:
        _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
