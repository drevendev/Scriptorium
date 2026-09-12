import json
from pathlib import Path
import unittest

from scriptorium.benchmark import build_comparison
from scriptorium.dialogue import (
    DIALOGUE_PROFILE,
    author_remark_spans,
    dialogue_spans,
    narration_spans,
    paragraph_spans,
)
from scriptorium.metrics import SCHEMA_VERSION, analyze_deterministic_metrics
from scriptorium.text import TextSpan, normalize_text


class DialogueSpanTests(unittest.TestCase):
    def test_paragraph_dialogue_detection_and_offsets(self):
        text = (
            "  Нарратив.\r\n"
            "— Привет, — сказал он. — Пока.\r\n"
            " – Второй.\n"
            "- Третий.\n"
            "—Без пробела не диалог."
        )
        normalized = normalize_text(text)

        self.assertEqual(
            dialogue_spans(text),
            (
                TextSpan("— Привет, — сказал он. — Пока.", 12, 42),
                TextSpan("– Второй.", 44, 53),
                TextSpan("- Третий.", 54, 63),
            ),
        )
        self.assertEqual(
            narration_spans(text),
            (
                TextSpan("Нарратив.", 2, 11),
                TextSpan("—Без пробела не диалог.", 64, 87),
            ),
        )
        for span in paragraph_spans(text):
            self.assertEqual(normalized[span.start:span.end], span.text)

    def test_only_literal_lf_creates_paragraph_boundaries(self):
        text = "Автор\u2028— Реплика\u0085– Ответ\x0b- Третий"
        normalized = normalize_text(text)
        expected = (TextSpan(normalized, 0, len(normalized)),)

        self.assertEqual(paragraph_spans(text), expected)
        self.assertEqual(narration_spans(text), expected)
        self.assertEqual(dialogue_spans(text), ())

    def test_author_remark_segments_alternate_after_internal_separators(self):
        text = "— Привет, — сказал он. — Пока, — добавил он."
        normalized = normalize_text(text)
        remarks = author_remark_spans(text)

        self.assertEqual(
            remarks,
            (
                TextSpan("сказал он.", 12, 22),
                TextSpan("добавил он.", 33, 44),
            ),
        )
        for span in remarks:
            self.assertEqual(normalized[span.start:span.end], span.text)

    def test_quoted_speech_without_paragraph_dash_is_not_dialogue(self):
        self.assertEqual(dialogue_spans("«Привет», — сказал он."), ())
        self.assertEqual(len(narration_spans("«Привет», — сказал он.")), 1)


class DialogueMetricTests(unittest.TestCase):
    SAMPLE = "Автор пишет. Ещё.\n— Привет, — сказал он. — Пока.\n— Ответ."

    def test_dialogue_metrics_use_explicit_candidate_denominators(self):
        artifact = analyze_deterministic_metrics(self.SAMPLE)
        metrics = artifact["metrics"]

        self.assertEqual(artifact["profiles"]["dialogue"], DIALOGUE_PROFILE)
        self.assertAlmostEqual(
            metrics["fantlab.dialogue.mean_narration_sentence_length_chars"]["value"],
            8.0,
        )
        self.assertAlmostEqual(
            metrics["fantlab.dialogue.mean_dialogue_sentence_length_chars"]["value"],
            37 / 3,
        )
        self.assertAlmostEqual(
            metrics["fantlab.dialogue.share_percent"]["value"],
            31 * 100 / 46,
        )
        self.assertAlmostEqual(
            metrics["fantlab.dialogue.author_text_inside_dialogue_percent"]["value"],
            9 * 100 / 31,
        )
        for metric_id in (
            "fantlab.dialogue.mean_narration_sentence_length_chars",
            "fantlab.dialogue.mean_dialogue_sentence_length_chars",
            "fantlab.dialogue.share_percent",
            "fantlab.dialogue.author_text_inside_dialogue_percent",
        ):
            self.assertEqual(metrics[metric_id]["compatibility_status"], "inferred")
            self.assertEqual(metrics[metric_id]["definition_evidence"], "public_surface")

    def test_empty_and_no_dialogue_denominators_are_explicit(self):
        empty = analyze_deterministic_metrics("")["metrics"]
        self.assertIsNone(empty["fantlab.dialogue.mean_narration_sentence_length_chars"]["value"])
        self.assertIsNone(empty["fantlab.dialogue.mean_dialogue_sentence_length_chars"]["value"])
        self.assertIsNone(empty["fantlab.dialogue.share_percent"]["value"])
        self.assertIsNone(empty["fantlab.dialogue.author_text_inside_dialogue_percent"]["value"])

        narration = analyze_deterministic_metrics("Только авторский текст.")["metrics"]
        self.assertIsNotNone(
            narration["fantlab.dialogue.mean_narration_sentence_length_chars"]["value"]
        )
        self.assertIsNone(
            narration["fantlab.dialogue.mean_dialogue_sentence_length_chars"]["value"]
        )
        self.assertEqual(narration["fantlab.dialogue.share_percent"]["value"], 0.0)
        self.assertIsNone(
            narration["fantlab.dialogue.author_text_inside_dialogue_percent"]["value"]
        )

    def test_schema_v2_freezes_dialogue_profile_and_rows(self):
        schema_path = (
            Path(__file__).parents[1]
            / "schemas"
            / "scriptorium-deterministic-metrics-v2.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        self.assertEqual(schema["properties"]["schema_version"]["const"], SCHEMA_VERSION)
        self.assertEqual(
            schema["properties"]["profiles"]["properties"]["dialogue"]["const"],
            DIALOGUE_PROFILE,
        )
        required = schema["properties"]["metrics"]["required"]
        self.assertEqual(len(required), 23)
        self.assertIn("fantlab.dialogue.share_percent", required)

    def test_benchmark_exposes_all_four_dialogue_fields_as_unresolved_precision(self):
        reference = {
            "benchmark_id": "dialogue-test",
            "reference": {
                "site": "FantLab",
                "url": "https://fantlab.ru/work1/lp",
                "analysis_date": "2022-09-19",
                "work_id": 1,
                "title": "Test",
                "author": "Author",
            },
            "expected": {
                "mean_narration_sentence_length_characters": 8.0,
                "mean_dialogue_sentence_length_characters": 12.33,
                "dialogue_share_percent": 67.39,
                "author_text_inside_dialogue_percent": 29.03,
            },
        }
        artifact = build_comparison(
            json.dumps(reference, ensure_ascii=False),
            self.SAMPLE.encode("utf-8"),
            scriptorium_revision="abc123",
            edition_match="exact",
            edition_label="exact test edition",
            source_reference="local:test",
            legal_basis="public_domain",
        )

        self.assertEqual(len(artifact["metrics"]), 4)
        for metric_id, row in artifact["metrics"].items():
            self.assertTrue(metric_id.startswith("fantlab.dialogue."))
            self.assertEqual(row["comparison"]["rule"], "unresolved_precision")
            self.assertIsNone(row["comparison"]["numeric_match"])
            self.assertEqual(row["comparison"]["result"], "unresolved")


if __name__ == "__main__":
    unittest.main()
