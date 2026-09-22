"""Source-free deterministic diagnostics for Grin's *Running on Waves*.

The diagnostic replays the exact frozen 36-page Wikisource body transiently, verifies
its committed identity, runs the current deterministic metric profile, and persists only
derived values plus FantLab's public display references.  The FantLab analyzer input is
not source-matched, so every comparison is diagnostic-only and contributes zero to M2.
"""

from __future__ import annotations

import argparse
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from .metrics import analyze_deterministic_metrics
from .running_waves_body import (
    CHAPTER_SEPARATOR,
    MANIFEST_VERSION as BODY_MANIFEST_VERSION,
    _extract_bodies,
    validate_manifest as validate_body_manifest,
)
from .running_waves_inventory import CANDIDATE_ID
from .wikisource_replay import fetch_pinned_chapter_revisions

DIAGNOSTIC_VERSION = "scriptorium-running-waves-fantlab-diagnostic-v1"
FANTLAB_WORK_ID = 27344
FANTLAB_ANALYSIS_URL = "https://fantlab.ru/work27344/lp"
FANTLAB_ANALYSIS_DATE = "2022-09-18"
FROZEN_BODY_SHA256 = "41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc"
FROZEN_BODY_CHARACTERS = 363_819

# Exact display strings observed on FantLab's public work27344 analysis surface.
# Dictionary-dependent rows are retained as references but deliberately remain not-run
# until Scriptorium binds a dictionary compatible with the diagnostic run.
FANTLAB_REFERENCES: tuple[tuple[str, str, bool], ...] = (
    ("fantlab.general.characters", "360987", False),
    ("fantlab.general.words", "52985", False),
    ("fantlab.general.mean_word_length_chars", "5.16", False),
    ("fantlab.general.mean_sentence_length_chars", "73.46", False),
    ("fantlab.dialogue.mean_narration_sentence_length_chars", "97", False),
    ("fantlab.dialogue.mean_dialogue_sentence_length_chars", "52.67", False),
    ("fantlab.dialogue.share_percent", "38.23", False),
    ("fantlab.dialogue.author_text_inside_dialogue_percent", "12.49", False),
    ("fantlab.vocabulary.unique_words", "7107", False),
    ("fantlab.vocabulary.active_dictionary", "6784", True),
    ("fantlab.vocabulary.active_nondictionary", "323", True),
    ("fantlab.vocabulary.uasz_3000", "1170.79", True),
    ("fantlab.vocabulary.uasz_10000", "2636.17", True),
    ("fantlab.punctuation.comma.per_1000_words", "154.03", False),
    ("fantlab.punctuation.period.per_1000_words", "76.08", False),
    ("fantlab.punctuation.dash.per_1000_words", "29.84", False),
    ("fantlab.punctuation.exclamation.per_1000_words", "6.55", False),
    ("fantlab.punctuation.question.per_1000_words", "5.96", False),
    ("fantlab.punctuation.ellipsis.per_1000_words", "1.93", False),
    ("fantlab.punctuation.exclamation_ellipsis.per_1000_words", "0.06", False),
    ("fantlab.punctuation.question_ellipsis.per_1000_words", "0.04", False),
    ("fantlab.punctuation.triple_exclamation.per_1000_words", "0.00", False),
    ("fantlab.punctuation.question_exclamation.per_1000_words", "0.55", False),
    ("fantlab.punctuation.quote.per_1000_words", "10.72", False),
    ("fantlab.punctuation.parentheses.per_1000_words", "0.21", False),
    ("fantlab.punctuation.colon.per_1000_words", "5.42", False),
    ("fantlab.punctuation.semicolon.per_1000_words", "6.53", False),
)


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _numeric_display(value: str) -> Decimal:
    return Decimal(value)


def _delta(actual: object, display: str) -> int | str:
    if isinstance(actual, bool) or not isinstance(actual, (int, float)):
        raise TypeError("diagnostic metric value must be numeric")
    if isinstance(actual, int) and "." not in display:
        return actual - int(display)
    delta = Decimal(str(actual)) - _numeric_display(display)
    return format(delta, "f")


def _verify_composite_identity(composite: str, body_manifest: Mapping[str, object]) -> None:
    identity = body_manifest.get("composite_identity")
    if not isinstance(identity, Mapping):
        raise ValueError("missing Running on Waves composite identity")
    observed_bytes = composite.encode("utf-8")
    observed = {
        "character_count_including_spaces": len(composite),
        "utf8_byte_count": len(observed_bytes),
        "raw_sha256": sha256(observed_bytes).hexdigest(),
    }
    for key, value in observed.items():
        if identity.get(key) != value:
            raise ValueError(f"frozen Running on Waves body identity drift for {key}")
    if observed["character_count_including_spaces"] != FROZEN_BODY_CHARACTERS:
        raise ValueError("Running on Waves frozen character-count constant drift")
    if observed["raw_sha256"] != FROZEN_BODY_SHA256:
        raise ValueError("Running on Waves frozen body SHA-256 constant drift")


def build_diagnostic(
    source_manifest: Mapping[str, object],
    body_manifest: Mapping[str, object],
    *,
    fetcher: Callable[
        [Iterable[Mapping[str, object]]], dict[str, str]
    ] = fetch_pinned_chapter_revisions,
    enforce_canonical_body: bool = True,
) -> dict[str, object]:
    """Replay the frozen body and return a source-free diagnostic artifact."""

    validate_body_manifest(body_manifest, source_manifest)
    _, bodies = _extract_bodies(source_manifest, fetcher=fetcher)
    composite = CHAPTER_SEPARATOR.join(bodies)
    if enforce_canonical_body:
        _verify_composite_identity(composite, body_manifest)

    analysis = analyze_deterministic_metrics(composite)
    metrics = analysis.get("metrics")
    if not isinstance(metrics, Mapping):
        raise ValueError("deterministic metric artifact missing metrics")

    rows: list[dict[str, object]] = []
    for metric_id, display, dependency_unbound in FANTLAB_REFERENCES:
        metric = metrics.get(metric_id)
        if not isinstance(metric, Mapping):
            raise ValueError(f"deterministic metric missing: {metric_id}")
        actual = metric.get("value")
        if dependency_unbound:
            if actual is not None:
                raise ValueError(f"dictionary-dependent metric unexpectedly ran: {metric_id}")
            status = "not_run_dependency_unbound"
            delta: int | str | None = None
        else:
            if actual is None:
                raise ValueError(f"implemented diagnostic metric unexpectedly null: {metric_id}")
            status = "diagnostic_only_source_unmatched"
            delta = _delta(actual, display)
        rows.append(
            {
                "metric_id": metric_id,
                "fantlab_display_value": display,
                "scriptorium_raw_value": actual,
                "delta_against_fantlab_display": delta,
                "status": status,
            }
        )

    return {
        "diagnostic_version": DIAGNOSTIC_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_text_committed": False,
        "body_identity": {
            "manifest_version": BODY_MANIFEST_VERSION,
            "character_count_including_spaces": body_manifest["composite_identity"][
                "character_count_including_spaces"
            ],
            "raw_sha256": body_manifest["composite_identity"]["raw_sha256"],
        },
        "scriptorium": {
            "schema_version": analysis["schema_version"],
            "metric_contract_id": analysis["metric_contract_id"],
            "profiles": analysis["profiles"],
            "vocabulary_dictionary_dependency": analysis["dependencies"][
                "vocabulary_dictionary"
            ],
        },
        "fantlab": {
            "work_id": FANTLAB_WORK_ID,
            "analysis_url": FANTLAB_ANALYSIS_URL,
            "analysis_date": FANTLAB_ANALYSIS_DATE,
            "source_edition_disclosed": False,
            "source_bytes_disclosed": False,
        },
        "comparison_policy": {
            "class": "diagnostic_unmatched_source",
            "displayed_reference_is_not_exact_parity_tolerance": True,
            "decimal_display_precision_not_promoted_to_parity_rule": True,
            "numeric_resemblance_cannot_establish_source_identity": True,
        },
        "metrics": rows,
        "gates": {
            "general_calibration_profile_admissible": True,
            "fantlab_source_edition_match": "unknown",
            "diagnostic_ready": True,
            "gate_ready": False,
            "m2_parity_admissible": False,
            "m2_weight": 0,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Replay Running on Waves and emit source-free FantLab diagnostics."
    )
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--body-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    artifact = build_diagnostic(
        _load_object(args.source_manifest),
        _load_object(args.body_manifest),
    )
    text = json.dumps(artifact, ensure_ascii=False, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
