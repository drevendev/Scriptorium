"""Deterministic first-wave metric extraction.

The profiles in this module are explicit *inferred* candidates for FantLab-visible
general, dialogue and punctuation metrics. Public metric names do not imply reproduced
parity.
"""

from __future__ import annotations

from hashlib import sha256
from typing import Final

from .dialogue import (
    DIALOGUE_PROFILE,
    author_remark_spans,
    dialogue_spans,
    narration_spans,
)
from .text import NORMALIZATION_PROFILE, TextSpan, normalize_text, sentence_spans, word_tokens


METRIC_PROFILE: Final = "scriptorium-metrics-v2"
PUNCTUATION_PROFILE: Final = "scriptorium-punctuation-v1"
SCHEMA_VERSION: Final = "scriptorium-deterministic-metrics-v2"
METRIC_CONTRACT_ID: Final = "fantlab-2022-v1"

PUNCTUATION_KEYS: Final = (
    "comma",
    "period",
    "dash",
    "exclamation",
    "question",
    "ellipsis",
    "exclamation_ellipsis",
    "question_ellipsis",
    "triple_exclamation",
    "question_exclamation",
    "quote",
    "parentheses",
    "colon",
    "semicolon",
)

_METRIC_DEFINITIONS: Final = {
    "fantlab.general.characters": ("characters", "public_surface", "inferred"),
    "fantlab.general.words": ("words", "public_surface", "inferred"),
    "scriptorium.general.sentences": ("sentences", "scriptorium_extension", "extension"),
    "fantlab.general.mean_word_length_chars": (
        "characters/word",
        "public_surface",
        "inferred",
    ),
    "fantlab.general.mean_sentence_length_chars": (
        "characters/sentence",
        "public_surface",
        "inferred",
    ),
    "fantlab.dialogue.mean_narration_sentence_length_chars": (
        "characters/sentence",
        "public_surface",
        "inferred",
    ),
    "fantlab.dialogue.mean_dialogue_sentence_length_chars": (
        "characters/sentence",
        "public_surface",
        "inferred",
    ),
    "fantlab.dialogue.share_percent": ("percent", "public_surface", "inferred"),
    "fantlab.dialogue.author_text_inside_dialogue_percent": (
        "percent",
        "public_surface",
        "inferred",
    ),
}

_MULTI_PUNCTUATION: Final = (
    ("question_ellipsis", "?.."),
    ("question_ellipsis", "?…"),
    ("exclamation_ellipsis", "!.."),
    ("exclamation_ellipsis", "!…"),
    ("triple_exclamation", "!!!"),
    ("question_exclamation", "?!"),
    ("ellipsis", "..."),
    ("ellipsis", "…"),
)
_SINGLE_PUNCTUATION: Final = {
    ",": "comma",
    ".": "period",
    "-": "dash",
    "‐": "dash",
    "‑": "dash",
    "‒": "dash",
    "–": "dash",
    "—": "dash",
    "!": "exclamation",
    "?": "question",
    "\"": "quote",
    "«": "quote",
    "»": "quote",
    "“": "quote",
    "”": "quote",
    "„": "quote",
    "(": "parentheses",
    ":": "colon",
    ";": "semicolon",
}


def analyze_deterministic_metrics(text: str) -> dict[str, object]:
    """Return the versioned deterministic metric artifact for ``text``.

    All FantLab-namespaced values are compatibility candidates. They remain
    ``inferred`` until source-matched benchmarks satisfy the project gate.
    """

    normalized = normalize_text(text)
    words = word_tokens(normalized)
    sentences = sentence_spans(normalized)
    word_count = len(words)
    sentence_count = len(sentences)

    narration = narration_spans(normalized)
    dialogue = dialogue_spans(normalized)
    author_remarks = author_remark_spans(normalized)

    narration_sentence_lengths = _sentence_lengths(narration)
    dialogue_sentence_lengths = _sentence_lengths(dialogue)

    non_whitespace_characters = _non_whitespace_count(normalized)
    dialogue_characters = sum(_non_whitespace_count(span.text) for span in dialogue)
    author_remark_characters = sum(
        _non_whitespace_count(span.text) for span in author_remarks
    )

    metrics: dict[str, dict[str, object]] = {
        "fantlab.general.characters": _metric(len(normalized), "fantlab.general.characters"),
        "fantlab.general.words": _metric(word_count, "fantlab.general.words"),
        "scriptorium.general.sentences": _metric(
            sentence_count, "scriptorium.general.sentences"
        ),
        "fantlab.general.mean_word_length_chars": _metric(
            _safe_mean(sum(len(token.text) for token in words), word_count),
            "fantlab.general.mean_word_length_chars",
        ),
        "fantlab.general.mean_sentence_length_chars": _metric(
            _safe_mean(sum(len(sentence.text) for sentence in sentences), sentence_count),
            "fantlab.general.mean_sentence_length_chars",
        ),
        "fantlab.dialogue.mean_narration_sentence_length_chars": _metric(
            _safe_mean(sum(narration_sentence_lengths), len(narration_sentence_lengths)),
            "fantlab.dialogue.mean_narration_sentence_length_chars",
        ),
        "fantlab.dialogue.mean_dialogue_sentence_length_chars": _metric(
            _safe_mean(sum(dialogue_sentence_lengths), len(dialogue_sentence_lengths)),
            "fantlab.dialogue.mean_dialogue_sentence_length_chars",
        ),
        "fantlab.dialogue.share_percent": _metric(
            _percent(dialogue_characters, non_whitespace_characters),
            "fantlab.dialogue.share_percent",
        ),
        "fantlab.dialogue.author_text_inside_dialogue_percent": _metric(
            _percent(author_remark_characters, dialogue_characters),
            "fantlab.dialogue.author_text_inside_dialogue_percent",
        ),
    }

    counts = punctuation_counts(normalized)
    for key in PUNCTUATION_KEYS:
        metrics[f"fantlab.punctuation.{key}.per_1000_words"] = {
            "value": _per_1000(counts[key], word_count),
            "unit": "occurrences/1000_words",
            "definition_evidence": "public_surface",
            "compatibility_status": "inferred",
            "raw_count": counts[key],
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "metric_contract_id": METRIC_CONTRACT_ID,
        "profiles": {
            "normalization": NORMALIZATION_PROFILE,
            "metrics": METRIC_PROFILE,
            "dialogue": DIALOGUE_PROFILE,
            "punctuation": PUNCTUATION_PROFILE,
        },
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
        "metrics": metrics,
    }


def punctuation_counts(text: str) -> dict[str, int]:
    """Count punctuation events under ``scriptorium-punctuation-v1``.

    Multi-character surface patterns are greedily consumed before single-character
    events, so one glyph run cannot inflate both a compound and its component
    metrics. Ellipsis accepts either ``...`` or U+2026. Dash variants U+2010 through
    U+2014 plus ASCII hyphen count as ``dash``. Quote glyphs are counted
    individually. ``parentheses`` counts opening ``(`` glyphs as candidate pair
    events; unmatched closing glyphs do not increment it.

    These are inferred compatibility choices, not recovered FantLab rules.
    """

    normalized = normalize_text(text)
    counts = {key: 0 for key in PUNCTUATION_KEYS}
    index = 0

    while index < len(normalized):
        for key, token in _MULTI_PUNCTUATION:
            if normalized.startswith(token, index):
                counts[key] += 1
                index += len(token)
                break
        else:
            key = _SINGLE_PUNCTUATION.get(normalized[index])
            if key is not None:
                counts[key] += 1
            index += 1

    return counts


def _sentence_lengths(paragraphs: tuple[TextSpan, ...]) -> list[int]:
    lengths: list[int] = []
    for paragraph in paragraphs:
        lengths.extend(len(sentence.text) for sentence in sentence_spans(paragraph.text))
    return lengths


def _non_whitespace_count(text: str) -> int:
    return sum(1 for character in text if not character.isspace())


def _metric(value: int | float | None, metric_id: str) -> dict[str, object]:
    unit, definition_evidence, compatibility_status = _METRIC_DEFINITIONS[metric_id]
    return {
        "value": value,
        "unit": unit,
        "definition_evidence": definition_evidence,
        "compatibility_status": compatibility_status,
    }


def _safe_mean(total: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return total / denominator


def _percent(part: int, whole: int) -> float | None:
    if whole == 0:
        return None
    return part * 100.0 / whole


def _per_1000(count: int, word_count: int) -> float | None:
    if word_count == 0:
        return None
    return count * 1000.0 / word_count
