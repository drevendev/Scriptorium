import json
from pathlib import Path
import unittest

from scriptorium.metrics import METRIC_PROFILE, PUNCTUATION_PROFILE, SCHEMA_VERSION
from scriptorium.text import NORMALIZATION_PROFILE


class PunctuationPolicyEvidenceTests(unittest.TestCase):
    def test_evidence_stays_inferred_and_matches_runtime_profiles(self):
        path = Path("compatibility/punctuation-v2-evidence.json")
        artifact = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(
            artifact["artifact_version"],
            "scriptorium-punctuation-policy-evidence-v1",
        )
        self.assertEqual(artifact["unit_id"], "SCRIP-PUNCT-002")
        self.assertEqual(artifact["epistemic_status"]["status"], "inferred")
        self.assertIs(artifact["epistemic_status"]["recovered_fantlab_rule"], False)
        self.assertEqual(
            artifact["epistemic_status"]["fantlab_hyphen_dash_classifier"],
            "unknown",
        )
        self.assertEqual(
            artifact["epistemic_status"]["m2_source_matched_progress"],
            "0/5",
        )

        profiles = artifact["scriptorium_profiles"]
        self.assertEqual(profiles["normalization"], NORMALIZATION_PROFILE)
        self.assertEqual(profiles["punctuation"], PUNCTUATION_PROFILE)
        self.assertEqual(profiles["metrics"], METRIC_PROFILE)
        self.assertEqual(profiles["artifact_schema"], SCHEMA_VERSION)

        self.assertEqual(
            artifact["decision"]["ascii_hyphen_minus"][
                "token_internal_under_scriptorium_text_v1"
            ],
            "lexical_connector_not_dash_event",
        )
        self.assertEqual(
            artifact["historical_diagnostic"]["fantlab_source_edition_match"],
            "unknown",
        )


if __name__ == "__main__":
    unittest.main()
