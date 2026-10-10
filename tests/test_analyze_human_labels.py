"""Offline report readability without changing scientific metric identity."""
from __future__ import annotations

import unittest

from scriptorium.analyze import build_local_analysis, render_html
from scriptorium.metric_labels import METRIC_LABELS


class OfflineReadableMetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact = build_local_analysis("Лес шумит. Солнце светит!\n— Здравствуй, — сказала она.".encode("utf-8"))

    def test_all_current_metric_ids_have_clear_labels(self):
        self.assertEqual(len(self.artifact["metrics"]), 29)
        self.assertEqual(set(self.artifact["metrics"]), set(METRIC_LABELS))
        page = render_html(self.artifact)
        for metric_id, label in METRIC_LABELS.items():
            with self.subTest(metric=metric_id):
                self.assertIn(f'data-label="{label}"', page)
                self.assertIn(f'<span class="metric-label">{label}</span>', page)
                self.assertIn(f'aria-label="{label}, metric ID {metric_id}"', page)
                self.assertIn(f'<code class="metric-id">{metric_id}</code>', page)

    def test_names_are_readable_without_css_or_javascript(self):
        page = render_html(self.artifact)
        self.assertIn('Mean sentence length', page)
        self.assertIn('Dialogue character share', page)
        self.assertIn('Distinct surface words', page)
        self.assertIn('scope="row"', page)
        self.assertNotIn('<script', page.lower())
        self.assertIn('not parity claims', page)

    def test_at_a_glance_uses_real_engine_values_and_units(self):
        from scriptorium.analyze import _format_value
        page = render_html(self.artifact)
        self.assertIn('<h2 id="highlights-heading">At a glance</h2>', page)
        for label, metric_id in (
            ('Words', 'fantlab.general.words'),
            ('Sentences · Scriptorium', 'scriptorium.general.sentences'),
            ('Dialogue share', 'fantlab.dialogue.share_percent'),
            ('Distinct surface words', 'fantlab.vocabulary.unique_words'),
        ):
            with self.subTest(metric=metric_id):
                self.assertIn(f'<dt>{label}</dt>', page)
                self.assertIn(f'<dd>{_format_value(self.artifact["metrics"][metric_id]["value"])}', page)
        self.assertIn('grid-template-columns: repeat(auto-fit', page)

    def test_missing_highlight_displays_unavailable_not_zero(self):
        import copy
        data = copy.deepcopy(self.artifact)
        data['metrics']['fantlab.dialogue.share_percent']['value'] = None
        page = render_html(data)
        self.assertIn('<dt>Dialogue share</dt><dd>Unavailable', page)
        self.assertNotIn('<dt>Dialogue share</dt><dd>0', page)

    def test_unknown_extension_label_is_escaped_and_identified(self):
        data = dict(self.artifact)
        metrics = dict(self.artifact["metrics"])
        metrics['scriptorium.other.<img>'] = {
            "value": 1, "unit": "items", "compatibility_status": "extension",
            "definition_evidence": "scriptorium_extension",
        }
        data["metrics"] = metrics
        page = render_html(data)
        self.assertIn('scriptorium.other.&lt;img&gt;', page)
        self.assertNotIn('<img>', page)
        self.assertGreaterEqual(page.count('scriptorium.other.&lt;img&gt;'), 3)

    def test_rendering_does_not_mutate_exported_metrics(self):
        import json
        before = json.dumps(self.artifact, ensure_ascii=False, sort_keys=True)
        first = render_html(self.artifact)
        self.assertEqual(first, render_html(self.artifact))
        self.assertEqual(before, json.dumps(self.artifact, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
