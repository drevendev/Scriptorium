"""Verified source-free inventory of retained cross-work FantLab metric diagnostics.

Readiness (five source witnesses) is validated first. Anna Karenina has 28 rows, Running on Waves 27, Silver Dove 29 and Brothers Karamazov 29.
The remaining original candidate has no field run. Resurrection is separately verified
as a sixth source-unmatched diagnostic, never an addition to the five-work M2 gate.
"""
from __future__ import annotations

import argparse
import csv
from io import StringIO
from decimal import Decimal
from hashlib import sha1
import json
import math
from pathlib import Path
import re

from .benchmark import _MISSING, _lookup, _reference_specs
from .benchmark_readiness import build_readiness, _load
from . import full_work_gallery, running_waves_diagnostic, silver_dove_retained, karamazov_retained, resurrection_retained, hyperboloid_diagnostic
from .csv_safety import safe_csv_text

SCHEMA_VERSION = "scriptorium-fantlab-retained-metrics-v1"
REFERENCE = "benchmarks/fantlab/work270306.json"
DIAGNOSTIC = "benchmarks/fantlab/work270306-wikisource-diagnostic.json"
_ANNA_ID = "tolstoy-anna-karenina-ru"
_RUNNING_ID = "grin-running-on-waves-ru"
_RUNNING_DIAGNOSTIC = "corpus/candidates/diagnostics/grin-running-on-waves-ru.json"
_HYPER_ID = "tolstoy-hyperboloid-garin-wikisource-ru"
_HYPER_ARTIFACT = "corpus/candidates/diagnostics/tolstoy-hyperboloid-garin-wikisource-ru.retained.json"
_HYPER_GIT_BLOB_SHA1 = "c1278e87b08b6668073ef732f4841bf96d06cfe0"
_HYPER_CI_HEAD = "1b6f3867e407806102d4acd8758c5b2df4c89229"
_HYPER_CI_JSON_SHA256 = "95245fd09caea8b9150a6e7c1215c6f3c52fbaa54aa83d898a81a247192cf56d"
_HYPER_CI_ZIP_SHA256 = "4b5eca834a343cbe2c8bfa167942972ad652a1b64c25a97430a17dcf07ec698c"
_SHA = re.compile(r"[0-9a-f]{64}\Z")


def _same(actual: object, expected: object, field: str) -> None:
    if type(actual) is not type(expected) or actual != expected:
        raise ValueError(f"conflicting retained evidence for {field}")


def _number(value: object, field: str) -> int | float:
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"invalid numeric metric evidence: {field}")
    return value


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"missing retained evidence: {field}")
    return value


def _verify_metrics(reference: dict[str, object], diagnostic: dict[str, object]) -> list[dict[str, object]]:
    observed = diagnostic.get("metrics")
    if not isinstance(observed, dict):
        raise ValueError("retained diagnostic metrics missing")
    expected_section = reference.get("expected")
    if not isinstance(expected_section, dict):
        raise ValueError("retained reference metrics missing")

    specs = {
        metric_id: path for metric_id, path, _, _ in _reference_specs()
        if _lookup(expected_section, path) is not _MISSING
    }
    if set(observed) != set(specs):
        raise ValueError("retained metric IDs disagree with benchmark reference surface")

    rows: list[dict[str, object]] = []
    for metric_id in sorted(specs):
        item = observed[metric_id]
        if not isinstance(item, dict) or set(item) != {"expected", "actual", "raw_delta", "result"}:
            raise ValueError(f"invalid retained metric row: {metric_id}")
        expected = _number(_lookup(expected_section, specs[metric_id]), metric_id)
        _same(_number(item["expected"], metric_id), expected, f"{metric_id} expected")
        actual = item["actual"]
        delta = item["raw_delta"]
        result = item["result"]
        if actual is None:
            if delta is not None or result not in ("not_run", "unresolved"):
                raise ValueError(f"invalid unknown metric state: {metric_id}")
            state = "NOT_RUN" if result == "not_run" else "UNRESOLVED_NO_ACTUAL"
        else:
            numeric_actual = _number(actual, f"{metric_id} actual")
            numeric_delta = _number(delta, f"{metric_id} delta")
            if result != "unresolved":
                raise ValueError(f"source-unmatched metric may not pass/fail: {metric_id}")
            if type(expected) is int and type(numeric_actual) is int:
                if type(numeric_delta) is not int or numeric_delta != numeric_actual - expected:
                    raise ValueError(f"incorrect integer metric delta: {metric_id}")
            elif numeric_delta != numeric_actual - expected:
                # The retained artifact records Python's original float subtraction.
                # Approximate equality would accept altered diagnostic evidence.
                raise ValueError(f"incorrect floating metric delta: {metric_id}")
            state = "UNRESOLVED_SOURCE"
        rows.append({
            "metric_id": metric_id,
            "expected": expected,
            "actual": actual,
            "actual_minus_expected": delta,
            "result": state,
            "comparison_kind": "DIAGNOSTIC_ONLY",
            "display_rounding_evidence": "UNKNOWN",
        })
    return rows



def _verify_running_metrics(root: Path, witness: dict[str, object]) -> list[dict[str, object]]:
    """Use only already-frozen Grin diagnostics, never fresh or unpublished prose.

    The source-free record is blob-pinned by the existing full-work gallery.
    Count resemblance, matching labels and displayed decimals are not parity.
    """
    path = root / _RUNNING_DIAGNOSTIC
    if path.is_symlink():
        raise ValueError("unsafe Running on Waves evidence symlink")
    raw = path.read_bytes()
    expected_blob = full_work_gallery.SOURCES[0]
    _same(expected_blob[0], _RUNNING_ID, "Running on Waves gallery candidate")
    digest = sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    if not 0 < len(raw) < 2_000_000 or digest != expected_blob[1]:
        raise ValueError("Running on Waves retained evidence blob drift")
    data = _load(root, _RUNNING_DIAGNOSTIC)
    if set(data) != {"diagnostic_version", "candidate_id", "source_text_committed",
                     "body_identity", "scriptorium", "fantlab", "comparison_policy",
                     "metrics", "gates"}:
        raise ValueError("Running on Waves diagnostic object keys drift")
    _same(data["diagnostic_version"], running_waves_diagnostic.DIAGNOSTIC_VERSION,
          "Running on Waves diagnostic version")
    _same(data["candidate_id"], _RUNNING_ID, "Running on Waves candidate")
    _same(data["source_text_committed"], False, "Running on Waves source privacy")
    body = data["body_identity"]
    if not isinstance(body, dict):
        raise ValueError("Running on Waves body identity missing")
    _same(body.get("raw_sha256"), witness["source"]["raw_sha256"], "Running on Waves raw witness")
    _same(body.get("character_count_including_spaces"),
          witness["source"]["characters_including_spaces"], "Running on Waves characters")
    _same(body.get("manifest_version"), "scriptorium-running-waves-literary-body-v1",
          "Running on Waves body profile")
    provider = data["scriptorium"]
    if not isinstance(provider, dict):
        raise ValueError("Running on Waves measurement provenance missing")
    _same(provider.get("schema_version"), "scriptorium-deterministic-metrics-v4",
          "Running on Waves metric schema")
    _same(provider.get("metric_contract_id"), "fantlab-2022-v1",
          "Running on Waves metric contract")
    _same(provider.get("vocabulary_dictionary_dependency"), None,
          "Running on Waves dictionary dependency")
    _same(provider.get("profiles"), {
        "normalization": "scriptorium-text-v1",
        "metrics": "scriptorium-metrics-v4",
        "dialogue": "scriptorium-dialogue-v1",
        "vocabulary": "scriptorium-vocabulary-v1",
        "punctuation": "scriptorium-punctuation-v2",
    }, "Running on Waves metric profiles")
    reference = data["fantlab"]
    if not isinstance(reference, dict):
        raise ValueError("Running on Waves dated reference missing")
    _same(reference, {
        "work_id": witness["fantlab"]["work_id"],
        "analysis_url": witness["fantlab"]["reference_url"],
        "analysis_date": witness["fantlab"]["analysis_date"],
        "source_edition_disclosed": False,
        "source_bytes_disclosed": False,
    }, "Running on Waves unmatched FantLab reference")
    _same(data["comparison_policy"], {
        "class": "diagnostic_unmatched_source",
        "displayed_reference_is_not_exact_parity_tolerance": True,
        "decimal_display_precision_not_promoted_to_parity_rule": True,
        "numeric_resemblance_cannot_establish_source_identity": True,
    }, "Running on Waves scientific comparison policy")
    _same(data["gates"], {
        "general_calibration_profile_admissible": True,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": True,
        "gate_ready": False,
        "m2_parity_admissible": False,
        "m2_weight": 0,
    }, "Running on Waves M2 and source gates")

    records = data["metrics"]
    expected = running_waves_diagnostic.FANTLAB_REFERENCES
    if not isinstance(records, list) or len(records) != len(expected):
        raise ValueError("Running on Waves retained metric inventory drift")
    rows: list[dict[str, object]] = []
    for record, (metric_id, lexeme, dictionary_dependent) in zip(records, expected):
        if not isinstance(record, dict) or set(record) != {
            "metric_id", "fantlab_display_value", "scriptorium_raw_value",
            "delta_against_fantlab_display", "status",
        }:
            raise ValueError("Running on Waves retained metric row shape drift")
        _same(record["metric_id"], metric_id, "Running on Waves metric ID")
        _same(record["fantlab_display_value"], lexeme,
              "Running on Waves dated displayed reference")
        actual = record["scriptorium_raw_value"]
        raw_delta = record["delta_against_fantlab_display"]
        numeric_expected = int(lexeme) if "." not in lexeme else float(lexeme)
        if dictionary_dependent:
            if (actual is not None or raw_delta is not None
                    or record["status"] != "not_run_dependency_unbound"):
                raise ValueError("Running on Waves unknown dictionary actual was promoted")
            result, delta = "NOT_RUN", None
        else:
            if record["status"] != "diagnostic_only_source_unmatched":
                raise ValueError("Running on Waves diagnostic status was promoted")
            _number(actual, f"{metric_id} actual")
            if type(actual) is int and "." not in lexeme:
                if type(raw_delta) is not int or raw_delta != actual - numeric_expected:
                    raise ValueError("Running on Waves integer metric delta drift")
                delta = raw_delta
            else:
                if (not isinstance(raw_delta, str)
                        or Decimal(raw_delta) != Decimal(str(actual)) - Decimal(lexeme)):
                    raise ValueError("Running on Waves decimal metric delta drift")
                delta = float(raw_delta)
            result = "UNRESOLVED_SOURCE"
        rows.append({
            "metric_id": metric_id,
            "expected": numeric_expected,
            "actual": actual,
            "actual_minus_expected": delta,
            "result": result,
            "comparison_kind": "DIAGNOSTIC_ONLY",
            "display_rounding_evidence": "UNKNOWN",
        })
    if len(rows) != 27 or sum(row["actual"] is not None for row in rows) != 23:
        raise ValueError("Running on Waves verified measurement coverage drift")
    return rows



def _verify_hyperboloid_metrics(root: Path, witness: dict[str, object]) -> list[dict[str, object]]:
    """Reuse pinned Hyperboloid CI results as diagnostics, not parity evidence."""
    path = root
    for part in Path(_HYPER_ARTIFACT).parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("unsafe Hyperboloid retained evidence symlink")
    raw = path.read_bytes()
    digest = sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    if not 0 < len(raw) < 100_000 or digest != _HYPER_GIT_BLOB_SHA1:
        raise ValueError("Hyperboloid retained CI evidence blob drift")
    record = _load(root, _HYPER_ARTIFACT)
    header = {
        "schema_version": "scriptorium-hyperboloid-retained-ci-v1",
        "candidate_id": _HYPER_ID,
        "source_text_committed": False,
        "ci_run_id": 40469834658,
        "ci_head": _HYPER_CI_HEAD,
        "original_ci_artifact_json_sha256": _HYPER_CI_JSON_SHA256,
        "original_ci_archive_sha256": _HYPER_CI_ZIP_SHA256,
        "source_revision_id": 5014458,
        "source_body_characters": hyperboloid_diagnostic.FROZEN_BODY_CHARACTERS,
        "source_body_sha256": hyperboloid_diagnostic.FROZEN_BODY_SHA256,
        "source_input_identity_with_fantlab": "unknown",
        "m2_parity_admissible": False,
        "schema_profile": "scriptorium-deterministic-metrics-v4",
    }
    if set(record) != set(header) | {"metric_rows"}:
        raise ValueError("Hyperboloid retained CI evidence shape drift")
    for key, expected in header.items():
        _same(record[key], expected, "Hyperboloid " + key)

    traces = "corpus/candidates/source-edition-traces/" + _HYPER_ID
    hyperboloid_diagnostic._validate_pins(
        _load(root, traces + ".revision.json"),
        _load(root, traces + ".body.json"),
    )
    _same(witness["candidate_id"], _HYPER_ID, "Hyperboloid readiness identity")
    _same(witness["source"]["characters_including_spaces"],
          record["source_body_characters"], "Hyperboloid frozen count")
    _same(witness["source"]["raw_sha256"],
          record["source_body_sha256"], "Hyperboloid raw source SHA")
    _same(witness["source"]["normalized_sha256"],
          record["source_body_sha256"], "Hyperboloid normalized source SHA")
    _same(witness["fantlab"]["reference_url"],
          hyperboloid_diagnostic.FANTLAB_URL, "Hyperboloid FantLab URL")
    _same(witness["fantlab"]["analysis_date"],
          hyperboloid_diagnostic.FANTLAB_DATE, "Hyperboloid FantLab date")
    _same(witness["exact_fantlab_input_identity"], "UNKNOWN",
          "Hyperboloid input identity")
    _same(witness["parity_eligible"], False, "Hyperboloid M2 gate")

    records = record["metric_rows"]
    expected_ids = {metric_id for metric_id, *_ in _reference_specs()} | {
        "scriptorium.general.sentences"
    }
    if (type(records) is not list or len(records) != 29
            or any(type(row) is not dict for row in records)
            or [row.get("id") for row in records] != sorted(expected_ids)):
        raise ValueError("Hyperboloid retained metric ID inventory drift")
    rows = []
    for item in records:
        if set(item) != {"id", "actual", "reference", "status", "kind"}:
            raise ValueError("Hyperboloid retained metric row shape drift")
        metric_id = item["id"]
        extension = metric_id == "scriptorium.general.sentences"
        _same(item["kind"], "extension" if extension else "candidate",
              "Hyperboloid metric classification")
        reference = hyperboloid_diagnostic.FANTLAB_REFERENCES.get(metric_id)
        _same(item["reference"], int(reference) if reference is not None else None,
              "Hyperboloid displayed reference")
        actual = item["actual"]
        if metric_id in hyperboloid_diagnostic._UNBOUND:
            _same((actual, item["status"]), (None, "not_run"),
                  "Hyperboloid dictionary dependency")
            state = "NOT_RUN"
        else:
            if item["status"] != "measured" or type(actual) not in (int, float):
                raise ValueError("Hyperboloid missing or fabricated measurement")
            _number(actual, "Hyperboloid " + metric_id)
            if actual < 0:
                raise ValueError("Hyperboloid negative metric actual")
            if metric_id in {"fantlab.general.characters",
                             "fantlab.general.words",
                             "scriptorium.general.sentences"} and type(actual) is not int:
                raise ValueError("Hyperboloid integer metric changed")
            state = "UNRESOLVED_SOURCE" if reference is not None else "MEASURED_NO_REFERENCE"
        expected = int(reference) if reference is not None else None
        delta = actual - expected if expected is not None else None
        rows.append({
            "metric_id": metric_id,
            "expected": expected,
            "actual": actual,
            "actual_minus_expected": delta,
            "result": state,
            "comparison_kind": "EXTENSION_ONLY" if extension else "DIAGNOSTIC_ONLY",
            "display_rounding_evidence": "UNKNOWN",
        })
    if (sum(row["actual"] is not None for row in rows) != 24
            or sum(row["actual"] is None for row in rows) != 5
            or sum(row["expected"] is not None for row in rows) != 2):
        raise ValueError("Hyperboloid retained measurement coverage drift")
    values = {row["metric_id"]: row["actual"] for row in rows}
    _same(values["fantlab.general.characters"], 499066, "Hyperboloid character count")
    _same(values["fantlab.general.words"], 71921, "Hyperboloid word count")
    return rows


def build_metric_matrix(root: Path) -> dict[str, object]:
    """Join independently frozen corpus witnesses and retained metric observations.

    A retained artifact is not independent proof of the original manuscript
    bytes, FantLab's input edition, decimal rounding or any parity result.
    """
    readiness = build_readiness(root)
    entries = readiness["entries"]
    if len(entries) != 5 or {e["candidate_id"] for e in entries} != {
        "tolstoy-anna-karenina-ru", "dostoevsky-brothers-karamazov-ru",
        "bely-silver-dove-ru", "tolstoy-hyperboloid-garin-wikisource-ru",
        "grin-running-on-waves-ru",
    }:
        raise ValueError("five-work readiness inventory changed unexpectedly")

    anna = next(e for e in entries if e["candidate_id"] == _ANNA_ID)
    reference = _load(root, REFERENCE)
    diagnostic = _load(root, DIAGNOSTIC)
    _same(reference.get("benchmark_id"), diagnostic.get("benchmark_id"), "benchmark ID")
    _same(diagnostic.get("artifact_version"), "scriptorium-frozen-diagnostic-v1", "diagnostic schema")
    _same(diagnostic.get("candidate_id"), _ANNA_ID, "candidate ID")
    ref = reference.get("reference")
    evidence = diagnostic.get("evidence")
    epistemic = diagnostic.get("epistemic_status")
    if not isinstance(ref, dict) or not isinstance(evidence, dict) or not isinstance(epistemic, dict):
        raise ValueError("missing retained reference or provenance")
    _same(ref.get("url"), anna["fantlab"]["reference_url"], "FantLab reference URL")
    _same(ref.get("analysis_date"), anna["fantlab"]["analysis_date"], "FantLab reference date")
    _same(ref.get("work_id"), anna["fantlab"]["work_id"], "FantLab work ID")
    _same(evidence.get("reference_path"), REFERENCE, "reference binding")
    _same(evidence.get("raw_sha256"), anna["source"]["raw_sha256"], "raw frozen witness")
    _same(evidence.get("normalized_sha256"), anna["source"]["normalized_sha256"], "normalized frozen witness")
    _same(evidence.get("source_text_committed"), False, "source text committed")
    _same(evidence.get("source_text_uploaded"), False, "source text uploaded")
    _same(evidence.get("replay_integrity"), "passed", "retained replay status")
    revision = _text(evidence.get("scriptorium_revision"), "scriptorium revision")
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("invalid retained analyzer revision")
    _text(evidence.get("python_version"), "Python version")
    _same(epistemic.get("status"), "diagnostic_only", "scientific status")
    _same(epistemic.get("fantlab_source_edition_match"), "unknown", "source identity")
    _same(epistemic.get("m2_parity_admissible"), False, "parity admissibility")
    _same(epistemic.get("m2_source_matched_progress"), "0/5", "M2 source match")
    raw = evidence.get("raw_sha256")
    if not isinstance(raw, str) or not _SHA.fullmatch(raw):
        raise ValueError("invalid frozen digest")

    observed = _verify_metrics(reference, diagnostic)
    wave_witness = next(e for e in entries if e["candidate_id"] == _RUNNING_ID)
    wave_observed = _verify_running_metrics(root, wave_witness)
    silver_witness = next(e for e in entries if e["candidate_id"] == silver_dove_retained.CANDIDATE_ID)
    silver_observed = silver_dove_retained.verify(root, silver_witness)
    karamazov_witness = next(e for e in entries if e['candidate_id'] == karamazov_retained.CANDIDATE_ID)
    karamazov_observed = karamazov_retained.verify(root, karamazov_witness)
    hyperboloid_witness = next(e for e in entries if e["candidate_id"] == _HYPER_ID)
    hyperboloid_observed = _verify_hyperboloid_metrics(root, hyperboloid_witness)
    resurrection_observed = resurrection_retained.verify(root)
    output_entries: list[dict[str, object]] = []
    for source in entries:
        is_anna = source["candidate_id"] == _ANNA_ID
        is_wave = source["candidate_id"] == _RUNNING_ID
        is_silver = source["candidate_id"] == silver_dove_retained.CANDIDATE_ID
        is_karamazov = source["candidate_id"] == karamazov_retained.CANDIDATE_ID
        is_hyperboloid = source["candidate_id"] == _HYPER_ID
        rows = (observed if is_anna else wave_observed if is_wave else
                silver_observed if is_silver else karamazov_observed if is_karamazov else
                hyperboloid_observed if is_hyperboloid else [])
        output_entries.append({
            "candidate_id": source["candidate_id"],
            "title": source["title"],
            "author": source["author"],
            "source_witness_sha256": source["source"]["raw_sha256"],
            "reference_url": source["fantlab"]["reference_url"],
            "reference_date": source["fantlab"]["analysis_date"],
            "exact_fantlab_input_identity": "UNKNOWN",
            "metric_evidence": "RETAINED_DIAGNOSTIC" if rows else "NOT_RUN",
            "metric_rows": rows,
            "metric_rows_with_actual": sum(r["actual"] is not None for r in rows),
            "metric_rows_without_actual": sum(r["actual"] is None for r in rows),
            "retained_analyzer_revision": (revision if is_anna else
                                           silver_dove_retained.REPLAY_HEAD_SHA if is_silver else
                                           karamazov_retained.REPLAY_HEAD_SHA if is_karamazov else
                                           _HYPER_CI_HEAD if is_hyperboloid else None),
        })
    # The five independently validated readiness candidates and their M2
    # denominator remain unchanged. Resurrection is a sixth, supplemental
    # source-frozen DIAGNOSTIC, not another claimed matched FantLab input.
    supplemental = [{
        "candidate_id": resurrection_retained.CANDIDATE_ID,
        "title": "Воскресение",
        "author": "Лев Толстой",
        "source_witness_sha256": resurrection_retained.diagnostic.FROZEN_BODY_SHA256,
        "source_manifest": resurrection_retained.MANIFEST_PATH,
        "reference_url": resurrection_retained.diagnostic.FANTLAB_URL,
        "reference_date": resurrection_retained.diagnostic.FANTLAB_DATE,
        "exact_fantlab_input_identity": "UNKNOWN",
        "metric_evidence": "RETAINED_DIAGNOSTIC",
        "m2_candidate_scope": "SUPPLEMENTAL_NOT_SOURCE_MATCHED",
        "metric_rows": resurrection_observed,
        "metric_rows_with_actual": sum(r["actual"] is not None for r in resurrection_observed),
        "metric_rows_without_actual": sum(r["actual"] is None for r in resurrection_observed),
        "original_ci_artifact_sha256": resurrection_retained.ORIGINAL_JSON_SHA256,
        "retained_analyzer_revision": None,
    }]
    return {
        "schema_version": SCHEMA_VERSION,
        "source_readiness_schema": readiness["schema_version"],
        "works_reported": 5,
        "works_with_retained_metric_diagnostics": 5,
        "retained_metric_rows": len(observed) + len(wave_observed) + len(silver_observed) + len(karamazov_observed) + len(hyperboloid_observed) + len(resurrection_observed),
        "supplemental_retained_metric_rows": len(resurrection_observed),
        "m2_source_matched_pass_count": 0,
        "note": "Five core works retain the unchanged source-readiness/M2 denominator; Resurrection is supplemental source-unmatched evidence. All five core works have retained diagnostic field runs. Hyperboloid, Silver Dove, Brothers Karamazov and supplemental Resurrection each have only two retained FantLab reference counts. None establishes input identity or decimal rounding.",
        "entries": output_entries,
        "supplemental_diagnostics": supplemental,
    }


def render_metric_matrix(report: dict[str, object], kind: str) -> str:
    if kind == "json":
        return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"
    entries = report["entries"] + report["supplemental_diagnostics"]
    if kind == "csv":
        stream = StringIO(newline="")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("candidate_id", "title", "reference_url", "witness_sha256", "metric_id",
                         "expected", "actual", "delta", "status", "source_match", "rounding_evidence"))
        for entry in entries:
            for row in entry["metric_rows"] or [None]:
                writer.writerow((
                    safe_csv_text(entry["candidate_id"]), safe_csv_text(str(entry["title"])),
                    safe_csv_text(entry["reference_url"]), entry["source_witness_sha256"],
                    row["metric_id"] if row else "", row["expected"] if row else "",
                    row["actual"] if row and row["actual"] is not None else "",
                    row["actual_minus_expected"] if row and row["actual_minus_expected"] is not None else "",
                    row["result"] if row else "NOT_RUN", "UNKNOWN",
                    row["display_rounding_evidence"] if row else "UNKNOWN",
                ))
        return stream.getvalue()
    if kind != "markdown":
        raise ValueError("invalid report format")
    lines = [
        "# Scriptorium · retained FantLab metric diagnostics", "",
        "**M2: 0/5. No FantLab analyzer-input edition matches.** These rows never establish parity.", "",
        "| Work | Metrics recorded | With actual | Without actual | Input match |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for entry in entries:
        title = str(entry["title"]).replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {title} | {len(entry['metric_rows']) if entry['metric_rows'] else 'NOT_RUN'} | "
            f"{entry['metric_rows_with_actual'] if entry['metric_rows'] else 'NOT_RUN'} | "
            f"{entry['metric_rows_without_actual'] if entry['metric_rows'] else 'NOT_RUN'} | UNKNOWN |"
        )
    lines.extend([
        "", "## Retained source-unmatched diagnostic rows", "",
        "All numeric differences are **actual minus expected** on an unmatched public transcription.",
        "Unknown actual is not zero; displayed-rounding policy remains UNKNOWN.",
        "Resurrection is a sixth supplemental diagnostic, outside the fixed five-work M2 source-readiness set.", "",
        "| Metric ID | FantLab expected | Scriptorium actual | Raw Δ | Status |",
        "| --- | ---: | ---: | ---: | --- |",
    ])
    for entry in entries:
        if not entry["metric_rows"]:
            continue
        title = str(entry["title"]).replace("|", "\\|").replace("\n", " ")
        lines.extend(["", "### " + title, ""])
        for row in entry["metric_rows"]:
            fmt = lambda n: "NOT_RUN" if n is None else str(n)
            lines.append(
                f"| {row['metric_id']} | {fmt(row['expected'])} | {fmt(row['actual'])} | "
                f"{fmt(row['actual_minus_expected'])} | {row['result']} |"
            )
    lines.extend(["", "All five readiness works now have retained, source-unmatched field observations. Hyperboloid, Silver Dove, Brothers Karamazov and supplemental Resurrection each have only two displayed FantLab references; missing reference values are unknown, not zero. M2 remains 0/5.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and render source-free retained FantLab metric diagnostics")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--format", choices=("markdown", "json", "csv"), default="markdown")
    parser.add_argument("--output", type=Path, help="Create a report; never overwrite")
    args = parser.parse_args(argv)
    try:
        rendered = render_metric_matrix(build_metric_matrix(args.root), args.format)
        if args.output is None:
            print(rendered, end="")
        else:
            with args.output.open("x", encoding="utf-8", newline="") as destination:
                destination.write(rendered)
    except FileExistsError:
        parser.error("output already exists; choose a new filename")
    except (OSError, UnicodeError, ValueError, TypeError, KeyError):
        parser.error("retained metric evidence invalid or destination unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
