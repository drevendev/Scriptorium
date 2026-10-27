"""Verified source-free inventory of retained cross-work FantLab metric diagnostics.

Readiness (five source witnesses) is validated first. Anna Karenina has 28 rows, Running on Waves 27, Silver Dove 29 and Brothers Karamazov 29.
The remaining two candidates lack metric artifacts and remain NOT_RUN. Unknown input identity never becomes parity.
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
from . import full_work_gallery, running_waves_diagnostic, silver_dove_retained, karamazov_retained
from .csv_safety import safe_csv_text

SCHEMA_VERSION = "scriptorium-fantlab-retained-metrics-v1"
REFERENCE = "benchmarks/fantlab/work270306.json"
DIAGNOSTIC = "benchmarks/fantlab/work270306-wikisource-diagnostic.json"
_ANNA_ID = "tolstoy-anna-karenina-ru"
_RUNNING_ID = "grin-running-on-waves-ru"
_RUNNING_DIAGNOSTIC = "corpus/candidates/diagnostics/grin-running-on-waves-ru.json"
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
    output_entries: list[dict[str, object]] = []
    for source in entries:
        is_anna = source["candidate_id"] == _ANNA_ID
        is_wave = source["candidate_id"] == _RUNNING_ID
        is_silver = source["candidate_id"] == silver_dove_retained.CANDIDATE_ID
        is_karamazov = source["candidate_id"] == karamazov_retained.CANDIDATE_ID
        rows = (observed if is_anna else wave_observed if is_wave else
                silver_observed if is_silver else karamazov_observed if is_karamazov else [])
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
                                           karamazov_retained.REPLAY_HEAD_SHA if is_karamazov else None),
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "source_readiness_schema": readiness["schema_version"],
        "works_reported": 5,
        "works_with_retained_metric_diagnostics": 4,
        "retained_metric_rows": len(observed) + len(wave_observed) + len(silver_observed) + len(karamazov_observed),
        "m2_source_matched_pass_count": 0,
        "note": "Retained observations are diagnostic or extension, NOT parity. One work has no field run; Silver Dove and Brothers Karamazov each have only two retained FantLab reference counts. Exact FantLab input identity and decimal rounding remain UNKNOWN.",
        "entries": output_entries,
    }


def render_metric_matrix(report: dict[str, object], kind: str) -> str:
    if kind == "json":
        return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"
    entries = report["entries"]
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
        "Unknown actual is not zero; displayed-rounding policy remains UNKNOWN.", "",
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
    lines.extend(["", "One work still lacks field observations. Silver Dove and Brothers Karamazov each have two displayed FantLab references; missing reference values are unknown, not zero.", ""])
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
