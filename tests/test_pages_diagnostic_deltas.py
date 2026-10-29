"""Regression coverage for descriptive, source-unmatched Reader deltas."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]

class ReaderDeltaTests(unittest.TestCase):
    def test_static_fallback_uses_pinned_numbers_not_guessed_scores(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        data=json.loads((ROOT/"assets/evidence-snapshot.json").read_text(encoding="utf-8"))
        rows=html.split('<tbody id="measurement-rows">',1)[1].split("</tbody>",1)[0]
        self.assertEqual(rows.count("<tr>"),4)
        self.assertEqual(rows.count('class="benchmark-delta"'),4)
        for value in ("+12\u00a0958","+16\u00a0083","−0,145 п.п.","−0,174"):
            self.assertIn(value,rows)
        for metric in ("fantlab.general.characters","fantlab.general.words",
                       "fantlab.dialogue.share_percent",
                       "fantlab.general.mean_sentence_length_chars"):
            row=next(m for m in data["books"][0]["metrics"] if m["id"]==metric)
            self.assertIsNotNone(row["actual"])
            self.assertIsNotNone(row["reference"])
            self.assertIn("<code>"+metric+"</code>",rows)
        self.assertIn('<th scope="col">Δ S−F</th>',html)
        self.assertIn("не критерий прохождения",html)
        self.assertEqual(data["counts"]["m2_source_matched"],0)

    def test_no_fake_zero_and_six_column_empty_state(self):
        js=(ROOT/"assets/pages-reader.js").read_text(encoding="utf-8")
        self.assertIn('insertText(tr,"td",diagnosticDelta(m),"benchmark-delta")',js)
        self.assertIn("td.colSpan=6",js)
        self.assertIn('if (m.kind==="extension") return "N/A"',js)
        self.assertIn('if (!isNumeric(m.actual)||!isNumeric(m.reference)) return "—"',js)
        self.assertNotIn("innerHTML",js)

    @unittest.skipUnless(shutil.which("node"),"Node unavailable")
    def test_shipped_js_behaviour(self):
        for command in (["node","--check",str(ROOT/"assets/pages-reader.js")],
                        ["node",str(ROOT/"tests/pages_diagnostic_deltas_smoke.cjs")]):
            result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=20)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)

if __name__=="__main__":
    unittest.main()
