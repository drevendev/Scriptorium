"""Source-free diagnostic for the separately frozen Road to Nowhere alternate transcription.

Measures only Wikisource oldid 5585836 (az.lib family), not the incomplete
Pravda-1965 Wikisource route. FantLab input identity is UNKNOWN; M2 remains 0/5.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Callable, Mapping, Sequence

from . import road_nowhere_freeze as freeze
from .metrics import METRIC_CONTRACT_ID, SCHEMA_VERSION, analyze_deterministic_metrics

DIAGNOSTIC_VERSION = "scriptorium-road-nowhere-alternate-field-diagnostic-v1"
FROZEN_BODY_CHARACTERS = 442_656
FROZEN_BODY_SHA256 = "e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee"
FROZEN_WIKITEXT_SHA256 = "f47b9b05d06dc2f5c6e2642d0822e6db68128386e4f1374b9188206a69fef11b"
FANTLAB_REFERENCES = {"fantlab.general.characters": "438439", "fantlab.general.words": "61299"}
FANTLAB_URL = "https://fantlab.ru/work27346/lp"
FANTLAB_DATE = "2022-09-18"
_UNBOUND = frozenset({
    "fantlab.vocabulary.active_dictionary", "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000", "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})
_OPTIONAL_UNAVAILABLE = frozenset({
    "fantlab.dialogue.mean_narration_sentence_length_chars",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars",
    "fantlab.dialogue.author_text_inside_dialogue_percent",
})


def _validate_pins(revision: Mapping[str, object], body: Mapping[str, object]) -> Mapping[str, object]:
    """Reject rights, source or body drift before attempting the network."""
    freeze.validate_revision_manifest(revision)
    freeze.validate_body_manifest(body, revision_manifest=revision)
    source = revision.get("source_identity")
    body_source = body.get("source_revision")
    identity = body.get("literary_body_identity")
    if not isinstance(source, dict) or not isinstance(body_source, dict) or not isinstance(identity, dict):
        raise ValueError("Road to Nowhere source/body identity missing")
    if (
        revision.get("candidate_id") != freeze.CANDIDATE_ID
        or revision.get("legal_basis") != "public_domain"
        or source.get("revision_id") != freeze.REVISION_ID
        or body_source.get("revision_id") != freeze.REVISION_ID
        or source.get("wikitext_sha256") != FROZEN_WIKITEXT_SHA256
        or body_source.get("wikitext_sha256") != FROZEN_WIKITEXT_SHA256
        or source.get("mediawiki_sha1") != body_source.get("mediawiki_sha1")
        or identity.get("character_count_including_spaces") != FROZEN_BODY_CHARACTERS
        or identity.get("normalized_character_count_including_spaces") != FROZEN_BODY_CHARACTERS
        or identity.get("raw_sha256") != FROZEN_BODY_SHA256
        or identity.get("normalized_sha256") != FROZEN_BODY_SHA256
        or body.get("diagnostic_comparison_admissible") is not True
        or body.get("m2_parity_admissible") is not False
        or body.get("fantlab_source_edition_match") != "unknown"
    ):
        raise ValueError("Road to Nowhere manifests differ from canonical alternate pins")
    return identity


def build_diagnostic(revision: Mapping[str, object], body_manifest: Mapping[str, object], *,
                     fetcher: Callable[..., dict[str, object]] = freeze.fetch_pinned_wikitext
                     ) -> dict[str, object]:
    """Replay the source/body transiently and emit only derived numeric rows."""
    identity = _validate_pins(revision, body_manifest)
    captured: dict[str, str] = {}

    def capture(*, title: str, revision_id: int) -> dict[str, object]:
        observed = fetcher(title=title, revision_id=revision_id)
        if not isinstance(observed, dict) or not isinstance(observed.get("wikitext"), str):
            raise ValueError("pinned Road to Nowhere revision missing wikitext")
        captured["wikitext"] = observed["wikitext"]
        return dict(observed)

    receipt = freeze.replay_body_manifest(revision, body_manifest, fetcher=capture)
    if (
        receipt.get("verified") is not True
        or receipt.get("source_text_included") is not False
        or receipt.get("m2_parity_admissible") is not False
        or receipt.get("raw_sha256") != FROZEN_BODY_SHA256
    ):
        raise ValueError("Road to Nowhere replay or parity boundary drift")
    literary = freeze.extract_literary_body(captured["wikitext"])
    if (len(literary) != FROZEN_BODY_CHARACTERS or
            sha256(literary.encode("utf-8")).hexdigest() != FROZEN_BODY_SHA256):
        raise ValueError("Road to Nowhere literary-body identity drift")
    analysis = analyze_deterministic_metrics(literary)
    if (
        analysis.get("schema_version") != SCHEMA_VERSION
        or analysis.get("metric_contract_id") != METRIC_CONTRACT_ID
        or analysis.get("normalized_sha256") != FROZEN_BODY_SHA256
        or analysis.get("dependencies", {}).get("vocabulary_dictionary") is not None
    ):
        raise ValueError("Road to Nowhere profile/dictionary/normalization drift")
    metrics = analysis.get("metrics")
    if not isinstance(metrics, dict) or len(metrics) != 29:
        raise ValueError("Road to Nowhere must have 29 deterministic metric rows")
    if not (_UNBOUND | FANTLAB_REFERENCES.keys()) <= metrics.keys():
        raise ValueError("required Road to Nowhere metric missing")
    rows = []
    for metric_id, metric in sorted(metrics.items()):
        if not isinstance(metric, dict):
            raise ValueError("invalid Road to Nowhere metric record")
        value, unit, status = (metric.get("value"), metric.get("unit"),
                               metric.get("compatibility_status"))
        if (
            not isinstance(unit, str) or not unit
            or status not in ("inferred", "extension")
            or (value is not None and (type(value) not in (int, float) or not math.isfinite(value)))
        ):
            raise ValueError("invalid Road to Nowhere metric value, unit or compatibility")
        reference = FANTLAB_REFERENCES.get(metric_id)
        if metric_id in _UNBOUND:
            if value is not None:
                raise ValueError("dictionary-dependent metric cannot be measured without a dictionary")
            result = "NOT_RUN_DICTIONARY_UNBOUND"
        elif value is None:
            if metric_id not in _OPTIONAL_UNAVAILABLE:
                raise ValueError("unexpectedly null Road to Nowhere metric")
            result = "UNAVAILABLE_NO_OBSERVATIONS"
        else:
            result = ("DIAGNOSTIC_SOURCE_UNMATCHED" if reference is not None
                      else "MEASURED_REFERENCE_UNAVAILABLE")
        if reference is not None and type(value) is not int:
            raise ValueError("FantLab integer reference needs an integer observation")
        rows.append({
            "metric_id": metric_id, "actual": value, "unit": unit,
            "compatibility_status": status, "fantlab_display": reference,
            "actual_minus_fantlab_display": value - int(reference) if reference is not None else None,
            "result": result,
        })
    if next(row["actual"] for row in rows if row["metric_id"] == "fantlab.general.characters") != FROZEN_BODY_CHARACTERS:
        raise ValueError("Road to Nowhere measured character count drift")
    return {
        "diagnostic_version": DIAGNOSTIC_VERSION,
        "candidate_id": freeze.CANDIDATE_ID,
        "source_text_committed": False,
        "body_identity": {
            "revision_id": freeze.REVISION_ID, "extraction_profile": freeze.EXTRACTION_PROFILE,
            "character_count_including_spaces": FROZEN_BODY_CHARACTERS,
            "raw_sha256": FROZEN_BODY_SHA256, "normalized_sha256": identity["normalized_sha256"],
        },
        "scriptorium": {
            "schema_version": analysis["schema_version"],
            "metric_contract_id": analysis["metric_contract_id"],
            "profiles": analysis["profiles"], "vocabulary_dictionary_dependency": None,
        },
        "fantlab": {
            "analysis_url": FANTLAB_URL, "analysis_date": FANTLAB_DATE,
            "public_display_references_retained": dict(FANTLAB_REFERENCES),
            "source_edition_disclosed": False, "source_bytes_disclosed": False,
        },
        "comparison_policy": {
            "class": "diagnostic_unmatched_source",
            "transcription_family": "alternate_az_lib_not_primary_pravda_1965",
            "available_reference_fields": 2,
            "other_reference_fields": "NOT_RETAINED",
            "reference_rounding_evidence": "UNKNOWN",
            "numeric_similarity_does_not_prove_source_identity": True,
        },
        "metric_rows": rows,
        "gates": {
            "calibration_size_met": True,
            "alternate_transcription_diagnostic_ready": True,
            "primary_1965_transcription_body_ready": False,
            "fantlab_source_edition_match": "unknown",
            "m2_parity_admissible": False, "m2_weight": 0,
        },
    }


def render_json(artifact: Mapping[str, object]) -> str:
    return json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"


def write_new(path: Path, artifact: Mapping[str, object]) -> None:
    """Create only; preserve any previously reviewed evidence."""
    with path.open("x", encoding="utf-8") as output:
        output.write(render_json(artifact))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision-manifest", type=Path, required=True)
    parser.add_argument("--body-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    revision = json.loads(args.revision_manifest.read_text(encoding="utf-8"))
    body = json.loads(args.body_manifest.read_text(encoding="utf-8"))
    if not isinstance(revision, dict) or not isinstance(body, dict):
        raise ValueError("Road to Nowhere manifests must be JSON objects")
    artifact = build_diagnostic(revision, body)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_new(args.output, artifact)
    print("ROAD_NOWHERE_ALTERNATE_DIAGNOSTIC=" + json.dumps({
        "rows": len(artifact["metric_rows"]),
        "measured": sum(row["actual"] is not None for row in artifact["metric_rows"]),
        "references": len(FANTLAB_REFERENCES), "source_text_committed": False,
        "m2_weight": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
