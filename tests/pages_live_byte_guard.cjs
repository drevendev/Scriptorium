/* Exact-byte public Pages readback. HTTP success alone is not deployment evidence. */
"use strict";
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const PUBLISHED = Object.freeze([
  "index.html",
  "metrics.html",
  "assets/pages-reader.css",
  "assets/pages-reader.js",
  "assets/evidence-snapshot.json",
  "assets/scriptorium-ru-measured-metrics.csv",
  "assets/trusov-1775-interior-metrics.csv",
  "voice/index.html",
  "voice/holdout-three.csv",
]);
const BASE = "https://drevendev.github.io/Scriptorium/";
const digest = bytes => crypto.createHash("sha256").update(bytes).digest("hex");

async function verifyLiveBytes(request, repoRoot, base = BASE, revision = "unknown", files = PUBLISHED) {
  // An accidental preview or redirect to a different host must never be called live Pages.
  const site = new URL(base);
  if (site.href !== BASE) throw new Error("Unexpected public Pages origin/path");
  const results = [];
  for (const relative of files) {
    if (!PUBLISHED.includes(relative)) throw new Error("Unapproved public readback path");
    const url = new URL(relative === "index.html" ? "" : relative, site);
    url.searchParams.set("scriptorium_probe", revision);
    const response = await request.get(url.href, { timeout: 15000, failOnStatusCode: false });
    if (response.status() !== 200) throw new Error(`${relative}: HTTP ${response.status()} (not verified)`);
    const servedAt = new URL(response.url());
    if (servedAt.origin !== site.origin || servedAt.pathname !== url.pathname) {
      throw new Error(`${relative}: unexpected redirect target (not verified)`);
    }
    const expected = digest(fs.readFileSync(path.join(repoRoot, relative)));
    const observed = digest(await response.body());
    if (observed !== expected) throw new Error(`${relative}: published bytes differ from checkout (not verified)`);
    results.push({ path: relative, sha256: expected });
  }
  return results;
}

async function selfTest() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "scriptorium-pages-readback-"));
  try {
    fs.writeFileSync(path.join(root, "index.html"), "exact published Reader");
    const fake = (bytes, status = 200, redirect) => ({
      get: async url => ({ status: () => status, url: () => redirect || url,
        body: async () => Buffer.from(bytes) }),
    });
    const args = [root, BASE, "test", ["index.html"]];
    const found = await verifyLiveBytes(fake("exact published Reader"), ...args);
    assert.equal(found.length, 1);
    assert.equal(found[0].sha256, digest(Buffer.from("exact published Reader")));
    await assert.rejects(verifyLiveBytes(fake("old Reader"), ...args), /published bytes differ/);
    // Protect the new researcher download as well as the HTML entry point.
    // A stale or missing CSV is a failed live release, not a usable export.
    const csvPath = "assets/trusov-1775-interior-metrics.csv";
    const csvBytes = "metric_id,actual\nfantlab.general.characters,303882\n";
    fs.mkdirSync(path.join(root, "assets"));
    fs.writeFileSync(path.join(root, csvPath), csvBytes);
    const csvResponse = bytes => ({
      get: async url => ({
        status: () => 200, url: () => url,
        body: async () => Buffer.from(url.includes(csvPath) ? bytes : "exact published Reader"),
      }),
    });
    const csvArgs = [root, BASE, "test", ["index.html", csvPath]];
    const matched = await verifyLiveBytes(csvResponse(csvBytes), ...csvArgs);
    assert.deepEqual(matched.map(row => row.path), ["index.html", csvPath]);
    await assert.rejects(
      verifyLiveBytes(csvResponse(csvBytes + "stale"), ...csvArgs),
      /trusov-1775-interior-metrics.csv: published bytes differ/,
    );
    await assert.rejects(verifyLiveBytes(fake("", 404), ...args), /HTTP 404/);
    await assert.rejects(verifyLiveBytes(fake("exact published Reader", 200,
      "https://example.com/"), ...args), /redirect target/);
    await assert.rejects(verifyLiveBytes(fake("exact published Reader"), root,
      "https://example.com/Scriptorium/", "test", ["index.html"]), /origin\/path/);
    await assert.rejects(verifyLiveBytes(fake("exact published Reader"), root,
      BASE, "test", ["../secrets.txt"]), /Unapproved/);
    console.log("PASS: exact-byte readback; stale, 404, redirect and path negatives");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

module.exports = { BASE, PUBLISHED, verifyLiveBytes };
if (require.main === module) selfTest().catch(error => { console.error(error); process.exitCode = 1; });
