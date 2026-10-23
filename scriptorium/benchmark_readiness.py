"""Source-free, fail-closed readiness matrix for five frozen FantLab candidates.

This report compares *displayed character counts* as diagnostics, never as
edition identity or FantLab parity. All other metrics stay NOT_RUN until a
source-bound comparison artifact is supplied by the existing benchmark runner.
"""
from __future__ import annotations

import argparse
import csv
from io import StringIO
import json
from pathlib import Path
import re

from .csv_safety import safe_csv_text

SCHEMA_VERSION = "scriptorium-fantlab-readiness-v1"
CATALOG = "corpus/candidates/fantlab-parity-v1.json"
MINIMUM_CHARS = 300_000
# Frozen body witness paths are explicit; the older candidate index is known
# to lag the source-identity trace for Running on Waves.
_SPECS = (
    ("tolstoy-anna-karenina-ru", "public_transcription", "frozen_candidate"),
    ("dostoevsky-brothers-karamazov-ru", "public_transcription", "frozen_candidate"),
    ("bely-silver-dove-ru", "public_transcription", "frozen_candidate"),
    ("tolstoy-hyperboloid-garin-wikisource-ru", "public_source", "frozen_candidate"),
    ("grin-running-on-waves-ru", "composite_identity", ""),
)
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


def _pairs_unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def _load(root: Path, relative: str) -> dict[str, object]:
    if relative.startswith("/") or ".." in Path(relative).parts:
        raise ValueError("unsafe evidence path")
    data = json.loads((root / relative).read_text(encoding="utf-8"), object_pairs_hook=_pairs_unique)
    if not isinstance(data, dict):
        raise ValueError(f"invalid evidence object: {relative}")
    return data


def _get(data: dict[str, object], *keys: str) -> object:
    value: object = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            raise ValueError(f"missing evidence field: {'.'.join(keys)}")
        value = value[key]
    return value


def _positive_int(value: object, field: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"invalid positive integer: {field}")
    return value


def _sha(value: object) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ValueError("missing or invalid frozen SHA-256")
    return value


def _same(actual: object, expected: object, field: str) -> None:
    if type(actual) is not type(expected) or actual != expected:
        raise ValueError(f"conflicting evidence for {field}")


def build_readiness(root: Path) -> dict[str, object]:
    """Join current frozen witnesses to the retained catalog without upgrading parity.

    Raises ValueError on missing/conflicting source, rights, reference or digest
    evidence rather than manufacturing a partial success/unknown-as-zero row.
    """
    catalog = _load(root, CATALOG)
    _same(_get(catalog, "catalog_version"), "fantlab-parity-candidates-v1", "catalog version")
    _same(_get(catalog, "minimum_characters_including_spaces"), MINIMUM_CHARS, "minimum length")
    candidates = _get(catalog, "candidates")
    if not isinstance(candidates, list):
        raise ValueError("invalid candidate index")
    indexed: dict[str, dict[str, object]] = {}
    for candidate in candidates:
        if not isinstance(candidate, dict) or not isinstance(candidate.get("candidate_id"), str):
            raise ValueError("invalid candidate record")
        key = candidate["candidate_id"]
        if key in indexed:
            raise ValueError("duplicate candidate ID")
        indexed[key] = candidate

    entries: list[dict[str, object]] = []
    for identifier, namespace, field in _SPECS:
        if identifier not in indexed:
            raise ValueError(f"required candidate missing: {identifier}")
        c = indexed[identifier]
        trace_path = f"corpus/candidates/source-edition-traces/{identifier}.json"
        _same(_get(c, "source_edition_trace"), trace_path, "trace path")
        trace = _load(root, trace_path)
        _same(_get(trace, "candidate_id"), identifier, "trace candidate")
        fantlab = _get(c, "fantlab")
        if not isinstance(fantlab, dict):
            raise ValueError("invalid FantLab reference")
        work_id = _positive_int(_get(fantlab, "work_id"), "FantLab work ID")
        ref_url = f"https://fantlab.ru/work{work_id}/lp"
        _same(_get(fantlab, "analysis_url"), ref_url, "FantLab URL")
        date = _get(fantlab, "analysis_date")
        if not isinstance(date, str) or not _DATE.fullmatch(date):
            raise ValueError("invalid reference date")
        expected = _positive_int(_get(fantlab, "characters"), "FantLab displayed chars")
        _same(_get(trace, "fantlab", "work_id"), work_id, "trace FantLab ID")
        _same(_get(trace, "fantlab", "analysis_url"), ref_url, "trace FantLab URL")
        _same(_get(trace, "fantlab", "analysis_date"), date, "trace reference date")
        _same(_get(trace, "fantlab", "observed_counts", "characters"), expected, "trace reference count")
        _same(_get(c, "fantlab_source_edition_match"), "unknown", "catalog source match")
        _same(_get(trace, "admissibility", "fantlab_source_edition_match"), "unknown", "trace source match")
        _same(_get(trace, "admissibility", "m2_parity_admissible"), False, "parity gate")
        _same(_get(c, "gate_ready"), False, "candidate parity gate")
        source = _get(c, "source")
        if not isinstance(source, dict):
            raise ValueError("source provenance missing")
        _same(_get(source, "legal_basis"), "public_domain", "legal basis")
        legal_evidence = _get(source, "legal_evidence")
        if not isinstance(legal_evidence, str) or not legal_evidence.strip():
            raise ValueError("missing rights evidence")
        source_url = _get(source, "url")
        if not isinstance(source_url, str) or not source_url.startswith("https://ru.wikisource.org/wiki/"):
            raise ValueError("invalid source URL")

        witness_path = trace_path
        if field:
            witness = _get(trace, namespace, field)
        else:
            witness_path = f"corpus/candidates/source-edition-traces/{identifier}.literary-body.json"
            body = _load(root, witness_path)
            _same(_get(body, "candidate_id"), identifier, "body candidate")
            _same(_get(body, "composition", "source_text_committed"), False, "source text storage")
            _same(_get(body, "corpus_admission", "fantlab_source_edition_match"), "unknown", "body match")
            witness = _get(body, namespace)
        if not isinstance(witness, dict):
            raise ValueError("frozen body witness missing")
        if field:
            if witness.get("status") not in {"frozen", "frozen_public_candidate"}:
                raise ValueError("source witness is not frozen")
            _same(_get(witness, "source_text_committed"), False, "source text storage")
        count = _positive_int(_get(witness, "character_count_including_spaces"), "frozen characters")
        if count < MINIMUM_CHARS:
            raise ValueError("frozen candidate below 300,000 characters")
        raw_hash = _sha(_get(witness, "raw_sha256"))
        normalized_hash = _sha(_get(witness, "normalized_sha256"))
        if not field:
            # This newer body witness must agree with an independent trace
            # record, not only its own internally consistent hash fields.
            _same(_get(trace, "primary_public_transcription", "literary_body_witness", "raw_sha256"), raw_hash, "running body trace raw digest")
            _same(_get(trace, "primary_public_transcription", "literary_body_witness", "normalized_sha256"), normalized_hash, "running body trace normalized digest")
            _same(_get(trace, "primary_public_transcription", "literary_body_witness", "character_count_including_spaces"), count, "running body trace length")
            _same(_get(trace, "admissibility", "frozen_public_minus_fantlab_character_delta"), count - expected, "running body trace count delta")
        _positive_int(_get(witness, "utf8_byte_count"), "frozen bytes")
        _same(_get(witness, "normalization_profile"), "scriptorium-text-v1", "normalization profile")
        if "frozen_candidate_characters" in c:
            _same(c["frozen_candidate_characters"], count, "candidate body length")
        if "frozen_candidate_sha256" in c:
            _same(c["frozen_candidate_sha256"], raw_hash, "candidate body digest")
        if identifier == "tolstoy-anna-karenina-ru":
            reference = _load(root, "benchmarks/fantlab/work270306.json")
            _same(_get(reference, "reference", "work_id"), work_id, "reference file ID")
            _same(_get(reference, "reference", "url"), ref_url, "reference file URL")
            _same(_get(reference, "reference", "analysis_date"), date, "reference file date")
            _same(_get(reference, "expected", "characters"), expected, "reference file count")
            _same(_get(reference, "source_text", "raw_sha256"), raw_hash, "reference input digest")
        edition = source.get("edition_note")
        if not isinstance(edition, str) or not edition.strip():
            edition = None
        entries.append({
            "candidate_id": identifier,
            "title": _get(c, "title"),
            "author": _get(c, "author"),
            "work_identity": _get(c, "work_identity"),
            "translator": None,
            "source": {
                "url": source_url,
                "edition": edition,
                "legal_basis": "public_domain",
                "legal_evidence": legal_evidence,
                "witness_path": witness_path,
                "characters_including_spaces": count,
                "raw_sha256": raw_hash,
                "normalized_sha256": normalized_hash,
                "normalization_profile": "scriptorium-text-v1",
                "catalog_source_status": c.get("source_identity_status", "unknown"),
            },
            "fantlab": {"work_id": work_id, "reference_url": ref_url, "analysis_date": date},
            "exact_fantlab_input_identity": "UNKNOWN",
            "parity_eligible": False,
            "character_count_diagnostic": {
                "expected_displayed": expected,
                "actual_frozen_body": count,
                "actual_minus_expected": count - expected,
                "result": "UNRESOLVED_SOURCE",
                "rule": "displayed-character-count-diagnostic-only",
            },
            "other_metric_comparisons": "NOT_RUN",
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "catalog_path": CATALOG,
        "minimum_characters_including_spaces": MINIMUM_CHARS,
        "works_reported": len(entries),
        "m2_source_matched_pass_count": 0,
        "note": "Character-count deltas are DIAGNOSTIC, not FantLab parity. No source-matched input or full field-by-field comparison has passed.",
        "entries": entries,
    }


def render_report(report: dict[str, object], kind: str) -> str:
    if kind == "json":
        return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    entries = report["entries"]
    if kind == "csv":
        stream = StringIO(newline="")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("candidate_id", "title", "author", "edition", "legal_basis", "source_url", "witness_path", "raw_sha256", "reference_url", "reference_date", "expected_characters", "actual_characters", "delta_characters", "exact_input_identity", "parity_eligible", "other_metrics"))
        for e in entries:
            src, fl, diag = e["source"], e["fantlab"], e["character_count_diagnostic"]
            writer.writerow((safe_csv_text(e["candidate_id"]), safe_csv_text(e["title"]), safe_csv_text(e["author"]), safe_csv_text(src["edition"] or "UNKNOWN"), src["legal_basis"], safe_csv_text(src["url"]), safe_csv_text(src["witness_path"]), src["raw_sha256"], fl["reference_url"], fl["analysis_date"], diag["expected_displayed"], diag["actual_frozen_body"], diag["actual_minus_expected"], "UNKNOWN", "false", "NOT_RUN"))
        return stream.getvalue()
    if kind != "markdown":
        raise ValueError("invalid report format")
    lines = ["# Scriptorium · FantLab benchmark readiness", "", "**M2: 0/5 source-matched works.** Five frozen public candidates are shown below; no listed candidate has an independently established FantLab analyzer-input identity.", "", "| Work | Frozen characters | FantLab displayed | Δ characters | Input match |", "| --- | ---: | ---: | ---: | --- |"]
    for e in entries:
        d = e["character_count_diagnostic"]
        title = str(e["title"]).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {title} | {d['actual_frozen_body']:,} | {d['expected_displayed']:,} | {d['actual_minus_expected']:+,} | UNKNOWN |")
    lines += ["", "All character-count differences are **diagnostic only**, not exact parity comparisons. Other metric comparisons: **NOT_RUN**, not zero or PASS.", "", "Source rights, edition labels, frozen body hashes and dated reference URLs are retained in the JSON/CSV versions. This report contains no source prose. Refer to docs/BENCHMARKING.md for the per-metric comparison contract and its unresolved displayed-rounding semantics.", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Source-free five-work FantLab readiness and character diagnostic report")
    parser.add_argument("--root", type=Path, default=Path("."), help="Scriptorium repository root")
    parser.add_argument("--format", choices=("markdown", "json", "csv"), default="markdown")
    parser.add_argument("--output", type=Path, help="Create a new output file; never overwrite")
    args = parser.parse_args(argv)
    try:
        output = render_report(build_readiness(args.root), args.format)
        if args.output is None:
            print(output, end="")
        else:
            with args.output.open("x", encoding="utf-8", newline="") as stream:
                stream.write(output)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        parser.error(f"readiness evidence invalid or output unavailable: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
