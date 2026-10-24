"""Regression and scientific-boundary tests for the homepage real-work showcase."""
from __future__ import annotations

import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

from scriptorium import site_work_comparison
from scriptorium.site_home_showcase import HOME_CSS, render_demo
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
        self.assertEqual(sum(tag == "h2" for tag, _ in parsed.start_tags), 1)
        self.assertNotIn("<script", result)
        self.assertNotIn("fetch(", result)

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
        self.assertIn("not a claim that the public site is already live", readme)
        self.assertIn("SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true", readme)
        self.assertIn("build/site/index.html", readme)


if __name__ == "__main__":
    unittest.main()
