"""Verify the original source-free Silver Dove CI artifact before retention or display.

The Git blob is byte-identical to the completed PR #325 measured-workflow artifact
(run 40266373995, commit 5f107a3d). Source/rights readiness is verified by the
existing five-work matrix before this module consumes its bound witness.
"""
from __future__ import annotations

from hashlib import sha1
import math
from pathlib import Path

from . import metrics, silver_dove_diagnostic
from .benchmark import _reference_specs
from .benchmark_readiness import _load

CANDIDATE_ID = "bely-silver-dove-ru"
ARTIFACT_PATH = "corpus/candidates/diagnostics/bely-silver-dove-ru.json"
ARTIFACT_GIT_BLOB_SHA1 = "88bfe95435be1b72703de65d314c6926b5f83a60"
REPLAY_HEAD_SHA = "5f107a3d79a9a2270f0e672b777093cf893b006b"


def _same(actual: object, expected: object, field: str) -> None:
    if type(actual) is not type(expected) or actual != expected:
        raise ValueError("Silver Dove retained evidence mismatch: " + field)


def verify(root: Path, witness: dict[str, object]) -> list[dict[str, object]]:
    """Return 29 strictly checked source-unmatched candidate/extension rows."""
    path = root / ARTIFACT_PATH
    if path.is_symlink():
        raise ValueError("Silver Dove retained evidence symlink refused")
    raw = path.read_bytes()
    digest = sha1(b"blob " + str(len(raw)).encode("ascii") + bytes((0,)) + raw).hexdigest()
    if not 0 < len(raw) < 200_000 or digest != ARTIFACT_GIT_BLOB_SHA1:
        raise ValueError("Silver Dove retained CI evidence blob drift")
    data = _load(root, ARTIFACT_PATH)
    if set(data) != {"body_identity", "candidate_id", "comparison_policy",
                     "diagnostic_version", "fantlab", "gates", "metric_rows",
                     "scriptorium", "source_text_committed"}:
        raise ValueError("Silver Dove retained evidence shape drift")
    _same(data["candidate_id"], CANDIDATE_ID, "candidate")
    _same(data["source_text_committed"], False, "source safety")
    _same(data["diagnostic_version"], silver_dove_diagnostic.DIAGNOSTIC_VERSION,
          "diagnostic version")
    _same(data["body_identity"], {
        "revision_id": silver_dove_diagnostic.freeze.SOURCE_REVISION_ID,
        "character_count_including_spaces": witness["source"]["characters_including_spaces"],
        "raw_sha256": witness["source"]["raw_sha256"],
        "normalized_sha256": witness["source"]["normalized_sha256"],
    }, "frozen source identity")
    _same(data["body_identity"]["raw_sha256"], silver_dove_diagnostic.FROZEN_BODY_SHA256,
          "canonical pinned body digest")
    _same(data["fantlab"], {
        "analysis_url": witness["fantlab"]["reference_url"],
        "analysis_date": witness["fantlab"]["analysis_date"],
        "public_display_references_retained": silver_dove_diagnostic.FANTLAB_REFERENCES,
        "source_edition_disclosed": False,
        "source_bytes_disclosed": False,
    }, "dated unmatched FantLab references")
    _same(data["comparison_policy"], {
        "class": "diagnostic_unmatched_source",
        "available_reference_fields": 2,
        "other_reference_fields": "NOT_RETAINED",
        "rounding_evidence": "UNKNOWN",
        "numeric_similarity_does_not_prove_source_identity": True,
    }, "comparison policy")
    _same(data["gates"], {
        "calibration_size_met": True,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
        "m2_weight": 0,
    }, "unchanged M2 gate")
    _same(data["scriptorium"], {
        "schema_version": metrics.SCHEMA_VERSION,
        "metric_contract_id": metrics.METRIC_CONTRACT_ID,
        "profiles": {
            "normalization": "scriptorium-text-v1",
            "metrics": "scriptorium-metrics-v4",
            "dialogue": "scriptorium-dialogue-v1",
            "vocabulary": "scriptorium-vocabulary-v1",
            "punctuation": "scriptorium-punctuation-v2",
        },
        "vocabulary_dictionary_dependency": None,
    }, "metric profiles")
    records = data["metric_rows"]
    expected_ids = {metric_id for metric_id, *_ in _reference_specs()} | {
        "scriptorium.general.sentences"
    }
    if (not isinstance(records, list) or len(records) != 29
            or any(not isinstance(item, dict) for item in records)
            or [item["metric_id"] for item in records if "metric_id" in item]
               != sorted(expected_ids)):
        raise ValueError("Silver Dove retained metric ID inventory drift")
    rows: list[dict[str, object]] = []
    for record in records:
        if set(record) != {
            "metric_id", "actual", "unit", "compatibility_status",
            "fantlab_display", "actual_minus_fantlab_display", "result"
        }:
            raise ValueError("Silver Dove metric row shape drift")
        metric_id = record["metric_id"]
        definition = metrics._METRIC_DEFINITIONS.get(metric_id)
        if definition is None:
            expected_unit, expected_status = "occurrences/1000_words", "inferred"
        else:
            expected_unit, _, expected_status = definition
        _same(record["unit"], expected_unit, "metric unit")
        _same(record["compatibility_status"], expected_status,
              "compatibility status")
        reference = silver_dove_diagnostic.FANTLAB_REFERENCES.get(metric_id)
        _same(record["fantlab_display"], reference, "reference field")
        actual, delta = record["actual"], record["actual_minus_fantlab_display"]
        if metric_id in silver_dove_diagnostic._UNBOUND:
            _same((actual, delta, record["result"]),
                  (None, None, "NOT_RUN_DICTIONARY_UNBOUND"),
                  "unbound dictionary state")
            status = "NOT_RUN"
        elif reference is not None:
            if (type(actual) is not int or type(delta) is not int
                    or delta != actual - int(reference)):
                raise ValueError("Silver Dove integer reference delta drift")
            _same(record["result"], "DIAGNOSTIC_SOURCE_UNMATCHED",
                  "unmatched reference status")
            status = "UNRESOLVED_SOURCE"
        else:
            if type(actual) not in (int, float) or not math.isfinite(actual):
                raise ValueError("Silver Dove invalid or missing numeric actual")
            _same(delta, None, "unknown reference delta")
            _same(record["result"], "MEASURED_REFERENCE_UNAVAILABLE",
                  "unavailable reference status")
            status = "MEASURED_NO_REFERENCE"
        rows.append({
            "metric_id": metric_id,
            "expected": int(reference) if reference is not None else None,
            "actual": actual,
            "actual_minus_expected": delta,
            "result": status,
            "comparison_kind": "EXTENSION_ONLY" if metric_id.startswith("scriptorium.") else "DIAGNOSTIC_ONLY",
            "display_rounding_evidence": "UNKNOWN",
        })
    if (sum(r["actual"] is not None for r in rows) != 24
            or sum(r["actual"] is None for r in rows) != 5):
        raise ValueError("Silver Dove verified field coverage drift")
    return rows
