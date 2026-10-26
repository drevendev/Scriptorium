"""Interactive/no-JS acceptance for the independent 20-row evidence comparison."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from scriptorium import site_benchmark_matrix
from scriptorium.site_shared_metric_filter import CONTROLS, CSS, JS


ROOT = Path(__file__).resolve().parents[1]


class SharedMetricFilterTests(unittest.TestCase):
    def test_accessibility_and_no_script_or_print_regression(self):
        for marker in ('id="shared-rate-filters"', 'aria-controls="shared-metric-rows"',
                       'aria-live="polite"', 'type="search"', 'hidden>'):
            self.assertIn(marker, CONTROLS)
        self.assertIn('#shared-metric-rows tr[hidden]', CSS)
        self.assertIn('display:table-row !important;', CSS)
        self.assertIn('.shared-rate-filters { display:none !important; }', CSS)
        for forbidden in ('fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage',
                          'sessionStorage', 'document.cookie', 'innerHTML'):
            self.assertNotIn(forbidden, JS)

    def test_canonical_site_contains_controls_and_unchanged_science(self):
        result = site_benchmark_matrix.build(ROOT)
        page = result['body']
        self.assertEqual(page.count('class="cross-metric-row" data-metric-family='), 20)
        self.assertEqual(page.count('id="shared-metric-rows"'), 1)
        self.assertEqual(page.count('id="shared-rate-filters"'), 1)
        self.assertIn('src="../../assets/shared-metric-filter.js"', page)
        self.assertIn('src="../../assets/metric-filter.js"', page)
        document = json.loads(result['shared_json'])
        self.assertEqual(len(document['measurements']), 20)
        self.assertEqual(document['evidence_class'], 'diagnostic_source_unmatched')
        self.assertIs(document['m2_parity_admissible'], False)
        self.assertEqual(document['m2_weight'], 0)

    @unittest.skipUnless(shutil.which('node'), 'Node required for DOM interaction test')
    def test_search_family_empty_reset_and_invalid_family_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / 'shared-filter.js'
            script.write_text(JS, encoding='utf-8')
            harness = r"""
const assert = require('node:assert/strict');
class Element {
  constructor(id) {
    this.id = id; this.value = 'all'; this.hidden = true;
    this.disabled = false; this.textContent = ''; this.handlers = {};
    this.focusCount = 0;
  }
  addEventListener(name, callback) { this.handlers[name] = callback; }
  focus() { this.focusCount++; }
}
const ids = ['shared-rate-filters', 'shared-rate-query', 'shared-rate-family',
             'shared-rate-clear', 'shared-rate-count', 'shared-rate-empty',
             'shared-metric-rows'];
const elements = Object.fromEntries(ids.map(id => [id, new Element(id)]));
elements['shared-rate-query'].value = '';
let rows = Array.from({length:20}, (_,i)=>({
  hidden:false,
  dataset:{metricFamily:i<3?'general':i<6?'dialogue':i<8?'vocabulary':'punctuation'},
  querySelector(selector) {
    assert.equal(selector, 'th[scope="row"]');
    return {textContent:i===3?'Ёмкость · fantlab.dialogue.share_percent':
            'Metric '+i+' · fantlab.punctuation.foo'+i};
  }
}));
elements['shared-metric-rows'].querySelectorAll = selector => {
  assert.equal(selector, 'tr.cross-metric-row'); return rows;
};
global.document = {readyState:'complete', getElementById:id=>elements[id]};
require(process.argv[1]);
const input=elements['shared-rate-query'], family=elements['shared-rate-family'],
  clear=elements['shared-rate-clear'], panel=elements['shared-rate-filters'];
const count=()=>rows.filter(row=>!row.hidden).length;
assert.equal(panel.hidden, false); assert.equal(count(),20);
assert.match(elements['shared-rate-count'].textContent, /20 of 20/);
input.value='емкость';input.handlers.input();assert.equal(count(),1);
input.value='NOT FOUND';input.handlers.input();assert.equal(count(),0);
assert.equal(elements['shared-rate-empty'].hidden, false);
input.value='';input.handlers.input();assert.equal(count(),20);
family.value='dialogue';family.handlers.change();assert.equal(count(),3);
clear.handlers.click();assert.equal(count(),20);assert.equal(family.value,'all');
assert.equal(clear.disabled,true);assert.equal(input.focusCount,1);
// Scientific evidence drift must not silently filter or suppress any row.
panel.hidden=true;
rows[0].dataset.metricFamily='parity_pass';
delete require.cache[require.resolve(process.argv[1])];
require(process.argv[1]);
assert.equal(panel.hidden,true);assert.equal(count(),20);
"""
            output = subprocess.run(['node', '-e', harness, str(script)],
                                    text=True, capture_output=True, timeout=30)
            self.assertEqual(output.returncode, 0, output.stderr)


if __name__ == '__main__':
    unittest.main()
