"""Source-free sensitivity diagnostics for dialogue author-remark policies.

This module does not define FantLab-compatible dialogue semantics. It measures
inspectable delimiter and denominator choices while keeping the production
``scriptorium-dialogue-v1`` profile unchanged.
"""

from __future__ import annotations

from collections import Counter
import re
import unicodedata
from typing import Final

from .dialogue import author_remark_spans, dialogue_spans
from .text import TextSpan, normalize_text


DIALOGUE_DIAGNOSTIC_VERSION: Final = "scriptorium-dialogue-policy-diagnostic-v1"

_INTERNAL_SEPARATOR_RE: Final = re.compile(r"\s+[—–-]\s+")
_SPEECH_BOUNDARY_CONTEXTS: Final = frozenset(
    {
        "comma",
        "question",
        "exclamation",
        "unicode_ellipsis",
        "three_dot_ellipsis",
        "question_ellipsis",
        "exclamation_ellipsis",
    }
)


def analyze_dialogue_policy(
    text: str,
    *,
    expected_dialogue_share_percent: float | None = None,
    expected_author_text_inside_dialogue_percent: float | None = None,
) -> dict[str, object]:
    """Return diagnostic-only dialogue segmentation sensitivity evidence.

    ``scriptorium-dialogue-v1`` treats alternating whitespace-dash-whitespace
    separators inside every dash-led dialogue paragraph as speech/author-text
    boundaries. The boundary-filtered probe below is deliberately narrower: an
    author-text opener must follow comma, question, exclamation or ellipsis
    punctuation that is inspectable at the source-text surface. Once accepted,
    the next internal separator closes that candidate author remark.

    This probe is not a claim about FantLab's parser. It exists to distinguish
    ordinary dash use inside speech from punctuation-shaped direct-speech
    boundaries and to expose denominator sensitivity without fitting the
    source-unmatched benchmark target.
    """

    normalized = normalize_text(text)
    dialogues = dialogue_spans(normalized)
    current_remarks = author_remark_spans(normalized)
    boundary_remarks, separator_evidence = _boundary_filtered_author_remarks(normalized)

    total_characters = _non_whitespace_count(normalized)
    dialogue_characters = sum(_non_whitespace_count(span.text) for span in dialogues)
    current_remark_characters = sum(
        _non_whitespace_count(span.text) for span in current_remarks
    )
    boundary_remark_characters = sum(
        _non_whitespace_count(span.text) for span in boundary_remarks
    )

    variants = {
        "current_v1_over_dialogue": _ratio_row(
            current_remark_characters,
            dialogue_characters,
            expected_author_text_inside_dialogue_percent,
        ),
        "speech_boundary_openers_over_dialogue": _ratio_row(
            boundary_remark_characters,
            dialogue_characters,
            expected_author_text_inside_dialogue_percent,
        ),
        "current_v1_over_total_text": _ratio_row(
            current_remark_characters,
            total_characters,
            expected_author_text_inside_dialogue_percent,
        ),
        "speech_boundary_openers_over_total_text": _ratio_row(
            boundary_remark_characters,
            total_characters,
            expected_author_text_inside_dialogue_percent,
        ),
    }

    current_dialogue_share = _percent(dialogue_characters, total_characters)
    dialogue_share_row: dict[str, object] = {
        "value": current_dialogue_share,
        "numerator_non_whitespace_characters": dialogue_characters,
        "denominator_non_whitespace_characters": total_characters,
    }
    if expected_dialogue_share_percent is not None and current_dialogue_share is not None:
        dialogue_share_row["delta_to_reference"] = (
            current_dialogue_share - expected_dialogue_share_percent
        )

    return {
        "schema_version": DIALOGUE_DIAGNOSTIC_VERSION,
        "status": "diagnostic_only",
        "warning": (
            "Delimiter and denominator variants are Scriptorium sensitivity probes, "
            "not recovered FantLab semantics. They cannot promote parity while the "
            "FantLab analyzer-input source identity is unknown."
        ),
        "reference": {
            "expected_dialogue_share_percent": expected_dialogue_share_percent,
            "expected_author_text_inside_dialogue_percent": (
                expected_author_text_inside_dialogue_percent
            ),
        },
        "structure": {
            "dialogue_paragraph_count": len(dialogues),
            "internal_separator_count": separator_evidence["internal_separator_count"],
            "current_v1_author_remark_span_count": len(current_remarks),
            "speech_boundary_author_remark_span_count": len(boundary_remarks),
            "separator_left_context_counts": separator_evidence[
                "separator_left_context_counts"
            ],
            "speech_boundary_contexts": sorted(_SPEECH_BOUNDARY_CONTEXTS),
        },
        "character_counts": {
            "total_non_whitespace": total_characters,
            "dialogue_non_whitespace": dialogue_characters,
            "current_v1_author_remark_non_whitespace": current_remark_characters,
            "speech_boundary_author_remark_non_whitespace": boundary_remark_characters,
        },
        "dialogue_share": dialogue_share_row,
        "author_text_inside_dialogue_variants": variants,
    }


def _boundary_filtered_author_remarks(
    text: str,
) -> tuple[tuple[TextSpan, ...], dict[str, object]]:
    remarks: list[TextSpan] = []
    context_counts: Counter[str] = Counter()
    separator_count = 0

    for paragraph in dialogue_spans(text):
        body_start = paragraph.start + 1
        while body_start < paragraph.end and text[body_start].isspace():
            body_start += 1

        separators = list(
            _INTERNAL_SEPARATOR_RE.finditer(text, body_start, paragraph.end)
        )
        separator_count += len(separators)
        contexts = [
            _separator_left_context(text, paragraph.start, separator.start())
            for separator in separators
        ]
        context_counts.update(contexts)

        index = 0
        while index < len(separators):
            if contexts[index] not in _SPEECH_BOUNDARY_CONTEXTS:
                index += 1
                continue

            separator = separators[index]
            segment_end = (
                separators[index + 1].start()
                if index + 1 < len(separators)
                else paragraph.end
            )
            span = _trimmed_span(text, separator.end(), segment_end)
            if span is not None:
                remarks.append(span)

            # Once a punctuation-shaped opener is accepted, the next separator
            # is treated as its closer for this probe and is not reconsidered as
            # another opener. This avoids double-counting middle author remarks.
            index += 2 if index + 1 < len(separators) else 1

    return (
        tuple(remarks),
        {
            "internal_separator_count": separator_count,
            "separator_left_context_counts": dict(sorted(context_counts.items())),
        },
    )


def _separator_left_context(text: str, paragraph_start: int, separator_start: int) -> str:
    prefix = text[paragraph_start:separator_start].rstrip()
    if not prefix:
        return "other"

    if prefix.endswith("?.."):
        return "question_ellipsis"
    if prefix.endswith("!.."):
        return "exclamation_ellipsis"
    if prefix.endswith("..."):
        return "three_dot_ellipsis"

    character = prefix[-1]
    if character == ",":
        return "comma"
    if character == "?":
        return "question"
    if character == "!":
        return "exclamation"
    if character == "…":
        return "unicode_ellipsis"
    if character == ".":
        return "period"
    if character.isalnum():
        return "alnum"
    if unicodedata.category(character).startswith("P"):
        return "other_punctuation"
    return "other"


def _ratio_row(
    numerator: int,
    denominator: int,
    expected_percent: float | None,
) -> dict[str, object]:
    value = _percent(numerator, denominator)
    row: dict[str, object] = {
        "value": value,
        "numerator_non_whitespace_characters": numerator,
        "denominator_non_whitespace_characters": denominator,
    }
    if expected_percent is not None and value is not None:
        row["delta_to_reference"] = value - expected_percent
    return row


def _percent(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator * 100.0 / denominator


def _non_whitespace_count(text: str) -> int:
    return sum(1 for character in text if not character.isspace())


def _trimmed_span(text: str, start: int, end: int) -> TextSpan | None:
    segment = text[start:end]
    if not segment.strip():
        return None
    left_trim = len(segment) - len(segment.lstrip())
    right_trimmed_length = len(segment.rstrip())
    trimmed_start = start + left_trim
    trimmed_end = start + right_trimmed_length
    return TextSpan(text[trimmed_start:trimmed_end], trimmed_start, trimmed_end)
