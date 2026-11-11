"""Local offline HTML evidence must be complete and internally consistent."""
from __future__ import annotations

import copy
from decimal import Decimal
import unittest

from scriptorium.analyze import build_local_analysis, render_html
from scriptorium.metrics import METRIC_DEFINITIONS

TEXT = "Вечерний ветер. — Привет! — сказал герой."


class LocalHtmlEvidenceContractTests(unittest.TestCase):
    def setUp(self):
        self.artifact = build_local_analysis(TEXT.encode("utf-8"))

    def test_valid_short_and_empty_reports_remain_source_free_and_repeatable(self):
        for text in (TEXT.encode("utf-8"), b""):
            with self.subTest(length=len(text)):
                artifact = build_local_analysis(text)
                first = render_html(artifact, title="Literary report")
                self.assertEqual(first, render_html(copy.deepcopy(artifact), title="Literary report"))
                self.assertIn("Punctuation at a glance", first)
                self.assertIn("FantLab", first)
                self.assertNotIn(TEXT, first)
                self.assertEqual(first.count('class="metric-id"'), 29)
        unknown = render_html(build_local_analysis(b""))
        self.assertIn("Unavailable", unknown)

    def test_valid_dictionary_identity_and_small_decimal_are_preserved(self):
        artifact = build_local_analysis(
            TEXT.encode("utf-8"),
            dictionary_words=("ветер", "герой"),
            dictionary_profile="private-dict-v1",
        )
        artifact["metrics"]["fantlab.punctuation.comma.per_1000_words"]["value"] = Decimal("1E-30")
        html = render_html(artifact)
        self.assertIn("private-dict-v1", html)
        self.assertIn("1E-30 occurrences / 1,000 words", html)
        self.assertIn('data-nonzero="true"', html)

    def test_missing_or_extra_metric_rows_fail_closed(self):
        cases = [
            lambda a: a["metrics"].pop("fantlab.general.words"),
            lambda a: a["metrics"].update({"unreviewed.metric": {"value": 7}}),
            lambda a: a["metrics"].update({"fantlab.unproven.new": {
                "value": 7, "unit": "events", "compatibility_status": "inferred",
                "definition_evidence": "unsupported",
            }}),
            lambda a: a["metrics"].update({"scriptorium.other.unknown": {
                "value": 7, "unit": "events", "compatibility_status": "extension",
            }}),
            lambda a: a["metrics"].update({"fantlab.general.words": None}),
        ]
        for mutate in cases:
            with self.subTest(mutation=cases.index(mutate)):
                artifact = copy.deepcopy(self.artifact)
                mutate(artifact)
                with self.assertRaises(ValueError):
                    render_html(artifact)

    def test_future_namespaced_extension_stays_visible_and_escaped(self):
        artifact = copy.deepcopy(self.artifact)
        artifact["metrics"]["scriptorium.new.<future>"] = {
            "value": 3, "unit": "events",
            "compatibility_status": "extension",
            "definition_evidence": "scriptorium_extension",
        }
        html = render_html(artifact)
        self.assertEqual(html.count('class="metric-id"'), 30)
        self.assertIn("scriptorium.new.&lt;future&gt;", html)
        self.assertNotIn("<future>", html)
        self.assertIn("<h2>Other</h2>", html)

    def test_provenance_and_representativeness_must_agree(self):
        cases = [
            lambda a: a["source"].update(raw_sha256="not-a-digest"),
            lambda a: a["source"].update(normalized_sha256="A" * 64),
            lambda a: a["source"].update(byte_count=True),
            lambda a: a["source"].update(normalized_character_count=-1),
            lambda a: a["source"].update(normalized_character_count=999),
            lambda a: a["source"].update(source_text_embedded=True),
            lambda a: a["representativeness"].update(meets_calibration_threshold=True),
            lambda a: a["representativeness"].update(calibration_threshold_characters=12),
            lambda a: a.update(metric_contract_id="unverified"),
            lambda a: a["analyzer"]["profiles"].update(metrics=None),
            lambda a: a["analyzer"].update(dependencies={}),
            lambda a: a["analyzer"].update(scriptorium_revision=123),
        ]
        for mutate in cases:
            with self.subTest(mutation=cases.index(mutate)):
                artifact = copy.deepcopy(self.artifact)
                mutate(artifact)
                with self.assertRaises(ValueError):
                    render_html(artifact)

    def test_metric_values_units_evidence_and_raw_counts_fail_closed(self):
        cases = [
            lambda a: a["metrics"]["fantlab.general.words"].update(value=True),
            lambda a: a["metrics"]["fantlab.general.words"].update(value=float("nan")),
            lambda a: a["metrics"]["fantlab.general.words"].update(compatibility_status="reproduced"),
            lambda a: a["metrics"]["scriptorium.general.sentences"].update(compatibility_status="inferred"),
            lambda a: a["metrics"]["fantlab.general.words"].update(unit=None),
            lambda a: a["metrics"]["fantlab.general.words"].update(definition_evidence=""),
            lambda a: a["metrics"]["fantlab.punctuation.comma.per_1000_words"].update(raw_count=True),
            lambda a: a["metrics"]["fantlab.punctuation.comma.per_1000_words"].update(raw_count=-1),
        ]
        for mutate in cases:
            with self.subTest(mutation=cases.index(mutate)):
                artifact = copy.deepcopy(self.artifact)
                mutate(artifact)
                with self.assertRaises(ValueError):
                    render_html(artifact)

    def test_registered_metric_units_and_evidence_cannot_be_relabelled(self):
        self.assertEqual(set(METRIC_DEFINITIONS), set(self.artifact["metrics"]))
        for metric_id, expected in METRIC_DEFINITIONS.items():
            with self.subTest(registered_metric=metric_id):
                row = self.artifact["metrics"][metric_id]
                self.assertEqual(
                    (row["unit"], row["definition_evidence"], row["compatibility_status"]),
                    expected,
                )
        # Nonempty, plausible-looking declarations previously passed and could
        # cause the report to present counts as percentages or false evidence.
        drift = (
            ("fantlab.general.words", "unit", "percent"),
            ("scriptorium.general.sentences", "unit", "words"),
            ("fantlab.vocabulary.unique_words", "definition_evidence", "public_surface"),
            ("fantlab.dialogue.author_text_inside_dialogue_percent", "unit", "characters"),
            ("fantlab.punctuation.comma.per_1000_words", "unit", "percent"),
            ("fantlab.punctuation.dash.per_1000_words", "definition_evidence", "scriptorium_extension"),
        )
        for metric_id, key, replacement in drift:
            with self.subTest(metric=metric_id, field=key):
                artifact = copy.deepcopy(self.artifact)
                artifact["metrics"][metric_id][key] = replacement
                with self.assertRaisesRegex(ValueError, "registered metric contract mismatch"):
                    render_html(artifact)
        # An unavailable value still has a defined unit; null is not a bypass.
        empty = build_local_analysis(b"")
        empty["metrics"]["fantlab.punctuation.comma.per_1000_words"]["unit"] = "percent"
        with self.assertRaisesRegex(ValueError, "registered metric contract mismatch"):
            render_html(empty)

    def test_invalid_dictionary_provenance_fails_closed(self):
        original = build_local_analysis(
            TEXT.encode("utf-8"),
            dictionary_words=("вечерний",),
            dictionary_profile="dict-v1",
        )
        for mutate in (
            lambda d: d.update(profile=""),
            lambda d: d.update(lexeme_count=True),
            lambda d: d.update(normalized_lexemes_sha256="0"),
        ):
            artifact = copy.deepcopy(original)
            mutate(artifact["analyzer"]["dependencies"]["vocabulary_dictionary"])
            with self.assertRaises(ValueError):
                render_html(artifact)


if __name__ == "__main__":
    unittest.main()
