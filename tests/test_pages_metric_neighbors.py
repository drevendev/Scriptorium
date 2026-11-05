"""Regression checks for evidence-bound measured-neighbor Reader navigation."""
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReaderMetricNeighborsTests(unittest.TestCase):
    def test_accessible_fallback_and_static_science_boundary(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        js = (ROOT / "assets/pages-reader.js").read_text(encoding="utf-8")
        css = (ROOT / "assets/pages-reader.css").read_text(encoding="utf-8")
        self.assertIn('id="measured-neighbors" aria-labelledby="neighbor-title"', html)
        self.assertIn('id="neighbor-status" role="status" aria-live="polite"', html)
        self.assertIn('id="neighbor-list"', html)
        self.assertIn("стартовая пара, не вычисленная рекомендация", html)
        self.assertIn("Это не авторский почерк, не оценка качества текста", html)
        self.assertIn("function rankMetricNeighbors(anchorBook,books)", js)
        self.assertIn("updateMetricNeighbors(book);", js)
        self.assertIn("book.text_status===\"measured\"", js)
        self.assertIn("neighborProfiles.every", js)
        self.assertNotIn("innerHTML", js)
        self.assertIn(".neighbor-panel li a", css)
        self.assertIn("min-height:44px", css)
        self.assertIn("@media print { .neighbor-panel", css)

    @unittest.skipUnless(shutil.which("node"), "Node unavailable: structural check only")
    def test_shipped_js_ranking_and_links(self):
        for command in (
            ["node", "--check", str(ROOT / "assets/pages-reader.js")],
            ["node", str(ROOT / "tests/pages_metric_neighbors_smoke.cjs")],
        ):
            run = subprocess.run(
                command, cwd=ROOT, text=True, capture_output=True, check=False
            )
            self.assertEqual(run.returncode, 0, run.stdout + "\n" + run.stderr)


if __name__ == "__main__":
    unittest.main()
