"""Reader homepage snapshot generated only from the validated retained-metrics matrix.

The source-frozen measurements are diagnostic evidence, not FantLab parity.
This panel never includes source text or treats unknown observations as zero.
"""
from __future__ import annotations

import html
import json
import math
from collections.abc import Mapping, Sequence
from typing import Any


def _is_count(value: object) -> bool:
    return type(value) is int and value >= 0


def render_stage(entries: Sequence[Mapping[str, Any]]) -> str:
    """Render current evidence coverage, failing closed on inconsistent receipts."""
    registered = [item for item in entries if item.get("render_mode") == "benchmark_matrix"]
    if not registered:
        return ""
    if len(registered) != 1 or registered[0].get("slug") != "fantlab-evidence":
        raise ValueError("unexpected evidence matrix registration")
    raw = registered[0].get("json_data")
    if type(raw) is not str or len(raw) > 2_000_000:
        raise ValueError("retained evidence matrix unavailable")
    data = json.loads(raw)
    if type(data) is not dict or data.get("schema_version") != "scriptorium-fantlab-retained-metrics-v1":
        raise ValueError("unrecognized retained metric matrix")
    works = data.get("entries")
    if (type(works) is not list or not works or not all(type(w) is dict for w in works)
            or not _is_count(data.get("works_reported"))
            or data["works_reported"] != len(works)
            or data.get("m2_source_matched_pass_count") != 0):
        raise ValueError("evidence scope or parity claim changed")

    measured_works = 0
    measured_total = 0
    missing_total = 0
    observed_rows = 0
    table_rows = []
    seen = set()
    for work in works:
        candidate = work.get("candidate_id")
        title = work.get("title")
        rows = work.get("metric_rows")
        if (type(candidate) is not str or not candidate or candidate in seen
                or type(title) is not str or not 0 < len(title) <= 180
                or type(rows) is not list
                or work.get("exact_fantlab_input_identity") != "UNKNOWN"
                or not _is_count(work.get("metric_rows_with_actual"))
                or not _is_count(work.get("metric_rows_without_actual"))):
            raise ValueError("invalid or duplicated measured-work identity")
        seen.add(candidate)
        available = work["metric_rows_with_actual"]
        unavailable = work["metric_rows_without_actual"]
        if available + unavailable != len(rows):
            raise ValueError("unavailable values do not match recorded rows")
        if work.get("metric_evidence") != ("RETAINED_DIAGNOSTIC" if rows else "NOT_RUN"):
            raise ValueError("unverified measurement was promoted")
        for row in rows:
            if (type(row) is not dict
                    or row.get("display_rounding_evidence") != "UNKNOWN"
                    or row.get("comparison_kind") not in ("DIAGNOSTIC_ONLY", "EXTENSION_ONLY")):
                raise ValueError("metric scientific boundary changed")
            actual = row.get("actual")
            if actual is not None and (type(actual) not in (int, float) or not math.isfinite(actual)):
                raise ValueError("invalid numeric observation")
        if sum(row.get("actual") is not None for row in rows) != available:
            raise ValueError("measured totals disagree with rows")
        measured_works += bool(rows)
        measured_total += available
        missing_total += unavailable
        observed_rows += len(rows)
        count_label = str(available) if rows else "Not run"
        table_rows.append(
            '<tr><th scope="row">' + html.escape(title, quote=True) +
            '</th><td>' + count_label + '</td><td>' +
            (str(unavailable) if rows else "Not run") +
            '</td><td>Unverified</td></tr>'
        )

    if (data.get("works_with_retained_metric_diagnostics") != measured_works
            or data.get("retained_metric_rows") != observed_rows
            or measured_total + missing_total != observed_rows):
        raise ValueError("summary coverage disagrees with retained rows")

    def statistic(value: str, label: str) -> str:
        return ('<div class="stage-stat"><strong>' + value +
                '</strong><span>' + label + '</span></div>')

    return (
        '<section class="stage-overview" aria-labelledby="stage-title">'
        '<div class="stage-heading"><div><p class="eyebrow">Current research preview</p>'
        '<h2 id="stage-title">See what the analyzer can measure today.</h2>'
        '<p>These are real, source-frozen literary measurements, not an invented style score. '
        'Explore the full report to see units, edition witnesses and unresolved differences.</p>'
        '</div><a class="stage-link" href="evidence/fantlab/">Open the complete evidence table ↗</a></div>'
        '<div class="stage-stats" aria-label="Diagnostic measurement coverage">'
        + statistic(str(measured_works), "works with measured fields")
        + statistic(str(measured_total), "recorded numeric values")
        + statistic(str(missing_total), "unavailable actual values")
        + statistic("0/5", "proven FantLab source-matched works")
        + '</div>'
        '<p class="stage-disclaimer"><strong>Coverage is not parity.</strong> '
        'A measured value is only a Scriptorium observation. '
        'FantLab input editions and rounding are unverified; missing values are never zero. '
        'One source may be frozen without having field measurements.</p>'
        '<div class="stage-table-scroll" tabindex="0" role="region" '
        'aria-label="Per-work measurement availability" aria-describedby="stage-table-hint">'
        '<table><caption>Recorded fields in frozen works — source identity unverified</caption>'
        '<thead><tr><th scope="col">Work</th><th scope="col">Numeric</th>'
        '<th scope="col">Unavailable</th><th scope="col">FantLab parity</th>'
        '</tr></thead><tbody>' + "".join(table_rows) + '</tbody></table></div>'
        '<p id="stage-table-hint" class="stage-hint">On small screens, scroll the table horizontally. '
        'For keyboard use, focus the table region and use arrow keys.</p>'
        '</section>'
    )


STAGE_CSS = """
.stage-overview { margin:1.2rem 0 2.8rem; padding:clamp(1.2rem,3vw,2rem);
  background:var(--surface); border:1px solid var(--line); border-radius:.65rem; }
.stage-heading { display:flex; flex-wrap:wrap; align-items:end; justify-content:space-between;
  gap:1rem 2rem; }
.stage-heading h2 { font-size:clamp(1.65rem,3vw,2.5rem); margin:.1rem 0 .5rem; }
.stage-heading p { max-width:65ch; }
.stage-link { display:inline-flex; min-height:44px; align-items:center; padding:.65rem .9rem;
  border:1px solid var(--line); border-radius:.35rem; text-align:center; font-weight:700; }
.stage-link:hover { background:var(--accent-soft); }
.stage-stats { display:grid; grid-template-columns:repeat(4,minmax(0,1fr));
  gap:.8rem; margin:1.4rem 0; }
.stage-stat { display:flex; flex-direction:column; min-width:0; padding:1rem;
  border-left:3px solid var(--accent); background:var(--accent-soft); }
.stage-stat strong { font:750 clamp(1.9rem,3.5vw,2.8rem)/1.15 system-ui,sans-serif;
  font-variant-numeric:tabular-nums; }
.stage-stat span { font:.79rem/1.45 system-ui,sans-serif; margin-top:.45rem; }
.stage-disclaimer { max-width:84ch; font-size:.94rem; }
.stage-table-scroll { max-width:100%; overflow-x:auto; }
.stage-table-scroll table { min-width:36rem; }
.stage-hint { font:.79rem/1.5 system-ui,sans-serif; color:var(--muted); }
@media(max-width:800px) { .stage-stats { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media(max-width:450px) { .stage-stats { gap:.45rem; } .stage-stat { padding:.65rem; } }
@media print { .stage-overview, .stage-stat { background:#fff; color:#000; box-shadow:none; }
  .stage-link { color:#000; } .stage-table-scroll { overflow:visible; }
  .stage-table-scroll table { min-width:0; } .stage-hint { display:none; } }
"""
