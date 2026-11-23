"""Replay four frozen AOT/pylem full-work N receipts without source prose.

This is a diagnostic of candidate coverage, not noun/cardinal disambiguation,
author-voice estimation, or a source-matched FantLab benchmark.
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
from .native_n_crosswork_cli import build_crosswork_report
from .native_n_evidence import MAX_EVIDENCE_BYTES

SCHEMA = "scriptorium-native-n-fourwork-offline-v1"
# These are Git *blob* identities of independently reviewed, source-free
# projections, not claims that the original prose or native run was recreated.
EXTRA_RECEIPTS = (
    ("grin", "assets/n-uncertainty-grin-summary.json",
     "5bbef782be505695a02244470ed72ffcc4958341",
     "grin-running-on-waves-ru", "Александр Грин"),
    ("road", "assets/n-uncertainty-road-summary.json",
     "c49a4b6abd6aa14017f5c620ff3f0a86aa4d298a",
     "grin-road-nowhere-ru", "Александр Грин"),
)
MEASURES = ("n_only", "n_mixed", "any_n")


def _derived_row(identity: dict, counts: dict) -> dict:
    word_count = counts["word_count"]
    if type(word_count) is not int or word_count <= 0:
        raise ValueError("invalid native denominator")
    numbers = {
        "n_only": counts["n_only"],
        "n_mixed": counts["n_mixed_excluded"],
        "any_n": counts["n_only"] + counts["n_mixed_excluded"],
    }
    if (any(type(v) is not int or v < 0 for v in numbers.values())
            or numbers["any_n"] > word_count):
        raise ValueError("invalid native N candidate counts")
    return {
        **identity,
        "word_tokens": word_count,
        "counts": numbers,
        "percent_of_word_tokens": {
            k: 100 * v / word_count for k, v in numbers.items()
        },
    }


def _extra_receipt(root: Path, specification: tuple) -> dict:
    short, path, expected_blob, candidate_id, author = specification
    raw = _read_bounded_regular_file(
        root / path, MAX_EVIDENCE_BYTES, "pinned source-free native N receipt"
    )
    git_blob = b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    if sha1(git_blob).hexdigest() != expected_blob:
        raise ValueError("reviewed native N evidence blob identity mismatch")
    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_keys)
    if (doc["status"] != "diagnostic_only"
            or doc["source_text_included"] is not False
            or doc["m2_parity_admissible"] is not False
            or doc["work"]["candidate_id"] != candidate_id
            or doc["work"]["author"] != author
            or doc["work"]["characters_including_spaces"] < 300000
            or doc["provider"]["version"] != "0.0.18"
            or doc["provider"]["runtime_profile"] != "pylem-0.0.18-python39-sidecar-v1"):
        raise ValueError("native provider, work or scientific boundary mismatch")
    evidence = doc["evidence"]
    return _derived_row({
        "key": short,
        "candidate_id": candidate_id,
        "title": doc["work"]["title"],
        "author": author,
        "normalized_sha256": evidence["normalized_sha256"],
        "runtime_analysis_sha256": evidence["runtime_analysis_sha256"],
        "native_workflow": "https://github.com/drevendev/Scriptorium/actions/runs/"
                           + str(evidence["run_id"]),
        "reviewed_projection_git_blob_sha1": expected_blob,
    }, doc["counts"])


def build_fourwork_report(root: Path) -> dict:
    """Require byte-identical Tolstoy and Grin projections before replay."""
    pair = build_crosswork_report(root)
    works = []
    for index, key in enumerate(("anna", "resurrection")):
        original = pair["works"][index]
        suffix = key
        counts = {row["measure_id"]: row[key + "_count"] for row in pair["rows"]}
        works.append(_derived_row({
            "key": suffix,
            "candidate_id": original["candidate_id"],
            "title": original["title"],
            "author": "Лев Толстой",
            "normalized_sha256": original["normalized_sha256"],
            "runtime_analysis_sha256": original["runtime_analysis_sha256"],
            "native_workflow": original["native_workflow"],
        }, {
            "word_count": original["word_tokens"],
            "n_only": counts["n_only"],
            "n_mixed_excluded": counts["n_mixed"],
        }))
        if counts["any_n"] != works[-1]["counts"]["any_n"]:
            raise ValueError("retained Tolstoy native N aggregate drift")
    for specification in EXTRA_RECEIPTS:
        works.append(_extra_receipt(root, specification))

    by_key = {item["key"]: item for item in works}
    if len(by_key) != 4:
        raise ValueError("duplicate native work identity")
    deltas = {}
    for label, first, second in (
        ("tolstoy_resurrection_minus_anna", "anna", "resurrection"),
        ("grin_road_minus_waves", "grin", "road"),
    ):
        deltas[label] = {
            k: by_key[second]["percent_of_word_tokens"][k]
               - by_key[first]["percent_of_word_tokens"][k]
            for k in MEASURES
        }
    return {
        "schema_version": SCHEMA,
        "status": "diagnostic_only",
        "source_text_included": False,
        "m2_parity_admissible": False,
        "provider": "pylem==0.0.18 (AOT-lineage, pinned legacy sidecar)",
        "measurement": "replay_of_four_accepted_fullwork_native_receipts_not_new_analysis",
        "works": works,
        "same_author_percentage_point_deltas": deltas,
        "interpretation": (
            "Each percentage divides by that edition's word-token count; "
            "mixed-N excludes N-only tokens. Within-author differences are "
            "descriptive, not noun/cardinal recovery, voice attribution or FantLab parity."
        ),
    }


def render_fourwork_report(report: dict, kind: str) -> str:
    if kind == "json":
        return json.dumps(report, indent=2, sort_keys=True,
                          ensure_ascii=False, allow_nan=False) + "\n"
    if kind == "csv":
        stream = StringIO(newline="")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow((
            "candidate_id", "title", "measure_id", "count", "word_tokens",
            "percent_of_word_tokens", "evidence_status", "normalized_sha256",
            "runtime_analysis_sha256", "native_workflow",
        ))
        for work in report["works"]:
            for measure in MEASURES:
                writer.writerow((
                    safe_csv_text(work["candidate_id"]), safe_csv_text(work["title"]),
                    measure, work["counts"][measure], work["word_tokens"],
                    f'{work["percent_of_word_tokens"][measure]:.6f}',
                    "diagnostic_only", work["normalized_sha256"],
                    work["runtime_analysis_sha256"],
                    safe_csv_text(work["native_workflow"]),
                ))
        return stream.getvalue()
    if kind != "markdown":
        raise ValueError("unsupported four-work native N format")
    lines = [
        "# Scriptorium · четыре книги · нативная неопределённость N", "",
        "Сохранённые измерения pylem==0.0.18 (AOT), не новый запуск.",
        "**DIAGNOSTIC_ONLY · M2: 0/5**. N не разделён на существительные и числительные.",
        "Доли от словоформ данной редакции; смешанные N не входят в N-only.", "",
        "| Произведение | Словоформ | Только N | Смешанные N | Любой N |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for work in report["works"]:
        def value(measure):
            return (f'{work["counts"][measure]:,} '
                    f'({work["percent_of_word_tokens"][measure]:.2f}%)')
        lines.append(
            f'| {work["title"]} | {work["word_tokens"]:,} | '
            f'{value("n_only")} | {value("n_mixed")} | {value("any_n")} |'
        )
    lines.extend(["", "## Разности внутри автора · процентные пункты", "",
                  "| Пара (вторая − первая) | Только N | Смешанные N | Любой N |",
                  "| --- | ---: | ---: | ---: |"])
    for name, values in report["same_author_percentage_point_deltas"].items():
        label = ("Воскресение − Анна Каренина" if name.startswith("tolstoy")
                 else "Дорога в никуда − Бегущая по волнам")
        lines.append("| " + label + " | " + " | ".join(
            f'{values[k]:+.2f}' for k in MEASURES) + " |")
    lines.extend(["", "## Проверяемые источники и границы", ""])
    for work in report["works"]:
        lines.extend([
            f'- {work["title"]} · {work["candidate_id"]}',
            f'  - {work["native_workflow"]}',
            f'  - normalized SHA-256: {work["normalized_sha256"]}',
            f'  - native analysis SHA-256: {work["runtime_analysis_sha256"]}',
        ])
    lines.extend(["", report["interpretation"], ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Replay four pinned source-free AOT N witnesses; not FantLab parity"
    )
    parser.add_argument("--root", type=Path, default=Path("."),
                        help="repository checkout containing the four reviewed assets")
    parser.add_argument("--format", choices=("markdown", "csv", "json"),
                        default="markdown")
    parser.add_argument("--output", type=Path, help="create-only report path")
    args = parser.parse_args(argv)
    try:
        rendered = render_fourwork_report(
            build_fourwork_report(args.root), args.format
        )
        if args.output is None:
            print(rendered, end="")
        else:
            _write_new(args.output, rendered)
    except FileExistsError:
        parser.error("report output already exists; choose another destination")
    except (OSError, LocalInputError, UnicodeError, ValueError,
            KeyError, TypeError, RecursionError):
        parser.error("pinned four-work native N evidence invalid or destination unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
