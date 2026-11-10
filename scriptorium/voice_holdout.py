"""Source-bound leave-one-book-out rhythm stress tests (four or six editions).

These are exploratory in-sample diagnostics, not an author classifier, external
validation, confidence interval, FantLab parity or an accepted M3 profile.
No literary text is loaded; v1 remains a separate frozen four-work contract.
"""
from __future__ import annotations

from collections.abc import Mapping
from math import fsum, isfinite, sqrt
import re

from . import voice_profile as source

VERSION = "scriptorium-author-rhythm-holdout-v1"
EXTENDED_VERSION = "scriptorium-author-rhythm-holdout-v2"


def _finite(value: object) -> float:
    if type(value) not in (int, float) or not isfinite(value) or value < 0:
        raise ValueError("invalid held-out metric observation")
    return float(value)


def build_holdout(preview: Mapping[str, object]) -> dict[str, object]:
    """Rebuild each author's centroid without the evaluated book (four or six folds).

    Relative distance per feature is 2*abs(x-centroid)/(x+centroid), or 0
    if both are zero. The eight distances are equally weighted; the feature
    scale is not fitted using the held-out book. No held-out work contributes
    to either training centroid or to the feature weighting.
    """
    expanded = isinstance(preview, dict) and preview.get("schema_version") == source.EXTENDED_VERSION
    selected_authors = source.AUTHORS + (source._DOSTOEVSKY_AUTHOR,) if expanded else source.AUTHORS
    if (not isinstance(preview, dict)
            or preview.get("schema_version") not in (source.VERSION, source.EXTENDED_VERSION)
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
    if preview.get("source_metric_profiles") != source._SOURCE_PROFILES:
        raise ValueError("source metric-profile identity drift")
    authors = preview.get("authors")
    if not isinstance(authors, list) or len(authors) != len(selected_authors):
        raise ValueError("incomplete pinned author observations")
    ids = [feature[0] for feature in source.FEATURES]
    observed = []
    for author, expected in zip(authors, selected_authors):
        author_id, display_name, work_keys = expected
        if (not isinstance(author, dict) or author.get("author_id") != author_id
                or author.get("display_name") != display_name or author.get("work_count") != 2):
            raise ValueError("author preview identity drift")
        works, metrics = author.get("works"), author.get("metrics")
        if (not isinstance(works, list) or not isinstance(metrics, list)
                or len(works) != 2 or len(metrics) != len(ids)
                or [work.get("key") for work in works] != list(work_keys)):
            raise ValueError("incomplete or reordered work evidence")
        weights = [work.get("word_weight") for work in works]
        if (any(type(weight) is not int or weight <= 0 for weight in weights)
                or type(author.get("word_weight_total")) is not int
                or author["word_weight_total"] != sum(weights)):
            raise ValueError("inconsistent author word weights")
        weight_total = sum(weights)
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
            # Verify the source-bound descriptive preview before using its raw
            # observations for holdout. Do not treat declared aggregates as
            # independent source authentication or external validation.
            values = [values_by_work[key][metric_id] for key in work_keys]
            mean = fsum(weight * value for weight, value in zip(weights, values)) / weight_total
            deviation = sqrt(fsum(
                weight * (value - mean) ** 2 for weight, value in zip(weights, values)
            ) / weight_total)
            for field, expected in (
                ("weighted_mean", mean),
                ("weighted_population_stddev", deviation),
            ):
                reported = metric.get(field)
                if (type(reported) not in (int, float) or not isfinite(reported)
                        or reported < 0 or reported != round(expected, 6)):
                    raise ValueError("inconsistent source-bound author aggregate: " + metric_id)
        for work in works:
            if not isinstance(work, dict):
                raise ValueError("invalid pinned book")
            pins = source._PINS if work.get("key") in source._PINS else source._DOSTOEVSKY_PINS
            if (not isinstance(work, dict) or type(work.get("word_weight")) is not int
                    or work["word_weight"] <= 0
                    or type(work.get("characters_including_spaces")) is not int
                    or work["characters_including_spaces"] < 300_000
                    or work["word_weight"] > work["characters_including_spaces"]
                    or not isinstance(work.get("source_sha256"), str)
                    or not re.fullmatch(r"[a-f0-9]{64}", work["source_sha256"])
                    or work["source_sha256"] != pins[work["key"]][2]
                    or work.get("edition_id") != pins[work["key"]][1]
                    or work["characters_including_spaces"] != pins[work["key"]][3]
                    or not isinstance(work.get("title"), str) or not work["title"]):
                raise ValueError("invalid pinned book")
            observed.append({
                "key": work["key"], "title": work["title"],
                "author_id": author_id, "word_weight": work["word_weight"],
                "source_sha256": work["source_sha256"],
                "values": values_by_work[work["key"]],
            })
    if len({w["source_sha256"] for w in observed}) != 2 * len(selected_authors):
        raise ValueError("duplicate source bodies in holdout")
    fold_results = []
    author_ids = [a[0] for a in selected_authors]
    for held_out in observed:
        training = {
            author_id: [w for w in observed
                        if w["author_id"] == author_id and w["key"] != held_out["key"]]
            for author_id in author_ids
        }
        if (len(training[held_out["author_id"]]) != 1
                or any(len(training[aid]) != 2 for aid in author_ids
                       if aid != held_out["author_id"])):
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
        best = min(raw_distances.values())
        winners = [aid for aid in author_ids if abs(raw_distances[aid] - best) < 1e-12]
        closer = winners[0] if len(winners) == 1 else None
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
        "schema_version": EXTENDED_VERSION if expanded else VERSION,
        "source_preview_version": source.EXTENDED_VERSION if expanded else source.VERSION,
        "source_snapshot_git_blob_sha1": preview["source_snapshot_git_blob_sha1"],
        "method": {
            "folds": len(observed),
            "training": ("exclude_held_out_work_from_all_word_weighted_author_centroids"
                         if expanded else "exclude_held_out_work_from_both_word_weighted_author_centroids"),
            "features": ids,
            "feature_distance": "2*abs(observed-centroid)/(observed+centroid); zero_if_both_zero",
            "aggregation": "arithmetic_mean_of_eight_equal_weight_feature_distances",
            "tie_threshold": 1e-12,
            "train_works_per_fold": [1, 2, 2] if expanded else [1, 2],
            "distance_is_not_probability": True,
        },
        "summary": {
            "total_folds": len(observed),
            "nearer_to_labelled_author": sum(f["nearer_to_labelled_author"] is True for f in fold_results),
            "nearer_to_other_author": sum(f["nearer_to_labelled_author"] is False for f in fold_results),
            "ties": sum(f["nearer_to_labelled_author"] is None for f in fold_results),
        },
        "scientific_boundary": {
            "class": ("exploratory_six_work_three_author_within_sample_stress_test"
                      if expanded else "exploratory_four_work_within_sample_stress_test"),
            "independent_external_validation": False,
            "m2_source_matched": 0, "m3_accepted": False,
            "works_per_author": 2, "only_two_authors": not expanded,
            "no_fantlab_parity_claim": True, "no_source_text_committed": True,
        },
        "folds": fold_results,
    }



def _render_extended_markdown(result: Mapping[str, object]) -> str:
    """Six source-bound, exploratory folds; keep the existing v1 prose intact."""
    boundary = result.get("scientific_boundary")
    authors = source.AUTHORS + (source._DOSTOEVSKY_AUTHOR,)
    author_ids = [aid for aid, _, _ in authors]
    if (result.get("source_preview_version") != source.EXTENDED_VERSION
            or not isinstance(boundary, dict)
            or boundary.get("class") != "exploratory_six_work_three_author_within_sample_stress_test"
            or boundary.get("m3_accepted") is not False
            or boundary.get("m2_source_matched") != 0
            or boundary.get("independent_external_validation") is not False
            or boundary.get("no_source_text_committed") is not True
            or boundary.get("no_fantlab_parity_claim") is not True):
        raise ValueError("unverified three-author holdout boundary")
    folds, summary = result.get("folds"), result.get("summary")
    if (not isinstance(folds, list) or len(folds) != 6
            or not isinstance(summary, dict) or summary.get("total_folds") != 6):
        raise ValueError("missing six-fold holdout evidence")
    names = {aid: name for aid, name, _ in authors}
    lines = [
        "# Scriptorium — шесть проверок авторского ритма (исследовательский эксперимент)",
        "",
        "> По две заранее выбранные измеренные русские книги каждого из трёх авторов. "
        "Это внутренняя стресс-проверка, а не классификатор, независимая внешняя валидация, "
        "доверительный интервал или соответствие FantLab. M2: 0/5; M3: открыт.",
        "",
        "В каждом из шести прогонов исключаем проверяемую книгу из обучающих центров "
        "всех трёх авторов (1 оставшаяся книга своего автора, 2 книги каждого другого). "
        "Расстояния — средние восьми равновесных безразмерных величин: "
        "2 × |значение − центр| / (значение + центр), оба нуля → 0. "
        "Меньше — ближе, но это не вероятность и не оценка устойчивости авторства.",
        "",
        "| Исключённая книга | Известный автор | До Грина | До Толстого | До Достоевского | Ближе к |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for fold in folds:
        known, closest = fold.get("known_author_id"), fold.get("nearest_author_id")
        if known not in names or (closest is not None and closest not in names):
            raise ValueError("unknown author in holdout report")
        distances = fold.get("relative_distances")
        if not isinstance(distances, dict) or set(distances) != set(author_ids):
            raise ValueError("incomplete holdout distances")
        values = [_finite(distances[aid]) for aid in author_ids]
        lines.append(
            "| " + source._markdown_cell(fold.get("held_out_work_title"))
            + " | " + source._markdown_cell(names[known])
            + " | " + " | ".join(f"{value:.6f}" for value in values)
            + " | " + (source._markdown_cell(names[closest]) if closest is not None else "равенство")
            + " |"
        )
    correct = summary.get("nearer_to_labelled_author")
    other = summary.get("nearer_to_other_author")
    ties = summary.get("ties")
    if (any(type(v) is not int or v < 0 for v in (correct, other, ties))
            or correct + other + ties != 6):
        raise ValueError("invalid holdout summary")
    lines += [
        "",
        f"**Ближе к известному автору: {correct} из 6; "
        f"к другому: {other}; ничьи: {ties}.**",
        "",
        "Маленькая заранее выбранная выборка (по две книги на автора) не даёт "
        "оценки обобщения на новые произведения или переводчиков. Нельзя "
        "выбирать признаки по этим шести же книгам и затем называть результат "
        "независимой проверкой. М3 остаётся открыт; исходные тексты не читаются.",
        "",
    ]
    return "\n".join(lines)

def render_markdown(result: Mapping[str, object]) -> str:
    if result.get("schema_version") == EXTENDED_VERSION:
        return _render_extended_markdown(result)
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
