"""Offline source-free replay of the two pinned native N uncertainty measurements.

This never runs morphology or infers noun/cardinal categories. It rejects changed
witness bytes, including plausible-looking counts with a different source identity.
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
from .native_n_crosswork import compare_pinned_native_n
from .native_n_evidence import build_native_n_report, MAX_EVIDENCE_BYTES

SCHEMA = "scriptorium-native-n-crosswork-offline-v1"
RESURRECTION_PATH = Path("assets/n-uncertainty-resurrection-summary.json")
RESURRECTION_GIT_BLOB_SHA1 = "539fadbc88b3dff64da9fccae4d9aaf676cf2f7b"
MEASURES = (
    ("n_only", "Только N", "n_only", "anna_n_only_percent", "resurrection_n_only_percent"),
    ("n_mixed", "Смешанные N", "n_mixed_excluded", "anna_n_mixed_percent", "resurrection_n_mixed_percent"),
    ("any_n", "Любой N-кандидат", None, "anna_any_n_percent", "resurrection_any_n_percent"),
)


def _load_resurrection(root: Path) -> dict[str, object]:
    raw = _read_bounded_regular_file(root / RESURRECTION_PATH, MAX_EVIDENCE_BYTES,
                                     "retained Resurrection native N evidence")
    git_blob = b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    if sha1(git_blob).hexdigest() != RESURRECTION_GIT_BLOB_SHA1:
        raise ValueError("retained Resurrection N witness differs from reviewed Git blob")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_keys)


def build_crosswork_report(root: Path) -> dict[str, object]:
    """Validate exact immutable native receipts before deriving three token shares."""
    anna = build_native_n_report(root)["witness"]
    resurrection = _load_resurrection(root)
    values = compare_pinned_native_n(anna, resurrection)
    left, right = anna["counts"], resurrection["counts"]
    rows = []
    for measure_id, label, count_key, left_key, right_key in MEASURES:
        left_count = (left["n_only"] + left["n_mixed_excluded"]
                      if count_key is None else left[count_key])
        right_count = (right["n_only"] + right["n_mixed_excluded"]
                       if count_key is None else right[count_key])
        left_rate, right_rate = values[left_key], values[right_key]
        rows.append({
            "measure_id": measure_id,
            "label_ru": label,
            "anna_count": left_count,
            "resurrection_count": right_count,
            "anna_percent_of_word_tokens": left_rate,
            "resurrection_percent_of_word_tokens": right_rate,
            "resurrection_minus_anna_percentage_points": right_rate - left_rate,
        })
    return {
        "schema_version": SCHEMA,
        "status": "diagnostic_only",
        "source_text_included": False,
        "m2_parity_admissible": False,
        "provider": "pylem==0.0.18 (pylem-0.0.18-python39-sidecar-v1)",
        "measurement": "replay_of_two_independent_pinned_native_receipts_not_new_run",
        "works": [
            {
                "candidate_id": anna["work"]["candidate_id"],
                "title": anna["work"]["title"],
                "word_tokens": left["word_count"],
                "normalized_sha256": anna["evidence"]["normalized_sha256"],
                "runtime_analysis_sha256": anna["evidence"]["runtime_analysis_sha256"],
                "native_workflow": anna["evidence"]["workflow_url"],
            },
            {
                "candidate_id": resurrection["evidence"]["candidate_id"],
                "title": "Воскресение",
                "word_tokens": right["word_count"],
                "normalized_sha256": resurrection["evidence"]["normalized_sha256"],
                "runtime_analysis_sha256": resurrection["evidence"]["runtime_analysis_sha256"],
                "native_workflow": "https://github.com/drevendev/Scriptorium/actions/runs/"
                                   + str(resurrection["evidence"]["run_id"]),
            },
        ],
        "rows": rows,
        "interpretation": "observed candidate coverage; not recovered noun/cardinal POS or FantLab homonym selection",
    }


def render_crosswork_report(report: dict[str, object], kind: str) -> str:
    """Render exact data as machine-readable or accessible source-free tables."""
    if kind == "json":
        return json.dumps(report, ensure_ascii=False, sort_keys=True,
                          indent=2, allow_nan=False) + "\n"
    left, right = report["works"]
    if kind == "csv":
        stream = StringIO(newline="")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("measure_id", "anna_count", "anna_word_tokens",
                         "anna_percent_of_word_tokens", "resurrection_count",
                         "resurrection_word_tokens", "resurrection_percent_of_word_tokens",
                         "resurrection_minus_anna_percentage_points", "status",
                         "anna_candidate_id", "anna_normalized_sha256",
                         "anna_runtime_analysis_sha256", "anna_native_workflow",
                         "resurrection_candidate_id", "resurrection_normalized_sha256",
                         "resurrection_runtime_analysis_sha256", "resurrection_native_workflow"))
        for row in report["rows"]:
            writer.writerow((safe_csv_text(row["measure_id"]), row["anna_count"],
                             left["word_tokens"], f'{row["anna_percent_of_word_tokens"]:.6f}',
                             row["resurrection_count"], right["word_tokens"],
                             f'{row["resurrection_percent_of_word_tokens"]:.6f}',
                             f'{row["resurrection_minus_anna_percentage_points"]:+.6f}',
                             "diagnostic_only",
                             safe_csv_text(left["candidate_id"]), left["normalized_sha256"],
                             left["runtime_analysis_sha256"], safe_csv_text(left["native_workflow"]),
                             safe_csv_text(right["candidate_id"]), right["normalized_sha256"],
                             right["runtime_analysis_sha256"], safe_csv_text(right["native_workflow"])))
        return stream.getvalue()
    if kind != "markdown":
        raise ValueError("unsupported cross-work report format")
    lines = [
        "# Scriptorium · измеренная неопределённость N", "",
        "Две разные книги, два независимо закреплённых анализа AOT/pylem 0.0.18.",
        "**M2: 0/5.** Категория N не разделена на существительные и числительные; "
        "это не проверка соответствия FantLab.", "",
        "| Кандидаты | Анна Каренина · из 269 358 словоформ | "
        "Воскресение · из 136 129 словоформ | Воскресение − Анна · п. п. |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in report["rows"]:
        lines.append(
            f'| {row["label_ru"]} | {row["anna_count"]:,} ({row["anna_percent_of_word_tokens"]:.2f}%) '
            f'| {row["resurrection_count"]:,} ({row["resurrection_percent_of_word_tokens"]:.2f}%) '
            f'| {row["resurrection_minus_anna_percentage_points"]:+.2f} |'
        )
    lines += [
        "", "Доли N-only и смешанных N не пересекаются; «любой N» — их сумма. "
        "Числа округлены только для показа, это не правила округления FantLab.",
        "Разница между книгами описательная: не точность распознавания частей речи "
        "и не восстановленный выбор омонимов.", "",
        "Подтверждения независимых запусков и SHA-256 идентичностей:", "",
        f'- Анна Каренина ({left["candidate_id"]}): {left["native_workflow"]}',
        f'  - Нормализованный текст · SHA-256: \`{left["normalized_sha256"]}\`',
        f'  - Нативный анализ · SHA-256: \`{left["runtime_analysis_sha256"]}\`',
        f'- Воскресение ({right["candidate_id"]}): {right["native_workflow"]}',
        f'  - Нормализованный текст · SHA-256: \`{right["normalized_sha256"]}\`',
        f'  - Нативный анализ · SHA-256: \`{right["runtime_analysis_sha256"]}\`', "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Replay frozen source-free native N observations from two books (M2 0/5)")
    parser.add_argument("--root", type=Path, default=Path("."),
                        help="Repository checkout with two pinned assets/n-uncertainty JSON receipts")
    parser.add_argument("--format", choices=("markdown", "csv", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="Create-only offline report path")
    args = parser.parse_args(argv)
    try:
        output = render_crosswork_report(build_crosswork_report(args.root), args.format)
        if args.output is None:
            print(output, end="")
        else:
            _write_new(args.output, output)
    except FileExistsError:
        parser.error("report output already exists; choose another destination")
    except (LocalInputError, OSError, UnicodeError, ValueError, TypeError, KeyError, RecursionError):
        parser.error("pinned native N receipts invalid or destination unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
