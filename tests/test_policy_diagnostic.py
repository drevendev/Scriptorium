import json
from pathlib import Path
import unittest

from scriptorium.policy_diagnostic import analyze_word_dash_policy


class PolicyDiagnosticTests(unittest.TestCase):
    def test_reports_bounded_word_and_dash_sensitivity_without_source_text(self):
        text = "по-русски ‐ слово‑слово — 12 34-56 СЕКРЕТНЫЙЛЕКСЕМ"

        artifact = analyze_word_dash_policy(
            text,
            expected_word_count=3,
            expected_dash_per_1000_words=500.0,
        )

        word_variants = artifact["word_policy"]["variants"]
        self.assertEqual(word_variants["current_scriptorium_text_v1"]["count"], 6)
        self.assertEqual(word_variants["exclude_numeric_only_tokens"]["count"], 5)
        self.assertEqual(word_variants["join_unicode_hyphen_connectors"]["count"], 5)
        self.assertEqual(
            word_variants["join_unicode_hyphens_and_exclude_numeric_only"]["count"],
            4,
        )
        self.assertEqual(
            word_variants["join_unicode_hyphens_and_exclude_numeric_only"][
                "delta_to_reference"
            ],
            1,
        )

        dash_policy = artifact["dash_policy"]
        self.assertEqual(dash_policy["ascii_hyphen_contexts"]["between_letters"], 1)
        self.assertEqual(dash_policy["ascii_hyphen_contexts"]["between_digits"], 1)
        self.assertEqual(dash_policy["lexical_hyphen_like_between_letters"], 2)
        self.assertEqual(dash_policy["current_token_internal_ascii_hyphens"], 2)

        dash_variants = dash_policy["variants"]
        self.assertEqual(dash_variants["current_all_supported_dash_glyphs"]["count"], 5)
        self.assertEqual(dash_variants["exclude_ascii_hyphen_between_letters"]["count"], 4)
        self.assertEqual(
            dash_variants["exclude_lexical_hyphen_like_between_letters"]["count"],
            3,
        )
        self.assertEqual(
            dash_variants["exclude_all_current_token_internal_ascii_hyphens"]["count"],
            3,
        )
        self.assertAlmostEqual(
            dash_variants["exclude_lexical_hyphen_like_between_letters"][
                "per_1000_current_words"
            ],
            500.0,
        )
        self.assertAlmostEqual(
            dash_variants["exclude_lexical_hyphen_like_between_letters"][
                "rate_delta_to_reference"
            ],
            0.0,
        )

        serialized = json.dumps(artifact, ensure_ascii=False)
        self.assertNotIn("СЕКРЕТНЫЙЛЕКСЕМ", serialized)
        self.assertEqual(artifact["status"], "diagnostic_only")

    def test_empty_text_keeps_rates_not_run_instead_of_fabricating_zero(self):
        artifact = analyze_word_dash_policy("")

        self.assertEqual(
            artifact["word_policy"]["variants"]["current_scriptorium_text_v1"]["count"],
            0,
        )
        self.assertIsNone(
            artifact["dash_policy"]["variants"]["current_all_supported_dash_glyphs"][
                "per_1000_current_words"
            ]
        )

    def test_committed_sensitivity_artifact_stays_source_free_and_fail_closed(self):
        path = Path("benchmarks/fantlab/work270306-policy-sensitivity.json")
        artifact = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(artifact["artifact_version"], "scriptorium-text-policy-diagnostic-v1")
        self.assertEqual(artifact["epistemic_status"]["status"], "diagnostic_only")
        self.assertEqual(
            artifact["epistemic_status"]["fantlab_source_edition_match"], "unknown"
        )
        self.assertIs(artifact["epistemic_status"]["m2_parity_admissible"], False)
        self.assertEqual(artifact["epistemic_status"]["m2_source_matched_progress"], "0/5")
        self.assertIs(artifact["evidence"]["source_text_committed"], False)
        self.assertIs(artifact["evidence"]["source_text_uploaded"], False)
        self.assertEqual(
            artifact["word_policy"]["variants"]["exclude_numeric_only_tokens"][
                "delta_to_reference"
            ],
            16066,
        )
        self.assertAlmostEqual(
            artifact["dash_policy"]["variants"][
                "exclude_all_current_token_internal_ascii_hyphens"
            ]["rate_delta_to_reference"],
            14.91281699448318,
        )


if __name__ == "__main__":
    unittest.main()
