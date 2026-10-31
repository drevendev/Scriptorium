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
  "fantlab.dialogue.mean_dialogue_sentence_length_chars",
  "fantlab.dialogue.mean_narration_sentence_length_chars",
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
  "fantlab.dialogue.mean_dialogue_sentence_length_chars":"символов / предложение",
  "fantlab.dialogue.mean_narration_sentence_length_chars":"символов / предложение",
  "fantlab.general.mean_sentence_length_chars":"символов / предложение",
  "fantlab.general.mean_word_length_chars":"символов / слово",
  "fantlab.punctuation.comma.per_1000_words":"на 1000 слов",
  "fantlab.punctuation.dash.per_1000_words":"на 1000 слов",
  "fantlab.punctuation.question.per_1000_words":"на 1000 слов"
};
const unit=id=>{assert.ok(Object.hasOwn(units,id));return units[id];};
const leftSelect={value:"anna"},rightSelect={value:"beketova"};
const pairExportButton={disabled:false},pairCsvButton={disabled:false},pairMarkdownButton={disabled:false};
const label=id=>id;
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
  "getBook","pairedIds","lookup","isNumeric","unit","label",
  "leftSelect","rightSelect","pairExportButton","pairCsvButton","pairMarkdownButton","URL","document","setTimeout",
  source.slice(start,end)+"\nreturn {sharedPairRows,pairCoverageRows,buildPairExport,exportPair,serializePairCsv,csvText,exportPairCsv,serializePairMarkdown,exportPairMarkdown};"
)(getBook,pairedIds,lookup,isNumeric,unit,label,leftSelect,rightSelect,
  pairExportButton,pairCsvButton,pairMarkdownButton,fakeUrl,fakeDocument,()=>{});
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
assert.equal(data.metrics.length,7,"Beketova has seven jointly measured normalized metrics");
assert.ok(!data.metrics.some(m=>m.id==="fantlab.dialogue.mean_dialogue_sentence_length_chars"));
assert.ok(!data.metrics.some(m=>m.id==="fantlab.dialogue.mean_narration_sentence_length_chars"));
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
const resurrectionPair=actions.buildPairExport("anna","resurrection");
assert.ok(resurrectionPair && resurrectionPair.metrics.length===9,
  "Two fully measured novels export both dialogue-length metrics");
assert.equal(resurrectionPair.right.source_sha256,"2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0");
assert.equal(resurrectionPair.fantlab_input_identity,"UNKNOWN");
assert.equal(resurrectionPair.m2_source_matched,0);
for(const [left,right] of [
  ["anna","anna"],["petersburg","anna"],
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
  assert.ok(csv.startsWith("\uFEFFschema,csv_schema,scientific_claim,"));
  assert.equal(csv.trimEnd().split("\r\n").length,data.metrics.length+1);
  assert.ok(csv.includes('"Александра Андреевна Бекетова"'));
  assert.ok(csv.includes('"percentage_points"'));
  assert.ok(csv.includes('"DIAGNOSTIC_ONLY"'));
  // CSV must retain the translation's original/analysis languages and stable ID.
  const parseRow=line=>{
    const values=[];let value="",quoted=false;
    for (let i=0;i<line.length;i++) {
      const ch=line[i];
      if (ch==='"') {
        if (quoted&&line[i+1]==='"') {value+='"';i++;}
        else quoted=!quoted;
      } else if (ch===","&&!quoted) {values.push(value);value="";}
      else value+=ch;
    }
    assert.equal(quoted,false);
    values.push(value);
    return values;
  };
  const records=csv.slice(1).trimEnd().split("\r\n");
  const csvColumns=records[0].split(",");
  assert.equal(csvColumns.length,35);
  const col=name=>{const n=csvColumns.indexOf(name);assert.ok(n>=0,name);return n;};
  const row=parseRow(records[1]);
  assert.equal(row.length,csvColumns.length);
  assert.equal(row[col("schema")],"scriptorium-ru-pair-comparison-v1");
  assert.equal(row[col("csv_schema")],"scriptorium-ru-pair-csv-v2");
  assert.equal(row[col("left_original_language")],"ru");
  assert.equal(row[col("left_analysis_language")],"ru");
  assert.equal(row[col("left_translator_id")],"");
  assert.equal(row[col("right_original_language")],"fr");
  assert.equal(row[col("right_analysis_language")],"ru");
  assert.equal(row[col("right_translator_id")],"alexandra-a-beketova");
  assert.equal(row[col("right_translator")],"Александра Андреевна Бекетова");
  assert.equal(row[col("left_source_sha256")],data.left.source_sha256);
  assert.equal(row[col("right_source_sha256")],data.right.source_sha256);
  assert.equal(row[col("metric_id")],data.metrics[0].id);
  assert.equal(Number(row[col("delta_right_minus_left")]),data.metrics[0].delta_right_minus_left);
  for (const record of records.slice(1)) assert.equal(parseRow(record).length,csvColumns.length);
  const reverse=actions.buildPairExport("beketova","anna");
  const reversedRow=parseRow(actions.serializePairCsv(reverse).slice(1).trimEnd().split("\r\n")[1]);
  assert.equal(reversedRow[col("left_translator_id")],"alexandra-a-beketova");
  assert.equal(reversedRow[col("right_translator_id")],"");
  for (const mutate of [
    item=>{item.right.translator=null;},
    item=>{item.right.translator.id="";},
    item=>{item.right.analysis_language="en";},
    item=>{item.right.original_language="de";}
  ]) {
    const invalid=structuredClone(data);
    mutate(invalid);
    assert.throws(()=>actions.serializePairCsv(invalid),/происхождение/);
  }
  assert.match(actions.csvText(" =SUM(1,1)"),/^"'/);
  for(const unsafe of [
    "\u200B=SUM(1,1)", "\u2060＋SUM(1,1)", "\uFEFF＠SUM(1,1)",
    "\tplain text", "\rplain text", "\nplain text", "\u0000plain text",
    "－1", "＝HYPERLINK(1,2)"
  ]) assert.equal(actions.csvText(unsafe), '"\''+unsafe+'"');
  assert.equal(actions.csvText("\u200Bsafe text"), '"\u200Bsafe text"');
  assert.equal(actions.csvText("Русский перевод - 1913"), '"Русский перевод - 1913"');
  assert.equal(actions.csvText('Leo "Tolstoy"'),'"Leo ""Tolstoy"""');
  actions.exportPairCsv();
  assert.equal(clicked,2);
  assert.equal(filename,"scriptorium-pair-anna-beketova.csv");
  // Blob.text() strips the UTF-8 BOM; validate downloaded bytes instead.
  const downloadedCsv=Buffer.from(await downloadBlob.arrayBuffer());
  assert.deepEqual(downloadedCsv,Buffer.from(csv,"utf8"));
  assert.deepEqual([...downloadedCsv.subarray(0,3)],[0xEF,0xBB,0xBF]);
  const coverage=actions.pairCoverageRows(getBook("anna"),getBook("beketova"));
  const md=actions.serializePairMarkdown(data,coverage);
  assert.match(md,/DIAGNOSTIC_ONLY/);
  assert.match(md,/M2: 0\/5/);
  assert.match(md,/Александра Андреевна Бекетова/);
  assert.match(md,/alexandra-a-beketova/);
  assert.match(md,new RegExp(data.right.source_sha256));
  assert.equal(md.split("\n").filter(line=>line.startsWith("| fantlab.")).length,9);
  assert.equal(md.split("\n").filter(line=>line.includes("нет данных")).length,2);
  assert.match(md,/Δ в п\.п\./);
  assert.equal(actions.serializePairMarkdown(data,coverage),md);
  const complete=actions.serializePairMarkdown(resurrectionPair,
    actions.pairCoverageRows(getBook("anna"),getBook("resurrection")));
  assert.equal(complete.split("\n").filter(line=>line.includes("нет данных")).length,0);
  const injected=structuredClone(data);
  injected.right.title="<script>alert(1)</script> | [evil](javascript:alert(1)) \n next";
  const safe=actions.serializePairMarkdown(injected,coverage);
  assert.doesNotMatch(safe,/<script>|^\s*next/m);
  assert.match(safe,/&lt;script&gt;/);
  assert.match(safe,/\\\|/);
  assert.match(safe,/\\\[evil\\\]/);
  const forged=structuredClone(data);
  forged.scientific_claim="REPRODUCED";
  assert.throws(()=>actions.serializePairMarkdown(forged,coverage),/научный статус/);
  const missingTranslator=structuredClone(data);
  missingTranslator.right.translator=null;
  assert.throws(()=>actions.serializePairMarkdown(missingTranslator,coverage),/происхождение/);
  const forgedMetric=structuredClone(data);
  forgedMetric.metrics[0].delta_right_minus_left=999;
  assert.throws(()=>actions.serializePairMarkdown(forgedMetric,coverage),/Несогласованные/);
  const zero=structuredClone(data),zeroCoverage=structuredClone(coverage);
  zero.metrics[0].left_actual=0;
  zero.metrics[0].delta_right_minus_left=zero.metrics[0].right_actual;
  zeroCoverage[0].left=0;
  assert.match(actions.serializePairMarkdown(zero,zeroCoverage),/\| 0 \|/);
  actions.exportPairMarkdown();
  assert.equal(clicked,3);
  assert.equal(filename,"scriptorium-pair-anna-beketova.md");
  assert.equal(await downloadBlob.text(),md);
  rightSelect.value="anna";
  actions.exportPair();
  actions.exportPairCsv();
  actions.exportPairMarkdown();
  assert.equal(clicked,3);
  assert.equal(pairExportButton.disabled,true);
  assert.equal(pairCsvButton.disabled,true);
  assert.equal(pairMarkdownButton.disabled,true);
  console.log("Root Pages pair export: real numeric, identity, profile and negative cases PASS");
})().catch(err=>{console.error(err);process.exitCode=1;});
