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
const slots=Object.fromEntries(["pair-rows","paired-graphic","pair-status","pair-caption"]
  .map(id=>[id,new Node(id)]));
const el=id=>{assert.ok(Object.hasOwn(slots,id));return slots[id];};
const insertText=(parent,tag,value,cls)=>{
  const n=new Node(tag);n.textContent=value;
  if(cls)n.className=cls;parent.appendChild(n);return n;
};
const unit=id=>id.endsWith("_percent")||id==="fantlab.dialogue.share_percent"?"%":
  id.includes("length_chars")?"символов / предложение":"на 1000 слов";
const label=id=>id;
const pretty=(n,places=2)=>n.toFixed(places);
const exact=String;
const leftSelect={value:"anna"},rightSelect={value:"beketova"};
const pairMetric={value:"fantlab.dialogue.mean_dialogue_sentence_length_chars"};
const pairExportButton={disabled:true},pairCsvButton={disabled:true};
const viewStart=source.indexOf("  function updatePair() {");
const viewEnd=source.indexOf("  // Paired links carry only",viewStart);
assert(viewStart>=0&&viewEnd>viewStart,"Shipped comparison renderer missing");
const updatePair=new Function(
  "getBook","updatePairEditionContext","sharedPairRows","pairCoverageRows",
  "document","el","insertText","unit","label","pretty","exact","pairedIds",
  "pairMetric","pairExportButton","pairCsvButton","leftSelect","rightSelect",
  source.slice(viewStart,viewEnd)+"\nreturn updatePair;"
)(getBook,()=>{},sharedPairRows,pairCoverageRows,document,el,insertText,
  unit,label,pretty,exact,pairedIds,pairMetric,pairExportButton,pairCsvButton,leftSelect,rightSelect);
updatePair();
const rendered=slots["pair-rows"].children[0].children;
assert.equal(rendered.length,9);
assert.equal(rendered.filter(row=>row.children[2].textContent==="нет данных").length,2);
assert.equal(rendered.filter(row=>row.children[3].textContent==="— (нет совместного измерения)").length,2);
assert.match(slots["pair-status"].textContent,/7 из 9/);
assert.match(slots["paired-graphic"].children[0].children[0].textContent,/недоступна/);
assert.equal(pairExportButton.disabled,false);
assert.equal(pairCsvButton.disabled,false);
pairMetric.value="fantlab.general.mean_word_length_chars";
updatePair();
assert.equal(slots["paired-graphic"].children[0].children.filter(x=>x.className==="pair-row").length,2);
rightSelect.value="karamazov";
pairMetric.value="fantlab.dialogue.mean_dialogue_sentence_length_chars";
updatePair();
assert.equal(slots["pair-rows"].children[0].children.length,9);
assert.equal(slots["paired-graphic"].children[0].children.filter(x=>x.className==="pair-row").length,2);
assert.match(slots["pair-status"].textContent,/9 из 9/);
console.log("Reader pair coverage: complete/partial, missing/nonfinite, zero, DOM and chart PASS");
