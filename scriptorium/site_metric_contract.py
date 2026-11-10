"""Fail-closed publication contract for deterministic metrics v3/v4.

Keep historical version identities pinned here.  This deliberately does not import
the latest engine's mutable metric definitions or upgrade FantLab evidence.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping
from typing import Any

_SUPPORTED_PROFILES = {
    "scriptorium-deterministic-metrics-v3": {
        "normalization": "scriptorium-text-v1",
        "metrics": "scriptorium-metrics-v3",
        "dialogue": "scriptorium-dialogue-v1",
        "vocabulary": "scriptorium-vocabulary-v1",
        "punctuation": "scriptorium-punctuation-v1",
    },
    "scriptorium-deterministic-metrics-v4": {
        "normalization": "scriptorium-text-v1",
        "metrics": "scriptorium-metrics-v4",
        "dialogue": "scriptorium-dialogue-v1",
        "vocabulary": "scriptorium-vocabulary-v1",
        "punctuation": "scriptorium-punctuation-v2",
    },
}
_HEX64 = re.compile(r"[0-9a-f]{64}\Z")
_ANALYSIS_KEYS = frozenset({
    "schema_version", "metric_contract_id", "profiles",
    "dependencies", "normalized_sha256", "metrics",
})
_DICTIONARY_KEYS = frozenset({
    "profile", "normalized_lexemes_sha256", "lexeme_count",
})
_PUBLIC_ROWS = {
    "fantlab.general.characters": ("characters", "public_surface", "inferred"),
    "fantlab.general.words": ("words", "public_surface", "inferred"),
    "scriptorium.general.sentences": ("sentences", "scriptorium_extension", "extension"),
    "fantlab.general.mean_word_length_chars": ("characters/word", "public_surface", "inferred"),
    "fantlab.general.mean_sentence_length_chars": ("characters/sentence", "public_surface", "inferred"),
    "fantlab.dialogue.mean_narration_sentence_length_chars": ("characters/sentence", "public_surface", "inferred"),
    "fantlab.dialogue.mean_dialogue_sentence_length_chars": ("characters/sentence", "public_surface", "inferred"),
    "fantlab.dialogue.share_percent": ("percent", "public_surface", "inferred"),
    "fantlab.dialogue.author_text_inside_dialogue_percent": ("percent", "public_surface", "inferred"),
    "fantlab.vocabulary.unique_words": ("words", "public_definition", "inferred"),
    "fantlab.vocabulary.active_dictionary": ("words", "public_definition", "inferred"),
    "fantlab.vocabulary.active_nondictionary": ("words", "public_definition", "inferred"),
    "fantlab.vocabulary.uasz_3000": ("unique_dictionary_words/window", "public_definition", "inferred"),
    "fantlab.vocabulary.uasz_10000": ("unique_dictionary_words/window", "public_definition", "inferred"),
    "fantlab.vocabulary.uasz_100000": ("unique_dictionary_words/window", "public_definition", "inferred"),
}
_PUNCTUATION_NAMES = (
    "comma", "period", "dash", "exclamation", "question", "ellipsis",
    "exclamation_ellipsis", "question_ellipsis", "triple_exclamation",
    "question_exclamation", "quote", "parentheses", "colon", "semicolon",
)
_ROWS = {
    **_PUBLIC_ROWS,
    **{
        f"fantlab.punctuation.{name}.per_1000_words": (
            "occurrences/1000_words", "public_surface", "inferred"
        )
        for name in _PUNCTUATION_NAMES
    },
}
_DEPENDENT_VOCABULARY = (
    "fantlab.vocabulary.active_dictionary",
    "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000",
    "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
)


def _exact_fields(value: Any, keys: frozenset[str], context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != keys:
        raise ValueError(f"{context} has invalid fields")
    return value


def _sha(value: Any, context: str) -> None:
    if not isinstance(value, str) or not _HEX64.fullmatch(value):
        raise ValueError(f"{context} requires a lowercase SHA-256")


def _number(value: Any, context: str) -> None:
    if value is None:
        return
    if type(value) not in (int, float):
        raise ValueError(f"{context} must be numeric or null")
    try:
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{context} must be finite and nonnegative")
    except OverflowError as exc:
        raise ValueError(f"{context} must be finite") from exc


def validate_current_analysis(analysis: Any) -> None:
    """Validate a complete current-schema engine artifact before public rendering.

    This binds every v3/v4 row to its frozen identity, unit, evidence and
    status; accepting a version label alone is not sufficient.
    """

    analysis = _exact_fields(analysis, _ANALYSIS_KEYS, "analysis")
    version = analysis["schema_version"]
    if version not in _SUPPORTED_PROFILES:
        raise ValueError("unsupported current metric schema")
    if analysis["metric_contract_id"] != "fantlab-2022-v1":
        raise ValueError("metric contract identity mismatch")
    if analysis["profiles"] != _SUPPORTED_PROFILES[version]:
        raise ValueError("metric profile identity mismatch")
    _sha(analysis["normalized_sha256"], "analysis.normalized_sha256")

    dependencies = _exact_fields(
        analysis["dependencies"], frozenset({"vocabulary_dictionary"}), "dependencies"
    )
    dictionary = dependencies["vocabulary_dictionary"]
    if dictionary is not None:
        dictionary = _exact_fields(dictionary, _DICTIONARY_KEYS, "dictionary dependency")
        if not isinstance(dictionary["profile"], str) or not dictionary["profile"].strip():
            raise ValueError("dictionary profile must be nonempty")
        _sha(dictionary["normalized_lexemes_sha256"], "dictionary hash")
        if type(dictionary["lexeme_count"]) is not int or dictionary["lexeme_count"] < 0:
            raise ValueError("dictionary lexeme count must be nonnegative integer")

    metrics = analysis["metrics"]
    if not isinstance(metrics, Mapping) or set(metrics) != set(_ROWS):
        raise ValueError("current metrics must have exactly 29 canonical rows")
    for metric_id, expected in _ROWS.items():
        is_punctuation = metric_id.startswith("fantlab.punctuation.")
        keys = frozenset({
            "value", "unit", "definition_evidence", "compatibility_status",
            *("raw_count",) if is_punctuation else (),
        })
        row = _exact_fields(metrics[metric_id], keys, f"metric {metric_id}")
        actual = (row["unit"], row["definition_evidence"], row["compatibility_status"])
        if actual != expected:
            raise ValueError(f"metric {metric_id} contract mismatch")
        _number(row["value"], f"metric {metric_id}.value")
        if is_punctuation and (
            type(row["raw_count"]) is not int or row["raw_count"] < 0
        ):
            raise ValueError(f"metric {metric_id}.raw_count must be nonnegative integer")

    if dictionary is None and any(metrics[key]["value"] is not None for key in _DEPENDENT_VOCABULARY):
        raise ValueError("dictionary-dependent values require a bound dictionary")
