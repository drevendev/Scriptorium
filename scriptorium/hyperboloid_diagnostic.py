"""Source-free diagnostic of frozen Hyperboloid literary metrics (not FantLab parity)."""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Callable, Mapping, Sequence
from . import hyperboloid_freeze as freeze
from .metrics import METRIC_CONTRACT_ID, SCHEMA_VERSION, analyze_deterministic_metrics

DIAGNOSTIC_VERSION = "scriptorium-hyperboloid-field-diagnostic-v1"
FROZEN_BODY_CHARACTERS = 499_066
FROZEN_BODY_SHA256 = "a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513"
FROZEN_NORMALIZED_SHA256 = FROZEN_BODY_SHA256
FROZEN_WIKITEXT_SHA256 = "fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9"
FANTLAB_REFERENCES = {
    "fantlab.general.characters": "495539",
    "fantlab.general.words": "69126",
}
FANTLAB_URL = "https://fantlab.ru/work44824/lp"
FANTLAB_DATE = "2022-09-18"
_UNBOUND = frozenset({
    "fantlab.vocabulary.active_dictionary", "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000", "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})
_OPTIONAL_NO_OBSERVATIONS = frozenset({
    "fantlab.dialogue.mean_narration_sentence_length_chars",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars",
    "fantlab.dialogue.author_text_inside_dialogue_percent",
})

def _validate_pins(revision_manifest: Mapping[str, object],
                   body_manifest: Mapping[str, object]) -> Mapping[str, object]:
    """Reject altered revision, body, or rights evidence before network access."""
    freeze.validate_revision_manifest(revision_manifest)
    freeze.validate_body_manifest(body_manifest)
    source = revision_manifest.get("source_identity")
    body_source = body_manifest.get("source_revision")
    identity = body_manifest.get("literary_body_identity")
    if not isinstance(source, dict) or not isinstance(body_source, dict) or not isinstance(identity, dict):
        raise ValueError("Hyperboloid source/body manifest missing identity")
    if (
        revision_manifest.get("candidate_id") != freeze.CANDIDATE_ID
        or revision_manifest.get("legal_basis") != "public_domain"
        or body_source.get("revision_id") != freeze.REVISION_ID
        or source.get("wikitext_sha256") != FROZEN_WIKITEXT_SHA256
        or body_source.get("wikitext_sha256") != FROZEN_WIKITEXT_SHA256
        or body_source.get("mediawiki_sha1") != source.get("mediawiki_sha1")
        or identity.get("character_count_including_spaces") != FROZEN_BODY_CHARACTERS
        or identity.get("normalized_character_count_including_spaces") != FROZEN_BODY_CHARACTERS
        or identity.get("raw_sha256") != FROZEN_BODY_SHA256
        or identity.get("normalized_sha256") != FROZEN_NORMALIZED_SHA256
    ):
        raise ValueError("Hyperboloid manifests do not match canonical frozen pins")
    return identity

def build_diagnostic(revision_manifest: Mapping[str, object],
                     body_manifest: Mapping[str, object], *,
                     fetcher: Callable[..., dict[str, object]] = freeze.fetch_pinned_wikitext
                     ) -> dict[str, object]:
    """Replay the exact frozen body transiently and return derived numeric fields."""
    identity = _validate_pins(revision_manifest, body_manifest)
    captured: dict[str, str] = {}
    def capture(*, title: str, revision_id: int) -> dict[str, object]:
        observed = fetcher(title=title, revision_id=revision_id)
        if not isinstance(observed, dict) or not isinstance(observed.get("wikitext"), str):
            raise ValueError("Hyperboloid pinned revision missing transient wikitext")
        captured["wikitext"] = observed["wikitext"]
        return dict(observed)
    receipt = freeze.replay_body_manifest(revision_manifest, body_manifest, fetcher=capture)
    if (
        receipt.get("verified") is not True or receipt.get("source_text_included") is not False
        or receipt.get("m2_parity_admissible") is not False
        or receipt.get("raw_sha256") != FROZEN_BODY_SHA256
    ):
        raise ValueError("Hyperboloid replay receipt or scientific boundary drift")
    body = freeze.extract_literary_body(captured["wikitext"])
    if len(body) != FROZEN_BODY_CHARACTERS or sha256(body.encode("utf-8")).hexdigest() != FROZEN_BODY_SHA256:
        raise ValueError("Hyperboloid measured body differs from canonical pins")
    analysis = analyze_deterministic_metrics(body)
    if (
        analysis.get("schema_version") != SCHEMA_VERSION
        or analysis.get("metric_contract_id") != METRIC_CONTRACT_ID
        or analysis.get("normalized_sha256") != FROZEN_NORMALIZED_SHA256
        or analysis.get("dependencies", {}).get("vocabulary_dictionary") is not None
    ):
        raise ValueError("Hyperboloid analyzer profile, normalization or dependency drift")
    metrics = analysis.get("metrics")
    if not isinstance(metrics, dict) or len(metrics) != 29:
        raise ValueError("expected 29 deterministic Hyperboloid fields")
    if not (_UNBOUND | FANTLAB_REFERENCES.keys()) <= metrics.keys():
        raise ValueError("Hyperboloid required metric inventory missing")
    rows = []
    for metric_id, metric in sorted(metrics.items()):
        if not isinstance(metric, dict):
            raise ValueError("invalid Hyperboloid metric record")
        value, unit, compatibility = (
            metric.get("value"), metric.get("unit"), metric.get("compatibility_status")
        )
        if (
            not isinstance(unit, str) or not unit or compatibility not in ("inferred", "extension")
            or (value is not None and (type(value) not in (int, float) or not math.isfinite(value)))
        ):
            raise ValueError("invalid Hyperboloid metric value, unit or compatibility")
        reference = FANTLAB_REFERENCES.get(metric_id)
        if metric_id in _UNBOUND:
            if value is not None:
                raise ValueError("unbound dictionary unexpectedly produced a value")
            result = "NOT_RUN_DICTIONARY_UNBOUND"
        elif value is None:
            if metric_id not in _OPTIONAL_NO_OBSERVATIONS:
                raise ValueError("required Hyperboloid metric unexpectedly unavailable")
            result = "UNAVAILABLE_NO_OBSERVATIONS"
        else:
            result = ("DIAGNOSTIC_SOURCE_UNMATCHED" if reference is not None
                      else "MEASURED_REFERENCE_UNAVAILABLE")
        if reference is not None and type(value) is not int:
            raise ValueError("FantLab integral count requires integer measurement")
        rows.append({
            "metric_id": metric_id, "actual": value, "unit": unit,
            "compatibility_status": compatibility, "fantlab_display": reference,
            "actual_minus_fantlab_display": value - int(reference) if reference is not None else None,
            "result": result,
        })
    if next(r["actual"] for r in rows if r["metric_id"] == "fantlab.general.characters") != FROZEN_BODY_CHARACTERS:
        raise ValueError("Hyperboloid character count drift")
    return {
        "diagnostic_version": DIAGNOSTIC_VERSION,
        "candidate_id": freeze.CANDIDATE_ID, "source_text_committed": False,
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
            "class": "diagnostic_unmatched_source", "available_reference_fields": 2,
            "other_reference_fields": "NOT_RETAINED", "rounding_evidence": "UNKNOWN",
            "numeric_similarity_does_not_prove_source_identity": True,
        },
        "metric_rows": rows,
        "gates": {
            "calibration_size_met": True, "fantlab_source_edition_match": "unknown",
            "m2_parity_admissible": False, "m2_weight": 0,
        },
    }

def render_json(artifact: Mapping[str, object]) -> str:
    return json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"

def write_new(path: Path, artifact: Mapping[str, object]) -> None:
    """Create only: never overwrite independent measured evidence."""
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
        raise ValueError("Hyperboloid manifests must be objects")
    artifact = build_diagnostic(revision, body)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_new(args.output, artifact)
    print("HYPERBOLOID_DIAGNOSTIC=" + json.dumps({
        "rows": len(artifact["metric_rows"]),
        "measured": sum(row["actual"] is not None for row in artifact["metric_rows"]),
        "public_references": len(FANTLAB_REFERENCES), "m2_weight": 0, "source_text_committed": False,
    }, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
