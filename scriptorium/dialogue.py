"""Deterministic candidate dialogue segmentation for Russian prose.

This module implements ``scriptorium-dialogue-v1``. The rules are explicit
inferred candidates, not a claim that FantLab uses the same segmentation.
"""

from __future__ import annotations

from typing import Final
import re

from .text import TextSpan, normalize_text


DIALOGUE_PROFILE: Final = "scriptorium-dialogue-v1"
DIALOGUE_MARKERS: Final = ("—", "–", "-")

_INTERNAL_SEPARATOR_RE = re.compile(r"\s+[—–-]\s+")


def paragraph_spans(text: str) -> tuple[TextSpan, ...]:
    """Return non-blank LF-delimited paragraph/line spans into normalized text."""

    normalized = normalize_text(text)
    spans: list[TextSpan] = []
    offset = 0

    for line in normalized.splitlines(keepends=True):
        content_end = offset + len(line.rstrip("\n"))
        span = _trimmed_span(normalized, offset, content_end)
        if span is not None:
            spans.append(span)
        offset += len(line)

    return tuple(spans)


def dialogue_spans(text: str) -> tuple[TextSpan, ...]:
    """Return paragraph spans classified as dialogue under the v1 candidate rule.

    A non-blank paragraph is dialogue only when its first content character is
    one of ``—``, ``–`` or ``-`` and that marker is immediately followed by
    whitespace. Quoted speech without a leading paragraph dash is deliberately
    not classified as dialogue by this profile.
    """

    return tuple(span for span in paragraph_spans(text) if _is_dialogue(span))


def narration_spans(text: str) -> tuple[TextSpan, ...]:
    """Return paragraph spans not classified as dialogue by the v1 candidate."""

    return tuple(span for span in paragraph_spans(text) if not _is_dialogue(span))


def author_remark_spans(text: str) -> tuple[TextSpan, ...]:
    """Return candidate author-remarker spans embedded inside dialogue paragraphs.

    After the leading dialogue marker, internal whitespace-dash-whitespace
    separators partition the paragraph into alternating speech and author-text
    segments: speech → author → speech → author... . Only the author segments
    are returned. This deliberately simple rule makes the inference inspectable;
    Russian dialogue punctuation contains cases that FantLab may parse
    differently.
    """

    normalized = normalize_text(text)
    remarks: list[TextSpan] = []

    for paragraph in dialogue_spans(normalized):
        body_start = paragraph.start + 1
        while body_start < paragraph.end and normalized[body_start].isspace():
            body_start += 1

        separators = list(
            _INTERNAL_SEPARATOR_RE.finditer(normalized, body_start, paragraph.end)
        )
        for index, separator in enumerate(separators):
            if index % 2:
                continue
            segment_start = separator.end()
            segment_end = (
                separators[index + 1].start()
                if index + 1 < len(separators)
                else paragraph.end
            )
            span = _trimmed_span(normalized, segment_start, segment_end)
            if span is not None:
                remarks.append(span)

    return tuple(remarks)


def _is_dialogue(span: TextSpan) -> bool:
    return (
        len(span.text) >= 2
        and span.text[0] in DIALOGUE_MARKERS
        and span.text[1].isspace()
    )


def _trimmed_span(text: str, start: int, end: int) -> TextSpan | None:
    segment = text[start:end]
    if not segment.strip():
        return None

    left_trim = len(segment) - len(segment.lstrip())
    right_trimmed_length = len(segment.rstrip())
    trimmed_start = start + left_trim
    trimmed_end = start + right_trimmed_length
    return TextSpan(text[trimmed_start:trimmed_end], trimmed_start, trimmed_end)
