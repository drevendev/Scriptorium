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
        self.metric_focus_targets = []
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
            self.metric_focus_targets.append((attrs["id"], attrs.get("tabindex")))
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

    def test_metric_deep_links_land_on_focusable_rows_without_tab_stops(self):
        """Each no-JS fragment can receive focus but is not a new Tab stop."""
        page = (ROOT / "metrics.html").read_text(encoding="utf-8")
        parser = _GuideParser()
        parser.feed(page)
        self.assertEqual(len(parser.metric_focus_targets), 29)
        self.assertEqual(
            {target for target, _ in parser.metric_focus_targets},
            {"metric-" + metric for metric in METRIC_LABELS},
        )
        self.assertTrue(all(mode == "-1" for _, mode in parser.metric_focus_targets))
        # Negative regression: changing a single row to tabindex=0 adds a Tab stop.
        broken = _GuideParser()
        broken.feed(page.replace('tabindex="-1"', 'tabindex="0"', 1))
        self.assertFalse(all(mode == "-1" for _, mode in broken.metric_focus_targets))
        styles = page.split("<style>", 1)[1].split("</style>", 1)[0]
        self.assertIn(".metric-group tr:target{outline:3px solid var(--focus);", styles)
        self.assertIn("scroll-margin-block-start:1rem", styles)
        self.assertIn(".metric-group tr:target{outline-color:Highlight}", styles)
        self.assertNotIn("<script", page.lower())

    def test_long_glossary_print_tables_can_span_pages(self):
        page = (ROOT / "metrics.html").read_text(encoding="utf-8")
        styles = page.split("<style>", 1)[1].split("</style>", 1)[0]
        print_rules = styles.split("@media print", 1)[1]
        # The punctuation group has fourteen actual rows; forcing the whole
        # section to remain on a page can leave a blank/clipped print page.
        self.assertEqual(
            page.count('<tr id="metric-fantlab.punctuation.'),
            14,
        )
        self.assertIn(".metric-group{break-inside:auto;", print_rules)
        # Screen scrolling is useful, but its higher specificity would clip printed rows.
        self.assertIn(".metric-group .table-region{overflow-x:auto;", styles.split("@media print", 1)[0])
        self.assertIn(".metric-group .table-region{overflow:visible}", print_rules)
        self.assertNotIn(".metric-group{break-inside:avoid}", print_rules)
        self.assertIn(".metric-group thead{display:table-header-group}", print_rules)
        self.assertIn(".metric-group tr{break-inside:avoid;page-break-inside:avoid}", print_rules)
        self.assertIn(".metric-group table{min-width:0;width:100%;font-size:9pt;", print_rules)
        self.assertIn(".metric-group th,.metric-group td{overflow-wrap:anywhere;", print_rules)

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

    def test_branch_root_preview_contains_metric_guide(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        # Pages may be configured as branch deployment; the CI preview must
        # nevertheless contain every Reader route linked from its first screen.
        self.assertEqual(workflow.count('      - "metrics.html"'), 2)
        self.assertIn("cp metrics.html build/branch-root-preview/metrics.html", workflow)
        self.assertIn("test -s build/branch-root-preview/metrics.html", workflow)
        self.assertIn("cmp metrics.html build/branch-root-preview/metrics.html", workflow)

    def test_interactive_reader_links_to_exact_definitions(self):
        """Only canonical metric IDs become links; no source text or script URLs."""
        source = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        reader = (ROOT / "index.html").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn('link.href="./metrics.html#metric-"+encodeURIComponent(id);', source)
        self.assertIn('link.textContent=shown;', source)
        self.assertIn('link.setAttribute("aria-label","Методика показателя: "+label(id));', source)
        self.assertIn('appendMetricDefinition(th,m.id);', source)
        self.assertIn('appendMetricDefinition(metricTitle,curr.id,"Как считается ↗");', source)
        self.assertEqual(source.count('appendMetricDefinition(th,m.id);'), 2)
        self.assertEqual(reader.count('href="./metrics.html">Откройте определения всех 29 показателей'), 2)
        self.assertIn("node tests/pages_metric_deep_link_smoke.cjs", workflow)
        self.assertNotIn('link.innerHTML', source)


if __name__ == "__main__":
    unittest.main()
