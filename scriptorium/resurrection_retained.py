"""Verify the source-free, 129-revision Resurrection measurement before matrix use.

This is a sixth diagnostic outside the five-work source-readiness contract, not
a sixth source-matched FantLab parity candidate. The retained artifact is
pinned to its checked-in Git blob and original successful CI receipt.
"""
from __future__ import annotations

from hashlib import sha1
import math
from pathlib import Path

from . import metrics, resurrection_diagnostic as diagnostic
from .benchmark import _reference_specs
from .benchmark_readiness import _load

CANDIDATE_ID = "tolstoy-resurrection-ru"
ARTIFACT_PATH = "corpus/candidates/diagnostics/tolstoy-resurrection-ru.retained.json"
MANIFEST_PATH = "corpus/candidates/source-edition-traces/tolstoy-resurrection-ru.revisions.json"
ARTIFACT_GIT_BLOB_SHA1 = "0cc4d3d96fa3573ef7714ce3655a3120853fba16"
ORIGINAL_JSON_SHA256 = "c122b9c95273bb78064c66d4e58fd82beb5e95480f1b98c78c71f5fcf536eefe"
ORIGINAL_ZIP_SHA256 = "b74edf2ac8d721a4d65f59bd4eb0df8f84a443829664577368a28fbe4d6ad78b"
WORKFLOW_RUN = "https://github.com/drevendev/Scriptorium/actions/runs/40653324912"


def _same(actual: object, expected: object, field: str) -> None:
    if type(actual) is not type(expected) or actual != expected:
        raise ValueError("Resurrection retained evidence mismatch: " + field)


def verify(root: Path) -> list[dict[str, object]]:
    """Validate the frozen source, provenance and each of 29 diagnostic rows.

    Does not fetch or store the manuscript, infer unpublished FantLab values,
    or advance the five-work M2 parity gate.
    """
    path = root / ARTIFACT_PATH
    if path.is_symlink():
        raise ValueError("Resurrection retained evidence symlink refused")
    raw = path.read_bytes()
    git_blob = sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    if not 0 < len(raw) < 200_000 or git_blob != ARTIFACT_GIT_BLOB_SHA1:
        raise ValueError("Resurrection retained CI evidence blob drift")
    data = _load(root, ARTIFACT_PATH)
    if set(data) != {
        "candidate_id", "diagnostic_version", "source_text_committed",
        "source_manifest", "source_body_sha256", "body_identity", "scriptorium",
        "fantlab", "comparison_policy", "source_evidence", "gates", "metric_rows",
    }:
        raise ValueError("Resurrection retained evidence shape drift")
    _same(data["candidate_id"], CANDIDATE_ID, "candidate")
    _same(data["source_text_committed"], False, "source privacy")
    _same(data["diagnostic_version"], diagnostic.DIAGNOSTIC_VERSION, "diagnostic version")
    _same(data["source_manifest"], MANIFEST_PATH, "frozen revision manifest path")
    _same(data["source_body_sha256"], diagnostic.FROZEN_BODY_SHA256, "body digest")
    manifest = _load(root, MANIFEST_PATH)
    identities = diagnostic._pinned_manifest(manifest)
    _same(len(identities), diagnostic.FROZEN_CHAPTER_COUNT, "chapter count")
    _same(data["body_identity"], {
        "chapter_count": diagnostic.FROZEN_CHAPTER_COUNT,
        "character_count_including_spaces": diagnostic.FROZEN_BODY_CHARACTERS,
        "raw_sha256": diagnostic.FROZEN_BODY_SHA256,
        "normalized_sha256": diagnostic.FROZEN_BODY_SHA256,
    }, "frozen source identity")
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
    _same(data["fantlab"], {
        "analysis_url": diagnostic.FANTLAB_URL,
        "analysis_date": diagnostic.FANTLAB_DATE,
        "public_display_references_retained": diagnostic.FANTLAB_REFERENCES,
        "source_edition_disclosed": False,
        "source_bytes_disclosed": False,
    }, "dated unmatched FantLab reference")
    _same(data["comparison_policy"], {
        "class": "diagnostic_unmatched_source",
        "available_reference_fields": 2,
        "other_reference_fields": "NOT_RETAINED",
        "rounding_evidence": "UNKNOWN",
        "numeric_similarity_does_not_prove_source_identity": True,
    }, "scientific comparison policy")
    _same(data["source_evidence"], {
        "original_ci_artifact_json_sha256": ORIGINAL_JSON_SHA256,
        "original_ci_archive_sha256": ORIGINAL_ZIP_SHA256,
        "workflow_run": WORKFLOW_RUN,
    }, "original CI provenance")
    _same(data["gates"], {
        "calibration_size_met": True,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
        "m2_weight": 0,
    }, "unchanged M2 gate")

    records = data["metric_rows"]
    expected_ids = {metric_id for metric_id, *_ in _reference_specs()} | {
        "scriptorium.general.sentences"
    }
    if (not isinstance(records, list) or len(records) != 29
            or any(not isinstance(item, dict) for item in records)
            or [item.get("metric_id") for item in records] != sorted(expected_ids)):
        raise ValueError("Resurrection retained metric ID inventory drift")

    rows: list[dict[str, object]] = []
    for record in records:
        if set(record) != {
            "metric_id", "actual", "unit", "compatibility_status",
            "fantlab_display", "actual_minus_fantlab_display", "result",
        }:
            raise ValueError("Resurrection metric row shape drift")
        metric_id = record["metric_id"]
        definition = metrics._METRIC_DEFINITIONS.get(metric_id)
        expected_unit, expected_status = (
            (definition[0], definition[2]) if definition is not None
            else ("occurrences/1000_words", "inferred")
        )
        _same(record["unit"], expected_unit, "metric unit")
        _same(record["compatibility_status"], expected_status, "compatibility status")
        reference = diagnostic.FANTLAB_REFERENCES.get(metric_id)
        _same(record["fantlab_display"], reference, "reference field")
        actual, delta = record["actual"], record["actual_minus_fantlab_display"]
        if metric_id in diagnostic._UNBOUND:
            _same((actual, delta, record["result"]),
                  (None, None, "NOT_RUN_DICTIONARY_UNBOUND"), "unbound dictionary state")
            status = "NOT_RUN"
        elif reference is not None:
            if type(actual) is not int or type(delta) is not int or delta != actual - int(reference):
                raise ValueError("Resurrection integer reference delta drift")
            _same(record["result"], "DIAGNOSTIC_SOURCE_UNMATCHED",
                  "unmatched reference status")
            status = "UNRESOLVED_SOURCE"
        else:
            if type(actual) not in (int, float) or not math.isfinite(actual):
                raise ValueError("Resurrection invalid numeric actual")
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

    if (sum(row["actual"] is not None for row in rows) != 24
            or sum(row["actual"] is None for row in rows) != 5
            or sum(row["expected"] is not None for row in rows) != 2):
        raise ValueError("Resurrection verified metric coverage drift")
    _same(next(row["actual_minus_expected"] for row in rows
               if row["metric_id"] == "fantlab.general.characters"), 9591, "character delta")
    _same(next(row["actual_minus_expected"] for row in rows
               if row["metric_id"] == "fantlab.general.words"), 9672, "word delta")
    return rows
