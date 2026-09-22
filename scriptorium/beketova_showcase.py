"""Source-free deterministic showcase for Beketova's *Children of Captain Grant*.

The builder re-fetches the exact frozen Russian Wikisource revision transiently,
verifies the already committed literary-body identity, runs the current deterministic
metric surface, and emits only derived values and provenance identifiers.  It is a
Scriptorium showcase, not FantLab parity evidence.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Mapping, Sequence

from .beketova_body import CANDIDATE_ID, TITLE, REVISION_ID, extract_literary_body, validate_body_manifest
from .metrics import analyze_deterministic_metrics
from .single_page_body import fetch_pinned_wikitext
from .single_page_revision import validate_manifest as validate_revision_manifest
from .text import normalize_text

SHOWCASE_VERSION = "scriptorium-beketova-deterministic-showcase-v1"
FROZEN_BODY_CHARACTERS = 1_095_467
FROZEN_BODY_SHA256 = "4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161"

# Keep the public artifact compact while spanning the currently implemented deterministic
# families. Dictionary-dependent rows are excluded because no compatible lexicon is bound.
SHOWCASE_METRICS = (
    "fantlab.general.characters",
    "fantlab.general.words",
    "scriptorium.general.sentences",
    "fantlab.general.mean_word_length_chars",
    "fantlab.general.mean_sentence_length_chars",
    "fantlab.dialogue.share_percent",
    "fantlab.dialogue.author_text_inside_dialogue_percent",
    "fantlab.vocabulary.unique_words",
    "fantlab.punctuation.comma.per_1000_words",
    "fantlab.punctuation.dash.per_1000_words",
    "fantlab.punctuation.question.per_1000_words",
)


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _verify_source_and_load_body(
    revision_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> str:
    validate_revision_manifest(revision_manifest)
    if revision_manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Beketova candidate id")
    identity = revision_manifest.get("source_identity")
    if not isinstance(identity, dict):
        raise ValueError("Beketova revision identity missing")
    if identity.get("title") != TITLE or identity.get("revision_id") != REVISION_ID:
        raise ValueError("revision manifest does not identify the frozen Beketova revision")

    observed = fetcher(title=TITLE, revision_id=REVISION_ID)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient Beketova source prose missing")
    if observed != identity:
        differing = sorted(
            key for key in set(observed) | set(identity) if observed.get(key) != identity.get(key)
        )
        raise ValueError(f"pinned Beketova revision identity drift before analysis: {differing}")
    return extract_literary_body(wikitext)


def _verify_body_identity(body: str, body_manifest: Mapping[str, object]) -> None:
    identity = body_manifest.get("literary_body_identity")
    if not isinstance(identity, dict):
        raise ValueError("Beketova body identity missing")
    raw = body.encode("utf-8")
    normalized = normalize_text(body)
    observed = {
        "character_count_including_spaces": len(body),
        "utf8_byte_count": len(raw),
        "raw_sha256": sha256(raw).hexdigest(),
        "normalized_character_count_including_spaces": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }
    for key, value in observed.items():
        if identity.get(key) != value:
            raise ValueError(f"frozen Beketova body identity drift for {key}")
    if observed["character_count_including_spaces"] != FROZEN_BODY_CHARACTERS:
        raise ValueError("Beketova frozen character-count constant drift")
    if observed["raw_sha256"] != FROZEN_BODY_SHA256:
        raise ValueError("Beketova frozen body SHA-256 constant drift")


def build_showcase(
    revision_manifest: Mapping[str, object],
    body_manifest: Mapping[str, object],
    *,
    body_loader: Callable[[Mapping[str, object]], str] | None = None,
    enforce_canonical_body: bool = True,
) -> dict[str, object]:
    """Return a compact source-free deterministic analysis of the frozen work."""

    validate_body_manifest(body_manifest, revision_manifest=revision_manifest)
    body = body_loader(revision_manifest) if body_loader is not None else _verify_source_and_load_body(revision_manifest)
    if not isinstance(body, str) or not body:
        raise ValueError("Beketova body loader returned empty or non-string text")
    if enforce_canonical_body:
        _verify_body_identity(body, body_manifest)

    analysis = analyze_deterministic_metrics(body)
    metrics = analysis.get("metrics")
    if not isinstance(metrics, Mapping):
        raise ValueError("deterministic metric artifact missing metrics")

    rows: list[dict[str, object]] = []
    for metric_id in SHOWCASE_METRICS:
        row = metrics.get(metric_id)
        if not isinstance(row, Mapping):
            raise ValueError(f"deterministic metric missing: {metric_id}")
        value = row.get("value")
        if value is None:
            raise ValueError(f"showcase metric unexpectedly null: {metric_id}")
        rows.append(
            {
                "metric_id": metric_id,
                "value": value,
                "unit": row.get("unit"),
                "compatibility_status": row.get("compatibility_status"),
            }
        )

    body_identity = body_manifest["literary_body_identity"]
    source_revision = body_manifest["source_revision"]
    assert isinstance(body_identity, Mapping) and isinstance(source_revision, Mapping)
    return {
        "showcase_version": SHOWCASE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "translation_identity": "Alexandra A. Beketova Russian translation",
        "source_text_committed": False,
        "source_revision": {
            "provider": body_manifest.get("provider"),
            "revision_id": source_revision["revision_id"],
            "mediawiki_sha1": source_revision["mediawiki_sha1"],
        },
        "body_identity": {
            "character_count_including_spaces": body_identity["character_count_including_spaces"],
            "raw_sha256": body_identity["raw_sha256"],
        },
        "scriptorium": {
            "schema_version": analysis["schema_version"],
            "metric_contract_id": analysis["metric_contract_id"],
            "profiles": analysis["profiles"],
            "vocabulary_dictionary_dependency": analysis["dependencies"]["vocabulary_dictionary"],
        },
        "metrics": rows,
        "interpretation": {
            "class": "scriptorium_deterministic_showcase",
            "fantlab_comparison_performed": False,
            "fantlab_namespaced_metric_ids_are_compatibility_candidates_not_parity_claims": True,
        },
        "gates": {
            "general_calibration_profile_admissible": True,
            "fantlab_source_edition_match": "unknown",
            "showcase_ready": True,
            "gate_ready": False,
            "m2_parity_admissible": False,
            "m2_weight": 0,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay Beketova Captain Grant and emit a source-free deterministic showcase.")
    parser.add_argument("--revision-manifest", type=Path, required=True)
    parser.add_argument("--body-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    artifact = build_showcase(_load_json(args.revision_manifest), _load_json(args.body_manifest))
    text = json.dumps(artifact, ensure_ascii=False, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
