"""Unit-label regressions; historical numeric values must not change."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from scriptorium import frozen_diagnostic_report as report

MEAN_UNITS = {
    "fantlab.general.mean_word_length_chars": "characters / word",
    "fantlab.general.mean_sentence_length_chars": "characters / sentence",
    "fantlab.dialogue.mean_narration_sentence_length_chars": "characters / sentence",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars": "characters / sentence",
}


class FrozenDiagnosticUnitTests(unittest.TestCase):
    def test_mean_length_denominators(self):
        for metric_id, expected in MEAN_UNITS.items():
            with self.subTest(metric_id=metric_id):
                self.assertEqual(report._unit(metric_id), expected)

    def test_other_units_are_not_reclassified(self):
        controls = {
            "fantlab.general.characters": "characters",
            "fantlab.general.words": "word tokens",
            "fantlab.dialogue.share_percent": "% (delta: percentage points)",
            "fantlab.punctuation.dash.per_1000_words": "events / 1,000 words",
            "fantlab.extension.sentence_length_chars": "characters",
            "fantlab.unknown": "unspecified in artifact",
        }
        for metric_id, expected in controls.items():
            with self.subTest(metric_id=metric_id):
                self.assertEqual(report._unit(metric_id), expected)

    def test_canonical_html_keeps_four_denominators_and_frozen_bytes(self):
        path = Path(__file__).resolve().parents[1] / "benchmarks/fantlab/work270306-wikisource-diagnostic.json"
        raw = path.read_bytes()
        self.assertEqual(
            hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
            "0d5e420abb45e2b9e178df75a479ab7cdd5a4150",
        )
        artifact = json.loads(raw)
        before = copy.deepcopy(artifact)
        rendered = report.render_html(artifact)
        self.assertEqual(rendered.count("characters / word"), 1)
        self.assertEqual(rendered.count("characters / sentence"), 3)
        self.assertEqual(rendered.count('scope="row"'), 28)
        self.assertNotIn("unspecified in artifact", rendered)
        self.assertEqual(artifact, before)
        self.assertEqual(report.render_html(artifact), rendered)
        self.assertFalse(artifact["epistemic_status"]["m2_parity_admissible"])


if __name__ == "__main__":
    unittest.main()
