"""Russian-first branch Pages: metric integrity, translation identity, truthful catalogue.

The original texts are never stored here. Site figures are exclusively pinned
derived numeric observations; availability is not FantLab parity.
"""
from __future__ import annotations
from hashlib import sha1,sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"index.html"
DATA=ROOT/"assets/evidence-snapshot.json"
JS=ROOT/"assets/pages-reader.js"
CSS=ROOT/"assets/pages-reader.css"
HYPER=ROOT/"corpus/candidates/diagnostics/tolstoy-hyperboloid-garin-wikisource-ru.retained.json"

SOURCE=(
 ("anna","benchmarks/fantlab/work270306-wikisource-diagnostic.json",28,23),
 ("waves","corpus/candidates/diagnostics/grin-running-on-waves-ru.json",27,23),
 ("silver","corpus/candidates/diagnostics/bely-silver-dove-ru.json",29,24),
 ("karamazov","corpus/candidates/diagnostics/dostoevsky-brothers-karamazov-ru.json",29,24),
 ("hyperboloid","corpus/candidates/diagnostics/tolstoy-hyperboloid-garin-wikisource-ru.retained.json",29,24),
 ("beketova","corpus/candidates/diagnostics/verne-children-captain-grant-beketova-ru.json",11,11),
 ("resurrection","corpus/candidates/diagnostics/tolstoy-resurrection-ru.retained.json",29,24),
 ("road","corpus/candidates/diagnostics/grin-road-nowhere-ru.retained.json",29,24),
 ("oblomov","corpus/candidates/diagnostics/goncharov-oblomov-ru.json",29,24),
)
PENDING={
 "petersburg":"corpus/candidates/source-edition-traces/bely-petersburg-1916-ru.json",
 "darwin":"corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json",
}

class Tags(HTMLParser):
    def __init__(self,text):
        super().__init__()
        self.start=[]
        self.links=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        value=dict(attrs);self.start.append((tag,value))
        if tag=="a":self.links.append(value.get("href"))

def blob_sha(data:bytes)->str:
    return sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()

class RussianBranchReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DATA.read_text(encoding="utf-8"))
        cls.html=SITE.read_text(encoding="utf-8")
        cls.js=JS.read_text(encoding="utf-8")
        cls.css=CSS.read_text(encoding="utf-8")

    def test_russian_first_is_real_and_english_separate(self):
        d=self.data
        self.assertEqual(d["schema"],"scriptorium-ru-reader-v2")
        self.assertEqual(d["language_module"],"ru")
        self.assertEqual(d["scientific_claim"],"DIAGNOSTIC_ONLY")
        self.assertEqual(d["fantlab_input_identity"],"UNKNOWN")
        self.assertIs(d["comparability"]["m2_parity_admissible"],False)
        self.assertEqual(d["counts"],{
          "work_count":11,"measured_works":9,"awaiting_measurement":2,
          "metrics_total":240,"numeric_total":201,"unavailable_total":39,
          "m2_source_matched":0
        })
        self.assertEqual(d["language_modules"]["ru"]["measured_work_count"],9)
        self.assertEqual(d["language_modules"]["en"]["state"],"planned_not_measured")
        self.assertEqual(d["language_modules"]["en"]["measured_work_count"],0)
        self.assertEqual(d["language_modules"]["fr"]["measured_work_count"],0)
        self.assertEqual(len(d["books"]),11)
        self.assertEqual({b["language"] for b in d["books"]},{"ru"})
        self.assertEqual(len({b["candidate_id"] for b in d["books"]}),11)
        self.assertEqual(len({(b["family_id"],b["edition_id"]) for b in d["books"]}),11)
        self.assertEqual(sum(b["measured"] for b in d["books"]),201)
        self.assertEqual(sum(b["unavailable"] for b in d["books"]),39)
        self.assertEqual(sum(len(b["metrics"]) for b in d["books"]),240)

    def test_exact_source_free_measurements_preserved_for_seven_books(self):
        works={b["key"]:b for b in self.data["books"]}
        for key,path,total,observed in SOURCE:
            with self.subTest(book=key):
                b=works[key]
                raw=(ROOT/path).read_bytes()
                artifact=json.loads(raw)
                self.assertEqual(blob_sha(raw),b["blob_sha1"])
                self.assertEqual(b["candidate_id"],artifact["candidate_id"])
                self.assertEqual(b["text_status"],"measured")
                self.assertEqual(len(b["metrics"]),total)
                self.assertEqual(b["measured"],observed)
                self.assertEqual(b["unavailable"],total-observed)
                self.assertEqual(len({m["id"] for m in b["metrics"]}),total)
                self.assertEqual(b["language"],"ru")
                self.assertRegex(b["source_sha256"],r"^[0-9a-f]{64}$")
                self.assertIn("github.com/drevendev/Scriptorium/blob/master/",b["evidence_url"])
                self.assertIsInstance(b["profiles"],dict)
                if key=="anna":
                    self.assertIs(artifact["epistemic_status"]["m2_parity_admissible"],False)
                    self.assertIs(artifact["evidence"]["source_text_committed"],False)
                    self.assertEqual(b["source_sha256"],artifact["evidence"]["raw_sha256"])
                    readings={k:(v["actual"],v["expected"]) for k,v in artifact["metrics"].items()}
                elif key=="hyperboloid":
                    self.assertIs(artifact["m2_parity_admissible"],False)
                    self.assertIs(artifact["source_text_committed"],False)
                    self.assertEqual(artifact["original_ci_artifact_json_sha256"],
                                     "95245fd09caea8b9150a6e7c1215c6f3c52fbaa54aa83d898a81a247192cf56d")
                    self.assertEqual(artifact["original_ci_archive_sha256"],
                                     "4b5eca834a343cbe2c8bfa167942972ad652a1b64c25a97430a17dcf07ec698c")
                    self.assertEqual(b["source_sha256"],artifact["source_body_sha256"])
                    from scriptorium.hyperboloid_diagnostic import (
                        FROZEN_BODY_SHA256, FANTLAB_REFERENCES,
                    )
                    self.assertEqual(b["source_sha256"],FROZEN_BODY_SHA256)
                    self.assertEqual(FANTLAB_REFERENCES,{
                        "fantlab.general.characters":"495539",
                        "fantlab.general.words":"69126",
                    })
                    readings={m["id"]:(m["actual"],m["reference"]) for m in artifact["metric_rows"]}
                elif key=="resurrection":
                    self.assertIs(artifact["gates"]["m2_parity_admissible"],False)
                    self.assertIs(artifact["source_text_committed"],False)
                    self.assertEqual(artifact["body_identity"]["chapter_count"],129)
                    self.assertEqual(artifact["source_evidence"]["original_ci_artifact_json_sha256"],"c122b9c95273bb78064c66d4e58fd82beb5e95480f1b98c78c71f5fcf536eefe")
                    self.assertEqual(artifact["source_evidence"]["original_ci_archive_sha256"],"b74edf2ac8d721a4d65f59bd4eb0df8f84a443829664577368a28fbe4d6ad78b")
                    self.assertEqual(b["source_sha256"],artifact["source_body_sha256"])
                    from scriptorium.resurrection_diagnostic import FROZEN_BODY_SHA256, FROZEN_BODY_CHARACTERS, FANTLAB_REFERENCES
                    self.assertEqual(FROZEN_BODY_SHA256,b["source_sha256"])
                    self.assertEqual(FROZEN_BODY_CHARACTERS,890835)
                    self.assertEqual(artifact["fantlab"]["public_display_references_retained"],FANTLAB_REFERENCES)
                    self.assertEqual(sum(m["actual"] is None for m in artifact["metric_rows"]),5)
                    readings={m["metric_id"]:(m["actual"],None if m["fantlab_display"] is None else float(m["fantlab_display"])) for m in artifact["metric_rows"]}
                elif key=="oblomov":
                    self.assertIs(artifact["gates"]["m2_parity_admissible"],False)
                    self.assertIs(artifact["gates"]["source_text_committed"],False)
                    self.assertEqual(artifact["gates"]["source_edition_print_collation"],"NOT_RUN")
                    self.assertEqual(artifact["source"]["revision_id"],5724579)
                    self.assertEqual(b["source_sha256"],artifact["body"]["raw_sha256"])
                    readings={m["metric_id"]:(m["actual"],None) for m in artifact["metric_rows"]}
                elif key=="beketova":
                    self.assertIs(artifact["gates"]["m2_parity_admissible"],False)
                    self.assertIs(artifact["source_text_committed"],False)
                    self.assertEqual(artifact["translation_identity"],"Alexandra A. Beketova Russian translation")
                    self.assertEqual(b["source_sha256"],artifact["body_identity"]["raw_sha256"])
                    readings={m["metric_id"]:(m["value"],None) for m in artifact["metrics"]}
                else:
                    self.assertIs(artifact["gates"]["m2_parity_admissible"],False)
                    self.assertIs(artifact["source_text_committed"],False)
                    self.assertEqual(b["source_sha256"],artifact["body_identity"]["raw_sha256"])
                    if key=="waves":
                        readings={m["metric_id"]:(m["scriptorium_raw_value"],
                            None if m["fantlab_display_value"] is None
                            else float(m["fantlab_display_value"])) for m in artifact["metrics"]}
                    else:
                        readings={m["metric_id"]:(m["actual"],
                            None if m["fantlab_display"] is None
                            else float(m["fantlab_display"])) for m in artifact["metric_rows"]}
                self.assertEqual(len(readings),total)
                for row in b["metrics"]:
                    actual,reference=readings[row["id"]]
                    self.assertEqual(row["actual"],actual)
                    if row["kind"]=="extension":
                        self.assertIsNone(row["reference"])
                    elif reference is None:
                        self.assertIsNone(row["reference"])
                    else:
                        self.assertEqual(float(row["reference"]),float(reference))
                    self.assertEqual(row["status"]=="measured",actual is not None)
                self.assertEqual(sum(m["actual"] is not None for m in b["metrics"]),observed)

    def test_versioned_translation_and_corpus_status_not_faked(self):
        works={b["key"]:b for b in self.data["books"]}
        translation=works["beketova"]
        self.assertEqual(translation["family_id"],"verne-children-captain-grant")
        self.assertEqual(translation["original_language"],"fr")
        self.assertEqual(translation["language"],"ru")
        self.assertEqual(translation["translator"]["id"],"alexandra-a-beketova")
        self.assertIn("Бекетова",translation["translator"]["name"])
        darwin=works["darwin"]
        self.assertEqual(darwin["original_language"],"en")
        self.assertEqual(darwin["language"],"ru")
        self.assertIn("Рачинский",darwin["translator"]["name"])
        self.assertNotEqual(darwin["family_id"],translation["family_id"])
        self.assertNotEqual(darwin["edition_id"],translation["edition_id"])
        for key,path in PENDING.items():
            with self.subTest(pending=key):
                b=works[key]
                self.assertNotEqual(b["text_status"],"measured")
                self.assertEqual(b["measured"],0)
                self.assertEqual(b["unavailable"],0)
                self.assertEqual(b["metrics"],[])
                self.assertEqual(b["trace"],path)
                self.assertTrue((ROOT/path).is_file())
                self.assertTrue(b["reason"])
        trace=json.loads((ROOT/PENDING["darwin"]).read_text(encoding="utf-8"))
        self.assertEqual(trace["original_language"],"en")
        self.assertEqual(trace["analysis_language"],"ru")
        self.assertIn("Rachinsky",trace["translator"])
        trace2=json.loads((ROOT/translation["translator"]["authority_trace"]).read_text(encoding="utf-8"))
        self.assertEqual(trace2["original_language"],"fr")
        self.assertEqual(trace2["analysis_language"],"ru")

    def test_landing_has_real_charts_comparison_and_accessible_status(self):
        h=self.html
        parsed=Tags(h)
        self.assertIn('<html lang="ru">',h)
        self.assertEqual(sum(t=="h1" for t,_ in parsed.start),1)
        self.assertEqual(sum(t=="article" and a.get("class","").startswith("book") for t,a in parsed.start),11)
        self.assertEqual(h.count('class="chart-row"'),9)
        self.assertIn('id="pair-left"',h)
        self.assertIn('id="pair-right"',h)
        self.assertIn('id="pair-metric"',h)
        self.assertIn('id="paired-graphic"',h)
        self.assertIn('id="pair-rows"',h)
        self.assertIn('id="measurement-rows"',h)
        self.assertIn('type="search"',h)
        self.assertIn('aria-live="polite"',h)
        self.assertIn('tabindex="0" role="region"',h)
        self.assertIn('id="translations"',h)
        self.assertIn("Бекетовой",h)
        self.assertIn("Рачинского",h)
        self.assertIn("240",h)
        self.assertIn("201",h)
        self.assertIn("39",h)
        self.assertIn("M2: 0/5",h)
        for anchor in ("#books","#pairs","#measurements","#translations","#method"):
            self.assertIn(anchor,parsed.links)
        self.assertIn('./assets/pages-reader.css',h)
        self.assertIn('./assets/pages-reader.js',h)
        self.assertNotIn('http://',h)
        self.assertNotIn('fonts.googleapis',h)
        self.assertNotIn('<form',h) # no fake manuscript upload

    def test_js_fails_closed_on_wrong_language_unknown_or_fake_parity(self):
        js=self.js
        self.assertIn('doc.schema !== "scriptorium-ru-reader-v2"',js)
        self.assertIn('doc.counts?.measured_works !== 9',js)
        self.assertIn('doc.counts?.metrics_total !== 240',js)
        self.assertIn('doc.comparability?.m2_parity_admissible !== false',js)
        self.assertIn('doc.language_modules?.en?.measured_work_count !== 0',js)
        self.assertIn("book.original_language !== book.language",js)
        self.assertIn("book.family_id",js)
        self.assertIn("book.edition_id",js)
        self.assertIn('a.profiles[profile]===b.profiles?.[profile]',js)
        self.assertIn('m.actual !== null',js)
        self.assertIn('credentials:"omit"',js)
        self.assertIn('replaceChildren',js)
        self.assertIn('textContent',js)
        self.assertIn('function updatePair()',js)
        self.assertIn('function updateChart()',js)
        self.assertIn('function exportSelected()',js)
        self.assertNotIn('innerHTML',js)
        for forbidden in ("localStorage","sendBeacon","XMLHttpRequest","document.cookie","eval("):
            self.assertNotIn(forbidden,js)

    def test_mobile_print_keyboard_and_readable_charts(self):
        css=self.css
        for needed in ('.skip-link:focus',':focus-visible','min-height:44px',
                       '@media (max-width:490px)','@media (max-width:780px)',
                       '@media (prefers-reduced-motion: reduce)',
                       '@media (forced-colors: active)','@media print',
                       '.paired-graphic','.translation-card','.pair-track','.chart-row'):
            with self.subTest(rule=needed):
                self.assertIn(needed,css)
        self.assertNotIn("@import",css)
        self.assertNotIn("https://fonts.",css)

if __name__=="__main__":
    unittest.main()
