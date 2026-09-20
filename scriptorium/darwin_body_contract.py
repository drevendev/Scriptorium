"""Freeze the source-free literary-body composition contract for Darwin/Rachinsky 1864.

This unit selects which already-frozen ProofreadPage revision identities are inputs to the
literary body. It deliberately does not fetch or serialize Page wikitext, render prose,
compute body counts/digests, or advance corpus/FantLab gates.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from .darwin_page_freeze import (
    CANDIDATE_ID,
    EXPLICIT_NO_TEXT_NON_DEPENDENCIES,
    FAMILY_ID,
    PARENT_RANGES,
    ROUTE_RANGES,
    expected_page_sequences,
)
from .darwin_page_shards import INDEX_VERSION, load_sharded_manifest

CONTRACT_VERSION = "scriptorium-darwin-literary-body-contract-v1"
COMPOSITION_PROFILE = "scriptorium-darwin-numbered-routes-1-through-14-v1"
LITERARY_ROUTE_COUNT = 14
EXPECTED_LITERARY_PAGE_COUNT = 388
EXPECTED_APPARATUS_PAGE_COUNT = 30


def _expand_range(start: int, end: int, excluded: Sequence[int] = ()) -> tuple[int, ...]:
    blocked = set(excluded)
    return tuple(page for page in range(start, end + 1) if page not in blocked)


def literary_page_sequences() -> tuple[int, ...]:
    """Return exact Page-sequence dependencies for rendered routes /1 through /14."""

    numbered = ROUTE_RANGES[:LITERARY_ROUTE_COUNT]
    sequences = tuple(
        page
        for start, end, excluded in numbered
        for page in _expand_range(start, end, excluded)
    )
    if len(sequences) != EXPECTED_LITERARY_PAGE_COUNT:
        raise AssertionError(
            f"literary topology drift: expected {EXPECTED_LITERARY_PAGE_COUNT}, got {len(sequences)}"
        )
    if tuple(sorted(sequences)) != sequences or len(set(sequences)) != len(sequences):
        raise AssertionError("literary Page sequence order is not strictly increasing and unique")
    return sequences


def apparatus_page_sequences() -> tuple[int, ...]:
    """Return frozen dependencies intentionally excluded from literary composition."""

    frozen = set(expected_page_sequences())
    literary = set(literary_page_sequences())
    apparatus = tuple(sorted(frozen - literary))

    index_start, index_end, index_excluded = ROUTE_RANGES[LITERARY_ROUTE_COUNT]
    expected = {
        page
        for start, end in PARENT_RANGES
        for page in range(start, end + 1)
    }
    expected.update(_expand_range(index_start, index_end, index_excluded))
    if set(apparatus) != expected:
        raise AssertionError("apparatus partition drifted from parent-only plus alphabetical-index topology")
    if len(apparatus) != EXPECTED_APPARATUS_PAGE_COUNT:
        raise AssertionError(
            f"apparatus topology drift: expected {EXPECTED_APPARATUS_PAGE_COUNT}, got {len(apparatus)}"
        )
    return apparatus


def _canonical_identity_rows(rows: Sequence[Mapping[str, object]]) -> str:
    allowed = {"page_sequence", "title", "revision_id", "timestamp", "mediawiki_sha1"}
    normalized: list[list[object]] = []
    for row in rows:
        if set(row) != allowed:
            raise ValueError("Page identity row shape drift or source payload key detected")
        sequence = row.get("page_sequence")
        revid = row.get("revision_id")
        title = row.get("title")
        timestamp = row.get("timestamp")
        mediawiki_sha1 = row.get("mediawiki_sha1")
        if not isinstance(sequence, int) or not isinstance(revid, int):
            raise ValueError("invalid Page sequence or revision ID")
        if not all(isinstance(value, str) for value in (title, timestamp, mediawiki_sha1)):
            raise ValueError("incomplete Page identity row")
        normalized.append([sequence, title, revid, timestamp, mediawiki_sha1])
    return json.dumps(normalized, ensure_ascii=False, separators=(",", ":"))


def build_contract(
    rows: Sequence[Mapping[str, object]], *, index_sha256: str
) -> dict[str, object]:
    """Build a machine-checkable source-free selection/composition contract."""

    frozen_sequences = tuple(int(row["page_sequence"]) for row in rows)
    if frozen_sequences != expected_page_sequences():
        raise ValueError("contract input must be the exact frozen 418-Page identity inventory")
    if len(index_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in index_sha256):
        raise ValueError("index_sha256 must be a lowercase SHA-256 hex digest")

    literary = literary_page_sequences()
    apparatus = apparatus_page_sequences()
    if set(literary) & set(apparatus):
        raise AssertionError("literary/apparatus partitions overlap")
    if set(literary) | set(apparatus) != set(frozen_sequences):
        raise AssertionError("literary/apparatus partitions do not cover all frozen dependencies")
    if any(page in frozen_sequences for page in EXPLICIT_NO_TEXT_NON_DEPENDENCIES):
        raise AssertionError("source-declared no-text non-dependency entered frozen inventory")

    identity_sha256 = sha256(_canonical_identity_rows(rows).encode("utf-8")).hexdigest()
    numbered_route_specs = [
        {"route": str(index), "from": start, "to": end, "excluded": list(excluded)}
        for index, (start, end, excluded) in enumerate(
            ROUTE_RANGES[:LITERARY_ROUTE_COUNT], start=1
        )
    ]
    index_start, index_end, index_excluded = ROUTE_RANGES[LITERARY_ROUTE_COUNT]
    parent_specs = [
        {"from": start, "to": end, "count": end - start + 1}
        for start, end in PARENT_RANGES
    ]

    return {
        "contract_version": CONTRACT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "family_id": FAMILY_ID,
        "source_revision_manifest_version": INDEX_VERSION,
        "source_revision_index_sha256": index_sha256,
        "source_identity_set_sha256": identity_sha256,
        "frozen_dependency_count": len(frozen_sequences),
        "source_text_included": False,
        "composition": {
            "profile": COMPOSITION_PROFILE,
            "selection": "rendered numbered routes /1 through /14 only",
            "order": "ascending frozen Page sequence in rendered route order",
            "separator": "deferred_until_body_rendering_contract",
            "literary_dependency_count": len(literary),
            "numbered_routes": numbered_route_specs,
            "apparatus_excluded": {
                "parent_only_ranges": parent_specs,
                "alphabetical_index_route": {
                    "route": "Указатель",
                    "from": index_start,
                    "to": index_end,
                    "excluded": list(index_excluded),
                },
                "apparatus_dependency_count": len(apparatus),
            },
            "explicit_no_text_non_dependencies": list(EXPLICIT_NO_TEXT_NON_DEPENDENCIES),
        },
        "extraction_boundary": {
            "exact_revision_identity_required_before_content_fetch": True,
            "content_fetch_mode": "transient exact-revision MediaWiki main-slot content only",
            "persist_source_wikitext": False,
            "persist_rendered_prose": False,
            "page_body_rendering_profile": "not_frozen_in_this_contract",
            "fail_closed_on_identity_or_topology_drift": True,
        },
        "deferred_gates": {
            "literary_body_rendering_profile_frozen": False,
            "literary_body_count_and_digests_frozen": False,
            "minimum_300k_proved": False,
            "independent_scan_sha256_frozen": False,
        },
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "gate_ready": False,
        "m2_parity_admissible": False,
    }


def validate_contract(
    contract: Mapping[str, object], rows: Sequence[Mapping[str, object]], *, index_sha256: str
) -> None:
    expected = build_contract(rows, index_sha256=index_sha256)
    if dict(contract) != expected:
        raise ValueError("Darwin literary-body composition contract drift")


def build_contract_from_index(index_path: Path) -> dict[str, object]:
    rows = load_sharded_manifest(index_path)
    return build_contract(rows, index_sha256=sha256(index_path.read_bytes()).hexdigest())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    contract = build_contract_from_index(args.index)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(contract, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
