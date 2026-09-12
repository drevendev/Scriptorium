"""Deterministic text normalization and structural segmentation.

This module implements Scriptorium's first *inferred* text profile. It is a
versioned candidate, not a claim that FantLab uses the same rules.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata


NORMALIZATION_PROFILE = "scriptorium-text-v1"

_WORD_RE = re.compile(r"[^\W_]+(?:[-'’][^\W_]+)*", re.UNICODE)
_SENTENCE_END_RE = re.compile(r'''[.!?…]+(?:["'»”’)\]]+)?(?=\s|$)''', re.UNICODE)


@dataclass(frozen=True, slots=True)
class TextSpan:
    """A half-open span into normalized text."""

    text: str
    start: int
    end: int


def normalize_text(text: str) -> str:
    """Return text normalized by the ``scriptorium-text-v1`` profile.

    The profile intentionally does only transformations that are explicit and
    easy to reproduce: CRLF/CR line endings become LF and Unicode is composed
    with NFC. Whitespace other than line endings, punctuation, case and quote
    style are preserved.
    """

    if not isinstance(text, str):
        raise TypeError("text must be str")
    canonical_newlines = text.replace("\r\n", "\n").replace("\r", "\n")
    return unicodedata.normalize("NFC", canonical_newlines)


def word_tokens(text: str) -> tuple[TextSpan, ...]:
    """Return candidate word tokens with offsets into normalized text.

    Unicode letters and decimal digits form token bodies. Internal ASCII
    apostrophe, right single quotation mark and hyphen are retained when they
    connect two token bodies. Underscores and surrounding punctuation split
    tokens.
    """

    normalized = normalize_text(text)
    return tuple(
        TextSpan(match.group(0), match.start(), match.end())
        for match in _WORD_RE.finditer(normalized)
    )


def sentence_spans(text: str) -> tuple[TextSpan, ...]:
    """Return deterministic candidate sentence spans.

    A sentence boundary is a run of ``.``, ``!``, ``?`` or ``…`` optionally
    followed by closing quotes/brackets, when the run is followed by whitespace
    or end-of-text. Leading/trailing whitespace is excluded from each span.
    Remaining non-whitespace tail text is returned as a final span.

    This deliberately does not guess abbreviation rules or FantLab's hidden
    sentence-boundary behavior.
    """

    normalized = normalize_text(text)
    spans: list[TextSpan] = []
    cursor = 0

    for match in _SENTENCE_END_RE.finditer(normalized):
        _append_trimmed_span(spans, normalized, cursor, match.end())
        cursor = match.end()

    _append_trimmed_span(spans, normalized, cursor, len(normalized))
    return tuple(spans)


def _append_trimmed_span(
    spans: list[TextSpan],
    text: str,
    start: int,
    end: int,
) -> None:
    segment = text[start:end]
    if not segment.strip():
        return

    left_trim = len(segment) - len(segment.lstrip())
    right_trimmed_length = len(segment.rstrip())
    trimmed_start = start + left_trim
    trimmed_end = start + right_trimmed_length
    spans.append(TextSpan(text[trimmed_start:trimmed_end], trimmed_start, trimmed_end))
