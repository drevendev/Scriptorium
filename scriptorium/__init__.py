"""Scriptorium analysis primitives."""

from .dialogue import (
    DIALOGUE_MARKERS,
    DIALOGUE_PROFILE,
    author_remark_spans,
    dialogue_spans,
    narration_spans,
    paragraph_spans,
)
from .metrics import (
    METRIC_PROFILE,
    PUNCTUATION_PROFILE,
    analyze_deterministic_metrics,
    punctuation_counts,
)
from .text import NORMALIZATION_PROFILE, TextSpan, normalize_text, sentence_spans, word_tokens

__all__ = [
    "DIALOGUE_MARKERS",
    "DIALOGUE_PROFILE",
    "METRIC_PROFILE",
    "NORMALIZATION_PROFILE",
    "PUNCTUATION_PROFILE",
    "TextSpan",
    "analyze_deterministic_metrics",
    "author_remark_spans",
    "dialogue_spans",
    "narration_spans",
    "normalize_text",
    "paragraph_spans",
    "punctuation_counts",
    "sentence_spans",
    "word_tokens",
]
