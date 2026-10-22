"""Reader site appearance must preserve working, accessible HTML and honest evidence."""
import unittest

from scriptorium.site_renderer import _SITE_CSS, _page, _render_index


class LiteraryReaderThemeTests(unittest.TestCase):
    def test_real_navigation_and_source_honesty(self):
        entry = {
            "render_mode": "frozen_diagnostic",
            "slug": "a-frozen-work",
            "entry_id": "a-work-v1",
            "title": "<Read & Learn>",
            "author": "A. Writer",
            "work_title": "A Novel",
            "publication_status": "diagnostic",
            "compatibility_claim": "inferred",
            "benchmark_admissibility": "diagnostic_only",
            "corpus_admissibility": "not_admissible",
            "metric_count": 28,
        }
        page = _render_index([entry])
        self.assertIn('href="works/a-frozen-work/"', page)
        self.assertIn('href="#works"', page)
        self.assertIn('&lt;Read &amp; Learn&gt;', page)
        self.assertNotIn('<Read & Learn>', page)
        self.assertIn('diagnostic evidence is not parity', page)
        self.assertIn('inferred measurement is not verified FantLab parity', page)
        self.assertIn('Reader CLI', page)
        self.assertEqual(page.count('<h1>'), 1)
        self.assertEqual(page.count('id="works"'), 1)
        self.assertIn('<header class="hero">', page)
        self.assertIn('aria-labelledby="reading-guide-title"', page)

    def test_empty_state_is_explained_without_fake_results(self):
        page = _render_index([])
        self.assertIn('No public analyses are available in this build.', page)
        self.assertNotIn('Explore the 28-metric', page)
        self.assertIn('Published work and evidence', page)

    def test_keyboard_mobile_print_and_no_remote_font(self):
        page = _page("Reader", "assets/site.css", '<main id="main-content"></main>')
        self.assertIn('name="viewport"', page)
        self.assertIn('href="#main-content"', page)
        self.assertIn('<title>Reader</title>', page)
        for required in (
            '.skip-link:not(:focus)',
            ':focus-visible',
            'min-height: 44px',
            'overflow-x: auto',
            '@media (max-width: 720px)',
            '@media (prefers-color-scheme: dark)',
            '@media (prefers-reduced-motion: reduce)',
            '@media (forced-colors: active)',
            '@media print',
            'break-inside: avoid',
            'grid-template-columns: 1fr',
        ):
            with self.subTest(required=required):
                self.assertIn(required, _SITE_CSS)
        self.assertNotIn('@import', _SITE_CSS)
        self.assertNotIn('url(', _SITE_CSS)


if __name__ == "__main__":
    unittest.main()
