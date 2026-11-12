/* Check actual shipped pair rendering and honest missingness using pinned source-free data. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const data=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const begin=source.indexOf("  const pairedIds = [");
const end=source.indexOf("  // Source-free, edition-bound",begin);
assert(begin>=0&&end>begin,"Shipped pair helpers missing");
const lookup=(book,id)=>book.metrics.find(m=>m.id===id);
const isNumeric=n=>typeof n==="number"&&Number.isFinite(n);
const {pairedIds,sharedPairRows,pairCoverageRows}=new Function("lookup","isNumeric",
  source.slice(begin,end)+"\nreturn {pairedIds,sharedPairRows,pairCoverageRows};"
)(lookup,isNumeric);
const getBook=key=>data.books.find(b=>b.key===key&&b.text_status==="measured");
const anna=getBook("anna"),beketova=getBook("beketova"),karamazov=getBook("karamazov");
assert.equal(pairedIds.length,9);
const complete=pairCoverageRows(anna,karamazov);
assert.equal(complete.length,9);
assert.ok(complete.every(m=>isNumeric(m.left)&&isNumeric(m.right)));
assert.equal(sharedPairRows(anna,karamazov).length,9);
const partial=pairCoverageRows(anna,beketova);
assert.equal(partial.length,9);
assert.equal(sharedPairRows(anna,beketova).length,7);
const missing=partial.filter(m=>m.right===null);
assert.deepEqual(missing.map(m=>m.id),[
  "fantlab.dialogue.mean_dialogue_sentence_length_chars",
  "fantlab.dialogue.mean_narration_sentence_length_chars"
]);
assert.ok(missing.every(m=>isNumeric(m.left)));
assert.ok(sharedPairRows(anna,beketova).every(m=>isNumeric(m.left)&&isNumeric(m.right)));
const malformed={...beketova,metrics:beketova.metrics.map(m=>
  m.id==="fantlab.dialogue.share_percent"?{...m,actual:"0"}:m)};
assert.equal(pairCoverageRows(anna,malformed).find(m=>
  m.id==="fantlab.dialogue.share_percent").right,null);
const zero={...beketova,metrics:[...beketova.metrics,
  {id:"fantlab.dialogue.mean_dialogue_sentence_length_chars",actual:0,status:"measured"}]};
assert.equal(pairCoverageRows(anna,zero).find(m=>
  m.id==="fantlab.dialogue.mean_dialogue_sentence_length_chars").right,0,
  "A measured zero must remain distinct from unavailable");
class Node {
  constructor(tag){this.tag=tag;this.children=[];this.textContent="";this.style={};}
  appendChild(child){this.children.push(child);return child;}
  replaceChildren(...children){this.children=children;}
  setAttribute(key,value){this[key]=value;}
}
const document={
  createElement:tag=>new Node(tag),
  createDocumentFragment:()=>new Node("#fragment")
};
const slots=Object.fromEntries(["pair-rows","paired-graphic","pair-status","pair-caption","pair-only-shared"]
  .map(id=>[id,new Node(id)]));
const el=id=>{assert.ok(Object.hasOwn(slots,id));return slots[id];};
const insertText=(parent,tag,value,cls)=>{
  const n=new Node(tag);n.textContent=value;
  if(cls)n.className=cls;parent.appendChild(n);return n;
};
const unit=id=>id.endsWith("_percent")||id==="fantlab.dialogue.share_percent"?"%":
  id.includes("length_chars")?"символов / предложение":"на 1000 слов";
const label=id=>id;
// Exercise the actual shipped helper when the isolated pair renderer is evaluated.
const metricLinkStart=source.indexOf("  function appendMetricDefinition(parent,id,shown=label(id)) {");
const metricLinkEnd=source.indexOf("  // Source-unmatched",metricLinkStart);
assert.ok(metricLinkStart>=0&&metricLinkEnd>metricLinkStart);
const appendMetricDefinition=new Function("document","label",
  source.slice(metricLinkStart,metricLinkEnd)+"\nreturn appendMetricDefinition;"
)(document,label);
const pretty=(n,places=2)=>n.toFixed(places);
const exact=String;
const deltaStart=source.indexOf("  function pairTableDeltaText(difference) {");
const deltaEnd=source.indexOf("  function updatePair() {",deltaStart);
assert(deltaStart>=0&&deltaEnd>deltaStart,"Shipped signed-delta function missing");
const {pairTableDeltaText,pairDeltaDescription}=new Function("pretty","unit",
  source.slice(deltaStart,deltaEnd)+"\nreturn {pairTableDeltaText,pairDeltaDescription};"
)(pretty,unit);
assert.match(pairDeltaDescription({id:"fantlab.dialogue.share_percent",left:3,right:3}),/0\.000 п\.п\./);
assert.match(pairDeltaDescription({id:"fantlab.dialogue.share_percent",left:3,right:3.00000001}),
  /положительная \(менее 0,001\) п\.п\./);
assert.match(pairDeltaDescription({id:"fantlab.dialogue.share_percent",left:3.00000001,right:3}),
  /отрицательная \(менее 0,001\) п\.п\./);
for (const [value, expected] of [
  [0,"0"],[-0,"0"],[0.00000001,"+<0,001"],[-0.00000001,"−<0,001"],
  [0.0009999,"+<0,001"],[-0.0009999,"−<0,001"],[0.001,"+0.001"]
]) assert.equal(pairTableDeltaText(value),expected,"No false zero in the reader table");
assert.throws(()=>pairTableDeltaText(NaN),/Неизвестная разница/);
const leftSelect={value:"anna"},rightSelect={value:"beketova"};
const pairMetric={value:"fantlab.dialogue.mean_dialogue_sentence_length_chars"};
const pairExportButton={disabled:true},pairCsvButton={disabled:true},pairMarkdownButton={disabled:true};
const viewStart=source.indexOf("  function updatePair() {");
const viewEnd=source.indexOf("  // Paired links carry only",viewStart);
assert(viewStart>=0&&viewEnd>viewStart,"Shipped comparison renderer missing");
const updatePair=new Function(
  "getBook","updatePairEditionContext","sharedPairRows","pairCoverageRows",
  "document","el","insertText","unit","label","pretty","exact","pairedIds",
  "pairMetric","pairOnlyShared","pairExportButton","pairCsvButton","pairMarkdownButton","leftSelect","rightSelect",
  "pairDeltaDescription","pairTableDeltaText","appendMetricDefinition",
  source.slice(viewStart,viewEnd)+"\nreturn updatePair;"
)(getBook,()=>{},sharedPairRows,pairCoverageRows,document,el,insertText,
  unit,label,pretty,exact,pairedIds,pairMetric,slots["pair-only-shared"],pairExportButton,pairCsvButton,pairMarkdownButton,leftSelect,rightSelect,pairDeltaDescription,pairTableDeltaText,appendMetricDefinition);
updatePair();
const rendered=slots["pair-rows"].children[0].children;
assert.equal(rendered.length,9);
assert.ok(rendered.every(row=>row.children[0].children[0]?.href===
  "./metrics.html#metric-"+encodeURIComponent(row.children[0].children[0].textContent)),
  "Every paired metric label must link to its matching definition");
assert.equal(rendered.filter(row=>row.children[2].textContent==="нет данных").length,2);
assert.equal(rendered.filter(row=>row.children[3].textContent==="— (нет совместного измерения)").length,2);
assert.match(slots["pair-status"].textContent,/7 из 9/);
assert.match(slots["pair-status"].textContent,/отсутствуют значения: слева 0, справа 2/);
assert.match(slots["paired-graphic"].children[0].children[0].textContent,/недоступна/);
assert.equal(slots["paired-graphic"].children[0].children.some(x=>x.className==="pair-delta"),false,
  "Unavailable metric must not create an invented delta");
assert.equal(pairExportButton.disabled,false);
assert.equal(pairCsvButton.disabled,false);
assert.equal(pairMarkdownButton.disabled,false);
// Actual checkbox filters only unavailable table rows; exports keep their measured data.
slots["pair-only-shared"].checked=true;
updatePair();
assert.equal(slots["pair-rows"].children[0].children.length,7);
assert.ok(slots["pair-rows"].children[0].children.every(row=>
  row.children[2].textContent!=="нет данных"));
assert.match(slots["pair-status"].textContent,/неполные строки скрыты только в таблице/);
assert.equal(pairExportButton.disabled,false);
assert.equal(pairCsvButton.disabled,false);
assert.equal(pairMarkdownButton.disabled,false);
// A real measured zero is still a shared observation and must remain visible.
const trueZero=lookup(beketova,"fantlab.dialogue.share_percent");
const savedZero=trueZero.actual;
try {
  trueZero.actual=0;
  updatePair();
  const zeroRow=slots["pair-rows"].children[0].children.find(row=>
    row.children[0].children[0].textContent==="fantlab.dialogue.share_percent");
  assert.equal(zeroRow.children[2].textContent,"0");
  assert.equal(zeroRow.children[3].textContent,"-34.975");
  assert.match(slots["pair-status"].textContent,/отсутствуют значения: слева 0, справа 2/,
    "Measured zero is not a missing observation");
} finally { trueZero.actual=savedZero; }
slots["pair-only-shared"].checked=false;
updatePair();
assert.equal(slots["pair-rows"].children[0].children.length,9);
assert.equal(slots["pair-rows"].children[0].children.filter(row=>
  row.children[2].textContent==="нет данных").length,2);
pairMetric.value="fantlab.general.mean_word_length_chars";
updatePair();
assert.equal(slots["paired-graphic"].children[0].children.filter(x=>x.className==="pair-row").length,2);
rightSelect.value="karamazov";
pairMetric.value="fantlab.dialogue.mean_dialogue_sentence_length_chars";
updatePair();
assert.equal(slots["pair-rows"].children[0].children.length,9);
assert.equal(slots["paired-graphic"].children[0].children.filter(x=>x.className==="pair-row").length,2);
assert.match(slots["pair-status"].textContent,/9 из 9/);
assert.match(slots["pair-status"].textContent,/отсутствуют значения: слева 0, справа 0/);
pairMetric.value="fantlab.dialogue.share_percent";
updatePair();
const delta=()=>slots["paired-graphic"].children[0].children.find(x=>x.className==="pair-delta")?.textContent;
assert.match(delta(),/^Δ \(правая − левая\): \+/);
assert.match(delta(),/п\.п\./);
assert.match(delta(),/не эффект автора или переводчика/);
leftSelect.value="karamazov";
rightSelect.value="anna";
updatePair();
assert.match(delta(),/^Δ \(правая − левая\): −/);
assert.match(delta(),/п\.п\./);
// Exercise the actual table renderer with source-free synthetic precision cases.
const id="fantlab.dialogue.share_percent";
const leftValue=lookup(anna,id).actual;
const rightMetric=lookup(karamazov,id);
const savedRightValue=rightMetric.actual;
const tableDelta=()=>slots["pair-rows"].children[0].children
  .find(row=>row.children[0].children[0].textContent===id).children[3].textContent;
try {
  rightMetric.actual=leftValue+0.0001;
  leftSelect.value="anna";rightSelect.value="karamazov";updatePair();
  assert.equal(tableDelta(),"+<0,001");
  leftSelect.value="karamazov";rightSelect.value="anna";updatePair();
  assert.equal(tableDelta(),"−<0,001","Reversed pair must flip the tiny sign");
  rightMetric.actual=leftValue;
  leftSelect.value="anna";rightSelect.value="karamazov";updatePair();
  assert.equal(tableDelta(),"0","Measured equality is not missing");
} finally {
  rightMetric.actual=savedRightValue;
}
// Missing counts are per side, not the number of distinct absent metric IDs.
// The same field missing from both editions must contribute once to each count.
const missingId="fantlab.dialogue.share_percent";
const leftMissingRow=lookup(anna,missingId),rightMissingRow=lookup(karamazov,missingId);
const oldLeft=leftMissingRow.actual,oldRight=rightMissingRow.actual;
try {
  leftMissingRow.actual=null;
  rightMissingRow.actual=null;
  leftSelect.value="anna";rightSelect.value="karamazov";
  updatePair();
  assert.match(slots["pair-status"].textContent,/8 из 9/);
  assert.match(slots["pair-status"].textContent,/отсутствуют значения: слева 1, справа 1/);
  assert.equal(slots["pair-rows"].children[0].children.find(row=>
    row.children[0].children[0].textContent===missingId).children[3].textContent,
    "— (нет совместного измерения)");
} finally {
  leftMissingRow.actual=oldLeft;
  rightMissingRow.actual=oldRight;
}
console.log("Reader pair coverage: complete/partial, per-side missingness, zero, DOM and chart PASS");
