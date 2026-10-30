"""Root Pages comparison deep links preserve source and identity constraints."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
import json
import shutil
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links=[]
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        if tag=="a":
            self.links.append(dict(attrs))

class PairLinks(unittest.TestCase):
    def test_share_link_measured_pair_and_keyboard(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        links=Links(html).links
        self.assertEqual([a["href"] for a in links if a.get("id")=="share-pair"],
                         ["?left=anna&right=karamazov#pairs"])
        doc=json.loads((ROOT/"assets/evidence-snapshot.json").read_text(encoding="utf-8"))
        measured={b["key"] for b in doc["books"] if b["text_status"]=="measured"}
        self.assertEqual(len(measured),9)
        self.assertTrue({"anna","karamazov"}.issubset(measured))
        self.assertIn('id="pair-status" class="control-note" aria-live="polite"',html)
        css=(ROOT/"assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn(".permalink-help a { display:inline-flex; min-height:44px",css)

    def test_allowlisted_routing_and_history(self):
        js=(ROOT/"assets/pages-reader.js").read_text(encoding="utf-8")
        for fragment in ('function pairFromUrl() {','params.get("left"), right = params.get("right")',
                         'getBook(left) && getBook(right) && left !== right',
                         'function selectPair(left, right, addHistory=false)',
                         'if (!getBook(left) || !getBook(right)) return',
                         'share.removeAttribute("href")','url.searchParams.set("left", left)',
                         'url.searchParams.set("right", right)',
                         'window.history.pushState(null, "", url)','selectPair(left,right)',
                         'leftSelect.addEventListener("change",()=>selectPair',
                         'rightSelect.addEventListener("change",()=>selectPair'):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment,js)
        self.assertNotIn("fetch(window.location",js)
        self.assertNotIn("innerHTML",js)

    @unittest.skipUnless(shutil.which("node"),"Node missing; structural tests still run")
    def test_actual_routing_functions(self):
        for args in (["node","--check",str(ROOT/"assets/pages-reader.js")],
                     ["node",str(ROOT/"tests/pages_pair_permalink_smoke.cjs")]):
            proc=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=20,check=False)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)

if __name__=="__main__":
    unittest.main()
