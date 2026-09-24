"""Promote the reviewed Darwin/Rachinsky zero-argument {{ё}} rule fail-closed.

This module preserves the original frozen render profile/backlog as immutable predecessor
artifacts.  It validates those predecessors plus the independently reviewed v6 replay
contract, then derives a compact source-free promotion contract and a mechanically
reduced semantic backlog.  It does not implement a general MediaWiki renderer and does
not widen the live-snapshot evidence into historical transclusion provenance.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from .darwin_render_profile import validate_profile
from .darwin_semantic_backlog import validate_backlog

CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
PROMOTION_SCHEMA = "scriptorium-darwin-render-profile-yo-promotion-v1"
EFFECTIVE_PROFILE_VERSION = "scriptorium-darwin-page-render-profile-v2"
BACKLOG_SCHEMA = "scriptorium-darwin-render-semantic-backlog-v2"
BASE_PROFILE_VERSION = "scriptorium-darwin-page-render-profile-v1"
BASE_PROFILE_SHA256 = "2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d"
BASE_BACKLOG_SCHEMA = "scriptorium-darwin-render-semantic-backlog-v1"
BASE_BACKLOG_SHA256 = "4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2"
REPLAY_SCHEMA = "scriptorium-darwin-template-yo-replay-contract-v6"
REPLAY_SHA256 = "c317eb5247701f0ad860811e9349f4e6f42274e72e8856eecb8a9aff610f988f"
FORCED_OUTPUT = "ё"
FORCED_SHA256 = "30fbc377ae9122edc2cdbed70b9261817d196eca8db96ac8bfa4cfaf412667ac"
NON_FORCED_OUTPUT = "е"
NON_FORCED_SHA256 = "259f56cb715ba3a3f1ca41a4ff1972cca698cb49eef1ae018dff325507da8b26"
YO_COUNT = 2227


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


def _verify_base_profile(profile: Mapping[str, object], surface: Mapping[str, object]) -> dict[str, object]:
    validate_profile(profile, surface)
    if profile.get("profile_version") != BASE_PROFILE_VERSION:
        raise ValueError("Darwin predecessor render-profile version drift")
    if profile.get("profile_sha256") != BASE_PROFILE_SHA256:
        raise ValueError("Darwin predecessor render-profile digest identity drift")

    rules = profile.get("template_rules")
    if not isinstance(rules, list):
        raise ValueError("Darwin predecessor render profile is missing template rules")
    matches = [
        row for row in rules
        if isinstance(row, dict)
        and row.get("name") == "ё"
        and row.get("positional") == 0
        and row.get("named") == 0
    ]
    if len(matches) != 1:
        raise ValueError("Darwin predecessor {{ё}} shape identity drift")
    rule = matches[0]
    expected = {
        "name": "ё",
        "positional": 0,
        "named": 0,
        "count": YO_COUNT,
        "handling": "provider_template_semantics_required",
        "semantic_status": "unresolved",
    }
    if rule != expected:
        raise ValueError("Darwin predecessor {{ё}} rule drift")
    return rule


def _verify_base_backlog(
    backlog: Mapping[str, object],
    profile: Mapping[str, object],
    surface: Mapping[str, object],
) -> list[dict[str, object]]:
    validate_backlog(backlog, profile, surface)
    if backlog.get("schema_version") != BASE_BACKLOG_SCHEMA:
        raise ValueError("Darwin predecessor semantic-backlog schema drift")
    if backlog.get("backlog_sha256") != BASE_BACKLOG_SHA256:
        raise ValueError("Darwin predecessor semantic-backlog digest identity drift")

    items = backlog.get("prioritized_items")
    if not isinstance(items, list) or len(items) != 43 or not all(isinstance(row, dict) for row in items):
        raise ValueError("Darwin predecessor semantic-backlog item set drift")
    first = items[0]
    expected_first = {
        "source_kind": "template",
        "name": "ё",
        "positional": 0,
        "named": 0,
        "count": YO_COUNT,
        "handling": "provider_template_semantics_required",
        "semantic_status": "unresolved",
        "track": "provider_template",
        "priority_rank": 1,
    }
    if first != expected_first:
        raise ValueError("Darwin predecessor semantic-backlog {{ё}} item drift")
    return [dict(row) for row in items]


def _verify_replay_v6(replay: Mapping[str, object]) -> None:
    if replay.get("schema_version") != REPLAY_SCHEMA or replay.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin reviewed v6 replay identity drift")
    if replay.get("contract_sha256") != REPLAY_SHA256 or _self_digest(replay, "contract_sha256") != REPLAY_SHA256:
        raise ValueError("Darwin reviewed v6 replay self-digest drift")

    environment = replay.get("replay_environment")
    if not isinstance(environment, dict):
        raise ValueError("Darwin reviewed v6 replay environment missing")
    if environment.get("historical_transclusion_provenance_proved") is not False:
        raise ValueError("Darwin reviewed v6 historical-transclusion boundary drift")
    if environment.get("offline_version_pinned_mediawiki_environment_claimed") is not False:
        raise ValueError("Darwin reviewed v6 offline-runtime boundary drift")
    if environment.get("identity_stable_window_required") is not True:
        raise ValueError("Darwin reviewed v6 identity-window boundary drift")

    modes = replay.get("mode_verification")
    if not isinstance(modes, dict) or modes.get("outputs_verified") is not True:
        raise ValueError("Darwin reviewed v6 output-verification gate drift")
    expected_modes = {
        "forced_yoification": (FORCED_OUTPUT, FORCED_SHA256),
        "non_forced_yoification": (NON_FORCED_OUTPUT, NON_FORCED_SHA256),
    }
    for name, (value, digest) in expected_modes.items():
        mode = modes.get(name)
        if not isinstance(mode, dict):
            raise ValueError(f"Darwin reviewed v6 mode missing: {name}")
        if mode.get("verified_semantic_output") != value or mode.get("verified_semantic_output_sha256") != digest:
            raise ValueError(f"Darwin reviewed v6 mode output drift: {name}")

    promotion = replay.get("promotion_decision")
    if not isinstance(promotion, dict) or promotion.get("render_profile_rule_promoted") is not False:
        raise ValueError("Darwin reviewed v6 predecessor promotion boundary drift")
    gates = replay.get("gates")
    if not isinstance(gates, dict) or gates.get("zero_argument_template_yo_outputs_verified") is not True:
        raise ValueError("Darwin reviewed v6 {{ё}} evidence gate drift")


def build_profile_promotion(
    profile: Mapping[str, object],
    backlog: Mapping[str, object],
    surface: Mapping[str, object],
    replay_v6: Mapping[str, object],
) -> dict[str, object]:
    """Build the compact effective-profile promotion after validating every predecessor."""
    _verify_base_profile(profile, surface)
    _verify_base_backlog(backlog, profile, surface)
    _verify_replay_v6(replay_v6)

    coverage = profile.get("coverage")
    if not isinstance(coverage, dict):
        raise ValueError("Darwin predecessor render-profile coverage missing")
    if coverage.get("unresolved_template_shape_count") != 38 or coverage.get("unresolved_template_invocation_count") != 4583:
        raise ValueError("Darwin predecessor unresolved-template coverage drift")

    result: dict[str, object] = {
        "schema_version": PROMOTION_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "predecessor_profile": {
            "profile_version": BASE_PROFILE_VERSION,
            "profile_sha256": BASE_PROFILE_SHA256,
        },
        "semantic_evidence": {
            "schema_version": REPLAY_SCHEMA,
            "contract_sha256": REPLAY_SHA256,
            "historical_transclusion_provenance_proved": False,
            "offline_version_pinned_mediawiki_environment_claimed": False,
        },
        "promoted_rule": {
            "source_kind": "template",
            "name": "ё",
            "positional": 0,
            "named": 0,
            "count": YO_COUNT,
            "predecessor_handling": "provider_template_semantics_required",
            "predecessor_semantic_status": "unresolved",
            "handling": "emit_zero_argument_yo_by_yoification_mode",
            "semantic_status": "defined",
            "outputs": {
                "forced_yoification": {"value": FORCED_OUTPUT, "sha256": FORCED_SHA256},
                "non_forced_yoification": {"value": NON_FORCED_OUTPUT, "sha256": NON_FORCED_SHA256},
            },
        },
        "effective_profile": {
            "profile_version": EFFECTIVE_PROFILE_VERSION,
            "unresolved_tag_shape_count": int(coverage["unresolved_tag_shape_count"]),
            "unresolved_tag_token_count": int(coverage["unresolved_tag_token_count"]),
            "unresolved_template_shape_count": 37,
            "unresolved_template_invocation_count": 4583 - YO_COUNT,
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
            "promotes only the observed zero-argument {{ё}} shape for the reviewed v6 identity-stable live "
            "snapshot; no historical transclusion or general MediaWiki runtime claim"
        ),
    }
    result["promotion_sha256"] = _self_digest(result, "promotion_sha256")
    return result


def build_backlog_v2(
    profile_promotion: Mapping[str, object],
    profile: Mapping[str, object],
    backlog: Mapping[str, object],
    surface: Mapping[str, object],
    replay_v6: Mapping[str, object],
) -> dict[str, object]:
    expected_promotion = build_profile_promotion(profile, backlog, surface, replay_v6)
    if dict(profile_promotion) != expected_promotion:
        raise ValueError("Darwin effective render-profile promotion drift")
    items = _verify_base_backlog(backlog, profile, surface)
    remaining = items[1:]
    if len(remaining) != 42 or any(row.get("name") == "ё" and row.get("source_kind") == "template" for row in remaining):
        raise ValueError("Darwin semantic-backlog one-shape promotion drift")

    totals = backlog.get("unresolved_totals")
    tracks = backlog.get("resolution_tracks")
    if not isinstance(totals, dict) or not isinstance(tracks, list):
        raise ValueError("Darwin predecessor semantic-backlog totals missing")
    track_by_name = {row.get("track"): row for row in tracks if isinstance(row, dict)}
    provider = track_by_name.get("provider_template")
    if not isinstance(provider, dict) or provider.get("shape_count") != 37 or provider.get("occurrence_count") != 4579:
        raise ValueError("Darwin predecessor provider-template track drift")

    next_item = remaining[0]
    expected_next = {
        "source_kind": "tag",
        "name": "references",
        "kind": "self_closing",
        "count": 388,
        "handling": "provider_reference_semantics_required",
        "semantic_status": "unresolved",
        "track": "provider_reference",
        "priority_rank": 2,
    }
    if next_item != expected_next:
        raise ValueError("Darwin successor semantic-backlog ordering drift")

    result: dict[str, object] = {
        "schema_version": BACKLOG_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "predecessor_backlog": {
            "schema_version": BASE_BACKLOG_SCHEMA,
            "backlog_sha256": BASE_BACKLOG_SHA256,
        },
        "source_profile_promotion": {
            "schema_version": PROMOTION_SCHEMA,
            "promotion_sha256": profile_promotion["promotion_sha256"],
            "effective_profile_version": EFFECTIVE_PROFILE_VERSION,
        },
        "resolved_item": {
            "source_kind": "template",
            "name": "ё",
            "positional": 0,
            "named": 0,
            "count": YO_COUNT,
            "predecessor_priority_rank": 1,
            "semantic_status": "defined",
            "resolution": "render_profile_rule_promoted_from_reviewed_v6",
        },
        "remaining_priority_count": len(remaining),
        "remaining_priority_order": "predecessor order with only resolved item removed; priority ranks compacted from 1",
        "unresolved_totals": {
            "tag_shape_count": int(totals["tag_shape_count"]),
            "tag_token_count": int(totals["tag_token_count"]),
            "template_shape_count": int(totals["template_shape_count"]) - 1,
            "template_invocation_count": int(totals["template_invocation_count"]) - YO_COUNT,
        },
        "resolution_tracks": [
            {"track": "provider_template", "shape_count": 36, "occurrence_count": 4579 - YO_COUNT},
            {"track": "provider_reference", "shape_count": 3, "occurrence_count": 466},
            {"track": "provider_math", "shape_count": 2, "occurrence_count": 52},
            {"track": "inter_page", "shape_count": 1, "occurrence_count": 4},
        ],
        "next_research_slice": {
            "source_kind": "tag",
            "name": "references",
            "kind": "self_closing",
            "count": 388,
            "predecessor_priority_rank": 2,
            "priority_rank": 1,
            "semantic_status": "unresolved",
            "reason": (
                "highest remaining unresolved occurrence count after reviewed {{ё}} promotion; ties preserve "
                "deterministic predecessor ordering"
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
    backlog_v2: Mapping[str, object],
    profile: Mapping[str, object],
    backlog: Mapping[str, object],
    surface: Mapping[str, object],
    replay_v6: Mapping[str, object],
) -> None:
    expected_promotion = build_profile_promotion(profile, backlog, surface, replay_v6)
    if dict(promotion) != expected_promotion:
        raise ValueError("Darwin effective render-profile promotion drift")
    expected_backlog = build_backlog_v2(promotion, profile, backlog, surface, replay_v6)
    if dict(backlog_v2) != expected_backlog:
        raise ValueError("Darwin semantic-backlog v2 drift")


def build_from_paths(
    profile_path: Path,
    backlog_path: Path,
    surface_path: Path,
    replay_v6_path: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    profile = _load_object(profile_path, label="render profile v1")
    backlog = _load_object(backlog_path, label="semantic backlog v1")
    surface = _load_object(surface_path, label="render surface")
    replay_v6 = _load_object(replay_v6_path, label="reviewed replay v6")
    promotion = build_profile_promotion(profile, backlog, surface, replay_v6)
    backlog_v2 = build_backlog_v2(promotion, profile, backlog, surface, replay_v6)
    return promotion, backlog_v2


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-v1", type=Path, required=True)
    parser.add_argument("--backlog-v1", type=Path, required=True)
    parser.add_argument("--surface", type=Path, required=True)
    parser.add_argument("--replay-v6", type=Path, required=True)
    parser.add_argument("--promotion-output", type=Path, required=True)
    parser.add_argument("--backlog-v2-output", type=Path, required=True)
    args = parser.parse_args(argv)

    promotion, backlog_v2 = build_from_paths(args.profile_v1, args.backlog_v1, args.surface, args.replay_v6)
    args.promotion_output.parent.mkdir(parents=True, exist_ok=True)
    args.backlog_v2_output.parent.mkdir(parents=True, exist_ok=True)
    args.promotion_output.write_text(json.dumps(promotion, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.backlog_v2_output.write_text(json.dumps(backlog_v2, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "promotion_sha256": promotion["promotion_sha256"],
        "backlog_sha256": backlog_v2["backlog_sha256"],
        "remaining_unresolved_template_invocations": backlog_v2["unresolved_totals"]["template_invocation_count"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
