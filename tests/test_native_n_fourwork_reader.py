"""Four independent pinned native N witnesses; source-free Reader acceptance."""
import copy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"word_count":65072,"sentence_count":6521,"baseline_defined":27916,"n_only":17352,"n_mixed_excluded":4469,"conditional_defined":45268}
PROVIDER = {"distribution":"pylem","version":"0.0.18","runtime_profile":"pylem-0.0.18-python39-sidecar-v1","sdist_sha256":"66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515"}
EVIDENCE = {"normalized_sha256":"e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee","wikitext_sha256":"f47b9b05d06dc2f5c6e2642d0822e6db68128386e4f1374b9188206a69fef11b","runtime_analysis_sha256":"f3d3bbdb730b950e3819c79fbef63e2f192c5139cd8b2dc7c6e9c1a20c43d5be","artifact_json_sha256":"358134587e6981dd538c047aa8bc88d4d9ebb50c09e9f82cf45ded9292ac606a","artifact_zip_sha256":"25c9148a4f70d99dc94d32485f334ed5dafd44863dd331acfde59e21cf82dfb0","head_sha":"b876f16544d5bff83c8f3d0510468cbc7494b042","run_id":45074193614,"artifact_id":14774267987,"receipt_url":"https://github.com/drevendev/Scriptorium/pull/617#issuecomment-7086364319"}
WORK = {"candidate_id":"grin-road-nowhere-ru","title":"Дорога в никуда","author":"Александр Грин","language":"ru","wikisource_revision_id":5585836,"characters_including_spaces":442656}

def validate(doc):
    if set(doc) != {"schema_version","status","source_text_included",
                    "m2_parity_admissible","work","provider","evidence","counts","note"}:
        raise ValueError("unexpected evidence or potential source text")
    if (doc["schema_version"] != "scriptorium-native-n-road-public-summary-v1"
        or doc["status"] != "diagnostic_only"
        or doc["source_text_included"] is not False
        or doc["m2_parity_admissible"] is not False
        or doc["provider"] != PROVIDER or doc["evidence"] != EVIDENCE
        or doc["work"] != WORK or "Source-free projection" not in doc["note"]):
        raise ValueError("native source, runtime or privacy drift")
    c=doc["counts"]
    if (type(c) is not dict or set(c) != set(EXPECTED)
        or any(type(v) is not int for v in c.values())
        or c != EXPECTED
        or c["n_only"]+c["baseline_defined"] != c["conditional_defined"]
        or c["n_only"]+c["n_mixed_excluded"] > c["word_count"]):
        raise ValueError("native counts drift")
    return c

def human(n):
    return f"{n:,}".replace(",", " ")

def pct(n):
    return f"{n:.2f}".replace(".", ",")

class FourWorkTests(unittest.TestCase):
    def setUp(self):
        self.doc=json.loads((ROOT/"assets/n-uncertainty-road-summary.json").read_text(encoding="utf-8"))
        self.html=(ROOT/"n-uncertainty.html").read_text(encoding="utf-8")

    def test_four_real_rows_and_bars_from_source_free_receipts(self):
        road=validate(self.doc)
        self.assertEqual(self.html.count('class="n-compare-track"'),4)
        self.assertIn("Четыре книги",self.html)
        self.assertIn("DIAGNOSTIC_ONLY · M2: 0/5",self.html)
        self.assertNotIn("<script",self.html)
        for field in ("normalized_sha256","runtime_analysis_sha256","receipt_url"):
            self.assertIn(EVIDENCE[field],self.html)
        for key,title,c in (
          ("anna","Анна Каренина",json.loads((ROOT/"assets/n-uncertainty-anna.json").read_text())["counts"]),
          ("resurrection","Воскресение",json.loads((ROOT/"assets/n-uncertainty-resurrection-summary.json").read_text())["counts"]),
          ("grin","Бегущая по волнам",json.loads((ROOT/"assets/n-uncertainty-grin-summary.json").read_text())["counts"]),
          ("road","Дорога в никуда",road),
        ):
            w,o,m=(c[k] for k in ("word_count","n_only","n_mixed_excluded"))
            row=(f'<tr data-n-threework="{key}"><th scope="row">{title}</th>'
                 f'<td>{human(w)}</td><td>{human(o)} · {pct(100*o/w)}%</td>'
                 f'<td>{human(m)} · {pct(100*m/w)}%</td>'
                 f'<td>{human(o+m)} · {pct(100*(o+m)/w)}%</td></tr>')
            self.assertIn(row,self.html)
            self.assertIn(f'data-n-bar="{key}"',self.html)
            self.assertIn(f'style="width:{100*o/w:.6f}%"',self.html)
            self.assertIn(f'style="width:{100*m/w:.6f}%"',self.html)

    def test_forged_receipt_and_text_leaks_fail_closed(self):
        for group,key,value in (
          ("counts","n_only",17353),("counts","word_count",65072.0),
          ("counts","n_mixed_excluded",True),("provider","version","0.0.19"),
          ("work","wikisource_revision_id",5585837),
          ("evidence","artifact_json_sha256","0"*64),
          (None,"source_text_included",True),(None,"m2_parity_admissible",True),
        ):
            bad=copy.deepcopy(self.doc)
            (bad[group] if group else bad)[key]=value
            with self.subTest(field=key),self.assertRaises(ValueError):validate(bad)
        bad=copy.deepcopy(self.doc);bad["normalized_text"]="private"
        with self.assertRaises(ValueError):validate(bad)
        serialized=json.dumps(self.doc)
        for field in ('"normalized_text"','"tokens"','"lemmas"','"source_text"'):
            self.assertNotIn(field,serialized)

    def test_exact_branch_stage_and_live_byte_guard(self):
        w=(ROOT/".github/workflows/pages.yml").read_text()
        audit=(ROOT/"scriptorium/branch_pages_audit.py").read_text()
        live=(ROOT/"tests/pages_live_byte_guard.cjs").read_text()
        browser=(ROOT/"tests/pages_browser_acceptance.cjs").read_text()
        for needle in (f'cp assets/n-uncertainty-road-summary.json build/branch-root-preview/assets/n-uncertainty-road-summary.json',
                       f'test -s build/branch-root-preview/assets/n-uncertainty-road-summary.json',
                       f'cmp assets/n-uncertainty-road-summary.json build/branch-root-preview/assets/n-uncertainty-road-summary.json'):
            self.assertIn(needle,w)
        self.assertIn('"assets/n-uncertainty-road-summary.json"',audit)
        self.assertIn('"assets/n-uncertainty-road-summary.json"',live)
        self.assertIn('"n-uncertainty.html"',live)
        self.assertIn('data-n-threework="road"',browser)
        self.assertIn('n-uncertainty.html#n-three-work',(ROOT/"README.md").read_text())

if __name__=="__main__":
    unittest.main()
