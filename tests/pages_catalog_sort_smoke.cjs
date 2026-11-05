/* Sort the shipped eleven measured Russian texts plus two honest research leads. */
"use strict";
const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const catalog=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const start=source.indexOf("  function sortCatalog() {");
const end=source.indexOf("  function updateSingle() {",start);
assert.ok(start>=0&&end>start,"Ship the actual catalogue sorter");
const sortCode=source.slice(start,end)+"return sortCatalog;";
assert.doesNotMatch(sortCode,/getBook\(/,
  "The catalogue must not use the measured-only reader lookup for pending cards");
const keys=catalog.books.map(b=>b.key);
function harness(doc){
  const cards=keys.map(key=>({dataset:{catalogKey:key},hidden:false}));
  const nodes=[...cards];
  const grid={appendChild(card){
    const current=nodes.indexOf(card);
    assert.notEqual(current,-1);
    nodes.splice(current,1);
    nodes.push(card);
  }};
  const selection={value:"catalog"};
  const status={textContent:""};
  const sorter=new Function("catalogCards","catalogOrder","catalogGrid","data",
    "lookup","isNumeric","el",sortCode)(
    cards,selection,grid,doc,
    (book,id)=>book.metrics.find(m=>m.id===id),
    x=>typeof x==="number"&&Number.isFinite(x),
    id=>{assert.equal(id,"catalog-sort-status");return status;});
  return {sorter,selection,status,order:()=>nodes.map(c=>c.dataset.catalogKey)};
}
const h=harness(catalog);
h.sorter();
assert.deepEqual(h.order(),keys,"Default and static catalogue must match");
h.selection.value="title";h.sorter();
const collator=new Intl.Collator("ru",{sensitivity:"base",numeric:true});
const sortedTitles=catalog.books.map((book,index)=>({book,index}))
  .sort((a,b)=>collator.compare(a.book.display_title,b.book.display_title)||a.index-b.index)
  .map(x=>x.book.key);
assert.deepEqual(h.order(),sortedTitles);
assert.match(h.status.textContent,/клавиатуры/);
h.selection.value="dialogue";h.sorter();
const expected=catalog.books.map((book,index)=>({
  book,index,value:book.text_status==="measured"
    ?book.metrics.find(m=>m.id==="fantlab.dialogue.share_percent")?.actual??null:null
})).sort((a,b)=>{
  if(a.value===null)return b.value===null?a.index-b.index:1;
  if(b.value===null)return -1;
  return b.value-a.value||a.index-b.index;
}).map(x=>x.book.key);
assert.deepEqual(h.order(),expected);
assert.deepEqual(h.order().slice(-2),["petersburg","darwin"],"Pending works cannot be ranked as measured");
assert.match(h.status.textContent,/Ноль не означает отсутствие данных/);
h.selection.value="__proto__";h.sorter();
assert.equal(h.selection.value,"catalog");
assert.deepEqual(h.order(),keys,"Unknown sort modes fail closed");
const synthetic=structuredClone(catalog);
synthetic.books.find(b=>b.key==="anna").metrics
  .find(m=>m.id==="fantlab.dialogue.share_percent").actual=0;
synthetic.books.find(b=>b.key==="shishmareva").metrics
  .find(m=>m.id==="fantlab.dialogue.share_percent").actual=null;
const z=harness(synthetic);z.selection.value="dialogue";z.sorter();
assert.deepEqual(z.order().slice(-4),["anna","shishmareva","petersburg","darwin"],
  "Numeric zero before missing observations; missing measurement before research leads");
assert.match(html,/<select id="catalog-order" disabled>[\s\S]*?value="dialogue"/);
assert.match(html,/id="catalog-sort-status" role="status" aria-live="polite"/);
assert.match(source,/catalogOrder.addEventListener\("change",\(\)=>\{sortCatalog\(\);updateCatalog\(\);\}\)/);
assert.match(source,/sortCatalog\(\);\n      el\("catalog-tools"\)\.hidden=false;/);
assert.doesNotMatch(source,/innerHTML/);
console.log("Real catalogue title/metric DOM sorting, zero, unknown, no-JS and keyboard order: PASS");
