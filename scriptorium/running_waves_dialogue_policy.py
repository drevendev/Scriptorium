"""Source-free dialogue-policy sensitivity for Grin's *Running on Waves*.

This diagnostic replays the exact frozen 36-page body transiently and applies the
existing diagnostic-only dialogue policy probe. It does not change production
``scriptorium-dialogue-v1`` semantics and cannot establish FantLab parity while the
FantLab analyzer input remains source-unmatched.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from .dialogue_diagnostic import analyze_dialogue_policy
from .running_waves_body import (
    CHAPTER_SEPARATOR,
    MANIFEST_VERSION as BODY_MANIFEST_VERSION,
    _extract_bodies,
    validate_manifest as validate_body_manifest,
)
from .running_waves_diagnostic import (
    FANTLAB_ANALYSIS_DATE,
    FANTLAB_ANALYSIS_URL,
    FANTLAB_WORK_ID,
    FROZEN_BODY_CHARACTERS,
    FROZEN_BODY_SHA256,
)
from .running_waves_inventory import CANDIDATE_ID
from .wikisource_replay import fetch_pinned_chapter_revisions


DIAGNOSTIC_VERSION = "scriptorium-running-waves-dialogue-policy-diagnostic-v1"
FANTLAB_DIALOGUE_SHARE_PERCENT = 38.23
FANTLAB_AUTHOR_TEXT_INSIDE_DIALOGUE_PERCENT = 12.49


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _verify_composite_identity(composite: str, body_manifest: Mapping[str, object]) -> None:
    identity = body_manifest.get("composite_identity")
    if not isinstance(identity, Mapping):
        raise ValueError("missing Running on Waves composite identity")
    if identity.get("character_count_including_spaces") != len(composite):
        raise ValueError("frozen Running on Waves body identity drift for character count")
    if len(composite) != FROZEN_BODY_CHARACTERS:
        raise ValueError("Running on Waves frozen character-count constant drift")

    from hashlib import sha256

    observed_sha256 = sha256(composite.encode("utf-8")).hexdigest()
    if identity.get("raw_sha256") != observed_sha256:
        raise ValueError("frozen Running on Waves body identity drift for SHA-256")
    if observed_sha256 != FROZEN_BODY_SHA256:
        raise ValueError("Running on Waves frozen body SHA-256 constant drift")


def _variant_ranking(policy: Mapping[str, object]) -> list[dict[str, object]]:
    variants = policy.get("author_text_inside_dialogue_variants")
    if not isinstance(variants, Mapping):
        raise ValueError("dialogue policy diagnostic missing variants")

    rows: list[dict[str, object]] = []
    for variant_id, raw_row in variants.items():
        if not isinstance(raw_row, Mapping):
            raise ValueError(f"invalid dialogue policy row: {variant_id}")
        value = raw_row.get("value")
        delta = raw_row.get("delta_to_reference")
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"dialogue policy variant has no numeric value: {variant_id}")
        if not isinstance(delta, (int, float)) or isinstance(delta, bool):
            raise ValueError(f"dialogue policy variant has no numeric delta: {variant_id}")
        rows.append(
            {
                "variant_id": str(variant_id),
                "value_percent": value,
                "delta_to_fantlab_display_percentage_points": delta,
                "absolute_delta_percentage_points": abs(delta),
            }
        )
    rows.sort(key=lambda row: (row["absolute_delta_percentage_points"], row["variant_id"]))
    return rows


def build_diagnostic(
    source_manifest: Mapping[str, object],
    body_manifest: Mapping[str, object],
    *,
    fetcher: Callable[
        [Iterable[Mapping[str, object]]], dict[str, str]
    ] = fetch_pinned_chapter_revisions,
    enforce_canonical_body: bool = True,
) -> dict[str, object]:
    """Replay the frozen body and return source-free dialogue sensitivity evidence."""

    validate_body_manifest(body_manifest, source_manifest)
    _, bodies = _extract_bodies(source_manifest, fetcher=fetcher)
    composite = CHAPTER_SEPARATOR.join(bodies)
    if enforce_canonical_body:
        _verify_composite_identity(composite, body_manifest)

    policy = analyze_dialogue_policy(
        composite,
        expected_dialogue_share_percent=FANTLAB_DIALOGUE_SHARE_PERCENT,
        expected_author_text_inside_dialogue_percent=(
            FANTLAB_AUTHOR_TEXT_INSIDE_DIALOGUE_PERCENT
        ),
    )

    return {
        "diagnostic_version": DIAGNOSTIC_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_text_committed": False,
        "body_identity": {
            "manifest_version": BODY_MANIFEST_VERSION,
            "character_count_including_spaces": body_manifest["composite_identity"][
                "character_count_including_spaces"
            ],
            "raw_sha256": body_manifest["composite_identity"]["raw_sha256"],
        },
        "fantlab": {
            "work_id": FANTLAB_WORK_ID,
            "analysis_url": FANTLAB_ANALYSIS_URL,
            "analysis_date": FANTLAB_ANALYSIS_DATE,
            "displayed_dialogue_share_percent": FANTLAB_DIALOGUE_SHARE_PERCENT,
            "displayed_author_text_inside_dialogue_percent": (
                FANTLAB_AUTHOR_TEXT_INSIDE_DIALOGUE_PERCENT
            ),
            "source_edition_disclosed": False,
            "source_bytes_disclosed": False,
        },
        "probe": policy,
        "author_text_variant_distance_ranking": _variant_ranking(policy),
        "interpretation": {
            "production_dialogue_profile_changed": False,
            "closest_variant_is_not_a_semantics_selection": True,
            "numeric_proximity_cannot_establish_fantlab_grammar": True,
            "numeric_proximity_cannot_establish_source_identity": True,
        },
        "gates": {
            "general_calibration_profile_admissible": True,
            "fantlab_source_edition_match": "unknown",
            "diagnostic_ready": True,
            "gate_ready": False,
            "m2_parity_admissible": False,
            "m2_weight": 0,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Replay Running on Waves and emit source-free dialogue policy sensitivity."
    )
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--body-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    artifact = build_diagnostic(
        _load_object(args.source_manifest),
        _load_object(args.body_manifest),
    )
    text = json.dumps(artifact, ensure_ascii=False, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
