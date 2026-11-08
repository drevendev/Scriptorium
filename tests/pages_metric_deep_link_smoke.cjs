/* Root Reader metric definitions: all canonical entries remain linkable and safe. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path");
const root=path.resolve(__dirname,"..");
const guide=fs.readFileSync(path.join(root,"metrics.html"),"utf8");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const ids=[...guide.matchAll(/<tr id="metric-([^"]+)">/g)].map(m=>m[1]);
assert.equal(ids.length,29,"Exactly 29 individual definitions");
assert.equal(new Set(ids).size,29,"No duplicate definition targets");
const found=source.match(/  function appendMetricDefinition\(parent,id,shown=label\(id\)\) \{[\s\S]*?\n  \}/);
assert.ok(found,"Actual Reader helper must exist");
assert.doesNotMatch(found[0],/innerHTML|outerHTML|document\.write/);
const created=[];
const document={createElement(tag){assert.equal(tag,"a");const el={attrs:{},setAttribute(name,value){this.attrs[name]=value;}};created.push(el);return el;}};
const label=id=>"Показатель "+id;
const make=new Function("document","label",found[0]+"\nreturn appendMetricDefinition;")(document,label);
for(const id of ids){
  const parent={children:[],appendChild(node){this.children.push(node);}};
  const link=make(parent,id);
  assert.equal(parent.children.length,1);
  assert.equal(link.href,"./metrics.html#metric-"+encodeURIComponent(id));
  assert.equal(link.textContent,label(id));
  assert.equal(link.className,"metric-definition-link");
  assert.equal(link.attrs["aria-label"],"Методика показателя: "+label(id));
  assert.ok(guide.includes('id="metric-'+id+'"'),"Missing actual guide target: "+id);
}
const malicious='fantlab.general.words" onclick="alert(1)';
const parent={appendChild(){}};
const suspicious=make(parent,malicious);
assert.ok(suspicious.href.includes("%22"));
assert.ok(!suspicious.href.includes('"'));
assert.ok(suspicious.href.startsWith("./metrics.html#metric-"));
assert.equal((source.match(/appendMetricDefinition\(th,m\.id\);/g)||[]).length,2,
  "Both single-book and paired rows must expose links");
assert.match(source,/appendMetricDefinition\(metricTitle,curr\.id,"Как считается ↗"\);/);
assert.equal((html.match(/href="\.\/metrics\.html">Откройте определения всех 29 показателей/g)||[]).length,2,
  "Both no-script fallback tables need a plain guide entry point");
console.log("Metric definitions: 29 canonical targets, interactive rows, safe encoded fragments and static fallback PASS");
