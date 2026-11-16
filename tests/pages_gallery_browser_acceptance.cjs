/* Real Chromium acceptance for generated evidence gallery, NOT live Pages. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const http = require("node:http");
const {chromium} = require("playwright");
const root = path.resolve(__dirname, "../build/site");
const screenshots = path.resolve(__dirname, "../build/reader-browser-acceptance");
const mime = {".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",
  ".js":"text/javascript; charset=utf-8",".json":"application/json; charset=utf-8"};

function serve() {
  return http.createServer((req, res) => {
    try {
      const url = new URL(req.url, "http://127.0.0.1");
      if (req.method !== "GET" || url.pathname.includes("\0")) {
        res.writeHead(405).end(); return;
      }
      const decoded = decodeURIComponent(url.pathname);
      const relative = decoded.endsWith("/") ? decoded + "index.html" : decoded;
      const filename = path.resolve(root, "." + relative);
      if (!filename.startsWith(root + path.sep) || !fs.statSync(filename).isFile()) {
        res.writeHead(404).end(); return;
      }
      res.writeHead(200, {"Content-Type": mime[path.extname(filename)] || "application/octet-stream",
        "Cache-Control":"no-store","X-Content-Type-Options":"nosniff"});
      fs.createReadStream(filename).pipe(res);
    } catch (_) { res.writeHead(404).end(); }
  });
}

async function inspect(page, origin, label) {
  const errors = [], external = [];
  page.on("pageerror", error => errors.push(error.message));
  page.on("request", request => {
    if (!request.url().startsWith(origin + "/")) external.push(request.url());
  });
  const response = await page.goto(origin + "/", {waitUntil:"networkidle"});
  assert.equal(response.status(), 200, label + ": built gallery route");
  assert.match(await page.title(), /Scriptorium/);
  const total = await page.locator("#works article.card[data-evidence-kind]").count();
  assert.ok(total >= 6, label + ": source-backed cards present");
  assert.equal(await page.locator("#works article.card:visible").count(), total);
  assert.equal(await page.locator("#evidence-filters").isVisible(), true);
  assert.equal(await page.locator("#filter-count").getAttribute("role"), "status");
  assert.equal(await page.locator("#filter-query").getAttribute("aria-describedby"),
    "filter-shortcut-help");
  assert.equal(await page.locator("#filter-count").innerText(),
    total + " of " + total + " evidence pages shown");
  const input = page.locator("#filter-query"), kind = page.locator("#filter-kind");
  await input.fill("Гарина Гиперболоид");
  const visibleLinks = () => page.locator("#works article.card:visible h2 a")
    .evaluateAll(links => links.map(link => link.getAttribute("href")));
  const selected = await visibleLinks();
  assert.deepEqual(selected, ["works/hyperboloid-garin-measured/"],
    label + ": exact measured-work search");
  await input.fill("гиперболоид   гарина");
  assert.deepEqual(await visibleLinks(), selected, label + ": unordered Russian terms");
  await input.fill("Giperboloid Garina");
  assert.deepEqual(await visibleLinks(), selected,
    label + ": Romanized title/author search on built work");
  await input.fill("Garina Гиперболоид");
  assert.deepEqual(await visibleLinks(), selected,
    label + ": mixed Cyrillic/Latin search on built work");
  await kind.selectOption("excerpt");
  assert.equal(await page.locator("#works article.card:visible").count(), 0);
  assert.equal(await page.locator("#filter-empty").isVisible(), true);
  assert.match(await page.locator("#filter-count").innerText(), /^0 of /);
  await input.focus();
  await page.keyboard.press("Escape");
  assert.equal(await input.inputValue(), "", label + ": Escape clears focused query");
  assert.equal(await kind.inputValue(), "excerpt", label + ": Escape keeps facet");
  assert.ok(await page.locator("#works article.card:visible").count() >= 2);
  await page.locator("#filter-count").click();
  await page.keyboard.press("/");
  assert.equal(await input.evaluate(node => node === document.activeElement), true);
  await input.fill("Гарина");
  await page.keyboard.press("/");
  assert.equal(await input.inputValue(), "Гарина/", label + ": native slash typing");
  await page.keyboard.press("Escape");
  assert.equal(await input.inputValue(), "");
  await page.locator("#filter-reset").click();
  assert.equal(await kind.inputValue(), "all");
  assert.equal(await page.locator("#works article.card:visible").count(), total);
  assert.equal(await page.locator("#filter-reset").isDisabled(), true);
  assert.equal(await input.evaluate(node => node === document.activeElement), true);
  // A comparison is evidence-backed, but must not appear as a measured book.
  await kind.selectOption("comparison");
  const comparisons = page.locator('#works article.card[data-evidence-kind="comparison"]:visible');
  assert.ok(await comparisons.count() >= 1, label + ": comparisons are discoverable");
  assert.equal(await page.locator('#works article.card[data-evidence-kind="full_work"]:visible').count(), 0,
    label + ": comparisons are not classified as measured books");
  await kind.selectOption("full_work");
  assert.ok(await page.locator('#works article.card[data-evidence-kind="full_work"]:visible').count() >= 1,
    label + ": measured books are discoverable");
  assert.equal(await comparisons.count(), 0, label + ": measured-book facet excludes comparisons");
  await kind.selectOption("all");
  assert.equal(await page.locator("#works article.card:visible").count(), total);
  await page.locator("#filter-count").click();
  await page.keyboard.press("/");
  const ring = await input.evaluate(node => ({
    style:getComputedStyle(node).outlineStyle,
    width:parseFloat(getComputedStyle(node).outlineWidth)
  }));
  assert.equal(ring.style, "solid", label + ": visible keyboard focus");
  assert.ok(ring.width >= 3, label + ": focus ring >= 3 CSS px");
  const dims = await page.evaluate(() => ({
    width:document.documentElement.scrollWidth, viewport:window.innerWidth
  }));
  assert.ok(dims.width <= dims.viewport + 2,
    label + ": no horizontal overflow: " + JSON.stringify(dims));
  await page.screenshot({path:path.join(screenshots,label + "-evidence-gallery.png"),
    fullPage:true, animations:"disabled"});
  const linked = await page.goto(origin + "/" + selected[0], {waitUntil:"networkidle"});
  assert.equal(linked.status(), 200, label + ": measured-work link must resolve");
  assert.match(await page.locator("h1").first().innerText(), /Гиперболоид/);
  assert.deepEqual(errors, [], label + ": no JavaScript errors");
  assert.deepEqual(external, [], label + ": no external filter requests");
}

async function main() {
  assert.ok(fs.statSync(path.join(root,"index.html")).isFile(),
    "Build the canonical generated gallery before browser acceptance");
  assert.ok(fs.statSync(path.join(root,"assets/evidence-filter.js")).isFile());
  fs.mkdirSync(screenshots,{recursive:true});
  const server = serve();
  await new Promise(resolve => server.listen(0,"127.0.0.1",resolve));
  let browser;
  try {
    browser = await chromium.launch({headless:true});
    const origin = "http://127.0.0.1:" + server.address().port;
    const desktop = await browser.newPage({viewport:{width:1440,height:900}});
    await inspect(desktop,origin,"desktop");
    const mobile = await browser.newPage({viewport:{width:390,height:844},
      deviceScaleFactor:1,isMobile:true,hasTouch:true});
    await inspect(mobile,origin,"mobile");
    const noJsContext = await browser.newContext({javaScriptEnabled:false});
    const noJs = await noJsContext.newPage();
    assert.equal((await noJs.goto(origin + "/",{waitUntil:"networkidle"})).status(),200);
    assert.equal(await noJs.locator("#evidence-filters").isHidden(),true);
    assert.ok(await noJs.locator("#works article.card:visible").count() >= 6,
      "No-JS retains actual source-backed evidence cards and links");
    await noJsContext.close();
    console.log("Generated-gallery Chromium PASS: desktop/mobile, Cyrillic/Latin search, " +
      "facets, keyboard, focus, reset, linked work and no-JS fallback.");
    console.log("Staged build/site only; NOT live Pages verification.");
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
}
main().catch(error => {console.error(error);process.exitCode=1;});
