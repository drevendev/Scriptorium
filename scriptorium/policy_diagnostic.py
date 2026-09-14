"""Source-free sensitivity diagnostics for word and dash policies.

This module does not define FantLab-compatible semantics. It measures how a few
inspectable policy choices affect counts on a replayed text so an unmatched-source
benchmark cannot tempt the implementation into numerical fitting.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Final

from .metrics import punctuation_counts
from .text import normalize_text, word_tokens


POLICY_DIAGNOSTIC_VERSION: Final = "scriptorium-text-policy-diagnostic-v2"

# U+002D HYPHEN-MINUS is retained for continuity with scriptorium-text-v1.
# U+2010 HYPHEN and U+2011 NON-BREAKING HYPHEN are included only in this
# sensitivity candidate because their Unicode semantics make them plausible
# lexical connectors. U+2012..U+2014 remain punctuation separators here.
_LEXICAL_HYPHEN_CONNECTORS: Final = "-‐‑"
_WORD_WITH_UNICODE_HYPHEN_RE: Final = re.compile(
    rf"[^\W_]+(?:[{_LEXICAL_HYPHEN_CONNECTORS}'’][^\W_]+)*",
    re.UNICODE,
)
_DASH_GLYPHS: Final = ("-", "‐", "‑", "‒", "–", "—")


def analyze_word_dash_policy(
    text: str,
    *,
    expected_word_count: int | None = None,
    expected_dash_per_1000_words: float | None = None,
) -> dict[str, object]:
    """Return source-free diagnostics for inspectable token/dash policy choices.

    The returned variants are sensitivity probes, not compatibility candidates.
    In particular, a variant getting numerically closer to FantLab is never evidence
    that FantLab uses that policy while the analyzer-input edition is unknown.
    """

    normalized = normalize_text(text)
    current_tokens = word_tokens(normalized)
    unicode_hyphen_tokens = tuple(
        match.group(0) for match in _WORD_WITH_UNICODE_HYPHEN_RE.finditer(normalized)
    )

    current_word_count = len(current_tokens)
    current_numeric_only = sum(token.text.isdecimal() for token in current_tokens)
    unicode_hyphen_numeric_only = sum(token.isdecimal() for token in unicode_hyphen_tokens)

    word_variants = {
        "current_scriptorium_text_v1": current_word_count,
        "exclude_numeric_only_tokens": current_word_count - current_numeric_only,
        "join_unicode_hyphen_connectors": len(unicode_hyphen_tokens),
        "join_unicode_hyphens_and_exclude_numeric_only": (
            len(unicode_hyphen_tokens) - unicode_hyphen_numeric_only
        ),
    }

    glyph_counts = {glyph: normalized.count(glyph) for glyph in _DASH_GLYPHS}
    all_supported_dash_glyphs = sum(glyph_counts.values())
    ascii_contexts = _ascii_hyphen_contexts(normalized)
    lexical_hyphen_like_between_letters = _lexical_hyphen_like_between_letters(normalized)
    token_internal_ascii_hyphens = sum(token.text.count("-") for token in current_tokens)
    current_dash_count = punctuation_counts(normalized)["dash"]
    if current_dash_count != all_supported_dash_glyphs - token_internal_ascii_hyphens:
        raise AssertionError(
            "scriptorium-punctuation-v2 dash count diverged from its token-internal "
            "ASCII-hyphen exclusion"
        )

    dash_variants = {
        "legacy_punctuation_v1_all_supported_dash_glyphs": all_supported_dash_glyphs,
        "current_scriptorium_punctuation_v2": current_dash_count,
        "exclude_ascii_hyphen_between_letters": (
            all_supported_dash_glyphs - ascii_contexts["between_letters"]
        ),
        "exclude_lexical_hyphen_like_between_letters": (
            all_supported_dash_glyphs - lexical_hyphen_like_between_letters
        ),
        "exclude_all_current_token_internal_ascii_hyphens": current_dash_count,
    }

    word_rows: dict[str, dict[str, object]] = {}
    for name, count in word_variants.items():
        row: dict[str, object] = {"count": count, "delta_from_current": count - current_word_count}
        if expected_word_count is not None:
            row["delta_to_reference"] = count - expected_word_count
        word_rows[name] = row

    dash_rows: dict[str, dict[str, object]] = {}
    for name, count in dash_variants.items():
        rate = _per_1000(count, current_word_count)
        row = {
            "count": count,
            "delta_from_current_count": count - current_dash_count,
            "per_1000_current_words": rate,
        }
        if expected_dash_per_1000_words is not None and rate is not None:
            row["rate_delta_to_reference"] = rate - expected_dash_per_1000_words
        dash_rows[name] = row

    return {
        "schema_version": POLICY_DIAGNOSTIC_VERSION,
        "status": "diagnostic_only",
        "warning": (
            "Sensitivity variants are not FantLab semantics and cannot promote parity "
            "while analyzer-input source identity is unknown."
        ),
        "reference": {
            "expected_word_count": expected_word_count,
            "expected_dash_per_1000_words": expected_dash_per_1000_words,
        },
        "word_policy": {
            "variants": word_rows,
            "current_numeric_only_tokens": current_numeric_only,
            "unicode_hyphen_candidate_numeric_only_tokens": unicode_hyphen_numeric_only,
        },
        "dash_policy": {
            "glyph_counts": {
                f"U+{ord(glyph):04X} {unicodedata.name(glyph, 'UNKNOWN')}": count
                for glyph, count in glyph_counts.items()
            },
            "ascii_hyphen_contexts": ascii_contexts,
            "lexical_hyphen_like_between_letters": lexical_hyphen_like_between_letters,
            "current_token_internal_ascii_hyphens": token_internal_ascii_hyphens,
            "variants": dash_rows,
        },
    }


def _ascii_hyphen_contexts(text: str) -> dict[str, int]:
    counts = {
        "between_letters": 0,
        "between_digits": 0,
        "between_other_alnum": 0,
        "other": 0,
    }
    for index, character in enumerate(text):
        if character != "-":
            continue
        left = text[index - 1] if index else ""
        right = text[index + 1] if index + 1 < len(text) else ""
        if left.isalpha() and right.isalpha():
            counts["between_letters"] += 1
        elif left.isdecimal() and right.isdecimal():
            counts["between_digits"] += 1
        elif left.isalnum() and right.isalnum():
            counts["between_other_alnum"] += 1
        else:
            counts["other"] += 1
    return counts


def _lexical_hyphen_like_between_letters(text: str) -> int:
    count = 0
    for index, character in enumerate(text):
        if character not in _LEXICAL_HYPHEN_CONNECTORS:
            continue
        left = text[index - 1] if index else ""
        right = text[index + 1] if index + 1 < len(text) else ""
        if left.isalpha() and right.isalpha():
            count += 1
    return count


def _per_1000(count: int, word_count: int) -> float | None:
    if word_count == 0:
        return None
    return count * 1000.0 / word_count
