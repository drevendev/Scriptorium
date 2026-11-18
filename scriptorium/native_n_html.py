"""Accessible, source-free HTML rendering for retained native AOT N uncertainty.

The caller validates an exact pinned native witness first. This renderer never
recovers raw text, asserts noun/cardinal assignments, or claims FantLab parity.
"""
from __future__ import annotations

from html import escape


def render_native_n_html(report: dict[str, object]) -> str:
    """Render a validated source-free diagnostic as a self-contained HTML page."""
    witness = report["witness"]
    counts = witness["counts"]
    evidence = witness["evidence"]
    rates = report["rates"]
    units = report["conditional_units"]

    def cell(value: object) -> str:
        return escape(str(value), quote=True)

    def table(caption: str, headers: tuple[str, ...], rows: list[tuple[object, ...]]) -> str:
        head = "".join(f'<th scope="col">{cell(name)}</th>' for name in headers)
        body = "".join("<tr>" + "".join(
            f'<th scope="row">{cell(value)}</th>' if index == 0 else f'<td>{cell(value)}</td>'
            for index, value in enumerate(row)) + "</tr>" for row in rows)
        return (f'<div class="scroll" role="region" tabindex="0" aria-label="{cell(caption)}">'
                f'<table><caption>{cell(caption)}</caption><thead><tr>{head}</tr></thead>'
                f'<tbody>{body}</tbody></table></div>')

    observed = table("Наблюдения pylem · счётчики",
                     ("Категория", "Значение", "Единица"), [
        ("Всего слов", counts["word_count"], "слов-токенов"),
        ("Всего предложений", counts["sentence_count"], "предложений"),
        ("Однозначно определено в базовой модели", counts["baseline_defined"], "слов-токенов"),
        ("Только N", counts["n_only"], "слов-токенов"),
        ("N вместе с другими метками (исключено)", counts["n_mixed_excluded"], "слов-токенов"),
        ("Определено при условном распределении только N", counts["conditional_defined"], "слов-токенов"),
        ("Только N · доля", f'{rates["n_only_percent_of_words"]:.2f}', "% слов-токенов"),
        ("N смешанное · исключено", f'{rates["n_mixed_excluded_percent_of_words"]:.2f}', "% слов-токенов"),
        ("Любая метка N", f'{rates["n_candidate_percent_of_words"]:.2f}', "% слов-токенов"),
    ])

    buckets = table("Условные границы для классов слов",
                    ("Класс", "Минимум", "Максимум", "Мин. %", "Макс. %", "Нормировка"), [
        (key, bounds[0], bounds[1],
         f'{units["bucket_percent_of_conditional_defined"][key][0]:.6f}',
         f'{units["bucket_percent_of_conditional_defined"][key][1]:.6f}',
         "% условно определённых слов")
        for key, bounds in witness["bucket_bounds"].items()
    ])

    bigrams = table("Условные интервалы POS-биграмм",
                    ("Пара", "Мин.", "Макс.", "Независимый верх", "Мин. /1000", "Макс. /1000", "Единицы"), [
        (f'{pair["first"]} → {pair["second"]}', pair["min"], pair["max"],
         pair["independent_edge_upper"], f'{scaled["min"]:.6f}', f'{scaled["max"]:.6f}',
         "на 1000 слов-токенов")
        for pair, scaled in zip(witness["bigram_bounds"], units["bigram_per_1000_word_tokens"])
    ])

    positions = table("Условные интервалы позиций в предложении",
                      ("Позиция", "Мин.", "Макс.", "Мин. %", "Макс. %", "Нормировка"), [
        (row["position"], row["min"], row["max"],
         f'{scaled["min"]:.6f}', f'{scaled["max"]:.6f}', "% всех предложений")
        for row, scaled in zip(witness["sentence_position_bounds"],
                               units["sentence_position_percent_of_all_sentences"])
    ])

    controls = table("Малые нативные контрольные примеры",
                     ("Аннотация", "Только N", "Примеров", "% примеров"), [
        (name, group["n_only"], group["token_count"],
         "НЕ ВЫЧИСЛЕНО" if units["native_control_n_only_percent_of_annotated_examples"][name] is None
         else f'{units["native_control_n_only_percent_of_annotated_examples"][name]:.6f}')
        for name, group in witness["native_controls"].items()
    ])

    title = cell(witness["work"]["title"])
    digest = cell(evidence["runtime_analysis_sha256"])
    version = cell(evidence["pylem_version"])
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Scriptorium · неопределённость N · {title}</title>
<style>
:root{{color-scheme:light dark;font-family:system-ui,-apple-system,Segoe UI,sans-serif;line-height:1.6}}
body{{max-width:75rem;margin:auto;padding:clamp(1rem,3vw,2.5rem);background:Canvas;color:CanvasText}}
header{{border-bottom:3px solid #789b83;padding-bottom:1rem;margin-bottom:2rem}}
h1,h2{{line-height:1.25}}h1{{font-family:Georgia,serif;font-size:clamp(1.65rem,4vw,2.8rem)}}
.lede{{max-width:74ch}}.warning{{padding:1rem;border-inline-start:5px solid #bd8633;background:color-mix(in srgb,CanvasText 5%,Canvas)}}
section{{margin:2rem 0}}.scroll{{overflow-x:auto;max-width:100%;border:1px solid GrayText;border-radius:.4rem}}
.scroll:focus-visible{{outline:3px solid Highlight;outline-offset:3px}}
table{{border-collapse:collapse;width:100%;min-width:44rem;font-variant-numeric:tabular-nums;font-size:.9rem}}
caption{{text-align:start;font-weight:700;padding:.8rem}}th,td{{text-align:start;padding:.65rem .8rem;border-top:1px solid GrayText}}
thead{{background:color-mix(in srgb,CanvasText 7%,Canvas)}}tbody tr:nth-child(even){{background:color-mix(in srgb,CanvasText 4%,Canvas)}}
th[scope=row]{{font-weight:650}}small{{overflow-wrap:anywhere}}a:focus-visible{{outline:3px solid Highlight}}
@media print{{body{{max-width:none;padding:0}}.scroll{{overflow:visible}}table{{min-width:0;font-size:8pt}}section{{break-inside:avoid}}}}
</style></head><body>
<header><p>Scriptorium / исследовательский отчёт / только производные данные</p>
<h1>Неопределённость N · {title}</h1>
<p class="lede">Зафиксированное наблюдение AOT-lineage pylem {version}. Формирование HTML не запускает морфологический анализ заново и не использует рукопись.</p></header>
<p class="warning"><strong>Только диагностика · M2: 0/5.</strong> N не идентифицирует существительное или числительное.
Неизвестны тождество словаря FantLab и алгоритм выбора омонимов. N со смешанными метками исключено из условных интервалов. Неизвестное не является нулём.</p>
<section aria-labelledby="observed"><h2 id="observed">Измеренные счётчики</h2>{observed}</section>
<section aria-labelledby="buckets"><h2 id="buckets">Условные POS-классы</h2><p>Границы по только-N; доли относятся к условно определённым словам. Это не наблюдаемые частоты существительных или числительных.</p>{buckets}</section>
<section aria-labelledby="bigrams"><h2 id="bigrams">Соседние POS-пары</h2><p>Минимум и максимум получены с согласованными назначениями внутри одной пары соседних позиций. Независимая верхняя оценка заведомо более свободна; максимумы разных строк нельзя суммировать.</p>{bigrams}</section>
<section aria-labelledby="positions"><h2 id="positions">Начало предложения</h2><p>Доли нормированы по всем предложениям, а не по числу условно размеченных слов.</p>{positions}</section>
<section aria-labelledby="controls"><h2 id="controls">Нативные контрольные примеры</h2><p>Аннотации отражают роли специально подобранных лексем. Малый объём не позволяет оценивать точность классификатора или частоты корпуса.</p>{controls}</section>
<footer><p>Версия pylem: {version}. SHA-256 зафиксированного результата: <small>{digest}</small>.</p>
<p>Интервалы для отдельных ячеек не образуют совместно достижимого вектора. Шесть знаков после запятой — точность отображения, не правило округления FantLab. Исходный текст не включён.</p></footer>
</body></html>
'''
