"""Public projection is exact accepted #664 data, not an admission."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class RobinsonReaderTests(unittest.TestCase):
    def test_receipt_is_exact_and_holds_preserved(self):
        raw = (ROOT / "assets/robinson-pair.json").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), "36fc43f4651bec044c9febab1ebacc688751c2b7b4a5f17586c97641cfe65a1b")
        r = json.loads(raw)
        self.assertEqual(r["translation_coverage_alignment"], "NOT_RUN")
        self.assertFalse(r["corpus_admitted"])
        self.assertFalse(r["m2_parity_admissible"])
        self.assertEqual(r["fantlab_input_identity"], "UNKNOWN")
        self.assertEqual(len({x["metric_id"] for x in r["metric_rows"]}), 29)
        self.assertEqual(sum(x["delta_trusov_minus_shishmareva"] is not None for x in r["metric_rows"]), 22)

    def test_static_table_binds_every_value(self):
        r = json.loads((ROOT / "assets/robinson-pair.json").read_bytes())
        html = (ROOT / "robinson-pair.html").read_text(encoding="utf-8")
        rows = re.findall(r'<tr data-metric="([^"]+)">(.*?)</tr>', html)
        self.assertEqual([k for k, _ in rows], [x["metric_id"] for x in r["metric_rows"]])
        for (_, markup), row in zip(rows, r["metric_rows"], strict=True):
            cells = dict(re.findall(r'data-field="([^"]+)" data-value="([^"]+)"', markup))
            self.assertEqual(set(cells), {"trusov", "shishmareva", "delta_trusov_minus_shishmareva"})
            for k, value in cells.items():
                self.assertEqual(json.loads(value), row[k])
        self.assertLess(html.index("Диагностика, не эффект переводчика"), html.index("data-chart="))
        self.assertIn('href="./robinson-pair.html"', (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertNotIn("<script", html)
