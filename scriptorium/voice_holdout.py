"""Exploratory leave-one-book-out stress test for the four pinned Russian editions.

This tests *whether the four selected works distinguish the two authors under
one documented distance rule*. It is not an author classifier, external
validation, confidence interval, FantLab parity, or an accepted M3 profile.
No literary text is loaded; the input is the strictly source-bound v1 preview.
"""
from __future__ import annotations

from collections.abc import Mapping
from math import fsum, isfinite
import re

from . import voice_profile as source

VERSION = "scriptorium-author-rhythm-holdout-v1"


def _finite(value: object) -> float:
    if type(value) not in (int, float) or not isfinite(value) or value < 0:
        raise ValueError("invalid held-out metric observation")
    return float(value)


def build_holdout(preview: Mapping[str, object]) -> dict[str, object]:
    """Rebuild each author's centroid without the evaluated book (four folds).

    Relative distance per feature is 2*abs(x-centroid)/(x+centroid), or 0
    if both are zero. The eight distances are equally weighted; the feature
    scale is not fitted using the held-out book. No held-out work contributes
    to either training centroid or to the feature weighting.
    """
    if (not isinstance(preview, dict) or preview.get("schema_version") != source.VERSION
            or preview.get("language") != "ru"
            or preview.get("source_snapshot") != "assets/evidence-snapshot.json"
            or not isinstance(preview.get("source_snapshot_git_blob_sha1"), str)
            or not re.fullmatch(r"[a-f0-9]{40}", preview["source_snapshot_git_blob_sha1"])):
        raise ValueError("invalid source-bound preview identity")
    boundary = preview.get("scientific_boundary")
    if (not isinstance(boundary, dict)
            or boundary.get("m3_accepted") is not False
            or boundary.get("m2_source_matched") != 0
            or boundary.get("m2_parity_admissible") is not False
            or boundary.get("translation_mixed") is not False
            or boundary.get("source_text_committed") is not False):
        raise ValueError("scientific boundary is not admissible for exploratory holdout")
    authors = preview.get("authors")
    if not isinstance(authors, list) or len(authors) != len(source.AUTHORS):
        raise ValueError("four pinned author observations required")
    ids = [feature[0] for feature in source.FEATURES]
    observed = []
    for author, expected in zip(authors, source.AUTHORS):
        author_id, display_name, work_keys = expected
        if (not isinstance(author, dict) or author.get("author_id") != author_id
                or author.get("display_name") != display_name or author.get("work_count") != 2):
            raise ValueError("author preview identity drift")
        works, metrics = author.get("works"), author.get("metrics")
        if (not isinstance(works, list) or not isinstance(metrics, list)
                or len(works) != 2 or len(metrics) != len(ids)
                or [work.get("key") for work in works] != list(work_keys)):
            raise ValueError("incomplete or reordered work evidence")
        values_by_work = {key: {} for key in work_keys}
        for metric, (metric_id, label, unit) in zip(metrics, source.FEATURES):
            if (not isinstance(metric, dict) or metric.get("id") != metric_id
                    or metric.get("label") != label or metric.get("unit") != unit):
                raise ValueError("changed metric definition")
            rows = metric.get("per_work")
            if (not isinstance(rows, list) or len(rows) != 2
                    or [row.get("work_key") for row in rows] != list(work_keys)):
                raise ValueError("missing source-specific measurements")
            for row in rows:
                values_by_work[row["work_key"]][metric_id] = _finite(row.get("value"))
        for work in works:
            if (not isinstance(work, dict) or type(work.get("word_weight")) is not int
                    or work["word_weight"] <= 0
                    or type(work.get("characters_including_spaces")) is not int
                    or work["characters_including_spaces"] < 300_000
                    or work["word_weight"] > work["characters_including_spaces"]
                    or not isinstance(work.get("source_sha256"), str)
                    or not re.fullmatch(r"[a-f0-9]{64}", work["source_sha256"])
                    or work["source_sha256"] != source._PINS[work["key"]][2]
                    or work.get("edition_id") != source._PINS[work["key"]][1]
                    or work["characters_including_spaces"] != source._PINS[work["key"]][3]
                    or not isinstance(work.get("title"), str) or not work["title"]):
                raise ValueError("invalid pinned book")
            observed.append({
                "key": work["key"], "title": work["title"],
                "author_id": author_id, "word_weight": work["word_weight"],
                "source_sha256": work["source_sha256"],
                "values": values_by_work[work["key"]],
            })
    if len({w["source_sha256"] for w in observed}) != 4:
        raise ValueError("duplicate source bodies in holdout")
    fold_results = []
    author_ids = [a[0] for a in source.AUTHORS]
    for held_out in observed:
        training = {
            author_id: [w for w in observed
                        if w["author_id"] == author_id and w["key"] != held_out["key"]]
            for author_id in author_ids
        }
        if sorted(len(v) for v in training.values()) != [1, 2]:
            raise ValueError("invalid training fold partition")
        raw_distances = {}
        for author_id in author_ids:
            rows = training[author_id]
            weight_total = sum(row["word_weight"] for row in rows)
            relative_errors = []
            for metric_id in ids:
                centroid = fsum(row["word_weight"] * row["values"][metric_id]
                                for row in rows) / weight_total
                value = held_out["values"][metric_id]
                denominator = value + centroid
                relative_errors.append(
                    0.0 if denominator == 0 else 2.0 * abs(value - centroid) / denominator
                )
            raw_distances[author_id] = fsum(relative_errors) / len(ids)
        if abs(raw_distances[author_ids[0]] - raw_distances[author_ids[1]]) < 1e-12:
            closer = None
        else:
            closer = min(author_ids, key=lambda item: raw_distances[item])
        fold_results.append({
            "held_out_work_key": held_out["key"],
            "held_out_work_title": held_out["title"],
            "known_author_id": held_out["author_id"],
            "training_work_keys": {aid: [row["key"] for row in training[aid]]
                                   for aid in author_ids},
            "relative_distances": {aid: round(raw_distances[aid], 6) for aid in author_ids},
            "nearest_author_id": closer,
            "nearer_to_labelled_author": None if closer is None
                                        else closer == held_out["author_id"],
        })
    return {
        "schema_version": VERSION,
        "source_preview_version": source.VERSION,
        "source_snapshot_git_blob_sha1": preview["source_snapshot_git_blob_sha1"],
        "method": {
            "folds": 4,
            "training": "exclude_held_out_work_from_both_word_weighted_author_centroids",
            "features": ids,
            "feature_distance": "2*abs(observed-centroid)/(observed+centroid); zero_if_both_zero",
            "aggregation": "arithmetic_mean_of_eight_equal_weight_feature_distances",
            "tie_threshold": 1e-12,
            "train_works_per_fold": [1, 2],
            "distance_is_not_probability": True,
        },
        "summary": {
            "total_folds": 4,
            "nearer_to_labelled_author": sum(f["nearer_to_labelled_author"] is True for f in fold_results),
            "nearer_to_other_author": sum(f["nearer_to_labelled_author"] is False for f in fold_results),
            "ties": sum(f["nearer_to_labelled_author"] is None for f in fold_results),
        },
        "scientific_boundary": {
            "class": "exploratory_four_work_within_sample_stress_test",
            "independent_external_validation": False,
            "m2_source_matched": 0, "m3_accepted": False,
            "works_per_author": 2, "only_two_authors": True,
            "no_fantlab_parity_claim": True, "no_source_text_committed": True,
        },
        "folds": fold_results,
    }


def render_markdown(result: Mapping[str, object]) -> str:
    if (result.get("schema_version") != VERSION
            or result.get("scientific_boundary", {}).get("m3_accepted") is not False
            or result.get("scientific_boundary", {}).get("independent_external_validation") is not False):
        raise ValueError("unverified holdout scientific boundary")
    summary = result["summary"]
    lines = [
        "# Scriptorium — проверка устойчивости авторского ритма",
        "",
        "> Эксперимент на четырёх заранее выбранных русских книгах двух авторов. "
        "Это не авторский классификатор, внешняя валидация или доказательство FantLab. "
        "M2: 0/5; M3: открыт.",
        "",
        "Каждую книгу по очереди убираем из расчёта. Два авторских центра "
        "строятся только по оставшимся книгам (1 книга своего автора, 2 другого), "
        "с весами по числу слов. Расстояние — среднее по 8 равновесным признакам: "
        "2 × |значение − центр| / (значение + центр), оба нуля → 0. "
        "Меньше — ближе; расстояние не является вероятностью.",
        "",
        "| Исключённая книга | Известный автор | До Грина | До Толстого | Ближе к |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    author_names = {aid: name for aid, name, _ in source.AUTHORS}
    for row in result["folds"]:
        closest = row["nearest_author_id"]
        lines.append(
            "| " + source._markdown_cell(row["held_out_work_title"])
            + " | " + author_names[row["known_author_id"]]
            + " | " + f'{row["relative_distances"]["grin"]:.6f}'
            + " | " + f'{row["relative_distances"]["tolstoy"]:.6f}'
            + " | " + (author_names[closest] if closest is not None else "равенство") + " |"
        )
    lines += [
        "",
        "**Ближе к указанному автору: "
        + str(summary["nearer_to_labelled_author"]) + " из 4; к другому: "
        + str(summary["nearer_to_other_author"]) + "; ничьи: "
        + str(summary["ties"]) + ".**",
        "",
        "Этот результат ограничен четырьмя книгами, выбранными авторами и "
        "произвольным равным весом признаков. Даже совпадение 4/4 не "
        "подтвердило бы устойчивый авторский отпечаток. "
        "Внешняя проверка на новых произведениях и авторах НЕ ПРОВОДИЛАСЬ. "
        "М3 остаётся открыт; исходные тексты не читаются.",
        "",
    ]
    return "\n".join(lines)
