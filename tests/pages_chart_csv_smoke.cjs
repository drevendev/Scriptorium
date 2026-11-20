/* Exercise the shipped chart CSV serializer on the eleven pinned measured books. */
"use strict";
const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const doc=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const metrics=new Function(source.slice(source.indexOf("  const metrics ="),source.indexOf("  const names ="))+"return metrics;")();
const csvText=new Function(source.slice(source.indexOf("  function csvText(value) {"),source.indexOf("  function serializePairCsv("))+"return csvText;")();
const start=source.indexOf("  function serializeChartCsv("),end=source.indexOf("  function exportChartCsv(",start);
assert(start>0&&end>start);
const serialize=new Function("metrics","lookup","isNumeric","csvText",source.slice(start,end)+"return serializeChartCsv;")(metrics,(b,id)=>b.metrics.find(m=>m.id===id),n=>typeof n==="number"&&Number.isFinite(n),csvText);
const parse=(csv,expectedCount=11)=>{
  assert(csv.startsWith("\uFEFF"));
  const [head,...lines]=csv.slice(1).trimEnd().split("\r\n");
  const labels=head.split(",");
  assert.equal(lines.length,expectedCount);
  return lines.map(line=>{
    const cells=[...line.matchAll(/"((?:[^"]|"")*)"(?:,|$)/g)].map(m=>m[1].replaceAll('""','"'));
    assert.equal(cells.length,labels.length);
    return Object.fromEntries(labels.map((name,i)=>[name,cells[i]]));
  });
};
const measured=doc.books.filter(b=>b.text_status==="measured");
assert.equal(measured.length,11);
for(const id of Object.keys(metrics)){
  for(const sorted of [false,true]){
    const rows=parse(serialize(doc,id,sorted));
    const expected=measured.map((b,ordinal)=>({book:b,ordinal,value:b.metrics.find(m=>m.id===id)?.actual??null}));
    if(sorted)expected.sort((a,b)=>a.value===null?(b.value===null?a.ordinal-b.ordinal:1):
      b.value===null?-1:b.value-a.value||a.ordinal-b.ordinal);
    assert.deepEqual(rows.map(r=>r.book_key),expected.map(r=>r.book.key));
    for(const [i,row] of rows.entries()){
      const book=expected[i].book,field=book.metrics.find(m=>m.id===id);
      assert.equal(row.actual,field?.actual==null?"":String(field.actual));
      assert.equal(row.status,field?.status||"not_recorded");
      assert.equal(row.unit,metrics[id][1]);
      assert.equal(row.source_sha256,book.source_sha256);
      assert.equal(row.edition_id,book.edition_id);
      assert.equal(row.translator,book.translator?.name||"");
      assert.equal(row.fantlab_input_identity,"UNKNOWN");
      assert.equal(row.scientific_claim,"DIAGNOSTIC_ONLY");
      assert.equal(row.m2_source_matched,"0");
      assert.equal(row.position,String(i+1));
    }
  }
}
const id="fantlab.dialogue.mean_dialogue_sentence_length_chars";
const missing=parse(serialize(doc,id,true)).at(-1);
assert.equal(missing.book_key,"beketova");assert.equal(missing.actual,"");assert.equal(missing.status,"not_recorded");
const zero=JSON.parse(JSON.stringify(doc));
zero.books[0].metrics.find(m=>m.id==="fantlab.dialogue.share_percent").actual=0;
const zr=parse(serialize(zero,"fantlab.dialogue.share_percent",false))[0];
assert.equal(zr.actual,"0");assert.equal(zr.status,"measured");
// Scoped single-metric exports must be distinct from full-chart exports.
const selectedKeys=new Set(["anna","resurrection"]);
const selected=parse(serialize(doc,"fantlab.dialogue.share_percent",false,selectedKeys),2);
assert.deepEqual(selected.map(r=>r.book_key),["anna","resurrection"]);
assert.deepEqual(selected.map(r=>r.position),["1","2"]);
assert.ok(selected.every(r=>r.schema==="scriptorium-ru-chart-subset-csv-v1" &&
  r.selection_scope==="catalog_highlight" && r.scientific_claim==="DIAGNOSTIC_ONLY" &&
  r.fantlab_input_identity==="UNKNOWN" && r.m2_source_matched==="0"));
assert.deepEqual(selected.map(r=>r.source_sha256),
  measured.filter(b=>selectedKeys.has(b.key)).map(b=>b.source_sha256));
const rankedSelected=parse(serialize(doc,"fantlab.dialogue.share_percent",true,selectedKeys),2);
assert.deepEqual(rankedSelected.map(r=>r.book_key),["anna","resurrection"]);
assert.ok(rankedSelected.every(r=>r.sort_order==="value_desc"));
const selectedZero=parse(serialize(zero,"fantlab.dialogue.share_percent",false,new Set(["anna"])),1);
assert.equal(selectedZero[0].actual,"0");assert.equal(selectedZero[0].status,"measured");
const selectedMissing=parse(serialize(doc,id,false,new Set(["beketova"])),1);
assert.equal(selectedMissing[0].actual,"");assert.equal(selectedMissing[0].status,"not_recorded");
assert.equal(parse(serialize(doc,"fantlab.dialogue.share_percent",false))[0].schema,
  "scriptorium-ru-chart-csv-v1");
for(const bad of [new Set(),new Set(["missing"]),new Set(["anna","pending"]),["anna"],"anna"]){
  assert.throws(()=>serialize(doc,"fantlab.dialogue.share_percent",false,bad),/выбор книг/);
}
const injected=JSON.parse(JSON.stringify(doc));injected.books[0].display_title="=1+2";
assert.equal(parse(serialize(injected,"fantlab.dialogue.share_percent",false))[0].title,"'=1+2");
assert.throws(()=>serialize({...doc,scientific_claim:"PARITY"},"fantlab.dialogue.share_percent",false),/научный статус/);
assert.throws(()=>serialize(doc,"constructor",false),/не разрешён/);
const damaged=JSON.parse(JSON.stringify(doc));damaged.books[0].source_sha256="bad";
assert.throws(()=>serialize(damaged,"fantlab.dialogue.share_percent",false),/редакция/);
console.log("9 metrics × 2 orders, 11 actual editions, zero/missing, safety/provenance: PASS");
