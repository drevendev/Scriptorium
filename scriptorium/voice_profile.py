"""Source-bound two-work author rhythm preview; not FantLab parity or an accepted M3 profile.

No source prose is loaded or published. We aggregate existing, versioned and
independently measured Russian-edition scalars. This is a descriptive extension,
not a pooled corpus remeasurement, classifier or confidence interval.
"""
from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from hashlib import sha1
import json
from math import fsum, isfinite, sqrt
from pathlib import Path
import re

VERSION = "scriptorium-author-rhythm-preview-v1"
EXTENDED_VERSION = "scriptorium-author-rhythm-preview-v2"
# Exact Git blob for the pinned, source-free wheel resource; drift must fail closed.
_PACKAGED_SOURCE_BLOB_SHA1 = "a84986fd72ad616006b8ce179d1653e5ecf13729"
_MIN_CHARACTERS = 300_000
_SOURCE_PROFILES = {
    "metrics": "scriptorium-metrics-v4",
    "normalization": "scriptorium-text-v1",
    "dialogue": "scriptorium-dialogue-v1",
    "vocabulary": "scriptorium-vocabulary-v1",
    "punctuation": "scriptorium-punctuation-v2",
}
# This is a closed, independently frozen set, not an automatic author classifier.
_PINS = {
    "waves": (
        "grin-running-on-waves-ru", "ru-frozen-363819",
        "41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc", 363819
    ),
    "road": (
        "grin-road-nowhere-ru", "ru-wikisource-az-lib-oldid-5585836",
        "e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee", 442656
    ),
    "anna": (
        "tolstoy-anna-karenina-ru", "ru-wikisource-239-chapters",
        "1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205", 1705605
    ),
    "resurrection": (
        "tolstoy-resurrection-ru", "ru-wikisource-129-chapters",
        "2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0", 890835
    ),
}
AUTHORS = (
    ("grin", "Александр Грин", ("waves", "road")),
    ("tolstoy", "Лев Толстой", ("anna", "resurrection")),
)
# The opt-in third author uses existing independently frozen source-free
# measurements. The original v1 preview/holdout/ablation are not re-fitted.
_DOSTOEVSKY_AUTHOR = ("dostoevsky", "Фёдор Достоевский", ("karamazov", "humiliated"))
_DOSTOEVSKY_PINS = {
    "karamazov": (
        "dostoevsky-brothers-karamazov-ru", "ru-wikisource-98",
        "26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6", 1810351,
    ),
    "humiliated": (
        "dostoevsky-humiliated-and-insulted-azlib-ru",
        "ru-wikisource-az-lib-oldid-5611473",
        "ffc6825db7f442c7df93136e8ddf90ce44be8801cdbaa727d5fe642db3fad8fa", 713925,
    ),
}
# Rates and mean lengths only. Unique-vocabulary sizes and absolute counts do
# not have a meaningful work-weighted author-average interpretation.
FEATURES = (
    ("fantlab.general.mean_word_length_chars", "Средняя длина слова", "знаков/слово"),
    ("fantlab.general.mean_sentence_length_chars", "Средняя длина предложения", "знаков/предложение"),
    ("fantlab.dialogue.share_percent", "Доля диалогов", "%"),
    ("fantlab.dialogue.author_text_inside_dialogue_percent", "Авторские ремарки в диалогах", "%"),
    ("fantlab.punctuation.comma.per_1000_words", "Запятые", "на 1000 слов"),
    ("fantlab.punctuation.dash.per_1000_words", "Тире", "на 1000 слов"),
    ("fantlab.punctuation.question.per_1000_words", "Вопросы", "на 1000 слов"),
    ("fantlab.punctuation.semicolon.per_1000_words", "Точка с запятой", "на 1000 слов"),
)


def _number(row: Mapping[str, object], key: str, *, integer: bool = False) -> int | float:
    if row.get("id") != key or row.get("status") != "measured" or row.get("kind") != "candidate":
        raise ValueError("non-measured or changed metric identity: " + key)
    value = row.get("actual")
    if (type(value) is not int if integer else type(value) not in (int, float)):
        raise ValueError("non-numeric measurement: " + key)
    if not isfinite(value) or value < 0:
        raise ValueError("invalid measurement: " + key)
    if integer and value == 0:
        raise ValueError("zero word-count weight")
    if key.endswith("_percent") and value > 100:
        raise ValueError("invalid percentage: " + key)
    return value


def _frozen_work(book: Mapping[str, object], key: str, author: str) -> dict[str, object]:
    pins = _PINS if key in _PINS else _DOSTOEVSKY_PINS
    expected_candidate, expected_edition, expected_hash, expected_chars = pins[key]
    if (book.get("key") != key or book.get("candidate_id") != expected_candidate
            or book.get("edition_id") != expected_edition
            or book.get("source_sha256") != expected_hash
            or book.get("original_language") != "ru" or book.get("language") != "ru"
            or book.get("translator") is not None or book.get("display_author") != author
            or book.get("text_status") != "measured"
            or book.get("profiles") != _SOURCE_PROFILES):
        raise ValueError("source, translation, author or profile drift: " + key)
    rows = book.get("metrics")
    if type(rows) is not list or len(rows) < len(FEATURES) + 2:
        raise ValueError("missing metric rows: " + key)
    by_id: dict[str, Mapping[str, object]] = {}
    for row in rows:
        if not isinstance(row, dict) or type(row.get("id")) is not str or row["id"] in by_id:
            raise ValueError("duplicate or malformed metric rows: " + key)
        by_id[row["id"]] = row
    characters = _number(by_id.get("fantlab.general.characters", {}), "fantlab.general.characters", integer=True)
    words = _number(by_id.get("fantlab.general.words", {}), "fantlab.general.words", integer=True)
    if characters != expected_chars or characters < _MIN_CHARACTERS or words > characters:
        raise ValueError("invalid frozen work size: " + key)
    measurements = {}
    for metric_id, _label, _unit in FEATURES:
        value = _number(by_id.get(metric_id, {}), metric_id)
        measurements[metric_id] = value
    evidence = book.get("evidence_url")
    if type(evidence) is not str or not evidence.startswith("https://github.com/drevendev/Scriptorium/blob/master/"):
        raise ValueError("missing retained source evidence: " + key)
    if type(book.get("display_title")) is not str or not book["display_title"]:
        raise ValueError("invalid work title: " + key)
    return {
        "key": key, "candidate_id": expected_candidate, "title": book["display_title"],
        "edition_id": expected_edition, "source_sha256": expected_hash,
        "characters_including_spaces": characters, "word_weight": words,
        "evidence_url": evidence, "measurements": measurements,
    }


def build_preview(snapshot: Mapping[str, object], *, source_blob_sha1: str,
                  include_dostoevsky: bool = False) -> dict[str, object]:
    """Produce fixed-source weighted mean and population SD; no source text or M2 claims."""
    if type(include_dostoevsky) is not bool:
        raise ValueError("invalid optional author selection")
    selected_authors = AUTHORS + (_DOSTOEVSKY_AUTHOR,) if include_dostoevsky else AUTHORS
    required_keys = {key for _, _, keys in selected_authors for key in keys}
    if (not isinstance(snapshot, dict) or snapshot.get("schema") != "scriptorium-ru-reader-v2"
            or snapshot.get("language_module") != "ru"
            or snapshot.get("scientific_claim") != "DIAGNOSTIC_ONLY"
            or snapshot.get("fantlab_input_identity") != "UNKNOWN"
            or snapshot.get("counts", {}).get("m2_source_matched") != 0
            or snapshot.get("comparability", {}).get("m2_parity_admissible") is not False):
        raise ValueError("unverified input scientific boundary")
    if type(source_blob_sha1) is not str or not re.fullmatch(r"[0-9a-f]{40}", source_blob_sha1):
        raise ValueError("source snapshot Git blob identity missing")
    books = snapshot.get("books")
    if type(books) is not list:
        raise ValueError("missing edition list")
    indexed = {}
    for book in books:
        if not isinstance(book, dict) or type(book.get("key")) is not str or book["key"] in indexed:
            raise ValueError("duplicate or malformed edition keys")
        indexed[book["key"]] = book
    if not required_keys.issubset(indexed):
        raise ValueError("incomplete frozen work inventory")
    output_authors = []
    for author_id, name, keys in selected_authors:
        work_rows = [_frozen_work(indexed[key], key, name) for key in keys]
        if len({row["source_sha256"] for row in work_rows}) != len(keys):
            raise ValueError("duplicate source body in author preview")
        weights = [int(row["word_weight"]) for row in work_rows]
        denominator = sum(weights)
        metrics = []
        for metric_id, label, unit in FEATURES:
            values = [float(row["measurements"][metric_id]) for row in work_rows]
            average = fsum(w * x for w, x in zip(weights, values)) / denominator
            dispersion = sqrt(fsum(w * (x - average) ** 2 for w, x in zip(weights, values)) / denominator)
            metrics.append({
                "id": metric_id, "label": label, "unit": unit,
                "weighted_mean": round(average, 6),
                "weighted_population_stddev": round(dispersion, 6),
                # Preserve independently measured book values, not merely their
                # weighted aggregate. These are source-bound observations, not
                # a within-author confidence interval or validated style score.
                "per_work": [
                    {"work_key": row["key"], "value": value}
                    for row, value in zip(work_rows, values)
                ],
            })
        for row in work_rows:
            del row["measurements"]
        output_authors.append({
            "author_id": author_id, "display_name": name,
            "work_count": len(work_rows), "word_weight_total": denominator,
            "works": work_rows, "metrics": metrics,
        })
    return {
        "schema_version": EXTENDED_VERSION if include_dostoevsky else VERSION,
        "language": "ru",
        "source_snapshot": "assets/evidence-snapshot.json",
        "source_snapshot_git_blob_sha1": source_blob_sha1,
        "aggregation": {
            "weight": "scriptorium_measured_word_count_per_work",
            "mean": "sum(word_weight * work_metric) / sum(word_weight)",
            "dispersion": "sqrt(sum(word_weight * (work_metric - weighted_mean)^2) / sum(word_weight))",
            "round_decimal_places": 6, "not_a_pooled_raw_text_analysis": True,
        },
        "scientific_boundary": {
            "class": "independent_descriptive_extension_preview",
            "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False,
            "m2_source_matched": 0, "m3_accepted": False,
            "cross_validation": "NOT_RUN", "uncertainty": "ONLY_TWO_WORKS_PER_AUTHOR",
            "translation_mixed": False, "source_text_committed": False,
        },
        "source_metric_profiles": dict(_SOURCE_PROFILES),
        "authors": output_authors,
    }


def _git_blob_sha(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def render_json(artifact: Mapping[str, object]) -> str:
    return json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"


def _markdown_cell(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def render_markdown(artifact: Mapping[str, object]) -> str:
    """A source-free human report, not a FantLab or statistically accepted author profile."""
    selected_version = artifact.get("schema_version")
    if (selected_version not in (VERSION, EXTENDED_VERSION)
            or len(artifact.get("authors", [])) != (3 if selected_version == EXTENDED_VERSION else 2)
            or artifact.get("scientific_boundary", {}).get("m3_accepted") is not False
            or artifact.get("scientific_boundary", {}).get("m2_source_matched") != 0):
        raise ValueError("unverified author-preview scientific boundary")
    lines = [
        ("# Scriptorium — ритм трёх авторов (исследовательский предпросмотр)"
         if selected_version == EXTENDED_VERSION else
         "# Scriptorium — ритм двух авторов (исследовательский предпросмотр)"),
        "",
        "> Только описательное расширение Scriptorium: по две измеренные русские книги "
        "на автора. Это не авторский отпечаток, доверительный интервал, доказательство "
        "совместимости с FantLab или принятый M3-профиль. M2: 0/5; M3: открыт.",
        "",
        "Среднее взвешено по количеству слов каждой книги. Стандартное отклонение "
        "показывает разброс **между двумя книгами**, а не неопределённость оценки автора.",
        "",
        "Источник: `" + _markdown_cell(artifact["source_snapshot"]) + "`, Git blob `"
        + _markdown_cell(artifact["source_snapshot_git_blob_sha1"]) + "`.",
        "",
    ]
    for author in artifact["authors"]:
        works = author["works"]
        if len(works) != 2:
            raise ValueError("preview requires two independently measured works")
        lines += [
            "## " + _markdown_cell(author["display_name"]),
            "",
            "Книга 1: " + _markdown_cell(works[0]["title"]) + " (`" + _markdown_cell(works[0]["key"]) + "`).  "
            "Книга 2: " + _markdown_cell(works[1]["title"]) + " (`" + _markdown_cell(works[1]["key"]) + "`).",
            "",
            "| Метрика | Единица | Книга 1 | Книга 2 | Среднее по словам | Разброс между книгами |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
        for metric in author["metrics"]:
            observed = metric["per_work"]
            if len(observed) != 2 or [row["work_key"] for row in observed] != [w["key"] for w in works]:
                raise ValueError("source-bound book observations missing")
            lines.append(
                "| " + _markdown_cell(metric["label"]) + " | " + _markdown_cell(metric["unit"])
                + " | " + f'{observed[0]["value"]:.6f}'
                + " | " + f'{observed[1]["value"]:.6f}'
                + " | " + f'{metric["weighted_mean"]:.6f}'
                + " | " + f'{metric["weighted_population_stddev"]:.6f}' + " |"
            )
        lines.append("")
    lines.append("Исходные тексты не читаются и не публикуются; единицы и версии показателей сохранены.")
    return "\n".join(lines) + "\n"


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate snapshot JSON field")
        value[key] = item
    return value


def main(argv: Sequence[str] | None = None) -> int:
    from .analyze import LocalInputError, _read_bounded_regular_file, _write_new

    parser = argparse.ArgumentParser(
        description="Read the pinned source-free two-author rhythm preview (M2 0/5; M3 open)"
    )
    parser.add_argument("--snapshot", type=Path, help="override the pinned bundled source-free snapshot")
    parser.add_argument("--include-dostoevsky", action="store_true",
                        help="opt-in source-bound third author from two Russian editions (v2)")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    analysis_group = parser.add_mutually_exclusive_group()
    analysis_group.add_argument("--holdout", action="store_true",
                                help="exploratory leave-one-book-out stress test; not accepted M3")
    analysis_group.add_argument("--ablate", action="store_true",
                                help="rerun four-book holdout with each feature omitted; not feature selection")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--output", type=Path, help="create a new derived report; never overwrite")
    group.add_argument("--check", type=Path, help="verify an existing JSON artifact")
    args = parser.parse_args(argv)
    if args.check is not None and args.format != "json":
        parser.error("--check requires JSON format")
    if args.check is not None and (args.holdout or args.ablate):
        parser.error("--holdout/--ablate cannot be combined with --check")
    if args.include_dostoevsky and (args.holdout or args.ablate):
        parser.error("four-book holdout/ablation require the original two-author preview")
    try:
        source = args.snapshot if args.snapshot is not None else Path(__file__).parent / "data" / "evidence-snapshot.json"
        raw = _read_bounded_regular_file(source, 8 * 1024 * 1024, "snapshot")
        if args.snapshot is None and _git_blob_sha(raw) != _PACKAGED_SOURCE_BLOB_SHA1:
            raise ValueError("bundled source-free snapshot identity drift")
        artifact = build_preview(
            json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_pairs),
            source_blob_sha1=_git_blob_sha(raw),
            include_dostoevsky=args.include_dostoevsky,
        )
        if args.check is not None:
            reference = _read_bounded_regular_file(args.check, 8 * 1024 * 1024, "reference")
            actual = json.loads(reference.decode("utf-8"), object_pairs_hook=_unique_pairs)
            if artifact != actual:
                raise ValueError("retained preview differs from source evidence")
            print("VOICE_PREVIEW=VERIFIED; authors=" + ("3; editions=6; fields=24" if args.include_dostoevsky
                  else "2; editions=4; fields=16") + "; M2=0/5; M3=OPEN")
        else:
            if args.holdout:
                from .voice_holdout import build_holdout, render_markdown as render_holdout_markdown
                evaluation = build_holdout(artifact)
                rendered = (render_holdout_markdown(evaluation) if args.format == "markdown"
                            else render_json(evaluation))
            elif args.ablate:
                from .voice_ablation import build_ablation, render_markdown as render_ablation_markdown
                evaluation = build_ablation(artifact)
                rendered = (render_ablation_markdown(evaluation) if args.format == "markdown"
                            else render_json(evaluation))
            else:
                rendered = render_markdown(artifact) if args.format == "markdown" else render_json(artifact)
            if args.output is None:
                print(rendered, end="")
            else:
                _write_new(args.output, rendered)
                print("VOICE_PREVIEW=VERIFIED; authors=" + ("3; editions=6; fields=24" if args.include_dostoevsky
                      else "2; editions=4; fields=16") + "; M2=0/5; M3=OPEN")
    except FileExistsError:
        parser.error("derived report already exists; choose another destination")
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError, LocalInputError):
        parser.error("unable to verify the source-free author preview or write the derived report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
