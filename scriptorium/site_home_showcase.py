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
        '<p id="demo-scroll-hint" class="demo-scroll-hint">On narrow screens, swipe to view '
        'all columns. Keyboard: focus the table region and use arrow keys.</p>'
        '<div class="demo-scroll" tabindex="0" role="region" '
        'aria-label="Exact comparison values" aria-describedby="demo-scroll-hint">'
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



_ATLAS_BOOKS = (
    ("tolstoy-anna-karenina-ru", "metrics-title", 28, 23),
    ("grin-running-on-waves-ru", "waves-metrics-title", 27, 23),
    ("bely-silver-dove-ru", "silver-title", 29, 24),
    ("dostoevsky-brothers-karamazov-ru", "karamazov-title", 29, 24),
    ("tolstoy-hyperboloid-garin-wikisource-ru", "works-title", 29, 24),
)


def render_research_atlas(entries: Sequence[Mapping[str, Any]]) -> str:
    """Evidence-first publication: availability is not FantLab reproduction."""
    found = [item for item in entries if item.get("render_mode") == "benchmark_matrix"]
    if not found:
        return ""
    if len(found) != 1 or type(found[0].get("json_data")) is not str:
        raise ValueError("invalid evidence atlas registration")
    raw = found[0]["json_data"]
    if len(raw) > 1_000_000:
        raise ValueError("oversized evidence atlas data")
    data = json.loads(raw)
    if (type(data) is not dict
            or data.get("schema_version") != "scriptorium-fantlab-retained-metrics-v1"
            or type(data.get("m2_source_matched_pass_count")) is not int
            or data["m2_source_matched_pass_count"] != 0
            or data.get("works_reported") != 5
            or data.get("works_with_retained_metric_diagnostics") != 5
            or data.get("retained_metric_rows") != 171
            or data.get("supplemental_retained_metric_rows") != 29):
        raise ValueError("changed evidence atlas scientific boundary")
    supplemental = data.get("supplemental_diagnostics")
    if (type(supplemental) is not list or len(supplemental) != 1
            or type(supplemental[0]) is not dict
            or supplemental[0].get("candidate_id") != "tolstoy-resurrection-ru"
            or supplemental[0].get("m2_candidate_scope") != "SUPPLEMENTAL_NOT_SOURCE_MATCHED"
            or supplemental[0].get("exact_fantlab_input_identity") != "UNKNOWN"
            or supplemental[0].get("metric_evidence") != "RETAINED_DIAGNOSTIC"
            or supplemental[0].get("metric_rows_with_actual") != 24
            or supplemental[0].get("metric_rows_without_actual") != 5
            or type(supplemental[0].get("metric_rows")) is not list
            or len(supplemental[0]["metric_rows"]) != 29):
        raise ValueError("changed evidence atlas supplemental scope")
    if sum(row.get("actual") is not None for row in supplemental[0]["metric_rows"]) != 24:
        raise ValueError("changed evidence atlas supplemental coverage")
    source_rows = data.get("entries")
    if type(source_rows) is not list or len(source_rows) != 5:
        raise ValueError("incomplete evidence atlas inventory")
    rows_by_id = {item.get("candidate_id"): item for item in source_rows if type(item) is dict}
    if len(rows_by_id) != 5 or set(rows_by_id) != {book[0] for book in _ATLAS_BOOKS}:
        raise ValueError("duplicate or unexpected atlas book")
    separate = [item for item in entries
                if item.get("render_mode") == "hyperboloid_diagnostic"]
    if len(separate) > 1 or (separate and separate[0].get("slug")
                             != "hyperboloid-garin-measured"):
        raise ValueError("unrecognized separate Hyperboloid report")
    cards = []
    total_measured = 0
    total_missing = 0
    for position, (identity, anchor, expected, observed) in enumerate(_ATLAS_BOOKS, 1):
        item = rows_by_id[identity]
        title, author = item.get("title"), item.get("author")
        source_metrics = item.get("metric_rows")
        missing = expected - observed
        if (type(title) is not str or not title or len(title) > 160
                or type(author) is not str or not author or len(author) > 160
                or type(source_metrics) is not list or len(source_metrics) != expected
                or item.get("metric_rows_with_actual") != observed
                or item.get("metric_rows_without_actual") != missing
                or item.get("exact_fantlab_input_identity") != "UNKNOWN"
                or item.get("metric_evidence") != ("RETAINED_DIAGNOSTIC" if expected else "NOT_RUN")
                or sum(r.get("actual") is not None for r in source_metrics) != observed):
            raise ValueError("evidence atlas changed source or measurement identity")
        total_measured += observed
        total_missing += missing
        progress = f'<span class="atlas-bar" aria-hidden="true"><span style="width:{observed / expected * 100:.2f}%"></span></span>' if expected else ""
        separate_report = bool(separate) and identity == "tolstoy-hyperboloid-garin-wikisource-ru"
        count = f"{observed} of {expected} matrix measurements available"
        target_href = ("works/hyperboloid-garin-measured/" if separate_report
                       else f"evidence/fantlab/#{anchor}")
        link_label = ("Open 29-row report" if separate_report else
                      "View source status" if not expected else "Explore measurements")
        cards.append(
            '<li class="atlas-book' + (' atlas-pending' if not expected else '') + '">'
            f'<p class="atlas-number">VOLUME {position:02d} / 05</p>'
            f'<h3>{escape(title)}</h3><p class="atlas-author">{escape(author)}</p>'
            f'<p class="atlas-count">{count}</p>' + progress +
            f'<a href="{target_href}">'
            + link_label
            + ' <span aria-hidden="true">↗</span></a></li>'
        )
    if (total_measured, total_missing) != (118, 24):
        raise ValueError("evidence atlas summary no longer matches verified rows")
    return (
        '<section class="atlas" id="research-atlas" aria-labelledby="atlas-title">'
        '<div class="atlas-heading"><div>'
        '<p class="atlas-kicker">THE READING ROOM · VERIFIED DIAGNOSTIC DATA</p>'
        '<h2 id="atlas-title">Five books under the lens.</h2>'
        '<p>Explore measured vocabulary, sentence rhythm, dialogue and punctuation '
        'without downloading a manuscript. All values come from the retained evidence matrix.</p>'
        '</div><div class="atlas-boundary"><strong>M2 · 0 / 5</strong>'
        '<span>Source-matched FantLab reproduction is not yet established.</span></div></div>'
        '<div class="atlas-numbers" aria-label="Retained measurement coverage">'
        '<p><strong>5 / 5</strong><span>works with observations</span></p>'
        '<p><strong>142</strong><span>recorded metric fields</span></p>'
        '<p><strong>118</strong><span>numeric measurements</span></p>'
        '<p><strong>24</strong><span>unavailable, never zero-filled</span></p></div>'
        '<ol class="atlas-books">' + ''.join(cards) + '</ol>'
        '<div class="atlas-foot"><p><strong>Proved:</strong> reproducible, source-frozen '
        'Scriptorium diagnostics. <strong>Not proved:</strong> the same text, dictionary '
        'or coefficients as FantLab. This is an honest preview, not a parity score.</p>'
        '<a href="evidence/fantlab/">See all sources and exact values →</a></div>'
        '</section>'
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
.demo-scroll-hint { color:#e6e9da; font:400 .75rem/1.5 system-ui,sans-serif;
  margin:.25rem 0 .55rem; }
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
  .demo-eyebrow, .demo-panel table caption, .demo-open { color:#000; }
  .demo-open { text-decoration:underline; }
  /* Hover/focus can survive print preview; their higher-specificity screen color
     must not turn the evidence link nearly white on a white printed page. */
  .demo-open:hover, .demo-open:focus-visible { color:#000; text-decoration:underline; }
  .demo-scroll-hint { display:none; }
  .demo-scroll { overflow:visible; }
  .demo-panel table { min-width:0; width:100%; }
}
/* Accessible research atlas. Bars are decorative: exact values appear as text. */
.atlas { background:var(--surface); border:1px solid var(--line);
  border-radius:1rem; padding:clamp(1.2rem,3vw,2.7rem); margin:0 0 3rem;
  box-shadow:0 1rem 2rem rgba(16,43,35,.08); }
.atlas-heading { display:grid; grid-template-columns:minmax(0,1fr) 14rem; gap:2rem; align-items:end; }
.atlas-kicker { color:var(--accent); font:750 .7rem/1.5 system-ui,sans-serif;
  letter-spacing:.14em; margin:0 0 .5rem; }
.atlas h2 { color:var(--ink); font:600 clamp(2rem,4vw,3.5rem)/1.08 Georgia,serif;
  margin:0 0 .6rem; letter-spacing:-.035em; }
.atlas-heading p:not(.atlas-kicker) { color:var(--muted); max-width:64ch;
  font:400 .95rem/1.65 system-ui,sans-serif; }
.atlas-boundary { display:flex; flex-direction:column; gap:.45rem; padding:1rem;
  background:var(--accent-soft); border-left:4px solid var(--accent); }
.atlas-boundary strong { font:750 1.16rem/1.3 system-ui,sans-serif; color:var(--ink); }
.atlas-boundary span { font:400 .8rem/1.45 system-ui,sans-serif; color:var(--ink); }
.atlas-numbers { display:grid; grid-template-columns:repeat(4,minmax(0,1fr));
  margin:1.6rem 0; border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
.atlas-numbers p { display:flex; flex-direction:column; gap:.25rem; margin:.8rem 0;
  padding:.4rem .9rem; border-right:1px solid var(--line); }
.atlas-numbers p:first-child { padding-left:0; }
.atlas-numbers p:last-child { border:0; }
.atlas-numbers strong { font:600 clamp(1.6rem,3vw,2.4rem)/1.15 Georgia,serif;
  color:var(--ink); font-variant-numeric:tabular-nums; }
.atlas-numbers span { font:500 .76rem/1.4 system-ui,sans-serif; color:var(--muted); }
.atlas-books { display:grid; grid-template-columns:repeat(4,minmax(0,1fr));
  gap:.75rem; padding:0; margin:0; list-style:none; }
.atlas-book { display:flex; flex-direction:column; min-width:0; padding:1rem;
  background:var(--paper); border:1px solid var(--line); border-radius:.65rem; }
.atlas-number { font:750 .68rem/1.4 system-ui,sans-serif; letter-spacing:.12em;
  color:var(--muted); margin:0 0 1.05rem; }
.atlas-book h3 { font:600 1.23rem/1.23 Georgia,serif; margin:0 0 .4rem;
  color:var(--ink); overflow-wrap:anywhere; }
.atlas-author { color:var(--muted); font:500 .76rem/1.4 system-ui,sans-serif;
  margin:0 0 1.2rem; }
.atlas-count { margin:auto 0 .45rem; font:700 .76rem/1.45 system-ui,sans-serif;
  color:var(--ink); font-variant-numeric:tabular-nums; }
.atlas-bar { display:block; height:.4rem; background:var(--accent-soft);
  border-radius:1rem; overflow:hidden; }
.atlas-bar span { display:block; height:100%; background:var(--accent); }
.atlas-book a { color:var(--accent); min-height:44px; display:inline-flex; align-items:center;
  margin-top:.65rem; font:700 .8rem/1.4 system-ui,sans-serif; text-underline-offset:.2em; }
.atlas-pending { grid-column:1/-1; display:grid;
  grid-template-columns:7rem minmax(0,1fr) minmax(9rem,.8fr) auto;
  align-items:center; gap:1rem; }
.atlas-pending .atlas-number,.atlas-pending h3,.atlas-pending .atlas-count,
.atlas-pending a { margin:0; }
.atlas-pending .atlas-author { display:none; }
.atlas-foot { display:flex; flex-wrap:wrap; align-items:baseline; gap:1rem;
  border-top:1px solid var(--line); margin-top:1.5rem; padding-top:1.1rem;
  font:400 .82rem/1.6 system-ui,sans-serif; }
.atlas-foot p { flex:1 1 20rem; margin:0; color:var(--muted); }
.atlas-foot strong { color:var(--ink); }
.atlas-foot a { color:var(--accent); font-weight:750; min-height:44px;
  display:inline-flex; align-items:center; text-underline-offset:.2em; }
@media(max-width:1080px) {
  .atlas-books { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .atlas-pending { grid-template-columns:6rem minmax(0,1fr) auto; }
}
@media(max-width:720px) {
  .atlas-heading { grid-template-columns:1fr; gap:.6rem; }
  .atlas-numbers { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .atlas-numbers p:nth-child(2) { border-right:0; }
  .atlas-pending { display:flex; align-items:stretch; }
  .atlas-pending .atlas-count { margin:.5rem 0; }
}
@media(max-width:490px) { .atlas-books { grid-template-columns:1fr; } }
@media print {
  .atlas { box-shadow:none; background:#fff; }
  .atlas-book,.atlas-boundary { background:#fff; border-color:#555; }
  .atlas-book { break-inside:avoid; }
  .atlas h2,.atlas-kicker,.atlas-book h3,.atlas-number,.atlas-count,
  .atlas-author,.atlas-numbers strong,.atlas-numbers span,.atlas-heading p,
  .atlas-boundary strong,.atlas-boundary span,.atlas-foot p,.atlas-foot strong,
  .atlas-foot a,.atlas-book a { color:#000 !important; }
  .atlas-book a,.atlas-foot a { text-decoration:underline; }
}

"""
