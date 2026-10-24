"""Verified source-free inventory of retained cross-work FantLab metric diagnostics.

Readiness (five source witnesses) is validated first. One retained Anna Karenina
diagnostic has 28 numeric-reference rows; four other candidates have no matching
metric artifact and remain NOT_RUN. Unknown input identity never becomes parity.
"""
from __future__ import annotations

import argparse
import csv
from io import StringIO
import json
import math
from pathlib import Path
import re

from .benchmark import _MISSING, _lookup, _reference_specs
from .benchmark_readiness import build_readiness, _load
from .csv_safety import safe_csv_text

SCHEMA_VERSION = "scriptorium-fantlab-retained-metrics-v1"
REFERENCE = "benchmarks/fantlab/work270306.json"
DIAGNOSTIC = "benchmarks/fantlab/work270306-wikisource-diagnostic.json"
_ANNA_ID = "tolstoy-anna-karenina-ru"
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
    output_entries: list[dict[str, object]] = []
    for source in entries:
        is_anna = source["candidate_id"] == _ANNA_ID
        rows = observed if is_anna else []
        output_entries.append({
            "candidate_id": source["candidate_id"],
            "title": source["title"],
            "author": source["author"],
            "source_witness_sha256": source["source"]["raw_sha256"],
            "reference_url": source["fantlab"]["reference_url"],
            "reference_date": source["fantlab"]["analysis_date"],
            "exact_fantlab_input_identity": "UNKNOWN",
            "metric_evidence": "RETAINED_DIAGNOSTIC" if is_anna else "NOT_RUN",
            "metric_rows": rows,
            "metric_rows_with_actual": sum(r["actual"] is not None for r in rows),
            "metric_rows_without_actual": sum(r["actual"] is None for r in rows),
            "retained_analyzer_revision": revision if is_anna else None,
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "source_readiness_schema": readiness["schema_version"],
        "works_reported": 5,
        "works_with_retained_metric_diagnostics": 1,
        "retained_metric_rows": len(observed),
        "m2_source_matched_pass_count": 0,
        "note": "All retained observations are diagnostic, NOT parity. Four works lack retained metric runs; decimal display rounding and exact FantLab input identity remain UNKNOWN.",
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
        "", "## Retained Anna Karenina diagnostic rows", "",
        "All numeric differences are **actual minus expected** on an unmatched public transcription.",
        "Unknown actual is not zero; displayed-rounding policy remains UNKNOWN.", "",
        "| Metric ID | FantLab expected | Scriptorium actual | Raw Δ | Status |",
        "| --- | ---: | ---: | ---: | --- |",
    ])
    for row in entries[0]["metric_rows"]:
        fmt = lambda n: "NOT_RUN" if n is None else str(n)
        lines.append(
            f"| {row['metric_id']} | {fmt(row['expected'])} | {fmt(row['actual'])} | "
            f"{fmt(row['actual_minus_expected'])} | {row['result']} |"
        )
    lines.extend(["", "Other four works have no retained metric observations and remain NOT_RUN.", ""])
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
