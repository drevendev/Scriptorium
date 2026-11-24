/* No-JavaScript branch-root Grin lexical Reader: actual mobile/desktop Chromium. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs"), path = require("node:path"), http = require("node:http");
const {chromium} = require("playwright");
const root = path.resolve(__dirname, "../build/branch-root-preview");
const screenshots = path.resolve(__dirname, "../build/reader-browser-acceptance");
function server() {
  return http.createServer((req,res) => {
    try {
      const url = new URL(req.url, "http://127.0.0.1");
      if (req.method !== "GET") {res.writeHead(405).end();return;}
      const rel = decodeURIComponent(url.pathname).replace(/^\//,"");
      const file = path.resolve(root, rel || "index.html");
      if (!file.startsWith(root + path.sep) || !fs.statSync(file).isFile()) {
        res.writeHead(404).end();return;
      }
      const type = file.endsWith(".json") ? "application/json" :
        file.endsWith(".csv") ? "text/csv" :
        file.endsWith(".css") ? "text/css" : "text/html";
      res.writeHead(200,{"Content-Type":type+"; charset=utf-8","X-Content-Type-Options":"nosniff","Cache-Control":"no-store"});
      fs.createReadStream(file).pipe(res);
    } catch(_) {res.writeHead(404).end();}
  });
}
async function inspect(browser, origin, tag, width, height) {
  const context = await browser.newContext({javaScriptEnabled:false,viewport:{width,height}});
  const page = await context.newPage();
  const errors = [],external=[];
  page.on("pageerror",e=>errors.push(e.message));
  page.on("request",r=>{if(!r.url().startsWith(origin+"/"))external.push(r.url());});
  try {
    const response = await page.goto(origin+"/lexical-grin.html",{waitUntil:"networkidle"});
    assert.equal(response.status(),200,tag+": lexical route");
    assert.match(await page.title(),/Scriptorium/);
    assert.match(await page.locator("h1").innerText(),/Грин/);
    assert.equal(await page.locator("#lex-exact-table tbody tr").count(),5);
    assert.equal(await page.locator("#lex-type-chart span").count(),3);
    assert.equal(await page.locator("#lex-token-chart span").count(),1);
    assert.match(await page.locator(".lex-stats").innerText(),/23,19%/);
    assert.match(await page.locator(".lex-stats").innerText(),/59,84%/);
    assert.match(await page.locator(".lex-stats").innerText(),/0,29/);
    assert.match(await page.locator(".lex-callout").innerText(),/M2: 0\/5/);
    const resource = await page.request.get(origin+"/assets/grin-lexical-diagnostic.json");
    assert.equal(resource.status(),200,tag+": source-free JSON route");
    const data = await resource.json();
    assert.equal(data.status,"DIAGNOSTIC_ONLY");
    assert.equal(data.source_text_included,false);
    assert.equal(data.per_form_data_included,false);
    assert.equal(data.corpus_admission,"NOT_VERIFIED");
    assert.equal(data.aggregate.shared_form_count,5901);
    assert.equal(data.aggregate.token_distribution_overlap_percent,59.843147);
    assert.equal(data.provenance.ci_run_id,45009800452);
    const csvRel="assets/grin-lexical-diagnostic.csv";
    const csvResource=await page.request.get(origin+"/"+csvRel);
    assert.equal(csvResource.status(),200,tag+": CSV route");
    const expectedCsv=fs.readFileSync(path.join(root,csvRel));
    assert.deepEqual(await csvResource.body(),expectedCsv);
    const link=page.locator('a[download][href="./'+csvRel+'"]');
    assert.equal(await link.count(),1);
    const downloadPromise=page.waitForEvent("download");
    await link.click();
    const download=await downloadPromise;
    assert.equal(download.suggestedFilename(),"grin-lexical-diagnostic.csv");
    assert.deepEqual(fs.readFileSync(await download.path()),expectedCsv);
    assert.deepEqual(errors,[]);
    assert.deepEqual(external,[],tag+": no external tracking/fonts/manuscript requests");
    const dims = await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,inner:innerWidth}));
    assert.ok(dims.scroll <= dims.inner+2,tag+": no horizontal overflow "+JSON.stringify(dims));
    await page.screenshot({path:path.join(screenshots,"lexical-grin-"+tag+".png"),fullPage:true,animations:"disabled"});
    const skip = page.locator(".skip-link").first();
    await skip.focus();
    assert.ok((await skip.boundingBox()).y>=-1,tag+": visible keyboard skip link");
    const table = page.locator(".lex-table-scroll");
    const hint = page.locator("#lex-table-help");
    assert.equal(await hint.count(),1,tag+": scroll instruction exists");
    assert.match(await hint.innerText(),/прокрутите таблицу вправо/);
    assert.equal(await table.getAttribute("aria-describedby"),"lex-table-help");
    await table.focus();
    assert.equal(await table.evaluate(e=>e===document.activeElement),true);
    if(tag==="mobile"){
      const size=await table.evaluate(e=>({visible:e.clientWidth,content:e.scrollWidth}));
      assert.ok(size.content > size.visible+100,tag+": second book requires horizontal scroll");
      await table.press("ArrowRight");
      // Poll from the Node runner: waitForFunction can stall in a no-JS context
      // while native keyboard scrolling continues asynchronously.
      let keyboardMoved=false;
      for(let poll=0;poll<30;poll++){
        const left=await table.evaluate(e=>e.scrollLeft);
        if(left>0){keyboardMoved=true;break;}
        await new Promise(resolve=>setTimeout(resolve,80));
      }
      assert.ok(keyboardMoved,tag+": ArrowRight must move the native scroll region");
      let lastVisible=false;
      for(let step=0;step<20;step++){
        lastVisible=await table.evaluate(e=>{
          const box=e.getBoundingClientRect();
          const last=e.querySelector("thead th:last-child").getBoundingClientRect();
          return last.left>=box.left-2 && last.right<=box.right+2;
        });
        if(lastVisible)break;
        await table.press("ArrowRight");
        await new Promise(resolve=>setTimeout(resolve,80));
      }
      assert.ok(lastVisible,tag+": keyboard arrows must reveal the third column");
      await page.screenshot({path:path.join(screenshots,"lexical-grin-mobile-third-column.png"),animations:"disabled"});
    }
    if(tag==="desktop"){
      await page.emulateMedia({media:"print"});
      const printTable=await table.evaluate(e=>({width:e.clientWidth,content:e.scrollWidth}));
      assert.ok(printTable.content<=printTable.width+2,"Print table must fit its region without horizontal clipping");
      const printColors = await page.locator(".lex-hero h1").evaluate(e => ({
        color: getComputedStyle(e).color,
        background: getComputedStyle(e.parentElement).backgroundColor,
      }));
      assert.equal(printColors.color, "rgb(0, 0, 0)",
        "Print must render the literary hero heading in readable ink");
      const pdf=await page.pdf({path:path.join(screenshots,"lexical-grin-a4.pdf"),format:"A4",printBackground:true});
      assert.ok(pdf.length>2000,"nonempty printable evidence page");
      await page.emulateMedia({media:"screen"});
    }
  } finally {await context.close();}
}
(async()=>{
  assert.ok(fs.existsSync(path.join(root,"lexical-grin.html")));
  assert.ok(fs.existsSync(path.join(root,"assets/grin-lexical-diagnostic.json")));
  fs.mkdirSync(screenshots,{recursive:true});
  const s=server();await new Promise(ok=>s.listen(0,"127.0.0.1",ok));
  let browser;
  try {
    browser=await chromium.launch({headless:true});
    const origin="http://127.0.0.1:"+s.address().port;
    await inspect(browser,origin,"desktop",1440,900);
    await inspect(browser,origin,"mobile",390,844);
    console.log("Grin lexical branch-root Chromium PASS: desktop/mobile/no-JS, exact data, keyboard, print; LIVE_NOT_VERIFIED.");
  } finally {if(browser)await browser.close();await new Promise(ok=>s.close(ok));}
})().catch(e=>{console.error(e);process.exitCode=1;});
