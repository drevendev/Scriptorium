"""Freeze a source-free composition-membership decision for Twelve Chairs scan gaps.

The 1928 Zemlya i Fabrika route already freezes 410 Page-namespace dependencies plus a
source-free audit of four scan-index gaps outside those canonical part routes. This module
binds those two evidence surfaces and decides only whether the four gap pages participate
in the current Scriptorium composition surface. It does not classify printed-page content,
render Page wikitext, compose literary prose, or advance corpus/FantLab gates.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping, Sequence

from .twelve_chairs_gap_audit import GAP_SEQUENCES, validate_gap_audit_manifest
from .twelve_chairs_page_freeze import (
    CANDIDATE_ID,
    EXPECTED_PAGE_COUNT,
    FAMILY_ID,
    INDEX_VERSION,
    NON_TRANSCLUDED_GAPS,
    PAGE_RANGES,
    expected_page_sequences,
    load_sharded_manifest,
)

DECISION_VERSION = "scriptorium-twelve-chairs-gap-membership-v1"
COMPOSITION_SURFACE = "scriptorium-twelve-chairs-zif-1928-canonical-part-routes-v1"


def _load_object(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def _gap_decisions(gap_manifest: Mapping[str, object]) -> list[dict[str, object]]:
    rows = validate_gap_audit_manifest(gap_manifest)
    if tuple(int(row["page_sequence"]) for row in rows) != GAP_SEQUENCES:
        raise ValueError("gap audit sequence order drift")

    dependencies = set(expected_page_sequences())
    decisions: list[dict[str, object]] = []
    for row in rows:
        sequence = int(row["page_sequence"])
        if sequence in dependencies:
            raise ValueError(f"gap page {sequence} entered frozen dependency inventory")
        body_class = str(row["body_presence_class"])
        if body_class == "nonempty_body_unclassified":
            rationale = "nonempty_but_not_transcluded_by_frozen_canonical_part_routes"
        elif body_class == "no_transcluded_body":
            rationale = "no_transcluded_body_and_not_transcluded_by_frozen_canonical_part_routes"
        else:
            raise ValueError(f"unsupported gap body-presence class: {body_class}")
        decisions.append(
            {
                "page_sequence": sequence,
                "revision_id": int(row["revision_id"]),
                "mediawiki_sha1": str(row["mediawiki_sha1"]),
                "body_presence_class": body_class,
                "transcluded_body_sha256": str(row["transcluded_body_sha256"]),
                "composition_membership": "excluded",
                "rationale": rationale,
                "semantic_literary_classification": "not_claimed",
            }
        )
    return decisions


def build_decision(
    *, index_path: Path, gap_audit_path: Path
) -> dict[str, object]:
    """Build the exact source-free gap-membership decision from frozen evidence."""

    rows = load_sharded_manifest(index_path)
    sequences = tuple(int(row["page_sequence"]) for row in rows)
    if sequences != expected_page_sequences() or len(rows) != EXPECTED_PAGE_COUNT:
        raise ValueError("decision input must be the exact frozen 410-Page inventory")

    index = _load_object(index_path)
    if index.get("manifest_version") != INDEX_VERSION:
        raise ValueError("unexpected Page revision manifest version")
    if index.get("candidate_id") != CANDIDATE_ID or index.get("family_id") != FAMILY_ID:
        raise ValueError("Page revision manifest candidate/family mismatch")
    topology = index.get("topology_contract")
    expected_topology = {
        "ranges": [list(item) for item in PAGE_RANGES],
        "non_transcluded_gaps": [list(item) for item in NON_TRANSCLUDED_GAPS],
    }
    if topology != expected_topology:
        raise ValueError("Page revision topology drift")

    gap_manifest = _load_object(gap_audit_path)
    decisions = _gap_decisions(gap_manifest)
    if {int(item["page_sequence"]) for item in decisions} & set(sequences):
        raise AssertionError("excluded gap decision overlaps frozen dependency inventory")

    return {
        "decision_version": DECISION_VERSION,
        "candidate_id": CANDIDATE_ID,
        "family_id": FAMILY_ID,
        "source_text_included": False,
        "composition_surface": COMPOSITION_SURFACE,
        "decision_basis": (
            "The three frozen canonical part routes define the current composition surface. "
            "Pages outside those routes remain excluded even when their audited Page body is "
            "nonempty; body presence alone is not evidence of literary membership."
        ),
        "source_revision_anchor": {
            "manifest_version": INDEX_VERSION,
            "page_identity_count": EXPECTED_PAGE_COUNT,
            "topology_contract": expected_topology,
            "shards": index.get("shards"),
        },
        "gap_audit_anchor": {
            "manifest_version": gap_manifest.get("manifest_version"),
            "captured_at_utc": gap_manifest.get("captured_at_utc"),
            "dependency_inventory_unchanged": gap_manifest.get("dependency_inventory_unchanged"),
        },
        "decisions": decisions,
        "dependency_inventory_unchanged": True,
        "literary_dependency_count": EXPECTED_PAGE_COUNT,
        "gap_membership_frozen": True,
        "literary_body_composition_frozen": False,
        "page_body_rendering_profile_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "gate_ready": False,
        "m2_parity_admissible": False,
    }


def validate_decision(
    decision: Mapping[str, object], *, index_path: Path, gap_audit_path: Path
) -> None:
    expected = build_decision(index_path=index_path, gap_audit_path=gap_audit_path)
    if dict(decision) != expected:
        raise ValueError("Twelve Chairs gap membership decision drift")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--gap-audit", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    decision = build_decision(index_path=args.index, gap_audit_path=args.gap_audit)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(decision, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(decision, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
