"""Promote reviewed Darwin/Rachinsky <references/> containment fail-closed.

This successor consumes the independently reviewed source-free containment probe from
SCRIP-CORPUS-079. It removes only the observed self-closing <references/> shape from
this candidate's unresolved semantic backlog because all 388 occurrences are already
removed by the existing noinclude strip. It does not reproduce Cite semantics or claim
historical MediaWiki transclusion/runtime equivalence.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
PROMOTION_SCHEMA = "scriptorium-darwin-render-profile-references-promotion-v1"
EFFECTIVE_PROFILE_VERSION = "scriptorium-darwin-page-render-profile-v3"
BACKLOG_SCHEMA = "scriptorium-darwin-render-semantic-backlog-v3"
PREDECESSOR_PROMOTION_SCHEMA = "scriptorium-darwin-render-profile-yo-promotion-v1"
PREDECESSOR_PROMOTION_SHA256 = "153f6ceb89025da90971ddc265df680359ff498103bb47ecd68f86bb3205ed28"
PREDECESSOR_BACKLOG_SCHEMA = "scriptorium-darwin-render-semantic-backlog-v2"
PREDECESSOR_BACKLOG_SHA256 = "6d4ba2bb9ec78731d97d91c87d0628207ec880901e9d388fa7aa7c70fb20e3be"
PROBE_SCHEMA = "scriptorium-darwin-references-containment-probe-v1"
PROBE_SHA256 = "3dde2e1ea259ccc4f855ad20dc8df588f9546a9ec181f84155175a86c3b139e3"
REFERENCES_COUNT = 388


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _self_digest(value: Mapping[str, object], field: str) -> str:
    unsigned = deepcopy(dict(value))
    unsigned.pop(field, None)
    return _sha256_json(unsigned)


def _load_object(path: Path, *, label: str) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Darwin {label} must be a JSON object")
    return value


def _verify_predecessors(
    yo_promotion: Mapping[str, object],
    backlog_v2: Mapping[str, object],
    probe: Mapping[str, object],
) -> None:
    if yo_promotion.get("schema_version") != PREDECESSOR_PROMOTION_SCHEMA:
        raise ValueError("Darwin predecessor promotion schema drift")
    if yo_promotion.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin predecessor promotion candidate drift")
    if yo_promotion.get("promotion_sha256") != PREDECESSOR_PROMOTION_SHA256:
        raise ValueError("Darwin predecessor promotion digest drift")

    if backlog_v2.get("schema_version") != PREDECESSOR_BACKLOG_SCHEMA:
        raise ValueError("Darwin predecessor backlog schema drift")
    if backlog_v2.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin predecessor backlog candidate drift")
    if backlog_v2.get("backlog_sha256") != PREDECESSOR_BACKLOG_SHA256:
        raise ValueError("Darwin predecessor backlog digest drift")
    expected_next = {
        "source_kind": "tag",
        "name": "references",
        "kind": "self_closing",
        "count": REFERENCES_COUNT,
        "predecessor_priority_rank": 2,
        "priority_rank": 1,
        "semantic_status": "unresolved",
        "reason": (
            "highest remaining unresolved occurrence count after reviewed {{ё}} promotion; "
            "ties preserve deterministic predecessor ordering"
        ),
    }
    if backlog_v2.get("next_research_slice") != expected_next:
        raise ValueError("Darwin predecessor backlog next-slice drift")

    if probe.get("schema_version") != PROBE_SCHEMA or probe.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin references probe identity drift")
    if probe.get("probe_sha256") != PROBE_SHA256 or _self_digest(probe, "probe_sha256") != PROBE_SHA256:
        raise ValueError("Darwin references probe self-digest drift")
    evidence = probe.get("containment_evidence")
    decision = probe.get("promotion_decision")
    if not isinstance(evidence, dict) or not isinstance(decision, dict):
        raise ValueError("Darwin references probe evidence missing")
    if evidence != {
        "references_total": REFERENCES_COUNT,
        "references_inside_noinclude": REFERENCES_COUNT,
        "references_outside_noinclude": 0,
        "all_observed_references_inside_noinclude": True,
        "existing_defined_handling": "strip_nontranscluded_region",
    }:
        raise ValueError("Darwin references containment evidence drift")
    if decision.get("candidate_local_drop_supported_by_containment") is not True:
        raise ValueError("Darwin references candidate-local promotion gate drift")
    if decision.get("provider_cite_semantics_replayed") is not False:
        raise ValueError("Darwin references Cite-semantics boundary drift")
    if decision.get("profile_rule_promoted") is not False:
        raise ValueError("Darwin references predecessor promotion-state drift")
    for key in (
        "historical_transclusion_provenance_proved",
        "offline_version_pinned_mediawiki_environment_claimed",
        "renderer_semantics_complete",
        "renderer_implementation_ready",
        "inter_page_composition_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    ):
        if probe.get(key) is not False:
            raise ValueError(f"Darwin references downstream gate drift: {key}")
    if probe.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("Darwin references FantLab identity boundary drift")


def build_profile_promotion(
    yo_promotion: Mapping[str, object],
    backlog_v2: Mapping[str, object],
    probe: Mapping[str, object],
) -> dict[str, object]:
    _verify_predecessors(yo_promotion, backlog_v2, probe)
    totals = backlog_v2.get("unresolved_totals")
    if totals != {
        "tag_shape_count": 5,
        "tag_token_count": 518,
        "template_shape_count": 37,
        "template_invocation_count": 2356,
    }:
        raise ValueError("Darwin predecessor unresolved totals drift")

    result: dict[str, object] = {
        "schema_version": PROMOTION_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "predecessor_effective_profile": {
            "profile_version": "scriptorium-darwin-page-render-profile-v2",
            "promotion_schema": PREDECESSOR_PROMOTION_SCHEMA,
            "promotion_sha256": PREDECESSOR_PROMOTION_SHA256,
        },
        "predecessor_backlog": {
            "schema_version": PREDECESSOR_BACKLOG_SCHEMA,
            "backlog_sha256": PREDECESSOR_BACKLOG_SHA256,
        },
        "semantic_evidence": {
            "schema_version": PROBE_SCHEMA,
            "probe_sha256": PROBE_SHA256,
            "all_observed_references_inside_noinclude": True,
            "references_total": REFERENCES_COUNT,
            "references_inside_noinclude": REFERENCES_COUNT,
            "references_outside_noinclude": 0,
            "existing_defined_handling": "strip_nontranscluded_region",
            "provider_cite_semantics_replayed": False,
            "historical_transclusion_provenance_proved": False,
            "offline_version_pinned_mediawiki_environment_claimed": False,
        },
        "promoted_rule": {
            "source_kind": "tag",
            "name": "references",
            "kind": "self_closing",
            "count": REFERENCES_COUNT,
            "predecessor_handling": "provider_reference_semantics_required",
            "predecessor_semantic_status": "unresolved",
            "handling": "drop_via_existing_strip_nontranscluded_region",
            "semantic_status": "defined_candidate_local",
        },
        "effective_profile": {
            "profile_version": EFFECTIVE_PROFILE_VERSION,
            "unresolved_tag_shape_count": 4,
            "unresolved_tag_token_count": 130,
            "unresolved_template_shape_count": 37,
            "unresolved_template_invocation_count": 2356,
            "renderer_semantics_complete": False,
            "renderer_implementation_ready": False,
            "rendering_equivalence_claimed": False,
            "inter_page_composition_frozen": False,
            "literary_body_count_and_digests_frozen": False,
            "minimum_300k_proved": False,
            "admitted_for_calibration": False,
            "diagnostic_ready": False,
            "fantlab_source_edition_match": "unknown",
            "m2_parity_admissible": False,
        },
        "scope": (
            "candidate-local promotion only: all 388 observed self-closing <references/> tokens are removed "
            "by the already-defined noinclude strip; no Cite semantics, historical transclusion, or general "
            "MediaWiki runtime claim"
        ),
    }
    result["promotion_sha256"] = _self_digest(result, "promotion_sha256")
    return result


def build_backlog_v3(
    promotion: Mapping[str, object],
    yo_promotion: Mapping[str, object],
    backlog_v2: Mapping[str, object],
    probe: Mapping[str, object],
) -> dict[str, object]:
    expected_promotion = build_profile_promotion(yo_promotion, backlog_v2, probe)
    if dict(promotion) != expected_promotion:
        raise ValueError("Darwin references profile-promotion drift")

    tracks = backlog_v2.get("resolution_tracks")
    expected_tracks = [
        {"track": "provider_template", "shape_count": 36, "occurrence_count": 2352},
        {"track": "provider_reference", "shape_count": 3, "occurrence_count": 466},
        {"track": "provider_math", "shape_count": 2, "occurrence_count": 52},
        {"track": "inter_page", "shape_count": 1, "occurrence_count": 4},
    ]
    if tracks != expected_tracks:
        raise ValueError("Darwin predecessor resolution tracks drift")

    result: dict[str, object] = {
        "schema_version": BACKLOG_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "predecessor_backlog": {
            "schema_version": PREDECESSOR_BACKLOG_SCHEMA,
            "backlog_sha256": PREDECESSOR_BACKLOG_SHA256,
        },
        "source_profile_promotion": {
            "schema_version": PROMOTION_SCHEMA,
            "promotion_sha256": promotion["promotion_sha256"],
            "effective_profile_version": EFFECTIVE_PROFILE_VERSION,
        },
        "resolved_item": {
            "source_kind": "tag",
            "name": "references",
            "kind": "self_closing",
            "count": REFERENCES_COUNT,
            "predecessor_priority_rank": 2,
            "predecessor_effective_priority_rank": 1,
            "semantic_status": "defined_candidate_local",
            "resolution": "removed_by_existing_strip_nontranscluded_region_after_reviewed_388_of_388_containment",
        },
        "remaining_priority_count": 41,
        "remaining_priority_order": (
            "original v1 predecessor order with resolved {{ё}} and self-closing <references/> removed; "
            "priority ranks compacted from 1"
        ),
        "unresolved_totals": {
            "tag_shape_count": 4,
            "tag_token_count": 130,
            "template_shape_count": 37,
            "template_invocation_count": 2356,
        },
        "resolution_tracks": [
            {"track": "provider_template", "shape_count": 36, "occurrence_count": 2352},
            {"track": "provider_reference", "shape_count": 2, "occurrence_count": 78},
            {"track": "provider_math", "shape_count": 2, "occurrence_count": 52},
            {"track": "inter_page", "shape_count": 1, "occurrence_count": 4},
        ],
        "next_research_slice": {
            "source_kind": "template",
            "name": "ВАР",
            "positional": 2,
            "named": 0,
            "count": 388,
            "predecessor_priority_rank": 3,
            "priority_rank": 1,
            "semantic_status": "unresolved",
            "reason": (
                "highest remaining unresolved occurrence count after reviewed {{ё}} and candidate-local "
                "<references/> promotions; deterministic predecessor ordering preserved"
            ),
        },
        "renderer_semantics_complete": False,
        "renderer_implementation_ready": False,
        "inter_page_composition_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    result["backlog_sha256"] = _self_digest(result, "backlog_sha256")
    return result


def validate_promotion(
    promotion: Mapping[str, object],
    backlog_v3: Mapping[str, object],
    yo_promotion: Mapping[str, object],
    backlog_v2: Mapping[str, object],
    probe: Mapping[str, object],
) -> None:
    expected_promotion = build_profile_promotion(yo_promotion, backlog_v2, probe)
    expected_backlog = build_backlog_v3(expected_promotion, yo_promotion, backlog_v2, probe)
    if dict(promotion) != expected_promotion:
        raise ValueError("Darwin references profile-promotion artifact drift")
    if dict(backlog_v3) != expected_backlog:
        raise ValueError("Darwin references semantic-backlog v3 drift")
    if promotion.get("promotion_sha256") != _self_digest(promotion, "promotion_sha256"):
        raise ValueError("Darwin references promotion self-digest drift")
    if backlog_v3.get("backlog_sha256") != _self_digest(backlog_v3, "backlog_sha256"):
        raise ValueError("Darwin references backlog self-digest drift")


def build_from_paths(
    yo_promotion_path: Path,
    backlog_v2_path: Path,
    probe_path: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    yo_promotion = _load_object(yo_promotion_path, label="yo promotion")
    backlog_v2 = _load_object(backlog_v2_path, label="semantic backlog v2")
    probe = _load_object(probe_path, label="references containment probe")
    promotion = build_profile_promotion(yo_promotion, backlog_v2, probe)
    backlog_v3 = build_backlog_v3(promotion, yo_promotion, backlog_v2, probe)
    return promotion, backlog_v3


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yo-promotion", type=Path, required=True)
    parser.add_argument("--backlog-v2", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--promotion-output", type=Path, required=True)
    parser.add_argument("--backlog-output", type=Path, required=True)
    args = parser.parse_args(argv)
    promotion, backlog_v3 = build_from_paths(args.yo_promotion, args.backlog_v2, args.probe)
    args.promotion_output.write_text(
        json.dumps(promotion, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.backlog_output.write_text(
        json.dumps(backlog_v3, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(promotion["promotion_sha256"])
    print(backlog_v3["backlog_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
