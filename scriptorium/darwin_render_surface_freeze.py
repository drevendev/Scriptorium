"""Materialize the durable source-free Darwin rendering-surface freeze.

The hosted audit keeps per-Page receipts only as transient CI evidence. This module
reduces that evidence to a compact deterministic manifest containing construct shapes,
aggregate counts, and one digest over the 388 per-Page source-free receipts.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from .darwin_render_surface import (
    CANDIDATE_ID,
    EXPECTED_LITERARY_PAGE_COUNT,
    PROFILE_STATUS,
    validate_audit_manifest,
)

FREEZE_VERSION = "scriptorium-darwin-render-surface-freeze-v1"


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def build_freeze_manifest(audit: Mapping[str, object]) -> dict[str, object]:
    """Reduce a validated hosted audit to deterministic source-free durable evidence."""

    validate_audit_manifest(audit)
    pages = audit["page_surface_receipts"]
    assert isinstance(pages, list)
    manifest: dict[str, object] = {
        "schema_version": FREEZE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "status": PROFILE_STATUS,
        "source_revision_index_sha256": audit["source_revision_index_sha256"],
        "literary_dependency_count": audit["literary_dependency_count"],
        "identity_replay_match": audit["identity_replay_match"],
        "source_text_included": False,
        "template_shapes": audit["template_shapes"],
        "tag_shapes": audit["tag_shapes"],
        "construct_totals": audit["construct_totals"],
        "page_surface_receipts_count": len(pages),
        "page_surface_receipts_sha256": _sha256_json(pages),
        "rendering_profile_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    manifest["freeze_manifest_sha256"] = _sha256_json(manifest)
    return manifest


def validate_freeze_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("schema_version") != FREEZE_VERSION:
        raise ValueError("Darwin rendering-surface freeze schema drift")
    if manifest.get("candidate_id") != CANDIDATE_ID or manifest.get("status") != PROFILE_STATUS:
        raise ValueError("Darwin rendering-surface freeze identity/status drift")
    if manifest.get("literary_dependency_count") != EXPECTED_LITERARY_PAGE_COUNT:
        raise ValueError("Darwin rendering-surface freeze literary dependency drift")
    if manifest.get("page_surface_receipts_count") != EXPECTED_LITERARY_PAGE_COUNT:
        raise ValueError("Darwin rendering-surface freeze receipt count drift")
    if manifest.get("identity_replay_match") is not True or manifest.get("source_text_included") is not False:
        raise ValueError("Darwin rendering-surface freeze source boundary drift")
    for key in (
        "rendering_profile_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    ):
        if manifest.get(key) is not False:
            raise ValueError(f"{key} must remain false in rendering-surface freeze")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")
    for key in ("template_shapes", "tag_shapes", "construct_totals"):
        if key not in manifest:
            raise ValueError(f"missing rendering-surface freeze field: {key}")
    digest = manifest.get("freeze_manifest_sha256")
    unsigned = dict(manifest)
    unsigned.pop("freeze_manifest_sha256", None)
    if digest != _sha256_json(unsigned):
        raise ValueError("Darwin rendering-surface freeze digest drift")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    audit = json.loads(args.input.read_text(encoding="utf-8"))
    manifest = build_freeze_manifest(audit)
    validate_freeze_manifest(manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(manifest["freeze_manifest_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
