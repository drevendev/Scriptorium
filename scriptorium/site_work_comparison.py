"""Canonical, source-free comparison route for two exact frozen full works.

A registered page reuses the installed pinned offline gallery; it never reads
manuscripts, discovers artifacts, or promotes diagnostic metrics to parity.
"""
from __future__ import annotations

from decimal import Decimal
from html import escape
import json
from pathlib import Path
from typing import Any

from . import full_work_gallery as gallery
from .metric_labels import METRIC_LABELS_RU

SLUG = "two-full-work-differences"
TITLE = "Running on Waves × The Children of Captain Grant — measured differences"
SOURCE_PATHS = tuple(
    "corpus/candidates/diagnostics/" + candidate + ".json"
    for candidate, *_ in gallery.SOURCES
)
EXPECTED_ENTRY: dict[str, Any] = {
    "entry_id": "grin-verne-frozen-work-comparison-v1",
    "kind": "work_comparison",
    "slug": SLUG,
    "title": TITLE,
    "artifact_paths": list(SOURCE_PATHS),
    "artifact_schema": "scriptorium-full-work-gallery-v1",
    "publication_status": "diagnostic",
    "benchmark_admissibility": "diagnostic_only",
    "corpus_admissibility": "not_admissible",
    "compatibility_claim": "inferred",
    "source_text_included": False,
}


class ComparisonBuildError(ValueError):
    """Refuse unregistered, drifted or unsafe comparative evidence."""



# Display-only Russian labels. Metric IDs, numerical values, schemas and CSV/JSON
# are unchanged; the independent gallery HTML remains in its original language.
_RU_UNITS = {
    "characters": "символов",
    "words": "слов",
    "characters/word": "символов на слово",
    "characters/sentence": "символов на предложение",
    "%": "%",
    "types": "словоформ",
    "per 1,000 words": "на 1 000 слов",
    "percentage points": "п. п.",
}
_RU_COPY = (
    ("<html lang='en'>", "<html lang='ru'>"),
    ("<title>Scriptorium — Two analyzed works</title>",
     "<title>Scriptorium — сравнение двух измеренных книг</title>"),
    ("<a class='skip' href='#main'>Skip to content</a>",
     "<a class='skip' href='#main'>К содержанию</a>"),
    ("<p class='eyebrow'>Scriptorium / Literary measurement</p>",
     "<p class='eyebrow'>Scriptorium / Измерение литературного языка</p>"),
    ("<h1>Two books. Different rhythms.</h1>",
     "<h1>Две книги. Разный ритм.</h1>"),
    ("<p class='lede'>Real source-free measurements from two frozen full works. "
     "These are Scriptorium-side observations, not proven FantLab parity.</p>",
     "<p class='lede'>Реальные измерения двух закреплённых полных произведений "
     "без публикации исходных текстов. Совпадение с FantLab не доказано.</p>"),
    ("<a href='#comparison'>See the comparison ↓</a>",
     "<a href='#comparison'>К сравнению ↓</a>"),
    ("<strong>Scientific boundary: M2 0/5.</strong> Both works exceed 300,000 characters, "
     "but FantLab analyzer-input identity is unknown. The Verne entry is the distinct "
     "Beketova translation. No manuscript text is present.",
     "<strong>Научная граница: M2 — 0/5.</strong> Оба произведения превышают "
     "300 000 символов с пробелами, но исходный текст, использованный FantLab, "
     "неизвестен. Текст Верна — отдельная редакция перевода А. А. Бекетовой. "
     "Сами произведения здесь не опубликованы."),
    ("<h2 id='works'>The works</h2>", "<h2 id='works'>Произведения</h2>"),
    ("<h2 id='comparison'>Compare the language</h2>",
     "<h2 id='comparison'>Сравнение языка</h2>"),
    ("<p>Seven normalized measures, scaled separately within each row. "
     "Bar lengths cannot be compared across measures.</p>",
     "<p>Семь относительных и средних показателей. Полосы масштабируются "
     "отдельно в каждой строке: сравнивать длины полос между показателями нельзя.</p>"),
    ("<h2 id='values'>Exact numbers</h2>",
     "<h2 id='values'>Точные значения</h2>"),
    ("<p>Absolute counts are not style scores. "
     "Values retain their inferred or diagnostic scientific status.</p>",
     "<p>Абсолютные количества — не оценки стиля. Показатели остаются "
     "предположительными или диагностическими, а не проверенным паритетом.</p>"),
    ("aria-label='Exact metrics comparison'",
     "aria-label='Точные сравнительные значения'"),
    ("<caption>Ten shared metrics and their units</caption>",
     "<caption>Десять общих показателей с единицами измерения</caption>"),
    ("<th scope='col'>Metric</th>", "<th scope='col'>Показатель</th>"),
    ("<th scope='col'>Running on Waves</th>",
     "<th scope='col'>«Бегущая по волнам»</th>"),
    ("<th scope='col'>Children of Captain Grant · Beketova</th>",
     "<th scope='col'>«Дети капитана Гранта» · Бекетова</th>"),
    ("<h2>Running on Waves</h2>", "<h2>«Бегущая по волнам»</h2>"),
    ("<h2>The Children of Captain Grant</h2>",
     "<h2>«Дети капитана Гранта»</h2>"),
    ("<p>Alexander Grin</p>", "<p>Александр Грин</p>"),
    ("<p>Jules Verne · Alexandra Beketova translation</p>",
     "<p>Жюль Верн · перевод А. А. Бекетовой</p>"),
    ("<p class='eyebrow'>unmatched FantLab diagnostic</p>",
     "<p class='eyebrow'>Сопоставление с FantLab без подтверждённого исходного текста</p>"),
    ("<p class='eyebrow'>Scriptorium-only derived metrics</p>",
     "<p class='eyebrow'>Расчёты Scriptorium, не паритет FantLab</p>"),
    ("<p>Characters including spaces</p>",
     "<p>Символов с пробелами</p>"),
    ("<summary>Inspect source identity</summary>",
     "<summary>Идентичность источника и контрольные суммы</summary>"),
    ("Literary body SHA-256:", "SHA-256 текста произведения:"),
    ("Frozen JSON SHA-256:", "SHA-256 закреплённого JSON:"),
    ("<span>Grin</span>", "<span>Грин</span>"),
    ("<span>Verne</span>", "<span>Верн</span>"),
    ("<h2 id='signed-differences'>Observed differences</h2>",
     "<h2 id='signed-differences'>Измеренные различия</h2>"),
    ("Verne minus Grin (right minus left), calculated from the exact pinned measurements. "
     "A plus or minus sign gives direction, not literary quality. "
     "Percentages are subtracted in percentage points. "
     "The two books differ in length; these descriptive differences cannot isolate "
     "author or translator effects.",
     "Верн минус Грин (правая книга минус левая) — разность точных закреплённых "
     "измерений. Знак не означает литературное качество; доли вычитаются "
     "в процентных пунктах. Книги существенно отличаются по объёму, поэтому "
     "различия нельзя приписывать отдельно автору или переводчику."),
    ("aria-label='Signed differences across seven rate and mean metrics'",
     "aria-label='Разности семи относительных и средних показателей'"),
    ("<caption>Seven measured rate/mean comparisons and signed deltas</caption>",
     "<caption>Семь измерений с разностями со знаком</caption>"),
    ("<th scope='col'>Grin</th>", "<th scope='col'>Грин</th>"),
    ("<th scope='col'>Verne · Beketova</th>",
     "<th scope='col'>Верн · перевод Бекетовой</th>"),
    ("<th scope='col'>Verne − Grin</th>",
     "<th scope='col'>Верн − Грин</th>"),
    ("aria-label='Reader navigation'", "aria-label='Навигация по результатам'"),
    ("← All published analyses", "← Все опубликованные результаты"),
    ("Download verified values (JSON)", "Скачать измерения (JSON)"),
    ("Download metric table (CSV)", "Скачать таблицу метрик (CSV)"),
    (" · offline · no tracking · M2 0/5",
     " · без сети · без отслеживания · M2 0/5"),
)


def _russian_reader_html(page: str) -> str:
    """Localize only this pinned comparison route; refuse silent template drift."""
    for metric_id, english_label, unit, normalized in gallery.METRICS:
        russian_label = METRIC_LABELS_RU.get(metric_id)
        russian_unit = _RU_UNITS.get(unit)
        if not russian_label or not russian_unit:
            raise ComparisonBuildError("Russian metric label or unit missing")
        for tag, count in (("<th scope='row'>", 2 if normalized else 1),
                           ("<h3>", 1 if normalized else 0)):
            source = f"{tag}{escape(english_label)} <small>{escape(unit)}</small>"
            if page.count(source) != count:
                raise ComparisonBuildError("frozen comparison metric markup drift")
            if count:
                page = page.replace(
                    source,
                    f"{tag}{escape(russian_label)} <small>{escape(russian_unit)}</small>",
                )
    for english, russian in _RU_COPY:
        if english not in page:
            raise ComparisonBuildError("frozen comparison language markup drift")
        page = page.replace(english, russian)
    return page


def validate_entry(entry: object) -> None:
    """Only the exact reviewed pair and scientific boundaries may be published."""
    if not isinstance(entry, dict) or entry != EXPECTED_ENTRY:
        raise ComparisonBuildError("unrecognized frozen-work comparison registration")


def _decimal_delta(a: int | float, b: int | float) -> str:
    return format(Decimal(str(b)) - Decimal(str(a)), "f")


def _render_signed_differences(measurements: list[dict[str, Any]]) -> str:
    """Expose only rate/mean deltas from the pinned source-free comparison."""
    rows = []
    for item in measurements:
        if not item["normalized_for_visual_comparison"]:
            continue
        delta = item["right_minus_left_decimal"]
        signed_delta = ("+" if Decimal(delta) > 0 else "") + delta
        rows.append(
            f"<tr data-metric-id='{escape(item['metric_id'], quote=True)}'>"
            f"<th scope='row'>{escape(item['label'])} "
            f"<small>{escape(item['unit'])}</small></th>"
            f"<td>{escape(str(item['left']))}</td>"
            f"<td>{escape(str(item['right']))}</td>"
            f"<td>{escape(signed_delta)} {escape(_RU_UNITS[item['difference_unit']])}</td></tr>"
        )
    if len(rows) != 7:
        raise ComparisonBuildError("unexpected comparable metric count")
    return (
        "<section aria-labelledby='signed-differences'>"
        "<h2 id='signed-differences'>Observed differences</h2>"
        "<p>Verne minus Grin (right minus left), calculated from the exact pinned "
        "measurements. A plus or minus sign gives direction, not literary quality. "
        "Percentages are subtracted in percentage points. The two books differ in "
        "length; these descriptive differences cannot isolate author or translator effects.</p>"
        "<div class='scroll' tabindex='0' role='region' "
        "aria-label='Signed differences across seven rate and mean metrics'>"
        "<table><caption>Seven measured rate/mean comparisons and signed deltas</caption>"
        "<thead><tr><th scope='col'>Metric</th><th scope='col'>Grin</th>"
        "<th scope='col'>Verne · Beketova</th><th scope='col'>Verne − Grin</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div></section>"
    )


def build(root: Path) -> dict[str, Any]:
    """Generate deterministic HTML/CSV/JSON in memory before site publication."""
    try:
        records = gallery.load_gallery(root)
    except (gallery.GalleryError, OSError, UnicodeError, ValueError,
            TypeError, KeyError, AttributeError) as exc:
        raise ComparisonBuildError("frozen comparison evidence is missing or incompatible") from exc
    if len(records) != 2 or tuple(record["id"] for record in records) != tuple(
        candidate for candidate, *_ in gallery.SOURCES
    ):
        raise ComparisonBuildError("frozen comparison source identity drift")

    measurements = []
    for metric_id, label, unit, normalized in gallery.METRICS:
        left, right = (record["values"][metric_id] for record in records)
        measurements.append({
            "metric_id": metric_id,
            "label": label,
            "unit": unit,
            "left": left,
            "right": right,
            "right_minus_left_decimal": _decimal_delta(left, right),
            "difference_unit": "percentage points" if unit == "%" else unit,
            "normalized_for_visual_comparison": normalized,
            "compatibility_status": "diagnostic_or_inferred_not_parity",
        })

    result = {
        "schema_version": "scriptorium-work-comparison-export-v1",
        "profile": gallery.PROFILE,
        "comparison_direction": "right_minus_left",
        "scientific_boundary": {
            "fantlab_analyzer_input_identity": "unknown",
            "m2_parity_admissible": False,
            "m2_weight": 0,
            "note": "Source-unmatched descriptive comparison; not FantLab parity or an author profile.",
        },
        "works": [
            {
                "candidate_id": record["id"],
                "title": record["title"],
                "author_or_translator": record["author"],
                "characters_including_spaces": record["body"],
                "body_sha256": record["body_hash"],
                "derived_json_sha256": record["json_hash"],
                "evidence": record["evidence"],
            }
            for record in records
        ],
        "measurement_profiles": dict(zip(
            ("metrics", "normalization", "dialogue", "vocabulary", "punctuation"),
            records[0]["profiles"],
        )),
        "measurements": measurements,
    }
    try:
        json_text = json.dumps(result, ensure_ascii=False, indent=2,
                               sort_keys=True, allow_nan=False) + "\n"
        csv_text = gallery.render_csv(records)
        html_text = gallery.render_html(records)
        delta_section = _render_signed_differences(measurements)
    except (gallery.GalleryError, ValueError, TypeError, KeyError, ArithmeticError) as exc:
        raise ComparisonBuildError("frozen comparison export failed validation") from exc
    marker = "<main id='main' class='wrap'>"
    values_marker = "<section aria-labelledby='values'>"
    if (html_text.count(marker) != 1 or html_text.count("</header>") != 1 or
            html_text.count(values_marker) != 1):
        raise ComparisonBuildError("gallery HTML integration markers drifted")
    html_text = html_text.replace(
        marker,
        marker + "<nav aria-label='Reader navigation'>"
        "<a href='../../'>← All published analyses</a></nav>",
        1,
    ).replace(
        "</header>",
        "<p class='actions'><a href='measurements.json' download>"
        "Download verified values (JSON)</a> · "
        "<a href='measurements.csv' download>Download metric table (CSV)"
        "</a></p></header>",
        1,
    ).replace(values_marker, delta_section + values_marker, 1)
    html_text = _russian_reader_html(html_text)
    return {
        "html": html_text,
        "json": json_text,
        "csv": csv_text,
        "input_artifacts": [
            {"path": source_path, "sha256": record["json_hash"]}
            for source_path, record in zip(SOURCE_PATHS, records)
        ],
    }
