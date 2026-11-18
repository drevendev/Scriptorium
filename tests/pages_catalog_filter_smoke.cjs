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
const cards=cards0.map(m=>({dataset:{status:m[1],catalogKey:m[2]},hidden:false,
  focused:false,focus(){this.focused=true;}}));
const domOrder=[...cards];
const catalogGrid={get children(){return domOrder;},appendChild(card){
  const previous=domOrder.indexOf(card);
  assert.notEqual(previous,-1,"Cannot reorder a foreign catalogue card");
  domOrder.splice(previous,1);
  domOrder.push(card);
}};
const filter={value:"all"},origin={value:"all"},author={value:"all"},order={value:"catalog"},search={value:"",focused:false,focus(){this.focused=true;}},status={textContent:""};
const empty={hidden:true},sortStatus={textContent:""},jump={hidden:true,disabled:true};
const pairPrompt={hidden:true},pairLink={href:"",textContent:"",removeAttribute(name){
  assert.equal(name,"href");this.href="";
}};
const share={hidden:false,href:"",textContent:"",removeAttribute(name){
  assert.equal(name,"href");this.href="";
},getAttribute(name){assert.equal(name,"href");return this.href||null;}};
const copyButton={disabled:true,hidden:true}, feedback={textContent:""}, copied=[];
const location={search:"",href:"https://drevendev.github.io/Scriptorium/"};
const browser={location,isSecureContext:true,navigator:{clipboard:{
  async writeText(url){copied.push(url);}
}},history:{replaceState(_state,_title,url){
  location.href=String(url);location.search=new URL(location.href).search;
}}};
const s=js.indexOf("  let catalogCopyAttempt=0;"),e=js.indexOf("  function updateSingle() {",s);
assert.ok(s>=0&&e>s);
const code=js.slice(s,e)+"return {updateCatalog,restoreCatalogFromUrl,resetCatalog,sortCatalog,jumpToFirstCatalogResult,verifiedCatalogShareUrl,copyCatalogShareUrl};";
const make=d=>new Function("data","catalogCards","catalogFilter","catalogOrigin","catalogAuthor","catalogSearch","catalogOrder",
  "catalogGrid","lookup","isNumeric","el","window","catalogCopyButton","catalogJump",code)(
  d,cards,filter,origin,author,search,order,catalogGrid,
  (book,id)=>book.metrics.find(m=>m.id===id),
  value=>typeof value==="number"&&Number.isFinite(value),
  id=>id==="share-catalog"?share:id==="catalog-empty"?empty:
    id==="catalog-sort-status"?sortStatus:id==="catalog-pair-prompt"?pairPrompt:
    id==="catalog-pair-link"?pairLink:id==="copy-catalog-feedback"?feedback:status,
  browser,copyButton,jump);
const {updateCatalog:run,restoreCatalogFromUrl:restore,resetCatalog,sortCatalog,
  jumpToFirstCatalogResult,verifiedCatalogShareUrl,copyCatalogShareUrl}=make(data);
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
// Authorship facet uses exact checked names; names are NOT inferred from tokens.
for(const [name,keys,measured,pending] of [
  ["Лев Толстой",["anna","resurrection"],2,0],
  ["Андрей Белый",["silver","petersburg"],1,1],
  ["Алексей Толстой",["hyperboloid"],1,0],
  ["Жюль Верн",["beketova"],1,0]
]){
  author.value=name;origin.value="all";filter.value="all";search.value="";run();
  assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),keys,name);
  assert.match(status.textContent,new RegExp(measured+" измерено, "+pending+" в подготовке"));
  assert.equal(share.href,"?catalog=all&author="+encodeURIComponent(name)+"#books");
  if(name==="Лев Толстой"){
    assert.equal(pairPrompt.hidden,false,"two measured Tolstoy editions must enable real comparison");
    assert.equal(pairLink.href,
      "?left=anna&right=resurrection&pair_metric=fantlab.dialogue.share_percent#pairs");
    assert.match(pairLink.textContent,/Анна Каренина.*Воскресение/);
  } else {
    assert.equal(pairPrompt.hidden,true,"unmeasured or one-book facet must not offer pair");
    assert.equal(pairLink.href,"","stale actionable pair links must be removed");
  }
}
author.value="Андрей Белый";origin.value="ru";filter.value="measured";run();
assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),["silver"]);
location.search="?catalog=all&author="+encodeURIComponent("Андрей Белый");
restore();assert.equal(author.value,"Андрей Белый");
assert.deepEqual(cards.filter(c=>!c.hidden).map(c=>c.dataset.catalogKey),["silver","petersburg"]);
location.search="?catalog=all&author="+encodeURIComponent("Неизвестный автор");
restore();assert.equal(author.value,"all");
assert.equal(cards.filter(c=>!c.hidden).length,13);
author.value="all";location.search="";
const broken=structuredClone(data);
broken.books.find(book=>book.key==="resurrection").profiles.metrics="incompatible-test-profile";
author.value="Лев Толстой";origin.value="all";filter.value="all";search.value="";
make(broken).updateCatalog();
assert.equal(pairPrompt.hidden,true,"incompatible measured profiles cannot be compared");
assert.equal(pairLink.href,"");
const noMetric=structuredClone(data);
const dialogue=noMetric.books.find(book=>book.key==="resurrection").metrics
  .find(metric=>metric.id==="fantlab.dialogue.share_percent");
dialogue.actual=null;dialogue.status="not_run";
make(noMetric).updateCatalog();
assert.equal(pairPrompt.hidden,true,"missing metric cannot enable a comparison");
assert.equal(pairLink.href,"");
author.value="all";run();
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
// Explicit focus jump follows real filtered/sorted DOM; zero matches disable it.
author.value="Лев Толстой";order.value="author";sortCatalog();run();
assert.equal(jump.hidden,false);assert.equal(jump.disabled,false);
const firstResult=domOrder.find(card=>!card.hidden);
assert.equal(firstResult.dataset.catalogKey,"anna");
jumpToFirstCatalogResult();
assert.equal(firstResult.focused,true);assert.equal(firstResult.tabIndex,-1);
search.value="несуществующая редакция";run();
assert.equal(jump.hidden,true);assert.equal(jump.disabled,true);
const focusedBefore=cards.filter(card=>card.focused).length;
jumpToFirstCatalogResult();
assert.equal(cards.filter(card=>card.focused).length,focusedBefore);
search.value="";author.value="all";order.value="catalog";sortCatalog();run();
// Coverage sorting uses verified observed metric counts, not a guessed quality score.
order.value="coverage";run();sortCatalog();
const expectedCoverage=[...data.books].map((book,i)=>({book,i})).sort((a,b)=>{
  const x=a.book.text_status==="measured"?a.book.measured:null;
  const y=b.book.text_status==="measured"?b.book.measured:null;
  if(x===null)return y===null?a.i-b.i:1;
  if(y===null)return -1;
  return y-x||a.i-b.i;
}).map(x=>x.book.key);
assert.deepEqual(domOrder.map(card=>card.dataset.catalogKey),expectedCoverage);
assert.deepEqual(expectedCoverage.slice(-2),["petersburg","darwin"]);
assert.match(sortStatus.textContent,/числу измеренных полей/);
assert.equal(share.href,"?catalog=all&catalog_order=coverage#books");
location.search="?catalog=measured&catalog_order=coverage";restore();sortCatalog();
assert.equal(order.value,"coverage");
assert.equal(cards.filter(card=>!card.hidden).length,11);
assert.equal(share.href,"?catalog=measured&catalog_order=coverage#books");
order.value="author";run();sortCatalog();
assert.equal(share.href,"?catalog=measured&catalog_order=author#books");
location.search="?catalog=measured&catalog_order=author";restore();sortCatalog();
assert.equal(order.value,"author");
assert.equal(cards.filter(c=>!c.hidden).length,11);
assert.match(sortStatus.textContent,/По имени автора/);
order.value="catalog";filter.value="all";location.search="";sortCatalog();run();
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
assert.equal(search.value,"");assert.equal(filter.value,"all");assert.equal(origin.value,"all");assert.equal(author.value,"all");
assert.equal(cards.filter(c=>!c.hidden).length,13);
assert.equal(search.focused,true);
const clean=new URL(location.href);
assert.equal(clean.searchParams.has("catalog"),false);
assert.equal(clean.searchParams.has("q"),false);
assert.equal(clean.searchParams.has("original"),false);
assert.equal(clean.searchParams.has("author"),false);
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
// Invisible bidi format controls must not become spoofable public share links.
for(const query of ["Верн\u202eРачинский","Верн\u2066Рачинский","Верн\u0085Рачинский","\u061cДефо"]){
 search.value=query;run();assert.equal(share.hidden,true,"unsafe bidi/control query");
 assert.equal(share.href,"","unsafe query must remove the old share href");
}
location.search="?catalog=measured&q="+encodeURIComponent("Верн\u202eРачинский");
restore();assert.equal(search.value,"","unsafe shared query must fail closed");
assert.equal(cards.filter(c=>!c.hidden).length,11,"facets remain valid");
search.value="Шишмарёва";filter.value="translated";run();
assert.equal(share.hidden,false,"normal Cyrillic remains shareable");
assert.ok(share.href.includes(encodeURIComponent("Шишмарёва")));
search.value="";filter.value="all";run();
const tampered=structuredClone(data);tampered.books=tampered.books.filter(b=>b.key!=="darwin");
assert.throws(()=>make(tampered).updateCatalog(),/Нет проверенного источника/);
assert.match(html,/id="catalog-tools" hidden/);
assert.match(html,/id="catalog-empty" class="catalog-empty" hidden/);
assert.match(html,/id="catalog-reset" type="button" disabled/);
assert.match(html,/id="catalog-clear" class="catalog-clear" type="button" disabled/);
assert.match(js,/catalogClear.addEventListener\("click",resetCatalog\)/);
assert.match(js,/catalogReset,catalogClear,one,search,out/);
assert.match(css,/\.catalog-tools \.catalog-clear \{ min-height:44px/);
assert.match(html,/Показано 13 из 13 книг/);
assert.match(js,/catalogReset.addEventListener\("click",resetCatalog\)/);
assert.match(js,/catalogOrder.value="catalog";/);
assert.match(js,/url.searchParams.delete\("catalog_order"\)/);
assert.match(css,/\.catalog-empty\[hidden\]\s*\{\s*display:none\s*!important/);
assert.match(html,/id="catalog-filter" disabled/);
assert.match(html,/id="catalog-origin" aria-describedby="catalog-origin-help" disabled/);
assert.match(html,/id="catalog-origin-help"/);
assert.match(html,/id="catalog-author" aria-describedby="catalog-author-help" disabled/);
assert.match(html,/id="catalog-pair-prompt" class="catalog-pair-prompt" hidden/);
assert.match(html,/id="catalog-pair-link" href="#pairs"/);
assert.match(js,/catalogAuthor.addEventListener\("change",updateCatalog\)/);
assert.match(js,/option\.textContent=name\+" \("/);
assert.match(js,/catalogOrigin.addEventListener\("change",updateCatalog\)/);
assert.match(html,/id="catalog-search" type="search" autocomplete="off"[^>]*disabled/);
assert.match(html,/id="catalog-search"[^>]*maxlength="120"/);
assert.match(html,/id="share-catalog" href="\?catalog=all#books"/);
assert.match(js,/catalogSearch.addEventListener\("input",updateCatalog\)/);
assert.match(js,/catalogOrder.addEventListener\("change",\(\)=>\{sortCatalog\(\);updateCatalog\(\);\}\)/);
assert.match(js,/restoreCatalogFromUrl\(\);\s*sortCatalog\(\);\s*restoreChartFromUrl\(\)/);
const initializeSource=js.slice(js.indexOf("async function initialize() {"));
  const verificationIndex=initializeSource.indexOf("verify(incoming);");
  const assignmentIndex=initializeSource.indexOf("data=incoming;");
  const enableIndex=initializeSource.indexOf("for(const input of inputs)input.disabled=false;");
  assert.ok(verificationIndex>=0 && assignmentIndex>verificationIndex &&
    enableIndex>assignmentIndex,"snapshot must validate before assigning and enabling controls");
  assert.match(initializeSource.slice(verificationIndex,assignmentIndex),
    /catch\s*\(_\)\s*\{[\s\S]*\breturn;\s*\}/,
    "failed verification must exit before snapshot activation");
assert.match(js,/el\("catalog-tools"\)\.hidden=false/);
assert.match(css,/\.catalog-tools\[hidden\],\.book\[hidden\]\s*\{\s*display:none\s*!important/);
assert.match(css,/@media print\s*\{\s*\.catalog-tools\s*\{\s*display:none/);
assert.match(html,/id="copy-catalog-link" hidden disabled/);
assert.match(html,/id="copy-catalog-feedback"[^>]*role="status" aria-live="polite"/);
assert.match(css,/\.catalog-tools \.catalog-share button \{ min-height:44px/);
assert.match(js,/catalogCopyButton.addEventListener\("click",copyCatalogShareUrl\)/);
(async()=>{
  search.value="Шишмарёва";filter.value="translated";origin.value="all";order.value="title";run();
  const expected=new URL(share.href,location.href).href;
  assert.equal(copyButton.disabled,false);
  assert.equal(verifiedCatalogShareUrl(),expected);
  await copyCatalogShareUrl();
  assert.equal(copied.at(-1),expected);
  assert.match(feedback.textContent,/скопирована/);
  const copiedCount=copied.length;
  share.href="https://external.example/unsafe";
  assert.equal(verifiedCatalogShareUrl(),null);
  await copyCatalogShareUrl();
  assert.equal(copied.length,copiedCount);
  assert.match(feedback.textContent,/Нет проверенной ссылки/);
  run();
  browser.isSecureContext=false;
  await copyCatalogShareUrl();
  assert.equal(copied.length,copiedCount);
  assert.match(feedback.textContent,/недоступно/);
  browser.isSecureContext=true;
  browser.navigator.clipboard.writeText=async()=>{throw Error("denied");};
  await copyCatalogShareUrl();
  assert.match(feedback.textContent,/Не удалось/);
  let resolveWrite;
  browser.navigator.clipboard.writeText=()=>new Promise(resolve=>{resolveWrite=resolve;});
  const pendingCopy=copyCatalogShareUrl();
  search.value="Верн";run();
  resolveWrite();
  await pendingCopy;
  assert.equal(feedback.textContent,"");
  search.value="Верн\u202e";run();
  assert.equal(copyButton.disabled,true);
  assert.equal(verifiedCatalogShareUrl(),null);
  console.log("Verified catalogue filters, reset, safe clipboard success/denial, stale results and no-JS fallback: PASS");
})().catch(error=>{console.error(error);process.exitCode=1;});
