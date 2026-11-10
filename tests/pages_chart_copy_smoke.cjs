/* Real shipped Reader helpers, no DOM packages, network or clipboard permission. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const data=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const start=source.indexOf("  let chartCopyAttempt=0;");
const end=source.indexOf("  async function initialize() {",start);
assert.ok(start>=0 && end>start,"production chart copying helpers missing");
const code=source.slice(start,end)+"return {verifiedChartShareUrl,copyChartShareUrl};";
const ids=[...html.matchAll(/data-chart="([^"]+)"/g)].map(match=>match[1]);
assert.equal(ids.length,9);
assert.equal(new Set(ids).size,9);
assert.equal(data.counts.measured_works,11);
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
  assert.equal(copied.length,18);
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
    assert.equal(copied.length,18);
  }
  anchor.href="?metric="+ids[0]+"#charts";
  anchor.hidden=true;
  assert.equal(helpers.verifiedChartShareUrl(),null);
  anchor.hidden=false;
  chartCopyButton.disabled=true;
  await helpers.copyChartShareUrl();
  assert.equal(copied.length,18);
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
  assert.equal(copied.length,18);

  const deferred=[];
  window.navigator.clipboard={writeText(url){
    return new Promise((resolve,reject)=>deferred.push({url,resolve,reject}));
  }};
  const routeA="?metric="+ids[0]+"#charts";
  const routeB="?metric="+ids[1]+"#charts";
  anchor.href=routeA;
  const oldSuccess=helpers.copyChartShareUrl();
  assert.equal(deferred.length,1);
  anchor.href=routeB;
  feedback.textContent="";
  deferred[0].resolve();
  await oldSuccess;
  assert.equal(feedback.textContent,"","stale chart success must stay hidden");
  anchor.href=routeA;
  const oldFailure=helpers.copyChartShareUrl();
  anchor.href=routeB;
  feedback.textContent="";
  deferred[1].reject(Error("late NotAllowedError"));
  await oldFailure;
  assert.equal(feedback.textContent,"","stale chart denial must stay hidden");
  anchor.href=routeA;
  const slow=helpers.copyChartShareUrl();
  const fast=helpers.copyChartShareUrl();
  deferred[3].resolve();
  await fast;
  const latestFeedback=feedback.textContent;
  assert.match(latestFeedback,/скопирована/);
  deferred[2].reject(Error("late denial"));
  await slow;
  assert.equal(feedback.textContent,latestFeedback);
  assert.match(source,/function selectChart\(id, addHistory=false\) \{[\s\S]*?chartCopyAttempt\+\+;/);
  assert.equal(copied.length,18,"deferred tests never change source-backed routes");

  console.log("Verified 9×2 live-source chart permalinks, clipboard success/denial, unsafe URL and no-data guards: PASS");
}
main().catch(error=>{console.error(error);process.exitCode=1;});
