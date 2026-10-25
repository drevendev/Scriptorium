"""Browser-like behavior and fallback contracts for the FantLab metric explorer."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from scriptorium.site_metric_filter import FILTER_CONTROLS, WAVE_FILTER_CONTROLS, FILTER_CSS, FILTER_JS


class MetricExplorerTests(unittest.TestCase):
    def test_no_js_fallback_accessibility_and_print_inclusion(self):
        self.assertIn('id="metric-filters"', FILTER_CONTROLS)
        self.assertIn('aria-label="Explore Anna Karenina', FILTER_CONTROLS)
        self.assertIn('hidden>', FILTER_CONTROLS)
        self.assertIn('aria-controls="retained-metric-rows"', FILTER_CONTROLS)
        self.assertIn('aria-live="polite"', FILTER_CONTROLS)
        self.assertIn('type="search"', FILTER_CONTROLS)
        self.assertIn('min-height:44px', FILTER_CSS)
        self.assertIn('focus-visible', FILTER_CSS)
        self.assertIn('@media print', FILTER_CSS)
        self.assertIn('#retained-metric-rows tr[hidden] { display:table-row !important; }', FILTER_CSS)

    def test_waves_no_js_and_print_fallback(self):
        self.assertIn('id="wave-metric-filters"', WAVE_FILTER_CONTROLS)
        self.assertIn('aria-label="Explore Running on Waves', WAVE_FILTER_CONTROLS)
        self.assertIn('aria-controls="wave-metric-rows"', WAVE_FILTER_CONTROLS)
        self.assertIn('aria-live="polite"', WAVE_FILTER_CONTROLS)
        self.assertIn('hidden>', WAVE_FILTER_CONTROLS)
        self.assertIn('#wave-metric-rows tr[hidden]', FILTER_CSS)
        self.assertIn('#wave-metric-rows tr[hidden] { display:table-row !important; }', FILTER_CSS)

    def test_search_is_private_and_scoped_to_metric_identity(self):
        for forbidden in ('fetch(', 'XMLHttpRequest', 'sendBeacon',
                          'localStorage', 'sessionStorage', 'document.cookie',
                          'innerHTML', 'navigator.', 'window.location'):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, FILTER_JS)
        self.assertIn("row.querySelector('th[scope=\"row\"]')", FILTER_JS)
        self.assertIn("normalize('NFC')", FILTER_JS)
        self.assertIn("replace(/ё/g, 'е')", FILTER_JS)
        self.assertIn("rows.length !== 28", FILTER_JS)
        self.assertIn("rows.length !== 27", FILTER_JS)
        self.assertIn("wave-metric-rows", FILTER_JS)

    @unittest.skipUnless(shutil.which('node'), 'Node required for actual JS filtering regression')
    def test_filters_reset_navigation_empty_and_print_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / 'metric-filter.js'
            script.write_text(FILTER_JS, encoding='utf-8')
            harness = r"""
const assert = require('node:assert/strict');
class Element {
  constructor(id) {
    this.id = id;
    this.handlers = {};
    this.value = 'all';
    this.textContent = '';
    this.hidden = true;
    this.disabled = false;
    this.focusCount = 0;
  }
  addEventListener(name, callback) { this.handlers[name] = callback; }
  focus() { this.focusCount++; }
}
const ids = ['metric-filters', 'metric-query', 'metric-family-select', 'metric-state-select',
  'metric-clear', 'metric-result-count', 'metric-no-results', 'retained-metric-rows'];
const elements = Object.fromEntries(ids.map(id => [id, new Element(id)]));
elements['metric-query'].value = '';
const labels = ['Длина текста · fantlab.general.characters',
  'Ёмкость · fantlab.vocabulary.active_dictionary', 'Удельный словарь'];
const rows = Array.from({length: 28}, (_, i) => ({
  dataset: {metricFamily: i === 0 ? 'general' : i < 3 ? 'vocabulary' :
    i < 7 ? 'dialogue' : 'punctuation',
    metricState: i === 1 ? 'not_run' : i === 2 ? 'unavailable' : 'measured'},
  hidden: false,
  querySelector: selector => {
    assert.equal(selector, 'th[scope="row"]');
    return {textContent: labels[i] || 'Punctuation ' + i};
  }
}));
elements['retained-metric-rows'].querySelectorAll = selector => {
  assert.equal(selector, 'tr.metric-row');
  return rows;
};
const links = ['dialogue', 'general', 'punctuation', 'vocabulary'].map(name => ({
  name, handlers: {},
  getAttribute(attribute) { assert.equal(attribute, 'href'); return '#metric-family-' + this.name; },
  addEventListener(event, callback) { this.handlers[event] = callback; },
}));
global.document = {
  readyState: 'complete',
  getElementById: id => elements[id],
  querySelectorAll: selector => {
    assert.equal(selector, '#metric-families a[href^="#metric-family-"]');
    return links;
  },
};
require(process.argv[1]);
const q = elements['metric-query'], f = elements['metric-family-select'];
const s = elements['metric-state-select'], clear = elements['metric-clear'];
const count = () => rows.filter(r => !r.hidden).length;
assert.equal(elements['metric-filters'].hidden, false);
assert.equal(count(), 28);
assert.match(elements['metric-result-count'].textContent, /28 of 28/);
q.value = 'ДЛИНА'; q.handlers.input(); assert.equal(count(), 1);
q.value = 'емкость'; q.handlers.input(); assert.equal(count(), 1);
q.value = ''; q.handlers.input(); assert.equal(count(), 28);
s.value = 'not_run'; s.handlers.change(); assert.equal(count(), 1);
s.value = 'unavailable'; s.handlers.change(); assert.equal(count(), 1);
s.value = 'measured'; s.handlers.change(); assert.equal(count(), 26);
f.value = 'vocabulary'; f.handlers.change(); assert.equal(count(), 0);
assert.equal(elements['metric-no-results'].hidden, false);
links[0].handlers.click();
assert.equal(f.value, 'dialogue');
assert.equal(s.value, 'all');
assert.equal(count(), 4); // Jump target must be visible before anchor navigation.
clear.handlers.click();
assert.equal(count(), 28);
assert.equal(f.value, 'all');
assert.equal(clear.disabled, true);
assert.equal(q.focusCount, 1);
assert.equal(rows.length, 28); // JS never removes scientific rows.
"""
            proc = subprocess.run(['node', '-e', harness, str(script)],
                                  text=True, capture_output=True, timeout=30)
            self.assertEqual(proc.returncode, 0, proc.stderr)


    @unittest.skipUnless(shutil.which('node'), 'Node required for Waves filtering regression')
    def test_waves_filter_is_independent_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / 'metric-filter.js'
            script.write_text(FILTER_JS, encoding='utf-8')
            harness = r"""
const assert = require('node:assert/strict');
class Element {
  constructor(id) {
    this.id = id;
    this.handlers = {};
    this.value = 'all';
    this.textContent = '';
    this.hidden = true;
    this.disabled = false;
    this.focusCount = 0;
  }
  addEventListener(name, handler) { this.handlers[name] = handler; }
  focus() { this.focusCount++; }
}
const names = ['wave-metric-filters','wave-metric-query','wave-metric-family',
  'wave-metric-state','wave-metric-clear','wave-metric-result-count',
  'wave-metric-no-results','wave-metric-rows'];
const elements = Object.fromEntries(names.map(name => [name, new Element(name)]));
elements['wave-metric-query'].value = '';
let rows = Array.from({length: 27}, (_, i) => ({
  dataset: {metricFamily: i < 5 ? 'general' : i < 8 ? 'dialogue' :
    i < 14 ? 'vocabulary' : 'punctuation',
    metricState: i < 4 ? 'not_run' : 'measured'},
  hidden: false,
  querySelector: selector => {
    assert.equal(selector, 'th[scope="row"]');
    return {textContent: i === 5 ? 'Ёмкость / fantlab.dialogue.share_percent' :
      'Metric ' + i};
  }
}));
elements['wave-metric-rows'].querySelectorAll = selector => {
  assert.equal(selector, 'tr.wave-metric-row');
  return rows;
};
global.document = {
  readyState: 'complete',
  getElementById: id => elements[id],
};
require(process.argv[1]);
const query = elements['wave-metric-query'];
const family = elements['wave-metric-family'];
const state = elements['wave-metric-state'];
const clear = elements['wave-metric-clear'];
const count = () => rows.filter(row => !row.hidden).length;
assert.equal(elements['wave-metric-filters'].hidden, false);
assert.equal(count(), 27);
assert.match(elements['wave-metric-result-count'].textContent, /27 of 27/);
query.value = 'емкость';
query.handlers.input();
assert.equal(count(), 1);
query.value = '';
query.handlers.input();
state.value = 'not_run';
state.handlers.change();
assert.equal(count(), 4);
family.value = 'punctuation';
family.handlers.change();
assert.equal(count(), 0);
assert.equal(elements['wave-metric-no-results'].hidden, false);
clear.handlers.click();
assert.equal(count(), 27);
assert.equal(query.focusCount, 1);
assert.equal(clear.disabled, true);
// Corrupt coverage: do not activate controls or modify source rows.
elements['wave-metric-filters'].hidden = true;
rows[0].dataset.metricState = 'passed';
delete require.cache[require.resolve(process.argv[1])];
require(process.argv[1]);
assert.equal(elements['wave-metric-filters'].hidden, true);
assert.equal(count(), 27);
"""
            proc = subprocess.run(['node', '-e', harness, str(script)],
                                  text=True, capture_output=True, timeout=30)
            self.assertEqual(proc.returncode, 0, proc.stderr)

if __name__ == '__main__':
    unittest.main()
