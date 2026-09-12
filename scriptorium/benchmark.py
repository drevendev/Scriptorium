"""Provenance-safe FantLab benchmark comparison harness.

The harness executes the already-versioned ``fantlab-benchmark-comparison-v1``
contract. Numeric resemblance alone never upgrades a result to parity evidence:
integer equality is gated by exact source-edition/legal provenance and decimal
fields remain unresolved while FantLab display precision/tie behavior is unknown.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Final, Iterable

from .dialogue import DIALOGUE_PROFILE
from .metrics import (
    METRIC_CONTRACT_ID,
    METRIC_PROFILE,
    PUNCTUATION_KEYS,
    PUNCTUATION_PROFILE,
    analyze_deterministic_metrics,
)
from .text import NORMALIZATION_PROFILE


BENCHMARK_PROFILE: Final = "scriptorium-benchmark-v1"
BENCHMARK_SCHEMA_VERSION: Final = "fantlab-benchmark-comparison-v1"
COMPATIBILITY_PROFILE: Final = (
    f"{METRIC_PROFILE}+{DIALOGUE_PROFILE}+{PUNCTUATION_PROFILE}"
)

_GENERAL_SPECS: Final = (
    (
        "fantlab.general.characters",
        ("characters",),
        "Длина текста, знаков",
        "exact_integer",
    ),
    (
        "fantlab.general.words",
        ("words",),
        "Слов в произведении (СВП)",
        "exact_integer",
    ),
    (
        "fantlab.general.mean_word_length_chars",
        ("mean_word_length_characters",),
        "Средняя длина слова, знаков",
        "unresolved_precision",
    ),
    (
        "fantlab.general.mean_sentence_length_chars",
        ("mean_sentence_length_characters",),
        "Средняя длина предложения (СДП), знаков",
        "unresolved_precision",
    ),
)
_DIALOGUE_SPECS: Final = (
    (
        "fantlab.dialogue.mean_narration_sentence_length_chars",
        ("mean_narration_sentence_length_characters",),
        "СДП авторского текста, знаков",
        "unresolved_precision",
    ),
    (
        "fantlab.dialogue.mean_dialogue_sentence_length_chars",
        ("mean_dialogue_sentence_length_characters",),
        "СДП диалога, знаков",
        "unresolved_precision",
    ),
    (
        "fantlab.dialogue.share_percent",
        ("dialogue_share_percent",),
        "Доля диалогов в тексте",
        "unresolved_precision",
    ),
    (
        "fantlab.dialogue.author_text_inside_dialogue_percent",
        ("author_text_inside_dialogue_percent",),
        "Доля авторского текста в диалогах",
        "unresolved_precision",
    ),
)
_PUNCTUATION_LABELS: Final = {
    "comma": ",",
    "period": ".",
    "dash": "-",
    "exclamation": "!",
    "question": "?",
    "ellipsis": "...",
    "exclamation_ellipsis": "!..",
    "question_ellipsis": "?..",
    "triple_exclamation": "!!!",
    "question_exclamation": "?!",
    "quote": '"',
    "parentheses": "()",
    "colon": ":",
    "semicolon": ";",
}


def build_comparison(
    reference_json: str,
    source_bytes: bytes,
    *,
    scriptorium_revision: str,
    edition_match: str = "unknown",
    edition_label: str | None = None,
    source_reference: str | None = None,
    legal_basis: str | None = None,
) -> dict[str, object]:
    """Build one deterministic FantLab comparison artifact.

    ``reference_json`` is parsed twice: once numerically and once with numeric
    tokens preserved as strings. The second parse retains lexical evidence such
    as ``10.30`` that ordinary JSON decoding would collapse to ``10.3``.
    """

    if edition_match not in {"exact", "strong", "weak", "unknown"}:
        raise ValueError("edition_match must be exact, strong, weak, or unknown")
    if not scriptorium_revision:
        raise ValueError("scriptorium_revision must be non-empty")

    reference = json.loads(reference_json)
    lexical_reference = json.loads(reference_json, parse_int=str, parse_float=str)
    text = source_bytes.decode("utf-8")
    analysis = analyze_deterministic_metrics(text)

    raw_sha256 = sha256(source_bytes).hexdigest()
    source_text = {
        "edition_match": edition_match,
        "edition_label": _none_if_blank(edition_label),
        "source_reference": _none_if_blank(source_reference),
        "legal_basis": _none_if_blank(legal_basis),
        "raw_sha256": raw_sha256,
        "normalized_sha256": analysis["normalized_sha256"],
    }

    metrics: dict[str, object] = {}
    for metric_id, path, source_label, rule in _reference_specs():
        expected = _lookup(reference.get("expected", {}), path)
        if expected is _MISSING:
            continue
        expected_display = _lookup(lexical_reference.get("expected", {}), path)
        if expected_display is _MISSING:
            raise ValueError(f"missing lexical expected value for {metric_id}")

        actual_row = analysis["metrics"].get(metric_id)
        if actual_row is None:
            raise ValueError(f"analyzer does not emit mapped metric {metric_id}")

        actual = actual_row["value"]
        metrics[metric_id] = _comparison_row(
            expected=expected,
            expected_display=str(expected_display),
            actual=actual,
            definition_evidence=actual_row["definition_evidence"],
            source_label=source_label,
            rule=rule,
            provenance_admissible=_provenance_admissible(source_text),
        )

    if not metrics:
        raise ValueError("reference contains no currently implemented comparable metrics")

    return {
        "schema_version": BENCHMARK_SCHEMA_VERSION,
        "benchmark_id": reference["benchmark_id"],
        "metric_contract_id": METRIC_CONTRACT_ID,
        "reference": reference["reference"],
        "source_text": source_text,
        "analyzer": {
            "scriptorium_revision": scriptorium_revision,
            "compatibility_profile": COMPATIBILITY_PROFILE,
            "normalization_profile": NORMALIZATION_PROFILE,
        },
        "metrics": metrics,
    }


def _reference_specs() -> Iterable[tuple[str, tuple[str, ...], str, str]]:
    yield from _GENERAL_SPECS
    yield from _DIALOGUE_SPECS
    for key in PUNCTUATION_KEYS:
        yield (
            f"fantlab.punctuation.{key}.per_1000_words",
            ("punctuation_per_1000_words", key),
            _PUNCTUATION_LABELS[key],
            "unresolved_precision",
        )


def _comparison_row(
    *,
    expected: int | float,
    expected_display: str,
    actual: int | float | None,
    definition_evidence: str,
    source_label: str,
    rule: str,
    provenance_admissible: bool,
) -> dict[str, object]:
    raw_delta = None if actual is None else actual - expected
    actual_display = None if actual is None else str(actual)

    if rule == "exact_integer":
        numeric_match = None if actual is None else actual == expected
        if actual is None:
            result = "not_run"
            reason = "The analyzer did not produce an actual value."
        elif not provenance_admissible:
            result = "unresolved"
            reason = (
                "Numeric equality is diagnostic only because exact edition/legal "
                "provenance required for parity is incomplete."
            )
        elif numeric_match:
            result = "pass"
            reason = None
        else:
            result = "fail"
            reason = "Exact source-matched integer value differs from the FantLab reference."
        display_places: int | None = 0
    elif rule == "unresolved_precision":
        numeric_match = None
        result = "unresolved"
        display_places = None
        reasons = [
            "FantLab display precision and tie-breaking are not independently established."
        ]
        if not provenance_admissible:
            reasons.append("Exact edition/legal provenance required for parity is incomplete.")
        if actual is None:
            reasons.append("The analyzer produced no numeric value for this input.")
        reason = " ".join(reasons)
    else:
        raise ValueError(f"unsupported comparison rule: {rule}")

    return {
        "definition_evidence": definition_evidence,
        "expected": {
            "numeric_value": expected,
            "display_text": expected_display,
            "display_places": display_places,
            "source_label": source_label,
        },
        "actual": {
            "raw_value": actual,
            "display_text": actual_display,
        },
        "comparison": {
            "rule": rule,
            "numeric_match": numeric_match,
            "raw_delta": raw_delta,
            "result": result,
            "reason": reason,
        },
    }


def _provenance_admissible(source_text: dict[str, object]) -> bool:
    return (
        source_text["edition_match"] == "exact"
        and bool(source_text["edition_label"])
        and bool(source_text["source_reference"])
        and bool(source_text["legal_basis"])
        and bool(source_text["raw_sha256"])
    )


class _Missing:
    pass


_MISSING = _Missing()


def _lookup(data: object, path: tuple[str, ...]) -> object:
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return _MISSING
        current = current[key]
    return current


def _none_if_blank(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare a local UTF-8 text against a captured FantLab reference."
    )
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--scriptorium-revision", required=True)
    parser.add_argument(
        "--edition-match",
        choices=("exact", "strong", "weak", "unknown"),
        default="unknown",
    )
    parser.add_argument("--edition-label")
    parser.add_argument("--source-reference")
    parser.add_argument("--legal-basis")
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    artifact = build_comparison(
        args.reference.read_text(encoding="utf-8"),
        args.text.read_bytes(),
        scriptorium_revision=args.scriptorium_revision,
        edition_match=args.edition_match,
        edition_label=args.edition_label,
        source_reference=args.source_reference,
        legal_basis=args.legal_basis,
    )
    rendered = json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
