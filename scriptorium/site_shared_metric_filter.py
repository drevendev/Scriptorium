"""Local-only progressive filtering of the twenty frozen shared diagnostic rates.

The underlying table, downloads, source identities and parity gates never change.
No script means no filtering: every row stays available.
"""

CONTROLS = """<section id="shared-rate-filters" class="shared-rate-filters"
  aria-label="Explore the twenty shared measured cross-work rates" hidden>
<div class="shared-rate-fields">
<label for="shared-rate-query">Search metric name or ID
<input id="shared-rate-query" type="search" autocomplete="off"
 placeholder="e.g. диалоги, punctuation" aria-controls="shared-metric-rows"></label>
<label for="shared-rate-family">Metric family
<select id="shared-rate-family" aria-controls="shared-metric-rows">
<option value="all">All families</option>
<option value="dialogue">Dialogue</option>
<option value="general">General</option>
<option value="punctuation">Punctuation</option>
<option value="vocabulary">Vocabulary</option>
</select></label>
<button id="shared-rate-clear" type="button">Clear comparison filters</button>
</div>
<p id="shared-rate-count" role="status" aria-live="polite" aria-atomic="true"></p>
<p id="shared-rate-empty" hidden>No shared rates match. Clear filters to see all twenty.</p>
</section>"""

CSS = """
.shared-rate-filters { margin:1rem 0; padding:1rem; background:var(--accent-soft);
 border:1px solid var(--line); border-radius:.5rem; }
.shared-rate-filters[hidden], #shared-rate-empty[hidden],
#shared-metric-rows tr[hidden] { display:none !important; }
.shared-rate-fields { display:flex; flex-wrap:wrap; align-items:end; gap:.75rem; }
.shared-rate-fields label { display:grid; gap:.3rem; flex:1 1 12rem;
 min-width:min(100%,12rem); font:700 .85rem/1.4 system-ui,sans-serif; }
.shared-rate-fields :is(input,select,button) { min-height:44px; width:100%;
 padding:.55rem .7rem; border:1px solid var(--line); border-radius:.35rem;
 background:var(--surface); color:var(--ink); font:400 1rem/1.4 system-ui,sans-serif; }
.shared-rate-fields button { width:auto; cursor:pointer; font-weight:700; }
.shared-rate-fields button:disabled { cursor:default; opacity:.65; }
.shared-rate-fields :is(input,select,button):focus-visible {
 outline:3px solid var(--focus); outline-offset:3px; }
#shared-rate-count { margin:.7rem 0 0; color:var(--muted); }
#shared-rate-empty { padding:.7rem; background:var(--surface); }
@media (max-width:650px) { .shared-rate-fields button { width:100%; } }
@media print {
 .shared-rate-filters { display:none !important; }
 #shared-metric-rows tr[hidden] { display:table-row !important; }
}
"""

JS = r"""/* Private/offline table search. No fetch, storage, cookies, or telemetry. */
(function () {
  'use strict';
  function ready() {
    const panel = document.getElementById('shared-rate-filters');
    const query = document.getElementById('shared-rate-query');
    const family = document.getElementById('shared-rate-family');
    const clear = document.getElementById('shared-rate-clear');
    const count = document.getElementById('shared-rate-count');
    const empty = document.getElementById('shared-rate-empty');
    const body = document.getElementById('shared-metric-rows');
    if (!panel || !query || !family || !clear || !count || !empty || !body) return;
    const rows = Array.from(body.querySelectorAll('tr.cross-metric-row'));
    const families = new Set(['dialogue','general','punctuation','vocabulary']);
    // Refuse partial or reclassified evidence: leave the complete static table visible.
    if (rows.length !== 20 || rows.some(row =>
        !families.has(row.dataset.metricFamily) ||
        !row.querySelector('th[scope="row"]') ||
        !row.querySelector('th[scope="row"]').textContent.trim())) return;
    function key(value) {
      return String(value || '').normalize('NFC').toLocaleLowerCase('ru-RU').replace(/ё/g,'е');
    }
    const inventory = rows.map(row => ({
      row, family:row.dataset.metricFamily,
      label:key(row.querySelector('th[scope="row"]').textContent)
    }));
    function update() {
      const needle = key(query.value.trim());
      const chosen = family.value;
      let visible = 0;
      inventory.forEach(item => {
        const matches = (!needle || item.label.includes(needle)) &&
          (chosen === 'all' || item.family === chosen);
        item.row.hidden = !matches;
        if (matches) visible++;
      });
      count.textContent = visible + ' of 20 measured cross-work rows shown (not parity)';
      empty.hidden = visible !== 0;
      clear.disabled = !needle && chosen === 'all';
    }
    query.addEventListener('input', update);
    family.addEventListener('change', update);
    clear.addEventListener('click', () => {
      query.value = ''; family.value = 'all'; update(); query.focus();
    });
    panel.hidden = false;
    update();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ready, {once:true});
  } else ready();
})();
"""
