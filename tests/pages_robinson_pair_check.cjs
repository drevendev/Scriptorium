"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs"), path = require("node:path");
async function inspectDownload(page,expected,label){
  const link=page.locator('a[download][href="./assets/robinson-pair.json"]');
  assert.equal(await link.count(),1,label);
  assert.equal(await link.evaluate(e=>new URL(e.href).origin),new URL(page.url()).origin,label);
  const geometry=()=>link.evaluate(e=>{
    const b=e.getBoundingClientRect(), x=b.x+b.width/2,y=b.y+b.height/2;
    const hit=document.elementFromPoint(x,y);
    return {scrollY, x, y, hitLink:!!hit&&e.contains(hit), focused:document.activeElement===e};
  });
  const before=await geometry();
  let download;
  try{
    [download]=await Promise.all([page.waitForEvent("download"),link.click()]);
  }catch(error){
    console.error(label,JSON.stringify({before,after:await geometry(),route:new URL(page.url()).pathname}));
    throw error;
  }
  assert.equal(download.suggestedFilename(),"robinson-pair.json",label);
  assert.equal(await download.failure(),null,label);
  assert.deepEqual(fs.readFileSync(await download.path()),expected,label);
  console.log(label+": exact JSON download PASS");
}
async function inspectRobinson(page,origin,screenshots,tag){
  // Separate a fresh reader's click from the existing sequential CSV/JSON flow.
  // Both must pass; a successful HTTP request is not a substitute for a download.
  const expectedBytes=fs.readFileSync(path.resolve(__dirname,"../assets/robinson-pair.json"));
  const browser=page.context().browser();
  assert.ok(browser);
  const fresh=await browser.newContext({javaScriptEnabled:false,viewport:page.viewportSize()});
  let freshError;
  try{
    const reader=await fresh.newPage();
    assert.equal((await reader.goto(origin+"/#translations")).status(),200);
    await reader.locator('a[href="./robinson-pair.html"]').click();
    assert.match(reader.url(),/robinson-pair\.html$/);
    await reader.screenshot({path:path.join(screenshots,"robinson-pair-fresh-"+tag+".png"),fullPage:true,animations:"disabled"});
    await inspectDownload(reader,expectedBytes,tag+": fresh no-JS context");
  }catch(error){freshError=error;console.error(tag+": fresh download failed",error.message);}
  finally{await fresh.close();}

  assert.equal((await page.goto(origin+"/#translations")).status(),200);
  await page.locator('a[href="./robinson-pair.html"]').click();
  assert.match(page.url(),/robinson-pair\.html$/);
  const rr=await page.request.get(origin+"/assets/robinson-pair.json");
  assert.equal(rr.status(),200);
  const expected=fs.readFileSync(path.resolve(__dirname,"../assets/robinson-pair.json"));
  assert.deepEqual(await rr.body(),expected);
  const r=JSON.parse(expected);
  assert.equal(r.joint_numeric_count,22);
  assert.equal(r.translation_coverage_alignment,"NOT_RUN");
  assert.equal(await page.locator(".rp-table tbody tr").count(),29);
  for(const row of r.metric_rows){
    const tr=page.locator('tr[data-metric="'+row.metric_id+'"]');
    assert.equal(await tr.count(),1);
    for(const key of ["trusov","shishmareva","delta_trusov_minus_shishmareva"]){
      const td=tr.locator('[data-field="'+key+'"]');
      assert.equal(await td.getAttribute("data-value"),String(row[key]));
      const displayed=(await td.innerText()).replaceAll(" ","").replace(",",".");
      if(row[key]===null)assert.equal(displayed,"Нет данных");
      else assert.equal(Number(displayed),Number(row[key].toPrecision(8)));
    }
  }
  assert.equal(await page.locator("[data-chart]").count(),5);
  for(const chart of await page.locator("[data-chart]").all()){
    const key=await chart.getAttribute("data-chart");
    const actual=r.metric_rows.find(x=>x.metric_id===key);
    for(const ed of ["trusov","shishmareva"]){
      const value=chart.locator('[data-edition="'+ed+'"]');
      assert.equal(Number(await value.getAttribute("data-value")),actual[ed]);
      assert.equal(Number((await value.innerText()).replaceAll(" ","").replace(",",".")),Number(actual[ed].toPrecision(8)));
    }
  }
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));
  await page.locator("#rp-table-region").focus();
  assert.ok(await page.locator("#rp-table-region").evaluate(e=>e===document.activeElement));
  await page.screenshot({path:path.join(screenshots,"robinson-pair-"+tag+".png"),fullPage:true,animations:"disabled"});
  await inspectDownload(page,expected,tag+": after lexical downloads and table focus");
  if(freshError)throw freshError;
}
module.exports={inspectRobinson};
