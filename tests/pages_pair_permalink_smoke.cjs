/* Run the shipped pair-routing functions in Node without external packages. */
"use strict";
const fs=require("node:fs"),path=require("node:path"),assert=require("node:assert/strict");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const catalog=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const start=source.indexOf("  function pairFromUrl() {");
const end=source.indexOf("  function exportSelected() {",start);
assert(start>=0&&end>start,"Shipped pair-route functions not found");
const books=catalog.books.filter(b=>b.text_status==="measured");
const getBook=k=>books.find(b=>b.key===k);
const window={
  location:new URL("https://drevendev.github.io/Scriptorium/?book=silver&left=waves&right=beketova&pair_metric=fantlab.punctuation.dash.per_1000_words#pairs"),
  history:{pushes:[],pushState(_state,_title,url){
    this.pushes.push(String(url));
    window.location=new URL(String(url),window.location.href);
  }}
};
const l={value:"anna"},r={value:"karamazov"};
const choices=["fantlab.dialogue.share_percent","fantlab.general.mean_sentence_length_chars",
  "fantlab.punctuation.comma.per_1000_words","fantlab.punctuation.dash.per_1000_words",
  "fantlab.general.mean_word_length_chars"];
const pairMetric={value:choices[0],options:choices.map(value=>({value}))};
const pairedIds=[...choices,"fantlab.dialogue.author_text_inside_dialogue_percent",
                 "fantlab.punctuation.question.per_1000_words"];
const share={hidden:false,href:"",textContent:"",removeAttribute(k){assert.equal(k,"href");this.href="";}};
const el=id=>{assert.equal(id,"share-pair");return share;};
let renders=0;
const routes=new Function("window","getBook","leftSelect","rightSelect","pairMetric",
  "pairedIds","updatePair","el",
  source.slice(start,end)+"\nreturn {pairFromUrl,pairMetricFromUrl,selectPairMetric,selectPair};"
)(window,getBook,l,r,pairMetric,pairedIds,()=>{renders++;},el);
assert.equal(routes.pairMetricFromUrl(),"fantlab.punctuation.dash.per_1000_words");
pairMetric.value=routes.pairMetricFromUrl();
assert.deepEqual(routes.pairFromUrl(),["waves","beketova"]);
routes.selectPair(...routes.pairFromUrl());
assert.equal(l.value,"waves");
assert.equal(r.value,"beketova");
assert.equal(share.href,"?left=waves&right=beketova&pair_metric=fantlab.punctuation.dash.per_1000_words#pairs");
assert.match(share.textContent,/Гранта/);
assert.equal(window.history.pushes.length,0);
routes.selectPair("anna","silver",true);
assert.equal(window.location.search,"?book=silver&left=anna&right=silver&pair_metric=fantlab.punctuation.dash.per_1000_words");
assert.equal(window.location.hash,"#pairs");
assert.equal(window.history.pushes.length,1);
assert.equal(renders,2);
for(const query of [
 "?left=road&right=anna",
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
routes.selectPair("road","anna",true);
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
window.location=new URL("https://drevendev.github.io/Scriptorium/?book=anna&left=anna&right=beketova#pairs");
pairMetric.value=routes.pairMetricFromUrl();
assert.equal(pairMetric.value,"fantlab.dialogue.share_percent");
routes.selectPair("anna","beketova");
routes.selectPairMetric("fantlab.general.mean_word_length_chars",true);
assert.equal(pairMetric.value,"fantlab.general.mean_word_length_chars");
assert.equal(window.location.searchParams.get("pair_metric"),pairMetric.value);
assert.equal(window.location.searchParams.get("book"),"anna");
assert.equal(window.location.searchParams.get("right"),"beketova");
assert.equal(window.location.hash,"#pairs");
assert.equal(share.href,"?left=anna&right=beketova&pair_metric=fantlab.general.mean_word_length_chars#pairs");
const validPushes=window.history.pushes.length;
for(const invalid of ["__proto__","constructor","does.not.exist",
                      "fantlab.dialogue.author_text_inside_dialogue_percent"]){
  window.location=new URL("https://drevendev.github.io/Scriptorium/?left=anna&right=beketova&pair_metric="+encodeURIComponent(invalid)+"#pairs");
  assert.equal(routes.pairMetricFromUrl(),"fantlab.dialogue.share_percent");
  routes.selectPairMetric(invalid,true);
  assert.equal(window.history.pushes.length,validPushes);
}
window.location=new URL("https://drevendev.github.io/Scriptorium/?left=silver&right=waves&pair_metric=fantlab.punctuation.comma.per_1000_words#pairs");
const [restoredLeft,restoredRight]=routes.pairFromUrl();
pairMetric.value=routes.pairMetricFromUrl();
routes.selectPair(restoredLeft,restoredRight);
assert.equal(pairMetric.value,"fantlab.punctuation.comma.per_1000_words");
assert.equal(share.href,"?left=silver&right=waves&pair_metric=fantlab.punctuation.comma.per_1000_words#pairs");
console.log("Pages pair chart permalink: allow-list, reload, back/forward, history PASS");
