"""Provider-neutral bridge for the pinned AOT/pylem compatibility candidate.

Native ``pylem==0.0.18`` currently requires a legacy Python 3.9 runtime, while
Scriptorium itself targets the modern Python runtime used by its main verification
lane.  This module therefore defines only the inspectable candidate contract consumed
by ``scriptorium-pos-v1``. Native execution is exercised separately by the pinned
sidecar probe in ``tools/pylem_runtime_probe.py`` until a reviewed transport is wired.
"""
from __future__ import annotations

from typing import Final, Iterable, Protocol

from .morphology import DIRECT_RUNTIME_TO_BUCKET, analyze_pos_metrics
from .text import word_tokens

PYLEM_VERSION: Final = "0.0.18"
PYLEM_RUNTIME_PROFILE: Final = "pylem-0.0.18-python39-sidecar-v1"
_UNRESOLVED_RUNTIME_POS: Final = frozenset(
    {"N", "POSL", "COLLOC", "ADJ_SHORT", "PARTICIPLE_SHORT", "INFINITIVE"}
)
KNOWN_RUNTIME_POS: Final = frozenset(DIRECT_RUNTIME_TO_BUCKET) | _UNRESOLVED_RUNTIME_POS


class _Analysis(Protocol):
    part_of_speech: object


class _Holder(Protocol):
    def lemmatize(self, word: str) -> Iterable[_Analysis]: ...


def runtime_candidates_from_holder(
    text: str,
    holder: _Holder,
) -> tuple[tuple[str, ...], ...]:
    """Return all pylem-style POS strings aligned to Scriptorium word tokens.

    Candidate order and multiplicity are preserved exactly as supplied by the holder.
    Unknown/blank runtime values fail closed so a changed provider vocabulary cannot be
    silently folded into the existing compatibility contract.
    """

    rows: list[tuple[str, ...]] = []
    for token in word_tokens(text):
        runtime_values: list[str] = []
        for analysis in holder.lemmatize(token.text):
            value = getattr(analysis, "part_of_speech", None)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeError("pylem analysis returned a blank/non-string part_of_speech")
            runtime_pos = value.strip()
            if runtime_pos not in KNOWN_RUNTIME_POS:
                raise RuntimeError(f"pylem returned unknown runtime POS value: {runtime_pos!r}")
            runtime_values.append(runtime_pos)
        rows.append(tuple(runtime_values))
    return tuple(rows)


def analyze_pos_with_holder(
    text: str,
    holder: _Holder,
    *,
    runtime_profile: str = PYLEM_RUNTIME_PROFILE,
) -> dict[str, object]:
    """Aggregate POS metrics from an already constructed pylem-compatible holder."""

    return analyze_pos_metrics(
        text,
        runtime_candidates_from_holder(text, holder),
        runtime_profile=runtime_profile,
    )
