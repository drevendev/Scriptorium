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

function contrastRatio(foreground, background) {
  function luminance(color) {
    const parts = color.match(/\d+(?:\.\d+)?/g);
    assert.ok(parts && parts.length >= 3, "Expected computed RGB color");
    const [r, g, b] = parts.slice(0, 3).map(Number).map(value => {
      const x = value / 255;
      return x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4;
    });
    return 0.2126*r + 0.7152*g + 0.0722*b;
  }
  const a = luminance(foreground), b = luminance(background);
  return (Math.max(a,b) + 0.05) / (Math.min(a,b) + 0.05);
}

async function checkChartStripeContrast(page, label) {
  const details = page.locator(".chart-table");
  const wasOpen = await details.evaluate(node => node.open);
  await details.evaluate(node => { node.open = true; });
  const row = await page.locator("#chart-table-rows tr:nth-child(2)").evaluate(node => ({
    background: getComputedStyle(node).backgroundColor,
    foregrounds: [...node.cells].map(cell => getComputedStyle(cell).color),
  }));
  for (const foreground of row.foregrounds)
    assert.ok(contrastRatio(foreground, row.background) >= 4.5,
      label + ": chart striped table text must meet 4.5:1; got " +
      contrastRatio(foreground, row.background).toFixed(2));
  const evidenceLinks = await page.locator("#chart-table-rows th a").evaluateAll(links =>
    links.map(link => link.getAttribute("href")));
  const bookEvidence = await page.locator("#books .book[data-status='measured'] a[data-book]").evaluateAll(links =>
    links.map(link => link.getAttribute("href")));
  assert.equal(evidenceLinks.length, 11, label + ": chart evidence links for all measured editions");
  assert.deepEqual([...evidenceLinks].sort(), [...bookEvidence].sort(),
    label + ": chart and catalogue must use identical source-backed evidence URLs");
  await details.evaluate((node, open) => { node.open = open; }, wasOpen);
}

// Test actual keyboard focus rings against the surface underneath their outline.
async function checkKeyboardFocusContrast(page, label) {
  const chart = page.locator(".chart-table");
  const wasOpen = await chart.evaluate(node => node.open);
  await chart.evaluate(node => { node.open = true; });
  await chart.locator("summary").focus();
  await page.keyboard.press("Tab");
  const dark = await page.locator(".chart-table .table-region").evaluate(node => {
    const ring = getComputedStyle(node);
    return {
      focused: node === document.activeElement,
      style: ring.outlineStyle, pixels: parseFloat(ring.outlineWidth),
      ring: ring.outlineColor,
      surface: getComputedStyle(node.closest(".hero-visual")).backgroundColor,
    };
  });
  assert.equal(dark.focused, true, label + ": Tab reaches the dark chart table");
  assert.equal(dark.style, "solid", label + ": dark focus ring is visible");
  assert.ok(dark.pixels >= 3, label + ": dark focus ring thickness");
  assert.ok(contrastRatio(dark.ring, dark.surface) >= 3,
    label + ": dark focus ring must reach 3:1, got " +
    contrastRatio(dark.ring, dark.surface).toFixed(2));
  await chart.evaluate((node, open) => { node.open = open; }, wasOpen);

  await page.locator("#hero-title").click();
  await page.keyboard.press("/");
  const light = await page.locator("#catalog-search").evaluate(node => {
    const ring = getComputedStyle(node);
    return {
      focused: node === document.activeElement,
      style: ring.outlineStyle, pixels: parseFloat(ring.outlineWidth),
      ring: ring.outlineColor,
      surface: getComputedStyle(node.closest(".catalog-tools")).backgroundColor,
    };
  });
  assert.equal(light.focused, true, label + ": shortcut focuses catalogue search");
  assert.equal(light.style, "solid", label + ": light focus ring is visible");
  assert.ok(light.pixels >= 3, label + ": light focus ring thickness");
  assert.ok(contrastRatio(light.ring, light.surface) >= 3,
    label + ": light focus ring must reach 3:1, got " +
    contrastRatio(light.ring, light.surface).toFixed(2));
}

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

async function inspectHome(page, origin, tag, evidenceDir = output) {
  const errors = [];
  page.on("pageerror", error => errors.push(error.message));
  const response = await page.goto(origin + "/", { waitUntil: "networkidle" });
  assert.equal(response.status(), 200, tag + ": homepage HTTP");
  assert.match(await page.title(), /Scriptorium/);
  await page.waitForFunction(() => !document.querySelector("#export-button").disabled,
    null, { timeout: 20000 });
  assert.equal(await page.locator("#reader-data-status").getAttribute("data-state"),
    "ready", tag + ": verified snapshot enables controls");
  assert.match(await page.locator("#reader-data-status").innerText(), /11 измеренных редакций/);
  // The actual Reader table, not a reimplemented filter: unordered words,
  // honest zero-result feedback, and restoration of all frozen Anna rows.
  const metricSearch=page.locator("#search-metric");
  await metricSearch.fill("1000   ЗАПЯТЫЕ");
  assert.equal(await page.locator("#measurement-rows tr").count(),1,tag+": metric multi-term result");
  assert.match(await page.locator("#measurement-rows tr").innerText(),
    /fantlab\.punctuation\.comma\.per_1000_words/);
  await metricSearch.fill("запятые несуществующее");
  assert.match(await page.locator("#measurement-rows").innerText(),/Ничего не найдено/);
  await metricSearch.fill("");
  assert.equal(await page.locator("#measurement-rows tr").count(),28,tag+": metric clear");
  await checkChartStripeContrast(page, tag + " screen");
  await checkKeyboardFocusContrast(page, tag + " keyboard");
  // Exercise the real slash-to-search and Escape-to-clear flow on both viewports.
  await page.locator("#hero-title").click();
  await page.keyboard.press("/");
  assert.equal(await page.locator("#catalog-search").evaluate(node =>
    node === document.activeElement), true, tag + ": slash focuses catalogue search");
  await page.locator("#catalog-search").fill("Дефо");
  assert.match(await page.locator("#catalog-filter-status").innerText(), /1 из 13/);
  await page.keyboard.press("/");
  assert.equal(await page.locator("#catalog-search").inputValue(), "Дефо/",
    tag + ": typing slash inside search is not hijacked");
  await page.keyboard.press("Escape");
  assert.equal(await page.locator("#catalog-search").inputValue(), "",
    tag + ": Escape clears only catalogue query");
  assert.match(await page.locator("#catalog-filter-status").innerText(), /13 из 13/);
  // Exercise the shipped handler with a deterministic browser clipboard spy.
  await page.locator("#catalog-filter").selectOption("translated");
  await page.locator("#catalog-search").fill("Шишмарёва");
  await page.evaluate(() => {
    Object.defineProperty(navigator,"clipboard",{configurable:true,value:{
      writeText:async url=>{window.__scriptoriumCatalogCopied=url;}
    }});
  });
  assert.equal(await page.locator("#copy-catalog-link").isEnabled(),true);
  await page.locator("#copy-catalog-link").click();
  const copiedCatalog=await page.evaluate(()=>window.__scriptoriumCatalogCopied);
  assert.match(copiedCatalog,/catalog=translated/);
  assert.match(copiedCatalog,/#books$/);
  assert.equal(new URL(copiedCatalog).searchParams.get("q"),"Шишмарёва");
  assert.match(await page.locator("#copy-catalog-feedback").innerText(),/скопирована/);
  await page.locator("#catalog-search").fill("Верн");
  assert.equal(await page.locator("#copy-catalog-feedback").innerText(),"");
  await page.locator("#catalog-clear").click();
  assert.match(await page.locator("#catalog-filter-status").innerText(), /13 из 13/);
  assert.match(await page.locator("#table-status").innerText(), /M2 0\/5/);
  assert.equal(await page.locator("#choose-book option").count(), 11);
  const excerpt = page.locator("#trusov-excerpt");
  assert.equal(await excerpt.getAttribute("data-coverage"), "incomplete");
  // The historical coverage disclosure embeds a separate three-row table:
  // count only metric rows, not all nested table descendants.
  assert.equal(await excerpt.locator('tr[data-excerpt-metric]').count(), 8);
  const coverage = page.locator("#trusov-coverage");
  assert.equal(await coverage.count(), 1, tag + ": historical Page coverage disclosure");
  assert.equal(await coverage.evaluate(node => node.open), false);
  // Native details must be operable by keyboard on both desktop and mobile.
  await coverage.locator("summary").focus();
  await page.keyboard.press("Enter");
  assert.equal(await coverage.evaluate(node => node.open), true,
    tag + ": keyboard opens no-JS Page coverage details");
  assert.deepEqual(await coverage.locator("tbody tr[data-trusov-range]").evaluateAll(rows =>
    rows.map(row => [
      row.dataset.trusovRange, Number(row.dataset.pageFirst),
      Number(row.dataset.pageLast), Number(row.dataset.pageCount),
      row.dataset.coverageStatus,
    ])), [
      ["opening", 2, 2, 1, "not-run"],
      ["interior", 3, 147, 145, "incomplete-excerpt"],
      ["ending", 148, 151, 4, "not-run"],
    ], tag + ": historical Page intervals and evidence statuses");
  assert.match(await coverage.innerText(), /не доля полного текста по символам/);
  assert.equal(await coverage.locator('a[href$=".page-graph.json"]').count(), 1);
  await coverage.screenshot({ path: path.join(evidenceDir, tag + "-trusov-coverage.png"),
    animations: "disabled" });
  // The excerpt's visible download must work on the real staged AND public
  // Reader; a valid panel with a broken CSV route is not functional delivery.
  const excerptExport = excerpt.locator('a[download][href="./assets/trusov-1775-interior-metrics.csv"]');
  assert.equal(await excerptExport.count(), 1, tag + ": source-bound CSV download link");
  const downloadReady = page.waitForEvent("download");
  await excerptExport.click();
  const downloaded = await downloadReady;
  assert.equal(downloaded.suggestedFilename(), "trusov-1775-interior-metrics.csv",
    tag + ": actual CSV download action");
  const csvResponse = await page.context().request.get(
    origin + "/assets/trusov-1775-interior-metrics.csv");
  assert.equal(csvResponse.status(), 200, tag + ": Trusov CSV route");
  const csvLines = (await csvResponse.text()).trimEnd().split("\n");
  assert.equal(csvLines.length, 30, tag + ": header plus 29 metrics");
  assert.match(csvLines[0], /^metric_id,actual,unit,/);
  assert.ok(csvLines.some(line => line.startsWith("fantlab.general.characters,303882,")));
  assert.ok(csvLines.some(line => line.startsWith("fantlab.vocabulary.active_dictionary,,")));
  assert.match(await excerpt.innerText(), /303 882/);
  assert.match(await excerpt.innerText(), /не полный перевод/);
  assert.match(await excerpt.innerText(), /M2: 0\/5/);
  assert.equal(await page.locator('[data-translation-witness="trusov"]').getAttribute("data-analysis-status"), "unmeasured");
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
  // Real browser: a deep-linked ranked catalogue with zero results must
  // reset the actual DOM/keyboard sequence and retain unrelated pair links.
  const query = new URLSearchParams({
    left: "anna", right: "beketova", catalog: "pending",
    catalog_order: "length", q: "Бекетова",
  });
  await page.goto(origin + "/?" + query + "#books", { waitUntil: "networkidle" });
  await page.waitForFunction(() => !document.querySelector("#catalog-reset").disabled,
    null, { timeout: 20000 });
  assert.equal(await page.locator("#catalog-order").inputValue(), "length");
  assert.equal(await page.locator("#books .book:visible").count(), 0);
  await page.locator("#catalog-reset").click();
  assert.equal(await page.locator("#catalog-order").inputValue(), "catalog");
  assert.equal(await page.locator("#books .book:visible").count(), 13);
  const sourceOrder = [
    "anna", "waves", "silver", "karamazov", "hyperboloid", "beketova",
    "resurrection", "road", "oblomov", "humiliated", "shishmareva", "petersburg", "darwin"
  ];
  assert.deepEqual(await page.locator("#books .book").evaluateAll(cards =>
    cards.map(card => card.dataset.catalogKey)), sourceOrder,
    tag + ": reset must restore DOM and keyboard order");
  const cleaned = new URL(page.url());
  for (const key of ["catalog", "original", "q", "catalog_order"])
    assert.equal(cleaned.searchParams.has(key), false, tag + ": stale catalogue " + key);
  assert.equal(cleaned.searchParams.get("left"), "anna");
  assert.equal(cleaned.searchParams.get("right"), "beketova");
  // Nonempty intersections also need an immediate, keyboard-accessible all-filter reset.
  const activeQuery = new URLSearchParams({
    left: "anna", right: "beketova", catalog: "measured",
    original: "en", catalog_order: "title", q: "Дефо",
  });
  await page.goto(origin + "/?" + activeQuery + "#books", { waitUntil: "networkidle" });
  await page.waitForFunction(() => !document.querySelector("#catalog-clear").disabled,
    null, { timeout: 20000 });
  assert.equal(await page.locator("#books .book:visible").count(), 1,
    tag + ": nonempty combined facets must narrow to one measured translation");
  await page.locator("#catalog-clear").click();
  assert.equal(await page.locator("#books .book:visible").count(), 13);
  assert.equal(await page.locator("#catalog-order").inputValue(), "catalog");
  assert.deepEqual(await page.locator("#books .book").evaluateAll(cards =>
    cards.map(card => card.dataset.catalogKey)), sourceOrder);
  assert.equal(await page.locator("#catalog-search").evaluate(el => el===document.activeElement),
    true, tag + ": focus must move to search after clear");
  const afterClear=new URL(page.url());
  for(const key of ["catalog","original","q","catalog_order"])
    assert.equal(afterClear.searchParams.has(key),false,tag + ": clear must remove " + key);
  assert.equal(afterClear.searchParams.get("left"),"anna");
  assert.equal(afterClear.searchParams.get("right"),"beketova");
  await page.screenshot({ path: path.join(evidenceDir, tag + "-reader.png"),
    fullPage: true, animations: "disabled" });
  assert.deepEqual(errors, [], tag + ": browser JavaScript errors");
}


async function inspectLive() {
  const { BASE, verifyLiveBytes } = require("./pages_live_byte_guard.cjs");
  const evidenceDir = path.resolve(__dirname, "../build/reader-live-readback");
  const repoRoot = path.resolve(__dirname, "..");
  const revision = process.env.GITHUB_SHA || "unversioned";
  fs.mkdirSync(evidenceDir, { recursive: true });
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    let receipt;
    let lastError;
    // GitHub-managed branch Pages can lag the master push; never accept stale bytes.
    for (let attempt = 1; attempt <= 8; attempt++) {
      try {
        receipt = await verifyLiveBytes(context.request, repoRoot, BASE, revision);
        break;
      } catch (error) {
        lastError = error;
        console.log("LIVE_NOT_VERIFIED attempt " + attempt + "/8: " + error.message);
        if (attempt < 8) await new Promise(resolve => setTimeout(resolve, 15000));
      }
    }
    if (!receipt) throw lastError;
    const origin = BASE.slice(0, -1);
    const desktop = await context.newPage();
    await inspectHome(desktop, origin, "live-desktop", evidenceDir);
    await desktop.emulateMedia({ media: "print" });
    assert.equal(await desktop.locator(".hero-visual").evaluate(element =>
      getComputedStyle(element).breakInside), "auto");
    const pdf = await desktop.pdf({ path: path.join(evidenceDir, "live-reader-a4.pdf"),
      format: "A4", printBackground: true });
    assert.ok(pdf.length > 2000);

    const mobile = await browser.newPage({ viewport: { width: 390, height: 844 },
      deviceScaleFactor: 1, isMobile: true, hasTouch: true });
    await inspectHome(mobile, origin, "live-mobile", evidenceDir);
    const width = await mobile.evaluate(() => ({ page: document.documentElement.scrollWidth,
      viewport: window.innerWidth }));
    assert.ok(width.page <= width.viewport + 2, "Live mobile horizontal overflow");

    const keyboard = await context.newPage();
    await keyboard.goto(origin + "/", { waitUntil: "networkidle" });
    await keyboard.keyboard.press("Tab");
    assert.equal(await keyboard.evaluate(() =>
      document.activeElement?.classList.contains("skip-link")), true);
    const glossary = await context.newPage();
    const glossaryResponse = await glossary.goto(origin + "/metrics.html" +
      "#metric-fantlab.dialogue.share_percent", { waitUntil: "networkidle" });
    assert.equal(glossaryResponse.status(), 200);
    assert.equal(await glossary.locator('tr[id^="metric-"]').count(), 29);
    await glossary.screenshot({ path: path.join(evidenceDir, "live-metric-glossary.png"),
      fullPage: true, animations: "disabled" });
    const voice = await context.newPage();
    assert.equal((await voice.goto(origin + "/voice/", { waitUntil: "networkidle" })).status(), 200);
    assert.ok(await voice.locator("table").count() > 0);
    const csv = await context.request.get(origin + "/voice/holdout-three.csv");
    assert.equal(csv.status(), 200);
    assert.match(await csv.text(), /DIAGNOSTIC_ONLY|diagnostic_only|2\/6|Dostoevsky|Достоевск/i);

    // A successful UI test against a moving deployment is not an exact-master claim.
    receipt = await verifyLiveBytes(context.request, repoRoot, BASE, revision);
    fs.writeFileSync(path.join(evidenceDir, "status.json"), JSON.stringify({
      status: "LIVE_VERIFIED", checkout_sha: revision, exact_routes: receipt,
      checks: "desktop/mobile/keyboard/glossary/voice/CSV/A4",
    }, null, 2) + "\n");
    console.log("LIVE_VERIFIED: exact master bytes on " + receipt.length +
      " public routes; real desktop/mobile/keyboard/print acceptance. SHA=" + revision);
  } catch (error) {
    fs.writeFileSync(path.join(evidenceDir, "status.json"), JSON.stringify({
      status: "LIVE_NOT_VERIFIED", checkout_sha: revision, error: String(error.message),
    }, null, 2) + "\n");
    throw error;
  } finally {
    if (browser) await browser.close();
  }
}

// The no-JavaScript native N page must be a real accessible route, on mobile
// and desktop, and must print the backed 9/9 control slate without false parity.
async function checkNativeNPage(browser, origin) {
  const context = await browser.newContext({ javaScriptEnabled: false });
  try {
    for (const [tag, width, height] of [
      ["desktop", 1440, 900], ["mobile", 390, 844]
    ]) {
      const page = await context.newPage();
      await page.setViewportSize({ width, height });
      const response = await page.goto(origin + "/n-uncertainty.html", {
        waitUntil: "networkidle",
      });
      assert.equal(response.status(), 200, tag + ": N-evidence page HTTP");
      assert.match(await page.title(), /Scriptorium/);
      const rows = page.locator("#n-native-control-survey-table tr[data-survey-role]");
      assert.equal(await rows.count(), 3, tag + ": exactly three native groups");
      const cells = await rows.evaluateAll(elements => elements.map(row => [
        row.dataset.surveyRole,
        ...[...row.cells].slice(1).map(cell => cell.textContent.trim())
      ]));
      assert.deepEqual(cells, [
        ["adjectives", "3", "3", "0"],
        ["adverbs", "3", "3", "0"],
        ["verbs", "3", "3", "0"],
      ], tag + ": pinned source-free 9/9 survey");
      const original = page.locator(
        '#n-native-controls-table tr[data-native-control="other_pos_controls"]'
      );
      assert.equal(await original.locator("td").first().innerText(), "0",
        tag + ": retained N-only control");
      const originalNote = await page.locator(
        '.n-panel[aria-labelledby="n-controls"]'
      ).innerText();
      assert.match(originalNote, /один из трёх/);
      assert.match(originalNote, /INCONCLUSIVE/);
      const surveyText = await page.locator(
        '.n-panel[aria-labelledby="n-survey"]'
      ).innerText();
      assert.match(surveyText, /M2: 0\/5/);
      assert.equal(await page.locator(
        '.n-panel[aria-labelledby="n-survey"] a[href*="actions/runs/44068624527"]'
      ).count(), 1, tag + ": native CI provenance link");
      const witness = await page.request.get(origin + "/assets/n-uncertainty-anna.json");
      assert.equal(witness.status(), 200, tag + ": exact frozen witness exists");
      assert.equal((await witness.json()).m2_parity_admissible, false);
      // The skip link is visually hidden until keyboard focus, not permanently
      // exposed above the masthead on small screens.
      const skip = page.locator(".skip-links .skip-link");
      assert.equal(await skip.count(), 1, tag + ": accessible skip navigation");
      await skip.focus();
      assert.ok((await skip.boundingBox()).y >= -1,
        tag + ": keyboard focused skip link becomes visible");
      await skip.evaluate(node => node.blur());
      const dims = await page.evaluate(() => ({
        page: document.documentElement.scrollWidth, viewport: innerWidth,
      }));
      assert.ok(dims.page <= dims.viewport + 2,
        tag + ": no horizontal page overflow " + JSON.stringify(dims));
      if (tag === "mobile") {
        const lastNumber = await rows.last().locator("td").last().boundingBox();
        assert.ok(lastNumber && lastNumber.x + lastNumber.width <= width + 2,
          "Mobile N survey must show all four columns without horizontal clipping");
      }
      // Capture the natural non-focused view; test focus separately afterward.
      await page.screenshot({
        path: path.join(output, "native-n-evidence-" + tag + ".png"),
        fullPage: true, animations: "disabled",
      });
      const table = page.locator('.n-panel[aria-labelledby="n-survey"] .n-table');
      await table.focus();
      assert.equal(await table.evaluate(node => node === document.activeElement),
        true, tag + ": keyboard-scrollable table region");
      if (tag === "desktop") {
        await page.emulateMedia({ media: "print" });
        assert.equal(await rows.evaluateAll(elements => elements.every(
          row => row.checkVisibility() && row.getBoundingClientRect().width > 0)),
        true, "A4 preserves all native evidence rows");
        const pdf = await page.pdf({
          path: path.join(output, "native-n-evidence-a4.pdf"),
          format: "A4", printBackground: true,
        });
        assert.ok(pdf.length > 2000, "N evidence A4 output cannot be blank");
        await page.emulateMedia({ media: "screen" });
      }
      await page.close();
    }
  } finally {
    await context.close();
  }
}

async function main() {
  if (process.argv.includes("--live-only")) { await inspectLive(); return; }
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
    await checkNativeNPage(browser, origin);

    // A failed source-bound snapshot must explain why controls are disabled
    // while preserving the already rendered no-JS evidence and table.
    const unavailable = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    let snapshotAttempts = 0;
    await unavailable.route("**/assets/evidence-snapshot.json", route => {
      snapshotAttempts++;
      if (snapshotAttempts === 1) return route.fulfill({
        status: 503, contentType: "application/json", body: "{}",
      });
      if (snapshotAttempts === 2) return route.fulfill({
        status: 200, contentType: "application/json", body: '{"schema":"invalid"}',
      });
      return route.continue();
    });
    await unavailable.goto(origin + "/", { waitUntil: "networkidle" });
    assert.equal(await unavailable.locator("#reader-data-status").getAttribute("data-state"),
      "unavailable", "network failure must be disclosed near the chart");
    assert.match(await unavailable.locator("#reader-data-status").innerText(), /не прошли проверку/);
    assert.equal(await unavailable.locator('[data-chart="fantlab.dialogue.share_percent"]').isDisabled(), true);
    assert.equal(await unavailable.locator("#books .book").count(), 13,
      "Source links remain when interactive JSON fails");
    assert.equal(await unavailable.locator("#chart-table-rows tr").count(), 11,
      "Exact static chart observations remain on network failure");
    await unavailable.screenshot({ path: path.join(output, "reader-data-unavailable.png"),
      animations: "disabled" });
    const retry = unavailable.locator("#retry-reader-data");
    assert.equal(await retry.isVisible(), true, "Retry is available only after failed validation");
    await retry.click();
    await unavailable.waitForFunction(() =>
      document.querySelector("#reader-data-status").dataset.state === "unavailable" &&
      !document.querySelector("#retry-reader-data").hidden);
    assert.equal(snapshotAttempts, 2, "Second request exercised invalid source data");
    assert.equal(await unavailable.locator('[data-chart="fantlab.dialogue.share_percent"]').isDisabled(),
      true, "Invalid JSON must never unlock interactive controls");
    assert.equal(await unavailable.locator("#chart-table-rows tr").count(), 11,
      "Static source-backed table survives repeated validation failures");
    await retry.click();
    await unavailable.waitForFunction(() =>
      document.querySelector("#reader-data-status").dataset.state === "ready", null,
      { timeout: 20000 });
    assert.equal(snapshotAttempts, 3, "Recovery must fetch the pinned snapshot again");
    assert.equal(await retry.isHidden(), true, "Successful validation hides retry");
    assert.equal(await unavailable.locator('[data-chart="fantlab.dialogue.share_percent"]').isEnabled(),
      true, "Recovered snapshot unlocks verified charts");
    assert.equal(await unavailable.locator("#choose-book option").count(), 11,
      "Recovered snapshot enables exactly the measured editions");
    await unavailable.locator("#catalog-search").fill("Шишмарёва");
    assert.match(await unavailable.locator("#catalog-filter-status").innerText(), /1 из 13/,
      "Recovered catalogue search works without a page reload");
    await unavailable.screenshot({ path: path.join(output, "reader-data-recovered.png"),
      animations: "disabled" });
    const noJsContext = await browser.newContext({ javaScriptEnabled: false });
    const noJs = await noJsContext.newPage();
    await noJs.goto(origin + "/", { waitUntil: "networkidle" });
    assert.equal(await noJs.locator("#reader-data-status").getAttribute("data-state"),
      "static", "No-JS fallback must not claim validation");
    assert.match(await noJs.locator("#reader-data-status").innerText(), /таблица доступны сразу/);
    assert.equal(await noJs.locator("#chart-table-rows tr").count(), 11);
    assert.equal(await noJs.locator("#retry-reader-data").isHidden(), true,
      "No-JavaScript Reader must not show an inert retry control");
    await checkChartStripeContrast(noJs, "no-JS screen");
    assert.equal(await noJs.locator('[data-chart="fantlab.dialogue.share_percent"]').isDisabled(), true);
    // The Trusov source-coverage disclosure must print all three pinned Page
    // ranges with JavaScript disabled, without opening it on screen.
    const trusovCoverage = noJs.locator("#trusov-coverage");
    await trusovCoverage.evaluate(node => { node.open = false; });
    const trusovEnding = trusovCoverage.locator('tr[data-trusov-range="ending"]');
    assert.equal(await trusovEnding.evaluate(node => node.checkVisibility()), false,
      "Closed Trusov coverage must stay collapsed on screen");
    // The closed exact-value disclosure must also print with JavaScript disabled.
    await noJs.locator(".chart-table").evaluate(node => { node.open = false; });
    await noJs.emulateMedia({ media: "print" });
    assert.equal(await noJs.locator("#chart-table-rows tr:first-child td:nth-child(2)").evaluate(node =>
      node.checkVisibility() && node.getBoundingClientRect().width > 0), true,
    "No-JS print must reveal exact-value rows while the details stays closed");
    assert.equal(await trusovEnding.evaluate(node =>
      node.checkVisibility() && node.getBoundingClientRect().width > 0), true,
      "No-JS print must reveal the excluded ending Page range, not hide closed details");
    assert.equal(await trusovCoverage.locator('tbody tr[data-trusov-range]').count(), 3,
      "Printed coverage must retain both excluded edges and the incomplete interior");
    assert.equal(await trusovCoverage.evaluate(node => node.open), false,
      "Printing must not mutate the closed Trusov disclosure");
    await noJs.emulateMedia({ media: "screen" });
    assert.equal(await trusovEnding.evaluate(node => node.checkVisibility()), false,
      "Screen mode must restore collapsed Trusov disclosure");
    await noJsContext.close();
    // Printing must expose the exact-value table even when the on-screen details is closed.
    await desktop.locator(".chart-table").evaluate(node => { node.open = false; });
    assert.equal(await desktop.locator("#chart-table-rows tr:first-child td:nth-child(2)")
      .evaluate(node => node.checkVisibility()), false,
    "Closed disclosure must remain collapsed on screen");
    // An actual print PDF exercises print CSS (distinct from a visual review).
    await desktop.emulateMedia({ media: "print" });
    const printLayout = await desktop.evaluate(() => ({
      heroBreak: getComputedStyle(document.querySelector(".hero-visual")).breakInside,
      chartLayout: getComputedStyle(document.querySelector("#chart-series")).display,
      rowsIntact: [...document.querySelectorAll("#chart-series .chart-row")]
        .every(row => getComputedStyle(row).breakInside === "avoid"),
      exactTable: getComputedStyle(document.querySelector(".chart-table")).display,
      exactRowsRendered: [...document.querySelectorAll("#chart-table-rows tr")]
        .every(row => row.checkVisibility() && row.getBoundingClientRect().width > 0),
      disclosureClosed: !document.querySelector(".chart-table").open,
    }));
    assert.equal(printLayout.heroBreak, "auto",
      "Tall evidence panel must paginate, not leave an almost empty first A4 page");
    assert.equal(printLayout.chartLayout, "block", "Print chart must allow row-level pagination");
    assert.equal(printLayout.rowsIntact, true, "Printed book observations must not split");
    assert.equal(printLayout.exactTable, "block", "Keep the exact-value table on paper");
    assert.equal(printLayout.disclosureClosed, true, "Print must not mutate details state");
    assert.equal(printLayout.exactRowsRendered, true,
      "Printed exact-value rows must be laid out, not hidden in closed details");
    await checkChartStripeContrast(desktop, "A4 print");
    const pdf = await desktop.pdf({ path: path.join(output, "reader-a4.pdf"),
      format: "A4", printBackground: true });
    assert.ok(pdf.length > 2000, "Real Chromium A4 output must not be empty");
    await desktop.emulateMedia({ media: "screen" });
    assert.equal(await desktop.locator("#chart-table-rows tr:first-child td:nth-child(2)")
      .evaluate(node => node.checkVisibility()), false,
    "Screen disclosure must remain collapsed after print mode");

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
