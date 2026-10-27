/* Exercises actual Pages routing functions without a browser, network or dependencies.
 * Source text is extracted from the shipped script, not reimplemented in the test.
 */
"use strict";
const fs = require("node:fs");
const assert = require("node:assert/strict");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(root, "assets/pages-reader.js"), "utf8");
const catalog = JSON.parse(fs.readFileSync(path.join(root, "assets/evidence-snapshot.json"), "utf8"));
const start = source.indexOf("  function bookFromUrl() {");
const end = source.indexOf("  function updateChart() {", start);
assert(start >= 0 && end > start, "route functions not found in shipped JavaScript");
const code = source.slice(start, end);
const books = catalog.books.filter(b => b.text_status === "measured");
const getBook = key => books.find(b => b.key === key);
const window = {
  location: new URL("https://drevendev.github.io/Scriptorium/?book=beketova#measurements"),
  history: { pushes: [], pushState(_state, _title, url) {
    this.pushes.push(String(url));
    window.location = new URL(String(url), window.location.href);
  }}
};
const one = {value: "anna"};
const search = {value: "stale filter"};
const focus = {count: 0, focus({preventScroll}) { assert.equal(preventScroll, true); this.count++; }};
const scroll = {count: 0, scrollIntoView(options) { assert.equal(options.behavior, "auto"); this.count++; }};
const direct = {href: "", textContent: ""};
const el = id => ({
  "share-work": direct,
  "measurements": scroll,
  "measurements-title": focus
})[id];
let renders = 0;
const routes = new Function("window", "getBook", "one", "search", "updateSingle", "el",
  'let currentBook = "anna";\n' + code +
  '\nreturn {bookFromUrl,selectBook,current:()=>currentBook};'
)(window, getBook, one, search, () => { renders++; }, el);

assert.equal(routes.bookFromUrl(), "beketova");
routes.selectBook(routes.bookFromUrl());
assert.equal(routes.current(), "beketova");
assert.equal(one.value, "beketova");
assert.equal(search.value, "");
assert.match(direct.href, /^\\?book=beketova#measurements$/);
assert.match(direct.textContent, /Бекетова|Гранта/);
assert.equal(window.history.pushes.length, 0);
assert.equal(renders, 1);

routes.selectBook("silver", true, true);
assert.equal(window.location.search, "?book=silver");
assert.equal(window.location.hash, "#measurements");
assert.equal(focus.count, 1);
assert.equal(scroll.count, 1);
assert.equal(window.history.pushes.length, 1);
assert.equal(routes.current(), "silver");

// Unknown and pending IDs are never source paths or fabricated book measurements.
for (const bad of ["resurrection", "../../secrets", "SILVER", "", "__proto__"]) {
  window.location = new URL("https://drevendev.github.io/Scriptorium/?book=" + encodeURIComponent(bad));
  assert.equal(routes.bookFromUrl(), "anna");
}
const before = renders;
routes.selectBook("resurrection", true, true);
assert.equal(renders, before);
assert.equal(window.history.pushes.length, 1);

// Native back/forward navigation re-renders the previously selected edition.
window.location = new URL("https://drevendev.github.io/Scriptorium/?book=anna#measurements");
routes.selectBook(routes.bookFromUrl());
assert.equal(routes.current(), "anna");
assert.equal(one.value, "anna");
assert.equal(direct.href, "?book=anna#measurements");
assert.equal(window.history.pushes.length, 1);
console.log("Pages per-work deep links: valid, translated, unknown, pending, history, focus PASS");
