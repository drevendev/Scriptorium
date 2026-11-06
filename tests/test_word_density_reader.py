"""Fail-closed root Reader case study against the canonical frozen diagnostic."""
from __future__ import annotations

import re
from pathlib import Path
import unittest

from scriptorium.benchmark_metric_matrix import build_metric_matrix
from scriptorium.word_gap import build_word_density_diagnostic

ROOT = Path(__file__).resolve().parents[1]
VALUES = (
    "expected_characters",
    "actual_characters",
    "expected_words",
    "actual_words",
    "fantlab_words_per_1000_characters",
    "scriptorium_words_per_1000_characters",
    "density_gap_per_1000_characters",
    "length_adjusted_word_residual",
)


class WordDensityReaderTests(unittest.TestCase):
    def _assert_matches_frozen(self, html: str) -> None:
        pairs = re.findall(
            r'<data data-diagnostic="([^"]+)" value="([^"]+)">',
            html,
        )
        self.assertEqual(len(pairs), len(VALUES), "page must have every exact data cell")
        self.assertEqual({key for key, _ in pairs}, set(VALUES))
        anna = next(
            entry for entry in build_word_density_diagnostic(build_metric_matrix(ROOT))["entries"]
            if entry["candidate_id"] == "tolstoy-anna-karenina-ru"
        )
        self.assertEqual(anna["status"], "DIAGNOSTIC_ONLY")
        self.assertEqual(
            {key: value for key, value in pairs},
            {key: str(anna[key]) for key in VALUES},
            "every public number must match the current source-bound diagnostic",
        )

    def test_public_case_study_uses_real_frozen_counts(self):
        html = (ROOT / "word-density.html").read_text(encoding="utf-8")
        self._assert_matches_frozen(html)
        for claim in (
            'lang="ru"', 'href="#main"', 'role="region"', 'tabindex="0"',
            'scope="col"', 'scope="row"', 'prefers-reduced-motion',
            "DIAGNOSTIC_ONLY", "M2: 0/5", "UNKNOWN", "NOT_RUN",
            "scriptorium word-gap", "1000 символов",
        ):
            self.assertIn(claim, html)
        self.assertNotIn("<script", html, "static result must work without scripts")
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./word-density.html"', homepage)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("(word-density.html)", readme)

    def test_single_digit_corruption_is_detected(self):
        html = (ROOT / "word-density.html").read_text(encoding="utf-8")
        corrupted = html.replace(
            'data-diagnostic="density_gap_per_1000_characters" value="8.292695"',
            'data-diagnostic="density_gap_per_1000_characters" value="8.292696"',
        )
        self.assertNotEqual(html, corrupted)
        with self.assertRaises(AssertionError):
            self._assert_matches_frozen(corrupted)


if __name__ == "__main__":
    unittest.main()
