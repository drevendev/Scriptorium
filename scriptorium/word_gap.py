"""Conditional word-density contrasts for frozen, source-unmatched FantLab evidence.

No text ingestion, POS guesswork, new metric profile, or parity inference.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, localcontext
import io
import json
from pathlib import Path

from .csv_safety import safe_csv_text

SCHEMA_VERSION = "scriptorium-word-density-diagnostic-v1"
_COUNT_METRICS = ("fantlab.general.characters", "fantlab.general.words")
_OUTPUT_KEYS = (
    "candidate_id", "status", "source_identity", "expected_characters",
    "actual_characters", "expected_words", "actual_words", "raw_character_gap",
    "raw_word_gap", "fantlab_words_per_1000_characters",
    "scriptorium_words_per_1000_characters", "density_gap_per_1000_characters",
    "length_adjusted_word_residual",
)


def build_word_density_diagnostic(report: dict[str, object]) -> dict[str, object]:
    """Separate word-count drift from a *hypothetical* scalar length difference.

    A source-length correction does not control for editions, tokenization or
    FantLab's unpublished methodology. The upstream matrix validates witnesses.
    """
    if report.get("m2_source_matched_pass_count") != 0:
        raise ValueError("word-density diagnostics require source-unmatched evidence")
    entries = report.get("entries")
    extra = report.get("supplemental_diagnostics")
    if not isinstance(entries, list) or not isinstance(extra, list):
        raise ValueError("missing retained work inventory")
    output = []
    for entry in [*entries, *extra]:
        if not isinstance(entry, dict) or entry.get("exact_fantlab_input_identity") != "UNKNOWN":
            raise ValueError("unexpected source identity")
        rows = entry.get("metric_rows")
        if not isinstance(rows, list):
            raise ValueError("missing retained metric rows")
        counts = {}
        available = True
        for key in _COUNT_METRICS:
            found = [r for r in rows if isinstance(r, dict) and r.get("metric_id") == key]
            if len(found) > 1:
                raise ValueError("duplicate retained count")
            if not found or found[0].get("expected") is None or found[0].get("actual") is None:
                available = False
                continue
            row = found[0]
            expected, actual = row["expected"], row["actual"]
            if type(expected) is not int or type(actual) is not int or min(expected, actual) < 0:
                raise ValueError("retained word/character counts must be nonnegative integers")
            if row.get("result") != "UNRESOLVED_SOURCE" or row.get("actual_minus_expected") != actual - expected:
                raise ValueError("invalid retained source-unmatched count delta")
            counts[key] = (expected, actual)
        result = {key: None for key in _OUTPUT_KEYS}
        result.update(candidate_id=entry["candidate_id"], status="DIAGNOSTIC_ONLY" if available else "NOT_RUN",
                      source_identity="UNKNOWN")
        if available:
            expected_chars, actual_chars = counts["fantlab.general.characters"]
            expected_words, actual_words = counts["fantlab.general.words"]
            if not expected_chars or not actual_chars:
                raise ValueError("word-density denominators must be positive")
            with localcontext() as context:
                context.prec = 50
                expected_density = Decimal(expected_words) * 1000 / expected_chars
                actual_density = Decimal(actual_words) * 1000 / actual_chars
                residual = Decimal(actual_words) - Decimal(expected_words) * actual_chars / expected_chars
                def six(value: Decimal) -> str:
                    return format(value.quantize(Decimal("0.000001")), ".6f")
                result.update(
                    expected_characters=expected_chars, actual_characters=actual_chars,
                    expected_words=expected_words, actual_words=actual_words,
                    raw_character_gap=actual_chars - expected_chars,
                    raw_word_gap=actual_words - expected_words,
                    fantlab_words_per_1000_characters=six(expected_density),
                    scriptorium_words_per_1000_characters=six(actual_density),
                    density_gap_per_1000_characters=six(actual_density - expected_density),
                    length_adjusted_word_residual=six(residual),
                )
        output.append(result)
    return {
        "schema_version": SCHEMA_VERSION,
        "m2_source_matched_pass_count": 0,
        "units": {
            "densities": "words / 1,000 characters including spaces",
            "length_adjusted_word_residual": "words; hypothetical proportional character scaling",
        },
        "note": (
            "Source-unmatched diagnostic only; density is not FantLab parity or proof of "
            "identical text. Length adjustment models proportional character scaling, "
            "not actual edition differences, segmentation errors, morphology or hidden "
            "FantLab coefficients."
        ),
        "entries": output,
    }


def render_word_density_diagnostic(report: dict[str, object], kind: str) -> str:
    if kind == "json":
        return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if kind == "csv":
        stream = io.StringIO(newline="")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(_OUTPUT_KEYS)
        for entry in report["entries"]:
            writer.writerow(
                "" if entry[key] is None else safe_csv_text(str(entry[key]))
                if key == "candidate_id" else entry[key] for key in _OUTPUT_KEYS
            )
        return stream.getvalue()
    if kind != "markdown":
        raise ValueError("invalid word-density report format")
    lines = [
        "# Scriptorium · conditional word-density diagnostic", "",
        "**M2: 0/5 — FantLab analyzer-input editions remain unmatched.**", "",
        report["note"], "",
        "Density = words per 1,000 **characters including spaces**; signed gap = Scriptorium minus FantLab.",
        "Hypothetical residual words = Scriptorium words − (FantLab words × Scriptorium characters / FantLab characters).",
        "This scalar correction is **not** an estimate of the real tokenization error.", "",
        "| Work | FantLab words / 1k chars | Scriptorium words / 1k chars | Signed density gap | Conditional residual words | Status |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for entry in report["entries"]:
        title = str(entry["title"]).replace("|", "\\|").replace("\n", " ")
        keys = ("fantlab_words_per_1000_characters", "scriptorium_words_per_1000_characters",
                "density_gap_per_1000_characters", "length_adjusted_word_residual")
        values = [str(entry[key]) if entry[key] is not None else "NOT_RUN" for key in keys]
        lines.append(f"| {title} | {' | '.join(values)} | {entry['status']} |")
    lines.extend(["", "UNKNOWN / NOT_RUN never means zero; no row is source-matched parity.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    from .benchmark_metric_matrix import build_metric_matrix

    parser = argparse.ArgumentParser(description="Normalize retained FantLab word-count gaps without asserting parity")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--format", choices=("markdown", "json", "csv"), default="markdown")
    parser.add_argument("--output", type=Path, help="Create a new report; never overwrite")
    args = parser.parse_args(argv)
    try:
        rendered = render_word_density_diagnostic(
            build_word_density_diagnostic(build_metric_matrix(args.root)), args.format
        )
        if args.output is None:
            print(rendered, end="")
        else:
            with args.output.open("x", encoding="utf-8", newline="") as destination:
                destination.write(rendered)
    except FileExistsError:
        parser.error("output already exists; choose another filename")
    except (OSError, UnicodeError, ValueError, TypeError, KeyError):
        parser.error("retained evidence invalid or destination unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
