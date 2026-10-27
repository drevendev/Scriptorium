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
  location:new URL("https://drevendev.github.io/Scriptorium/?book=silver&left=waves&right=beketova#pairs"),
  history:{pushes:[],pushState(_state,_title,url){
    this.pushes.push(String(url));
    window.location=new URL(String(url),window.location.href);
  }}
};
const l={value:"anna"},r={value:"karamazov"};
const share={hidden:false,href:"",textContent:"",removeAttribute(k){assert.equal(k,"href");this.href="";}};
const el=id=>{assert.equal(id,"share-pair");return share;};
let renders=0;
const routes=new Function("window","getBook","leftSelect","rightSelect","updatePair","el",
  source.slice(start,end)+"\nreturn {pairFromUrl,selectPair};"
)(window,getBook,l,r,()=>{renders++;},el);
assert.deepEqual(routes.pairFromUrl(),["waves","beketova"]);
routes.selectPair(...routes.pairFromUrl());
assert.equal(l.value,"waves");
assert.equal(r.value,"beketova");
assert.equal(share.href,"?left=waves&right=beketova#pairs");
assert.match(share.textContent,/Гранта/);
assert.equal(window.history.pushes.length,0);
routes.selectPair("anna","silver",true);
assert.equal(window.location.search,"?book=silver&left=anna&right=silver");
assert.equal(window.location.hash,"#pairs");
assert.equal(window.history.pushes.length,1);
assert.equal(renders,2);
for(const query of [
 "?left=resurrection&right=anna",
 "?left=anna&right=anna",
 "?left=../../secrets&right=silver",
 "?left=silver",
 "?left=SILVER&right=anna",
 "?left=__proto__&right=beketova"
]){
 window.location=new URL("https://drevendev.github.io/Scriptorium/"+query);
 assert.deepEqual(routes.pairFromUrl(),["anna","karamazov"],query);
}
const before=renders;
routes.selectPair("resurrection","anna",true);
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
console.log("Pages pair permalink valid, translation, invalid, duplicate and history PASS");
