"""Feature-removal sensitivity on four pinned Russian editions (exploratory only).

Eight independent seven-feature reruns of the existing leave-one-book-out
experiment. No manuscript prose or user-supplied text is loaded.
A change in the number of nearer-to-labelled books is NOT a model-selection
criterion, significance test, classifier accuracy, FantLab parity, or M3 evidence.
"""
from __future__ import annotations

from collections.abc import Mapping
from math import fsum

from . import voice_holdout, voice_profile

VERSION = "scriptorium-author-rhythm-feature-ablation-v1"


def build_ablation(preview: Mapping[str, object]) -> dict[str, object]:
    """Exclude one of the eight features at a time, preserving all four folds.

    The existing holdout builder validates scientific boundaries, exact pinned
    editions and metric identities. All seven retained features receive equal
    weight; no fold uses its held-out book in either author's centroid.
    """
    baseline = voice_holdout.build_holdout(preview)
    feature_ids = [feature[0] for feature in voice_profile.FEATURES]
    author_ids = [author[0] for author in voice_profile.AUTHORS]
    observed = {}
    for author in preview["authors"]:
        measurements = {
            metric["id"]: {row["work_key"]: row["value"]
                            for row in metric["per_work"]}
            for metric in author["metrics"]
        }
        for work in author["works"]:
            key = work["key"]
            observed[key] = {
                "author_id": author["author_id"],
                "word_weight": work["word_weight"],
                "values": {fid: measurements[fid][key] for fid in feature_ids},
            }

    # Check that this independent feature-level reconstruction is consistent
    # with the existing all-eight-feature holdout; never silently diverge.
    contributions = {}
    for fold in baseline["folds"]:
        held_key = fold["held_out_work_key"]
        held = observed[held_key]
        contributions[held_key] = {}
        for author_id in author_ids:
            training_keys = fold["training_work_keys"][author_id]
            training = [observed[key] for key in training_keys]
            denominator_weight = sum(row["word_weight"] for row in training)
            errors = {}
            for metric_id in feature_ids:
                centroid = fsum(
                    row["word_weight"] * row["values"][metric_id]
                    for row in training
                ) / denominator_weight
                value = held["values"][metric_id]
                denominator = value + centroid
                errors[metric_id] = (
                    0.0 if denominator == 0
                    else 2 * abs(value - centroid) / denominator
                )
            full_distance = fsum(errors.values()) / len(feature_ids)
            if abs(full_distance - fold["relative_distances"][author_id]) > 0.0000006:
                raise ValueError("holdout and feature sensitivity calculations diverged")
            contributions[held_key][author_id] = errors

    ablations = []
    for omitted_id, label, unit in voice_profile.FEATURES:
        remaining = [fid for fid in feature_ids if fid != omitted_id]
        folds = []
        for baseline_fold in baseline["folds"]:
            held_key = baseline_fold["held_out_work_key"]
            distances = {
                aid: fsum(contributions[held_key][aid][fid] for fid in remaining)
                     / len(remaining)
                for aid in author_ids
            }
            if abs(distances[author_ids[0]] - distances[author_ids[1]]) < 1e-12:
                closest = None
            else:
                closest = min(author_ids, key=lambda aid: distances[aid])
            folds.append({
                "held_out_work_key": held_key,
                "known_author_id": baseline_fold["known_author_id"],
                "relative_distances": {
                    aid: round(distances[aid], 6) for aid in author_ids
                },
                "nearest_author_id": closest,
                "nearer_to_labelled_author": (
                    None if closest is None
                    else closest == baseline_fold["known_author_id"]
                ),
                "nearest_changed_from_eight_features": (
                    closest != baseline_fold["nearest_author_id"]
                ),
            })
        ablations.append({
            "omitted_feature_id": omitted_id,
            "omitted_feature_label": label,
            "omitted_feature_unit": unit,
            "retained_features": remaining,
            "summary": {
                "nearer_to_labelled_author": sum(
                    row["nearer_to_labelled_author"] is True for row in folds),
                "nearer_to_other_author": sum(
                    row["nearer_to_labelled_author"] is False for row in folds),
                "ties": sum(row["nearer_to_labelled_author"] is None for row in folds),
                "changed_nearest": sum(
                    row["nearest_changed_from_eight_features"] for row in folds),
            },
            "folds": folds,
        })

    return {
        "schema_version": VERSION,
        "source_preview_version": voice_profile.VERSION,
        "source_holdout_version": voice_holdout.VERSION,
        "source_snapshot_git_blob_sha1": baseline["source_snapshot_git_blob_sha1"],
        "method": {
            "baseline_features": feature_ids,
            "omitted_features_per_run": 1,
            "retained_features_per_run": len(feature_ids) - 1,
            "unchanged_folds": 4,
            "feature_distance": baseline["method"]["feature_distance"],
            "aggregation": "mean_of_seven_equal_weight_feature_distances",
            "unchanged_word_weighted_training": True,
            "distance_is_not_probability": True,
        },
        "baseline_summary": baseline["summary"],
        "ablations": ablations,
        "scientific_boundary": {
            "class": "exploratory_within_sample_feature_removal_sensitivity",
            "does_not_select_features": True,
            "independent_external_validation": False,
            "m2_source_matched": 0,
            "m3_accepted": False,
            "no_fantlab_parity_claim": True,
            "no_source_text_committed": True,
        },
    }


def render_markdown(result: Mapping[str, object]) -> str:
    if (result.get("schema_version") != VERSION
            or result.get("scientific_boundary", {}).get("m3_accepted") is not False
            or result.get("scientific_boundary", {}).get("independent_external_validation") is not False
            or result.get("scientific_boundary", {}).get("does_not_select_features") is not True):
        raise ValueError("unverified ablation scientific boundary")
    baseline = result["baseline_summary"]
    lines = [
        "# Scriptorium — чувствительность к удалению одного показателя",
        "",
        "> Восемь диагностических пересчётов на тех же четырёх книгах Грина и Толстого. "
        "Это не подбор признаков, независимая проверка, классификатор, "
        "статистическая значимость или паритет с FantLab. M2: 0/5; M3: открыт.",
        "",
        "В каждой строке убирается ровно один из восьми показателей. Остальные семь "
        "сравниваются с теми же авторскими центрами, пересчитанными без "
        "исключённой книги. Все семь признаков имеют равный вес; "
        "меньшее безразмерное расстояние означает большую близость, "
        "но не вероятность.",
        "",
        "**Исходный эксперимент (8 показателей): "
        + str(baseline["nearer_to_labelled_author"]) + " из 4 книг ближе к своему автору.**",
        "",
        "| Убранный показатель | Ближе к своему автору | К другому | Ничья | Изменён ближайший автор |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in result["ablations"]:
        summary = row["summary"]
        lines.append(
            "| " + voice_profile._markdown_cell(row["omitted_feature_label"])
            + " | " + str(summary["nearer_to_labelled_author"]) + " из 4"
            + " | " + str(summary["nearer_to_other_author"])
            + " | " + str(summary["ties"])
            + " | " + str(summary["changed_nearest"]) + " |"
        )
    lines += [
        "",
        "Любое изменение после исключения признака показывает чувствительность "
        "этой конкретной выборки, **не улучшение классификатора**. Выбирать "
        "признаки по этим же четырём книгам означало бы подгонку. "
        "Только независимо собранные произведения и авторы смогут проверить "
        "переносимость результата.",
        "",
        "Источник: закреплённый JSON четырёх измеренных редакций; Git blob "
        + voice_profile._markdown_cell(result["source_snapshot_git_blob_sha1"])
        + ". Исходные литературные тексты не читаются и не публикуются.",
        "",
    ]
    return "\n".join(lines)
