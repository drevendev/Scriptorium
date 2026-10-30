/* Exercise shipped chart code, with the real pinned ten-book evidence JSON. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const source=fs.readFileSync(path.join(root,"assets/pages-reader.js"),"utf8");
const catalog=JSON.parse(fs.readFileSync(path.join(root,"assets/evidence-snapshot.json"),"utf8"));
const start=source.indexOf("  function updateChart() {");
const end=source.indexOf("  const pairedIds =",start);
assert.ok(start>=0&&end>start,"Shipped chart function not found");
const metrics=new Function(source.slice(source.indexOf("  const metrics ="),source.indexOf("  const names ="))+"return metrics;")();
const ids=Object.keys(metrics);
assert.equal(ids.length,8);
const measured=catalog.books.filter(b=>b.text_status==="measured");
assert.equal(measured.length,10);
const node=tag=>({tag,children:[],style:{},attrs:{},className:"",textContent:"",appendChild(n){this.children.push(n);return n;},setAttribute(k,v){this.attrs[k]=v;},replaceChildren(f){this.children=f.children;}});
const elements={"chart-series":node("div"),"chart-unit":node("p"),"chart-table-rows":node("tbody"),"chart-table-caption":node("caption")};
const chartSortButton=node("button");
const document={createElement:node,createDocumentFragment:()=>node("fragment")};
const insertText=(parent,tag,v,cls)=>{const n=node(tag);n.textContent=v;if(cls)n.className=cls;parent.appendChild(n);return n;};
const buttons=ids.map(id=>({dataset:{chart:id},attrs:{},setAttribute(k,v){this.attrs[k]=v;}}));
const action=new Function("data","metrics","currentChart","lookup","isNumeric","document","el","insertText","pretty","chartButtons","exact","sortChart","chartSortButton",source.slice(start,end)+"return updateChart();");
const render=(id,data=catalog,sorted=false)=>action(data,metrics,id,(book,key)=>book.metrics.find(row=>row.id===key),n=>typeof n==="number"&&Number.isFinite(n),document,key=>elements[key],insertText,(n,p)=>new Intl.NumberFormat("ru-RU",{maximumFractionDigits:p}).format(n),buttons,n=>n===null?"UNKNOWN":String(n),sorted,chartSortButton);
for(const id of ids){
  render(id);
  const rows=elements["chart-series"].children;
  assert.equal(rows.length,10,id);
  const tab=elements["chart-table-rows"].children;
  assert.equal(tab.length,10,id);
  assert.ok(elements["chart-table-caption"].textContent.includes("из 10"),id);
  for(let i=0;i<10;i++){
    assert.equal(tab[i].children[0].tag,"th",id);
    assert.equal(tab[i].children[0].textContent,measured[i].display_title,id);
    assert.equal(tab[i].children[2].textContent,metrics[id][1],id);
    const field=measured[i].metrics.find(m=>m.id===id);
    assert.equal(tab[i].children[1].textContent,field&&Number.isFinite(field.actual)?String(field.actual):"нет данных",id);
  }
  const expected=measured.filter(book=>book.metrics.some(m=>m.id===id&&Number.isFinite(m.actual))).length;
  assert.equal(expected,id.includes("mean_dialogue_sentence")||id.includes("mean_narration_sentence")?9:10,id);
  assert.ok(elements["chart-unit"].textContent.includes(expected+" из 10"),id);
  assert.equal(buttons.filter(btn=>btn.attrs["aria-pressed"]==="true").length,1,id);
  const missing=rows.filter(row=>row.className.includes("chart-missing"));
  assert.equal(missing.length,10-expected,id);
  for(const row of missing){assert.equal(row.children[2].textContent,"нет данных");assert.equal(row.children[1].children.length,0);}
}
render("fantlab.dialogue.mean_dialogue_sentence_length_chars");
assert.equal(elements["chart-series"].children[5].children[2].textContent,"нет данных");
assert.equal(elements["chart-table-rows"].children[5].children[1].textContent,"нет данных");
render("fantlab.dialogue.share_percent");
assert.equal(elements["chart-series"].children[5].children[2].textContent,"32,47%");
assert.throws(()=>render("fantlab.unregistered"),/Показатель диаграммы не разрешён/);
const changed=structuredClone(catalog);
changed.books.find(b=>b.key==="anna").metrics.find(m=>m.id==="fantlab.dialogue.share_percent").actual=0;
render("fantlab.dialogue.share_percent",changed);
assert.equal(elements["chart-series"].children[0].children[2].textContent,"0%");
assert.equal(elements["chart-table-rows"].children[0].children[1].textContent,"0");
assert.equal(elements["chart-series"].children[0].children[1].children[0].style.width,"0.00%");
assert.ok(!elements["chart-series"].children[0].className.includes("chart-missing"));
// Regression: the rendered graph and accessible table must share stable order.
render("fantlab.dialogue.share_percent",catalog,true);
const ranked=measured.map((b,i)=>({title:b.display_title,value:b.metrics.find(m=>m.id==="fantlab.dialogue.share_percent").actual,i})).sort((a,b)=>b.value-a.value||a.i-b.i);
assert.deepEqual(elements["chart-series"].children.map(r=>r.children[0].textContent),ranked.map(r=>r.title));
assert.deepEqual(elements["chart-table-rows"].children.map(r=>r.children[0].textContent),ranked.map(r=>r.title));
assert.equal(chartSortButton.attrs["aria-pressed"],"true");
render("fantlab.dialogue.mean_dialogue_sentence_length_chars",catalog,true);
assert.equal(elements["chart-series"].children.at(-1).children[0].textContent,"Дети капитана Гранта");
assert.equal(elements["chart-series"].children.at(-1).children[2].textContent,"нет данных");
const zeroSorted=structuredClone(catalog);
zeroSorted.books.find(b=>b.key==="anna").metrics.find(m=>m.id==="fantlab.dialogue.share_percent").actual=0;
render("fantlab.dialogue.share_percent",zeroSorted,true);
assert.equal(elements["chart-series"].children.at(-1).children[0].textContent,"Анна Каренина");
assert.equal(elements["chart-series"].children.at(-1).children[2].textContent,"0%");
render("fantlab.dialogue.share_percent",catalog,false);
assert.deepEqual(elements["chart-series"].children.map(r=>r.children[0].textContent),measured.map(b=>b.display_title));
assert.equal(chartSortButton.attrs["aria-pressed"],"false");
console.log("Chart ranking: descending, missing-last, true-zero and reset PASS");
// Execute the shipped print lifecycle, not a separately rewritten algorithm.
const printStart=source.indexOf("  // Print the selected metric's exact, source-backed table");
const printEnd=source.indexOf("  async function initialize()",printStart);
assert.ok(printStart>=0&&printEnd>printStart,"Print lifecycle missing from shipped JS");
const printCode=source.slice(printStart,printEnd);
function printHarness(open,includeTable=true){
  const table=includeTable?{open}:null;
  const events={};
  new Function("document","window",printCode)(
    {querySelector:selector=>{assert.equal(selector,".chart-table");return table;}},
    {addEventListener:(type,callback)=>{events[type]=callback;}}
  );
  assert.equal(typeof events.beforeprint,"function");
  assert.equal(typeof events.afterprint,"function");
  return {table,events};
}
for(const initiallyOpen of [false,true]){
  const {table,events}=printHarness(initiallyOpen);
  events.afterprint(); // No prior preview must be harmless.
  assert.equal(table.open,initiallyOpen);
  events.beforeprint();
  assert.equal(table.open,true,"Exact data must be printable");
  events.beforeprint(); // Some browsers dispatch beforeprint more than once.
  events.afterprint();
  assert.equal(table.open,initiallyOpen,"Disclosure state must be restored");
  events.afterprint();
  assert.equal(table.open,initiallyOpen);
}
const absent=printHarness(false,false);
absent.events.beforeprint();
absent.events.afterprint(); // Missing table cannot break the rest of Reader.
const printCss=fs.readFileSync(path.join(root,"assets/pages-reader.css"),"utf8");
assert.match(printCss,/\.chart-table td:nth-child\(2\).*overflow-wrap:anywhere/);
assert.match(printCss,/@media print \{[\s\S]*\.chart-table summary \{ display:none; \}/);
console.log("Print preview opens the exact chart table and restores disclosure state: PASS");
console.log("Ten-book real charts and exact-value accessible tables: measured/missing/zero PASS");

/* Exercise chart URL selection against shipped code and real Node URL handling. */
const linkStart=source.indexOf("  // Share an allow-listed chart");
const linkEnd=source.indexOf("  const pairedIds =",linkStart);
assert.ok(linkStart>0&&linkEnd>linkStart);
const chartLinkCode=source.slice(linkStart,linkEnd);
const fallbackChart="fantlab.dialogue.share_percent";
function chartLinkHarness(query){
  const anchor={href:"",textContent:""};
  const win={location:new URL("https://drevendev.github.io/Scriptorium/?book=beketova&left=anna&right=waves"+(query?"&metric="+encodeURIComponent(query):"")+"#books")};
  win.history={pushState(_a,_b,url){win.location=new URL(String(url));}};
  let renders=0;
  const ctl=new Function("window","metrics","el","updateChart",
    "let currentChart='fantlab.dialogue.share_percent';\n"+chartLinkCode+
    "return {chartFromUrl,selectChart,current:()=>currentChart};")(
      win,metrics,id=>{assert.equal(id,"share-chart");return anchor;},()=>renders++);
  return {win,anchor,ctl,renders:()=>renders};
}
for(const id of ids){
  const h=chartLinkHarness(id);
  assert.equal(h.ctl.chartFromUrl(),id);
  h.ctl.selectChart(h.ctl.chartFromUrl());
  assert.equal(h.ctl.current(),id);
  assert.equal(h.anchor.href,"?metric="+encodeURIComponent(id)+"#charts");
  assert.ok(h.anchor.textContent.includes(metrics[id][0]));
  assert.equal(h.renders(),1);
  h.ctl.selectChart(fallbackChart,true);
  assert.equal(h.win.location.searchParams.get("metric"),fallbackChart);
  assert.equal(h.win.location.searchParams.get("book"),"beketova");
  assert.equal(h.win.location.searchParams.get("left"),"anna");
  assert.equal(h.win.location.hash,"#charts");
  h.win.location=new URL("https://drevendev.github.io/Scriptorium/?metric="+encodeURIComponent(id)+"#charts");
  h.ctl.selectChart(h.ctl.chartFromUrl());
  assert.equal(h.ctl.current(),id,"Back/Forward metric restoration");
}
for(const invalid of [null,"does.not.exist","__proto__","constructor","toString"]){
  const h=chartLinkHarness(invalid);
  assert.equal(h.ctl.chartFromUrl(),fallbackChart);
  h.ctl.selectChart(h.ctl.chartFromUrl());
  assert.equal(h.anchor.href,"?metric="+fallbackChart+"#charts");
  const n=h.renders();
  h.ctl.selectChart(invalid);
  assert.equal(h.renders(),n,"invalid metric must not render");
}
const siteHtml=fs.readFileSync(path.join(root,"index.html"),"utf8");
assert.match(siteHtml,/id="charts" aria-labelledby="chart-title"/);
assert.match(siteHtml,/id="share-chart" href="\?metric=fantlab\.dialogue\.share_percent#charts"/);
assert.match(siteHtml,/id="chart-table-rows"/);
console.log("Eight source-backed chart permalinks, URL fallback and history: PASS");
