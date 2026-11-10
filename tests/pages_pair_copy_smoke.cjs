/* Execute shipped comparison-link helpers against pinned Reader data in Node. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const css=fs.readFileSync(path.join(root,"assets/pages-reader.css"),"utf8");
const data=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
assert.equal(data.scientific_claim,"DIAGNOSTIC_ONLY");
assert.equal(data.counts.m2_source_matched,0);
assert.match(html,/<button[^>]+id="copy-pair-link"[^>]+hidden disabled/);
assert.match(html,/<span[^>]+id="copy-pair-feedback"[^>]+role="status" aria-live="polite"/);
assert.match(css,/\.permalink-help button\s*\{[^}]*min-height:44px/);
const pairMenu=html.match(/<select id="pair-metric"[\s\S]*?<\/select>/);
assert.ok(pairMenu);
const options=[...pairMenu[0].matchAll(/<option value="([^"]+)"/g)].map(m=>({value:m[1]}));
assert.equal(options.length,7);
const start=source.indexOf("  function verifiedPairShareUrl() {");
const end=source.indexOf("  // Only a validated same-page chart permalink may enter the clipboard.",start);
assert.ok(start>0&&end>start,"production pair clipboard helpers not found");
const code=source.slice(start,end)+"return {verifiedPairShareUrl,copyPairShareUrl};";
const books=data.books.filter(b=>b.text_status==="measured");
const getBook=key=>books.find(b=>b.key===key);
assert.equal(books.length,11);
const anchor={hidden:false,href:"",getAttribute(name){
  assert.equal(name,"href");return this.href;
}};
const feedback={textContent:""};
const pairCopyButton={disabled:false};
const current="https://drevendev.github.io/Scriptorium/?book=anna&catalog=pending#measurements";
const copied=[];
const window={location:{href:current},isSecureContext:true,navigator:{
  clipboard:{async writeText(value){copied.push(value);}}
}};
const el=id=>({"share-pair":anchor,"copy-pair-feedback":feedback})[id];
const helpers=new Function("el","window","getBook","pairMetric","pairCopyButton",code)(
  el,window,getBook,{options},pairCopyButton);
async function main(){
  for(const [left,right] of [["anna","beketova"],["waves","road"],["karamazov","humiliated"]]){
    for(const {value:metric} of options){
      anchor.href="?left="+left+"&right="+right+"&pair_metric="+encodeURIComponent(metric)+"#pairs";
      const expected="https://drevendev.github.io/Scriptorium/"+anchor.href;
      assert.equal(helpers.verifiedPairShareUrl(),expected);
      await helpers.copyPairShareUrl();
      assert.equal(copied.at(-1),expected);
      assert.match(feedback.textContent,/скопирована/);
      assert.equal(window.location.href,current,"copy must not change routing");
    }
  }
  assert.equal(copied.length,21);
  const metric=encodeURIComponent(options[0].value);
  for(const href of [
    "", "https://evil.invalid/?left=anna&right=beketova&pair_metric="+metric+"#pairs",
    "?left=anna&right=anna&pair_metric="+metric+"#pairs",
    "?left=petersburg&right=anna&pair_metric="+metric+"#pairs",
    "?left=anna&right=unknown&pair_metric="+metric+"#pairs",
    "?left=anna&right=beketova&pair_metric=unknown#pairs",
    "?left=anna&right=beketova&pair_metric="+metric+"&book=anna#pairs",
    "?left=anna&left=anna&right=beketova&pair_metric="+metric+"#pairs",
    "?left=anna&right=beketova&right=beketova&pair_metric="+metric+"#pairs",
    "?left=anna&right=beketova&pair_metric="+metric+"&pair_metric="+metric+"#pairs",
    "?left=anna&right=beketova&pair_metric="+metric+"#charts",
    "?left=anna&right=beketova#pairs",
    "?left=__proto__&right=anna&pair_metric="+metric+"#pairs"
  ]){
    anchor.href=href;
    assert.equal(helpers.verifiedPairShareUrl(),null,href);
    await helpers.copyPairShareUrl();
    assert.match(feedback.textContent,/Нет проверенной ссылки/);
    assert.equal(copied.length,21);
  }
  anchor.href="?left=anna&right=beketova&pair_metric="+metric+"#pairs";
  anchor.hidden=true;
  assert.equal(helpers.verifiedPairShareUrl(),null);
  anchor.hidden=false;
  pairCopyButton.disabled=true;
  await helpers.copyPairShareUrl();
  assert.equal(copied.length,21);
  pairCopyButton.disabled=false;
  window.isSecureContext=false;
  await helpers.copyPairShareUrl();
  assert.match(feedback.textContent,/Копирование недоступно/);
  window.isSecureContext=true;
  window.navigator.clipboard=null;
  await helpers.copyPairShareUrl();
  assert.match(feedback.textContent,/Копирование недоступно/);
  window.navigator.clipboard={async writeText(){throw Error("NotAllowedError");}};
  await helpers.copyPairShareUrl();
  assert.match(feedback.textContent,/Не удалось скопировать/);
  assert.equal(copied.length,21);
  console.log("Source-bound comparison permalink copy: 21 allowed routes, invalid URLs and clipboard failures PASS");
}
main().catch(e=>{console.error(e);process.exitCode=1;});
