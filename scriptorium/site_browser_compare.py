"""Static, source-free browser desk using the canonical Python metric snapshot.

No remote resources or analysis text. Numeric JSON lexemes stay exact in the
browser; the 29-entry registry is generated at build time from the engine.
"""
from __future__ import annotations

import json
from importlib.resources import files

from .metric_labels import METRIC_LABELS
from .metrics import analyze_deterministic_metrics


CONTRACT_SLOT = "/*SCRIPTORIUM_METRIC_CONTRACT*/ null"


def render_script() -> str:
    canonical = analyze_deterministic_metrics("")
    if set(canonical["metrics"]) != set(METRIC_LABELS) or len(METRIC_LABELS) != 29:
        raise ValueError("browser contract does not match the canonical analyzer")
    metrics = {
        metric_id: {"label": METRIC_LABELS[metric_id], "row": {
            name: None if name == "value" else value
            for name, value in row.items()
        }}
        for metric_id, row in canonical["metrics"].items()
    }
    contract = {
        "metric_contract_id": canonical["metric_contract_id"],
        "profiles": canonical["profiles"],
        "metrics": metrics,
    }
    source = files("scriptorium").joinpath("browser_compare.js").read_text(encoding="utf-8")
    if source.count(CONTRACT_SLOT) != 1:
        raise ValueError("browser contract insertion point missing or ambiguous")
    data = json.dumps(contract, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return source.replace(CONTRACT_SLOT, data)


BODY = """<main id="main-content" tabindex="-1" class="private-desk">
<nav aria-label="Breadcrumb"><a href="../">← Published literary evidence</a></nav>
<header class="hero"><p class="eyebrow">Scriptorium · private Reader desk</p>
<h1>Compare your writing, not your privacy.</h1>
<p class="lede">Select two Scriptorium Reader JSON reports. Inspect 29 exact measurements,
reasons for unavailable results and right-minus-left differences, without uploading
reports or manuscripts.</p></header>
<section aria-labelledby="desk-heading" class="desk-panel">
<h2 id="desk-heading">Two local reports, one comparison</h2>
<p>First create JSON reports with <code>scriptorium analyze manuscript.txt --output report.json</code>.
Files are read only in this browser tab. The JSON and CSV exports contain derived data and
source hashes, never source prose; hashes can still identify known works.</p>
<div class="desk-inputs"><label for="report-left">01 · Left Reader JSON
<input id="report-left" type="file" accept=".json,application/json" aria-describedby="desk-help"></label>
<label for="report-right">02 · Right Reader JSON
<input id="report-right" type="file" accept=".json,application/json" aria-describedby="desk-help"></label></div>
<p id="desk-help">Reports must use the same 29-metric contract. Incompatible profiles or
missing values are labelled—not silently converted to zero. Each file is limited to 8 MiB.</p>
<button type="button" id="run-comparison" disabled>Compare reports →</button>
<p id="comparison-message" role="status" aria-live="polite" aria-atomic="true">Select both reports to begin.</p>
<noscript><p class="notice">Browser comparison requires JavaScript. You can always compare files
with the <a href="https://github.com/drevendev/Scriptorium/blob/master/docs/PRIVATE_COMPARISON.md">offline Python Reader CLI</a>.</p></noscript>
</section>
<section id="comparison-result" hidden aria-labelledby="comparison-title">
<h2 id="comparison-title">Source-free comparison</h2>
<p class="notice">Inferred/extension measurements only: not verified FantLab parity (M2 0/5).
Imported hashes are declarations, not authenticated evidence. Percent differences use
percentage points, never relative percentages. Re-analyze originals to verify.</p>
<pre class="desk-sources" id="source-summary" aria-label="Declared source hashes and lengths"></pre>
<p class="actions"><button type="button" id="save-comparison-json" disabled>Export JSON ↓</button>
<button type="button" id="save-comparison-csv" disabled>Export CSV ↓</button></p>
<div class="table-wrap" tabindex="0" role="region" aria-label="29 report measurements">
<table><caption>29 metrics · original values, units and comparison status</caption>
<thead><tr><th scope="col">Metric</th><th scope="col">Left</th><th scope="col">Right</th>
<th scope="col">Unit</th><th scope="col">Difference</th><th scope="col">Difference unit</th>
<th scope="col">Status</th><th scope="col">Reason</th></tr></thead>
<tbody id="comparison-rows"></tbody></table></div></section>
<p class="reading-guide">This tool never enrolls a work in the public corpus. Read the
<a href="https://github.com/drevendev/Scriptorium/blob/master/docs/PRIVATE_COMPARISON.md">validation and provenance method</a>
before sharing a derived report.</p>
<script src="../assets/private-compare.js" defer></script></main>"""


CSS = """
.private-desk .hero { padding-block: clamp(1.8rem, 5vw, 4rem); }
.private-desk .hero h1 { max-width: 19ch; }
.desk-panel { margin: 2rem 0; padding: clamp(1.2rem, 3vw, 2rem); border: 1px solid var(--line);
  background: var(--surface); border-radius: .45rem; }
.desk-panel p { max-width: 75ch; }
.desk-inputs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; margin: 1.4rem 0; }
.desk-inputs label { display: grid; gap: .65rem; border-left: 4px solid var(--accent);
  background: var(--accent-soft); padding: 1rem; min-width: 0;
  font: 700 1rem/1.5 system-ui,sans-serif; }
.desk-inputs input { width: 100%; min-width: 0; padding: .65rem; border: 1px solid var(--line);
  color: var(--ink); background: var(--surface); border-radius: .3rem;
  font: 400 .95rem/1.6 system-ui,sans-serif; }
.private-desk button { min-height: 44px; padding: .7rem 1rem; border: 2px solid var(--accent);
  border-radius: .3rem; background: var(--accent); color: var(--paper);
  font: 700 1rem/1.5 system-ui,sans-serif; cursor: pointer; }
.private-desk button:disabled { opacity: .65; cursor: default; }
.private-desk button:focus-visible, .desk-inputs input:focus-visible {
  outline: 3px solid var(--focus); outline-offset: 3px; }
#comparison-message { border-left: 4px solid var(--line); padding-left: 1rem; min-height: 2rem; }
#comparison-result[hidden] { display: none !important; }
.desk-sources { white-space: pre-wrap; overflow-wrap: anywhere; padding: 1rem;
  border: 1px solid var(--line); background: var(--surface);
  font: .84rem/1.6 ui-monospace,Consolas,monospace; }
.private-desk .table-wrap { border: 1px solid var(--line); border-radius: .35rem; }
.private-desk table { min-width: 64rem; }
.private-desk td { font-variant-numeric: tabular-nums; }
.private-desk th { min-width: 10rem; }
.private-desk th:first-child { min-width: 17rem; }
@media(max-width:720px) { .desk-inputs { grid-template-columns: 1fr; } }
@media(prefers-color-scheme:dark) { .private-desk button { color: #14201d; } }
@media print {
  .desk-panel, .private-desk .actions { display: none !important; }
  .private-desk .table-wrap { overflow: visible; border: 0; }
  .private-desk table, .private-desk tbody { display: block; width: 100%; min-width: 0; }
  .private-desk thead { display: none; }
  .private-desk tbody tr {
    display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0 .75rem; padding: .3rem .65rem; margin: .65rem 0;
    border: 1px solid #666; break-inside: avoid; page-break-inside: avoid;
  }
  .private-desk tbody th, .private-desk tbody th:first-child {
    grid-column: 1 / -1; min-width: 0; overflow-wrap: anywhere;
    border-bottom: 1px solid #666; font-size: .93rem;
  }
  .private-desk tbody td {
    display: block; min-width: 0; width: 100%; padding: .3rem 0;
    font-size: .85rem; overflow-wrap: anywhere;
  }
  .private-desk tbody td::before {
    display: block; font: 700 .72rem/1.3 system-ui, sans-serif;
  }
  .private-desk tbody td:nth-of-type(1)::before { content: "Left"; }
  .private-desk tbody td:nth-of-type(2)::before { content: "Right"; }
  .private-desk tbody td:nth-of-type(3)::before { content: "Unit"; }
  .private-desk tbody td:nth-of-type(4)::before { content: "Difference"; }
  .private-desk tbody td:nth-of-type(5)::before { content: "Difference unit"; }
  .private-desk tbody td:nth-of-type(6)::before { content: "Status"; }
  .private-desk tbody td:nth-of-type(7)::before { content: "Reason"; }
}
"""