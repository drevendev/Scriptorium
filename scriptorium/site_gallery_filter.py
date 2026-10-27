"""Progressive, local-only filters for the Scriptorium evidence gallery.

Navigation categories are not evidence, parity or corpus-admissibility claims.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def evidence_kind(item: Mapping[str, Any]) -> str:
    """Classify presentation modes, not scientific evidence status."""
    mode = item.get("render_mode")
    if mode in {"frozen_diagnostic", "hyperboloid_diagnostic", "beketova_diagnostic", "comparison"}:
        return "full_work"
    if mode == "provenance":
        return "provenance"
    if item.get("publication_status") == "illustrative_excerpt":
        return "excerpt"
    return "other"


FILTER_CONTROLS = """<section id="evidence-filters" class="evidence-filters" aria-label="Find evidence" hidden>
<div class="filter-fields"><label for="filter-query">Search works and authors
<input id="filter-query" type="search" autocomplete="off" placeholder="e.g. Tolstoy or Grin" aria-controls="works"></label>
<label for="filter-kind">Evidence type
<select id="filter-kind" aria-controls="works"><option value="all">All evidence</option>
<option value="full_work">Full-work measurements &amp; comparisons</option>
<option value="excerpt">Illustrative excerpts</option><option value="provenance">Provenance-only pages</option></select></label>
<button type="button" id="filter-reset">Clear filters</button></div>
<p id="filter-count" class="filter-count" role="status" aria-live="polite" aria-atomic="true"></p>
<p id="filter-empty" class="empty-state" hidden>No evidence pages match these filters. Clear the filters to see everything.</p>
</section>"""


FILTER_CSS = """
/* Without JavaScript every allow-listed evidence card stays visible. */
.evidence-filters { margin: 1.5rem 0 0; padding: 1.2rem; background: var(--accent-soft);
  border: 1px solid var(--line); border-radius: .5rem; }
.evidence-filters[hidden], .card[hidden], .empty-state[hidden] { display: none !important; }
.filter-fields { display: flex; flex-wrap: wrap; gap: .9rem; align-items: end; }
.filter-fields label { display: grid; gap: .35rem; min-width: min(100%, 15rem);
  flex: 1 1 15rem; font: 700 .88rem/1.45 system-ui, sans-serif; }
.filter-fields input, .filter-fields select, .filter-fields button { width: 100%; min-height: 44px;
  border: 1px solid var(--line); border-radius: .35rem; padding: .6rem .7rem;
  color: var(--ink); background: var(--surface); font: 400 1rem/1.4 system-ui,sans-serif; }
.filter-fields button { width: auto; font-weight: 700; cursor: pointer; }
.filter-fields button:disabled { cursor: default; opacity: .65; }
.filter-fields input:focus-visible, .filter-fields select:focus-visible,
.filter-fields button:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
.filter-count { margin: .8rem 0 0; font: .91rem/1.55 system-ui,sans-serif; color: var(--muted); }
.empty-state { background: var(--surface); padding: 1rem; margin-top: 1rem; }
@media(max-width:650px) { .filter-fields button { width: 100%; } }
"""


FILTER_JS = r"""/* No uploads, network requests, cookies, tracking or stored queries. */
(function () {
  'use strict';
  function ready() {
    const panel = document.getElementById('evidence-filters');
    const input = document.getElementById('filter-query');
    const kind = document.getElementById('filter-kind');
    const reset = document.getElementById('filter-reset');
    const status = document.getElementById('filter-count');
    const empty = document.getElementById('filter-empty');
    const work = document.getElementById('works');
    if (!panel || !input || !kind || !reset || !status || !empty || !work) return;
    const cards = Array.from(work.querySelectorAll('article.card[data-evidence-kind]'));
    if (cards.length === 0) return;
    // Restrict search to visible title/author fields, not scientific warning text.
    function searchKey(value) {
      return String(value || '').normalize('NFC').toLocaleLowerCase('ru-RU').replace(/ё/g, 'е');
    }
    const inventory = cards.map(card => {
      const heading = card.querySelector('h2');
      const byline = card.querySelector('h2 + p');
      return {
        card,
        titleKnown: Boolean(heading && heading.textContent.trim()),
        key: searchKey(`${heading ? heading.textContent : ''} ${byline ? byline.textContent : ''}`),
      };
    });
    function refresh() {
      const query = searchKey(input.value.trim());
      const chosen = kind.value;
      let visible = 0;
      inventory.forEach(({card, titleKnown, key}) => {
        const match = (!query || !titleKnown || key.includes(query)) &&
          (chosen === 'all' || card.dataset.evidenceKind === chosen);
        card.hidden = !match;
        if (match) visible++;
      });
      status.textContent = `${visible} of ${cards.length} evidence pages shown`;
      empty.hidden = visible !== 0;
      reset.disabled = query === '' && chosen === 'all';
    }
    input.addEventListener('input', refresh);
    kind.addEventListener('change', refresh);
    reset.addEventListener('click', () => {
      input.value = '';
      kind.value = 'all';
      refresh();
      input.focus();
    });
    panel.hidden = false;
    refresh();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ready, { once: true });
  } else { ready(); }
})();
"""
