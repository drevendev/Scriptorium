"""Regression and scientific-boundary tests for the homepage real-work showcase."""
from __future__ import annotations

import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

from scriptorium import site_work_comparison
from scriptorium.site_home_showcase import HOME_CSS, render_demo, render_research_atlas
from scriptorium.site_renderer import _render_index

ROOT = Path(__file__).resolve().parents[1]


def comparison_entry() -> dict:
    published = site_work_comparison.build(ROOT)
    return {
        **site_work_comparison.EXPECTED_ENTRY,
        "render_mode": "comparison",
        "author": "Alexander Grin / Jules Verne",
        "work_title": "Running on Waves / The Children of Captain Grant",
        "json_data": published["json"],
    }



def benchmark_entry() -> dict:
    from scriptorium import site_benchmark_matrix
    published = site_benchmark_matrix.build(ROOT)
    return {**site_benchmark_matrix.EXPECTED_ENTRY,
            "render_mode": "benchmark_matrix", "json_data": published["json"]}


class RecordedHTML(HTMLParser):
    def __init__(self, content: str):
        super().__init__()
        self.links = []
        self.start_tags = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.start_tags.append((tag, attributes))
        if tag == "a":
            self.links.append(attributes.get("href", ""))


class HomeShowcaseTests(unittest.TestCase):
    def test_showcase_uses_frozen_full_work_numbers_and_sources(self):
        entry = comparison_entry()
        result = render_demo([entry])
        doc = json.loads(entry["json_data"])
        metrics = {row["metric_id"]: row for row in doc["measurements"]}
        self.assertIn("Running on Waves", result)
        self.assertIn("The Children of Captain Grant", result)
        self.assertIn("M2: 0/5", result)
        self.assertIn("not FantLab parity", result)
        for metric_id in (
            "fantlab.dialogue.share_percent",
            "fantlab.general.mean_sentence_length_chars",
            "fantlab.punctuation.comma.per_1000_words",
        ):
            row = metrics[metric_id]
            with self.subTest(metric=metric_id):
                self.assertIn(row["label"], result)
                self.assertIn(str(row["left"]), result)
                self.assertIn(str(row["right"]), result)
                self.assertIn(f'{row["left"]:,.1f}', result)
                self.assertIn(f'{row["right"]:,.1f}', result)
        parsed = RecordedHTML(result)
        self.assertIn("works/two-full-work-differences/", parsed.links)
        self.assertEqual(sum(tag == "tr" for tag, _ in parsed.start_tags), 4)
        self.assertIn('<section class="demo-exact" aria-labelledby="demo-exact-title">', result)
        self.assertIn('<h3 id="demo-exact-title">Exact numbers and units</h3>', result)
        self.assertIn('role="region" aria-label="Exact comparison values"', result)
        self.assertNotIn("<details", result)
        self.assertNotIn("<summary", result)
        self.assertIn(".demo-exact h3 { color:#000; }", HOME_CSS)
        self.assertIn(".demo-scroll { overflow:visible; }", HOME_CSS)
        self.assertIn(".demo-panel table { min-width:0; width:100%; }", HOME_CSS)
        self.assertEqual(sum(tag == "h2" for tag, _ in parsed.start_tags), 1)
        self.assertNotIn("<script", result)
        self.assertNotIn("fetch(", result)


    def test_mobile_scroll_hint_and_print_text_legibility(self):
        result = render_demo([comparison_entry()])
        parsed = RecordedHTML(result)
        regions = [attrs for tag, attrs in parsed.start_tags
                   if tag == "div" and attrs.get("class") == "demo-scroll"]
        hints = [attrs for tag, attrs in parsed.start_tags
                 if tag == "p" and attrs.get("id") == "demo-scroll-hint"]
        self.assertEqual(len(regions), 1)
        self.assertEqual(len(hints), 1)
        self.assertEqual(regions[0]["tabindex"], "0")
        self.assertEqual(regions[0]["aria-describedby"], hints[0]["id"])
        self.assertIn("swipe to view all columns", result)
        self.assertIn("focus the table region and use arrow keys", result)
        self.assertIn(".demo-scroll-hint { color:#e6e9da;", HOME_CSS)

        print_css = HOME_CSS.split("@media print {", 1)[1]
        self.assertIn(
            ".demo-eyebrow, .demo-panel table caption, .demo-open { color:#000; }",
            print_css,
        )
        self.assertIn(".demo-open { text-decoration:underline; }", print_css)
        self.assertIn(".demo-scroll-hint { display:none; }", print_css)
        self.assertNotIn(".demo-scroll-hint { color:#e6e9da;", print_css)


    def test_print_preview_hover_and_focus_keep_link_readable(self):
        # Extract final @media print declarations rather than merely asserting that
        # a dark color appears somewhere in CSS. Hover has greater specificity than
        # the ordinary link, so a missing state-specific override would be unreadable.
        import re

        print_css = re.sub(r"/\*.*?\*/", "", HOME_CSS.split("@media print {", 1)[1], flags=re.S)
        self.assertRegex(print_css, r"\.demo-panel\s*\{[^{}]*background:\s*#fff\b")

        def declared_color(selector):
            result = None
            for heading, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", print_css):
                if selector in {item.strip() for item in heading.split(",")}:
                    color = re.search(
                        r"(?:^|;)\s*color\s*:\s*(#[0-9a-fA-F]{3,6})\s*;",
                        declarations,
                    )
                    if color:
                        result = color.group(1)
            return result

        def luminance(hex_color):
            digits = hex_color[1:]
            if len(digits) == 3:
                digits = "".join(character * 2 for character in digits)
            channels = [int(digits[index:index + 2], 16) / 255 for index in (0, 2, 4)]
            linear = [value / 12.92 if value <= 0.04045
                      else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
            return sum(channel * weight for channel, weight
                       in zip(linear, (0.2126, 0.7152, 0.0722)))

        def contrast_against_white(hex_color):
            return 1.05 / (luminance(hex_color) + 0.05)

        # This was the former :hover color: approximately 1.07:1 on printed white.
        self.assertLess(contrast_against_white("#fff6e5"), 4.5)
        for selector in (
            ".demo-eyebrow",
            ".demo-panel table caption",
            ".demo-open",
            ".demo-open:hover",
            ".demo-open:focus-visible",
        ):
            with self.subTest(selector=selector):
                color = declared_color(selector)
                self.assertIsNotNone(color, f"missing print color for {selector}")
                self.assertGreaterEqual(contrast_against_white(color), 4.5)

        # Color alone must not be the only way to identify the printed link.
        self.assertRegex(print_css, r"\.demo-open:hover,\s*\.demo-open:focus-visible\s*"
                                        r"\{[^{}]*text-decoration:\s*underline;")

    def test_absent_registered_comparison_shows_no_synthetic_chart(self):
        self.assertEqual(render_demo([]), "")
        home = _render_index([])
        self.assertNotIn("demo-panel", home)
        self.assertIn("No public analyses are available", home)

    def test_changed_evidence_identity_or_unit_fails_closed(self):
        original = comparison_entry()
        doc = json.loads(original["json_data"])
        for mutate in (
            lambda d: d["scientific_boundary"].update(m2_parity_admissible=True),
            lambda d: d["works"][0].update(candidate_id="unknown"),
            lambda d: d["measurements"][4].update(unit="words"),
            lambda d: d["measurements"][4].update(left="35%"),
            lambda d: d["measurements"][4].update(left=101),
        ):
            with self.subTest(mutator=mutate):
                changed = copy.deepcopy(doc)
                mutate(changed)
                entry = dict(original, json_data=json.dumps(changed))
                with self.assertRaises(ValueError):
                    render_demo([entry])

    def test_visible_titles_escape_markup(self):
        entry = comparison_entry()
        doc = json.loads(entry["json_data"])
        doc["works"][0]["title"] = "<script>steal()</script>"
        entry["json_data"] = json.dumps(doc)
        rendered = render_demo([entry])
        self.assertIn("&lt;script&gt;steal()&lt;/script&gt;", rendered)
        self.assertNotIn("<script>steal()", rendered)

    def test_homepage_presents_evidence_with_working_routes(self):
        home = _render_index([comparison_entry()])
        self.assertIn("site-masthead", home)
        self.assertIn("hero-stage", home)
        self.assertIn('id="demo-title"', home)
        self.assertIn('id="works"', home)
        self.assertIn('href="compare/"', home)
        self.assertIn('href="works/two-full-work-differences/"', home)
        self.assertEqual(home.count('<h1>'), 1)
        self.assertEqual(home.count('<script'), 1)
        self.assertIn('src="assets/evidence-filter.js"', home)
        self.assertIn("Print", HOME_CSS.replace("print", "Print"))  # has a print style

    def test_readme_links_to_expected_pages_without_fake_live_claim(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("https://drevendev.github.io/Scriptorium/", readme)
        self.assertRegex(readme, r"not a\s+claim that the public site is already live")
        self.assertIn("SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true", readme)
        self.assertIn("build/site/index.html", readme)


    def test_atlas_uses_four_retained_book_diagnostics_not_fake_parity(self):
        entry = benchmark_entry()
        rendered = render_research_atlas([entry])
        self.assertIn('id="research-atlas"', rendered)
        self.assertIn('113', rendered)
        self.assertIn('94', rendered)
        self.assertIn('19', rendered)
        self.assertIn('M2 · 0 / 5', rendered)
        self.assertIn('Not yet retained in Reader', rendered)
        self.assertEqual(rendered.count('class="atlas-book'), 5)
        parsed = RecordedHTML(rendered)
        for anchor in ('metrics-title', 'waves-metrics-title', 'silver-title',
                       'karamazov-title', 'works-title'):
            self.assertIn('evidence/fantlab/#' + anchor, parsed.links)
        self.assertNotIn('<script', rendered)
        home = _render_index([comparison_entry(), entry])
        self.assertIn('id="research-atlas"', home)
        self.assertEqual(home.count('<h1>'), 1)

    def test_atlas_rejects_parity_and_metric_drift(self):
        original = benchmark_entry()
        self.assertEqual(render_research_atlas([]), '')
        data = json.loads(original["json_data"])
        for mutate in (
            lambda d: d.update(m2_source_matched_pass_count=1),
            lambda d: d["entries"][0].update(exact_fantlab_input_identity="MATCHED"),
            lambda d: d["entries"][0].update(metric_rows_with_actual=0),
            lambda d: d["entries"].append(copy.deepcopy(d["entries"][0])),
        ):
            with self.subTest(mutate=mutate):
                altered = copy.deepcopy(data)
                mutate(altered)
                with self.assertRaises(ValueError):
                    render_research_atlas([dict(original, json_data=json.dumps(altered))])
        altered = copy.deepcopy(data)
        altered["entries"][0]["title"] = "<script>malicious()</script>"
        output = render_research_atlas([dict(original, json_data=json.dumps(altered))])
        self.assertIn("&lt;script&gt;malicious()&lt;/script&gt;", output)
        self.assertNotIn("<script>malicious()", output)
        self.assertIn("@media print", HOME_CSS)


if __name__ == "__main__":
    unittest.main()
