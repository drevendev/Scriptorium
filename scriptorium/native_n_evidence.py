"""Offline, source-free CLI reports from retained pinned AOT/pylem N evidence.

This formats previous native measurements; it never lemmatizes prose or
recovers noun/cardinal labels from the collapsed runtime N tag.
"""
from __future__ import annotations

import argparse
import csv
from hashlib import sha1
from io import StringIO
import json
from pathlib import Path

from .analyze import LocalInputError, _read_bounded_regular_file, _write_new
from .csv_safety import safe_csv_text
from .frozen_diagnostic_report import _unique_keys
from .n_uncertainty_publication import validate_n_summary
from .native_n_units import normalized_n_bounds

SCHEMA = "scriptorium-native-n-cli-evidence-v2"
RETAINED_PATH = Path("assets/n-uncertainty-anna.json")
MAX_EVIDENCE_BYTES = 64 * 1024
# Exact reviewed git blob for the retained AOT/pylem witness; prevents plausible
# numerical edits from passing the schema validator as original native evidence.
RETAINED_GIT_BLOB_SHA1 = "876e85cd5eed0d2bbf92ee63caed467cb493b1ca"


def build_native_n_report(root: Path) -> dict[str, object]:
    """Validate exact retained, source-free native evidence before rendering."""
    raw = _read_bounded_regular_file(root / RETAINED_PATH, MAX_EVIDENCE_BYTES, "native N evidence")
    blob = b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    if sha1(blob).hexdigest() != RETAINED_GIT_BLOB_SHA1:
        raise ValueError("retained native N witness differs from reviewed Git blob")
    witness = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_keys)
    rates = validate_n_summary(witness)
    conditional_units = normalized_n_bounds(witness)
    return {
        "schema_version": SCHEMA,
        "status": "diagnostic_only",
        "m2_source_matched_progress": "0/5",
        "measurement": "retained_native_pylem_0.0.18_not_rerun",
        "rates": rates,
        "conditional_units": conditional_units,
        "witness": witness,
    }


def _markdown_cell(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def render_native_n_report(report: dict[str, object], kind: str) -> str:
    """Show native counts and separately conditional, not joint, N-only bounds."""
    if kind == "json":
        return json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    witness = report["witness"]
    counts = witness["counts"]
    evidence = witness["evidence"]
    rates = report["rates"]
    units = report["conditional_units"]
    if kind == "csv":
        stream = StringIO(newline="")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("category", "measure", "observed", "conditional_min", "conditional_max", "unit", "evidence_status", "candidate_id", "pylem_version", "runtime_analysis_sha256", "conditional_min_normalized", "conditional_max_normalized", "independent_edge_upper_raw", "independent_edge_upper_normalized", "normalized_unit"))

        def row(category: str, measure: str, observed: int | str = "",
                low: int | str = "", high: int | str = "", unit: str = "tokens",
                status: str = "OBSERVED_NATIVE", normalized_low: str = "",
                normalized_high: str = "", loose_raw: int | str = "",
                normalized_loose: str = "", normalized_unit: str = "") -> None:
            writer.writerow((
                safe_csv_text(category), safe_csv_text(measure), observed, low, high, unit,
                status, safe_csv_text(witness["work"]["candidate_id"]),
                evidence["pylem_version"], evidence["runtime_analysis_sha256"],
                normalized_low, normalized_high, loose_raw, normalized_loose, normalized_unit,
            ))

        for key in ("word_count", "sentence_count", "baseline_defined", "n_only",
                    "n_mixed_excluded", "conditional_defined"):
            row("count", key, counts[key],
                unit="sentences" if key == "sentence_count" else "word tokens",
                status="DERIVED_CONDITIONAL" if key == "conditional_defined" else "OBSERVED_NATIVE")
        row("rate", "n_only_percent_of_words", f"{rates['n_only_percent_of_words']:.6f}", unit="percent", status="DERIVED_NATIVE")
        row("rate", "conditional_noun_or_cardinal_percent_of_defined",
            f"{rates['conditional_noun_or_cardinal_percent_of_defined']:.6f}", unit="percent", status="DERIVED_CONDITIONAL")
        for bucket, bounds in witness["bucket_bounds"].items():
            scaled = units["bucket_percent_of_conditional_defined"][bucket]
            row("bucket", bucket, low=bounds[0], high=bounds[1],
                status="CONDITIONAL_N_ONLY",
                normalized_low=f"{scaled[0]:.6f}", normalized_high=f"{scaled[1]:.6f}",
                normalized_unit="percent_of_conditional_defined")
        for pair, scaled in zip(witness["bigram_bounds"], units["bigram_per_1000_word_tokens"]):
            row("bigram", pair["first"] + "->" + pair["second"],
                low=pair["min"], high=pair["max"], unit="adjacent pairs",
                status="CONDITIONAL_N_ONLY",
                normalized_low=f"{scaled['min']:.6f}", normalized_high=f"{scaled['max']:.6f}",
                loose_raw=pair["independent_edge_upper"],
                normalized_loose=f"{scaled['independent_edge_upper']:.6f}",
                normalized_unit="per_1000_word_tokens")
        for position, scaled in zip(
                witness["sentence_position_bounds"],
                units["sentence_position_percent_of_all_sentences"]):
            row("sentence_position", str(position["position"]),
                low=position["min"], high=position["max"], unit="sentences",
                status="CONDITIONAL_N_ONLY",
                normalized_low=f"{scaled['min']:.6f}", normalized_high=f"{scaled['max']:.6f}",
                normalized_unit="percent_of_all_sentences")
        for name, group in witness["native_controls"].items():
            row("native_control", name + "_n_only", group["n_only"],
                unit="of " + str(group["token_count"]) + " annotated examples")
        return stream.getvalue()
    if kind != "markdown":
        raise ValueError("invalid native N evidence format")
    lines = [
        "# Scriptorium · pinned AOT/pylem N ambiguity", "",
        f"**{_markdown_cell(witness['work']['title'])}** · retained native pylem=={evidence['pylem_version']} diagnostic, not a new analysis.", "",
        "**M2: 0/5.** FantLab analyzer-input identity and homonym selection remain unknown. Native N does not identify a noun or cardinal.", "",
        "| Observed native count | Value |", "| --- | ---: |",
    ]
    for key in ("word_count", "sentence_count", "baseline_defined", "n_only",
                "n_mixed_excluded", "conditional_defined"):
        lines.append(f"| {key} | {counts[key]} |")
    lines += ["", f"N-only tokens: **{rates['n_only_percent_of_words']:.2f}% of words**. N-mixed tokens stay excluded.", "",
              "## Conditional noun/cardinal envelopes", "",
              "Only N-only tokens are hypothetically assigned. Each cell is bounded separately; endpoints cannot be combined into one claimed analysis.",
              "Rates use word tokens / all sentences / conditionally defined tokens as explicitly labeled. Six decimals are presentation precision only, NOT FantLab rounding.", "",
              "| Bucket | Min tokens | Max tokens | Min % of conditionally defined | Max % |",
              "| --- | ---: | ---: | ---: | ---: |"]
    for bucket, (lo, hi) in witness["bucket_bounds"].items():
        scaled = units["bucket_percent_of_conditional_defined"][bucket]
        lines.append(f"| {bucket} | {lo} | {hi} | {scaled[0]:.6f} | {scaled[1]:.6f} |")
    lines += ["", "The achievable maximum respects linked adjacent token assignments; the independent-edge upper is a looser bound, not an observed or jointly attainable count.", "",
              "| Adjacent POS pair | Min | Max | Independent-edge upper | Min / 1,000 words | Max / 1,000 words | Independent-edge upper / 1,000 words |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for pair, scaled in zip(witness["bigram_bounds"], units["bigram_per_1000_word_tokens"]):
        lines.append(f"| {pair['first']} → {pair['second']} | {pair['min']} | {pair['max']} | {pair['independent_edge_upper']} | {scaled['min']:.6f} | {scaled['max']:.6f} | {scaled['independent_edge_upper']:.6f} |")
    lines += ["", "| Sentence position | Min | Max | Min % of all sentences | Max % |",
              "| ---: | ---: | ---: | ---: | ---: |"]
    for position, scaled in zip(witness["sentence_position_bounds"], units["sentence_position_percent_of_all_sentences"]):
        lines.append(f"| {position['position']} | {position['min']} | {position['max']} | {scaled['min']:.6f} | {scaled['max']:.6f} |")
    lines += ["", "## Pinned native controls", "",
              "These role labels annotate test examples, not inferred grammatical classes.", "",
              "| Annotation | N-only | Tested |", "| --- | ---: | ---: |"]
    for name, group in witness["native_controls"].items():
        lines.append(f"| {name} | {group['n_only']} | {group['token_count']} |")
    lines += ["", f"Native CI witness: {evidence['workflow_url']}",
              f"Pinned runtime-analysis SHA-256: {evidence['runtime_analysis_sha256']}", "",
              "**Diagnostic only:** no FantLab parity; no production POS remapping; no source text included.", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read pinned native AOT/pylem N-collision evidence without downloading text")
    parser.add_argument("--root", type=Path, default=Path("."),
                        help="Repository checkout containing assets/n-uncertainty-anna.json")
    parser.add_argument("--format", choices=("markdown", "json", "csv"), default="markdown")
    parser.add_argument("--output", type=Path, help="Create-only report path")
    args = parser.parse_args(argv)
    try:
        rendered = render_native_n_report(build_native_n_report(args.root), args.format)
        if args.output is None:
            print(rendered, end="")
        else:
            _write_new(args.output, rendered)
    except FileExistsError:
        parser.error("report output already exists; choose another destination")
    except (LocalInputError, OSError, UnicodeError, ValueError, TypeError, KeyError, RecursionError):
        parser.error("retained native N evidence invalid or destination unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
