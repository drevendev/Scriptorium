"""Pinned, source-free measurements of Alexandra A. Beketova's Russian translation.

This Reader route reuses the already-reviewed 11-field Wikisource diagnostic.
It does not infer values for the French original or claim FantLab parity.
"""
from __future__ import annotations

import csv
from hashlib import sha256
from html import escape
import io
import json
import math
from pathlib import Path

from . import full_work_gallery as gallery

CANDIDATE_ID = "verne-children-captain-grant-beketova-ru"
ARTIFACT_PATH = "corpus/candidates/diagnostics/" + CANDIDATE_ID + ".json"
ARTIFACT_GIT_BLOB_SHA1 = "140823b70e9ac28a5fc24b402e75f3e83bf5bb8f"
BODY_SHA256 = "4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161"
SLUG = "captain-grant-beketova-measured"
TITLE = "Дети капитана Гранта — перевод А. А. Бекетовой"
REPORT_PROFILE = "scriptorium-beketova-measured-reader-v1"
EXPECTED_PROFILES = (
    "scriptorium-metrics-v4", "scriptorium-text-v1",
    "scriptorium-dialogue-v1", "scriptorium-vocabulary-v1",
    "scriptorium-punctuation-v2",
)
EXPECTED_ENTRY = {
    "entry_id": "verne-beketova-retained-reader-v1",
    "kind": "measured_diagnostic",
    "slug": SLUG,
    "title": TITLE,
    "artifact_paths": [ARTIFACT_PATH],
    "artifact_schema": REPORT_PROFILE,
    "publication_status": "diagnostic",
    "benchmark_admissibility": "diagnostic_only",
    "corpus_admissibility": "not_admissible",
    "compatibility_claim": "inferred",
    "source_text_included": False,
}
# Shared human-facing metric definitions live in the already-pinned gallery.
# The extra sentence count is a Scriptorium extension, not a FantLab field.
METRICS = gallery.METRICS[:2] + (
    ("scriptorium.general.sentences", "Sentence candidates", "sentences", False),
) + gallery.METRICS[2:]


class BeketovaBuildError(ValueError):
    """Refuse any unreviewed translation evidence or scientific status upgrade."""


def validate_entry(entry: object) -> None:
    if type(entry) is not dict or entry != EXPECTED_ENTRY:
        raise BeketovaBuildError("unrecognized Beketova measurement registration")


def _verified_record(root: Path) -> dict:
    # The gallery checks the precise Git blob, disallows symlinks, duplicate keys,
    # nonfinite readings, incompatible units, and false parity declarations.
    try:
        record = gallery._load(root, 1)
    except (gallery.GalleryError, OSError, UnicodeError, ValueError,
            KeyError, TypeError) as exc:
        raise BeketovaBuildError("pinned Beketova source-free evidence invalid") from exc
    values = record["values"]
    if (
        record["id"] != CANDIDATE_ID
        or record["body"] != 1_095_467
        or record["body_hash"] != BODY_SHA256
        or record["profiles"] != EXPECTED_PROFILES
        or type(values) is not dict
        or set(values) != {metric_id for metric_id, *_ in METRICS}
        or values["fantlab.general.words"] != 158_881
        or values["scriptorium.general.sentences"] != 14_568
        or any(type(value) not in (int, float) or not math.isfinite(value) or value < 0
               for value in values.values())
        or type(values["scriptorium.general.sentences"]) is not int
    ):
        raise BeketovaBuildError("Beketova body, field set or metric profiles drifted")
    return record


def build(root: Path) -> dict[str, str]:
    record = _verified_record(root)
    rows = []
    html_rows = []
    csv_file = io.StringIO(newline="")
    writer = csv.writer(csv_file, lineterminator="\n")
    writer.writerow(("metric_id", "value", "source_unit", "compatibility_status",
                     "fantlab_reference", "source_body_sha256"))
    for metric_id, label, display_unit, _ in METRICS:
        value = record["values"][metric_id]
        status = "extension" if metric_id.startswith("scriptorium.") else "inferred"
        unit = ("sentences" if display_unit == "sentences"
                else gallery._SOURCE_UNIT_BY_DISPLAY_UNIT[display_unit])
        row = {
            "metric_id": metric_id, "label": label, "value": value,
            "unit": unit, "compatibility_status": status,
            "fantlab_reference": None,
        }
        rows.append(row)
        writer.writerow((metric_id, str(value), unit, status, "UNKNOWN", BODY_SHA256))
        html_rows.append(
            '<tr><th scope="row"><code>' + escape(metric_id) + '</code>'
            '<span class="eyebrow">' + escape(label) + '</span></th>'
            '<td>' + escape(str(value)) + '</td>'
            '<td>' + escape(unit) + '</td>'
            '<td>' + escape(status) + '</td>'
            '<td>UNKNOWN</td></tr>'
        )
    data = {
        "schema_version": REPORT_PROFILE,
        "candidate_id": CANDIDATE_ID,
        "work": "Les Enfants du capitaine Grant",
        "author": "Jules Verne",
        "analysis_language": "ru",
        "original_language": "fr",
        "translator": "Alexandra A. Beketova",
        "translation_identity": "Alexandra A. Beketova Russian translation",
        "wikisource_revision_id": 5304880,
        "source_text_committed": False,
        "frozen_body_characters_including_spaces": record["body"],
        "frozen_body_sha256": BODY_SHA256,
        "retained_git_blob_sha1": ARTIFACT_GIT_BLOB_SHA1,
        "derived_artifact_sha256": record["json_hash"],
        "analysis_profiles": list(record["profiles"]),
        "fantlab_comparison_performed": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
        "metrics": rows,
    }
    body = (
        '<main id="main-content" tabindex="-1"><nav aria-label="Breadcrumb">'
        '<a href="../../">← К каталогу произведений</a></nav>'
        '<p class="eyebrow">Русский перевод · 11 измеренных показателей</p>'
        '<h1 lang="ru">Дети капитана Гранта</h1>'
        '<p class="lede" lang="ru">Жюль Верн · перевод А. А. Бекетовой</p>'
        '<p class="notice" lang="ru"><strong>Граница достоверности.</strong> '
        'Все 11 значений вычислены для закреплённого русского перевода. '
        'Оригинальный французский текст здесь не анализировался. '
        'Сопоставление с FantLab не проводилось, идентичность входного текста '
        'FantLab неизвестна; соответствие M2: <strong>0/5</strong>. '
        'Неизмеренные показатели не заменяются нулями. Текст книги не публикуется.</p>'
        '<p class="actions"><a href="measurements.json" download>JSON · 11 показателей</a>'
        ' · <a href="measurements.csv" download>CSV · таблица значений</a>'
        ' · <a href="../two-full-work-differences/">Сравнить с «Бегущей по волнам»</a></p>'
        '<div class="table-wrap" role="region" tabindex="0" '
        'aria-label="Измерения перевода Бекетовой">'
        '<table><caption>11 результатов Scriptorium: единицы и научный статус</caption>'
        '<thead><tr><th scope="col">Метрика</th><th scope="col">Значение</th>'
        '<th scope="col">Единица</th><th scope="col">Тип</th>'
        '<th scope="col">FantLab</th></tr></thead><tbody>'
        + "".join(html_rows) + '</tbody></table></div>'
        '<h2 lang="ru">Источник и воспроизводимость</h2>'
        '<dl><dt>Язык анализа</dt><dd>Русский перевод; оригинал — французский</dd>'
        '<dt>Закреплённая редакция</dt><dd><a rel="noopener noreferrer" '
        'href="https://ru.wikisource.org/w/index.php?oldid=5304880">'
        'Wikisource oldid 5304880</a></dd>'
        '<dt>Размер корпуса</dt><dd>1 095 467 символов с пробелами</dd>'
        '<dt>SHA-256 исходного литературного тела</dt><dd><code>'
        + BODY_SHA256 + '</code></dd>'
        '<dt>Git blob сохранённых измерений</dt><dd><code>'
        + ARTIFACT_GIT_BLOB_SHA1 + '</code></dd>'
        '<dt>Методика</dt><dd><code>scriptorium-metrics-v4</code>; '
        '<code>scriptorium-text-v1</code>; <code>scriptorium-punctuation-v2</code></dd>'
        '</dl><p class="notice">Это воспроизводимый описательный анализ перевода, '
        'не подтверждение равенства результатов FantLab.</p></main>'
    )
    return {
        "body": body,
        "json": json.dumps(data, ensure_ascii=False, indent=2,
                           sort_keys=True, allow_nan=False) + "\n",
        "csv": csv_file.getvalue(),
        "artifact_sha256": record["json_hash"],
    }
