/* Exercise the shipped Reader's evidence-bound metric-neighbor ranking and DOM links. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const data=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const begin=source.indexOf("  // Reader extension v1:");
const end=source.indexOf("  function updateSingle() {",begin);
assert.ok(begin>=0&&end>begin,"Use the actual shipped neighbor implementation");

const lookup=(book,id)=>book.metrics.find(m=>m.id===id);
const isNumeric=n=>typeof n==="number"&&Number.isFinite(n);
class Node {
  constructor(tag){this.tag=tag;this.children=[];this.textContent="";this.href="";}
  appendChild(child){this.children.push(child);return child;}
  replaceChildren(...nodes){this.children=nodes;}
}
const document={createElement:tag=>new Node(tag),createDocumentFragment:()=>new Node("#fragment")};
const slots={"neighbor-list":new Node("ol"),"neighbor-status":new Node("p")};
const el=id=>{assert.ok(Object.hasOwn(slots,id));return slots[id];};
const insertText=(parent,tag,text)=>{
  const node=new Node(tag);node.textContent=text;parent.appendChild(node);return node;
};
const pretty=n=>n.toFixed(3);
const {neighborMetricIds,measuredNeighborValue,rankMetricNeighbors,updateMetricNeighbors}
  =new Function("lookup","isNumeric","el","data","document","insertText","pretty",
    source.slice(begin,end)+
    "\nreturn {neighborMetricIds,measuredNeighborValue,rankMetricNeighbors,updateMetricNeighbors};"
  )(lookup,isNumeric,el,data,document,insertText,pretty);

assert.deepEqual(neighborMetricIds,[
  "fantlab.dialogue.share_percent",
  "fantlab.general.mean_sentence_length_chars",
  "fantlab.punctuation.comma.per_1000_words"
]);
const measured=data.books.filter(b=>b.text_status==="measured");
const anna=measured.find(b=>b.key==="anna");
const ranked=rankMetricNeighbors(anna,data.books);
assert.equal(ranked.length,3);
assert.ok(ranked.every(item=>item.book!==anna&&item.book.text_status==="measured"));
assert.ok(ranked.every(item=>Number.isFinite(item.distance)&&item.distance>=0&&item.distance<=1));
assert.ok(ranked.every((item,i)=>i===0||ranked[i-1].distance<=item.distance));
assert.ok(ranked.every(item=>neighborMetricIds.every(id=>isNumeric(measuredNeighborValue(item.book,id)))));
assert.ok(ranked.every(item=>["metrics","normalization","dialogue","vocabulary","punctuation"]
  .every(p=>item.book.profiles[p]===anna.profiles[p])));
const spans=neighborMetricIds.map(id=>{
  const vals=measured.map(book=>lookup(book,id).actual);
  return Math.max(...vals)-Math.min(...vals);
});
const reference=measured.filter(b=>b!==anna).map((book,index)=>({
  book,order:index,distance:neighborMetricIds.reduce((acc,id,i)=>
    acc+(spans[i]===0?0:Math.abs(lookup(book,id).actual-lookup(anna,id).actual)/spans[i]),0)/3
})).sort((a,b)=>a.distance-b.distance||a.order-b.order).slice(0,3);
assert.deepEqual(ranked.map(x=>x.book.key),reference.map(x=>x.book.key));
for(let i=0;i<ranked.length;i++)assert.ok(Math.abs(ranked[i].distance-reference[i].distance)<1e-12);

updateMetricNeighbors(anna);
const links=slots["neighbor-list"].children[0].children.map(li=>li.children[0]);
assert.equal(links.length,3);
assert.deepEqual(links.map(link=>link.href),ranked.map(item=>
  "?left=anna&right="+item.book.key+
  "&pair_metric=fantlab.dialogue.share_percent#pairs"));
assert.ok(links.every(link=>link.textContent.includes("сравнить")));
assert.match(slots["neighbor-status"].textContent,/не авторский профиль/);
assert.doesNotMatch(JSON.stringify(slots),/PRIVATE SOURCE TEXT/);

const ids=neighborMetricIds;
function book(key,vals,profile="v1",status="measured"){
  return {key,text_status:status,profiles:{
    metrics:profile,normalization:profile,dialogue:profile,vocabulary:profile,punctuation:profile
  },metrics:ids.map((id,i)=>({id,actual:vals[i],status:vals[i]===null?"not_run":"measured"}))};
}
const anchor=book("a",[0,0,0]);
const identical=book("b",[0,0,0]),far=book("c",[10,10,10]);
const notMeasured=book("d",[0,0,0],"v1","pending");
const otherProfile=book("e",[0,0,0],"v2");
const synthetic=rankMetricNeighbors(anchor,[anchor,identical,far,notMeasured,otherProfile]);
assert.deepEqual(synthetic.map(x=>[x.book.key,x.distance]),[["b",0],["c",1]]);
assert.deepEqual(rankMetricNeighbors(anchor,[anchor,identical]),[],
  "Constant columns alone cannot support a nearest-neighbor recommendation");
assert.deepEqual(rankMetricNeighbors(anchor,[anchor,book("x",[null,1,1])]),[],
  "Unknown is not a measured zero");
assert.deepEqual(rankMetricNeighbors(anchor,[anchor,otherProfile]),[],
  "Incompatible profiles must not create dead comparison links");
assert.deepEqual(rankMetricNeighbors(notMeasured,[anchor,notMeasured]),[]);
assert.match(html,/<aside class="neighbor-panel" id="measured-neighbors"/);
assert.match(html,/id="neighbor-list"/);
assert.match(html,/id="neighbor-status" role="status" aria-live="polite"/);
assert.match(html,/стартовая пара, не вычисленная рекомендация/);
assert.match(source,/updateSingle\(\);\n    updateMetricNeighbors\(book\);/);
assert.doesNotMatch(source,/innerHTML/);
console.log("Reader measured neighbors: real ranking, pair links, profiles, missing/zero, static fallback PASS");
