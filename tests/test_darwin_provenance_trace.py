import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = (
    ROOT
    / "corpus"
    / "candidates"
    / "source-edition-traces"
    / "darwin-origin-species-rachinsky-1864-ru.json"
)


class DarwinProvenanceTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))

    def test_composition_contract_is_frozen_without_promoting_rendered_body(self) -> None:
        contract = self.trace["source"]["literary_body_composition_contract"]
        self.assertEqual(
            contract["contract_version"],
            "scriptorium-darwin-literary-body-contract-v1",
        )
        self.assertEqual(
            contract["composition_profile"],
            "scriptorium-darwin-numbered-routes-1-through-14-v1",
        )
        self.assertEqual(contract["frozen_dependency_count"], 418)
        self.assertEqual(contract["literary_dependency_count"], 388)
        self.assertEqual(contract["apparatus_dependency_count"], 30)
        self.assertEqual(contract["explicit_no_text_non_dependencies"], [114, 411])
        self.assertTrue(contract["selection_and_partition_frozen"])
        self.assertFalse(contract["page_wikitext_to_prose_rendering_profile_frozen"])
        self.assertFalse(contract["composite_separator_semantics_frozen"])
        self.assertFalse(contract["literary_body_count_and_digests_frozen"])
        self.assertFalse(contract["source_text_committed"])

    def test_threshold_and_fantlab_gates_remain_closed(self) -> None:
        threshold = self.trace["corpus_threshold"]
        self.assertTrue(threshold["composition_contract_is_not_threshold_proof"])
        self.assertFalse(threshold["literary_body_character_count_verified"])
        self.assertIsNone(threshold["literary_body_character_count"])
        self.assertFalse(threshold["admitted_for_calibration"])

        fantlab = self.trace["fantlab"]
        self.assertEqual(fantlab["source_edition_match"], "unknown")
        self.assertFalse(fantlab["analyzer_input_identity_established"])

        admissibility = self.trace["admissibility"]
        self.assertFalse(admissibility["diagnostic_ready"])
        self.assertFalse(admissibility["gate_ready"])
        self.assertFalse(admissibility["m2_parity_admissible"])

    def test_next_evidence_no_longer_redefines_the_frozen_partition(self) -> None:
        next_evidence = self.trace["next_evidence"]
        self.assertIn("388 exact literary dependencies", next_evidence[0])
        self.assertIn("Page-wikitext-to-prose rendering profile", next_evidence[0])
        self.assertNotIn("Define a candidate-specific deterministic fail-closed literary-body extraction/composition contract", next_evidence[0])


if __name__ == "__main__":
    unittest.main()
