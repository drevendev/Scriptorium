/* Complete static pair fallback must agree with pinned measured JSON and live metric IDs. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const js=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const db=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const ids=JSON.parse(js.match(/  const pairedIds = (\\[[\\s\\S]*?\\]);/)[1]);
const names=JSON.parse(js.match(/  const names = (\\{[\\s\\S]*?\\});\\n  const el =/)[1]);
const metrics=JSON.parse(js.match(/  const metrics = (\\{[\\s\\S]*?\\});\\n  const names =/)[1]);
const tbody=html.match(/<tbody id="pair-rows">([\\s\\S]*?)<\\/tbody>/);
assert.ok(tbody,"Default paired comparison must remain available without scripts");
const rows=[...tbody[1].matchAll(/<tr data-static-metric="([^"]+)"><th scope="row">([^<]+)<\\/th><td>([^<]+)<\\/td><td>([^<]+)<\\/td><td>([^<]+)<\\/td><td>([^<]+)<\\/td><\\/tr>/g)];
assert.equal(rows.length,ids.length,"All eligible pair metrics must be rendered statically");
assert.equal((tbody[1].match(/<tr /g)||[]).length,rows.length,"No unverified static rows");
const left=db.books.find(b=>b.key==="anna"&&b.text_status==="measured");
const right=db.books.find(b=>b.key==="karamazov"&&b.text_status==="measured");
assert.ok(left&&right&&left.edition_id!==right.edition_id);
const fmt=n=>n===0?"0":Math.abs(n)<0.001?(n>0?"+":"−")+"<0,001":
  (n>0?"+":"")+new Intl.NumberFormat("ru-RU",{maximumFractionDigits:3}).format(n);
for (let i=0;i<ids.length;i++) {
  const [,id,title,leftText,rightText,diffText,unitText]=rows[i];
  assert.equal(id,ids[i],"Static row order must match shipped pair renderer");
  const lhs=left.metrics.find(m=>m.id===id),rhs=right.metrics.find(m=>m.id===id);
  assert.ok(lhs&&rhs&&lhs.status==="measured"&&rhs.status==="measured");
  assert.ok(Number.isFinite(lhs.actual)&&Number.isFinite(rhs.actual));
  const label=metrics[id]?.[0]||names[id];
  const unit=metrics[id]?.[1]||(id.includes(".punctuation.")?"на 1000 слов":null);
  assert.ok(label&&unit,"No machine metric IDs as visible labels");
  assert.equal(title,label,"Readable static and interactive labels must agree");
  assert.equal(leftText,String(lhs.actual),"Left source precision lost");
  assert.equal(rightText,String(rhs.actual),"Right source precision lost");
  assert.equal(diffText,fmt(rhs.actual-lhs.actual),"Signed pair delta differs from Reader");
  assert.equal(unitText,unit+(unit==="%"?" · Δ в п.п.":""),"Mismatched scientific units");
}
assert.equal(names["fantlab.punctuation.question.per_1000_words"],"Вопросительные знаки");
assert.match(html,/Сопоставление описательное/);
assert.match(html,/M2: 0\\/5/);
console.log("Static paired comparison: nine exact measured rows, units and signed deltas PASS");
