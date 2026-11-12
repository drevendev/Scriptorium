/* Real Chromium acceptance for the branch-root Reader, not a mockup or live-deploy claim. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const http = require("node:http");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "../build/branch-root-preview");
const output = path.resolve(__dirname, "../build/reader-browser-acceptance");
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".csv": "text/csv; charset=utf-8",
};

function staticServer() {
  return http.createServer((req, res) => {
    try {
      const request = new URL(req.url, "http://127.0.0.1");
      if (req.method !== "GET" || request.pathname.includes("\0")) {
        res.writeHead(405).end(); return;
      }
      const name = decodeURIComponent(request.pathname);
      const relative = name.endsWith("/") ? name + "index.html" : name;
      const filename = path.resolve(root, "." + relative);
      if (!filename.startsWith(root + path.sep) || !fs.statSync(filename).isFile()) {
        res.writeHead(404).end(); return;
      }
      res.writeHead(200, {
        "Content-Type": types[path.extname(filename)] || "application/octet-stream",
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
      });
      fs.createReadStream(filename).pipe(res);
    } catch (_) {
      res.writeHead(404).end();
    }
  });
}

async function inspectHome(page, origin, tag) {
  const errors = [];
  page.on("pageerror", error => errors.push(error.message));
  const response = await page.goto(origin + "/", { waitUntil: "networkidle" });
  assert.equal(response.status(), 200, tag + ": homepage HTTP");
  assert.match(await page.title(), /Scriptorium/);
  await page.waitForFunction(() => !document.querySelector("#export-button").disabled,
    null, { timeout: 20000 });
  assert.match(await page.locator("#table-status").innerText(), /M2 0\/5/);
  assert.equal(await page.locator("#choose-book option").count(), 11);
  await page.locator("#choose-book").selectOption("shishmareva");
  assert.match(await page.locator("#table-caption").innerText(), /Робинзон/);
  await page.locator("#choose-book").selectOption("anna");
  await page.locator("#pair-left").selectOption("anna");
  await page.locator("#pair-right").selectOption("beketova");
  assert.match(await page.locator("#pair-status").innerText(), /7 из 9/);
  assert.match(await page.locator("#pair-status").innerText(), /слева 0, справа 2/);
  await page.locator("#pair-only-shared").check();
  assert.equal(await page.locator("#pair-rows tr").count(), 7);
  await page.locator('[data-chart="fantlab.punctuation.question.per_1000_words"]').click();
  assert.equal(await page.locator('[data-chart="fantlab.punctuation.question.per_1000_words"]')
    .getAttribute("aria-pressed"), "true");
  await page.screenshot({ path: path.join(output, tag + "-reader.png"),
    fullPage: true, animations: "disabled" });
  assert.deepEqual(errors, [], tag + ": browser JavaScript errors");
}

async function main() {
  assert.ok(fs.existsSync(path.join(root, "index.html")), "Stage exact branch-root Reader first");
  assert.ok(fs.existsSync(path.join(root, "assets/evidence-snapshot.json")));
  fs.mkdirSync(output, { recursive: true });
  const server = staticServer();
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  let browser;
  try {
    const origin = "http://127.0.0.1:" + server.address().port;
    browser = await chromium.launch({ headless: true });
    const desktop = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await inspectHome(desktop, origin, "desktop");

    // An actual print PDF exercises print CSS (distinct from a visual review).
    await desktop.emulateMedia({ media: "print" });
    const pdf = await desktop.pdf({ path: path.join(output, "reader-a4.pdf"),
      format: "A4", printBackground: true });
    assert.ok(pdf.length > 2000, "Real Chromium A4 output must not be empty");
    await desktop.emulateMedia({ media: "screen" });

    const mobile = await browser.newPage({
      viewport: { width: 390, height: 844 }, deviceScaleFactor: 1,
      isMobile: true, hasTouch: true,
    });
    await inspectHome(mobile, origin, "mobile");
    const dimensions = await mobile.evaluate(() => ({
      page: document.documentElement.scrollWidth, viewport: window.innerWidth,
    }));
    assert.ok(dimensions.page <= dimensions.viewport + 2,
      "Mobile page overflows horizontally: " + JSON.stringify(dimensions));

    // Keyboard skip-link behavior is checked with real key events.
    const keyboard = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await keyboard.goto(origin + "/", { waitUntil: "networkidle" });
    await keyboard.keyboard.press("Tab");
    assert.equal(await keyboard.evaluate(() =>
      document.activeElement?.classList.contains("skip-link")), true);

    const glossary = await browser.newPage();
    const glossaryResponse = await glossary.goto(origin + "/metrics.html" +
      "#metric-fantlab.dialogue.share_percent", { waitUntil: "networkidle" });
    assert.equal(glossaryResponse.status(), 200);
    const targets = glossary.locator('tr[id^="metric-"]');
    assert.equal(await targets.count(), 29);
    assert.equal(await glossary.locator('[id="metric-fantlab.dialogue.share_percent"]')
      .getAttribute("tabindex"), "-1");
    await glossary.screenshot({ path: path.join(output, "metric-glossary.png"),
      fullPage: true, animations: "disabled" });

    const voice = await browser.newPage();
    const voiceResponse = await voice.goto(origin + "/voice/", { waitUntil: "networkidle" });
    assert.equal(voiceResponse.status(), 200);
    assert.ok(await voice.locator("table").count() > 0);
    await voice.screenshot({ path: path.join(output, "voice-evidence.png"),
      fullPage: true, animations: "disabled" });

    const csvResponse = await voice.request.get(origin + "/voice/holdout-three.csv");
    assert.equal(csvResponse.status(), 200);
    assert.match(await csvResponse.text(), /DIAGNOSTIC_ONLY|diagnostic_only|2\/6|Dostoevsky|Достоевск/i);

    console.log("Chromium PASS: real desktop/mobile Reader, 7/9 paired rows, " +
      "keyboard skip, 29 glossary targets, voice table, CSV and A4 PDF.");
    console.log("Evidence artifacts are branch-preview screenshots/PDF, NOT live Pages.");
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
