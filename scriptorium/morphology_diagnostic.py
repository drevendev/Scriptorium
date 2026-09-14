"""Source-free diagnostics for conservative pylem/FantLab POS investigation.

This module explains why ``scriptorium-pos-v1`` leaves a token undefined without
recovering, folding or selecting any morphology that the compatibility contract keeps
unresolved.  The output is diagnostic evidence only; it is never a FantLab parity
claim.
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Final

from .morphology import DIRECT_RUNTIME_TO_BUCKET, resolve_runtime_pos
from .pylem_provider import KNOWN_RUNTIME_POS

DIAGNOSTIC_SCHEMA: Final = "scriptorium-pos-undefined-diagnostic-v1"
N_RUNTIME_POS: Final = "N"
EXTRA_UNRESOLVED_RUNTIME_POS: Final = frozenset(
    KNOWN_RUNTIME_POS - frozenset(DIRECT_RUNTIME_TO_BUCKET) - {N_RUNTIME_POS}
)
UNDEFINED_REASONS: Final = (
    "no_analysis",
    "runtime_n_only",
    "runtime_n_mixed",
    "extra_runtime_only",
    "extra_runtime_mixed",
    "direct_cross_bucket_ambiguity",
)


def classify_runtime_candidates(candidates: Iterable[str]) -> str:
    """Classify one validated runtime-candidate row without guessing a resolution."""
    values = tuple(candidates)
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("runtime POS diagnostic values must be non-empty strings")
        if value not in KNOWN_RUNTIME_POS:
            raise ValueError(f"unknown runtime POS value in diagnostic: {value!r}")

    if resolve_runtime_pos(values) is not None:
        return "defined"
    if not values:
        return "no_analysis"

    unique = frozenset(values)
    if unique == {N_RUNTIME_POS}:
        return "runtime_n_only"
    if N_RUNTIME_POS in unique:
        return "runtime_n_mixed"
    if unique <= EXTRA_UNRESOLVED_RUNTIME_POS:
        return "extra_runtime_only"
    if unique & EXTRA_UNRESOLVED_RUNTIME_POS:
        return "extra_runtime_mixed"
    return "direct_cross_bucket_ambiguity"


def decompose_runtime_candidates(
    candidate_rows: Iterable[Iterable[str]],
) -> dict[str, object]:
    """Return aggregate, source-free reasons for conservative undefined tokens."""
    rows = tuple(tuple(row) for row in candidate_rows)
    reason_counts: Counter[str] = Counter()
    unresolved_presence: Counter[str] = Counter()
    direct_ambiguity_sets: Counter[str] = Counter()

    for row in rows:
        reason = classify_runtime_candidates(row)
        reason_counts[reason] += 1
        if reason == "defined":
            continue

        unique = frozenset(row)
        for runtime_pos in unique & ({N_RUNTIME_POS} | EXTRA_UNRESOLVED_RUNTIME_POS):
            unresolved_presence[runtime_pos] += 1

        if reason == "direct_cross_bucket_ambiguity":
            buckets = sorted({DIRECT_RUNTIME_TO_BUCKET[value] for value in unique})
            direct_ambiguity_sets["|".join(buckets)] += 1

    defined_count = reason_counts["defined"]
    undefined_reason_counts = {reason: reason_counts[reason] for reason in UNDEFINED_REASONS}
    undefined_count = sum(undefined_reason_counts.values())
    if defined_count + undefined_count != len(rows):
        raise AssertionError("POS diagnostic reason partition does not cover every token")

    provider_no_analysis_count = undefined_reason_counts["no_analysis"]
    policy_blocked_count = undefined_count - provider_no_analysis_count
    return {
        "schema_version": DIAGNOSTIC_SCHEMA,
        "status": "diagnostic_only",
        "token_count": len(rows),
        "defined_count": defined_count,
        "undefined_count": undefined_count,
        "undefined_reason_counts": undefined_reason_counts,
        "known_conservative_policy_blocked_count": policy_blocked_count,
        "known_conservative_policy_blocked_percent_of_undefined": _percent(
            policy_blocked_count, undefined_count
        ),
        "provider_no_analysis_count": provider_no_analysis_count,
        "provider_no_analysis_percent_of_undefined": _percent(
            provider_no_analysis_count, undefined_count
        ),
        "unresolved_runtime_pos_token_presence": {
            runtime_pos: unresolved_presence[runtime_pos]
            for runtime_pos in sorted({N_RUNTIME_POS} | EXTRA_UNRESOLVED_RUNTIME_POS)
        },
        "direct_ambiguity_bucket_set_counts": dict(sorted(direct_ambiguity_sets.items())),
        "classification_boundary": {
            "reason_precedence": list(UNDEFINED_REASONS),
            "runtime_n_semantics": "noun_cardinal_collision_unresolved",
            "extra_category_folding": "unresolved",
            "direct_homonym_selection": "unresolved",
            "no_analysis_interpretation": "provider_dictionary_or_prediction_coverage_unresolved",
            "fantlab_parity_claim": False,
        },
    }


def build_fantlab_pos_accounting(
    expected: Mapping[str, object],
    pos_artifact: Mapping[str, object],
) -> dict[str, object]:
    """Compare only integer POS partition accounting, never morphology semantics."""
    expected_words = _required_int(expected, "words")
    expected_defined = _required_int(expected, "defined_pos_words")
    expected_undefined = _required_int(expected, "undefined_pos_words")
    if expected_defined + expected_undefined != expected_words:
        raise ValueError("FantLab defined/undefined POS counts do not sum to word count")

    input_row = pos_artifact.get("input")
    metrics = pos_artifact.get("metrics")
    if not isinstance(input_row, Mapping) or not isinstance(metrics, Mapping):
        raise ValueError("POS artifact missing input/metrics accounting")
    actual_words = _required_int(input_row, "word_count")
    defined_row = metrics.get("defined")
    undefined_row = metrics.get("undefined")
    if not isinstance(defined_row, Mapping) or not isinstance(undefined_row, Mapping):
        raise ValueError("POS artifact missing defined/undefined accounting")
    actual_defined = _required_int(defined_row, "count")
    actual_undefined = _required_int(undefined_row, "count")
    if actual_defined + actual_undefined != actual_words:
        raise ValueError("Scriptorium defined/undefined POS counts do not sum to word count")

    return {
        "status": "diagnostic_only",
        "source_match_required_for_attribution": True,
        "word_count": _delta_row(expected_words, actual_words),
        "defined_pos_words": _delta_row(expected_defined, actual_defined),
        "undefined_pos_words": _delta_row(expected_undefined, actual_undefined),
        "interpretation": (
            "Count deltas are diagnostic accounting only. They combine source/tokenization "
            "differences with conservative morphology resolution and cannot be attributed "
            "to FantLab behavior while analyzer-input identity is unknown."
        ),
    }


def _required_int(mapping: Mapping[str, object], key: str) -> int:
    value = mapping.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    return value


def _delta_row(expected: int, actual: int) -> dict[str, int]:
    return {"expected": expected, "actual": actual, "delta": actual - expected}


def _percent(part: int, whole: int) -> float | None:
    if whole == 0:
        return None
    return part * 100.0 / whole
