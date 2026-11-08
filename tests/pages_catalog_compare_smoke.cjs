/* Run actual card-to-pair enhancement using the pinned 13-book Reader catalogue. */
"use strict";
const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const evidence=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const keys=[...html.matchAll(/<article class="book(?: book-research)?" data-status="(?:measured|pending)" data-catalog-key="([a-z]+)">/g)].map(m=>m[1]);
assert.deepEqual(keys,evidence.books.map(b=>b.key));
const catalogCards=keys.map(key=>({dataset:{catalogKey:key},children:[],appendChild(n){this.children.push(n);}}));
const getBook=key=>evidence.books.find(b=>b.key===key&&b.text_status==="measured");
const lookup=(book,id)=>book.metrics.find(m=>m.id===id);
const isNumeric=v=>typeof v==="number"&&Number.isFinite(v);
const first=source.indexOf("  const pairedIds = [");
const next=source.indexOf("  // Source-free, edition-bound",first);
assert.ok(first>=0&&next>first);
const sharedPairRows=new Function("lookup","isNumeric",source.slice(first,next)+"return sharedPairRows;")(lookup,isNumeric);
const leftSelect={value:"anna"},rightSelect={value:"karamazov"};
const pairMetric={value:"fantlab.dialogue.share_percent"};
const navigations=[],targets=[];
const target={focus(options){assert.deepEqual(options,{preventScroll:true});targets.push("focus");},
  scrollIntoView(options){assert.deepEqual(options,{block:"start"});targets.push("scroll");}};
const document={createElement(tag){
  assert.equal(tag,"button");
  return {attributes:{},events:{},setAttribute(name,value){this.attributes[name]=value;},
    addEventListener(type,fn){this.events[type]=fn;}};
}};
const start=source.indexOf("  function compareFromCatalog(key) {");
const end=source.indexOf("  function exportSelected() {",start);
assert.ok(start>0&&end>start,"Shipped verified-data compare actions not found");
const actions=new Function("data","catalogCards","getBook","leftSelect","rightSelect",
  "pairMetric","sharedPairRows","selectPair","el","document",source.slice(start,end)+
  "return {compareFromCatalog,installCatalogComparisonActions};")(
  evidence,catalogCards,getBook,leftSelect,rightSelect,pairMetric,sharedPairRows,
  (left,right,history)=>{
    assert.ok(getBook(left)&&getBook(right)&&left!==right);
    assert.equal(history,true,"Card action must update the canonical pair permalink");
    navigations.push([left,right]);leftSelect.value=left;rightSelect.value=right;
  },
  id=>{assert.equal(id,"pairs");return target;},document
);
actions.installCatalogComparisonActions();
assert.deepEqual(catalogCards.map(c=>c.children.length),[...Array(11).fill(1),0,0]);
for (const card of catalogCards.slice(0,11)) {
  const button=card.children[0];
  assert.equal(button.type,"button");
  assert.equal(button.className,"book-compare");
  assert.match(button.textContent,/Сравнить/);
  assert.match(button.attributes["aria-label"],/Сравнить «/);
  assert.equal(typeof button.events.click,"function");
}
const click=key=>catalogCards.find(c=>c.dataset.catalogKey===key).children[0].events.click();
click("karamazov");assert.deepEqual(navigations.at(-1),["karamazov","anna"]);
click("anna");assert.deepEqual(navigations.at(-1),["anna","karamazov"]);
pairMetric.value="fantlab.dialogue.mean_dialogue_sentence_length_chars";
click("beketova");assert.deepEqual(navigations.at(-1),["beketova","karamazov"]);
assert.equal(pairMetric.value,"fantlab.dialogue.share_percent",
  "Missing paired metric must select a measured chart, not fabricate a zero");
pairMetric.value="fantlab.dialogue.share_percent";
click("waves");assert.deepEqual(navigations.at(-1),["waves","karamazov"]);
assert.equal(pairMetric.value,"fantlab.dialogue.share_percent");
const before=navigations.length;
actions.compareFromCatalog("petersburg");actions.compareFromCatalog("darwin");
actions.compareFromCatalog("__proto__");
assert.equal(navigations.length,before,"Pending/invalid cards cannot compare");
assert.deepEqual(targets,Array(before).fill(["focus","scroll"]).flat());
assert.match(html,/Без JavaScript остаются исходные ссылки на свидетельства/);
assert.match(source,/selectBook\(bookFromUrl\(\)\);\s*installCatalogComparisonActions\(\);/);
console.log("Verified card-to-pair controls: 11 measured / 2 pending, safe pairing, fallback metric, history and focus PASS");
