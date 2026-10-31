"""Reader paired comparison distinguishes missing values from true measurements."""
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]

class PairCoverageTests(unittest.TestCase):
    def test_dom_and_static_scientific_caveat(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        js=(ROOT/"assets/pages-reader.js").read_text(encoding="utf-8")
        for metric_id in (
            "fantlab.dialogue.mean_dialogue_sentence_length_chars",
            "fantlab.dialogue.mean_narration_sentence_length_chars",
        ):
            self.assertIn('value="'+metric_id+'"',html)
        self.assertIn("«нет данных» — не ноль",html)
        self.assertIn("JSON/CSV содержат только измерения обеих книг",html)
        self.assertIn("function pairCoverageRows(a,b)",js)
        self.assertIn("const coverage=pairCoverageRows(a,b);",js)
        self.assertIn("for (const m of coverage)",js)
        self.assertIn('m.right===null?"нет данных":exact(m.right)',js)
        self.assertIn('const d=comparable?m.right-m.left:null;',js)
        self.assertIn('const rows=sharedPairRows(a,b);',js)
        self.assertNotIn("innerHTML",js)

    @unittest.skipUnless(shutil.which("node"),"Node unavailable: structural tests still run")
    def test_real_shipped_js_and_pinned_data(self):
        for cmd in (
            ["node","--check",str(ROOT/"assets/pages-reader.js")],
            ["node",str(ROOT/"tests/pages_pair_coverage_smoke.cjs")],
        ):
            completed=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,
                                     check=False,timeout=25)
            self.assertEqual(completed.returncode,0,completed.stdout+completed.stderr)

if __name__=="__main__":
    unittest.main()
