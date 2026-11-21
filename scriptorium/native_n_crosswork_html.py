"""Standalone source-free literary HTML for the pinned two-work AOT N diagnostic.

The caller must build its report from the byte-pinned witnesses. This presentation
layer also rejects contradictory or malformed measurements before rendering.
"""
from __future__ import annotations

from html import escape
from math import isfinite
import re


_EXPECTED_IDS = ("n_only", "n_mixed", "any_n")
_EXPECTED_SCHEMA = "scriptorium-native-n-crosswork-offline-v1"
_WORK_KEYS = {
    "candidate_id", "title", "word_tokens", "normalized_sha256",
    "runtime_analysis_sha256", "native_workflow",
}


def _esc(value: str) -> str:
    return escape(value, quote=True)


def _number(count: int) -> str:
    return f"{count:,}".replace(",", "\u202f")


def _validate(report: dict[str, object]) -> None:
    if (not isinstance(report, dict)
            or report.get("schema_version") != _EXPECTED_SCHEMA
            or report.get("status") != "diagnostic_only"
            or report.get("source_text_included") is not False
            or report.get("m2_parity_admissible") is not False
            or report.get("measurement")
                != "replay_of_two_independent_pinned_native_receipts_not_new_run"):
        raise ValueError("invalid diagnostic report boundary")
    works = report.get("works")
    rows = report.get("rows")
    if not isinstance(works, list) or len(works) != 2:
        raise ValueError("two native work identities required")
    for work in works:
        if not isinstance(work, dict) or set(work) != _WORK_KEYS:
            raise ValueError("incomplete native source identity")
        if type(work["word_tokens"]) is not int or work["word_tokens"] <= 0:
            raise ValueError("invalid native word denominator")
        for key in ("candidate_id", "title"):
            if not isinstance(work[key], str) or not work[key].strip():
                raise ValueError("blank native source identity")
        for key in ("normalized_sha256", "runtime_analysis_sha256"):
            if not isinstance(work[key], str) or not re.fullmatch(r"[0-9a-f]{64}", work[key]):
                raise ValueError("invalid native digest")
        url = work["native_workflow"]
        if not isinstance(url, str) or not re.fullmatch(
                r"https://github\.com/drevendev/Scriptorium/actions/runs/[0-9]+", url):
            raise ValueError("untrusted native workflow URL")
    if (not isinstance(rows, list) or len(rows) != 3
            or [row.get("measure_id") if isinstance(row, dict) else None
                for row in rows] != list(_EXPECTED_IDS)):
        raise ValueError("missing native N measurement")
    for row in rows:
        if not isinstance(row.get("label_ru"), str) or not row["label_ru"].strip():
            raise ValueError("missing measurement label")
        for prefix, work in (("anna", works[0]), ("resurrection", works[1])):
            count = row.get(prefix + "_count")
            rate = row.get(prefix + "_percent_of_word_tokens")
            if (type(count) is not int or count < 0 or count > work["word_tokens"]
                    or type(rate) not in (int, float) or not isfinite(rate)
                    or abs(rate - count * 100 / work["word_tokens"]) > 1e-9):
                raise ValueError("native count/rate mismatch")
        delta = row.get("resurrection_minus_anna_percentage_points")
        if (type(delta) not in (float, int) or not isfinite(delta)
                or abs(delta - (
                    row["resurrection_percent_of_word_tokens"]
                    - row["anna_percent_of_word_tokens"])) > 1e-9):
            raise ValueError("native signed delta mismatch")
    if any(
        rows[2][prefix + "_count"] != (
            rows[0][prefix + "_count"] + rows[1][prefix + "_count"])
        for prefix in ("anna", "resurrection")
    ):
        raise ValueError("N-only and N-mixed groups must be disjoint")


def render_crosswork_html(report: dict[str, object]) -> str:
    """Build an accessible, printable, offline HTML report without JavaScript."""
    _validate(report)
    left, right = report["works"]

    def metric_cell(count: int, rate: float) -> str:
        # Bar is decorative. The exact unit and rounded percentage stay readable.
        return (
            '<span class="metric"><span class="metric-number">'
            + _number(count) + ' <span class="share">(' + f"{rate:.2f}"
            + '%)</span></span><span class="track" aria-hidden="true">'
            + '<span class="fill" style="width:' + f"{rate:.6f}"
            + '%"></span></span></span>'
        )

    table_rows = []
    for row in report["rows"]:
        table_rows.append(
            '<tr><th scope="row">' + _esc(row["label_ru"]) + '</th>'
            + '<td>' + metric_cell(row["anna_count"], row["anna_percent_of_word_tokens"]) + '</td>'
            + '<td>' + metric_cell(row["resurrection_count"],
                                    row["resurrection_percent_of_word_tokens"]) + '</td>'
            + '<td class="delta">' + f'{row["resurrection_minus_anna_percentage_points"]:+.2f}'
            + ' <span class="unit">п. п.</span></td></tr>'
        )

    provenance = []
    for index, work in enumerate((left, right), start=1):
        provenance.append(
            '<article class="witness"><h3>' + str(index) + '. ' + _esc(work["title"])
            + '</h3><p><code>' + _esc(work["candidate_id"]) + '</code> · '
            + _number(work["word_tokens"]) + ' словоформ</p>'
            + '<dl><dt>Текст · SHA-256</dt><dd><code>'
            + work["normalized_sha256"] + '</code></dd>'
            + '<dt>Нативный анализ · SHA-256</dt><dd><code>'
            + work["runtime_analysis_sha256"] + '</code></dd></dl>'
            + '<p><a href="' + _esc(work["native_workflow"])
            + '" rel="noopener noreferrer">Подтверждение запуска в GitHub Actions</a></p></article>'
        )

    return """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Неопределённость N · две книги Толстого · Scriptorium</title>
<style>
:root{color-scheme:light;--ink:#232b29;--muted:#4a5551;--line:#c9d3cb;--paper:#f5f2e9;--panel:#fffdfa;--accent:#1b665b}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:1rem/1.6 system-ui,-apple-system,sans-serif}
main{max-width:68rem;margin:auto;padding:clamp(1rem,4vw,3.5rem)}h1,h2,h3{font-family:Georgia,"Times New Roman",serif;line-height:1.16;letter-spacing:-.02em}
h1{font-size:clamp(2rem,5vw,3.6rem);max-width:18ch;margin:.35em 0}h2{font-size:clamp(1.5rem,3vw,2rem)}
.eyebrow{font-size:.8rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.lead{max-width:66ch;font-size:1.08rem}.status{border-left:.3rem solid var(--accent);padding:.65rem 1rem;background:var(--panel)}
.table-scroll{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:.65rem}
table{width:100%;min-width:45rem;border-collapse:collapse}caption{text-align:left;padding:1rem;font-weight:650}
th,td{padding:1rem .85rem;text-align:left;vertical-align:middle;border-top:1px solid var(--line)}
thead th{background:#e6eee8;border-top:0}tbody th{width:24%;font-weight:650}
.metric{display:block;min-width:10rem}.metric-number{display:block;white-space:nowrap;font-variant-numeric:tabular-nums}
.share,.unit{color:var(--muted)}.track{display:block;background:#dce7df;height:.4rem;margin-top:.45rem;border-radius:1rem}
.fill{display:block;background:var(--accent);height:100%;border-radius:1rem}.delta{white-space:nowrap;font-weight:700;font-variant-numeric:tabular-nums}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr));gap:1rem}
.witness{background:var(--panel);border:1px solid var(--line);padding:1.2rem;border-radius:.65rem;min-width:0}
.witness h3{font-size:1.3rem;margin:.25rem 0}.witness dl{margin:.8rem 0}
.witness dt{font-size:.88rem;color:var(--muted);margin-top:.65rem}.witness dd{margin:0;overflow-wrap:anywhere}
code{font-size:.84rem;overflow-wrap:anywhere}a{color:#07574f;text-underline-offset:.2em}
a:hover{text-decoration-thickness:.15em}a:focus-visible{outline:.2rem solid var(--accent);outline-offset:.22rem}
footer{margin-top:2rem;padding-top:1rem;border-top:1px solid var(--line);color:var(--muted)}
@media print{body{background:#fff}main{max-width:none;padding:0}.table-scroll{overflow:visible}.witness{break-inside:avoid}a{color:inherit}}
</style>
</head>
<body><main>
<header><p class="eyebrow">Scriptorium · измерения, не оценки</p>
<h1>Одна метка N. Две разные книги.</h1>
<p class="lead">Наблюдаемые кандидаты морфологического анализа AOT/pylem 0.0.18.
Сравнение двух независимо закреплённых измерений, а не новый запуск анализатора.</p>
<p class="status"><strong>Диагностика · M2: 0/5.</strong> Метка N не разделяет
существительные и количественные числительные. Различия книг не показывают
точность определения частей речи и не подтверждают совпадение с FantLab.</p></header>
<section aria-labelledby="results"><h2 id="results">Доли словоформ с N-кандидатами</h2>
<p>В каждой ячейке — число словоформ и доля всех словоформ книги.
Разница «Воскресение» минус «Анна Каренина» измеряется в процентных пунктах.</p>
<div class="table-scroll" role="region" aria-label="Таблица наблюдаемых N-кандидатов" tabindex="0">
<table><caption>Сопоставление двух нативных измерений: целые счётчики и доли</caption>
<thead><tr><th scope="col">Кандидаты</th><th scope="col">Анна Каренина</th>
<th scope="col">Воскресение</th><th scope="col">Разница</th></tr></thead>
<tbody>""" + "".join(table_rows) + """</tbody></table></div>
<p><strong>Как читать:</strong> «Только N» и «Смешанные N» не пересекаются;
«Любой N-кандидат» — их сумма. Полосы лишь повторяют числовые доли в таблице.
Округление до двух знаков предназначено для чтения, а не для проверки FantLab.</p>
</section>
<section aria-labelledby="proof"><h2 id="proof">Проверяемое происхождение</h2>
<p>Файлы исходных произведений здесь не приводятся. Отчёт построен локально
из двух проверенных JSON-свидетельств с точным совпадением Git blob SHA-1,
хешей исходного текста и результатов нативного анализа.</p>
<div class="cards">""" + "".join(provenance) + """</div></section>
<footer>Scriptorium · метод: описательная межкнижная диагностика. Не классификатор
существительных/числительных, не выбор омонимов FantLab, не результат M2.</footer>
</main></body></html>
"""
