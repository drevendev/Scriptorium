/* Execute the shipped comparison-export functions without DOM dependencies. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const catalog=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const start=source.indexOf("  function sharedPairRows(a,b) {");
const end=source.indexOf("  function updatePair() {",start);
assert.ok(start>=0&&end>start,"Shipped pair-export source not found");
const pairedIds=[
  "fantlab.dialogue.share_percent",
  "fantlab.dialogue.author_text_inside_dialogue_percent",
  "fantlab.general.mean_sentence_length_chars",
  "fantlab.general.mean_word_length_chars",
  "fantlab.punctuation.comma.per_1000_words",
  "fantlab.punctuation.dash.per_1000_words",
  "fantlab.punctuation.question.per_1000_words"
];
const getBook=key=>catalog.books.find(b=>b.key===key&&b.text_status==="measured");
const lookup=(book,id)=>book.metrics.find(row=>row.id===id);
const isNumeric=n=>typeof n==="number"&&Number.isFinite(n);
const units={
  "fantlab.dialogue.share_percent":"%",
  "fantlab.dialogue.author_text_inside_dialogue_percent":"%",
  "fantlab.general.mean_sentence_length_chars":"символов / предложение",
  "fantlab.general.mean_word_length_chars":"символов / слово",
  "fantlab.punctuation.comma.per_1000_words":"на 1000 слов",
  "fantlab.punctuation.dash.per_1000_words":"на 1000 слов",
  "fantlab.punctuation.question.per_1000_words":"на 1000 слов"
};
const unit=id=>{assert.ok(Object.hasOwn(units,id));return units[id];};
const leftSelect={value:"anna"},rightSelect={value:"beketova"};
const pairExportButton={disabled:false},pairCsvButton={disabled:false};
let clicked=0,filename="",downloadBlob;
const fakeUrl={
  createObjectURL(blob){downloadBlob=blob;return "blob:test";},
  revokeObjectURL(){}
};
const fakeDocument={
  createElement(tag){
    assert.equal(tag,"a");
    return {
      set href(value){assert.equal(value,"blob:test");},
      set download(value){filename=value;},
      click(){clicked++;},
      remove(){}
    };
  },
  body:{appendChild(){}}
};
const actions=new Function(
  "getBook","pairedIds","lookup","isNumeric","unit",
  "leftSelect","rightSelect","pairExportButton","pairCsvButton","URL","document","setTimeout",
  source.slice(start,end)+"\nreturn {sharedPairRows,buildPairExport,exportPair,serializePairCsv,csvText,exportPairCsv};"
)(getBook,pairedIds,lookup,isNumeric,unit,leftSelect,rightSelect,
  pairExportButton,pairCsvButton,fakeUrl,fakeDocument,()=>{});
const data=actions.buildPairExport("anna","beketova");
assert.equal(data.schema,"scriptorium-ru-pair-comparison-v1");
assert.equal(data.scientific_claim,"DIAGNOSTIC_ONLY");
assert.equal(data.fantlab_input_identity,"UNKNOWN");
assert.equal(data.m2_source_matched,0);
assert.equal(data.text_included,false);
assert.equal(data.left.key,"anna");
assert.equal(data.right.key,"beketova");
assert.equal(data.right.translator.id,"alexandra-a-beketova");
assert.match(data.left.source_sha256,/^[a-f0-9]{64}$/);
assert.match(data.right.source_sha256,/^[a-f0-9]{64}$/);
assert.notEqual(data.left.source_sha256,data.right.source_sha256);
assert.ok(data.metrics.length>=3);
for(const metric of data.metrics){
  assert.equal(metric.delta_right_minus_left,metric.right_actual-metric.left_actual);
  assert.ok(pairedIds.includes(metric.id));
  assert.equal(metric.unit,units[metric.id]);
  assert.equal(metric.delta_unit,metric.unit==="%"?"percentage_points":metric.unit);
  assert.ok(Number.isFinite(metric.left_actual));
  assert.ok(Number.isFinite(metric.right_actual));
}
assert.ok(data.metrics.some(m=>m.delta_unit==="percentage_points"));
assert.ok(data.metrics.some(m=>m.delta_unit==="на 1000 слов"));
assert.ok(data.metrics.some(m=>m.delta_unit==="символов / предложение"));
assert.deepEqual(actions.buildPairExport("anna","beketova"),data);
for(const [left,right] of [
  ["anna","anna"],["resurrection","anna"],
  ["anna","darwin"],["../../private","silver"],["anna","SILVER"]
]) assert.equal(actions.buildPairExport(left,right),null,left+"/"+right);
const original=catalog.books.find(b=>b.key==="beketova").profiles.metrics;
catalog.books.find(b=>b.key==="beketova").profiles.metrics="unrelated-profile";
assert.equal(actions.buildPairExport("anna","beketova"),null);
catalog.books.find(b=>b.key==="beketova").profiles.metrics=original;
(async()=>{
  actions.exportPair();
  assert.equal(clicked,1);
  assert.equal(filename,"scriptorium-pair-anna-beketova.json");
  assert.deepEqual(JSON.parse(await downloadBlob.text()),data);
  const csv=actions.serializePairCsv(data);
  assert.ok(csv.startsWith("\uFEFFschema,scientific_claim,"));
  assert.equal(csv.trimEnd().split("\r\n").length,data.metrics.length+1);
  assert.ok(csv.includes('"Александра Андреевна Бекетова"'));
  assert.ok(csv.includes('"percentage_points"'));
  assert.ok(csv.includes('"DIAGNOSTIC_ONLY"'));
  assert.match(actions.csvText(" =SUM(1,1)"),/^"'/);
  assert.equal(actions.csvText('Leo "Tolstoy"'),'"Leo ""Tolstoy"""');
  actions.exportPairCsv();
  assert.equal(clicked,2);
  assert.equal(filename,"scriptorium-pair-anna-beketova.csv");
  assert.equal(await downloadBlob.text(),csv);
  rightSelect.value="anna";
  actions.exportPair();
  actions.exportPairCsv();
  assert.equal(clicked,2);
  assert.equal(pairExportButton.disabled,true);
  assert.equal(pairCsvButton.disabled,true);
  console.log("Root Pages pair export: real numeric, identity, profile and negative cases PASS");
})().catch(err=>{console.error(err);process.exitCode=1;});
