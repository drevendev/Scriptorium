"""Diagnostic-only analysis of pylem's pinned literature homonym weights.

The exact pylem 0.0.18 wrapper exposes homonym/word weights and prediction flags for
individual analyses.  This module measures whether those provider-side signals separate
direct cross-bucket ambiguities on a frozen work.  It never uses the signal to resolve a
token and never claims that FantLab used the same statistics or selection rule.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from typing import Final, Mapping, Sequence

from .morphology import DIRECT_RUNTIME_TO_BUCKET
from .morphology_diagnostic import classify_runtime_candidates
from .pylem_transport import consume_sidecar_response
from .text import NORMALIZATION_PROFILE

CANDIDATE_METADATA_SCHEMA: Final = "scriptorium-pylem-candidate-metadata-v1"
DIAGNOSTIC_SCHEMA: Final = "scriptorium-pylem-homonym-weight-diagnostic-v1"
PINNED_MORPH_DICT_REVISION: Final = "4c5e9b6d048d1ba74e02988593b23fb0cbc87772"


def _optional_int(value: object, *, field: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer or null")
    return value


def _validated_metadata_rows(
    request: Mapping[str, object],
    response: Mapping[str, object],
) -> tuple[tuple[dict[str, object], ...], ...]:
    """Validate candidate metadata after the base sidecar transport is accepted."""
    consume_sidecar_response(request, response)
    if response.get("candidate_metadata_schema") != CANDIDATE_METADATA_SCHEMA:
        raise ValueError("unexpected pylem candidate metadata schema")

    response_rows = response.get("rows")
    if not isinstance(response_rows, list):
        raise ValueError("sidecar response token rows must be an array")

    validated_rows: list[tuple[dict[str, object], ...]] = []
    for response_row in response_rows:
        if not isinstance(response_row, Mapping):
            raise ValueError("sidecar response token row must be an object")
        runtime_pos = response_row.get("runtime_pos")
        metadata = response_row.get("candidate_metadata")
        if not isinstance(runtime_pos, list) or not isinstance(metadata, list):
            raise ValueError("sidecar candidate metadata must align with runtime_pos")
        if len(metadata) != len(runtime_pos):
            raise ValueError("sidecar candidate metadata length mismatch")

        row: list[dict[str, object]] = []
        for index, (runtime_value, metadata_value) in enumerate(zip(runtime_pos, metadata)):
            if not isinstance(metadata_value, Mapping):
                raise ValueError("sidecar candidate metadata entry must be an object")
            if metadata_value.get("runtime_pos") != runtime_value:
                raise ValueError("sidecar candidate metadata runtime_pos mismatch")
            predicted = metadata_value.get("predicted")
            if not isinstance(predicted, bool):
                raise ValueError("candidate predicted flag must be boolean")
            row.append(
                {
                    "runtime_pos": runtime_value,
                    "predicted": predicted,
                    "homonym_weight": _optional_int(
                        metadata_value.get("homonym_weight"),
                        field=f"candidate[{index}].homonym_weight",
                    ),
                    "word_weight": _optional_int(
                        metadata_value.get("word_weight"),
                        field=f"candidate[{index}].word_weight",
                    ),
                }
            )
        validated_rows.append(tuple(row))
    return tuple(validated_rows)


def _metadata_digest(rows: tuple[tuple[dict[str, object], ...], ...]) -> str:
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def analyze_homonym_weight_signal(
    request: Mapping[str, object],
    response: Mapping[str, object],
) -> dict[str, object]:
    """Aggregate pylem homonym-weight evidence for direct cross-bucket ambiguity."""
    rows = _validated_metadata_rows(request, response)
    runtime_rows = tuple(tuple(str(item["runtime_pos"]) for item in row) for row in rows)

    direct_ambiguity_count = 0
    complete_weight_count = 0
    missing_weight_count = 0
    unique_max_bucket_count = 0
    tied_max_bucket_count = 0
    unique_positive_max_bucket_count = 0
    all_bucket_max_zero_count = 0
    any_predicted_count = 0
    all_predicted_count = 0
    nominated_buckets: Counter[str] = Counter()
    signature_rows: dict[str, Counter[str]] = {}

    for runtime_row, metadata_row in zip(runtime_rows, rows):
        if classify_runtime_candidates(runtime_row) != "direct_cross_bucket_ambiguity":
            continue
        direct_ambiguity_count += 1
        if any(bool(item["predicted"]) for item in metadata_row):
            any_predicted_count += 1
        if metadata_row and all(bool(item["predicted"]) for item in metadata_row):
            all_predicted_count += 1

        buckets = sorted({DIRECT_RUNTIME_TO_BUCKET[value] for value in runtime_row})
        signature = "|".join(buckets)
        stats = signature_rows.setdefault(signature, Counter())
        stats["row_count"] += 1

        weights = [item["homonym_weight"] for item in metadata_row]
        if any(weight is None for weight in weights):
            missing_weight_count += 1
            stats["missing_weight_count"] += 1
            continue
        complete_weight_count += 1
        stats["complete_weight_count"] += 1

        bucket_max: dict[str, int] = {}
        for item in metadata_row:
            bucket = DIRECT_RUNTIME_TO_BUCKET[str(item["runtime_pos"])]
            weight = int(item["homonym_weight"])
            bucket_max[bucket] = max(bucket_max.get(bucket, weight), weight)
        maximum = max(bucket_max.values())
        winners = sorted(bucket for bucket, weight in bucket_max.items() if weight == maximum)
        if all(weight == 0 for weight in bucket_max.values()):
            all_bucket_max_zero_count += 1
            stats["all_bucket_max_zero_count"] += 1
        if len(winners) == 1:
            unique_max_bucket_count += 1
            stats["unique_max_bucket_count"] += 1
            nominated_buckets[winners[0]] += 1
            if maximum > 0:
                unique_positive_max_bucket_count += 1
                stats["unique_positive_max_bucket_count"] += 1
        else:
            tied_max_bucket_count += 1
            stats["tied_max_bucket_count"] += 1

    if complete_weight_count + missing_weight_count != direct_ambiguity_count:
        raise AssertionError("homonym-weight availability partition mismatch")
    if unique_max_bucket_count + tied_max_bucket_count != complete_weight_count:
        raise AssertionError("homonym-weight winner partition mismatch")

    return {
        "schema_version": DIAGNOSTIC_SCHEMA,
        "status": "diagnostic_only",
        "candidate_metadata_schema": CANDIDATE_METADATA_SCHEMA,
        "candidate_metadata_sha256": _metadata_digest(rows),
        "direct_cross_bucket_ambiguity_count": direct_ambiguity_count,
        "homonym_weight_complete_count": complete_weight_count,
        "homonym_weight_missing_count": missing_weight_count,
        "unique_max_bucket_count": unique_max_bucket_count,
        "unique_max_bucket_percent_of_complete": _percent(
            unique_max_bucket_count, complete_weight_count
        ),
        "tied_max_bucket_count": tied_max_bucket_count,
        "unique_positive_max_bucket_count": unique_positive_max_bucket_count,
        "all_bucket_max_zero_count": all_bucket_max_zero_count,
        "rows_with_any_predicted_analysis": any_predicted_count,
        "rows_with_all_predicted_analyses": all_predicted_count,
        "unique_max_nominated_bucket_counts": dict(sorted(nominated_buckets.items())),
        "bucket_signature_signal": {
            signature: dict(sorted(counts.items()))
            for signature, counts in sorted(signature_rows.items())
        },
        "evidence_boundary": {
            "provider_signal": "pinned_aot_literature_homonym_weight",
            "pinned_morph_dict_revision": PINNED_MORPH_DICT_REVISION,
            "production_homonym_selection_changed": False,
            "fantlab_homonym_selection": "unresolved",
            "fantlab_dictionary_equivalence": "unknown",
            "source_match_required_for_policy_attribution": True,
            "m2_parity_admissible": False,
        },
    }


def build_frozen_homonym_weight_diagnostic(
    request: Mapping[str, object],
    response: Mapping[str, object],
    manifest: Mapping[str, object],
    *,
    scriptorium_revision: str,
) -> dict[str, object]:
    composite_identity = manifest.get("composite_identity")
    candidate_id = manifest.get("candidate_id")
    if not isinstance(composite_identity, Mapping):
        raise ValueError("packed manifest missing composite_identity")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("packed manifest missing candidate_id")
    if composite_identity.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError("packed manifest normalization profile mismatch")
    if request.get("normalized_sha256") != composite_identity.get("normalized_sha256"):
        raise ValueError("homonym-weight request is not bound to frozen manifest identity")

    signal = analyze_homonym_weight_signal(request, response)
    return {
        "schema_version": "scriptorium-frozen-homonym-weight-diagnostic-v1",
        "candidate_id": candidate_id,
        "scriptorium_revision": scriptorium_revision,
        "normalized_sha256": request["normalized_sha256"],
        "source_text_included": False,
        "signal": signal,
        "diagnostic_boundary": {
            "status": "diagnostic_only",
            "fantlab_source_edition_match": "unknown",
            "fantlab_dictionary_equivalence": "unknown",
            "fantlab_homonym_selection": "unresolved",
            "production_resolution_changed": False,
            "m2_parity_admissible": False,
        },
    }


def _percent(part: int, whole: int) -> float | None:
    if whole == 0:
        return None
    return part * 100.0 / whole


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--scriptorium-revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    artifact = build_frozen_homonym_weight_diagnostic(
        _load_object(args.request),
        _load_object(args.response),
        _load_object(args.manifest),
        scriptorium_revision=args.scriptorium_revision,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
