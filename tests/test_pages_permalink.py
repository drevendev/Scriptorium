"""Branch Pages permalink behavior: deterministic edition routing, safe fallbacks."""
from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AnchorReader(HTMLParser):
    def __init__(self, html: str):
        super().__init__()
        self.links: list[dict[str, str]] = []
        self.feed(html)

    def handle_starttag(self, tag: str, attrs):
        if tag == "a":
            self.links.append(dict(attrs))


class PagesEditionPermalinkTests(unittest.TestCase):
    def test_six_work_cards_have_source_fallback_and_one_share_link(self):
        catalog = json.loads((ROOT / "assets/evidence-snapshot.json").read_text(encoding="utf-8"))
        measured = {b["key"] for b in catalog["books"] if b["text_status"] == "measured"}
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        links = AnchorReader(html).links
        cards = [a for a in links if "data-book" in a]
        self.assertEqual(len(cards), 6)
        self.assertEqual({a["data-book"] for a in cards}, measured)
        for a in cards:
            self.assertTrue(a["href"].startswith(
                "https://github.com/drevendev/Scriptorium/blob/master/"
            ))
        self.assertEqual(
            [a["href"] for a in links if a.get("id") == "share-work"],
            ["?book=anna#measurements"],
        )
        self.assertRegex(html, r'id="measurements-title" tabindex="-1"')
        self.assertIn("M2: 0/5", html)
        css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn("#measurements-title:focus-visible", css)
        self.assertIn(".permalink-help a { display:inline-flex; min-height:44px", css)

    def test_edition_routes_use_allowlisted_data_not_arbitrary_paths(self):
        js = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        for phrase in (
            'new URLSearchParams(window.location.search).get("book")',
            'return getBook(requested) ? requested : "anna"',
            'const book = getBook(key)',
            'if (!book) return',
            'url.searchParams.set("book", key)',
            'url.hash = "measurements"',
            'window.history.pushState(null, "", url)',
            'window.addEventListener("popstate",()=>{',
            'selectBook(bookFromUrl());',
            'selectPair(left,right);',
            'selectBook(bookFromUrl())',
            'direct.href = "?book=" + encodeURIComponent(key) + "#measurements"',
            'el("measurements-title").focus({preventScroll:true})',
            'event.ctrlKey || event.metaKey',
        ):
            with self.subTest(fragment=phrase):
                self.assertIn(phrase, js)
        self.assertNotIn("innerHTML", js)
        self.assertNotIn("fetch(window.location", js)

    @unittest.skipUnless(shutil.which("node"), "Node.js not present; structural checks still run")
    def test_real_routing_functions_in_node_without_dom_packages(self):
        for command in (
            ["node", "--check", str(ROOT / "assets/pages-reader.js")],
            ["node", str(ROOT / "tests/pages_permalink_smoke.cjs")],
        ):
            result = subprocess.run(command, cwd=ROOT, text=True,
                                    capture_output=True, timeout=20, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
