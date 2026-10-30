/* Run shipped catalogue CSV serializer against the pinned eight-book evidence, not fixtures. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const catalog=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const cards=[...html.matchAll(/<article class="book(?: book-research)?" data-status="(measured|pending)" data-catalog-key="([a-z]+)">/g)]
  .map(match=>({dataset:{status:match[1],catalogKey:match[2]}}));
assert.equal(cards.length,10);
const section=(first,last)=>{
  const start=source.indexOf(first),end=source.indexOf(last,start);
  assert.ok(start>=0&&end>start,first);
  return source.slice(start,end);
};
const metricMap=new Function(section("  const metrics =","  const names =")+"return metrics;")();
let downloaded=null,filename="",clicks=0;
const browserUrl={createObjectURL(blob){downloaded=blob;return "blob:catalog";},revokeObjectURL(){}};
const doc={createElement(tag){assert.equal(tag,"a");return {
  set href(v){assert.equal(v,"blob:catalog");},
  set download(v){filename=v;},click(){clicks++;},remove(){}
};},body:{appendChild(){}}};
const run=new Function("metrics","catalogCards","data","URL","document","setTimeout",
  section("  function isNumeric(x) {","  function getBook(key) {")+
  section("  function unit(id) {","  function insertText(")+
  section("  function csvText(value) {","  function serializePairCsv(report) {")+
  section("  function serializeLibraryCsv(doc) {","  function updatePair() {")+
  "return {verify,serializeLibraryCsv,exportLibraryCsv,csvText};"
)(metricMap,cards,catalog,browserUrl,doc,()=>{});
const csv=run.serializeLibraryCsv(catalog);
assert.ok(csv.startsWith("\uFEFFexport_schema,scientific_claim,"));
const records=csv.slice(1).trimEnd().split("\r\n");
const headers=records[0].split(",");
assert.equal(records.length,212);
const parse=line=>[...line.matchAll(/"((?:[^"]|"")*)"(?:,|$)/g)]
  .map(m=>m[1].replaceAll('""','"'));
const rows=records.slice(1).map(parse);
for(const row of rows)assert.equal(row.length,headers.length);
const column=name=>headers.indexOf(name);
const index=Object.fromEntries(headers.map((name,i)=>[name,i]));
assert.ok(Object.values(index).every(Number.isInteger));
assert.equal(rows.filter(r=>r[index.actual]!=="").length,177);
assert.equal(rows.filter(r=>r[index.actual]==="").length,34);
assert.equal(new Set(rows.map(r=>r[index.book_key])).size,8);
assert.equal(rows.filter(r=>r[index.book_key]==="darwin"||r[index.book_key]==="petersburg").length,0);
for(const row of rows){
  assert.equal(row[index.scientific_claim],"DIAGNOSTIC_ONLY");
  assert.equal(row[index.fantlab_input_identity],"UNKNOWN");
  assert.equal(row[index.m2_source_matched],"0");
  assert.match(row[index.source_sha256],/^[0-9a-f]{64}$/);
  assert.ok(row[index.metrics_profile].startsWith("scriptorium-metrics-v"));
  if(row[index.actual]==="")assert.notEqual(row[index.actual_status],"measured");
  else assert.equal(row[index.actual_status],"measured");
  if(row[index.fantlab_reference_display]==="")assert.notEqual(row[index.reference_status],"DISPLAY_REFERENCE_ONLY");
}
const road=rows.find(r=>r[index.book_key]==="road"&&r[index.metric_id]==="fantlab.general.characters");
assert.equal(road[index.actual],"442656");
assert.equal(road[index.fantlab_reference_display],"438439");
assert.equal(road[index.source_revision_id],"5585836");
const beketova=rows.find(r=>r[index.book_key]==="beketova"&&r[index.metric_id]==="fantlab.general.characters");
assert.equal(beketova[index.translator_name],"Александра Андреевна Бекетова");
assert.equal(beketova[index.original_language],"fr");
const missing=rows.find(r=>r[index.actual]==="");
assert.equal(missing[index.actual],"");
const zero=structuredClone(catalog);
zero.books[0].metrics[0].actual=0;
assert.equal(parse(run.serializeLibraryCsv(zero).slice(1).split("\r\n")[1])[index.actual],"0");
const injected=structuredClone(catalog);
injected.books[0].display_title="\u200B=HYPERLINK(1,2)";
assert.match(run.serializeLibraryCsv(injected),/'\u200B=HYPERLINK\(1,2\)/);
const invalid=structuredClone(catalog);
invalid.books.find(b=>b.key==="road").source_sha256="0".repeat(64);
assert.throws(()=>run.serializeLibraryCsv(invalid),/подмена|Подмена|закрепл/);
const altered=structuredClone(catalog);
altered.scientific_claim="REPRODUCED";
assert.throws(()=>run.serializeLibraryCsv(altered),/научный статус/);
(async()=>{
  run.exportLibraryCsv();
  assert.equal(clicks,1);
  assert.equal(filename,"scriptorium-ru-measured-metrics.csv");
  assert.equal(await downloaded.text(),csv.replace(/^\uFEFF/,""));
  const bytes=new Uint8Array(await downloaded.arrayBuffer());
  assert.deepEqual([...bytes.slice(0,3)],[0xef,0xbb,0xbf]);
  console.log("Full Reader catalogue CSV: 211 source-bound rows / 177 numeric / 34 status-only, safe download PASS");
})().catch(error=>{console.error(error);process.exitCode=1;});
