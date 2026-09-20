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
SCAN_RECEIPT_PATH = TRACE_PATH.with_name(
    "darwin-origin-species-rachinsky-1864-ru.scan-identity.json"
)


class DarwinProvenanceTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
        cls.scan_receipt = json.loads(SCAN_RECEIPT_PATH.read_text(encoding="utf-8"))

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

    def test_independent_scan_identity_is_reconciled_source_free(self) -> None:
        metadata = self.trace["source"]["scan_file_metadata"]
        identity = metadata["independent_binary_identity"]
        receipt_identity = self.scan_receipt["identity"]
        self.assertTrue(metadata["binary_bytes_retrieved_by_scriptorium"])
        self.assertTrue(metadata["binary_sha256_computed_by_scriptorium"])
        self.assertFalse(metadata["binary_bytes_committed"])
        self.assertEqual(identity["byte_count"], receipt_identity["byte_count"])
        self.assertEqual(identity["sha1"], receipt_identity["sha1"])
        self.assertEqual(identity["sha256"], receipt_identity["sha256"])
        self.assertEqual(
            identity["sha256"],
            "7f3ae1aadd4a844b193783a0c350e23815a76e7bb14a92bae7fa1c077354a2c8",
        )
        self.assertFalse(self.scan_receipt["binary_bytes_committed"])
        self.assertFalse(self.scan_receipt["source_text_included"])

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

    def test_next_evidence_no_longer_redefines_the_frozen_partition_or_scan_identity(self) -> None:
        next_evidence = self.trace["next_evidence"]
        self.assertIn("388 exact literary dependencies", next_evidence[0])
        self.assertIn("Page-wikitext-to-prose rendering profile", next_evidence[0])
        self.assertNotIn("Define a candidate-specific deterministic fail-closed literary-body extraction/composition contract", next_evidence[0])
        self.assertFalse(any("retrieve one exact DjVu byte stream" in item for item in next_evidence))


if __name__ == "__main__":
    unittest.main()
