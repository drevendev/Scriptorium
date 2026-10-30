"""End-to-end exported CSV contract for all ten measured Russian Reader editions."""
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LibraryExportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        if tag == "button":
            self.buttons.append(dict(attrs))


class LibraryCsvExportTests(unittest.TestCase):
    def test_source_verified_button_and_no_js_provenance_fallback(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parser = LibraryExportParser()
        parser.feed(html)
        buttons = [b for b in parser.buttons if b.get("id") == "library-export-csv"]
        self.assertEqual(len(buttons), 1)
        self.assertIn("disabled", buttons[0])
        self.assertIn("Скачать все 269 полей (CSV)", html)
        self.assertIn('id="evidence-source"', html)
        self.assertIn("Без JavaScript доступны карточки", html)
        js = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        self.assertIn("function serializeLibraryCsv(doc)", js)
        self.assertIn("verify(doc);", js)
        self.assertIn('libraryCsvButton.addEventListener("click",exportLibraryCsv)', js)
        self.assertIn("pairCsvButton,libraryCsvButton,chartSortButton", js)
        self.assertNotIn("innerHTML", js)
        self.assertNotIn("sendBeacon", js)

    @unittest.skipUnless(shutil.which("node"), "Node.js unavailable")
    def test_full_pinned_catalogue_csv_is_exercised_in_node(self):
        result = subprocess.run(
            ["node", "tests/pages_library_csv_smoke.cjs"],
            cwd=ROOT, capture_output=True, text=True, check=False, timeout=25
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
