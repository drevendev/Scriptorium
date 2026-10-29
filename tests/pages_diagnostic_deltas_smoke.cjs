/* Test shipped source-bound diagnostic formatter, not a copied algorithm. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const js=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const db=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const begin=js.indexOf("  function diagnosticDelta(m) {");
const finish=js.indexOf("  function makeTableRow(m) {",begin);
assert.ok(begin>=0&&finish>begin);
const numeric=n=>typeof n==="number"&&Number.isFinite(n);
const pretty=(n,places=2)=>new Intl.NumberFormat("ru-RU",{maximumFractionDigits:places}).format(n);
const unit=id=>id==="fantlab.dialogue.share_percent"?"%":"знаки";
const render=new Function("isNumeric","pretty","unit",js.slice(begin,finish)+"\nreturn diagnosticDelta;")(numeric,pretty,unit);
const anna=db.books.find(b=>b.key==="anna");
const metric=id=>anna.metrics.find(m=>m.id===id);
const spaces=s=>s.replace(/\s/g," ");
assert.equal(spaces(render(metric("fantlab.general.characters"))),"+12 958");
assert.equal(spaces(render(metric("fantlab.general.words"))),"+16 083");
assert.equal(render(metric("fantlab.dialogue.share_percent")),"−0,145 п.п.");
assert.equal(render(metric("fantlab.general.mean_sentence_length_chars")),"−0,174");
for(const [m,want] of [
 [{id:"test",kind:"candidate",actual:0,reference:1},"−1"],
 [{id:"test",kind:"candidate",actual:5,reference:5},"0"],
 [{id:"test",kind:"candidate",actual:1.0001,reference:1},"+<0,001"],
 [{id:"test",kind:"candidate",actual:null,reference:1},"—"],
 [{id:"test",kind:"candidate",actual:1,reference:null},"—"],
 [{id:"test",kind:"candidate",actual:NaN,reference:1},"—"],
 [{id:"test",kind:"extension",actual:2,reference:null},"N/A"]
])assert.equal(render(m),want);
for(const m of db.books.find(b=>b.key==="beketova").metrics)assert.equal(render(m),m.kind==="extension"?"N/A":"—");
console.log("Shipped Reader deltas: pinned numeric, missing, zero and negative cases PASS");
