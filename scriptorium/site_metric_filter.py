"""Progressively enhanced, private/offline filtering of FantLab evidence rows.

The filter affects the visible table only; canonical downloaded data, parity
statuses, print rows and source provenance remain unchanged.
"""

FILTER_CONTROLS = """<section id="metric-filters" class="metric-filters"
  aria-label="Explore Anna Karenina diagnostic metric rows" hidden>
<div class="metric-filter-grid">
<label for="metric-query">Search labels and metric IDs
<input id="metric-query" type="search" autocomplete="off"
  placeholder="e.g. диалоги, punctuation, word length"
  aria-controls="retained-metric-rows"></label>
<label for="metric-family-select">Metric family
<select id="metric-family-select" aria-controls="retained-metric-rows">
<option value="all">All families</option>
<option value="dialogue">Dialogue</option>
<option value="general">General</option>
<option value="punctuation">Punctuation</option>
<option value="vocabulary">Vocabulary</option>
</select></label>
<label for="metric-state-select">Measurement availability
<select id="metric-state-select" aria-controls="retained-metric-rows">
<option value="all">All states</option>
<option value="measured">Measured (not parity)</option>
<option value="not_run">Not run</option>
<option value="unavailable">Actual unavailable</option>
</select></label>
<button id="metric-clear" type="button">Clear metric filters</button>
</div>
<p id="metric-result-count" role="status" aria-live="polite" aria-atomic="true"></p>
<p id="metric-no-results" hidden>No diagnostic rows match. Clear the filters to see all 28.</p>
</section>"""

FILTER_CSS = """
.metric-filters { margin: 1.1rem 0; padding: 1rem; border: 1px solid var(--line);
  border-radius: .5rem; background: var(--accent-soft); }
.metric-filters[hidden], #metric-no-results[hidden], #retained-metric-rows tr[hidden] {
  display: none !important; }
.metric-filter-grid { display:flex; flex-wrap:wrap; align-items:end; gap:.8rem; }
.metric-filter-grid label { display:grid; gap:.3rem; flex:1 1 12rem; min-width:min(100%,12rem);
  font:700 .85rem/1.4 system-ui,sans-serif; }
.metric-filter-grid input, .metric-filter-grid select, .metric-filter-grid button {
  min-height:44px; width:100%; padding:.55rem .7rem; border-radius:.35rem;
  border:1px solid var(--line); background:var(--surface); color:var(--ink);
  font:400 1rem/1.45 system-ui,sans-serif; }
.metric-filter-grid button { width:auto; cursor:pointer; font-weight:700; }
.metric-filter-grid button:disabled { cursor:default; opacity:.65; }
.metric-filter-grid :is(input,select,button):focus-visible {
  outline:3px solid var(--focus); outline-offset:3px; }
#metric-result-count { margin:.75rem 0 0; color:var(--muted); }
#metric-no-results { padding:.7rem; background:var(--surface); }
@media(max-width:650px) { .metric-filter-grid button { width:100%; } }
@media print {
  .metric-filters { display:none !important; }
  #retained-metric-rows tr[hidden] { display:table-row !important; }
}
"""

FILTER_JS = r"""/* Local-only table filtering: no network calls, manuscripts, tracking or persistence. */
(function () {
  'use strict';
  function ready() {
    const panel = document.getElementById('metric-filters');
    const query = document.getElementById('metric-query');
    const family = document.getElementById('metric-family-select');
    const state = document.getElementById('metric-state-select');
    const reset = document.getElementById('metric-clear');
    const feedback = document.getElementById('metric-result-count');
    const empty = document.getElementById('metric-no-results');
    const table = document.getElementById('retained-metric-rows');
    if (!panel || !query || !family || !state || !reset || !feedback || !empty || !table) return;
    const rows = Array.from(table.querySelectorAll('tr.metric-row'));
    const families = new Set(['dialogue', 'general', 'punctuation', 'vocabulary']);
    const states = new Set(['measured', 'not_run', 'unavailable']);
    if (rows.length !== 28 || rows.some(row =>
        !families.has(row.dataset.metricFamily) || !states.has(row.dataset.metricState))) return;
    function key(value) {
      return String(value || '').normalize('NFC').toLocaleLowerCase('ru-RU').replace(/ё/g, 'е');
    }
    // Search the metric label and stable machine ID, not the scientific caveat/status cells.
    const inventory = rows.map(row => {
      const label = row.querySelector('th[scope="row"]');
      return {row, label: key(label ? label.textContent : ''),
              family: row.dataset.metricFamily, state: row.dataset.metricState};
    });
    function refresh() {
      const needle = key(query.value.trim());
      const chosenFamily = family.value;
      const chosenState = state.value;
      let shown = 0;
      inventory.forEach(item => {
        const visible = (!needle || item.label.includes(needle)) &&
          (chosenFamily === 'all' || chosenFamily === item.family) &&
          (chosenState === 'all' || chosenState === item.state);
        item.row.hidden = !visible;
        if (visible) shown++;
      });
      feedback.textContent = `${shown} of ${rows.length} diagnostic rows shown (not parity)`;
      empty.hidden = shown !== 0;
      reset.disabled = !needle && chosenFamily === 'all' && chosenState === 'all';
    }
    query.addEventListener('input', refresh);
    family.addEventListener('change', refresh);
    state.addEventListener('change', refresh);
    reset.addEventListener('click', () => {
      query.value = '';
      family.value = 'all';
      state.value = 'all';
      refresh();
      query.focus();
    });
    document.querySelectorAll('#metric-families a[href^="#metric-family-"]').forEach(link => {
      link.addEventListener('click', () => {
        const slug = link.getAttribute('href').slice('#metric-family-'.length);
        if (!families.has(slug)) return;
        // Reveal the jump target before the browser processes the fragment.
        query.value = '';
        family.value = slug;
        state.value = 'all';
        refresh();
      });
    });
    panel.hidden = false;
    refresh();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ready, {once: true});
  } else { ready(); }
})();
"""
