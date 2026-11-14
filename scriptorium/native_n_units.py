"""Convert pinned native N-only sensitivity counts to explicitly conditional units.

This is descriptive arithmetic over already verified source-free counts, not a
native morphology run, a token disambiguator or FantLab rounding/parity evidence.
"""
from __future__ import annotations

SCHEMA_VERSION = "scriptorium-native-n-conditional-units-v2"


def _scale(value: object, denominator: object, multiplier: int) -> float:
    if (type(value) is not int or value < 0 or type(denominator) is not int
            or denominator <= 0):
        raise ValueError("invalid conditional N rate count or denominator")
    return value * multiplier / denominator



def _native_control_rate(group: object) -> float | None:
    """N-only share of an annotated native fixture group, not classifier accuracy."""
    if not isinstance(group, dict) or set(group) != {"token_count", "n_only"}:
        raise ValueError("invalid native N control group")
    tested, observed = group["token_count"], group["n_only"]
    if (type(tested) is not int or type(observed) is not int
            or tested < 0 or not 0 <= observed <= tested):
        raise ValueError("invalid native N control counts")
    return _scale(observed, tested, 100) if tested else None


def normalized_n_bounds(witness: dict[str, object]) -> dict[str, object]:
    """Re-express individual-cell bounds; never sum independent maxima."""
    counts = witness["counts"]
    words = counts["word_count"]
    sentences = counts["sentence_count"]
    defined = counts["conditional_defined"]
    buckets = witness["bucket_bounds"]
    pairs = witness["bigram_bounds"]
    positions = witness["sentence_position_bounds"]
    controls = witness["native_controls"]
    if not isinstance(controls, dict) or set(controls) != {
            "noun_examples", "cardinal_examples", "other_pos_controls"}:
        raise ValueError("invalid native N lexical controls")
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
        "native_control_n_only_percent_of_annotated_examples": {
            name: _native_control_rate(group) for name, group in controls.items()
        },
    }
