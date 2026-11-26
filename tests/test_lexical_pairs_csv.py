"""Offline exact two-pair export and visible table contract."""
from contextlib import redirect_stderr, redirect_stdout
import csv
from decimal import Decimal
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import tempfile
import unittest

from scriptorium.lexical_pairs_csv import AGGREGATES, main, render_reviewed_pairs_csv

ROOT = Path(__file__).resolve().parents[1]
GRIN = ROOT / "assets/grin-lexical-diagnostic.json"
CROSS = ROOT / "assets/bely-tolstoy-lexical-diagnostic.json"
CSV = ROOT / "assets/lexical-pairs.csv"


class Table(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "td" and "data-export-field" in d:
            key = (d["data-export-pair"], d["data-export-field"])
            if key in self.cells:
                raise ValueError("duplicate cell")
            self.cells[key] = d["data-exact"]


class LexicalPairsCSVTests(unittest.TestCase):
    def test_exact_replay_and_every_table_cell(self):
        rendered = render_reviewed_pairs_csv(GRIN.read_bytes(), CROSS.read_bytes())
        self.assertEqual(rendered.encode(), CSV.read_bytes())
        rows = list(csv.DictReader(io.StringIO(rendered)))
        self.assertEqual(len(rows), 124)
        table = Table()
        table.feed((ROOT / "lexical-pairs.html").read_text(encoding="utf-8"))
        expected = {(r["pair"], r["field"]): r["value"] for r in rows
                    if r["section"] in ("aggregate", "difference")}
        self.assertEqual(table.cells, expected)
        for pair, source in (("grin", GRIN), ("cross", CROSS)):
            data = json.loads(source.read_bytes(), parse_float=Decimal)["aggregate"]
            for field in AGGREGATES:
                self.assertEqual(expected[(pair, field)], str(data[field]) if field in data else "NOT_RETAINED")
        self.assertEqual(expected[("cross_minus_grin", "type_jaccard_percent")], "-7.771349")
        self.assertEqual(expected[("cross_minus_grin", "token_distribution_overlap_percent")], "-14.366258")
        self.assertEqual(expected[("cross_minus_grin", "jensen_shannon_divergence_bits")], "0.1330")
        self.assertEqual(sum(r["status"] == "not_retained" for r in rows), 2)
        self.assertIn('href="./assets/lexical-pairs.csv" download', (ROOT / "lexical-pairs.html").read_text(encoding="utf-8"))

    def test_mutations_and_swapped_receipts_fail_closed(self):
        g, c = GRIN.read_bytes(), CROSS.read_bytes()
        for a, b in ((g+b" ", c), (g, c+b" "), (c, g), (g, b"{}")):
            with self.subTest(), self.assertRaises(ValueError):
                render_reviewed_pairs_csv(a, b)

    def test_cli_create_only_and_check(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / "pairs.csv"
            args = [str(GRIN), str(CROSS)]
            self.assertEqual(main(args + ["--output", str(out)]), 0)
            self.assertEqual(out.read_bytes(), CSV.read_bytes())
            self.assertEqual(main(args + ["--check", str(out)]), 0)
            with redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(main(args), 0)
            self.assertEqual(stdout.getvalue().encode(), CSV.read_bytes())
            out.write_bytes(b"stale")
            for flag in ("--output", "--check"):
                with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    main(args + [flag, str(out)])
                self.assertEqual(out.read_bytes(), b"stale")

    def test_bad_input_does_not_create_report(self):
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / "bad.json"
            bad.write_bytes(b"{}")
            out = Path(directory) / "pairs.csv"
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main([str(GRIN), str(bad), "--output", str(out)])
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
