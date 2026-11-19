"""Russian Reader catalogue filters retain measured/pending and translation identity."""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class CatalogueFilterTests(unittest.TestCase):
    def test_catalogue_static_and_evidence_identity(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        data=json.loads((ROOT/"assets/evidence-snapshot.json").read_text(encoding="utf-8"))
        cards=re.findall(r'<article class="book(?: book-research)?" data-status="(measured|pending)" data-catalog-key="([a-z]+)">',html)
        self.assertEqual([key for _,key in cards],[book["key"] for book in data["books"]])
        self.assertEqual([kind for kind,_ in cards],["measured"]*11+["pending"]*2)
        self.assertEqual(sum(book["language"]!=book["original_language"] for book in data["books"]),3)
        self.assertIn('id="catalog-tools" hidden',html)
        self.assertIn('id="catalog-empty" class="catalog-empty" hidden',html)
        self.assertIn('id="catalog-reset" type="button" disabled',html)
        self.assertIn('id="catalog-clear" class="catalog-clear" type="button" disabled',html)
        self.assertIn('id="catalog-jump" class="catalog-jump" type="button" hidden disabled',html)
        self.assertIn("Показано 13 из 13 книг.",html)
        self.assertIn('id="catalog-filter" disabled',html)
        self.assertIn('id="catalog-order" disabled',html)
        self.assertIn('id="catalog-metric" aria-describedby="catalog-metric-help" disabled',html)
        self.assertIn('id="catalog-author" aria-describedby="catalog-author-help" disabled',html)
        self.assertIn('id="catalog-pair-prompt" class="catalog-pair-prompt" hidden',html)
        self.assertIn('id="catalog-pair-link" href="#pairs"',html)
        self.assertIn('id="catalog-sort-status" role="status" aria-live="polite"',html)
        self.assertIn('id="catalog-search" type="search" autocomplete="off"',html)
        self.assertIn('aria-describedby="catalog-shortcut-help"',html)
        self.assertIn('Нажмите <kbd>/</kbd>',html)
        self.assertIn('placeholder="Например, Верн Бекетова" aria-describedby="catalog-shortcut-help" disabled',html)
        self.assertIn('maxlength="120"',html)
        self.assertIn('id="share-catalog" href="?catalog=all#books"',html)
        self.assertIn('id="catalog-filter-status" role="status" aria-live="polite"',html)
        self.assertIn('id="catalog-metric-range" class="catalog-metric-range" hidden',html)
        self.assertIn('id="catalog-chart-action" class="catalog-chart-action" hidden',html)
        self.assertIn('id="catalog-chart-link" href="#charts"',html)
        self.assertIn('<option value="metric_desc" disabled>',html)
        self.assertIn('<option value="metric_asc" disabled>',html)
        css=(ROOT/"assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn(".book[hidden] { display:none !important; }",css)
        self.assertIn(".book .book-compare",css)
        self.assertIn(".catalog-tools .catalog-metric-range[hidden]",css)
        self.assertIn(".catalog-tools .catalog-chart-action[hidden]",css)
        self.assertIn(".catalog-chart-action a:focus-visible",css)
        self.assertIn("@media print { .catalog-tools { display:none !important; } }",css)
        js=(ROOT/"assets/pages-reader.js").read_text(encoding="utf-8")
        self.assertIn('observedMedian(observedMetricValues)',js)
        self.assertIn('chartAction.hidden=observedMetricValues.length===0',js)
        self.assertIn('"&metric="+encodeURIComponent(availableMetric)+"#charts"',js)
        self.assertIn('Медиана: непроверенные наблюдения',js)
        self.assertIn('matchingMeasured.length===2',js)
        self.assertIn('pairPrompt.hidden=!pairReady;',js)
        self.assertIn("installCatalogComparisonActions();",js)
        self.assertIn('document.addEventListener("keydown",handleCatalogSearchKeys);',js)
        self.assertIn('target.closest("input, textarea, select, [contenteditable]")',js)
        self.assertIn("doc.books.some(book=>{",js)
        self.assertIn('catalogSearch.addEventListener("input",updateCatalog)',js)
        self.assertIn('catalogAuthor.addEventListener("change",updateCatalog)',js)
        self.assertIn('catalogMetric.addEventListener("change",()=>{sortCatalog();updateCatalog();})',js)
        self.assertIn('url.searchParams.delete("available_metric")',js)
        self.assertIn('url.searchParams.delete("author")',js)
        self.assertIn('allowedCatalogAuthor(requestedAuthor)',js)
        self.assertIn('catalogOrder.addEventListener("change",()=>{sortCatalog();updateCatalog();})',js)
        self.assertIn('catalogReset.addEventListener("click",resetCatalog)',js)
        self.assertIn('catalogClear.addEventListener("click",resetCatalog)',js)
        self.assertIn("catalogReset,catalogClear,catalogJump,one,search,out",js)
        self.assertIn('catalogJump.addEventListener("click",jumpToFirstCatalogResult)',js)
        self.assertIn("card.tabIndex=-1;",js)
        self.assertIn(".book:focus-visible",css)
        self.assertIn('el("catalog-empty").hidden=shown!==0;',js)
        self.assertIn('url.searchParams.delete("catalog")',js)
        self.assertIn('url.searchParams.delete("q")',js)
        self.assertIn('url.searchParams.delete("catalog_order")',js)
        self.assertIn('catalogOrder.value="catalog";',js)
        self.assertIn(".catalog-empty[hidden] { display:none !important; }",css)
        self.assertIn('book.translator?.name||""',js)
        self.assertIn('terms.every(term=>text.includes(term))',js)
        self.assertIn(".catalog-tools select,.catalog-tools input",css)
        restore=js.split("  function restoreCatalogFromUrl() {",1)[1].split("\n  }",1)[0]
        self.assertRegex(restore,r"sortCatalog\(\);\s*updateCatalog\(\);")
        self.assertIn('restoreCatalogFromUrl();\n      el("catalog-tools").hidden=false;',js)
        self.assertIn('window.addEventListener("popstate",()=>{\n        restoreCatalogFromUrl();',js)
        # Canonical URL building is shared by the visible link and the
        # verified clipboard action; preserve all five allow-listed facets.
        self.assertIn('share.href=catalogShareHref(mode,origin,raw,order,author,availableMetric);',js)
        self.assertIn('function catalogShareHref(mode,origin,raw,order,author="all",availableMetric="all")',js)
        self.assertIn('return "?catalog="+encodeURIComponent(mode)+',js)
        self.assertIn('copyCatalogShareUrl',js)
        self.assertIn('verifiedCatalogShareUrl',js)
        self.assertIn('safeCatalogQuery(raw)',js)
        self.assertNotIn("innerHTML",js)

    @unittest.skipUnless(shutil.which("node"),"Node unavailable; structural checks still run")
    def test_real_js_behavior(self):
        for command in (["node","--check",str(ROOT/"assets/pages-reader.js")],
                        ["node",str(ROOT/"tests/pages_catalog_filter_smoke.cjs")],
                        ["node",str(ROOT/"tests/pages_catalog_sort_smoke.cjs")],
                        ["node",str(ROOT/"tests/pages_catalog_compare_smoke.cjs")],
                        ["node",str(ROOT/"tests/pages_catalog_keyboard_shortcut_smoke.cjs")]):
            result=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,check=False)
            self.assertEqual(result.returncode,0,result.stdout+"\n"+result.stderr)

if __name__=="__main__":
    unittest.main()
