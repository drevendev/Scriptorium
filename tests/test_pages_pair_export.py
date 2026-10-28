"""Source-free root Pages two-book comparison download contract."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DownloadButtonParser(HTMLParser):
    def __init__(self, source: str):
        super().__init__()
        self.buttons = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag == "button":
            self.buttons.append(dict(attrs))


class PairExportTests(unittest.TestCase):
    def test_html_has_accessible_but_disabled_until_validated_export(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        buttons = DownloadButtonParser(html).buttons
        matching = [attrs for attrs in buttons if attrs.get("id") == "pair-export"]
        self.assertEqual(len(matching), 1)
        self.assertIn("disabled", matching[0])
        csv_buttons = [attrs for attrs in buttons if attrs.get("id") == "pair-export-csv"]
        self.assertEqual(len(csv_buttons), 1)
        self.assertIn("disabled", csv_buttons[0])
        self.assertIn("<td>% · Δ в п.п.</td>", html)
        self.assertIn("Только совместные измерения", html)
        self.assertIn('class="evidence-actions"', html)

    def test_export_is_source_free_scientifically_labeled_and_allowlisted(self):
        js = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        for claim in (
            "function sharedPairRows(a,b)",
            "function buildPairExport(leftKey,rightKey)",
            "function serializePairCsv(report)",
            "function csvText(value)",
            "function exportPairCsv()",
            'pairCsvButton.addEventListener("click",exportPairCsv)',
            "pairCsvButton.disabled=rows.length===0;",
            "sharedPairRows(a,b)",
            'schema:"scriptorium-ru-pair-comparison-v1"',
            'scientific_claim:"DIAGNOSTIC_ONLY"',
            'fantlab_input_identity:"UNKNOWN",m2_source_matched:0',
            "text_included:false",
            'comparison_direction:"right_minus_left"',
            'delta_unit:measurementUnit==="%"?"percentage_points":measurementUnit',
            "left_actual:row.left,right_actual:row.right",
            "delta_right_minus_left:row.right-row.left",
            'const result=buildPairExport(leftSelect.value,rightSelect.value)',
            "pairExportButton.disabled=rows.length===0",
            'pairExportButton.addEventListener("click",exportPair)',
        ):
            with self.subTest(claim=claim):
                self.assertIn(claim, js)
        self.assertNotIn("innerHTML", js)
        self.assertNotIn("localStorage", js)
        self.assertNotIn("sendBeacon", js)

    @unittest.skipUnless(shutil.which("node"), "Node unavailable: structural tests still run")
    def test_real_pair_export_node_smoke(self):
        for command in (
            ["node", "--check", str(ROOT / "assets/pages-reader.js")],
            ["node", str(ROOT / "tests/pages_pair_export_smoke.cjs")],
        ):
            proc = subprocess.run(command, cwd=ROOT, text=True,
                                  capture_output=True, timeout=20, check=False)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
