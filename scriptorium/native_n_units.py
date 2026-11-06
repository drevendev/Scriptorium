"""Convert pinned native N-only sensitivity counts to explicitly conditional units.

This is descriptive arithmetic over already verified source-free counts, not a
native morphology run, a token disambiguator or FantLab rounding/parity evidence.
"""
from __future__ import annotations

SCHEMA_VERSION = "scriptorium-native-n-conditional-units-v1"


def _scale(value: object, denominator: object, multiplier: int) -> float:
    if (type(value) is not int or value < 0 or type(denominator) is not int
            or denominator <= 0):
        raise ValueError("invalid conditional N rate count or denominator")
    return value * multiplier / denominator


def normalized_n_bounds(witness: dict[str, object]) -> dict[str, object]:
    """Re-express individual-cell bounds; never sum independent maxima."""
    counts = witness["counts"]
    words = counts["word_count"]
    sentences = counts["sentence_count"]
    defined = counts["conditional_defined"]
    buckets = witness["bucket_bounds"]
    pairs = witness["bigram_bounds"]
    positions = witness["sentence_position_bounds"]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "conditional_n_only_not_observed_pos_or_fantlab_parity",
        "display_decimal_places": 6,
        "denominators": {
            "word_tokens": words,
            "all_sentences": sentences,
            "conditionally_defined_tokens": defined,
        },
        "bucket_percent_of_conditional_defined": {
            key: [_scale(lo, defined, 100), _scale(hi, defined, 100)]
            for key, (lo, hi) in buckets.items()
        },
        "bigram_per_1000_word_tokens": [
            {
                "first": pair["first"], "second": pair["second"],
                "min": _scale(pair["min"], words, 1000),
                "max": _scale(pair["max"], words, 1000),
                "independent_edge_upper": _scale(pair["independent_edge_upper"], words, 1000),
            }
            for pair in pairs
        ],
        "sentence_position_percent_of_all_sentences": [
            {
                "position": row["position"],
                "min": _scale(row["min"], sentences, 100),
                "max": _scale(row["max"], sentences, 100),
            }
            for row in positions
        ],
    }
