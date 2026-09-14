import json
import unittest
from unittest.mock import patch

from scriptorium.repro_diagnostic import build_frozen_diagnostic


class ReproDiagnosticTests(unittest.TestCase):
    def test_frozen_diagnostic_remains_fail_closed_for_unknown_fantlab_source(self):
        reference = json.dumps(
            {
                "benchmark_id": "example",
                "reference": {
                    "site": "FantLab",
                    "url": "https://example.invalid/lp",
                    "analysis_date": "2022-09-19",
                    "work_id": 1,
                    "title": "Example",
                    "author": "Example",
                },
                "expected": {
                    "characters": 11,
                    "words": 2,
                    "dialogue_share_percent": 35.12,
                    "author_text_inside_dialogue_percent": 17.02,
                },
            }
        )
        manifest = {
            "bibliographic_source": "Frozen edition",
            "source_work_url": "https://example.invalid/source",
            "legal_basis": "public_domain",
        }

        with patch(
            "scriptorium.repro_diagnostic.replay_packed_manifest",
            return_value="Привет мир.",
        ):
            artifact = build_frozen_diagnostic(
                reference,
                manifest,
                scriptorium_revision="abc123",
            )

        self.assertEqual(artifact["source_text"]["edition_match"], "unknown")
        self.assertEqual(
            artifact["metrics"]["fantlab.general.characters"]["comparison"]["result"],
            "unresolved",
        )
        self.assertEqual(
            artifact["metrics"]["fantlab.general.characters"]["comparison"]["raw_delta"],
            0,
        )
        self.assertEqual(artifact["diagnostic_boundary"]["status"], "diagnostic_only")
        self.assertIs(artifact["diagnostic_boundary"]["m2_parity_admissible"], False)
        self.assertEqual(artifact["policy_sensitivity"]["status"], "diagnostic_only")
        self.assertEqual(
            artifact["policy_sensitivity"]["word_policy"]["variants"][
                "current_scriptorium_text_v1"
            ]["count"],
            2,
        )
        self.assertEqual(
            artifact["policy_sensitivity"]["reference"]["expected_word_count"],
            2,
        )
        self.assertIsNone(
            artifact["policy_sensitivity"]["reference"]["expected_dash_per_1000_words"]
        )

        self.assertEqual(artifact["dialogue_sensitivity"]["status"], "diagnostic_only")
        self.assertEqual(
            artifact["dialogue_sensitivity"]["reference"][
                "expected_dialogue_share_percent"
            ],
            35.12,
        )
        self.assertEqual(
            artifact["dialogue_sensitivity"]["reference"][
                "expected_author_text_inside_dialogue_percent"
            ],
            17.02,
        )
        self.assertIsNone(artifact["dialogue_sensitivity"]["dialogue_share"]["value"])
        self.assertIsNone(
            artifact["dialogue_sensitivity"]["author_text_inside_dialogue_variants"][
                "current_v1_over_dialogue"
            ]["value"]
        )


if __name__ == "__main__":
    unittest.main()
