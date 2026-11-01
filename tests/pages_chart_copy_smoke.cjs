/* Real shipped Reader helpers, no DOM packages, network or clipboard permission. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const data=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const start=source.indexOf("  function verifiedChartShareUrl() {");
const end=source.indexOf("  async function initialize() {",start);
assert.ok(start>=0 && end>start,"production chart copying helpers missing");
const code=source.slice(start,end)+"return {verifiedChartShareUrl,copyChartShareUrl};";
const ids=[...html.matchAll(/data-chart="([^"]+)"/g)].map(match=>match[1]);
assert.equal(ids.length,8);
assert.equal(new Set(ids).size,8);
assert.equal(data.counts.measured_works,10);
const metrics=Object.fromEntries(ids.map(id=>[id,true]));
const anchor={hidden:false,href:"",getAttribute(name){
  assert.equal(name,"href");return this.href;
}};
const feedback={textContent:""};
const chartCopyButton={disabled:false};
const page="https://drevendev.github.io/Scriptorium/?book=anna&left=beketova#pairs";
const copied=[];
const window={location:{href:page},isSecureContext:true,navigator:{
  clipboard:{async writeText(value){copied.push(value);}}
}};
const el=id=>({"share-chart":anchor,"copy-chart-feedback":feedback})[id];
const helpers=new Function("el","window","metrics","chartCopyButton",code)(
  el,window,metrics,chartCopyButton);
async function main(){
  for(const id of ids)for(const ranked of [false,true]){
    anchor.href="?metric="+encodeURIComponent(id)+(ranked?"&chart_order=ranked":"")+"#charts";
    const url=helpers.verifiedChartShareUrl();
    assert.equal(url,"https://drevendev.github.io/Scriptorium/"+anchor.href);
    await helpers.copyChartShareUrl();
    assert.equal(copied.at(-1),url);
    assert.match(feedback.textContent,/скопирована/);
    assert.equal(window.location.href,page,"copy must not navigate or mutate history");
  }
  assert.equal(copied.length,16);
  for(const href of [
    "", "https://outside.invalid/?metric="+ids[0]+"#charts",
    "?metric=other.metric#charts", "?metric="+ids[0]+"&chart_order=unknown#charts",
    "?metric="+ids[0]+"&chart_order=ranked&chart_order=ranked#charts",
    "?metric="+ids[0]+"&metric="+ids[0]+"#charts",
    "?metric="+ids[0]+"&book=anna#charts", "?metric="+ids[0]+"#pairs"
  ]){
    anchor.href=href;
    assert.equal(helpers.verifiedChartShareUrl(),null,href);
    await helpers.copyChartShareUrl();
    assert.match(feedback.textContent,/Нет проверенной ссылки/);
    assert.equal(copied.length,16);
  }
  anchor.href="?metric="+ids[0]+"#charts";
  anchor.hidden=true;
  assert.equal(helpers.verifiedChartShareUrl(),null);
  anchor.hidden=false;
  chartCopyButton.disabled=true;
  await helpers.copyChartShareUrl();
  assert.equal(copied.length,16);
  chartCopyButton.disabled=false;
  window.isSecureContext=false;
  await helpers.copyChartShareUrl();
  assert.match(feedback.textContent,/Копирование недоступно/);
  window.isSecureContext=true;
  window.navigator.clipboard=null;
  await helpers.copyChartShareUrl();
  assert.match(feedback.textContent,/Копирование недоступно/);
  window.navigator.clipboard={async writeText(){throw Error("NotAllowedError");}};
  await helpers.copyChartShareUrl();
  assert.match(feedback.textContent,/Не удалось скопировать/);
  assert.equal(copied.length,16);
  console.log("Verified 8×2 live-source chart permalinks, clipboard success/denial, unsafe URL and no-data guards: PASS");
}
main().catch(error=>{console.error(error);process.exitCode=1;});
