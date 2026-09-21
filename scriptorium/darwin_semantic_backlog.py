"""Prioritize unresolved Darwin/Rachinsky render semantics without inventing them.

The reviewed render profile already freezes the exact unresolved tag/template surface.
This module reduces that source-free evidence to a deterministic research backlog. It
never reads Page wikitext and never promotes an unresolved rendering behavior to a
semantic claim.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from .darwin_render_profile import CANDIDATE_ID, PROFILE_VERSION, validate_profile


BACKLOG_VERSION = "scriptorium-darwin-render-semantic-backlog-v1"
BACKLOG_STATUS = "unresolved_semantics_prioritized_no_semantics_inferred"
_TRACK_BY_HANDLING = {
    "provider_template_semantics_required": "provider_template",
    "provider_reference_semantics_required": "provider_reference",
    "provider_math_semantics_required": "provider_math",
    "inter_page_semantics_required": "inter_page",
}
_TRACK_ORDER = ("provider_template", "provider_reference", "provider_math", "inter_page")


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _priority_key(item: Mapping[str, object]) -> tuple[object, ...]:
    return (
        -int(item["count"]),
        str(item["source_kind"]),
        str(item["name"]),
        str(item.get("kind", "")),
        int(item.get("positional", -1)),
        int(item.get("named", -1)),
    )


def build_backlog(profile: Mapping[str, object], surface: Mapping[str, object]) -> dict[str, object]:
    """Build a source-free deterministic backlog from an already frozen profile."""

    validate_profile(profile, surface)
    if profile.get("renderer_semantics_complete") is not False:
        raise ValueError("Darwin semantic backlog requires incomplete renderer semantics")

    items: list[dict[str, object]] = []
    for source_kind, rules in (("tag", profile.get("tag_rules")), ("template", profile.get("template_rules"))):
        if not isinstance(rules, list):
            raise ValueError(f"Darwin render profile missing {source_kind} rules")
        for raw in rules:
            if not isinstance(raw, dict) or raw.get("semantic_status") != "unresolved":
                continue
            handling = raw.get("handling")
            if handling not in _TRACK_BY_HANDLING:
                raise ValueError(f"unclassified unresolved Darwin handling: {handling!r}")
            item: dict[str, object] = {
                "source_kind": source_kind,
                "name": raw["name"],
                "count": raw["count"],
                "handling": handling,
                "semantic_status": "unresolved",
                "track": _TRACK_BY_HANDLING[str(handling)],
            }
            if source_kind == "tag":
                item["kind"] = raw["kind"]
            else:
                item["positional"] = raw["positional"]
                item["named"] = raw["named"]
            items.append(item)

    items.sort(key=_priority_key)
    for rank, item in enumerate(items, 1):
        item["priority_rank"] = rank

    coverage = profile.get("coverage")
    if not isinstance(coverage, dict):
        raise ValueError("Darwin render profile missing coverage")
    tag_items = [row for row in items if row["source_kind"] == "tag"]
    template_items = [row for row in items if row["source_kind"] == "template"]
    totals = {
        "tag_shape_count": len(tag_items),
        "tag_token_count": sum(int(row["count"]) for row in tag_items),
        "template_shape_count": len(template_items),
        "template_invocation_count": sum(int(row["count"]) for row in template_items),
    }
    expected = {
        "tag_shape_count": int(coverage["unresolved_tag_shape_count"]),
        "tag_token_count": int(coverage["unresolved_tag_token_count"]),
        "template_shape_count": int(coverage["unresolved_template_shape_count"]),
        "template_invocation_count": int(coverage["unresolved_template_invocation_count"]),
    }
    if totals != expected:
        raise ValueError("Darwin unresolved semantic coverage drift")
    if not items:
        raise ValueError("Darwin semantic backlog unexpectedly empty")

    shape_counts: Counter[str] = Counter()
    occurrence_counts: Counter[str] = Counter()
    for item in items:
        track = str(item["track"])
        shape_counts[track] += 1
        occurrence_counts[track] += int(item["count"])
    tracks = [
        {
            "track": track,
            "shape_count": shape_counts[track],
            "occurrence_count": occurrence_counts[track],
        }
        for track in _TRACK_ORDER
    ]

    first = items[0]
    next_slice = {
        key: first[key]
        for key in ("source_kind", "name", "count")
    }
    if first["source_kind"] == "tag":
        next_slice["kind"] = first["kind"]
    else:
        next_slice["positional"] = first["positional"]
        next_slice["named"] = first["named"]
        next_slice["share_of_unresolved_template_invocations"] = {
            "numerator": first["count"],
            "denominator": totals["template_invocation_count"],
        }
    next_slice["semantic_status"] = "unresolved"
    next_slice["reason"] = (
        "highest observed unresolved occurrence count; semantic meaning remains unresolved "
        "until independently evidenced"
    )

    manifest: dict[str, object] = {
        "schema_version": BACKLOG_VERSION,
        "candidate_id": CANDIDATE_ID,
        "status": BACKLOG_STATUS,
        "source_profile": {
            "profile_version": PROFILE_VERSION,
            "profile_sha256": profile["profile_sha256"],
        },
        "source_text_included": False,
        "unresolved_totals": totals,
        "resolution_tracks": tracks,
        "prioritized_items": items,
        "next_research_slice": next_slice,
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
    manifest["backlog_sha256"] = _sha256_json(manifest)
    return manifest


def validate_backlog(manifest: Mapping[str, object], profile: Mapping[str, object], surface: Mapping[str, object]) -> None:
    expected = build_backlog(profile, surface)
    if dict(manifest) != expected:
        raise ValueError("Darwin semantic backlog drift")
    if manifest.get("source_text_included") is not False:
        raise ValueError("Darwin semantic backlog must remain source-free")
    for key in (
        "renderer_semantics_complete",
        "renderer_implementation_ready",
        "inter_page_composition_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    ):
        if manifest.get(key) is not False:
            raise ValueError(f"{key} must remain false in Darwin semantic backlog")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")


def build_backlog_from_paths(profile_path: Path, surface_path: Path) -> dict[str, object]:
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    surface = json.loads(surface_path.read_text(encoding="utf-8"))
    if not isinstance(profile, dict) or not isinstance(surface, dict):
        raise ValueError("Darwin semantic backlog inputs must be JSON objects")
    return build_backlog(profile, surface)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--surface", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = build_backlog_from_paths(args.profile, args.surface)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(manifest["backlog_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
