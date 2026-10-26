"""Replay the frozen Silver Dove source into a source-free diagnostic, not parity.

This is an incremental measurement run: only two FantLab display counts have
independently retained public references. Other calculated values are shown
without invented reference values or rounding rules. No literary bytes leave
the transient runtime or enter the JSON receipt.
"""
from __future__ import annotations

import argparse
from decimal import Decimal
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from . import silver_dove_freeze as freeze
from .metrics import analyze_deterministic_metrics, METRIC_CONTRACT_ID, SCHEMA_VERSION
from .wikisource_replay import fetch_pinned_chapter_revisions

DIAGNOSTIC_VERSION = "scriptorium-silver-dove-field-diagnostic-v1"
FROZEN_BODY_CHARACTERS = 563_125
FROZEN_BODY_SHA256 = "496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183"
FROZEN_WIKITEXT_SHA256 = "a611080e4dd1295336c3d8c7c78fc7a077608b247c9e96d7ae0a989fc256381a"
FANTLAB_REFERENCES = {
    "fantlab.general.characters": "549050",
    "fantlab.general.words": "83369",
}
FANTLAB_URL = "https://fantlab.ru/work293515/lp"
FANTLAB_DATE = "2022-09-19"
_OPTIONAL_NO_OBSERVATIONS = frozenset({
    "fantlab.dialogue.mean_narration_sentence_length_chars",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars",
    "fantlab.dialogue.author_text_inside_dialogue_percent",
})
_UNBOUND = frozenset({
    "fantlab.vocabulary.active_dictionary",
    "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000",
    "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})


def _pinned_manifest(manifest: Mapping[str, object]) -> Mapping[str, object]:
    freeze._validate_manifest(manifest)
    identity = manifest["composite_identity"]
    source = manifest["source_identity"]
    if not isinstance(identity, dict) or not isinstance(source, dict):
        raise ValueError("Silver Dove source or body identity missing")
    if (
        identity.get("raw_sha256") != FROZEN_BODY_SHA256
        or identity.get("normalized_sha256") != FROZEN_BODY_SHA256
        or identity.get("character_count_including_spaces") != FROZEN_BODY_CHARACTERS
        or identity.get("normalized_character_count_including_spaces") != FROZEN_BODY_CHARACTERS
        or source.get("wikitext_sha256") != FROZEN_WIKITEXT_SHA256
    ):
        raise ValueError("Silver Dove manifest does not match the retained canonical pins")
    return identity


def build_diagnostic(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Replay pinned Wikisource bytes transiently and measure 29 inferred fields."""
    identity = _pinned_manifest(manifest)
    captured: dict[str, str] = {}

    def capture(identities: Iterable[Mapping[str, object]]) -> dict[str, str]:
        revisions = fetcher(identities)
        if not isinstance(revisions, dict) or set(revisions) != {freeze.WORK_TITLE}:
            raise ValueError("Silver Dove replay returned an unexpected source inventory")
        if not isinstance(revisions[freeze.WORK_TITLE], str):
            raise ValueError("Silver Dove pinned page is not text")
        captured.update(revisions)
        return revisions

    # Existing replay validates the exact source revision, wikitext SHA, legal
    # profile, extracted characters and both composite SHA-256 identities.
    receipt = freeze.replay_manifest(manifest, fetcher=capture)
    if receipt.get("source_text_included") is not False:
        raise ValueError("source-free Silver Dove replay contract drift")
    body = freeze.extract_silver_dove_body(captured[freeze.WORK_TITLE])
    if sha256(body.encode("utf-8")).hexdigest() != FROZEN_BODY_SHA256:
        raise ValueError("replayed Silver Dove body differs from canonical pins")
    analysis = analyze_deterministic_metrics(body)
    if (
        analysis.get("schema_version") != SCHEMA_VERSION
        or analysis.get("metric_contract_id") != METRIC_CONTRACT_ID
        or analysis.get("normalized_sha256") != identity["normalized_sha256"]
        or analysis.get("dependencies", {}).get("vocabulary_dictionary") is not None
    ):
        raise ValueError("Silver Dove analyzer profile, normalized text, or dependency drift")

    metrics = analysis.get("metrics")
    if not isinstance(metrics, dict) or len(metrics) != 29:
        raise ValueError("expected all 29 deterministic Silver Dove metrics")
    if set(metrics).intersection(FANTLAB_REFERENCES) != set(FANTLAB_REFERENCES):
        raise ValueError("Silver Dove reference metric missing")
    if not _UNBOUND.issubset(metrics):
        raise ValueError("Silver Dove unbound dictionary metric missing")
    rows: list[dict[str, object]] = []
    for metric_id in sorted(metrics):
        metric = metrics[metric_id]
        if not isinstance(metric, dict):
            raise ValueError("invalid Silver Dove metric record")
        value, unit, compatibility = (
            metric.get("value"), metric.get("unit"), metric.get("compatibility_status")
        )
        if not isinstance(unit, str) or not unit or compatibility not in ("inferred", "extension"):
            raise ValueError("invalid Silver Dove metric units or compatibility")
        if value is not None and (
            type(value) not in (int, float)
            or not math.isfinite(value)
        ):
            raise ValueError("invalid/nonfinite Silver Dove metric value")
        reference = FANTLAB_REFERENCES.get(metric_id)
        if metric_id in _UNBOUND:
            if value is not None:
                raise ValueError("unbound dictionary produced a Silver Dove value")
            status = "NOT_RUN_DICTIONARY_UNBOUND"
        elif value is None:
            if metric_id not in _OPTIONAL_NO_OBSERVATIONS:
                raise ValueError("required Silver Dove metric is unexpectedly unknown")
            status = "UNAVAILABLE_NO_OBSERVATIONS"
        else:
            status = (
                "DIAGNOSTIC_SOURCE_UNMATCHED"
                if reference is not None else "MEASURED_REFERENCE_UNAVAILABLE"
            )
        delta: int | None = None
        if reference is not None:
            if type(value) is not int:
                raise ValueError("public integral-count reference requires an integral measured value")
            delta = value - int(reference)
        rows.append({
            "metric_id": metric_id,
            "actual": value,
            "unit": unit,
            "compatibility_status": compatibility,
            "fantlab_display": reference,
            "actual_minus_fantlab_display": delta,
            "result": status,
        })

    if next(row["actual"] for row in rows if row["metric_id"] == "fantlab.general.characters") != FROZEN_BODY_CHARACTERS:
        raise ValueError("Silver Dove measured character count does not match frozen body")
    return {
        "diagnostic_version": DIAGNOSTIC_VERSION,
        "candidate_id": freeze.CANDIDATE_ID,
        "source_text_committed": False,
        "body_identity": {
            "revision_id": freeze.SOURCE_REVISION_ID,
            "character_count_including_spaces": FROZEN_BODY_CHARACTERS,
            "raw_sha256": FROZEN_BODY_SHA256,
            "normalized_sha256": identity["normalized_sha256"],
        },
        "scriptorium": {
            "schema_version": analysis["schema_version"],
            "metric_contract_id": analysis["metric_contract_id"],
            "profiles": analysis["profiles"],
            "vocabulary_dictionary_dependency": None,
        },
        "fantlab": {
            "analysis_url": FANTLAB_URL,
            "analysis_date": FANTLAB_DATE,
            "public_display_references_retained": dict(FANTLAB_REFERENCES),
            "source_edition_disclosed": False,
            "source_bytes_disclosed": False,
        },
        "comparison_policy": {
            "class": "diagnostic_unmatched_source",
            "available_reference_fields": 2,
            "other_reference_fields": "NOT_RETAINED",
            "rounding_evidence": "UNKNOWN",
            "numeric_similarity_does_not_prove_source_identity": True,
        },
        "metric_rows": rows,
        "gates": {
            "calibration_size_met": True,
            "fantlab_source_edition_match": "unknown",
            "m2_parity_admissible": False,
            "m2_weight": 0,
        },
    }


def render_json(artifact: Mapping[str, object]) -> str:
    return json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"


def write_new(path: Path, artifact: Mapping[str, object]) -> None:
    """Create-only source-free receipt; do not overwrite an earlier observation."""
    rendered = render_json(artifact)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(rendered)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Measure the frozen Silver Dove source without retaining literary prose")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Silver Dove revision manifest must be a JSON object")
    artifact = build_diagnostic(manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_new(args.output, artifact)
    print("SILVER_DOVE_DIAGNOSTIC=" + json.dumps({
        "metric_rows": len(artifact["metric_rows"]),
        "measured_rows": sum(row["actual"] is not None for row in artifact["metric_rows"]),
        "reference_fields": 2,
        "m2_weight": 0,
        "source_text_committed": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
