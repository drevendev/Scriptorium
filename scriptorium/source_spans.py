"""Opt-in, conservative Unicode code-point provenance for normalized spans.

No changes to scriptorium-text-v1 or the normalized token/sentence offsets.
The original manuscript is retained only in this explicitly requested local
object; do not serialize it to analysis reports or Pages.
"""
from __future__ import annotations

from dataclasses import dataclass
import unicodedata

from .text import NORMALIZATION_PROFILE, normalize_text

PROVENANCE_PROFILE = "scriptorium-source-spans-v1"


@dataclass(frozen=True, slots=True)
class OriginalSpan:
    """Conservative half-open Python code-point range in original input.

    exact is false when reordering/composition crosses an output boundary
    or the original slice alone cannot normalize to the requested span.
    start and end still bound all contributing original code points.
    """
    start: int
    end: int
    exact: bool


@dataclass(frozen=True, slots=True)
class NormalizationProvenance:
    """Local-only, opt-in normalized text and per-scalar origin bounds.

    Memory is O(input+output code points), plus temporary NFD units. No public
    report or default analyzer/segmentation path constructs this object.
    """
    original: str
    normalized: str
    source_ranges: tuple[tuple[int, int], ...]
    safe_boundaries: tuple[bool, ...]
    profile: str = PROVENANCE_PROFILE
    normalization_profile: str = NORMALIZATION_PROFILE

    def original_span(self, start: int, end: int) -> OriginalSpan:
        """Map a nonempty normalized half-open span conservatively to source.

        Indices are Python Unicode code points, NOT byte/UTF-16 offsets. An
        ambiguous result must not be used as an exact source substring match.
        """
        if (type(start) is not int or type(end) is not int or not
                (0 <= start < end <= len(self.normalized))):
            raise ValueError("expected nonempty normalized code-point span")
        relevant = self.source_ranges[start:end]
        left = min(bounds[0] for bounds in relevant)
        right = max(bounds[1] for bounds in relevant)
        exact = (self.safe_boundaries[start] and self.safe_boundaries[end]
                 and normalize_text(self.original[left:right]) == self.normalized[start:end])
        return OriginalSpan(left, right, exact)


def normalize_with_provenance(original: str) -> NormalizationProvenance:
    """Normalize with optional conservative original-coordinate provenance.

    Uses canonical NFD ordering to associate decomposed units with original
    Unicode code points, then composes those units while tracking origins.
    CRLF is one LF with a two-code-point source range. No guessed one-to-one
    offset mapping is supplied across reordered combining sequences.
    """
    normalized = normalize_text(original)  # preserves the existing TypeError

    # Source-unit records are (scalar, start, end); canonical newline
    # conversion happens before Unicode normalization, just as in text.py.
    canonical: list[tuple[str, int, int]] = []
    cursor = 0
    while cursor < len(original):
        char = original[cursor]
        width = 2 if char == "\r" and original[cursor:cursor + 2] == "\r\n" else 1
        canonical.append(("\n" if char == "\r" else char, cursor, cursor + width))
        cursor += width

    # NFD canonical ordering is stable within each run of nonstarter marks.
    # Sorting the runs (rather than comparing every prefix of a manuscript)
    # keeps normal work linear and long combining sequences O(k log k).
    decomposed: list[tuple[str, int, int]] = []
    pending: list[tuple[str, int, int]] = []

    def flush() -> None:
        if not pending:
            return
        if unicodedata.combining(pending[0][0]) == 0:
            decomposed.append(pending[0])
            decomposed.extend(sorted(pending[1:], key=lambda unit: unicodedata.combining(unit[0])))
        else:
            decomposed.extend(sorted(pending, key=lambda unit: unicodedata.combining(unit[0])))
        pending.clear()

    for char, start, end in canonical:
        for scalar in unicodedata.normalize("NFD", char):
            if unicodedata.combining(scalar) == 0:
                flush()
            pending.append((scalar, start, end))
    flush()

    if "".join(unit[0] for unit in decomposed) != unicodedata.normalize("NFD", normalized):
        raise ValueError("unable to establish canonical source alignment")

    # Canonical composition must be tracked with origins: decomposing each
    # final NFC scalar separately and consuming consecutive NFD units is NOT
    # generally valid (an accent on a composed starter may reorder past a
    # previously output combining mark). Apply Unicode blocked composition.
    composed: list[list[object]] = []  # [scalar, earliest_source, latest_source]
    starter_index: int | None = None
    last_class = 0
    for scalar, start, end in decomposed:
        category = unicodedata.combining(scalar)
        if starter_index is not None and (last_class < category or last_class == 0):
            starter = composed[starter_index]
            candidate = unicodedata.normalize("NFC", str(starter[0]) + scalar)
            if len(candidate) == 1:
                starter[0] = candidate
                starter[1] = min(int(starter[1]), start)
                starter[2] = max(int(starter[2]), end)
                continue
        if category == 0:
            starter_index = len(composed)
        composed.append([scalar, start, end])
        last_class = category
    if "".join(str(entry[0]) for entry in composed) != normalized:
        raise ValueError("unable to compose canonical source alignment")
    ranges = [(int(entry[1]), int(entry[2])) for entry in composed]

    # Only report an exact range when both boundaries split the source into
    # noninterleaved regions. This refuses a seemingly exact interior span
    # when canonical combining-class reordering crosses either boundary.
    max_before = [0]
    for _, end in ranges:
        max_before.append(max(max_before[-1], end))
    min_after = [len(original)] * (len(ranges) + 1)
    for i in range(len(ranges) - 1, -1, -1):
        min_after[i] = min(min_after[i + 1], ranges[i][0])
    safe = tuple(a <= b for a, b in zip(max_before, min_after))

    return NormalizationProvenance(original, normalized, tuple(ranges), safe)
