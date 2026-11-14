/* Real Reader keyboard shortcut implementation, including safety negatives. */
"use strict";
const assert=require("node:assert/strict"), fs=require("node:fs"), path=require("node:path");
const root=path.resolve(__dirname,"..");
const js=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const begin=js.indexOf("  function handleCatalogSearchKeys(event) {");
const end=js.indexOf("  function safeCatalogQuery(raw) {",begin);
assert.ok(begin>=0 && end>begin,"Run the actual Reader shortcut function");
assert.match(js.slice(js.indexOf("async function initialize()")),/verify\(incoming\); data=incoming;[\s\S]*document\.addEventListener\("keydown",handleCatalogSearchKeys\);/);
assert.match(html,/id="catalog-search"[^>]*aria-describedby="catalog-shortcut-help" disabled/);
assert.match(html,/id="catalog-shortcut-help"[^>]*>Нажмите <kbd>\/</kbd>/);
assert.doesNotMatch(js.slice(begin,end),/fetch\(|localStorage|sendBeacon|innerHTML/);
let focuses=0, updates=0;
const search={disabled:false,value:"",focus(){focuses++;},closest(){return this;}};
const handle=new Function("catalogSearch","updateCatalog",js.slice(begin,end)+
  "return handleCatalogSearchKeys;")(search,()=>{updates++;});
const neutral={closest(){return null;}};
function send(key="/", options={}) {
  const event={key,target:neutral,defaultPrevented:false,isComposing:false,
    ctrlKey:false,altKey:false,metaKey:false,shiftKey:false,
    preventDefault(){this.defaultPrevented=true;}};
  Object.assign(event,options);
  handle(event);return event;
}
assert.equal(send().defaultPrevented,true);
assert.equal(focuses,1,"Slash focuses verified catalogue search");
for(const options of [
  {key:"a"},{defaultPrevented:true},{isComposing:true},
  {ctrlKey:true},{altKey:true},{metaKey:true},{shiftKey:true},
  {target:search},
  {target:{closest(){return {};}}},
  {target:{closest(){return {};},isContentEditable:true}},
]){
  const before=focuses;
  const {key,...rest}=options;
  const event=send(key??"/",rest);
  assert.equal(focuses,before,"Do not steal typing or modifier/composition keys");
  if(!options.defaultPrevented)assert.equal(event.defaultPrevented,false);
}
search.value="Дефо";
let ev=send("Escape",{target:neutral});
assert.equal(ev.defaultPrevented,false);
assert.equal(search.value,"Дефо");
ev=send("Escape",{target:search});
assert.equal(ev.defaultPrevented,true);
assert.equal(search.value,"");
assert.equal(updates,1,"Escape reruns the real catalogue filter and status update");
ev=send("Escape",{target:search});
assert.equal(ev.defaultPrevented,false);
assert.equal(updates,1,"Empty search leaves Escape to the browser");
search.disabled=true;
ev=send();
assert.equal(ev.defaultPrevented,false);
ev=send("Escape",{target:search});
assert.equal(ev.defaultPrevented,false);
assert.equal(focuses,1);
assert.equal(updates,1);
console.log("Reader verified / focus, Esc clear, editable/IME/modifier and disabled negatives: PASS");
