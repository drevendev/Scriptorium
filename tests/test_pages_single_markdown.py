"""Source-free single-edition Markdown Reader contract and real Node behavior."""
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Buttons(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []
    def handle_starttag(self, tag, attrs):
        if tag == "button":
            self.buttons.append(dict(attrs))


class ReaderBookMarkdownTests(unittest.TestCase):
    def test_button_is_opt_in_and_disabled_until_verified(self):
        parser = Buttons()
        parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        matches = [b for b in parser.buttons if b.get("id") == "export-markdown-button"]
        self.assertEqual(len(matches), 1)
        self.assertIn("disabled", matches[0])
        js = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        for fragment in (
            'const singleMarkdownButton = el("export-markdown-button")',
            "function serializeBookMarkdown(book)",
            "function exportSelectedMarkdown()",
            "verify(data);",
            'singleMarkdownButton.addEventListener("click",exportSelectedMarkdown)',
            'catalogReset,one,search,out,singleMarkdownButton,leftSelect,rightSelect',
            'scientific_claim:"DIAGNOSTIC_ONLY"',
            'fantlab_input_identity:"UNKNOWN",m2_source_matched:0',
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, js)
        self.assertNotIn("innerHTML", js)
        self.assertNotIn("sendBeacon", js)

    @unittest.skipUnless(shutil.which("node"), "Node.js unavailable")
    def test_shipped_serializer_uses_ten_pinned_books(self):
        for command in (
            ["node", "--check", "assets/pages-reader.js"],
            ["node", "tests/pages_single_markdown_smoke.cjs"],
        ):
            result = subprocess.run(command, cwd=ROOT, text=True,
                                    capture_output=True, timeout=25, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
