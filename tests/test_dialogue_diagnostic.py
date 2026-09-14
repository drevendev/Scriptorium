import json
import unittest

from scriptorium.dialogue_diagnostic import (
    DIALOGUE_DIAGNOSTIC_VERSION,
    analyze_dialogue_policy,
)


class DialoguePolicyDiagnosticTests(unittest.TestCase):
    SAMPLE = (
        "Нарратив здесь.\n"
        "— Привет, — сказал он. — Пока.\n"
        "— Я — человек.\n"
        "— Почему? — спросил он.\n"
        "— Я думаю, — сказал он, — что да."
    )

    def test_boundary_probe_separates_speech_internal_dash_from_author_openers(self):
        artifact = analyze_dialogue_policy(
            self.SAMPLE,
            expected_dialogue_share_percent=35.12,
            expected_author_text_inside_dialogue_percent=17.02,
        )

        self.assertEqual(artifact["schema_version"], DIALOGUE_DIAGNOSTIC_VERSION)
        self.assertEqual(artifact["status"], "diagnostic_only")
        self.assertEqual(
            artifact["structure"]["separator_left_context_counts"],
            {"alnum": 1, "comma": 3, "period": 1, "question": 1},
        )
        self.assertEqual(artifact["structure"]["internal_separator_count"], 6)
        self.assertEqual(artifact["structure"]["current_v1_author_remark_span_count"], 4)
        self.assertEqual(
            artifact["structure"]["speech_boundary_author_remark_span_count"], 3
        )

        counts = artifact["character_counts"]
        self.assertEqual(counts["total_non_whitespace"], 93)
        self.assertEqual(counts["dialogue_non_whitespace"], 79)
        self.assertEqual(counts["current_v1_author_remark_non_whitespace"], 36)
        self.assertEqual(
            counts["speech_boundary_author_remark_non_whitespace"], 28
        )

        variants = artifact["author_text_inside_dialogue_variants"]
        self.assertAlmostEqual(
            variants["current_v1_over_dialogue"]["value"], 36 * 100 / 79
        )
        self.assertAlmostEqual(
            variants["speech_boundary_openers_over_dialogue"]["value"],
            28 * 100 / 79,
        )
        self.assertAlmostEqual(
            variants["current_v1_over_total_text"]["value"], 36 * 100 / 93
        )
        self.assertAlmostEqual(
            variants["speech_boundary_openers_over_total_text"]["value"],
            28 * 100 / 93,
        )

    def test_diagnostic_is_source_free_and_fail_closed(self):
        artifact = analyze_dialogue_policy(
            self.SAMPLE,
            expected_author_text_inside_dialogue_percent=17.02,
        )
        serialized = json.dumps(artifact, ensure_ascii=False)

        self.assertNotIn("Привет", serialized)
        self.assertNotIn("сказал он", serialized)
        self.assertIn("not recovered FantLab semantics", artifact["warning"])
        self.assertEqual(
            artifact["reference"]["expected_author_text_inside_dialogue_percent"],
            17.02,
        )

    def test_empty_input_keeps_undefined_denominators_explicit(self):
        artifact = analyze_dialogue_policy("")
        self.assertEqual(artifact["structure"]["dialogue_paragraph_count"], 0)
        self.assertEqual(artifact["structure"]["internal_separator_count"], 0)
        self.assertIsNone(artifact["dialogue_share"]["value"])
        for row in artifact["author_text_inside_dialogue_variants"].values():
            self.assertIsNone(row["value"])


if __name__ == "__main__":
    unittest.main()
