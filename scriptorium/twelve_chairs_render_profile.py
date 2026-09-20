"""Freeze a fail-closed Page-rendering decision profile for Twelve Chairs 1928.

The profile consumes only the committed source-free exact-410 rendering-surface freeze.
It classifies every observed tag/template shape and deliberately refuses to invent
Wikisource template expansion semantics.  This is a profile boundary, not a renderer:
page prose, inter-page composition, body counts/digests and corpus/FantLab gates stay
closed until the unresolved semantic classes are independently frozen and implemented.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

PROFILE_VERSION = "scriptorium-twelve-chairs-page-render-profile-v1"
PROFILE_STATUS = "fail_closed_profile_frozen_template_semantics_pending"
CANDIDATE_ID = "ilf-petrov-twelve-chairs-ru"
FAMILY_ID = "wikisource-zif-1928-first-standalone-edition"
SURFACE_SCHEMA = "scriptorium-twelve-chairs-render-surface-freeze-v1"
SURFACE_STATUS = "surface_inventory_verified_renderer_unfrozen"
EXPECTED_DEPENDENCY_COUNT = 410
EXPECTED_INDEX_SHA256 = "c1e3280984e640b8fe739a752ff49a3327633f49b52a635bd2d2d1e6a09f538f"
EXPECTED_SURFACE_FREEZE_SHA256 = "8a4f04238c68c40e59464e76a7911f0bee9488e09daab9f8772b1af970768d23"

# Keys are exact shapes observed in the reviewed source-free exact-410 surface freeze.
# Decisions are intentionally conservative.  Structural Page tags whose textual effect is
# local and explicit can be classified now; template expansion is not guessed from names.
TAG_DECISIONS: dict[tuple[str, str], tuple[str, str]] = {
    ("br", "open"): ("emit_line_break", "defined"),
    ("center", "close"): ("preserve_inner_text_container", "defined"),
    ("center", "open"): ("preserve_inner_text_container", "defined"),
    ("div", "close"): ("preserve_inner_text_container", "defined"),
    ("div", "open"): ("preserve_inner_text_container", "defined"),
    ("noinclude", "close"): ("strip_nontranscluded_region", "defined"),
    ("noinclude", "open"): ("strip_nontranscluded_region", "defined"),
    ("pagequality", "self_closing"): ("drop_proofread_metadata", "defined"),
    ("poem", "close"): ("preserve_inner_text_container", "defined"),
    ("poem", "open"): ("preserve_inner_text_container", "defined"),
    ("references", "self_closing"): ("provider_reference_semantics_required", "unresolved"),
    ("section", "self_closing"): ("drop_proofread_section_marker", "defined"),
}

_TEMPLATE_SHAPES = (
    ("Justify", 1, 0),
    ("Lang", 2, 0),
    ("^", 1, 0),
    ("block center/e", 0, 0),
    ("block center/s", 0, 0),
    ("c", 1, 0),
    ("heading", 2, 0),
    ("heading", 2, 1),
    ("heading", 2, 2),
    ("indent", 1, 0),
    ("justify", 1, 0),
    ("left", 2, 0),
    ("nobr", 1, 0),
    ("noindent", 0, 0),
    ("nop", 0, 0),
    ("razr2", 1, 0),
    ("right", 2, 0),
    ("sc", 1, 0),
    ("uc", 1, 0),
    ("Так в тексте", 1, 0),
    ("Так в тексте", 2, 0),
    ("Центр", 1, 1),
    ("акут", 0, 0),
    ("буквица3", 1, 2),
    ("гравис", 0, 0),
    ("конец рамки2", 0, 0),
    ("опечатка2", 2, 0),
    ("опечатка2", 3, 0),
    ("рамка2", 0, 0),
    ("центр", 1, 1),
)

TEMPLATE_DECISIONS: dict[tuple[str, int, int], tuple[str, str]] = {
    shape: (
        "inter_page_semantics_required" if shape[0] == "nop" else "provider_template_semantics_required",
        "unresolved",
    )
    for shape in _TEMPLATE_SHAPES
}


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_canonical(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _shape_key_tag(row: Mapping[str, object]) -> tuple[str, str]:
    name = row.get("name")
    kind = row.get("kind")
    count = row.get("count")
    if not isinstance(name, str) or not isinstance(kind, str) or not isinstance(count, int) or count < 1:
        raise ValueError("invalid tag-shape row")
    return name, kind


def _shape_key_template(row: Mapping[str, object]) -> tuple[str, int, int]:
    name = row.get("name")
    positional = row.get("positional")
    named = row.get("named")
    count = row.get("count")
    if (
        not isinstance(name, str)
        or not isinstance(positional, int)
        or not isinstance(named, int)
        or not isinstance(count, int)
        or positional < 0
        or named < 0
        or count < 1
    ):
        raise ValueError("invalid template-shape row")
    return name, positional, named


def _validate_surface_identity(surface: Mapping[str, object]) -> None:
    expected = {
        "schema_version": SURFACE_SCHEMA,
        "status": SURFACE_STATUS,
        "candidate_id": CANDIDATE_ID,
        "family_id": FAMILY_ID,
        "dependency_count": EXPECTED_DEPENDENCY_COUNT,
        "source_revision_index_sha256": EXPECTED_INDEX_SHA256,
        "freeze_manifest_sha256": EXPECTED_SURFACE_FREEZE_SHA256,
        "source_text_included": False,
        "rendering_profile_frozen": False,
        "inter_page_composition_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    for key, value in expected.items():
        if surface.get(key) != value:
            raise ValueError(f"render-surface identity/gate drift: {key}")


def build_profile(surface: Mapping[str, object]) -> dict[str, object]:
    """Build the deterministic source-free profile, failing closed on surface drift."""

    _validate_surface_identity(surface)
    tag_rows = surface.get("tag_shapes")
    template_rows = surface.get("template_shapes")
    if not isinstance(tag_rows, list) or not isinstance(template_rows, list):
        raise ValueError("render surface is missing shape inventories")

    observed_tags = {_shape_key_tag(row) for row in tag_rows if isinstance(row, dict)}
    observed_templates = {_shape_key_template(row) for row in template_rows if isinstance(row, dict)}
    if len(observed_tags) != len(tag_rows) or len(observed_templates) != len(template_rows):
        raise ValueError("duplicate or invalid render-surface shape rows")
    if observed_tags != set(TAG_DECISIONS):
        missing = sorted(observed_tags - set(TAG_DECISIONS))
        stale = sorted(set(TAG_DECISIONS) - observed_tags)
        raise ValueError(f"tag decision coverage drift: unclassified={missing!r} stale={stale!r}")
    if observed_templates != set(TEMPLATE_DECISIONS):
        missing = sorted(observed_templates - set(TEMPLATE_DECISIONS))
        stale = sorted(set(TEMPLATE_DECISIONS) - observed_templates)
        raise ValueError(f"template decision coverage drift: unclassified={missing!r} stale={stale!r}")

    tag_rules: list[dict[str, object]] = []
    for row in tag_rows:
        assert isinstance(row, dict)
        key = _shape_key_tag(row)
        handling, status = TAG_DECISIONS[key]
        tag_rules.append({
            "name": key[0],
            "kind": key[1],
            "count": int(row["count"]),
            "handling": handling,
            "semantic_status": status,
        })

    template_rules: list[dict[str, object]] = []
    for row in template_rows:
        assert isinstance(row, dict)
        key = _shape_key_template(row)
        handling, status = TEMPLATE_DECISIONS[key]
        template_rules.append({
            "name": key[0],
            "positional": key[1],
            "named": key[2],
            "count": int(row["count"]),
            "handling": handling,
            "semantic_status": status,
        })

    tag_rules.sort(key=lambda row: (str(row["name"]), str(row["kind"])))
    template_rules.sort(key=lambda row: (str(row["name"]), int(row["positional"]), int(row["named"])))
    unresolved_tag_rules = [row for row in tag_rules if row["semantic_status"] == "unresolved"]
    unresolved_template_rules = [row for row in template_rules if row["semantic_status"] == "unresolved"]

    profile: dict[str, object] = {
        "profile_version": PROFILE_VERSION,
        "status": PROFILE_STATUS,
        "candidate_id": CANDIDATE_ID,
        "family_id": FAMILY_ID,
        "source_text_included": False,
        "source_surface": {
            "schema_version": SURFACE_SCHEMA,
            "dependency_count": EXPECTED_DEPENDENCY_COUNT,
            "source_revision_index_sha256": EXPECTED_INDEX_SHA256,
            "freeze_manifest_sha256": EXPECTED_SURFACE_FREEZE_SHA256,
        },
        "extraction_policy": {
            "exact_revision_identity_required_before_content_fetch": True,
            "comments": "drop",
            "noinclude_regions": "drop",
            "unknown_tag_shape": "fail_closed",
            "unknown_template_shape": "fail_closed",
            "template_expansion_policy": "do_not_guess; freeze provider/local semantics before literary-body rendering",
            "persist_source_wikitext": False,
            "persist_rendered_prose": False,
        },
        "tag_rules": tag_rules,
        "template_rules": template_rules,
        "coverage": {
            "observed_tag_shape_count": len(tag_rules),
            "observed_tag_token_count": sum(int(row["count"]) for row in tag_rules),
            "observed_template_shape_count": len(template_rules),
            "observed_template_invocation_count": sum(int(row["count"]) for row in template_rules),
            "unresolved_tag_shape_count": len(unresolved_tag_rules),
            "unresolved_tag_token_count": sum(int(row["count"]) for row in unresolved_tag_rules),
            "unresolved_template_shape_count": len(unresolved_template_rules),
            "unresolved_template_invocation_count": sum(int(row["count"]) for row in unresolved_template_rules),
            "all_observed_shapes_classified": True,
        },
        "rendering_profile_frozen": True,
        "renderer_semantics_complete": False,
        "renderer_implementation_ready": False,
        "rendering_equivalence_claimed": False,
        "inter_page_composition_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    profile["profile_sha256"] = _sha256_canonical(profile)
    return profile


def validate_profile(profile: Mapping[str, object], surface: Mapping[str, object]) -> None:
    expected = build_profile(surface)
    if dict(profile) != expected:
        raise ValueError("Twelve Chairs rendering profile drift")


def build_profile_from_path(surface_path: Path) -> dict[str, object]:
    value = json.loads(surface_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("render-surface JSON must be an object")
    return build_profile(value)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surface", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    profile = build_profile_from_path(args.surface)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "profile_sha256": profile["profile_sha256"],
        "renderer_semantics_complete": profile["renderer_semantics_complete"],
        "unresolved_template_shape_count": profile["coverage"]["unresolved_template_shape_count"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
