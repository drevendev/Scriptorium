"""Reader CSV export is complete, reproducible and scientifically fail-closed."""
from __future__ import annotations

import copy
import csv
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from scriptorium.trusov_excerpt_export import (
    FIELDS, SOURCE_RELATIVE, COVERAGE, load_frozen_report, render_csv,
)

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "assets" / "trusov-1775-interior-metrics.csv"


class TrusovExcerptCsvTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load_frozen_report(ROOT / SOURCE_RELATIVE)

    def test_csv_is_exactly_reproducible_from_pinned_metric_source(self):
        export = render_csv(self.source)
        self.assertEqual(CSV.read_text(encoding="utf-8"), export)
        reader = csv.DictReader(StringIO(export))
        self.assertEqual(reader.fieldnames, list(FIELDS))
        rows = list(reader)
        self.assertEqual(len(rows), 29)
        self.assertEqual(sum(row["actual"] != "" for row in rows), 22)
        self.assertEqual(sum(row["actual"] == "" for row in rows), 7)
        for row, original in zip(rows, self.source["metric_rows"]):
            self.assertEqual(row["metric_id"], original["metric_id"])
            self.assertEqual(row["unit"], original["unit"])
            self.assertEqual(row["result"], original["result"])
            self.assertEqual(row["compatibility_status"], original["compatibility_status"])
            self.assertEqual(row["coverage"], COVERAGE)
            self.assertEqual((row["page_from"], row["page_to"]), ("3", "147"))
            self.assertEqual(row["source_page_graph_sha256"], self.source["source_page_graph_sha256"])
            self.assertEqual(row["normalized_sha256"], self.source["normalized_sha256"])
            if original["actual"] is None:
                self.assertEqual(row["actual"], "")
            else:
                self.assertEqual(float(row["actual"]), float(original["actual"]))
        by_id = {row["metric_id"]: row for row in rows}
        self.assertEqual(by_id["fantlab.general.characters"]["actual"], "303882")
        self.assertEqual(by_id["fantlab.dialogue.share_percent"]["actual"], "0")
        self.assertEqual(by_id["fantlab.vocabulary.active_dictionary"]["actual"], "")
        self.assertEqual(by_id["fantlab.vocabulary.active_dictionary"]["result"],
                         "NOT_RUN_DICTIONARY_UNBOUND")

    def test_broken_source_bytes_are_rejected_even_if_json_remains_valid(self):
        raw = (ROOT / SOURCE_RELATIVE).read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "receipt.json"
            path.write_bytes(raw + b" ")
            with self.assertRaisesRegex(ValueError, "SHA-1 mismatch"):
                load_frozen_report(path)

    def test_scope_promotion_and_false_numeric_zero_are_rejected(self):
        bad = copy.deepcopy(self.source)
        bad["gates"]["corpus_admitted_for_calibration"] = True
        with self.assertRaisesRegex(ValueError, "scientific scope"):
            render_csv(bad)
        bad = copy.deepcopy(self.source)
        row = next(r for r in bad["metric_rows"] if r["actual"] is None)
        row["actual"] = 0
        with self.assertRaisesRegex(ValueError, "unverified"):
            render_csv(bad)
        bad = copy.deepcopy(self.source)
        bad["metric_rows"][0]["metric_id"] = "=SUM(1,1)"
        with self.assertRaisesRegex(ValueError, "unsafe CSV"):
            render_csv(bad)

    def test_reader_download_is_real_and_not_presented_as_complete_book(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        block = html.split('<section id="trusov-excerpt"', 1)[1].split("</section>", 1)[0]
        self.assertIn('href="./assets/trusov-1775-interior-metrics.csv" download', block)
        self.assertIn("НЕ КНИГА", block)
        self.assertIn("M2: 0/5", block)
        self.assertIn('data-analysis-status="unmeasured"', html)
        self.assertIn("assets/trusov-1775-interior-metrics.csv", readme)
        self.assertTrue(CSV.is_file())


if __name__ == "__main__":
    unittest.main()
