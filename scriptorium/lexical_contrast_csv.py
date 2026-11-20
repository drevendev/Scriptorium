"""Spreadsheet-safe, source-free CSV view of private lexical aggregates.

Only the versioned aggregate and declared replay metadata are serialized.
This does not grant publication rights or embed manuscript tokens.
"""
from __future__ import annotations

import csv
import re
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
# Token-frequency overlap is independent of type Jaccard and uses all types.
_TOKEN_METRICS = (("token_distribution_overlap_percent", "% of token mass"),)
_TOKEN_OVERLAP_PROFILE = "scriptorium-lexical-token-overlap-v1"
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



def _validate_witness(witness: dict[str, object]) -> None:
    """Validate declared replay evidence, not the truth of the source claim."""
    # Reuse the builder's identity rules so re-rendered JSON cannot smuggle
    # arbitrary text into numeric/provenance cells.
    from .lexical_contrast import _id, _LANG, _translator
    from .analyze import REPRESENTATIVE_CHARACTERS
    from .text import NORMALIZATION_PROFILE
    from .vocabulary import VOCABULARY_PROFILE

    _id(witness["edition_id"], "edition")
    _id(witness["original_work_id"], "original work", required=False)
    translator = witness["translator"]
    if _translator(translator) != translator:
        raise ValueError("invalid lexical translator attribution")
    language = witness["language"]
    if type(language) is not str or _LANG.fullmatch(language) is None:
        raise ValueError("invalid lexical language identity")
    if (witness["normalization_profile"] != NORMALIZATION_PROFILE or
            witness["vocabulary_profile"] != VOCABULARY_PROFILE):
        raise ValueError("invalid lexical witness profile")
    digest = witness["normalized_sha256"]
    if type(digest) is not str or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise ValueError("invalid lexical normalized digest")
    counts = ("characters_including_spaces", "word_tokens", "distinct_forms")
    if any(type(witness[key]) is not int or witness[key] < 0 for key in counts):
        raise ValueError("invalid lexical witness counts")
    chars, tokens, forms = (witness[key] for key in counts)
    if forms > tokens or tokens > chars:
        raise ValueError("inconsistent lexical witness counts")
    if (type(witness["meets_300000_character_floor"]) is not bool or
            witness["meets_300000_character_floor"] !=
            (chars >= REPRESENTATIVE_CHARACTERS)):
        raise ValueError("invalid lexical size-floor witness")
    if (witness["source_text_embedded"] is not False or
            witness["metadata_verified"] is not False):
        raise ValueError("invalid lexical source-free witness flags")


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
    # Stored reports may be replayed without source text. Method descriptions
    # are fixed evidence labels, not free-form manuscript or user input.
    from .lexical_contrast import _METHOD
    optional_method_fields = {
        "type_overlap_profile", "type_overlap",
        "token_overlap_profile", "token_overlap",
    }
    if (set(method) - set(_METHOD) or
            any(key not in method or type(method[key]) is not type(value) or
                method[key] != value for key, value in _METHOD.items()
                if key not in optional_method_fields) or
            any(type(method[key]) is not type(_METHOD[key]) or
                method[key] != _METHOD[key] for key in optional_method_fields
                if key in method)):
        raise ValueError("invalid lexical method metadata")
    with_overlap = "type_overlap_profile" in method
    if ("type_overlap" in method) != with_overlap or (
        with_overlap and (
            method["type_overlap_profile"] != _TYPE_OVERLAP_PROFILE or
            type(method["type_overlap"]) is not str
        )
    ):
        raise ValueError("invalid lexical type-overlap method")
    with_token_overlap = "token_overlap_profile" in method
    if ("token_overlap" in method) != with_token_overlap or (
        with_token_overlap and (
            method["token_overlap_profile"] != _TOKEN_OVERLAP_PROFILE or
            type(method["token_overlap"]) is not str
        )
    ):
        raise ValueError("invalid lexical token-overlap method")
    metrics = (_METRICS + (_OVERLAP_METRICS if with_overlap else ()) +
               (_TOKEN_METRICS if with_token_overlap else ()))
    if aggregate is not None and (
        type(aggregate) is not dict or set(aggregate) != {key for key, _ in metrics}
    ):
        raise ValueError("invalid lexical aggregate")


    for witness in (left, right):
        if any(key not in witness for key, _ in _WITNESS_FIELDS):
            raise ValueError("incomplete lexical witness")
        _validate_witness(witness)

    lengths = (left["characters_including_spaces"], right["characters_including_spaces"])
    expected_length_ratio = (round(max(lengths) / min(lengths), 6)
                             if min(lengths) else None)
    if (type(report.get("length_imbalance_warning")) is not bool or
            report.get("length_ratio_max_over_min") != expected_length_ratio or
            report["length_imbalance_warning"] !=
            (expected_length_ratio is not None and expected_length_ratio >= 2)):
        raise ValueError("invalid lexical length-balance evidence")

    if (report.get("profile") != "scriptorium-lexical-aggregate-contrast-v1" or
            report.get("compatibility_status") != "extension" or
            report.get("corpus_admission") != "NOT_VERIFIED" or
            report.get("public_release_ready") is not False):
        raise ValueError("invalid lexical source-free comparison boundary")

    # Stored source-free reports are untrusted input: human-readable outputs
    # must not repeat arbitrary prose in the status or scientific disclaimer.
    from .lexical_contrast import SCIENTIFIC_BOUNDARY
    if report.get("scientific_boundary") != SCIENTIFIC_BOUNDARY:
        raise ValueError("invalid lexical scientific boundary")

    if left["edition_id"] == right["edition_id"] and any(
        left[key] != right[key] for key in (
            "normalized_sha256", "original_work_id", "language", "translator"
        )
    ):
        raise ValueError("conflicting identity for one lexical edition")

    # Translation-pair intent was not serialized in historical v1 reports.
    # With missing/different original-work IDs, either an ordinary comparison
    # or explicit translation-lineage incomparability can be genuine.
    if not left["word_tokens"] or not right["word_tokens"]:
        admissible = {"NOT_RUN_EMPTY"}
    elif left["language"] != right["language"]:
        admissible = {"INCOMPARABLE_LANGUAGE"}
    else:
        same_text = left["normalized_sha256"] == right["normalized_sha256"]
        admissible = {"IDENTICAL_NORMALIZED_TEXT" if same_text else "COMPARABLE"}
        if (left["original_work_id"] is None or
                left["original_work_id"] != right["original_work_id"]):
            admissible.add("INCOMPARABLE_TRANSLATION_LINEAGE")
    status = report.get("status")
    measured = status in ("COMPARABLE", "IDENTICAL_NORMALIZED_TEXT")
    if (type(status) is not str or status not in admissible or
            measured != (aggregate is not None)):
        raise ValueError("inconsistent lexical comparison status")

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
        tokens = (left["word_tokens"], right["word_tokens"])
        expected_token_ratio = (round(max(tokens) / min(tokens), 6)
                                if min(tokens) else None)
        if ratio != expected_token_ratio:
            raise ValueError("inconsistent lexical word-token ratio")
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
    if with_token_overlap:
        for key in ("token_overlap_profile", "token_overlap"):
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
