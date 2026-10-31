/* Run shipped root Reader paired-edition captions against pinned data. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const catalog=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const start=source.indexOf("  function pairEditionDescription(book, side) {");
const end=source.indexOf("  function updatePair() {",start);
assert(start>=0&&end>start,"Shipped edition-context code is missing");
const slots=Object.fromEntries(["pair-left-edition","pair-right-edition","pair-edition-caveat"]
  .map(id=>[id,{textContent:""}]));
const {pairEditionDescription,updatePairEditionContext}=new Function("el",
  source.slice(start,end)+"\nreturn {pairEditionDescription,updatePairEditionContext};"
)(id=>{assert.ok(Object.hasOwn(slots,id));return slots[id];});
const getBook=id=>catalog.books.find(b=>b.key===id);
const anna=getBook("anna"),kara=getBook("karamazov"),bek=getBook("beketova");
updatePairEditionContext(anna,kara);
assert.match(slots["pair-left-edition"].textContent,/Анна Каренина.*русский оригинал/);
assert.match(slots["pair-right-edition"].textContent,/Братья Карамазовы.*русский оригинал/);
assert.match(slots["pair-left-edition"].textContent,new RegExp(anna.source_sha256.slice(0,12)));
assert.match(slots["pair-edition-caveat"].textContent,/не доказывает/);
updatePairEditionContext(anna,bek);
assert.match(slots["pair-right-edition"].textContent,/перевод с французского/);
assert.match(slots["pair-right-edition"].textContent,/Александра Андреевна Бекетова/);
assert.match(slots["pair-right-edition"].textContent,/ru-beketova-wikisource-oldid-5304880/);
assert.match(slots["pair-right-edition"].textContent,new RegExp(bek.source_sha256.slice(0,12)));
assert.match(slots["pair-edition-caveat"].textContent,/НЕ французский\/английский оригинал/);
updatePairEditionContext(bek,anna);
assert.match(slots["pair-left-edition"].textContent,/перевод с французского/);
assert.match(slots["pair-right-edition"].textContent,/русский оригинал/);
const fake={...anna,display_title:"<img src=x onerror=alert(1)>"};
updatePairEditionContext(fake,kara);
assert.ok(slots["pair-left-edition"].textContent.includes(fake.display_title));
assert.ok(!source.slice(start,end).includes("innerHTML"));
assert.equal(pairEditionDescription(bek,"Справа"),slots["pairEditionDescription"]?.textContent||pairEditionDescription(bek,"Справа"));
console.log("Root Reader paired edition, translation and text-only negative cases PASS");
