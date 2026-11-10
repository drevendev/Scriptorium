"""Source-level acceptance of voice table contrast/focus; not browser acceptance."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def rule(css, selector):
    match = re.search(re.escape(selector) + r"\s*\{([^}]+)\}", css)
    if match is None:
        raise AssertionError("missing scoped stylesheet rule: " + selector)
    return dict((key.strip(), value.strip()) for key, value in
                (item.split(":", 1) for item in match[1].split(";") if ":" in item))


def contrast(left, right):
    def luminance(value):
        value = value.lstrip("#")
        components = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        return sum(weight * (c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4)
                   for c, weight in zip(components, (.2126, .7152, .0722)))
    lo, hi = sorted((luminance(left), luminance(right)))
    return (hi + .05) / (lo + .05)


class Regions(HTMLParser):
    def __init__(self):
        super().__init__()
        self.regions = []
        self.captions = 0
        self.tables = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "scroll-table" in attrs.get("class", "").split():
            self.regions.append(attrs)
        self.tables += tag == "table"
        self.captions += tag == "caption"


class VoiceTableAccessibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        cls.html = (ROOT / "voice/index.html").read_text(encoding="utf-8")
        cls.colors = dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{6})", cls.css))

    def test_actual_voice_header_colors_do_not_inherit_white_on_pale(self):
        foreground = rule(self.css, ".voice-wrap .scroll-table thead th")["color"]
        background = rule(self.html, ".scroll-table thead th")["background"]
        self.assertEqual(foreground, "var(--ink)")
        self.assertEqual(background, "var(--wash)")
        self.assertGreaterEqual(contrast(self.colors["--ink"], self.colors["--wash"]), 4.5)
        self.assertLess(contrast("#ffffff", self.colors["--wash"]), 1.2)
        # The fix is scoped, not a change to the normal dark-header tables.
        self.assertEqual(rule(self.css, "\nthead th")["color"], "white")

    def test_scroll_regions_and_source_disclosures_have_explicit_focus(self):
        selector = ".voice-wrap .scroll-table:focus-visible, .voice-wrap summary:focus-visible"
        declarations = rule(self.css, selector)
        self.assertEqual(declarations["outline"], "3px solid var(--green-deep)")
        self.assertEqual(declarations["outline-offset"], "3px")
        self.assertGreaterEqual(contrast(self.colors["--green-deep"], self.colors["--paper"]), 3)
        self.assertRegex(self.css, r"@media\(forced-colors:active\)\s*\{\s*"
                         + re.escape(selector) + r"\s*\{\s*outline-color:Highlight;")

    def test_actual_no_js_tables_keep_names_captions_and_keyboard_entry(self):
        document = Regions()
        document.feed(self.html)
        self.assertGreaterEqual(len(document.regions), 4)
        self.assertEqual(document.tables, document.captions)
        for attrs in document.regions:
            with self.subTest(label=attrs.get("aria-label")):
                self.assertEqual(attrs.get("tabindex"), "0")
                self.assertEqual(attrs.get("role"), "region")
                self.assertTrue(attrs.get("aria-label") or attrs.get("aria-labelledby"))


if __name__ == "__main__":
    unittest.main()
