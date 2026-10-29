/* Real, pinned ten-book catalogue against the shipped filter implementation. */
"use strict";
const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const js=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const data=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const css=fs.readFileSync(path.join(root,"assets/pages-reader.css"),"utf8");
const cards0=[...html.matchAll(/<article class="book(?: book-research)?" data-status="(measured|pending)" data-catalog-key="([a-z]+)">/g)];
assert.equal(cards0.length,10);
assert.deepEqual(cards0.map(m=>m[2]),data.books.map(b=>b.key));
const cards=cards0.map(m=>({dataset:{status:m[1],catalogKey:m[2]},hidden:false}));
const filter={value:"all"},search={value:""},status={textContent:""};
const s=js.indexOf("  function updateCatalog() {"),e=js.indexOf("  function updateSingle() {",s);
assert.ok(s>=0&&e>s);
const code=js.slice(s,e)+"return updateCatalog;";
const make=d=>new Function("data","catalogCards","catalogFilter","catalogSearch","el",code)(
  d,cards,filter,search,id=>{assert.equal(id,"catalog-filter-status");return status;});
const run=make(data);
for(const [mode,keys,measured,pending] of [
 ["all",data.books.map(b=>b.key),7,3],
 ["measured",["anna","waves","silver","karamazov","hyperboloid","beketova","resurrection"],7,0],
 ["pending",["road","petersburg","darwin"],0,3],
 ["translated",["beketova","darwin"],1,1],
 ["unknown",data.books.map(b=>b.key),7,3]]){
 filter.value=mode;run();
 assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),keys,mode);
 assert.ok(status.textContent.includes(measured+" измерено, "+pending+" в подготовке"),mode);
}
for(const [q,mode,keys] of [
 ["Толстой","all",["anna","hyperboloid","resurrection"]],
 ["Лев Толстой","all",["anna","resurrection"]],
 ["БЕКЕТОВА","all",["beketova"]],
 ["Рачинский","translated",["darwin"]],
 ["О ПРОИСХОЖДЕНИИ","all",["darwin"]],
 ["Бекетова","pending",[]],
 ["несуществующая книга","all",[]]
]){
 search.value=q;filter.value=mode;run();
 assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),keys,q);
 if(!keys.length)assert.match(status.textContent,/Книг не найдено/);
}
search.value="";filter.value="all";run();
assert.equal(cards.filter(c=>!c.hidden).length,10);
const tampered=structuredClone(data);tampered.books=tampered.books.filter(b=>b.key!=="darwin");
assert.throws(()=>make(tampered)(),/Нет проверенного источника/);
assert.match(html,/id="catalog-tools" hidden/);
assert.match(html,/id="catalog-filter" disabled/);
assert.match(html,/id="catalog-search" type="search" autocomplete="off"[^>]*disabled/);
assert.match(js,/catalogSearch.addEventListener\("input",updateCatalog\)/);
assert.match(js,/verify\(incoming\); data=incoming/);
assert.match(js,/el\("catalog-tools"\)\.hidden=false/);
assert.match(css,/\.catalog-tools\[hidden\],\.book\[hidden\]\s*\{\s*display:none\s*!important/);
assert.match(css,/@media print\s*\{\s*\.catalog-tools\s*\{\s*display:none/);
console.log("Verified catalogue filters, searchable Russian titles/authors/translators, combined empty states and no-JS fallback: PASS");
