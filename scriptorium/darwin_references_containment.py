"""Probe Darwin/Rachinsky <references/> containment without persisting source text.

The frozen render-surface inventory counts raw tag shapes before non-transcluded
<noinclude> regions are removed. This probe replays the exact pinned literary Page
revisions, identity-checks them through the existing fetcher, and proves whether the
observed self-closing <references/> shape survives the already-defined noinclude strip.

It deliberately does not implement Cite semantics and does not promote the render
profile/backlog rule. The durable output is aggregate and source-free.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
import re
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from .darwin_body_contract import literary_page_sequences
from .darwin_page_shards import load_sharded_manifest
from .darwin_render_surface import (
    _NOINCLUDE_BLOCK_RE,
    _TAG_RE,
    _strip_nontranscluded_regions,
    fetch_pinned_literary_wikitext,
)

CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
PROBE_SCHEMA = "scriptorium-darwin-references-containment-probe-v1"
EXPECTED_LITERARY_PAGE_COUNT = 388
EXPECTED_REFERENCES_COUNT = 388
SOURCE_REVISION_INDEX_SHA256 = "a1b1011095dc84ab0a5cd3ef45b2a46ce99588a0ef9cf507c1f711c925ba86dd"
RENDER_SURFACE_SCHEMA = "scriptorium-darwin-render-surface-freeze-v1"
RENDER_SURFACE_SHA256 = "e5ae625fef6afb2e890de990e1ef3b9e108a409a2e0ea2136947c2c3e1cea44d"
PROFILE_PROMOTION_SCHEMA = "scriptorium-darwin-render-profile-yo-promotion-v1"
PROFILE_PROMOTION_SHA256 = "153f6ceb89025da90971ddc265df680359ff498103bb47ecd68f86bb3205ed28"
BACKLOG_SCHEMA = "scriptorium-darwin-render-semantic-backlog-v2"
BACKLOG_SHA256 = "6d4ba2bb9ec78731d97d91c87d0628207ec880901e9d388fa7aa7c70fb20e3be"


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _self_digest(value: Mapping[str, object], field: str) -> str:
    unsigned = deepcopy(dict(value))
    unsigned.pop(field, None)
    return _sha256_json(unsigned)


def _tag_kind(match: re.Match[str]) -> str:
    suffix = match.group(3).rstrip()
    if match.group(1):
        return "close"
    return "self_closing" if suffix.endswith("/") else "open"


def audit_reference_containment(wikitext: str) -> dict[str, int | bool]:
    """Count raw <references/> tags and prove their noinclude containment."""

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")

    # Reuse the frozen renderer's fail-closed noinclude parser to reject unbalanced
    # non-transcluded markup before interpreting containment spans.
    _strip_nontranscluded_regions(wikitext)

    noinclude_spans = [(match.start(), match.end()) for match in _NOINCLUDE_BLOCK_RE.finditer(wikitext)]
    references = []
    for match in _TAG_RE.finditer(wikitext):
        if match.group(2).lower() != "references":
            continue
        kind = _tag_kind(match)
        if kind != "self_closing":
            raise ValueError(f"unexpected non-self-closing <references> tag: {kind}")
        references.append((match.start(), match.end()))

    inside = sum(
        any(block_start <= start and end <= block_end for block_start, block_end in noinclude_spans)
        for start, end in references
    )
    total = len(references)
    outside = total - inside
    return {
        "references_total": total,
        "references_inside_noinclude": inside,
        "references_outside_noinclude": outside,
        "all_observed_references_inside_noinclude": total > 0 and outside == 0,
    }


def _load_object(path: Path, *, label: str) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Darwin {label} must be a JSON object")
    return value


def _verify_predecessors(
    surface: Mapping[str, object],
    promotion: Mapping[str, object],
    backlog: Mapping[str, object],
) -> None:
    if surface.get("schema_version") != RENDER_SURFACE_SCHEMA:
        raise ValueError("Darwin render-surface schema drift")
    if surface.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin render-surface candidate drift")
    if surface.get("freeze_manifest_sha256") != RENDER_SURFACE_SHA256:
        raise ValueError("Darwin render-surface identity drift")
    if surface.get("source_revision_index_sha256") != SOURCE_REVISION_INDEX_SHA256:
        raise ValueError("Darwin render-surface source-index drift")
    if surface.get("literary_dependency_count") != EXPECTED_LITERARY_PAGE_COUNT:
        raise ValueError("Darwin render-surface literary dependency drift")

    tag_shapes = surface.get("tag_shapes")
    if not isinstance(tag_shapes, list):
        raise ValueError("Darwin render-surface tag inventory missing")
    reference_shapes = [
        row for row in tag_shapes
        if isinstance(row, dict) and str(row.get("name", "")).lower() == "references"
    ]
    expected_shape = {"count": EXPECTED_REFERENCES_COUNT, "kind": "self_closing", "name": "references"}
    if reference_shapes != [expected_shape]:
        raise ValueError("Darwin frozen <references/> shape drift")

    if promotion.get("schema_version") != PROFILE_PROMOTION_SCHEMA:
        raise ValueError("Darwin profile-promotion schema drift")
    if promotion.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin profile-promotion candidate drift")
    if promotion.get("promotion_sha256") != PROFILE_PROMOTION_SHA256:
        raise ValueError("Darwin profile-promotion identity drift")

    if backlog.get("schema_version") != BACKLOG_SCHEMA:
        raise ValueError("Darwin semantic-backlog schema drift")
    if backlog.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin semantic-backlog candidate drift")
    if backlog.get("backlog_sha256") != BACKLOG_SHA256:
        raise ValueError("Darwin semantic-backlog identity drift")
    expected_next = {
        "source_kind": "tag",
        "name": "references",
        "kind": "self_closing",
        "count": EXPECTED_REFERENCES_COUNT,
        "predecessor_priority_rank": 2,
        "priority_rank": 1,
        "semantic_status": "unresolved",
        "reason": (
            "highest remaining unresolved occurrence count after reviewed {{ё}} promotion; "
            "ties preserve deterministic predecessor ordering"
        ),
    }
    if backlog.get("next_research_slice") != expected_next:
        raise ValueError("Darwin semantic-backlog next-slice drift")


def build_probe_contract(
    surface: Mapping[str, object],
    promotion: Mapping[str, object],
    backlog: Mapping[str, object],
    *,
    source_revision_index_sha256: str,
    literary_dependency_count: int,
    references_total: int,
    references_inside_noinclude: int,
    references_outside_noinclude: int,
) -> dict[str, object]:
    """Build the source-free containment contract from aggregate replay evidence."""

    _verify_predecessors(surface, promotion, backlog)
    if source_revision_index_sha256 != SOURCE_REVISION_INDEX_SHA256:
        raise ValueError("Darwin replay source-index identity drift")
    if literary_dependency_count != EXPECTED_LITERARY_PAGE_COUNT:
        raise ValueError("Darwin replay literary dependency count drift")
    if references_total != EXPECTED_REFERENCES_COUNT:
        raise ValueError("Darwin replay <references/> total drift")
    if references_inside_noinclude != EXPECTED_REFERENCES_COUNT:
        raise ValueError("Darwin replay <references/> containment drift")
    if references_outside_noinclude != 0:
        raise ValueError("Darwin replay found <references/> outside noinclude")

    manifest: dict[str, object] = {
        "schema_version": PROBE_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "source_revision_index": {
            "sha256": SOURCE_REVISION_INDEX_SHA256,
            "literary_dependency_count": EXPECTED_LITERARY_PAGE_COUNT,
            "identity_replay_match": True,
        },
        "source_render_surface": {
            "schema_version": RENDER_SURFACE_SCHEMA,
            "freeze_manifest_sha256": RENDER_SURFACE_SHA256,
            "observed_shape": {
                "source_kind": "tag",
                "name": "references",
                "kind": "self_closing",
                "count": EXPECTED_REFERENCES_COUNT,
                "predecessor_handling": "provider_reference_semantics_required",
                "predecessor_semantic_status": "unresolved",
            },
        },
        "effective_state": {
            "profile_promotion_schema": PROFILE_PROMOTION_SCHEMA,
            "profile_promotion_sha256": PROFILE_PROMOTION_SHA256,
            "semantic_backlog_schema": BACKLOG_SCHEMA,
            "semantic_backlog_sha256": BACKLOG_SHA256,
        },
        "containment_evidence": {
            "references_total": references_total,
            "references_inside_noinclude": references_inside_noinclude,
            "references_outside_noinclude": references_outside_noinclude,
            "all_observed_references_inside_noinclude": True,
            "existing_defined_handling": "strip_nontranscluded_region",
        },
        "promotion_decision": {
            "candidate_local_drop_supported_by_containment": True,
            "provider_cite_semantics_replayed": False,
            "profile_rule_promoted": False,
            "next_action": "independent_review_then_separate_profile_backlog_promotion_judgement",
        },
        "renderer_semantics_complete": False,
        "renderer_implementation_ready": False,
        "historical_transclusion_provenance_proved": False,
        "offline_version_pinned_mediawiki_environment_claimed": False,
        "inter_page_composition_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    manifest["probe_sha256"] = _self_digest(manifest, "probe_sha256")
    return manifest


def build_probe_from_paths(
    index_path: Path,
    surface_path: Path,
    promotion_path: Path,
    backlog_path: Path,
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[int, str]] = fetch_pinned_literary_wikitext,
) -> dict[str, object]:
    surface = _load_object(surface_path, label="render surface")
    promotion = _load_object(promotion_path, label="profile promotion")
    backlog = _load_object(backlog_path, label="semantic backlog")
    _verify_predecessors(surface, promotion, backlog)

    source_index_sha256 = sha256(index_path.read_bytes()).hexdigest()
    if source_index_sha256 != SOURCE_REVISION_INDEX_SHA256:
        raise ValueError("Darwin source revision index physical digest drift")

    rows = load_sharded_manifest(index_path)
    literary = set(literary_page_sequences())
    selected = tuple(row for row in rows if int(row["page_sequence"]) in literary)
    if len(selected) != EXPECTED_LITERARY_PAGE_COUNT:
        raise ValueError("expected exactly 388 frozen Darwin literary Page identities")
    fetched = fetcher(selected)

    total = inside = outside = 0
    for row in selected:
        revid = int(row["revision_id"])
        wikitext = fetched.get(revid)
        if not isinstance(wikitext, str):
            raise ValueError(f"missing replayed Page wikitext for revision {revid}")
        evidence = audit_reference_containment(wikitext)
        total += int(evidence["references_total"])
        inside += int(evidence["references_inside_noinclude"])
        outside += int(evidence["references_outside_noinclude"])

    return build_probe_contract(
        surface,
        promotion,
        backlog,
        source_revision_index_sha256=source_index_sha256,
        literary_dependency_count=len(selected),
        references_total=total,
        references_inside_noinclude=inside,
        references_outside_noinclude=outside,
    )


def validate_probe(
    manifest: Mapping[str, object],
    surface: Mapping[str, object],
    promotion: Mapping[str, object],
    backlog: Mapping[str, object],
) -> None:
    evidence = manifest.get("containment_evidence")
    if not isinstance(evidence, dict):
        raise ValueError("Darwin references containment evidence missing")
    expected = build_probe_contract(
        surface,
        promotion,
        backlog,
        source_revision_index_sha256=SOURCE_REVISION_INDEX_SHA256,
        literary_dependency_count=EXPECTED_LITERARY_PAGE_COUNT,
        references_total=int(evidence.get("references_total", -1)),
        references_inside_noinclude=int(evidence.get("references_inside_noinclude", -1)),
        references_outside_noinclude=int(evidence.get("references_outside_noinclude", -1)),
    )
    if dict(manifest) != expected:
        raise ValueError("Darwin references containment probe drift")
    if manifest.get("probe_sha256") != _self_digest(manifest, "probe_sha256"):
        raise ValueError("Darwin references containment self-digest drift")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--surface", type=Path, required=True)
    parser.add_argument("--promotion", type=Path, required=True)
    parser.add_argument("--backlog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    manifest = build_probe_from_paths(
        args.index,
        args.surface,
        args.promotion,
        args.backlog,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(manifest["probe_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
