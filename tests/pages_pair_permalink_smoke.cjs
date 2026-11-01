/* Run the shipped pair-routing functions in Node without external packages. */
"use strict";
const fs=require("node:fs"),path=require("node:path"),assert=require("node:assert/strict");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const catalog=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const start=source.indexOf("  function pairMetricFromUrl() {");
const end=source.indexOf("  function exportSelected() {",start);
assert(start>=0&&end>start,"Shipped pair-route functions not found");
const books=catalog.books.filter(b=>b.text_status==="measured");
const getBook=k=>books.find(b=>b.key===k);
const window={
  location:new URL("https://drevendev.github.io/Scriptorium/?book=silver&left=waves&right=beketova#pairs"),
  history:{pushes:[],pushState(_state,_title,url){
    this.pushes.push(String(url));
    window.location=new URL(String(url),window.location.href);
  }}
};
const l={value:"anna"},r={value:"karamazov"},swap={disabled:true};
const pairMetric={value:"fantlab.dialogue.share_percent",options:[
  "fantlab.dialogue.share_percent","fantlab.general.mean_sentence_length_chars",
  "fantlab.punctuation.comma.per_1000_words","fantlab.punctuation.dash.per_1000_words",
  "fantlab.general.mean_word_length_chars"].map(value=>({value}))};
const share={hidden:false,href:"",textContent:"",removeAttribute(k){assert.equal(k,"href");this.href="";}};
const el=id=>{assert.equal(id,"share-pair");return share;};
let renders=0;
const routes=new Function("window","getBook","leftSelect","rightSelect","pairMetric","updatePair","el","pairSwapButton",
  source.slice(start,end)+"\nreturn {pairMetricFromUrl,pairFromUrl,selectPair,swapPair};"
)(window,getBook,l,r,pairMetric,()=>{renders++;},el,swap);
assert.deepEqual(routes.pairFromUrl(),["waves","beketova"]);
assert.equal(routes.pairMetricFromUrl(),"fantlab.dialogue.share_percent");
routes.selectPair(...routes.pairFromUrl());
assert.equal(l.value,"waves");
assert.equal(r.value,"beketova");
assert.equal(share.href,"?left=waves&right=beketova&pair_metric=fantlab.dialogue.share_percent#pairs");
assert.match(share.textContent,/Гранта/);
assert.equal(window.history.pushes.length,0);
pairMetric.value="fantlab.punctuation.dash.per_1000_words";
routes.selectPair("anna","silver",true);
assert.equal(window.location.search,"?book=silver&left=anna&right=silver&pair_metric=fantlab.punctuation.dash.per_1000_words");
assert.equal(share.href,"?left=anna&right=silver&pair_metric=fantlab.punctuation.dash.per_1000_words#pairs");
assert.equal(window.location.hash,"#pairs");
assert.equal(window.history.pushes.length,1);
assert.equal(renders,2);
for(const invalid of ["__proto__","constructor","toString","unknown",""]){
 window.location=new URL("https://drevendev.github.io/Scriptorium/?left=anna&right=silver&pair_metric="+encodeURIComponent(invalid));
 assert.equal(routes.pairMetricFromUrl(),"fantlab.dialogue.share_percent",invalid);
}
window.location=new URL("https://drevendev.github.io/Scriptorium/?left=anna&right=silver&pair_metric=fantlab.general.mean_sentence_length_chars");
assert.equal(routes.pairMetricFromUrl(),"fantlab.general.mean_sentence_length_chars");
pairMetric.value=routes.pairMetricFromUrl();
routes.selectPair(...routes.pairFromUrl());
assert.equal(share.href,"?left=anna&right=silver&pair_metric=fantlab.general.mean_sentence_length_chars#pairs");
for(const query of [
 "?left=petersburg&right=anna",
 "?left=anna&right=anna",
 "?left=../../secrets&right=silver",
 "?left=silver",
 "?left=SILVER&right=anna",
 "?left=__proto__&right=beketova"
]){
 window.location=new URL("https://drevendev.github.io/Scriptorium/"+query);
 assert.deepEqual(routes.pairFromUrl(),["anna","karamazov"],query);
}
window.location=new URL("https://drevendev.github.io/Scriptorium/?left=resurrection&right=anna#pairs");
assert.deepEqual(routes.pairFromUrl(),["resurrection","anna"]);
const before=renders;
routes.selectPair("petersburg","anna",true);
assert.equal(renders,before);
assert.equal(window.history.pushes.length,1);
routes.selectPair("anna","anna",true);
assert.equal(share.hidden,true);
assert.equal(share.href,"");
assert.equal(window.history.pushes.length,1);
window.location=new URL("https://drevendev.github.io/Scriptorium/?left=karamazov&right=hyperboloid#pairs");
routes.selectPair(...routes.pairFromUrl());
assert.equal(l.value,"karamazov");
assert.equal(r.value,"hyperboloid");
assert.equal(window.history.pushes.length,1);
assert.equal(share.hidden,false);
assert.equal(swap.disabled,false);
window.location=new URL("https://drevendev.github.io/Scriptorium/?book=silver&left=karamazov&right=hyperboloid&pair_metric=fantlab.punctuation.comma.per_1000_words#pairs");
pairMetric.value="fantlab.punctuation.comma.per_1000_words";
routes.selectPair(...routes.pairFromUrl());
const count=window.history.pushes.length;
routes.swapPair();
assert.equal(l.value,"hyperboloid");
assert.equal(r.value,"karamazov");
assert.equal(pairMetric.value,"fantlab.punctuation.comma.per_1000_words");
assert.equal(window.location.search,"?book=silver&left=hyperboloid&right=karamazov&pair_metric=fantlab.punctuation.comma.per_1000_words");
assert.equal(share.href,"?left=hyperboloid&right=karamazov&pair_metric=fantlab.punctuation.comma.per_1000_words#pairs");
assert.equal(window.history.pushes.length,count+1);
routes.swapPair();
assert.equal(l.value,"karamazov");
assert.equal(r.value,"hyperboloid");
routes.selectPair("anna","anna",true);
assert.equal(swap.disabled,true);
routes.swapPair();
assert.equal(window.history.pushes.length,count+2);
routes.selectPair("anna","beketova");
assert.equal(swap.disabled,false);
routes.swapPair();
assert.equal(l.value,"beketova");
assert.equal(r.value,"anna");
console.log("Pages pair permalink, safe swap, translator, duplicate and history PASS");
