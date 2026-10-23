"""Keyboard, live-feedback and async-race checks for the real browser comparison.

Executes the canonical generated JS with a minimal in-process DOM, not a second
comparison implementation. This is not a substitute for live browser/Pages QA.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from scriptorium.analyze import build_local_analysis
from scriptorium import site_browser_compare


class BrowserCompareKeyboardTests(unittest.TestCase):
    def test_result_heading_and_scroll_region_are_discoverable(self):
        body = site_browser_compare.BODY
        self.assertIn('<h2 id="comparison-title" tabindex="-1">', body)
        self.assertIn('id="comparison-scroll-help"', body)
        self.assertIn('aria-describedby="comparison-scroll-help"', body)
        self.assertIn('role="status" aria-live="polite"', body)
        self.assertIn('id="metric-filter" type="search"', body)
        self.assertIn('id="metric-filter-status" role="status"', body)
        self.assertIn('.private-desk tbody tr[hidden] { display: none !important; }',
                      site_browser_compare.CSS)
        self.assertIn('.private-desk tbody tr[hidden] { display: grid !important; }',
                      site_browser_compare.CSS)
        self.assertIn('#comparison-title:focus { outline: 3px solid var(--focus)',
                      site_browser_compare.CSS)
        print_rules = site_browser_compare.CSS.split('@media print {', 1)[1]
        self.assertIn('.private-desk .scroll-help { display: none !important; }',
                      print_rules.replace('.desk-panel, .private-desk .actions, ', ''))

    @unittest.skipUnless(shutil.which('node'), 'Node required for browser DOM behavior check')
    def test_valid_error_and_stale_comparisons_manage_keyboard_focus(self):
        with tempfile.TemporaryDirectory() as temp:
            js_file = Path(temp) / 'private-compare.js'
            js_file.write_text(site_browser_compare.render_script(), encoding='utf-8')
            cases = {
                'left': json.dumps(build_local_analysis('Кот спит. Собака бежит!'.encode('utf-8')), ensure_ascii=False),
                'right': json.dumps(build_local_analysis('Лес шумит. Ветер поёт!'.encode('utf-8')), ensure_ascii=False),
            }
            harness = r'''
const assert = require('node:assert/strict');
const fs = require('node:fs');
const cases = JSON.parse(fs.readFileSync(0, 'utf8'));
class Element {
  constructor(id) {
    this.id = id;
    this.handlers = {};
    this.files = [];
    this.children = [];
    this.hidden = false;
    this.disabled = false;
    this.textContent = '';
    this.value = '';
    this.focuses = 0;
  }
  addEventListener(name, callback) { this.handlers[name] = callback; }
  appendChild(node) { this.children.push(node); }
  replaceChildren(fragment) { this.children = fragment.children; }
  focus() { this.focuses++; }
  remove() {}
}
const ids = [
  'report-left', 'report-right', 'run-comparison', 'comparison-message',
  'comparison-result', 'comparison-title', 'comparison-rows',
  'source-summary', 'save-comparison-json', 'save-comparison-csv',
  'metric-filter', 'metric-filter-status'
];
const elements = Object.fromEntries(ids.map(id => [id, new Element(id)]));
global.document = {
  readyState: 'complete',
  getElementById: id => elements[id],
  createDocumentFragment: () => new Element('fragment'),
  createElement: tag => new Element(tag),
  body: new Element('body'),
};
require(process.argv[1]);
const left = elements['report-left'];
const right = elements['report-right'];
const button = elements['run-comparison'];
const heading = elements['comparison-title'];
const result = elements['comparison-result'];
const rows = elements['comparison-rows'];
const message = elements['comparison-message'];
const metricFilter = elements['metric-filter'];
const metricFilterStatus = elements['metric-filter-status'];
function file(source) {
  const bytes = new TextEncoder().encode(source);
  return {size: bytes.byteLength, arrayBuffer: async () =>
    bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)};
}
function chosen() {
  left.handlers.change();
  right.handlers.change();
}
(async () => {
  assert.equal(button.disabled, true);
  left.files = [file(cases.left)];
  right.files = [file(cases.right)];
  chosen();
  assert.equal(button.disabled, false);
  await button.handlers.click();
  assert.equal(result.hidden, false);
  assert.equal(heading.focuses, 1);
  assert.equal(rows.children.length, 29);
  assert.match(message.textContent, /29 measurements validated/);
  assert.equal(metricFilter.disabled, false);
  assert.match(metricFilterStatus.textContent, /29 of 29 metrics shown/);
  const first = rows.children[0].children[0].textContent;
  const firstId = first.slice(first.lastIndexOf('(') + 1, -1);
  metricFilter.value = firstId.toUpperCase();
  metricFilter.handlers.input();
  const matching = rows.children.filter(row => !row.hidden);
  assert.ok(matching.length > 0 && matching.length < 29);
  assert.match(metricFilterStatus.textContent, new RegExp(matching.length + ' of 29'));
  metricFilter.value = 'unlikely-filter-[]-no-results';
  metricFilter.handlers.input();
  assert.equal(rows.children.filter(row => !row.hidden).length, 0);
  assert.match(metricFilterStatus.textContent, /No matching metrics/);
  metricFilter.value = '';
  metricFilter.handlers.input();
  assert.equal(rows.children.filter(row => !row.hidden).length, 29);
  assert.equal(rows.children.length, 29); // Full export/print data remains untouched.

  // Invalid input retains focus on the comparison action; only the polite
  // live status announces the rejection. No stale results remain visible.
  right.files = [file('{"invalid":true}')];
  right.handlers.change();
  assert.equal(metricFilter.disabled, true);
  await button.handlers.click();
  assert.equal(result.hidden, true);
  assert.equal(heading.focuses, 1);
  assert.match(message.textContent, /Comparison rejected/);

  // A new file selection during an async read invalidates the previous
  // generation; the old result may not appear or steal keyboard focus.
  const accepted = file(cases.left);
  let release;
  left.files = [{size: accepted.size, arrayBuffer: () =>
    new Promise(resolve => { release = () => accepted.arrayBuffer().then(resolve); })}];
  right.files = [file(cases.right)];
  chosen();
  const inFlight = button.handlers.click();
  assert.equal(typeof release, 'function');
  left.handlers.change();
  release();
  await inFlight;
  assert.equal(result.hidden, true);
  assert.equal(heading.focuses, 1);
  assert.equal(button.disabled, false);
  process.stdout.write(JSON.stringify({success: true, row_count: 29}));
})().catch(error => { console.error(error); process.exitCode = 1; });
'''
            completed = subprocess.run(
                ['node', '-e', harness, str(js_file)],
                input=json.dumps(cases, ensure_ascii=False),
                capture_output=True, text=True, timeout=60, check=True,
            )
            self.assertEqual(json.loads(completed.stdout),
                             {'success': True, 'row_count': 29})


if __name__ == '__main__':
    unittest.main()
