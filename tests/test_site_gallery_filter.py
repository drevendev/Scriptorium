"""Unit and privacy regressions for the #283 evidence-gallery filters."""
import json
import shutil
import subprocess
import unittest

from scriptorium.site_gallery_filter import (
    evidence_kind, FILTER_JS, FILTER_CSS, FILTER_CONTROLS,
)


class GalleryFilterContractTests(unittest.TestCase):
    def test_mode_classification_is_presentation_only(self):
        cases = {
            "frozen_diagnostic": "full_work",
            "comparison": "comparison",
            "provenance": "provenance",
        }
        for mode, expected in cases.items():
            with self.subTest(mode=mode):
                self.assertEqual(
                    evidence_kind({"render_mode": mode, "publication_status": "diagnostic"}),
                    expected,
                )
        self.assertEqual(evidence_kind({"publication_status": "illustrative_excerpt"}), "excerpt")
        self.assertEqual(evidence_kind({"publication_status": "diagnostic"}), "other")
        self.assertEqual(
            evidence_kind({"render_mode": "unknown", "publication_status": "diagnostic"}),
            "other",
        )

    def test_zero_js_fallback_keeps_all_cards_visible(self):
        self.assertIn('id="evidence-filters"', FILTER_CONTROLS)
        self.assertIn("hidden>", FILTER_CONTROLS)
        self.assertIn("panel.hidden = false", FILTER_JS)
        self.assertIn("if (cards.length === 0) return", FILTER_JS)
        self.assertIn(".card[hidden]", FILTER_CSS)

    def test_accessible_controls_and_feedback(self):
        for term in ('type="search"', "<select", 'aria-controls="works"',
                     'role="status"', 'aria-live="polite"',
                     "No evidence pages match", "Clear filters"):
            with self.subTest(term=term):
                self.assertIn(term, FILTER_CONTROLS)
        self.assertIn('aria-keyshortcuts="/" ', FILTER_CONTROLS)
        self.assertIn('<option value="comparison">Comparisons</option>', FILTER_CONTROLS)
        self.assertIn('<option value="full_work">Measured full works</option>', FILTER_CONTROLS)
        self.assertIn('aria-describedby="filter-shortcut-help"', FILTER_CONTROLS)
        self.assertIn("Escape clears only the query", FILTER_CONTROLS)
        self.assertIn(".filter-shortcut-help", FILTER_CSS)
        self.assertIn("min-height: 44px", FILTER_CSS)
        self.assertIn(":focus-visible", FILTER_CSS)

    def test_search_only_title_author_and_russian_normalization(self):
        self.assertNotIn("card.textContent", FILTER_JS)
        self.assertIn("card.querySelector('h2')", FILTER_JS)
        self.assertIn("card.querySelector('h2 + p')", FILTER_JS)
        self.assertIn("normalize('NFC')", FILTER_JS)
        self.assertIn("toLocaleLowerCase('ru-RU')", FILTER_JS)
        self.assertIn("replace(/ё/g, 'е')", FILTER_JS)
        self.assertIn("!titleKnown", FILTER_JS)
        self.assertIn("terms.every(term => key.includes(term)", FILTER_JS)
        self.assertIn("latinKey(label, 'yo')", FILTER_JS)
        self.assertIn("latinKey(label, 'e')", FILTER_JS)
        self.assertIn("card.querySelector('h2 + p')", FILTER_JS)

    @unittest.skipUnless(shutil.which("node"), "Node unavailable; static contract checks still run")
    def test_real_filter_js_matches_unordered_terms_without_text_leak(self):
        # Execute the shipped JS, not a Python imitation of its matching rules.
        script = "const source = " + json.dumps(FILTER_JS) + ";\n"
        script += r"""
const vm = require("node:vm"), assert = require("node:assert/strict");
function card(title, author, kind) {
  return {
    hidden: false, dataset: {evidenceKind: kind},
    querySelector(selector) {
      if (selector === "h2") return {textContent: title};
      if (selector === "h2 + p") return {textContent: author};
      return null;
    }
  };
}
function control(value = "") {
  return {value, listeners: {}, addEventListener(type, cb) {this.listeners[type] = cb;}};
}
const cards = [
  card("Бегущая по волнам", "Александр Грин", "full_work"),
  card("Тихий Дон", "Михаил Шолохов", "full_work"),
  card("Ёжик в тумане", "Семён", "excerpt")
];
const panel = {hidden: true}, input = control(), kind = control("all");
const reset = control(), status = {textContent: ""}, empty = {hidden: true};
reset.disabled = true; input.focus = () => {input.focused = true;};
const nodes = {
  "evidence-filters": panel, "filter-query": input, "filter-kind": kind,
  "filter-reset": reset, "filter-count": status, "filter-empty": empty,
  "works": {querySelectorAll() {return cards;}}
};
const keyHandlers = {};
input.tagName = "INPUT"; kind.tagName = "SELECT";
const document = {
  readyState: "complete", getElementById(id) {return nodes[id];},
  addEventListener(type, handler) {keyHandlers[type] = handler;}
};
function keydown(key, target, extra = {}) {
  let prevented = false;
  keyHandlers.keydown({
    key, target, preventDefault() {prevented = true;}, ...extra
  });
  return prevented;
}
vm.runInNewContext(source, {document});
assert.equal(panel.hidden, false);
assert.equal(keydown("/", {tagName: "MAIN"}), true);
assert.equal(input.focused, true);
input.focused = false;
assert.equal(keydown("/", input), false); // Native slash typing remains possible.
assert.equal(keydown("/", {tagName: "TEXTAREA"}), false);
assert.equal(keydown("/", {isContentEditable: true, tagName: "SPAN"}), false);
assert.equal(keydown("/", {tagName: "MAIN"}, {ctrlKey: true}), false);
assert.equal(keydown("/", {tagName: "MAIN"}, {isComposing: true}), false);
assert.equal(keydown("/", {tagName: "MAIN"}, {defaultPrevented: true}), false);
assert.equal(input.focused, false);
function query(value) {input.value = value; input.listeners.input();}
query("Грин волнам"); assert.deepEqual(cards.map(c=>!c.hidden), [true,false,false]);
query("волнам   Грин"); assert.deepEqual(cards.map(c=>!c.hidden), [true,false,false]);
query("Grin volnam"); assert.deepEqual(cards.map(c=>!c.hidden), [true,false,false]);
query("VOLNAM grin"); assert.deepEqual(cards.map(c=>!c.hidden), [true,false,false]);
query("Грин volnam"); assert.deepEqual(cards.map(c=>!c.hidden), [true,false,false]);
query("Sholokhov"); assert.deepEqual(cards.map(c=>!c.hidden), [false,true,false]);
query("Ёжик Семён"); assert.deepEqual(cards.map(c=>!c.hidden), [false,false,true]);
query("ежик семен"); assert.deepEqual(cards.map(c=>!c.hidden), [false,false,true]);
query("yozhik"); assert.deepEqual(cards.map(c=>!c.hidden), [false,false,true]);
query("ezhik"); assert.deepEqual(cards.map(c=>!c.hidden), [false,false,true]);
query("Грин Шолохов"); assert.equal(cards.filter(c=>!c.hidden).length, 0);
query("Grin Sholokhov"); assert.equal(cards.filter(c=>!c.hidden).length, 0);
query("Grin ocean"); assert.equal(cards.filter(c=>!c.hidden).length, 0); // No translation or fuzzy matching.
assert.equal(empty.hidden, false);
assert.match(status.textContent, /0 of 3/);
query("Грин"); kind.value = "full_work"; kind.listeners.change();
assert.equal(keydown("Escape", input), true);
assert.equal(input.value, "");
assert.equal(kind.value, "full_work");
assert.deepEqual(cards.map(c=>!c.hidden), [true,true,false]);
assert.equal(keydown("Escape", input), false); // Empty query: preserve native Escape.
query("Грин"); kind.value = "excerpt"; kind.listeners.change();
assert.equal(cards.filter(c=>!c.hidden).length, 0);
reset.listeners.click();
assert.equal(input.value, ""); assert.equal(kind.value, "all");
assert.equal(reset.disabled, true); assert.equal(input.focused, true);
assert.equal(cards.filter(c=>!c.hidden).length, 3);
assert.equal(empty.hidden, true);
console.log("Gallery Cyrillic/Romanized title/author matching, privacy, keyboard and facets PASS");
"""
        result = subprocess.run(["node", "-"], input=script, text=True,
                                capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_never_uploads_or_tracks_queries(self):
        forbidden = ("fetch(", "XMLHttpRequest", "sendBeacon", "localStorage",
                     "sessionStorage", "document.cookie", "innerHTML =",
                     "navigator.", "window.location")
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, FILTER_JS)
        self.assertIn("status.textContent =", FILTER_JS)


if __name__ == "__main__":
    unittest.main()
