"""Spreadsheet-safe, source-free CSV view of private lexical aggregates.

Only the versioned aggregate and declared replay metadata are serialized.
This does not grant publication rights or embed manuscript tokens.
"""
from __future__ import annotations

import csv
from io import StringIO
from math import isfinite

from .csv_safety import safe_csv_text

_SCHEMA = "scriptorium-private-lexical-contrast-v1"
_METRICS = (
    ("eligible_form_count", "forms"),
    ("excluded_rare_form_count", "forms"),
    ("left_dominant_form_count", "forms"),
    ("right_dominant_form_count", "forms"),
    ("balanced_form_count", "forms"),
    ("left_dominant_token_share_percent", "% of left tokens"),
    ("right_dominant_token_share_percent", "% of right tokens"),
    ("jensen_shannon_divergence_bits", "bits (0-1)"),
)
# An additive extension: pre-overlap v1 artifacts remain readable.
_OVERLAP_METRICS = (
    ("shared_form_count", "forms"),
    ("left_only_form_count", "forms"),
    ("right_only_form_count", "forms"),
    ("type_jaccard_percent", "% of pooled types"),
)
_TYPE_OVERLAP_PROFILE = "scriptorium-lexical-type-overlap-v1"
_WITNESS_FIELDS = (
    ("edition_id", ""),
    ("original_work_id", ""),
    ("translator", ""),
    ("language", ""),
    ("normalization_profile", ""),
    ("vocabulary_profile", ""),
    ("normalized_sha256", ""),
    ("characters_including_spaces", "characters"),
    ("word_tokens", "tokens"),
    ("distinct_forms", "forms"),
    ("meets_300000_character_floor", "boolean"),
    ("source_text_embedded", "boolean"),
    ("metadata_verified", "boolean"),
)


def _cell(value: object) -> str:
    if value is None:
        return "UNKNOWN"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is str:
        return safe_csv_text(value)
    if type(value) in (int, float) and isfinite(value):
        return str(value)
    raise ValueError("invalid lexical CSV value")


def render_lexical_contrast_csv(report: dict[str, object]) -> str:
    """Return a tidy, UTF-8-compatible four-column table with explicit units.

    Aggregate values are numeric only when the comparison is available. A
    genuinely unavailable aggregate is NOT_RUN rather than measured zero.
    """
    if type(report) is not dict or report.get("schema_version") != _SCHEMA:
        raise ValueError("unsupported lexical contrast schema")
    left, right, aggregate = report.get("left"), report.get("right"), report.get("aggregate")
    method = report.get("method")
    if type(left) is not dict or type(right) is not dict or type(method) is not dict:
        raise ValueError("incomplete lexical contrast report")
    with_overlap = "type_overlap_profile" in method
    if ("type_overlap" in method) != with_overlap or (
        with_overlap and (
            method["type_overlap_profile"] != _TYPE_OVERLAP_PROFILE or
            type(method["type_overlap"]) is not str
        )
    ):
        raise ValueError("invalid lexical type-overlap method")
    metrics = _METRICS + (_OVERLAP_METRICS if with_overlap else ())
    if aggregate is not None and (
        type(aggregate) is not dict or set(aggregate) != {key for key, _ in metrics}
    ):
        raise ValueError("invalid lexical aggregate")

    output = StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("section", "field", "value", "unit"))

    def add(section: str, key: str, value: object, unit: str = "") -> None:
        writer.writerow((section, key, _cell(value), unit))

    for key in ("schema_version", "profile", "compatibility_status", "status",
                "corpus_admission", "public_release_ready", "scientific_boundary",
                "length_ratio_max_over_min", "length_imbalance_warning"):
        if key not in report:
            raise ValueError("incomplete lexical contrast metadata")
        add("comparison", key, report[key])

    # Additive v1 metadata: old saved reports remain readable, but a partial
    # pair or contradictory warning cannot masquerade as measured evidence.
    has_ratio = "word_token_ratio_max_over_min" in report
    has_warning = "word_token_imbalance_warning" in report
    if has_ratio != has_warning:
        raise ValueError("incomplete word-token balance metadata")
    if has_ratio:
        ratio = report["word_token_ratio_max_over_min"]
        warning = report["word_token_imbalance_warning"]
        if (ratio is not None and (
            type(ratio) not in (int, float) or not isfinite(ratio) or ratio < 1
        )) or type(warning) is not bool or warning != (ratio is not None and ratio >= 2):
            raise ValueError("invalid word-token balance metadata")
        add("comparison", "word_token_ratio_max_over_min", ratio, "ratio")
        add("comparison", "word_token_imbalance_warning", warning, "boolean")

    for side, witness in (("left", left), ("right", right)):
        for key, unit in _WITNESS_FIELDS:
            if key not in witness:
                raise ValueError("incomplete lexical witness")
            add(side, key, witness[key], unit)

    for key in ("lexical_identity", "denominator", "min_pooled_occurrences",
                "smoothing", "dominance_cutoff", "divergence"):
        if key not in method:
            raise ValueError("incomplete lexical method")
        add("method", key, method[key])
    if with_overlap:
        for key in ("type_overlap_profile", "type_overlap"):
            add("method", key, method[key])

    for key, unit in metrics:
        value = "NOT_RUN" if aggregate is None else aggregate[key]
        if aggregate is not None:
            if (type(value) not in (int, float) or not isfinite(value)
                    or value < 0 or (unit.startswith("%") and value > 100)
                    or (key == "jensen_shannon_divergence_bits" and value > 1)
                    or (unit == "forms" and type(value) is not int)):
                raise ValueError("invalid lexical aggregate measurement")
        add("aggregate", key, value, unit)

    if aggregate is not None and with_overlap:
        shared = aggregate["shared_form_count"]
        left_only = aggregate["left_only_form_count"]
        right_only = aggregate["right_only_form_count"]
        union = shared + left_only + right_only
        if (shared + left_only != left["distinct_forms"] or
                shared + right_only != right["distinct_forms"] or
                union == 0 or
                aggregate["type_jaccard_percent"] != round(100 * shared / union, 6)):
            raise ValueError("inconsistent lexical type-overlap measurements")

    return output.getvalue()
