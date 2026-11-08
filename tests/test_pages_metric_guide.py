"""Regression for the published, no-JavaScript 29-metric reader guide."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

from scriptorium.metric_labels import METRIC_LABELS

ROOT = Path(__file__).resolve().parents[1]


class _GuideParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metric_rows = []
        self.ids = set()
        self.links = []
        self.language = False
        self.viewport = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.language = attrs.get("lang") == "ru"
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "tr" and attrs.get("id", "").startswith("metric-"):
            self.metric_rows.append(attrs["id"].removeprefix("metric-"))
        if tag == "a":
            self.links.append(attrs.get("href", ""))


class PublishedMetricGuideTests(unittest.TestCase):
    def test_all_frozen_metric_ids_have_exactly_one_explanation(self):
        page = (ROOT / "metrics.html").read_text(encoding="utf-8")
        parser = _GuideParser()
        parser.feed(page)
        self.assertTrue(parser.language)
        self.assertTrue(parser.viewport)
        self.assertEqual(len(parser.metric_rows), 29)
        self.assertEqual(len(set(parser.metric_rows)), 29)
        self.assertEqual(set(parser.metric_rows), set(METRIC_LABELS))
        self.assertEqual(len([m for m in parser.metric_rows if m.startswith("fantlab.punctuation.")]), 14)
        self.assertIn("scriptorium.general.sentences", parser.metric_rows)
        self.assertIn("scriptorium-text-v1", page)
        self.assertIn("scriptorium-punctuation-v2", page)
        self.assertIn("M2: 0/5", page)
        self.assertIn("NOT_RUN", page)
        self.assertIn("inferred", page)
        self.assertIn("reproduced", page)
        self.assertIn("Публичное определение", page)
        self.assertIn("Публичное поле", page)
        self.assertIn("Расширение Scriptorium", page)
        self.assertNotIn("<script", page.lower())
        self.assertTrue(all(h and not h.startswith(("javascript:", "data:")) for h in parser.links))

    def test_real_reader_has_accessible_guide_entry_points(self):
        reader = (ROOT / "index.html").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        page = (ROOT / "metrics.html").read_text(encoding="utf-8")
        self.assertIn('href="./metrics.html"', reader)
        self.assertIn("metrics.html", readme)
        self.assertIn('href="./?book=anna#measurements"', page)
        self.assertIn('href="./assets/pages-reader.css"', page)
        self.assertIn('href="./#measurements"', page)
        self.assertNotRegex(page, r'href="[.]\/docs\/[^"]+[.]md"')
        self.assertEqual(len(re.findall(r'<section class="metric-group"', page)), 4)
        self.assertEqual(len(re.findall(r'<table>', page)), 4)


if __name__ == "__main__":
    unittest.main()
