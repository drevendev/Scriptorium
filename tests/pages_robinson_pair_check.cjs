"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs"), path = require("node:path");
// Sample native scroll/layout from the Node runner, not an in-page rAF loop:
 // no-JS contexts can stall that loop. Never force a click or disable smooth
 // scrolling in the default-motion path. Poll only until geometry is stable.
async function settleGeometry(locator,label,ready){
  const samples=[];
  let consecutive=0;
  for(let i=0;i<120;i++){
    const current=await locator.evaluate(e=>{
      const b=e.getBoundingClientRect(),x=b.x+b.width/2,y=b.y+b.height/2;
      const hit=document.elementFromPoint(x,y);
      return {scrollY,x,y,top:b.top,width:b.width,height:b.height,
        viewportHeight:innerHeight,hitLink:!!hit&&e.contains(hit),
        behavior:getComputedStyle(document.documentElement).scrollBehavior,
        reduced:matchMedia("(prefers-reduced-motion: reduce)").matches};
    });
    const previous=samples.at(-1);
    samples.push(current);
    const stable=previous&&["scrollY","x","y","width","height"].every(
      key=>Math.abs(current[key]-previous[key])<=0.5);
    consecutive=ready(current)?(stable?consecutive+1:1):0;
    if(consecutive>=4){
      console.log(label+": geometry settled "+JSON.stringify(
        {samples:samples.length,first:samples[0],last:current}));
      return current;
    }
    await new Promise(resolve=>setTimeout(resolve,50));
  }
  assert.fail(label+": geometry did not settle "+JSON.stringify(
    {samples:samples.length,first:samples[0],last:samples.at(-1)}));
}
async function openRobinson(page,origin,label,motion){
  // A reader's tab must be foreground, especially after closing a separate
  // download context. Keep the real fragment and the real unforced link click.
  await page.bringToFront();
  assert.equal((await page.goto(origin+"/#translations")).status(),200,label);
  const section=page.locator("#translations");
  const fragment=await settleGeometry(section,label+": fragment",
    g=>g.top>=-2&&g.top<g.viewportHeight);
  assert.equal(fragment.reduced,motion==="reduce",label);
  assert.equal(fragment.behavior,motion==="reduce"?"auto":"smooth",label);
  const link=page.locator('a[href="./robinson-pair.html"]');
  assert.equal(await link.count(),1,label);
  // Emulate the reader scrolling the entry into view; auto respects the
  // computed CSS scroll-behavior. Then verify the native hit target.
  await link.evaluate(e=>e.scrollIntoView({block:"center",inline:"nearest",behavior:"auto"}));
  await settleGeometry(link,label+": entry",g=>g.hitLink);
  await link.click();
  assert.match(page.url(),/robinson-pair\.html$/,label);
}
async function inspectDownload(page,expected,label){
  const link=page.locator('a[download][href="./assets/robinson-pair.json"]');
  assert.equal(await link.count(),1,label);
  assert.equal(await link.evaluate(e=>new URL(e.href).origin),new URL(page.url()).origin,label);
  const geometry=()=>link.evaluate(e=>{
    const b=e.getBoundingClientRect(), x=b.x+b.width/2,y=b.y+b.height/2;
    const hit=document.elementFromPoint(x,y);
    return {scrollY, x, y, hitLink:!!hit&&e.contains(hit), focused:document.activeElement===e};
  });
  await link.evaluate(e=>e.scrollIntoView({block:"center",inline:"nearest",behavior:"auto"}));
  await settleGeometry(link,label+": download link",g=>g.hitLink);
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
  const freshErrors=[];
  for(const motion of ["no-preference","reduce"]){
    const label=tag+": fresh no-JS "+motion;
    const fresh=await browser.newContext({javaScriptEnabled:false,
      viewport:page.viewportSize(),reducedMotion:motion});
    try{
      const reader=await fresh.newPage();
      await openRobinson(reader,origin,label,motion);
      await reader.screenshot({path:path.join(screenshots,"robinson-pair-fresh-"+tag+
        (motion==="reduce"?"-reduced":"")+".png"),fullPage:true,animations:"disabled"});
      await inspectDownload(reader,expectedBytes,label);
    }catch(error){freshErrors.push(error);console.error(label+" failed",error.message);}
    finally{await fresh.close();}
  }

  await openRobinson(page,origin,tag+": after lexical downloads","no-preference");
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
  if(freshErrors.length)throw new AggregateError(freshErrors,"Fresh Reader paths failed");
}
module.exports={inspectRobinson};
