"""Exact PR #270 renderer integration: scientific output fidelity, not parity.

Run via ``python -m unittest discover -s tests -p test_analyze_precision.py -v``.
"""
from __future__ import annotations

from decimal import Decimal
from html.parser import HTMLParser
import json
import unittest

from scriptorium.analyze import build_local_analysis, render_html, _format_value


class ReportRowParser(HTMLParser):
    """Read the actual rendered table cells without a browser dependency."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = {}
        self.in_row = False
        self.active_cell = None
        self.cells = []
        self.metric_id = ""
        self.in_metric_id = False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.in_row = True
            self.cells = []
            self.metric_id = ""
        elif tag == "code" and dict(attrs).get("class") == "metric-id":
            self.in_metric_id = True
        elif self.in_row and tag in ("th", "td"):
            self.active_cell = [tag, ""]

    def handle_data(self, data):
        if self.in_metric_id:
            self.metric_id += data
        if self.active_cell is not None:
            self.active_cell[1] += data

    def handle_endtag(self, tag):
        if tag == "code":
            self.in_metric_id = False
        if self.active_cell is not None and tag == self.active_cell[0]:
            self.cells.append((self.active_cell[0], self.active_cell[1].strip()))
            self.active_cell = None
        if tag == "tr":
            if len(self.cells) == 5 and self.cells[0][0] == "th" and self.cells[1][0] == "td":
                self.rows[self.metric_id] = self.cells[1][1]
            self.in_row = False


class LocalHtmlNumericFidelityTests(unittest.TestCase):
    def setUp(self):
        self.manuscript = "Кот сидел. Птица летела.\n— Сколько слов? — Десять!"
        self.report = build_local_analysis(self.manuscript.encode("utf-8"))

    def test_actual_engine_all_29_values_match_json_numeric_lexemes(self):
        html = render_html(self.report)
        parser = ReportRowParser()
        parser.feed(html)
        native = json.loads(json.dumps(self.report, ensure_ascii=False, allow_nan=False))
        self.assertEqual(len(native["metrics"]), 29)
        self.assertEqual(set(parser.rows), set(native["metrics"]))
        values = native["metrics"]
        real_float_count = 0
        for metric_id, row in values.items():
            value = row["value"]
            displayed = parser.rows[metric_id]
            if value is None:
                self.assertEqual(displayed, "Unavailable", metric_id)
            elif isinstance(value, int):
                self.assertEqual(displayed.replace(",", ""), str(value), metric_id)
            else:
                real_float_count += 1
                self.assertEqual(displayed, repr(value), metric_id)
        self.assertGreaterEqual(real_float_count, 1)
        self.assertNotIn(self.manuscript, html)
        self.assertIn("not measurement accuracy", html)
        self.assertIn("not parity claims", html)

    def test_long_binary64_values_are_not_rounded(self):
        metric = self.report["metrics"]["fantlab.general.mean_word_length_chars"]
        for value in (0.032551102993042313, 1.2345678901234567,
                      1.234567891234567e-8, 1e50, -0.0):
            with self.subTest(value=value):
                metric["value"] = value
                html = render_html(self.report)
                self.assertIn("<td>" + repr(value) + "</td>", html)
                self.assertEqual(Decimal(_format_value(value)), Decimal(repr(value)))

    def test_nonfinite_boolean_int_and_null_are_preserved_or_rejected(self):
        metric = self.report["metrics"]["fantlab.general.mean_word_length_chars"]
        for value in (float("nan"), float("inf"), -float("inf"), True):
            with self.subTest(value=str(value)):
                metric["value"] = value
                with self.assertRaises(ValueError):
                    render_html(self.report)
        metric["value"] = None
        self.assertIn("<td>Unavailable</td>", render_html(self.report))
        self.report["metrics"]["fantlab.general.characters"]["value"] = 9007199254740993
        self.assertIn("<td>9,007,199,254,740,993</td>", render_html(self.report))


if __name__ == "__main__":
    unittest.main()
