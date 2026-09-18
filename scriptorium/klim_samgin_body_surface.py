"""Freeze source-free extraction prerequisites for the pinned Klim Samgin parts.

This module intentionally stops before literary-body extraction.  It replays the four
pinned Russian Wikisource revisions, inventories only the markup shapes that an
extractor must handle, and proves a subtle Part 2 boundary: target-only ``#lst``
substitution cannot remove the two direct parent-level ``poemx1`` calls because both
calls sit outside the frozen ``#lst`` span.

The artifact stores structural names, counts, offsets and cryptographic identities,
never literary prose.  It exists to keep the next body-extraction patch fail-closed
rather than silently treating the target-only Part 2 reconstruction as template-free.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .klim_samgin_freeze import LST_CONTRACT_VERSION
from .mediawiki_template_invocation import find_template_invocations
from .single_page_body import fetch_pinned_wikitext
from .single_page_revision import validate_manifest as validate_revision_manifest


MANIFEST_VERSION = "scriptorium-klim-samgin-body-extraction-surface-v1"
PROFILE_VERSION = "scriptorium-klim-samgin-pre-extraction-structural-surface-v1"
CANDIDATE_ID = "gorky-klim-samgin-ru"
EXPECTED_PART_REVISION_IDS = {1: 5733765, 2: 5198033, 3: 5138882, 4: 5724453}
EXPECTED_DIRECT_POEMX1_COUNTS = {1: 5, 2: 2, 3: 0, 4: 0}

_TEMPLATE_NAME_RE = re.compile(r"\{\{\s*([^|{}\n]+)")
_HTML_TAG_NAME_RE = re.compile(r"</?\s*([A-Za-z][A-Za-z0-9]*)\b")
_HEADING_RE = re.compile(r"(?m)^(={2,6})\s*.*?\s*\1\s*$")
_CATEGORY_RE = re.compile(r"(?mi)^\s*\[\[\s*(?:Категория|Category)\s*:")
_TABLE_START_RE = re.compile(r"(?m)^\s*\{\|")
_TABLE_END_RE = re.compile(r"(?m)^\s*\|\}")


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


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _verified_wikitext(
    revision_manifest: Mapping[str, object],
    *,
    expected_part: int,
    fetcher: Callable[..., dict[str, object]],
) -> tuple[str, Mapping[str, object]]:
    validate_revision_manifest(revision_manifest)
    expected_candidate = f"{CANDIDATE_ID}-part-{expected_part}"
    if revision_manifest.get("candidate_id") != expected_candidate:
        raise ValueError(f"unexpected candidate for Klim part {expected_part}")
    identity = revision_manifest.get("source_identity")
    if not isinstance(identity, Mapping):
        raise ValueError("revision source identity missing")
    if identity.get("revision_id") != EXPECTED_PART_REVISION_IDS[expected_part]:
        raise ValueError(f"unexpected revision for Klim part {expected_part}")
    title = identity.get("title")
    revision_id = identity.get("revision_id")
    if not isinstance(title, str) or not isinstance(revision_id, int):
        raise ValueError("revision source identity incomplete")
    observed = fetcher(title=title, revision_id=revision_id)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient pinned wikitext missing")
    if observed != dict(identity):
        differing = sorted(
            key
            for key in set(observed) | set(identity)
            if observed.get(key) != identity.get(key)
        )
        raise ValueError(f"pinned Klim part {expected_part} identity drift: {differing}")
    return wikitext, identity


def _analyze_part(
    *,
    part: int,
    wikitext: str,
    source_identity: Mapping[str, object],
) -> dict[str, object]:
    if part not in EXPECTED_PART_REVISION_IDS:
        raise ValueError("Klim part must be 1..4")
    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    if _sha256_text(wikitext) != source_identity.get("wikitext_sha256"):
        raise ValueError(f"Klim part {part} wikitext digest drift")

    templates = Counter(match.group(1).strip() for match in _TEMPLATE_NAME_RE.finditer(wikitext))
    tags = Counter(match.group(1).casefold() for match in _HTML_TAG_NAME_RE.finditer(wikitext))
    headings = Counter(len(match.group(1)) for match in _HEADING_RE.finditer(wikitext))
    poemx1 = find_template_invocations(wikitext, template_name="poemx1")
    if len(poemx1) != EXPECTED_DIRECT_POEMX1_COUNTS[part]:
        raise ValueError(
            f"Klim part {part} direct poemx1 inventory drift: {len(poemx1)}"
        )

    return {
        "part": part,
        "source_revision": {
            "title": source_identity["title"],
            "revision_id": source_identity["revision_id"],
            "wikitext_sha256": source_identity["wikitext_sha256"],
        },
        "wikitext_character_count": len(wikitext),
        "wikitext_utf8_byte_count": len(wikitext.encode("utf-8")),
        "template_name_counts": dict(sorted(templates.items())),
        "html_tag_name_counts": dict(sorted(tags.items())),
        "heading_level_counts": {
            str(level): count for level, count in sorted(headings.items())
        },
        "category_link_count": len(_CATEGORY_RE.findall(wikitext)),
        "table_start_count": len(_TABLE_START_RE.findall(wikitext)),
        "table_end_count": len(_TABLE_END_RE.findall(wikitext)),
        "direct_poemx1_invocation_count": len(poemx1),
        "direct_poemx1_invocations": poemx1,
        "source_text_included": False,
    }


def _part2_substitution_boundary(
    part2_row: Mapping[str, object],
    lst_contract: Mapping[str, object],
) -> dict[str, object]:
    if lst_contract.get("contract_version") != LST_CONTRACT_VERSION:
        raise ValueError("unexpected Klim Part 2 #lst contract version")
    invocation = lst_contract.get("invocation")
    if not isinstance(invocation, Mapping):
        raise ValueError("Klim Part 2 #lst invocation missing")
    if invocation.get("argument_count") != 1 or invocation.get("section_label") is not None:
        raise ValueError("Klim Part 2 #lst call is no longer target-only")
    lst_start = invocation.get("parent_start_offset")
    lst_end = invocation.get("parent_end_offset")
    if not isinstance(lst_start, int) or not isinstance(lst_end, int) or lst_end <= lst_start:
        raise ValueError("invalid Klim Part 2 #lst span")

    poem_rows = part2_row.get("direct_poemx1_invocations")
    if not isinstance(poem_rows, list) or len(poem_rows) != EXPECTED_DIRECT_POEMX1_COUNTS[2]:
        raise ValueError("unexpected Part 2 direct poemx1 rows")
    outside: list[dict[str, object]] = []
    for row in poem_rows:
        if not isinstance(row, Mapping):
            raise ValueError("invalid direct poemx1 row")
        start = row.get("parent_start_offset")
        end = row.get("parent_end_offset")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("direct poemx1 offsets missing")
        overlaps = start < lst_end and end > lst_start
        if overlaps:
            raise ValueError("direct parent poemx1 unexpectedly overlaps target-only #lst span")
        outside.append(
            {
                "invocation_index": row["invocation_index"],
                "parent_start_offset": start,
                "parent_end_offset": end,
                "invocation_sha256": row["invocation_sha256"],
            }
        )

    return {
        "lst_parent_start_offset": lst_start,
        "lst_parent_end_offset": lst_end,
        "lst_invocation_sha256": invocation["invocation_sha256"],
        "direct_parent_poemx1_count": len(outside),
        "direct_parent_poemx1_outside_lst_span": outside,
        "target_only_lst_substitution_preserves_direct_parent_poemx1": True,
        "resolved_target_substitution_is_not_a_template_free_parent_claim": True,
    }


def build_body_surface_manifest(
    revision_manifests: Sequence[Mapping[str, object]],
    lst_contract: Mapping[str, object],
    *,
    research_date: str,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    if len(revision_manifests) != 4:
        raise ValueError("exactly four Klim part revision manifests are required")
    if not isinstance(research_date, str) or not research_date:
        raise ValueError("research_date must be non-empty")

    rows: list[dict[str, object]] = []
    for part, revision_manifest in enumerate(revision_manifests, start=1):
        wikitext, identity = _verified_wikitext(
            revision_manifest, expected_part=part, fetcher=fetcher
        )
        rows.append(_analyze_part(part=part, wikitext=wikitext, source_identity=identity))

    part2_boundary = _part2_substitution_boundary(rows[1], lst_contract)
    aggregate_templates: Counter[str] = Counter()
    aggregate_tags: Counter[str] = Counter()
    for row in rows:
        aggregate_templates.update(row["template_name_counts"])
        aggregate_tags.update(row["html_tag_name_counts"])

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "research_date": research_date,
        "profile": PROFILE_VERSION,
        "parts": rows,
        "aggregate_template_name_counts": dict(sorted(aggregate_templates.items())),
        "aggregate_html_tag_name_counts": dict(sorted(aggregate_tags.items())),
        "part2_target_substitution_boundary": part2_boundary,
        "capture_scope": {
            "four_part_pinned_source_structural_surface_frozen": True,
            "direct_parent_poemx1_invocation_surfaces_frozen": True,
            "part2_target_substitution_residual_parent_template_boundary_frozen": True,
            "literary_body_extraction_frozen": False,
            "literary_composition_frozen": False,
            "composite_literary_body_identity_frozen": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This artifact freezes only source-free extraction prerequisites for the four pinned "
            "Klim Samgin parent revisions. In particular, two direct parent-level poemx1 calls sit "
            "outside the Part 2 target-only #lst span and therefore survive that substitution. "
            "No literary-body extraction, four-part composition, historical render equivalence, "
            "FantLab source identity, or parity movement is claimed."
        ),
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "gate_ready": False,
        "m2_parity_admissible": False,
    }


def validate_body_surface_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Klim body extraction surface manifest")
    if manifest.get("candidate_id") != CANDIDATE_ID or manifest.get("profile") != PROFILE_VERSION:
        raise ValueError("unexpected Klim body extraction surface identity")
    parts = manifest.get("parts")
    if not isinstance(parts, list) or len(parts) != 4:
        raise ValueError("Klim body surface must contain four parts")
    for part, row in enumerate(parts, start=1):
        if not isinstance(row, Mapping) or row.get("part") != part:
            raise ValueError("Klim body-surface part order drift")
        source = row.get("source_revision")
        if not isinstance(source, Mapping) or source.get("revision_id") != EXPECTED_PART_REVISION_IDS[part]:
            raise ValueError(f"Klim part {part} revision drift")
        if row.get("direct_poemx1_invocation_count") != EXPECTED_DIRECT_POEMX1_COUNTS[part]:
            raise ValueError(f"Klim part {part} direct poemx1 count drift")
        if row.get("source_text_included") is not False:
            raise ValueError("source text flag must remain false")

    boundary = manifest.get("part2_target_substitution_boundary")
    if not isinstance(boundary, Mapping):
        raise ValueError("Part 2 substitution boundary missing")
    if boundary.get("direct_parent_poemx1_count") != 2:
        raise ValueError("Part 2 direct parent poemx1 count drift")
    if boundary.get("target_only_lst_substitution_preserves_direct_parent_poemx1") is not True:
        raise ValueError("Part 2 residual-parent boundary must remain explicit")
    if boundary.get("resolved_target_substitution_is_not_a_template_free_parent_claim") is not True:
        raise ValueError("Part 2 target-substitution claim boundary drift")

    scope = manifest.get("capture_scope")
    if not isinstance(scope, Mapping):
        raise ValueError("Klim body surface capture scope missing")
    if scope.get("four_part_pinned_source_structural_surface_frozen") is not True:
        raise ValueError("four-part structural surface must be frozen")
    if scope.get("literary_body_extraction_frozen") is not False:
        raise ValueError("literary-body extraction must remain unresolved")
    if scope.get("literary_composition_frozen") is not False:
        raise ValueError("literary composition must remain unresolved")
    if scope.get("composite_literary_body_identity_frozen") is not False:
        raise ValueError("composite body identity must remain unresolved")
    if scope.get("historical_render_equivalence_proven") is not False:
        raise ValueError("historical render equivalence must remain unproven")
    if scope.get("source_text_committed") is not False or manifest.get("source_text_included") is not False:
        raise ValueError("source prose must not be persisted")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source identity must remain unknown")
    if manifest.get("diagnostic_ready") is not False or manifest.get("gate_ready") is not False:
        raise ValueError("body surface alone cannot open diagnostic/gate")
    if manifest.get("m2_parity_admissible") is not False:
        raise ValueError("body surface alone cannot advance M2")

    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(manifest):
        raise ValueError("source prose key leaked into Klim body-surface manifest")


def replay_body_surface_manifest(
    revision_manifests: Sequence[Mapping[str, object]],
    lst_contract: Mapping[str, object],
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    validate_body_surface_manifest(manifest)
    observed = build_body_surface_manifest(
        revision_manifests,
        lst_contract,
        research_date=str(manifest["research_date"]),
        fetcher=fetcher,
    )
    if observed != dict(manifest):
        raise ValueError("pinned Klim body extraction surface drift")
    boundary = manifest["part2_target_substitution_boundary"]
    assert isinstance(boundary, Mapping)
    return {
        "receipt_version": "scriptorium-klim-samgin-body-extraction-surface-replay-v1",
        "candidate_id": CANDIDATE_ID,
        "verified": True,
        "direct_parent_poemx1_counts": [
            EXPECTED_DIRECT_POEMX1_COUNTS[index] for index in range(1, 5)
        ],
        "part2_residual_direct_parent_poemx1_count": boundary["direct_parent_poemx1_count"],
        "source_text_included": False,
        "literary_body_extraction_frozen": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Freeze or replay Klim Samgin literary-body extraction prerequisites."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("capture", "replay"):
        sub = subparsers.add_parser(name)
        for part in range(1, 5):
            sub.add_argument(f"--part{part}-revision-manifest", type=Path, required=True)
        sub.add_argument("--lst-contract", type=Path, required=True)
        if name == "capture":
            sub.add_argument("--research-date", required=True)
            sub.add_argument("--output", type=Path, required=True)
        else:
            sub.add_argument("--manifest", type=Path, required=True)
            sub.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)

    revisions = [
        _load_json(getattr(args, f"part{part}_revision_manifest"))
        for part in range(1, 5)
    ]
    lst_contract = _load_json(args.lst_contract)
    if args.command == "capture":
        manifest = build_body_surface_manifest(
            revisions,
            lst_contract,
            research_date=args.research_date,
        )
        validate_body_surface_manifest(manifest)
        _write_json(args.output, manifest)
        return 0

    manifest = _load_json(args.manifest)
    receipt = replay_body_surface_manifest(revisions, lst_contract, manifest)
    if args.receipt is not None:
        _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
