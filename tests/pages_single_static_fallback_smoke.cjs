/* Root Reader no-JavaScript single-book table: all 28 frozen Anna observations. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const js=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const doc=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const book=doc.books.find(b=>b.key==="anna"&&b.text_status==="measured");
assert.ok(book&&book.metrics.length===28&&book.measured===23&&book.unavailable===5);
assert.equal(doc.scientific_claim,"DIAGNOSTIC_ONLY");
assert.equal(doc.counts.m2_source_matched,0);
const metrics=JSON.parse(js.match(/  const metrics = (\{[\s\S]*?\});\n  const names =/)[1]);
const names=JSON.parse(js.match(/  const names = (\{[\s\S]*?\});\n  const el =/)[1]);
const label=id=>metrics[id]?.[0]||names[id]||id.replace(/^fantlab\./,"").replaceAll("_"," ").replaceAll("."," · ");
const unit=id=>metrics[id]?.[1]||(id==="scriptorium.general.sentences"?"предложения":
  id==="fantlab.general.characters"?"символы с пробелами":id==="fantlab.general.words"?"слова":
  id.startsWith("fantlab.vocabulary.")?"словоформы / окно, по профилю":
  id.includes(".punctuation.")?"на 1000 слов":id.endsWith("_percent")?"%":"кандидатные единицы");
const enc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const fmt=(v,places)=>new Intl.NumberFormat("ru-RU",{maximumFractionDigits:places}).format(v);
function diagnostic(m) {
  if(m.kind==="extension")return "N/A";
  if(!Number.isFinite(m.actual)||!Number.isFinite(m.reference))return "—";
  const d=m.actual-m.reference;
  if(!Number.isFinite(d))return "—";
  if(d===0)return "0";
  const whole=Number.isInteger(m.actual)&&Number.isInteger(m.reference);
  const shown=!whole&&Math.abs(d)<.0005?"<0,001":fmt(Math.abs(d),whole?0:3);
  return (d>0?"+":"−")+shown+(unit(m.id)==="%"?" п.п.":"");
}
const region=html.match(/<tbody id="measurement-rows">([\s\S]*?)<\/tbody>/);
assert.ok(region,"Root Reader must retain a no-script evidence table");
const re=/<tr data-static-single-metric="([^"]+)"><th scope="row">([^<]+)<code>([^<]+)<\/code><\/th><td>([^<]+)<\/td><td>([^<]+)<\/td><td class="benchmark-delta">([^<]+)<\/td><td>([^<]+)<\/td><td>([^<]+)<\/td><\/tr>/g;
const rows=[...region[1].matchAll(re)];
assert.equal(rows.length,book.metrics.length,"Missing source-backed static measurements");
assert.equal((region[1].match(/<tr /g)||[]).length,rows.length,"Unexpected or invalid static row");
let unavailable=0;
for(let i=0;i<rows.length;i++) {
  const [_,id,text,code,actual,reference,delta,unitText,status]=rows[i];
  const m=book.metrics[i];
  assert.equal(id,m.id);assert.equal(code,id);
  assert.equal(text,enc(label(id)),"Static label must match the interactive Reader");
  assert.ok(!text.includes("fantlab."),"No raw metric identifier as a reader-facing label");
  assert.equal(actual,enc(m.actual===null?m.status.toUpperCase():String(m.actual)));
  assert.equal(reference,enc(m.kind==="extension"?"N/A":m.reference===null?"UNKNOWN":String(m.reference)));
  assert.equal(delta,enc(diagnostic(m)));
  assert.equal(unitText,enc(unit(id)));
  assert.equal(status,enc(m.kind==="extension"?"Расширение Scriptorium":
    m.actual===null?m.status.toUpperCase():"Диагностика · несовпавший источник"));
  if(m.actual===null)unavailable++;
}
assert.equal(unavailable,5,"Unknown must not become zero");
assert.match(region[1],/NOT_RUN/);
assert.match(region[1],/UNAVAILABLE/);
assert.match(html,/Анна Каренина · полный реестр: 28 полей, 23 измерено, 5 недоступно/);
assert.match(html,/M2: 0\/5/);
assert.match(html,/id="measurement-rows"/);
console.log("No-script Anna table: 28 pinned values, labels, deltas, explicit missingness PASS");
