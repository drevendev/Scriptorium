"""Native provider bridge for the pinned AOT/pylem compatibility candidate.

This module deliberately keeps native pylem import lazy. The deterministic POS
aggregation layer remains usable without the optional C++ provider, while the hosted
provider lane can prove the exact distribution version and feed every returned runtime
POS candidate into ``scriptorium-pos-v1`` without selecting homonyms or inventing a
noun/cardinal discriminator.
"""
from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform
from typing import Final, Iterable, Protocol

from .morphology import (
    DIRECT_RUNTIME_TO_BUCKET,
    POS_MAPPING_CONTRACT,
    analyze_pos_metrics,
)
from .text import word_tokens

PYLEM_DISTRIBUTION: Final = "pylem"
PYLEM_VERSION: Final = "0.0.18"
PYLEM_RUNTIME_PROFILE: Final = "pylem-0.0.18-python-api-v1"
PYLEM_RUNTIME_RECEIPT_SCHEMA: Final = "scriptorium-pylem-runtime-receipt-v1"
_UNRESOLVED_RUNTIME_POS: Final = frozenset(
    {"N", "POSL", "COLLOC", "ADJ_SHORT", "PARTICIPLE_SHORT", "INFINITIVE"}
)
KNOWN_RUNTIME_POS: Final = frozenset(DIRECT_RUNTIME_TO_BUCKET) | _UNRESOLVED_RUNTIME_POS
_SMOKE_TEXT: Final = "Красный быстро бежит."


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


def analyze_pos_with_pylem(text: str) -> dict[str, object]:
    """Run the exact installed ``pylem==0.0.18`` provider on ``text``.

    The installed distribution version is checked before importing the native module.
    This does not prove dictionary equivalence to FantLab; it proves only which provider
    package/runtime supplied the candidate matrix consumed by the inferred POS profile.
    """

    holder = _load_native_holder()
    return analyze_pos_with_holder(text, holder)


def build_native_runtime_receipt() -> dict[str, object]:
    """Execute a tiny native smoke and return a source-free provenance receipt."""

    holder = _load_native_holder()
    candidates = runtime_candidates_from_holder(_SMOKE_TEXT, holder)
    artifact = analyze_pos_metrics(
        _SMOKE_TEXT,
        candidates,
        runtime_profile=PYLEM_RUNTIME_PROFILE,
    )
    observed = sorted({runtime_pos for row in candidates for runtime_pos in row})
    metrics = artifact["metrics"]
    return {
        "schema_version": PYLEM_RUNTIME_RECEIPT_SCHEMA,
        "provider": {
            "distribution": PYLEM_DISTRIBUTION,
            "version": PYLEM_VERSION,
            "runtime_profile": PYLEM_RUNTIME_PROFILE,
            "mapping_contract": POS_MAPPING_CONTRACT,
        },
        "runtime": {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "fixture": {
            "normalized_sha256": artifact["normalized_sha256"],
            "word_count": artifact["input"]["word_count"],
            "sentence_count": artifact["input"]["sentence_count"],
            "runtime_analysis_sha256": artifact["runtime_analysis_sha256"],
            "observed_runtime_pos": observed,
            "source_text_included": False,
        },
        "result": {
            "defined_count": metrics["defined"]["count"],
            "undefined_count": metrics["undefined"]["count"],
            "compatibility_status": artifact["compatibility_status"],
        },
        "epistemic_boundary": {
            "fantlab_dictionary_equivalence": "unknown",
            "homonym_selection_policy": "unresolved",
            "noun_cardinal_runtime_collision": "unresolved",
            "m2_parity_admissible": False,
        },
    }


def _load_native_holder() -> _Holder:
    try:
        installed = version(PYLEM_DISTRIBUTION)
    except PackageNotFoundError as exc:
        raise RuntimeError("pylem==0.0.18 is not installed in this runtime") from exc
    if installed != PYLEM_VERSION:
        raise RuntimeError(
            f"expected pylem=={PYLEM_VERSION}, found {PYLEM_DISTRIBUTION}=={installed}"
        )

    from pylem import MorphanHolder, MorphLanguage

    return MorphanHolder(MorphLanguage.Russian)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute the pinned pylem native smoke and emit a source-free receipt."
    )
    parser.add_argument("--receipt", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    receipt = build_native_runtime_receipt()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
