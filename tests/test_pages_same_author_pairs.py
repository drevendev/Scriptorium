"""Same-author Reader launch links must target independently measured Russian editions.

These are descriptive pair comparisons, NOT M3 author-profile evidence.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "tolstoy": ("anna", "resurrection", "Лев Толстой"),
    "grin": ("waves", "road", "Александр Грин"),
    "dostoevsky": ("karamazov", "humiliated", "Фёдор Достоевский"),
}
METRIC = "fantlab.dialogue.share_percent"


class SameAuthorLinks(HTMLParser):
    def __init__(self, content: str):
        super().__init__()
        self.links = {}
        self.navs = []
        self.feed(content)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "nav" and values.get("class") == "pair-starters":
            self.navs.append(values)
        if tag == "a" and "data-same-author-pair" in values:
            key = values["data-same-author-pair"]
            if key in self.links:
                raise AssertionError("Duplicate same-author starter: " + key)
            self.links[key] = values.get("href", "")


class TestSameAuthorLaunches(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        cls.js = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        doc = json.loads((ROOT / "assets/evidence-snapshot.json").read_text(encoding="utf-8"))
        cls.books = {b["key"]: b for b in doc["books"] if b["text_status"] == "measured"}
        cls.links = SameAuthorLinks(cls.html)

    def test_only_source_verified_pairs_are_advertised(self) -> None:
        self.assertEqual(len(self.links.navs), 1)
        self.assertEqual(self.links.navs[0].get("aria-label"),
                         "Готовые сравнения книг одного автора")
        self.assertEqual(set(self.links.links), set(EXPECTED))
        self.assertEqual(len(self.books), 10)

        for group, (left_id, right_id, author) in EXPECTED.items():
            with self.subTest(group=group):
                url = urlsplit(self.links.links[group])
                args = parse_qs(url.query, strict_parsing=True)
                self.assertEqual(url.path, "")
                self.assertEqual(url.fragment, "pairs")
                self.assertEqual(args, {"left": [left_id], "right": [right_id],
                                        "pair_metric": [METRIC]})
                left, right = self.books[left_id], self.books[right_id]
                self.assertNotEqual(left_id, right_id)
                self.assertEqual(left["display_author"], author)
                self.assertEqual(right["display_author"], author)
                self.assertEqual(left["original_language"], "ru")
                self.assertEqual(right["original_language"], "ru")
                self.assertEqual(left["language"], "ru")
                self.assertEqual(right["language"], "ru")
                self.assertIsNone(left["translator"])
                self.assertIsNone(right["translator"])
                self.assertNotEqual(left["edition_id"], right["edition_id"])
                self.assertNotEqual(left["source_sha256"], right["source_sha256"])
                for book in (left, right):
                    self.assertRegex(book["source_sha256"], r"^[a-f0-9]{64}$")
                    value = next((m["actual"] for m in book["metrics"] if m["id"] == METRIC), None)
                    self.assertIsInstance(value, (int, float))
                for profile in ("metrics", "normalization", "dialogue", "vocabulary",
                                "punctuation"):
                    self.assertEqual(left["profiles"][profile], right["profiles"][profile])

    def test_accessibility_and_degraded_fallback(self) -> None:
        self.assertIn(".pair-starters a:focus-visible", self.css)
        self.assertIn("min-height:64px", self.css)
        self.assertIn("@media (max-width:780px) { .pair-starters { grid-template-columns:1fr; } }",
                      self.css)
        self.assertIn("Без JavaScript остаётся начальная статическая таблица", self.html)
        self.assertIn('id="pair-rows"', self.html)
        self.assertIn("function pairFromUrl() {", self.js)
        self.assertIn('getBook(left) && getBook(right) && left !== right', self.js)
        self.assertIn("function selectPair(left, right, addHistory=false)", self.js)
        self.assertNotIn("innerHTML", self.js)


if __name__ == "__main__":
    unittest.main()
