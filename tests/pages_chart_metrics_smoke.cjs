/* Exercise shipped chart code, with the real pinned seven-book evidence JSON. */
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
assert.equal(measured.length,7);
const node=tag=>({tag,children:[],style:{},attrs:{},className:"",textContent:"",appendChild(n){this.children.push(n);return n;},setAttribute(k,v){this.attrs[k]=v;},replaceChildren(f){this.children=f.children;}});
const elements={"chart-series":node("div"),"chart-unit":node("p"),"chart-table-rows":node("tbody"),"chart-table-caption":node("caption")};
const document={createElement:node,createDocumentFragment:()=>node("fragment")};
const insertText=(parent,tag,v,cls)=>{const n=node(tag);n.textContent=v;if(cls)n.className=cls;parent.appendChild(n);return n;};
const buttons=ids.map(id=>({dataset:{chart:id},attrs:{},setAttribute(k,v){this.attrs[k]=v;}}));
const action=new Function("data","metrics","currentChart","lookup","isNumeric","document","el","insertText","pretty","chartButtons",source.slice(start,end)+"return updateChart();");
const render=(id,data=catalog)=>action(data,metrics,id,(book,key)=>book.metrics.find(row=>row.id===key),n=>typeof n==="number"&&Number.isFinite(n),document,key=>elements[key],insertText,(n,p)=>new Intl.NumberFormat("ru-RU",{maximumFractionDigits:p}).format(n),buttons);
for(const id of ids){
  render(id);
  const rows=elements["chart-series"].children;
  assert.equal(rows.length,7,id);
  const tab=elements["chart-table-rows"].children;
  assert.equal(tab.length,7,id);
  assert.ok(elements["chart-table-caption"].textContent.includes("из 7"),id);
  for(let i=0;i<7;i++){
    assert.equal(tab[i].children[0].tag,"th",id);
    assert.equal(tab[i].children[0].textContent,measured[i].display_title,id);
    assert.equal(tab[i].children[2].textContent,metrics[id][1],id);
    const field=measured[i].metrics.find(m=>m.id===id);
    assert.equal(tab[i].children[1].textContent,field&&Number.isFinite(field.actual)?String(field.actual):"нет данных",id);
  }
  const expected=measured.filter(book=>book.metrics.some(m=>m.id===id&&Number.isFinite(m.actual))).length;
  assert.equal(expected,id.includes("mean_dialogue_sentence")||id.includes("mean_narration_sentence")?6:7,id);
  assert.ok(elements["chart-unit"].textContent.includes(expected+" из 7"),id);
  assert.equal(buttons.filter(btn=>btn.attrs["aria-pressed"]==="true").length,1,id);
  const missing=rows.filter(row=>row.className.includes("chart-missing"));
  assert.equal(missing.length,7-expected,id);
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
console.log("Eight real charts and exact-value accessible tables: measured/missing/zero PASS");
