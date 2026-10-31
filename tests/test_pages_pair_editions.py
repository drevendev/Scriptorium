"""Root Reader paired comparisons expose distinct source and translation identities."""
from pathlib import Path
import json
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PairEditionContextTests(unittest.TestCase):
    def test_static_fallback_is_real_and_source_bound(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        books={b["key"]:b for b in json.loads(
            (ROOT/"assets/evidence-snapshot.json").read_text(encoding="utf-8"))["books"]}
        for side,key in (("left","anna"),("right","karamazov")):
            book=books[key]
            self.assertIn('id="pair-'+side+'-edition"',html)
            self.assertIn(book["edition_id"],html)
            self.assertIn(book["source_sha256"][:12],html)
        self.assertIn('id="pair-edition-caveat"',html)
        self.assertIn("не доказывает влияние автора",html)
        self.assertIn("aria-label=\"Редакции выбранных текстов\"",html)
        css=(ROOT/"assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn(".pair-editions { display:grid",css)
        self.assertIn("@media (max-width:780px) { .pair-editions",css)

    def test_dynamic_is_conditional_on_validated_measured_json(self):
        js=(ROOT/"assets/pages-reader.js").read_text(encoding="utf-8")
        self.assertIn("function pairEditionDescription(book, side)",js)
        self.assertIn("function updatePairEditionContext(left,right)",js)
        self.assertIn("updatePairEditionContext(a,b);",js)
        self.assertIn("book.translator.name",js)
        self.assertIn("book.source_sha256.slice(0,12)",js)
        self.assertIn('el("pair-edition-caveat").textContent=',js)
        self.assertNotIn("innerHTML",js)

    @unittest.skipUnless(shutil.which("node"),"Node unavailable; structural tests run")
    def test_node_edition_context(self):
        for cmd in (["node","--check",str(ROOT/"assets/pages-reader.js")],
                    ["node",str(ROOT/"tests/pages_pair_editions_smoke.cjs")]):
            completed=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,
                                    check=False,timeout=20)
            self.assertEqual(completed.returncode,0,completed.stdout+completed.stderr)

if __name__=="__main__":
    unittest.main()
