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
        self.assertEqual([kind for kind,_ in cards],["measured"]*7+["pending"]*3)
        self.assertEqual(sum(book["language"]!=book["original_language"] for book in data["books"]),2)
        self.assertIn('id="catalog-tools" hidden',html)
        self.assertIn('id="catalog-filter" disabled',html)
        self.assertIn('id="catalog-search" type="search" autocomplete="off"',html)
        self.assertIn('placeholder="Например, Бекетова" disabled',html)
        self.assertIn('maxlength="120"',html)
        self.assertIn('id="share-catalog" href="?catalog=all#books"',html)
        self.assertIn('id="catalog-filter-status" role="status" aria-live="polite"',html)
        css=(ROOT/"assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn(".book[hidden] { display:none !important; }",css)
        self.assertIn("@media print { .catalog-tools { display:none !important; } }",css)
        js=(ROOT/"assets/pages-reader.js").read_text(encoding="utf-8")
        self.assertIn("doc.books.some(book=>{",js)
        self.assertIn('catalogSearch.addEventListener("input",updateCatalog)',js)
        self.assertIn('book.translator?.name||""',js)
        self.assertIn(".catalog-tools select,.catalog-tools input",css)
        self.assertIn('restoreCatalogFromUrl();\n      el("catalog-tools").hidden=false;',js)
        self.assertIn('window.addEventListener("popstate",()=>{\n        restoreCatalogFromUrl();',js)
        self.assertIn('share.href="?catalog="',js)
        self.assertIn('safeCatalogQuery(raw)',js)
        self.assertNotIn("innerHTML",js)

    @unittest.skipUnless(shutil.which("node"),"Node unavailable; structural checks still run")
    def test_real_js_behavior(self):
        for command in (["node","--check",str(ROOT/"assets/pages-reader.js")],
                        ["node",str(ROOT/"tests/pages_catalog_filter_smoke.cjs")]):
            result=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,check=False)
            self.assertEqual(result.returncode,0,result.stdout+"\n"+result.stderr)

if __name__=="__main__":
    unittest.main()
