"""Reader-first, verified source-free showcase built from frozen comparison evidence.

Presentation-only: these derived diagnostics are not FantLab source-matched parity,
author profiles, a manuscript upload, or independently reproduced results.
"""
from __future__ import annotations

from html import escape
import json
import math
from collections.abc import Mapping, Sequence
from typing import Any


_SHOWCASE_METRICS = (
    ("fantlab.dialogue.share_percent", "Dialogue share", "%"),
    ("fantlab.general.mean_sentence_length_chars", "Mean sentence length", "characters/sentence"),
    ("fantlab.punctuation.comma.per_1000_words", "Commas", "per 1,000 words"),
)


def _safe_measurement(value: object, label: str) -> float:
    if type(value) not in (int, float):
        raise ValueError("showcase measurement is not numeric: " + label)
    number = float(value)
    if not math.isfinite(number) or not 0 <= number <= 1_000_000:
        raise ValueError("showcase measurement outside safe display bounds: " + label)
    return number


def render_demo(entries: Sequence[Mapping[str, Any]]) -> str:
    """Render an optional real-data comparison preview, never synthetic numbers.

    Comparison JSON was already validated by site_work_comparison.build. Verify the
    narrow display contract once more so a changed/partial source cannot silently
    turn a demo into unqualified claims or fabricated metrics.
    """
    comparisons = [e for e in entries if e.get("render_mode") == "comparison"]
    if not comparisons:
        return ""
    if len(comparisons) != 1 or comparisons[0].get("slug") != "two-full-work-differences":
        raise ValueError("unexpected public comparison registration")
    data = comparisons[0].get("json_data")
    if type(data) is not str or len(data) > 1_000_000:
        raise ValueError("showcase comparison JSON unavailable")
    doc = json.loads(data)
    if (type(doc) is not dict
            or doc.get("schema_version") != "scriptorium-work-comparison-export-v1"
            or doc.get("comparison_direction") != "right_minus_left"):
        raise ValueError("unsupported showcase comparison contract")
    boundary = doc.get("scientific_boundary")
    if (type(boundary) is not dict
            or boundary.get("m2_parity_admissible") is not False
            or boundary.get("m2_weight") != 0
            or boundary.get("fantlab_analyzer_input_identity") != "unknown"):
        raise ValueError("unverified showcase scientific boundary")
    works = doc.get("works")
    rows = doc.get("measurements")
    if type(works) is not list or len(works) != 2 or type(rows) is not list:
        raise ValueError("unexpected comparison evidence dimensions")
    if (works[0].get("candidate_id") != "grin-running-on-waves-ru"
            or works[1].get("candidate_id") != "verne-children-captain-grant-beketova-ru"):
        raise ValueError("showcase work identities changed")
    if any(type(w.get("title")) is not str or not w["title"] or len(w["title"]) > 160 for w in works):
        raise ValueError("showcase title not bounded")
    by_id = {row.get("metric_id"): row for row in rows if type(row) is dict}
    if len(by_id) != len(rows):
        raise ValueError("duplicate or invalid showcase metric rows")

    spark_rows = []
    exact_rows = []
    for metric_id, title, unit in _SHOWCASE_METRICS:
        item = by_id.get(metric_id)
        if (type(item) is not dict
                or item.get("unit") != unit
                or item.get("normalized_for_visual_comparison") is not True
                or item.get("compatibility_status") != "diagnostic_or_inferred_not_parity"):
            raise ValueError("showcase metric contract changed")
        first = _safe_measurement(item.get("left"), metric_id)
        second = _safe_measurement(item.get("right"), metric_id)
        if unit == "%" and (first > 100 or second > 100):
            raise ValueError("showcase percentage exceeds 100")
        denominator = max(first, second)
        bars = []
        for short, value, tone in (("Grin", first, "ink"), ("Verne", second, "gold")):
            width = 0.0 if denominator == 0 else value / denominator * 100
            bars.append(
                '<div class="demo-series">'
                f'<span class="demo-series-label">{short}</span>'
                '<span class="demo-track" aria-hidden="true">'
                f'<span class="demo-fill demo-fill-{tone}" style="width:{width:.3f}%"></span>'
                '</span>'
                f'<span class="demo-reading">{value:,.1f}</span>'
                '</div>'
            )
        spark_rows.append(
            '<li class="demo-metric">'
            f'<h3>{escape(title)} <span class="demo-unit">{escape(unit)}</span></h3>'
            + "".join(bars) + '</li>'
        )
        # These strings are complete original numeric observations, not chart rounding.
        exact_rows.append(
            f'<tr><th scope="row">{escape(title)}</th>'
            f'<td>{escape(str(item["left"]))}</td>'
            f'<td>{escape(str(item["right"]))}</td>'
            f'<td>{escape(unit)}</td></tr>'
        )

    left = escape(works[0]["title"])
    right = escape(works[1]["title"])
    return (
        '<aside class="demo-panel" aria-labelledby="demo-title">'
        '<p class="demo-eyebrow"><span class="demo-indicator" aria-hidden="true"></span>'
        'REAL TEXT · REAL MEASUREMENTS</p>'
        '<h2 id="demo-title">Two books. Different rhythms.</h2>'
        '<p class="demo-intro">A glimpse of the measured language in '
        f'{left} and {right}.'
        ' These are frozen, source-free diagnostics, not FantLab parity.</p>'
        '<div class="demo-legend"><span class="demo-legend-ink">Alexander Grin</span>'
        '<span class="demo-legend-gold">Jules Verne · Beketova translation</span></div>'
        '<ul class="demo-metrics">' + "".join(spark_rows) + '</ul>'
        '<section class="demo-exact" aria-labelledby="demo-exact-title">'
        '<h3 id="demo-exact-title">Exact numbers and units</h3>'
        '<div class="demo-scroll" tabindex="0" role="region" aria-label="Exact comparison values">'
        '<table><caption>Frozen derived measurements; chart labels are rounded to 1 decimal</caption>'
        '<thead><tr><th scope="col">Metric</th><th scope="col">Grin</th>'
        '<th scope="col">Verne</th><th scope="col">Unit</th></tr></thead>'
        '<tbody>' + "".join(exact_rows) + '</tbody></table></div></section>'
        '<a class="demo-open" href="works/two-full-work-differences/">'
        'Inspect all 10 metrics, sources and caveats <span aria-hidden="true">↗</span></a>'
        '<p class="demo-footnote">No book text stored on this page. '
        'Source edition does not match a confirmed FantLab analyzer input. M2: 0/5.</p>'
        '</aside>'
    )


HOME_CSS = """
.site-masthead { display:flex; align-items:center; justify-content:space-between;
  flex-wrap:wrap; gap:1rem; border-bottom:1px solid var(--line); padding:1rem 0; }
.site-wordmark { display:inline-flex; gap:.7rem; align-items:center;
  font:800 .96rem/1.1 system-ui,sans-serif; letter-spacing:.17em; color:var(--ink);
  text-decoration:none; min-height:44px; }
.site-monogram { display:inline-grid; place-items:center; width:2.2rem; height:2.2rem;
  color:#fffaf0; background:#173e37; border-radius:50%;
  font:700 1.4rem/1 Georgia,serif; letter-spacing:0; }
.site-tagline { font:600 .77rem/1.5 system-ui,sans-serif; color:var(--muted); letter-spacing:.09em; text-transform:uppercase; }
.hero-stage { display:grid; grid-template-columns:minmax(0,1fr); align-items:center;
  gap:clamp(1.5rem,4vw,4rem); padding:clamp(1.5rem,4vw,3rem) 0; }
.hero-stage:has(.demo-panel) { grid-template-columns:minmax(0,.91fr) minmax(0,1.09fr); }
.hero-stage .hero { border:0; padding:0; min-width:0; }
.hero-stage .hero h1 { font-size:clamp(2.65rem,5.6vw,5.4rem); }
.hero-stage .hero .lede { max-width:53ch; }
.hero-stage .hero .actions { margin:1rem 0; }
.hero-stage .hero .actions:not(:first-of-type) .primary-action { background:transparent;
  color:var(--accent); font-weight:700; border-color:var(--line); }
.hero-stage .hero .actions:not(:first-of-type) .primary-action:hover { background:var(--accent-soft); }
.demo-panel { min-width:0; color:#fcf5e5; background:#17382f; padding:clamp(1.3rem,2.8vw,2.25rem);
  border:1px solid #4b786b; border-radius:.75rem; box-shadow:0 1.25rem 0 #142e2730; }
.demo-eyebrow { font:750 .71rem/1.5 system-ui,sans-serif; letter-spacing:.12em;
  color:#cee6d8; margin:0 0 .75rem; }
.demo-indicator { display:inline-block; width:.58rem; height:.58rem;
  background:#f1be73; border-radius:50%; margin-right:.4rem; }
.demo-panel h2 { color:#fff6e5; font-size:clamp(1.5rem,2.6vw,2.15rem); margin:.35rem 0 .7rem; }
.demo-intro, .demo-footnote { color:#e6e9da; font:400 .89rem/1.55 system-ui,sans-serif; }
.demo-legend { display:flex; flex-wrap:wrap; gap:.5rem 1rem; padding:.75rem 0;
  font:600 .8rem/1.5 system-ui,sans-serif; border-top:1px solid #4b786b; }
.demo-legend span::before { content:""; display:inline-block; width:.7rem;
  height:.7rem; margin-right:.45rem; border-radius:2px; }
.demo-legend-ink::before { background:#7cd0b7; }
.demo-legend-gold::before { background:#f1be73; }
.demo-metrics { margin:0; padding:0; list-style:none; }
.demo-metric { padding:.65rem 0; border-top:1px solid #4b786b; }
.demo-metric h3 { font:700 .91rem/1.4 system-ui,sans-serif; color:#fff6e5; margin:.15rem 0 .55rem; }
.demo-unit { color:#c9dacf; font-size:.73rem; font-weight:400; }
.demo-series { display:grid; grid-template-columns:2.4rem minmax(0,1fr) 4.4rem;
  gap:.65rem; align-items:center; font:500 .76rem/1.3 system-ui,sans-serif; margin:.42rem 0; }
.demo-series-label { color:#f8f6e8; }
.demo-reading { text-align:right; font-variant-numeric:tabular-nums; color:#fff6e5; }
.demo-track { height:.58rem; background:#426258; border-radius:.4rem; overflow:hidden; }
.demo-fill { display:block; height:100%; border-radius:.4rem; }
.demo-fill-ink { background:#7cd0b7; }
.demo-fill-gold { background:#f1be73; }
.demo-exact { margin-top:.8rem; padding-top:.6rem; border-top:1px solid #4b786b; }
.demo-exact h3 { margin:0 0 .6rem; font:700 .85rem/1.45 system-ui,sans-serif; color:#f6deaf; }
.demo-scroll { overflow:auto; max-width:100%; }
.demo-panel table { min-width:30rem; font:400 .76rem/1.5 system-ui,sans-serif; }
.demo-panel th, .demo-panel td { border-bottom:1px solid #547369; color:#fff6e5; padding:.5rem .35rem; }
.demo-panel table caption { font-size:.75rem; font-weight:400; color:#e6e9da; }
.demo-open { display:inline-block; padding:.75rem 0; min-height:44px;
  color:#ffe1aa; font:700 .89rem/1.5 system-ui,sans-serif; }
.demo-open:hover { color:#fff6e5; }
.demo-footnote { font-size:.76rem; margin:.45rem 0 0; }
@media(max-width:900px) {
  .hero-stage:has(.demo-panel) { grid-template-columns:1fr; }
  .hero-stage { gap:1.5rem; }
  .demo-panel { box-shadow:none; }
}
@media(max-width:480px) {
  .site-masthead { padding:.75rem 0; }
  .site-tagline { font-size:.66rem; }
  .demo-series { grid-template-columns:2.3rem minmax(0,1fr) 3.9rem; gap:.35rem; }
}
@media(prefers-reduced-motion:reduce) { .demo-panel * { transition:none !important; } }
@media print { .demo-panel { box-shadow:none; color:#000; background:#fff;
    border:1px solid #444; break-inside:avoid; }
  .demo-panel h2, .demo-intro, .demo-footnote, .demo-series-label, .demo-reading,
  .demo-metric h3, .demo-unit, .demo-panel th, .demo-panel td { color:#000; }
  .demo-track { border:1px solid #444; }
  .demo-exact h3 { color:#000; }
  .demo-scroll { overflow:visible; }
  .demo-panel table { min-width:0; width:100%; }
}
"""
