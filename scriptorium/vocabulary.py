"""Deterministic vocabulary metrics and rolling-window helpers.

``scriptorium-vocabulary-v1`` is an explicit inferred candidate for FantLab's
active-vocabulary family. It deliberately separates lexical normalization from
dictionary membership so a missing or unproven dictionary cannot silently become
compatibility evidence.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from hashlib import sha256
import json
from typing import Final

from .text import normalize_text, word_tokens


VOCABULARY_PROFILE: Final = "scriptorium-vocabulary-v1"
UASZ_WINDOW_SIZES: Final = (3000, 10000, 100000)


def normalize_lexeme(word: str) -> str:
    """Return the v1 lexical identity for one candidate word.

    The candidate uses Unicode ``casefold()`` only. It does not lemmatize, fold
    ``ё`` into ``е``, or otherwise rewrite token text. Exact FantLab lexical
    identity remains a benchmark question.
    """

    if not isinstance(word, str):
        raise TypeError("word must be str")
    return word.casefold()


def vocabulary_lexemes(text: str) -> tuple[str, ...]:
    """Return normalized lexical identities in text order."""

    normalized = normalize_text(text)
    return tuple(normalize_lexeme(token.text) for token in word_tokens(normalized))


def normalize_dictionary_lexemes(words: Iterable[str]) -> frozenset[str]:
    """Normalize an explicit external dictionary lexeme collection."""

    normalized: set[str] = set()
    for word in words:
        if not isinstance(word, str):
            raise TypeError("dictionary words must be str")
        candidate = word.strip()
        if candidate:
            normalized.add(normalize_lexeme(candidate))
    return frozenset(normalized)


def dictionary_lexemes_sha256(dictionary_lexemes: Iterable[str]) -> str:
    """Return a stable digest for a normalized dictionary lexeme set."""

    canonical = json.dumps(
        sorted(set(dictionary_lexemes)),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(canonical).hexdigest()


def rolling_unique_dictionary_counts(
    lexemes: Sequence[str],
    window_size: int,
    dictionary_lexemes: frozenset[str] | set[str],
) -> tuple[int, ...]:
    """Count unique dictionary lexemes in every complete step-1 window.

    The implementation is O(words): a frequency counter is updated as the
    one-token-step window advances. Incomplete windows do not contribute.
    """

    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if len(lexemes) < window_size:
        return ()

    dictionary = dictionary_lexemes
    counts: Counter[str] = Counter()
    unique_dictionary = 0

    for lexeme in lexemes[:window_size]:
        if lexeme not in dictionary:
            continue
        if counts[lexeme] == 0:
            unique_dictionary += 1
        counts[lexeme] += 1

    result = [unique_dictionary]
    for start in range(1, len(lexemes) - window_size + 1):
        outgoing = lexemes[start - 1]
        if outgoing in dictionary:
            counts[outgoing] -= 1
            if counts[outgoing] == 0:
                unique_dictionary -= 1
                del counts[outgoing]

        incoming = lexemes[start + window_size - 1]
        if incoming in dictionary:
            if counts[incoming] == 0:
                unique_dictionary += 1
            counts[incoming] += 1

        result.append(unique_dictionary)

    return tuple(result)


def mean_unique_dictionary_words(
    lexemes: Sequence[str],
    window_size: int,
    dictionary_lexemes: frozenset[str] | set[str],
) -> float | None:
    """Return the arithmetic mean of complete rolling-window counts."""

    counts = rolling_unique_dictionary_counts(lexemes, window_size, dictionary_lexemes)
    if not counts:
        return None
    return sum(counts) / len(counts)


def analyze_vocabulary(
    text: str,
    *,
    dictionary_words: Iterable[str] | None = None,
    dictionary_profile: str | None = None,
) -> dict[str, object]:
    """Return deterministic vocabulary values plus dependency identity.

    ``dictionary_words`` and ``dictionary_profile`` are an all-or-nothing pair.
    Without them, the surface-form unique-word count remains available while
    dictionary-dependent FantLab fields are ``None`` rather than guessed.
    """

    if dictionary_words is None:
        if dictionary_profile is not None:
            raise ValueError("dictionary_profile requires dictionary_words")
        dictionary = None
        dependency = None
    else:
        if dictionary_profile is None or not dictionary_profile.strip():
            raise ValueError("dictionary_words require a non-empty dictionary_profile")
        dictionary = normalize_dictionary_lexemes(dictionary_words)
        dependency = {
            "profile": dictionary_profile.strip(),
            "normalized_lexemes_sha256": dictionary_lexemes_sha256(dictionary),
            "lexeme_count": len(dictionary),
        }

    lexemes = vocabulary_lexemes(text)
    unique = frozenset(lexemes)

    if dictionary is None:
        active_dictionary = None
        active_nondictionary = None
        uasz = {size: None for size in UASZ_WINDOW_SIZES}
    else:
        active_dictionary = len(unique & dictionary)
        active_nondictionary = len(unique - dictionary)
        uasz = {
            size: mean_unique_dictionary_words(lexemes, size, dictionary)
            for size in UASZ_WINDOW_SIZES
        }

    return {
        "profile": VOCABULARY_PROFILE,
        "dictionary_dependency": dependency,
        "unique_words": len(unique),
        "active_dictionary": active_dictionary,
        "active_nondictionary": active_nondictionary,
        "uasz_3000": uasz[3000],
        "uasz_10000": uasz[10000],
        "uasz_100000": uasz[100000],
    }
