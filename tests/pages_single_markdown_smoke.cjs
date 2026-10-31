/* Exercise shipped one-edition Markdown export on all ten pinned source-free books. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const catalog=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
function section(start,end) {
  const a=source.indexOf(start),b=source.indexOf(end,a+start.length);
  assert.ok(a>=0&&b>a,"Missing shipped code: "+start);
  return source.slice(a,b);
}
const shared=section("  function markdownCell(value) {","  function serializePairMarkdown(");
const deltas=section("  function diagnosticDelta(m) {","  function makeTableRow(m) {");
const feature=section("  function serializeBookMarkdown(book) {",
                      "  // Print the selected metric's exact, source-backed table");
const getBook=key=>catalog.books.find(b=>b.key===key&&b.text_status==="measured");
const isNumeric=n=>typeof n==="number"&&Number.isFinite(n);
const pretty=(n,places=2)=>new Intl.NumberFormat("ru-RU",{maximumFractionDigits:places}).format(n);
const unit=id=>id.endsWith("_percent")?"%":"измеренная единица";
const label=id=>id;
const button={disabled:false};
let clicked=0,filename="",downloadBlob,verified=0;
const browserUrl={createObjectURL(blob){downloadBlob=blob;return "blob:single"},revokeObjectURL(){}};
const browserDocument={
  createElement(tag){
    assert.equal(tag,"a");
    return {set href(v){assert.equal(v,"blob:single")},
            set download(v){filename=v},click(){clicked++},remove(){}};
  },
  body:{appendChild(){}}
};
const actions=new Function("data","getBook","currentBook","singleMarkdownButton",
  "isNumeric","label","unit","pretty","verify","URL","document","setTimeout",
  deltas+shared+feature+"\nreturn {serializeBookMarkdown,exportSelectedMarkdown};"
)(catalog,getBook,"anna",button,isNumeric,label,unit,pretty,doc=>{
  assert.equal(doc,catalog); verified++;
},browserUrl,browserDocument,()=>{});
const measured=catalog.books.filter(book=>book.text_status==="measured");
assert.equal(measured.length,10);
let fields=0;
for(const book of measured) {
  const text=actions.serializeBookMarkdown(book);
  const rows=text.split("\n").filter(row=>/^\| (fantlab|scriptorium)\./.test(row));
  assert.equal(rows.length,book.metrics.length,book.key);
  assert.ok(text.includes(book.source_sha256),book.key);
  assert.match(text,/DIAGNOSTIC_ONLY[\s\S]*UNKNOWN[\s\S]*M2: 0\/5/);
  assert.ok(!text.includes("undefined"),book.key);
  assert.equal(actions.serializeBookMarkdown(book),text);
  fields+=rows.length;
}
assert.equal(fields,269);
const anna=getBook("anna"),beketova=getBook("beketova");
const translated=actions.serializeBookMarkdown(beketova);
assert.ok(translated.includes(beketova.translator.name));
assert.ok(translated.includes(beketova.translator.id));
assert.match(translated,/UNKNOWN/);
assert.match(translated,/^\| .* \| NOT_RUN \|/m.test(translated)
  ? /NOT_RUN/ : /DIAGNOSTIC_ONLY/);
const injection=actions.serializeBookMarkdown({...anna,display_title:"Danger | *bold* <script> [link]"});
assert.ok(injection.includes("Danger \\| \\*bold\\* &lt;script&gt; \\[link\\]"));
assert.ok(!injection.includes("Danger | *bold* <script> [link]"));
const zero=actions.serializeBookMarkdown({...anna,metrics:anna.metrics.map((m,i)=>
  i===0?{...m,actual:0,status:"measured"}:m)});
assert.match(zero,/^\| fantlab\.[^|]+ \| fantlab\.[^|]+ \| 0 \|/m);
const failures=[
  {...anna,source_sha256:"invalid"},
  {...anna,metrics:[...anna.metrics,{...anna.metrics[0]}]},
  {...anna,metrics:anna.metrics.map((m,i)=>i?m:{...m,actual:null,status:"measured"})},
  {...beketova,translator:null},
  {...anna,text_status:"pending"},
  {...anna,metrics:anna.metrics.map((m,i)=>i?m:{...m,actual:Infinity})}
];
for(const bad of failures) assert.throws(()=>actions.serializeBookMarkdown(bad));
(async()=>{
  actions.exportSelectedMarkdown();
  assert.equal(verified,1);
  assert.equal(clicked,1);
  assert.equal(filename,"scriptorium-anna-derived.md");
  assert.equal(await downloadBlob.text(),actions.serializeBookMarkdown(anna));
  const pending=new Function("data","getBook","currentBook","singleMarkdownButton",
    "isNumeric","label","unit","pretty","verify","URL","document","setTimeout",
    deltas+shared+feature+"\nreturn {exportSelectedMarkdown};"
  )(catalog,getBook,"petersburg",button,isNumeric,label,unit,pretty,doc=>assert.equal(doc,catalog),
    browserUrl,browserDocument,()=>{});
  pending.exportSelectedMarkdown();
  assert.equal(button.disabled,true);
  assert.equal(clicked,1);
  console.log("Root Pages book Markdown: 10 books / 269 fields, source identity, safe download, six negatives PASS");
})().catch(e=>{console.error(e);process.exitCode=1});
