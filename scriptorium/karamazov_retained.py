"""Verify the original source-free Brothers Karamazov CI artifact before retention or display.

The Git blob is byte-identical to the completed PR #327 measured-workflow artifact
(run 40441065263, commit ade9afa). Source/rights readiness is verified by the
existing five-work matrix before this module consumes its bound witness.
"""
from __future__ import annotations

from hashlib import sha1
import math
from pathlib import Path

from . import metrics, karamazov_diagnostic
from .benchmark import _reference_specs
from .benchmark_readiness import _load

CANDIDATE_ID = "dostoevsky-brothers-karamazov-ru"
ARTIFACT_PATH = "corpus/candidates/diagnostics/dostoevsky-brothers-karamazov-ru.json"
ARTIFACT_GIT_BLOB_SHA1 = "21cacd2d77575377b0d5e64d998cfd2687abc453"
REPLAY_HEAD_SHA = "ade9afa718967866530e58ec6cb9d731bf5b81a0"


def _same(actual: object, expected: object, field: str) -> None:
    if type(actual) is not type(expected) or actual != expected:
        raise ValueError("Brothers Karamazov retained evidence mismatch: " + field)


def verify(root: Path, witness: dict[str, object]) -> list[dict[str, object]]:
    """Return 29 strictly checked source-unmatched candidate/extension rows."""
    path = root / ARTIFACT_PATH
    if path.is_symlink():
        raise ValueError("Brothers Karamazov retained evidence symlink refused")
    raw = path.read_bytes()
    digest = sha1(b"blob " + str(len(raw)).encode("ascii") + bytes((0,)) + raw).hexdigest()
    if not 0 < len(raw) < 200_000 or digest != ARTIFACT_GIT_BLOB_SHA1:
        raise ValueError("Brothers Karamazov retained CI evidence blob drift")
    data = _load(root, ARTIFACT_PATH)
    if set(data) != {"body_identity", "candidate_id", "comparison_policy",
                     "diagnostic_version", "fantlab", "gates", "metric_rows",
                     "scriptorium", "source_text_committed"}:
        raise ValueError("Brothers Karamazov retained evidence shape drift")
    _same(data["candidate_id"], CANDIDATE_ID, "candidate")
    _same(data["source_text_committed"], False, "source safety")
    _same(data["diagnostic_version"], karamazov_diagnostic.DIAGNOSTIC_VERSION,
          "diagnostic version")
    _same(data["body_identity"], {
        "source_segment_count": karamazov_diagnostic.freeze.SOURCE_SEGMENT_COUNT,
        "character_count_including_spaces": witness["source"]["characters_including_spaces"],
        "raw_sha256": witness["source"]["raw_sha256"],
        "normalized_sha256": witness["source"]["normalized_sha256"],
    }, "frozen source identity")
    _same(data["body_identity"]["raw_sha256"], karamazov_diagnostic.FROZEN_BODY_SHA256,
          "canonical pinned body digest")
    _same(data["fantlab"], {
        "analysis_url": witness["fantlab"]["reference_url"],
        "analysis_date": witness["fantlab"]["analysis_date"],
        "public_display_references_retained": karamazov_diagnostic.FANTLAB_REFERENCES,
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
        raise ValueError("Brothers Karamazov retained metric ID inventory drift")
    rows: list[dict[str, object]] = []
    for record in records:
        if set(record) != {
            "metric_id", "actual", "unit", "compatibility_status",
            "fantlab_display", "actual_minus_fantlab_display", "result"
        }:
            raise ValueError("Brothers Karamazov metric row shape drift")
        metric_id = record["metric_id"]
        definition = metrics._METRIC_DEFINITIONS.get(metric_id)
        if definition is None:
            expected_unit, expected_status = "occurrences/1000_words", "inferred"
        else:
            expected_unit, _, expected_status = definition
        _same(record["unit"], expected_unit, "metric unit")
        _same(record["compatibility_status"], expected_status,
              "compatibility status")
        reference = karamazov_diagnostic.FANTLAB_REFERENCES.get(metric_id)
        _same(record["fantlab_display"], reference, "reference field")
        actual, delta = record["actual"], record["actual_minus_fantlab_display"]
        if metric_id in karamazov_diagnostic._UNBOUND:
            _same((actual, delta, record["result"]),
                  (None, None, "NOT_RUN_DICTIONARY_UNBOUND"),
                  "unbound dictionary state")
            status = "NOT_RUN"
        elif reference is not None:
            if (type(actual) is not int or type(delta) is not int
                    or delta != actual - int(reference)):
                raise ValueError("Brothers Karamazov integer reference delta drift")
            _same(record["result"], "DIAGNOSTIC_SOURCE_UNMATCHED",
                  "unmatched reference status")
            status = "UNRESOLVED_SOURCE"
        else:
            if type(actual) not in (int, float) or not math.isfinite(actual):
                raise ValueError("Brothers Karamazov invalid or missing numeric actual")
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
        raise ValueError("Brothers Karamazov verified field coverage drift")
    return rows
