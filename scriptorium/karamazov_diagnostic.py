"""Measure pinned Brothers Karamazov fields without retaining source text.

This is a diagnostic against a different, source-unmatched public transcription,
not a FantLab parity claim. Only two independently retained public count fields
have expected values; all other FantLab references remain unknown.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from . import karamazov_freeze as freeze
from .metrics import METRIC_CONTRACT_ID, SCHEMA_VERSION, analyze_deterministic_metrics
from .wikisource_replay import fetch_pinned_chapter_revisions

DIAGNOSTIC_VERSION = "scriptorium-karamazov-field-diagnostic-v1"
FROZEN_BODY_CHARACTERS = 1_810_351
FROZEN_BODY_SHA256 = "26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6"
FANTLAB_REFERENCES = {
    "fantlab.general.characters": "1807107",
    "fantlab.general.words": "281507",
}
FANTLAB_URL = "https://fantlab.ru/work168951/lp"
FANTLAB_DATE = "2022-09-18"
_UNBOUND = frozenset({
    "fantlab.vocabulary.active_dictionary",
    "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000",
    "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})
_OPTIONAL_NO_OBSERVATIONS = frozenset({
    "fantlab.dialogue.mean_narration_sentence_length_chars",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars",
    "fantlab.dialogue.author_text_inside_dialogue_percent",
})


def _pinned_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    identities = freeze._validate_manifest(manifest)
    body = manifest["composite_identity"]
    if not isinstance(body, dict) or (
        body.get("raw_sha256") != FROZEN_BODY_SHA256
        or body.get("normalized_sha256") != FROZEN_BODY_SHA256
        or body.get("character_count_including_spaces") != FROZEN_BODY_CHARACTERS
        or body.get("normalized_character_count_including_spaces") != FROZEN_BODY_CHARACTERS
        or len(identities) != freeze.SOURCE_SEGMENT_COUNT
    ):
        raise ValueError("Karamazov manifest does not match canonical frozen pins")
    return identities


def build_diagnostic(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Replay all 98 pinned source segments and return only 29 derived fields."""
    identities = _pinned_manifest(manifest)
    titles = {str(row["title"]) for row in identities}
    captured: dict[str, str] = {}

    def capture(rows: Iterable[Mapping[str, object]]) -> dict[str, str]:
        result = fetcher(rows)
        if (not isinstance(result, dict) or set(result) != titles
                or any(not isinstance(text, str) for text in result.values())):
            raise ValueError("Karamazov replay source inventory mismatch")
        captured.update(result)
        return result

    receipt = freeze.replay_manifest(manifest, fetcher=capture)
    if (receipt.get("source_text_included") is not False
            or receipt.get("m2_parity_admissible") is not False
            or receipt.get("source_segment_count") != freeze.SOURCE_SEGMENT_COUNT):
        raise ValueError("Karamazov source-free replay receipt drift")

    # The replay above validates each pinned revision plus the full composite.
    # Re-extract only after that validation, without serializing source prose.
    body = "\n\n".join(
        freeze.extract_karamazov_body(
            captured[str(row["title"])], kind=str(row["kind"])
        )
        for row in identities
    )
    if (len(body) != FROZEN_BODY_CHARACTERS
            or sha256(body.encode("utf-8")).hexdigest() != FROZEN_BODY_SHA256):
        raise ValueError("Karamazov measured body differs from canonical pins")
    analysis = analyze_deterministic_metrics(body)
    if (analysis.get("schema_version") != SCHEMA_VERSION
            or analysis.get("metric_contract_id") != METRIC_CONTRACT_ID
            or analysis.get("normalized_sha256") != FROZEN_BODY_SHA256
            or analysis.get("dependencies", {}).get("vocabulary_dictionary") is not None):
        raise ValueError("Karamazov metric identity or dependency drift")

    values = analysis.get("metrics")
    if not isinstance(values, dict) or len(values) != 29:
        raise ValueError("expected 29 deterministic Karamazov metric fields")
    if not (_UNBOUND | FANTLAB_REFERENCES.keys()) <= values.keys():
        raise ValueError("Karamazov required metric inventory missing")

    rows: list[dict[str, object]] = []
    for metric_id, metric in sorted(values.items()):
        if not isinstance(metric, dict):
            raise ValueError("Karamazov invalid metric record")
        value = metric.get("value")
        unit = metric.get("unit")
        status = metric.get("compatibility_status")
        if (not isinstance(unit, str) or not unit
                or status not in ("inferred", "extension")
                or (value is not None and
                    (type(value) not in (int, float) or not math.isfinite(value)))):
            raise ValueError("Karamazov invalid value, unit or compatibility status")
        reference = FANTLAB_REFERENCES.get(metric_id)
        if metric_id in _UNBOUND:
            if value is not None:
                raise ValueError("Karamazov dictionary-unbound metric measured unexpectedly")
            result = "NOT_RUN_DICTIONARY_UNBOUND"
        elif value is None:
            if metric_id not in _OPTIONAL_NO_OBSERVATIONS:
                raise ValueError("Karamazov required metric unexpectedly unknown")
            result = "UNAVAILABLE_NO_OBSERVATIONS"
        else:
            result = ("DIAGNOSTIC_SOURCE_UNMATCHED" if reference is not None
                      else "MEASURED_REFERENCE_UNAVAILABLE")
        if reference is not None and type(value) is not int:
            raise ValueError("Karamazov displayed integral reference requires an integer actual")
        rows.append({
            "metric_id": metric_id,
            "actual": value,
            "unit": unit,
            "compatibility_status": status,
            "fantlab_display": reference,
            "actual_minus_fantlab_display": value - int(reference) if reference is not None else None,
            "result": result,
        })
    if next(r["actual"] for r in rows if r["metric_id"] == "fantlab.general.characters") != FROZEN_BODY_CHARACTERS:
        raise ValueError("Karamazov measured character count drift")
    return {
        "diagnostic_version": DIAGNOSTIC_VERSION,
        "candidate_id": freeze.CANDIDATE_ID,
        "source_text_committed": False,
        "body_identity": {
            "source_segment_count": freeze.SOURCE_SEGMENT_COUNT,
            "character_count_including_spaces": FROZEN_BODY_CHARACTERS,
            "raw_sha256": FROZEN_BODY_SHA256,
            "normalized_sha256": FROZEN_BODY_SHA256,
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
    """Create-only receipt, never overwrite a prior measured observation."""
    with path.open("x", encoding="utf-8") as stream:
        stream.write(render_json(artifact))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Karamazov revision manifest must be a JSON object")
    artifact = build_diagnostic(manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_new(args.output, artifact)
    print("KARAMAZOV_DIAGNOSTIC=" + json.dumps({
        "rows": len(artifact["metric_rows"]),
        "measured": sum(r["actual"] is not None for r in artifact["metric_rows"]),
        "public_references": len(FANTLAB_REFERENCES),
        "m2_weight": 0, "source_text_committed": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
