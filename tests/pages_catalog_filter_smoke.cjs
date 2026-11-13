/* Real, pinned eleven-book catalogue against the shipped filter implementation. */
"use strict";
const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const js=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const data=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const css=fs.readFileSync(path.join(root,"assets/pages-reader.css"),"utf8");
const cards0=[...html.matchAll(/<article class="book(?: book-research)?" data-status="(measured|pending)" data-catalog-key="([a-z]+)">/g)];
assert.equal(cards0.length,13);
assert.deepEqual(cards0.map(m=>m[2]),data.books.map(b=>b.key));
const cards=cards0.map(m=>({dataset:{status:m[1],catalogKey:m[2]},hidden:false}));
const domOrder=[...cards];
const catalogGrid={appendChild(card){
  const previous=domOrder.indexOf(card);
  assert.notEqual(previous,-1,"Cannot reorder a foreign catalogue card");
  domOrder.splice(previous,1);
  domOrder.push(card);
}};
const filter={value:"all"},origin={value:"all"},order={value:"catalog"},search={value:"",focused:false,focus(){this.focused=true;}},status={textContent:""};
const empty={hidden:true},sortStatus={textContent:""};
const share={hidden:false,href:"",textContent:"",removeAttribute(name){
  assert.equal(name,"href");this.href="";
}};
const location={search:"",href:"https://drevendev.github.io/Scriptorium/"};
const browser={location,history:{replaceState(_state,_title,url){
  location.href=String(url);location.search=new URL(location.href).search;
}}};
const s=js.indexOf("  function updateCatalog() {"),e=js.indexOf("  function updateSingle() {",s);
assert.ok(s>=0&&e>s);
const code=js.slice(s,e)+"return {updateCatalog,restoreCatalogFromUrl,resetCatalog};";
const make=d=>new Function("data","catalogCards","catalogFilter","catalogOrigin","catalogSearch","catalogOrder",
  "catalogGrid","lookup","isNumeric","el","window",code)(
  d,cards,filter,origin,search,order,catalogGrid,
  (book,id)=>book.metrics.find(m=>m.id===id),
  value=>typeof value==="number"&&Number.isFinite(value),
  id=>id==="share-catalog"?share:id==="catalog-empty"?empty:
    id==="catalog-sort-status"?sortStatus:status,browser);
const {updateCatalog:run,restoreCatalogFromUrl:restore,resetCatalog,sortCatalog}=make(data);
for(const [mode,keys,measured,pending] of [
 ["all",data.books.map(b=>b.key),11,2],
 ["measured",["anna","waves","silver","karamazov","hyperboloid","beketova","resurrection","road","oblomov","humiliated","shishmareva"],11,0],
 ["pending",["petersburg","darwin"],0,2],
 ["translated",["beketova","shishmareva","darwin"],2,1],
 ["unknown",data.books.map(b=>b.key),11,2]]){
 filter.value=mode;run();
 assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),keys,mode);
 assert.ok(status.textContent.includes(measured+" измерено, "+pending+" в подготовке"),mode);
 assert.equal(empty.hidden,true,mode);
}
// The original-language facet is about edition provenance, not the language
// of the measured prose: English/French originals are NOT measured here.
for(const [language,keys,measured,pending] of [
 ["ru",["anna","waves","silver","karamazov","hyperboloid","resurrection","road","oblomov","humiliated","petersburg"],9,1],
 ["en",["shishmareva","darwin"],1,1],
 ["fr",["beketova"],1,0],
 ["all",data.books.map(b=>b.key),11,2]
]){
 origin.value=language;filter.value="all";search.value="";run();
 assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),keys,language);
 assert.match(status.textContent,new RegExp(measured+" измерено, "+pending+" в подготовке"));
}
origin.value="en";filter.value="measured";search.value="Дефо";run();
assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),["shishmareva"]);
origin.value="fr";filter.value="pending";search.value="";run();
assert.equal(cards.filter(c=>!c.hidden).length,0);
assert.equal(empty.hidden,false);
origin.value="all";filter.value="all";search.value="";run();
for(const [q,mode,keys] of [
 ["Толстой","all",["anna","hyperboloid","resurrection"]],
 ["Гончаров","all",["oblomov"]],
 ["Достоевский","all",["karamazov","humiliated"]],
 ["Лев Толстой","all",["anna","resurrection"]],
 ["БЕКЕТОВА","all",["beketova"]],
 ["Верн Бекетова","all",["beketova"]],
 ["БЕКЕТОВА   Верн","translated",["beketova"]],
 ["Дефо Шишмарева","all",["shishmareva"]],
 ["Шишмарева Дефо","translated",["shishmareva"]],
 ["  Верн    Бекетова  ","all",["beketova"]],
 ["Толстой Бекетова","all",[]],
 ["Рачинский","translated",["darwin"]],
 ["Шишмарёва","translated",["shishmareva"]],
 ["О ПРОИСХОЖДЕНИИ","all",["darwin"]],
 ["Бекетова","pending",[]],
 ["несуществующая книга","all",[]]
]){
 search.value=q;filter.value=mode;run();
 assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),keys,q);
 if(!keys.length)assert.match(status.textContent,/Книг не найдено/);
 assert.equal(empty.hidden,keys.length!==0,q);
}
search.value="";filter.value="all";run();
assert.equal(cards.filter(c=>!c.hidden).length,13);
assert.equal(share.href,"?catalog=all#books");
order.value="dialogue";run();
assert.equal(share.href,"?catalog=all&catalog_order=dialogue#books");
origin.value="fr";filter.value="translated";search.value="Верн";run();
assert.equal(share.href,"?catalog=translated&original=fr&q="+encodeURIComponent("Верн")+"&catalog_order=dialogue#books");
location.search="?catalog=translated&original=fr&q="+encodeURIComponent("Верн")+"&catalog_order=dialogue";
restore();assert.equal(origin.value,"fr");
assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),["beketova"]);
origin.value="all";filter.value="all";search.value="";run();
order.value="length";run();
assert.equal(share.href,"?catalog=all&catalog_order=length#books");
search.value="Бекетова";filter.value="translated";run();
assert.equal(share.href,"?catalog=translated&q="+encodeURIComponent("Бекетова")+"&catalog_order=length#books");
order.value="dialogue";run();
assert.equal(share.href,"?catalog=translated&q="+encodeURIComponent("Бекетова")+"&catalog_order=dialogue#books");
location.search="?catalog=translated&q="+encodeURIComponent("Бекетова")+"&catalog_order=length";
restore();
assert.equal(order.value,"length");
assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),["beketova"]);
assert.equal(share.href,"?catalog=translated&q="+encodeURIComponent("Бекетова")+"&catalog_order=length#books");
location.search="?catalog=translated&q="+encodeURIComponent("Бекетова")+"&catalog_order=title";
restore();
assert.equal(order.value,"title");
assert.equal(filter.value,"translated");assert.equal(search.value,"Бекетова");
assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),["beketova"]);
assert.equal(share.href,"?catalog=translated&q="+encodeURIComponent("Бекетова")+"&catalog_order=title#books");
location.search="?catalog=pending&q="+encodeURIComponent("Бекетова");
restore();assert.equal(cards.filter(c=>!c.hidden).length,0);
assert.match(status.textContent,/Книг не найдено/);
assert.equal(empty.hidden,false);
location.href="https://drevendev.github.io/Scriptorium/?left=anna&right=beketova&catalog=pending&catalog_order=length&q=%D0%91%D0%B5%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%D0%B0#books";
location.search=new URL(location.href).search;
restore();assert.equal(empty.hidden,false);
assert.equal(order.value,"length");
sortCatalog();
assert.notDeepEqual(domOrder.map(c=>c.dataset.catalogKey),data.books.map(b=>b.key),
  "Reproduce filtered, ranked DOM order before resetting");
resetCatalog();
assert.equal(empty.hidden,true);
assert.equal(order.value,"catalog","Reset must restore the visible sort control");
assert.deepEqual(domOrder.map(c=>c.dataset.catalogKey),data.books.map(b=>b.key),
  "Reset must restore actual DOM/keyboard order, not just the sort label");
assert.match(sortStatus.textContent,/Исходный порядок каталога/);
assert.equal(search.value,"");assert.equal(filter.value,"all");assert.equal(origin.value,"all");
assert.equal(cards.filter(c=>!c.hidden).length,13);
assert.equal(search.focused,true);
const clean=new URL(location.href);
assert.equal(clean.searchParams.has("catalog"),false);
assert.equal(clean.searchParams.has("q"),false);
assert.equal(clean.searchParams.has("original"),false);
assert.equal(clean.searchParams.has("catalog_order"),false,
  "Reset must not leave a stale sorted catalogue permalink");
assert.equal(clean.searchParams.get("left"),"anna");
assert.equal(clean.searchParams.get("right"),"beketova");
location.search="?catalog=__proto__&original=__proto__&q="+encodeURIComponent("Толстой")+"&catalog_order=__proto__";
restore();assert.equal(filter.value,"all");assert.equal(origin.value,"all");assert.equal(order.value,"catalog");
assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),
                 ["anna","hyperboloid","resurrection"]);
location.search="?catalog=measured&q="+encodeURIComponent("x".repeat(121));
restore();assert.equal(search.value,"");
assert.equal(cards.filter(c=>!c.hidden).length,11);
location.search="?catalog=translated&q="+encodeURIComponent("\u0000");
restore();assert.equal(search.value,"");
assert.equal(cards.filter(c=>!c.hidden).length,3);
search.value="<img src=x>";filter.value="all";run();
assert.ok(!share.href.includes("<img"));assert.ok(share.href.includes("%3Cimg"));
search.value="x".repeat(121);run();assert.equal(share.hidden,true);
assert.equal(share.href,"");
search.value="";filter.value="all";run();
const tampered=structuredClone(data);tampered.books=tampered.books.filter(b=>b.key!=="darwin");
assert.throws(()=>make(tampered).updateCatalog(),/Нет проверенного источника/);
assert.match(html,/id="catalog-tools" hidden/);
assert.match(html,/id="catalog-empty" class="catalog-empty" hidden/);
assert.match(html,/id="catalog-reset" type="button" disabled/);
assert.match(html,/Показано 13 из 13 книг/);
assert.match(js,/catalogReset.addEventListener\("click",resetCatalog\)/);
assert.match(js,/catalogOrder.value="catalog";/);
assert.match(js,/url.searchParams.delete\("catalog_order"\)/);
assert.match(css,/\.catalog-empty\[hidden\]\s*\{\s*display:none\s*!important/);
assert.match(html,/id="catalog-filter" disabled/);
assert.match(html,/id="catalog-origin" aria-describedby="catalog-origin-help" disabled/);
assert.match(html,/id="catalog-origin-help"/);
assert.match(js,/catalogOrigin.addEventListener\("change",updateCatalog\)/);
assert.match(html,/id="catalog-search" type="search" autocomplete="off"[^>]*disabled/);
assert.match(html,/id="catalog-search"[^>]*maxlength="120"/);
assert.match(html,/id="share-catalog" href="\?catalog=all#books"/);
assert.match(js,/catalogSearch.addEventListener\("input",updateCatalog\)/);
assert.match(js,/catalogOrder.addEventListener\("change",\(\)=>\{sortCatalog\(\);updateCatalog\(\);\}\)/);
assert.match(js,/restoreCatalogFromUrl\(\);\s*sortCatalog\(\);\s*restoreChartFromUrl\(\)/);
assert.match(js,/verify\(incoming\); data=incoming/);
assert.match(js,/el\("catalog-tools"\)\.hidden=false/);
assert.match(css,/\.catalog-tools\[hidden\],\.book\[hidden\]\s*\{\s*display:none\s*!important/);
assert.match(css,/@media print\s*\{\s*\.catalog-tools\s*\{\s*display:none/);
console.log("Verified catalogue filters, zero-result recovery, safe reset URLs, invalid inputs and no-JS fallback: PASS");
