"""Fail-closed, source-free POS join for a FantLab benchmark comparison.

The 17 displayed FantLab categories do not form a proven partition of its
'defined' count (the retained work488 counts actually sum to more than 100%).
Never treat numeric agreement here as reproduced morphology/parity.
"""
from __future__ import annotations

import json
import math
from collections.abc import Mapping
from typing import Final

from .metrics import METRIC_CONTRACT_ID
from .morphology import (
    FANTLAB_POS_BUCKETS,
    MAX_POSITION,
    POS_MAPPING_CONTRACT,
    POS_PROFILE,
    POS_SCHEMA_VERSION,
)
from .text import NORMALIZATION_PROFILE

POS_BENCHMARK_BOUNDARY: Final = (
    "POS compatibility is unproven: FantLab's dictionary, homonym selection, "
    "runtime N noun/cardinal collision and omitted category folding are unresolved."
)
_HEX = frozenset("0123456789abcdef")
_BUCKETS = frozenset(FANTLAB_POS_BUCKETS)
_POSITIONS = frozenset(str(i) for i in range(1, MAX_POSITION + 1))


def strict_json(text: str) -> object:
    """Reject duplicate keys and non-JSON NaN/Infinity instead of silently coercing."""
    def unique(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key in benchmark POS input")
            result[key] = value
        return result

    def invalid_constant(value: str) -> object:
        raise ValueError("nonfinite JSON constant in benchmark POS input")

    return json.loads(text, object_pairs_hook=unique, parse_constant=invalid_constant)


def _object(value: object, name: str, keys: set[str] | frozenset[str]) -> Mapping[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{name} must contain exactly {len(keys)} declared keys")
    return value


def _number(value: object, name: str, *, integer: bool = False, upper: float | None = None) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if integer and not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < 0 or (upper is not None and value > upper):
        raise ValueError(f"{name} is out of range")
    return value


def _ratio(value: object, numerator: int, denominator: int, multiplier: int, name: str) -> None:
    if denominator == 0:
        if value is not None:
            raise ValueError(f"{name} must be null for a zero denominator")
        return
    observed = _number(value, name, upper=100 if multiplier == 100 else None)
    computed = numerator * multiplier / denominator
    if not math.isclose(observed, computed, rel_tol=1e-12, abs_tol=1e-9):
        raise ValueError(f"{name} does not match its declared denominator")


def _count_percent(value: object, *, count_key: str, percent_key: str, denominator: int, name: str,
                   multiplier: int = 100) -> int:
    row = _object(value, name, {count_key, percent_key})
    count = _number(row[count_key], f"{name}.{count_key}", integer=True)
    _ratio(row[percent_key], count, denominator, multiplier, f"{name}.{percent_key}")
    return count


def _matrix(value: object, name: str, keys: frozenset[str]) -> Mapping[str, object]:
    return _object(value, name, keys)


def validate_pos_artifact(pos: object, *, normalized_sha256: str, word_count: int,
                          sentence_count: int) -> dict[str, str]:
    """Validate full canonical POS shape, accounting and exact input/profile join."""
    top = _object(pos, "POS artifact", {
        "schema_version", "metric_contract_id", "profile", "text_profile",
        "normalized_sha256", "mapping_contract", "runtime_profile",
        "runtime_analysis_sha256", "compatibility_status", "input", "metrics",
    })
    constants = {
        "schema_version": POS_SCHEMA_VERSION,
        "metric_contract_id": METRIC_CONTRACT_ID,
        "profile": POS_PROFILE,
        "text_profile": NORMALIZATION_PROFILE,
        "mapping_contract": POS_MAPPING_CONTRACT,
        "compatibility_status": "inferred",
        "normalized_sha256": normalized_sha256,
    }
    for key, expected in constants.items():
        if top[key] != expected:
            raise ValueError(f"POS {key} mismatch")
    if not isinstance(normalized_sha256, str) or len(normalized_sha256) != 64 or set(normalized_sha256) - _HEX:
        raise ValueError("benchmark normalized SHA-256 is malformed")
    runtime_profile = top["runtime_profile"]
    runtime_sha = top["runtime_analysis_sha256"]
    if not isinstance(runtime_profile, str) or not runtime_profile.strip() or len(runtime_profile) > 200:
        raise ValueError("POS runtime profile missing")
    if not isinstance(runtime_sha, str) or len(runtime_sha) != 64 or set(runtime_sha) - _HEX:
        raise ValueError("POS runtime analysis SHA-256 malformed")

    inputs = _object(top["input"], "POS input", {"word_count", "sentence_count"})
    if _number(inputs["word_count"], "POS words", integer=True) != word_count:
        raise ValueError("POS word count differs from text analysis")
    if _number(inputs["sentence_count"], "POS sentences", integer=True) != sentence_count:
        raise ValueError("POS sentence count differs from text analysis")

    metrics = _object(top["metrics"], "POS metrics", {
        "defined", "undefined", "service_words", "buckets", "bigrams", "positions",
    })
    defined = _count_percent(metrics["defined"], count_key="count", percent_key="percent_of_words",
                             denominator=word_count, name="defined")
    undefined = _count_percent(metrics["undefined"], count_key="count", percent_key="percent_of_words",
                               denominator=word_count, name="undefined")
    if defined + undefined != word_count:
        raise ValueError("POS defined and undefined counts must partition input words")
    service = _object(metrics["service_words"], "POS service_words", {
        "count", "percent_of_defined", "status", "reason",
    })
    if (service["count"] is not None or service["percent_of_defined"] is not None
            or service["status"] != "unresolved" or not isinstance(service["reason"], str)
            or not service["reason"].strip()):
        raise ValueError("POS service-word values must remain unresolved")

    buckets = _matrix(metrics["buckets"], "POS buckets", _BUCKETS)
    bucket_counts: dict[str, int] = {}
    for bucket in FANTLAB_POS_BUCKETS:
        bucket_counts[bucket] = _count_percent(
            buckets[bucket], count_key="count", percent_key="percent_of_defined",
            denominator=defined, name=f"bucket.{bucket}",
        )
    if sum(bucket_counts.values()) != defined:
        raise ValueError("POS bucket counts must partition defined words")

    bigrams = _matrix(metrics["bigrams"], "POS bigrams", _BUCKETS)
    outgoing: dict[str, int] = {bucket: 0 for bucket in FANTLAB_POS_BUCKETS}
    incoming: dict[str, int] = {bucket: 0 for bucket in FANTLAB_POS_BUCKETS}
    for left in FANTLAB_POS_BUCKETS:
        row = _matrix(bigrams[left], f"POS bigram row {left}", _BUCKETS)
        for right in FANTLAB_POS_BUCKETS:
            count = _count_percent(row[right], count_key="raw_count", percent_key="per_1000_words",
                                   denominator=word_count, multiplier=1000,
                                   name=f"bigram.{left}.{right}")
            outgoing[left] += count
            incoming[right] += count
    for bucket in FANTLAB_POS_BUCKETS:
        if outgoing[bucket] > bucket_counts[bucket] or incoming[bucket] > bucket_counts[bucket]:
            raise ValueError("POS bigram counts exceed constituent token counts")

    positions = _matrix(metrics["positions"], "POS positions", _POSITIONS)
    per_bucket_positions = {bucket: 0 for bucket in FANTLAB_POS_BUCKETS}
    for i in range(1, MAX_POSITION + 1):
        row = _matrix(positions[str(i)], f"POS position {i}", _BUCKETS)
        position_total = 0
        for bucket in FANTLAB_POS_BUCKETS:
            count = _count_percent(row[bucket], count_key="raw_count", percent_key="percent",
                                   denominator=sentence_count, name=f"position.{i}.{bucket}")
            per_bucket_positions[bucket] += count
            position_total += count
        if position_total > sentence_count:
            raise ValueError("POS position total exceeds sentence count")
    if any(per_bucket_positions[b] > bucket_counts[b] for b in FANTLAB_POS_BUCKETS):
        raise ValueError("POS position counts exceed bucket counts")
    return {"runtime_profile": runtime_profile, "runtime_analysis_sha256": runtime_sha,
            "mapping_contract": POS_MAPPING_CONTRACT}


def _expected(reference: Mapping[str, object], lexical: Mapping[str, object], path: tuple[str, ...],
              label: str, *, integer: bool = False) -> tuple[int | float, str]:
    def visit(doc: Mapping[str, object]) -> object:
        current: object = doc.get("expected")
        for key in path:
            if not isinstance(current, dict) or key not in current:
                raise ValueError(f"FantLab POS reference missing {label}")
            current = current[key]
        return current
    numeric = _number(visit(reference), label, integer=integer,
                      upper=None if integer else 100)
    lexeme = visit(lexical)
    if not isinstance(lexeme, str):
        raise ValueError(f"FantLab POS reference lexical value missing for {label}")
    return numeric, lexeme


def build_pos_comparisons(reference: Mapping[str, object], lexical: Mapping[str, object],
                          pos: Mapping[str, object], *, normalized_sha256: str, word_count: int,
                          sentence_count: int) -> tuple[dict[str, object], dict[str, str]]:
    """Return exactly 40 POS rows; equality is diagnostic even with exact edition."""
    metadata = validate_pos_artifact(pos, normalized_sha256=normalized_sha256,
                                     word_count=word_count, sentence_count=sentence_count)
    from .benchmark import _comparison_row  # Reuse the existing versioned row contract.

    actual = pos["metrics"]
    def emit(metric_id: str, path: tuple[str, ...], actual_value: object, *, integer: bool, label: str,
             service: bool = False) -> None:
        expected, lexeme = _expected(reference, lexical, path, label, integer=integer)
        if service and actual_value is not None:
            raise ValueError("service-word measurement cannot be inferred")
        row = _comparison_row(
            expected=expected, expected_display=lexeme, actual=actual_value,
            definition_evidence="inferred_candidate", source_label=label,
            rule="unresolved_precision" if service or not integer else "exact_integer",
            admission_issues=(POS_BENCHMARK_BOUNDARY,),
        )
        rows[metric_id] = row

    rows: dict[str, object] = {}
    labels = (
        ("undefined", "undefined_pos_words", "undefined_pos_percent_of_words"),
        ("defined", "defined_pos_words", "defined_pos_percent_of_words"),
    )
    ref_words = _expected(reference, lexical, ("words",), "reference words", integer=True)[0]
    ref_defined = _expected(reference, lexical, ("defined_pos_words",), "defined POS words", integer=True)[0]
    ref_undefined = _expected(reference, lexical, ("undefined_pos_words",), "undefined POS words", integer=True)[0]
    if ref_defined + ref_undefined != ref_words:
        raise ValueError("FantLab POS count partition is inconsistent with reference word count")
    for group, count_key, percent_key in labels:
        emit(f"fantlab.pos.{group}.count", (count_key,), actual[group]["count"],
             integer=True, label=count_key)
        emit(f"fantlab.pos.{group}.percent_of_words", (percent_key,),
             actual[group]["percent_of_words"], integer=False, label=percent_key)
    ref_service = _expected(reference, lexical, ("service_words",), "service words", integer=True)[0]
    if ref_service > ref_defined:
        raise ValueError("FantLab service-word count exceeds defined count")
    emit("fantlab.pos.service_words.count", ("service_words",), None, integer=True,
         label="service_words", service=True)
    emit("fantlab.pos.service_words.percent_of_defined", ("service_words_percent_of_defined_pos",),
         None, integer=False, label="service_words_percent_of_defined_pos", service=True)

    ref_buckets = reference.get("expected")
    if not isinstance(ref_buckets, dict):
        raise ValueError("FantLab reference expected section missing")
    ref_pos = _matrix(ref_buckets.get("pos"), "FantLab POS buckets", _BUCKETS)
    for bucket in FANTLAB_POS_BUCKETS:
        _object(ref_pos[bucket], f"FantLab bucket {bucket}", {"count", "percent_of_defined"})
        current = actual["buckets"][bucket]
        for suffix, integer in (("count", True), ("percent_of_defined", False)):
            emit(f"fantlab.pos.buckets.{bucket}.{suffix}", ("pos", bucket, suffix),
                 current[suffix], integer=integer, label=f"{bucket}.{suffix}")
    assert len(rows) == 40
    return rows, metadata
