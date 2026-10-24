"""Canonical source-free FantLab evidence page for the static Scriptorium site.

This is a diagnostic display of independently retained evidence, never an
assertion of source-matched parity. The underlying matrix validates its inputs.
"""
from __future__ import annotations

import html
from pathlib import Path
from urllib.parse import urlsplit

from . import benchmark_metric_matrix as matrix
from .benchmark import _reference_specs


EXPECTED_ENTRY = {
    "entry_id": "fantlab-five-work-retained-evidence-v1",
    "kind": "benchmark_matrix",
    "slug": "fantlab-evidence",
    "title": "FantLab evidence — five frozen works",
    "artifact_schema": matrix.SCHEMA_VERSION,
    "publication_status": "diagnostic",
    "benchmark_admissibility": "diagnostic_only",
    "corpus_admissibility": "not_admissible",
    "compatibility_claim": "inferred",
    "source_text_included": False,
}



# Display labels come from the versioned benchmark comparison registry.
# They do not establish FantLab definition equivalence or parity.
_METRIC_PRESENTATION = {
    metric_id: (label, metric_id.split(".")[1].title())
    for metric_id, _path, label, _rule in _reference_specs()
}
_DISPLAY_STATUS = {
    "UNRESOLVED_SOURCE": "Input identity unverified",
    "UNRESOLVED_NO_ACTUAL": "Actual value unavailable",
    "NOT_RUN": "Not run",
}

def validate_entry(entry: object) -> None:
    """The public report must be explicitly and exactly registered."""
    if not isinstance(entry, dict) or entry != EXPECTED_ENTRY:
        raise ValueError("unrecognized FantLab evidence publication registration")


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _number(value: object) -> str:
    return "NOT_RUN" if value is None else _esc(value)


def _reference(url: object) -> str:
    if not isinstance(url, str):
        raise ValueError("missing FantLab reference URL")
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc not in ("fantlab.ru", "www.fantlab.ru")
            or parsed.username or parsed.password or not parsed.path.startswith("/work")):
        raise ValueError("unsafe FantLab reference URL")
    return '<a href="' + _esc(url) + '" rel="noopener noreferrer">FantLab reference ↗</a>'


def build(root: Path) -> dict[str, str]:
    """Render verified source-free data into a readable offline HTML and downloads."""
    report = matrix.build_metric_matrix(root)
    entries = report["entries"]
    if (report["schema_version"] != matrix.SCHEMA_VERSION
            or report["m2_source_matched_pass_count"] != 0
            or report["works_reported"] != 5
            or report["works_with_retained_metric_diagnostics"] != 1
            or report["retained_metric_rows"] != 28
            or len(entries) != 5):
        raise ValueError("FantLab evidence publication gate has changed")

    anna = next(
        (entry for entry in entries if entry["candidate_id"] == "tolstoy-anna-karenina-ru"),
        None,
    )
    if (anna is None or len(anna["metric_rows"]) != 28
            or anna["metric_rows_with_actual"] != 23
            or anna["metric_rows_without_actual"] != 5):
        raise ValueError("retained Anna diagnostic coverage changed")

    works = []
    for item in entries:
        status = item["metric_evidence"]
        if item["exact_fantlab_input_identity"] != "UNKNOWN" or status not in (
            "RETAINED_DIAGNOSTIC", "NOT_RUN"
        ):
            raise ValueError("unproven source identity or metric evidence was upgraded")
        if status == "NOT_RUN" and item["metric_rows"]:
            raise ValueError("unreported metric run has fabricated rows")
        measured = str(item["metric_rows_with_actual"]) if item["metric_rows"] else "NOT_RUN"
        works.append(
            '<tr class="source-row"><th scope="row">' + _esc(item["title"]) +
            '<span class="eyebrow">' + _esc(item["author"]) + '</span></th><td>' +
            _esc(status) + '</td><td>' + measured + '</td><td>UNKNOWN</td><td>' +
            _reference(item["reference_url"]) + '<br><small>' +
            _esc(item["reference_date"]) + '</small></td></tr>'
        )

    if {row["metric_id"] for row in anna["metric_rows"]} != set(_METRIC_PRESENTATION):
        raise ValueError("unrecognized FantLab metric ID in evidence page")
    metrics = []
    for row in anna["metric_rows"]:
        if row["comparison_kind"] != "DIAGNOSTIC_ONLY" or row["display_rounding_evidence"] != "UNKNOWN":
            raise ValueError("metric evidence was promoted without source/rounding proof")
        status = row["result"]
        if (status not in _DISPLAY_STATUS or
                (row["actual"] is None) != (status != "UNRESOLVED_SOURCE")):
            raise ValueError("invalid diagnostic scientific status")
        label, group = _METRIC_PRESENTATION[row["metric_id"]]
        metrics.append(
            '<tr class="metric-row"><th scope="row"><span class="eyebrow">' +
            _esc(group) + '</span><br><span lang="ru">' + _esc(label) +
            '</span><br><code>' + _esc(row["metric_id"]) +
            '</code></th><td>' + _number(row["expected"]) + '</td><td>' +
            _number(row["actual"]) + '</td><td>' +
            _number(row["actual_minus_expected"]) + '</td><td>' +
            _esc(_DISPLAY_STATUS[status]) + '<br><code>' + _esc(status) +
            '</code></td></tr>'
        )

    body = (
        '<main id="main-content" tabindex="-1">'
        '<nav aria-label="Evidence navigation"><a href="../../">← All analyses</a></nav>'
        '<header class="hero"><p class="eyebrow">Methodology · diagnostic evidence</p>'
        '<h1>How close are the measurements?</h1>'
        '<p class="lede">Inspect retained differences against publicly displayed FantLab '
        'numbers, work by work and metric by metric. No manuscripts are shared.</p>'
        '<p class="notice"><strong>Not FantLab parity. M2: 0/5.</strong> '
        'Exact FantLab analyzer-input text identity is UNKNOWN for every work; '
        'decimal display rounding is UNKNOWN. Count resemblance does not prove source '
        'identity. Missing measurements are NOT_RUN, never zero.</p>'
        '<p class="actions"><a class="primary-action" href="metrics.json" download>'
        'Download verified JSON</a> <a href="metrics.csv" download>'
        'Download metric CSV</a> <a href="https://github.com/drevendev/Scriptorium/blob/master/'
        'docs/BENCHMARK_METRIC_MATRIX.md">Read the methodology ↗</a></p>'
        '</header>'
        '<section aria-labelledby="works-title"><h2 id="works-title">Five frozen public candidates</h2>'
        '<p>Only one work has retained metric observations. The four others '
        'have NOT_RUN metric status. These sources have legal provenance, '
        'but none has verified FantLab analyzer-input identity.</p>'
        '<p id="works-scroll">On narrow screens, scroll the table horizontally. '
        'Tab to the table to use keyboard scrolling.</p>'
        '<div class="table-wrap" role="region" aria-label="Five-work evidence status" '
        'tabindex="0" aria-describedby="works-scroll"><table>'
        '<caption>Source-frozen diagnostics, not parity benchmarks</caption>'
        '<thead><tr><th scope="col">Work</th><th scope="col">Metric evidence</th>'
        '<th scope="col">Observed values</th><th scope="col">FantLab input match</th>'
        '<th scope="col">Dated reference</th></tr></thead><tbody>' +
        ''.join(works) + '</tbody></table></div></section>'
        '<section aria-labelledby="metrics-title"><h2 id="metrics-title">'
        'Anna Karenina: 28 retained diagnostic rows</h2>'
        '<p>23 numeric observations; five missing actual values. '
        'Δ is Scriptorium actual minus FantLab expected; all observed rows '
        'remain unresolved because source identity is unknown. '
        'Names come from the existing benchmark field registry; each row retains '
        'its machine ID. Friendly statuses do not change the exported data.</p>'
        '<p id="metrics-scroll">On narrow screens, scroll the metric table horizontally. '
        'Tab to it for keyboard scrolling.</p>'
        '<div class="table-wrap" role="region" aria-label="Anna Karenina metric differences" '
        'tabindex="0" aria-describedby="metrics-scroll"><table>'
        '<caption>FantLab reference vs Scriptorium retained values, diagnostic only</caption>'
        '<thead><tr><th scope="col">Metric ID</th><th scope="col">FantLab expected</th>'
        '<th scope="col">Scriptorium actual</th><th scope="col">Actual − expected</th>'
        '<th scope="col">Scientific status</th></tr></thead><tbody>' +
        ''.join(metrics) + '</tbody></table></div></section>'
        '<p class="notice">No parity passes have been established. Reproduction '
        'requires five legally usable ≥300,000-character works with the actual '
        'FantLab analyzer-input identity and published rounding evidence.</p></main>'
    )
    return {
        "body": body,
        "json": matrix.render_metric_matrix(report, "json"),
        "csv": matrix.render_metric_matrix(report, "csv"),
    }
