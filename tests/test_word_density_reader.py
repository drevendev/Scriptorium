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


    def _assert_probe_matches_frozen(self, html: str) -> None:
        import json
        frozen = json.loads(
            (ROOT / "benchmarks/fantlab/work270306-word-boundaries.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(frozen["epistemic_status"]["status"], "DIAGNOSTIC_ONLY")
        self.assertEqual(frozen["epistemic_status"]["fantlab_analyzer_input_identity"], "UNKNOWN")
        self.assertFalse(frozen["epistemic_status"]["m2_parity_admissible"])
        pairs = re.findall(r'data-probe="([^"]+)" value="([^"]+)"', html)
        expected = {
            f'{variant["id"]}:{key}': str(variant[key])
            for variant in frozen["probe"]["variants"]
            for key in ("word_count", "delta_from_current_words", "delta_per_1000_current_words")
        }
        self.assertEqual(len(pairs), 21)
        self.assertEqual(dict(pairs), expected)
        meta = dict(re.findall(r'data-probe-meta="([^"]+)" value="([^"]+)"', html))
        self.assertEqual(meta, {
            "normalized_characters_including_spaces": str(frozen["source"]["normalized_character_count_including_spaces"]),
            "replayed_revision_count": str(frozen["evidence"]["replayed_revision_count"]),
        })
        self.assertIn(frozen["source"]["normalized_sha256"], html)
        self.assertIn(f'/actions/runs/{frozen["evidence"]["workflow_run_id"]}', html)

    def test_full_book_boundary_experiment_is_real_and_accessible(self):
        html = (ROOT / "word-density.html").read_text(encoding="utf-8")
        self._assert_probe_matches_frozen(html)
        for text in ('id="boundary-experiment"', 'id="boundary-title"', 'class="probe-bars"',
                     'role="region"', 'tabindex="0"', 'scope="row"',
                     'prefers-reduced-motion', 'forced-colors', 'M2: 0/5',
                     'DIAGNOSTIC_ONLY', 'UNKNOWN', 'нельзя складывать'):
            self.assertIn(text, html)
        self.assertNotIn("<script", html)
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./word-density.html"', home)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("(word-density.html#boundary-experiment)", readme)
        ci = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn('cp word-density.html build/branch-root-preview/word-density.html', ci)
        self.assertIn('test -s build/branch-root-preview/word-density.html', ci)

    def test_single_digit_full_book_probe_corruption_is_detected(self):
        html = (ROOT / "word-density.html").read_text(encoding="utf-8")
        corrupted = html.replace(
            'data-probe="split_ascii_hyphen:word_count" value="270969"',
            'data-probe="split_ascii_hyphen:word_count" value="270968"',
        )
        self.assertNotEqual(html, corrupted)
        with self.assertRaises(AssertionError):
            self._assert_probe_matches_frozen(corrupted)

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
