"""Chart CSV is evidence-bound and safe before any interactive export."""
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestChartCsv(unittest.TestCase):
    def test_control_is_disabled_until_verification(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        js = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn('id="chart-export-csv" disabled', html)
        self.assertIn("chartCsvButton,...chartButtons", js)
        self.assertIn('chartCsvButton.addEventListener("click",exportChartCsv)', js)
        self.assertIn('doc.scientific_claim!=="DIAGNOSTIC_ONLY"', js)
        self.assertIn("not_recorded", js)
        self.assertIn(".chart-sort button:focus-visible", css)

    @unittest.skipUnless(shutil.which("node"), "Node unavailable")
    def test_shipped_source_with_actual_catalogue(self):
        for command in (
            ["node", "--check", str(ROOT / "assets/pages-reader.js")],
            ["node", str(ROOT / "tests/pages_chart_csv_smoke.cjs")],
        ):
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                                    timeout=25, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
