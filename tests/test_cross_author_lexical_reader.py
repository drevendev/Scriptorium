"""Retained #645 public projection: numerical evidence, no source forms."""
import json
from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Metrics(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = {}
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "data-metric" in d:
            key = (d["data-pair"], d["data-metric"])
            if key in self.values:
                raise ValueError("duplicate metric")
            self.values[key] = float(d["data-value"])

class CrossAuthorReaderTests(unittest.TestCase):
    def test_reviewed_numbers_and_boundaries(self):
        d = json.loads((ROOT / "assets/bely-tolstoy-lexical-diagnostic.json").read_text())
        self.assertEqual(d["status"], "DIAGNOSTIC_ONLY")
        self.assertIs(d["source_text_included"], False)
        self.assertIs(d["per_form_data_included"], False)
        self.assertIs(d["m2_parity_admissible"], False)
        self.assertEqual(d["corpus_admission"], "NOT_VERIFIED")
        self.assertEqual(d["fantlab_analyzer_input_match"], "UNKNOWN")
        self.assertEqual(d["provenance"]["ci_artifact_id"], 15069667323)
        a = d["aggregate"]
        self.assertEqual(list(a.values()), [5819,16888,15039,4142,33604,1293,1400,1449,15.416203,45.476889,0.4268,26.939118,24.222411])
        self.assertEqual([w["revision_id"] for w in d["works"]], [5588003,5014458])
        self.assertEqual([w["characters_including_spaces"] for w in d["works"]], [563125,499066])
        self.assertEqual([w["word_tokens"] for w in d["works"]], [88236,71921])
        self.assertEqual([w["distinct_forms"] for w in d["works"]], [22707,20858])
        self.assertEqual(a["shared_form_count"]+a["left_only_form_count"]+a["right_only_form_count"],37746)
        self.assertAlmostEqual(a["type_jaccard_percent"],100*5819/37746,places=6)

    def test_charts_match_both_receipts(self):
        p = Metrics()
        page = (ROOT / "lexical-pairs.html").read_text()
        p.feed(page)
        expected = {}
        for pair,asset in (("grin","grin-lexical-diagnostic.json"),("cross","bely-tolstoy-lexical-diagnostic.json")):
            d = json.loads((ROOT / "assets" / asset).read_text())
            for key in ("type_jaccard_percent","token_distribution_overlap_percent","jensen_shannon_divergence_bits"):
                expected[(pair,key)] = d["aggregate"][key]
        self.assertEqual(p.values,expected)
        self.assertNotIn("<script",page)
        self.assertIn("M2: 0/5",page)
        self.assertIn('href="./lexical-pairs.html"', (ROOT / "index.html").read_text())

if __name__ == "__main__":
    unittest.main()
