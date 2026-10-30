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
    expected_candidate, expected_edition, expected_hash, expected_chars = _PINS[key]
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


def build_preview(snapshot: Mapping[str, object], *, source_blob_sha1: str) -> dict[str, object]:
    """Produce fixed-source weighted mean and population SD; no source text or M2 claims."""
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
    if not set(_PINS).issubset(indexed):
        raise ValueError("incomplete frozen work inventory")
    output_authors = []
    for author_id, name, keys in AUTHORS:
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
            })
        for row in work_rows:
            del row["measurements"]
        output_authors.append({
            "author_id": author_id, "display_name": name,
            "work_count": len(work_rows), "word_weight_total": denominator,
            "works": work_rows, "metrics": metrics,
        })
    return {
        "schema_version": VERSION, "language": "ru",
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify or export source-free two-author descriptive preview")
    parser.add_argument("--snapshot", type=Path, default=Path("assets/evidence-snapshot.json"))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", type=Path)
    group.add_argument("--check", type=Path)
    args = parser.parse_args(argv)
    raw = args.snapshot.read_bytes()
    artifact = build_preview(json.loads(raw), source_blob_sha1=_git_blob_sha(raw))
    if args.check is not None:
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        if artifact != actual:
            raise ValueError("retained author preview differs from deterministic source-derived values")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_json(artifact), encoding="utf-8")
    print("VOICE_PREVIEW=VERIFIED; authors=2; editions=4; fields=16; M2=0/5; M3=OPEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
