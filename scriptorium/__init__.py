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
from .morphology import (
    DIRECT_RUNTIME_TO_BUCKET,
    FANTLAB_POS_BUCKETS,
    MAX_POSITION,
    POS_MAPPING_CONTRACT,
    POS_PROFILE,
    POS_SCHEMA_VERSION,
    analyze_pos_metrics,
    resolve_runtime_pos,
)
from .text import NORMALIZATION_PROFILE, TextSpan, normalize_text, sentence_spans, word_tokens
from .vocabulary import (
    UASZ_WINDOW_SIZES,
    VOCABULARY_PROFILE,
    analyze_vocabulary,
    dictionary_lexemes_sha256,
    mean_unique_dictionary_words,
    normalize_dictionary_lexemes,
    normalize_lexeme,
    rolling_unique_dictionary_counts,
    vocabulary_lexemes,
)

__all__ = [
    "DIALOGUE_MARKERS",
    "DIALOGUE_PROFILE",
    "DIRECT_RUNTIME_TO_BUCKET",
    "FANTLAB_POS_BUCKETS",
    "MAX_POSITION",
    "METRIC_PROFILE",
    "NORMALIZATION_PROFILE",
    "POS_MAPPING_CONTRACT",
    "POS_PROFILE",
    "POS_SCHEMA_VERSION",
    "PUNCTUATION_PROFILE",
    "TextSpan",
    "UASZ_WINDOW_SIZES",
    "VOCABULARY_PROFILE",
    "analyze_deterministic_metrics",
    "analyze_pos_metrics",
    "analyze_vocabulary",
    "author_remark_spans",
    "dialogue_spans",
    "dictionary_lexemes_sha256",
    "mean_unique_dictionary_words",
    "narration_spans",
    "normalize_dictionary_lexemes",
    "normalize_lexeme",
    "normalize_text",
    "paragraph_spans",
    "punctuation_counts",
    "resolve_runtime_pos",
    "rolling_unique_dictionary_counts",
    "sentence_spans",
    "vocabulary_lexemes",
    "word_tokens",
]
