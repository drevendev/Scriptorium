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
RENDER_PROFILE_PATH = TRACE_PATH.with_name(
    "darwin-origin-species-rachinsky-1864-ru.render-profile.json"
)
RENDER_SOURCE_GRAPH_PATH = TRACE_PATH.with_name(
    "darwin-origin-species-rachinsky-1864-ru.render-surface.source-graph.json"
)


class DarwinProvenanceTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
        cls.scan_receipt = json.loads(SCAN_RECEIPT_PATH.read_text(encoding="utf-8"))
        cls.render_profile = json.loads(RENDER_PROFILE_PATH.read_text(encoding="utf-8"))
        cls.render_source_graph = json.loads(RENDER_SOURCE_GRAPH_PATH.read_text(encoding="utf-8"))

    def test_composition_contract_is_frozen_with_profile_but_without_promoting_rendered_body(self) -> None:
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
        self.assertTrue(contract["page_wikitext_to_prose_rendering_profile_frozen"])
        self.assertEqual(contract["render_profile_version"], "scriptorium-darwin-page-render-profile-v1")
        self.assertEqual(contract["render_profile_sha256"], self.render_profile["profile_sha256"])
        self.assertFalse(contract["renderer_semantics_complete"])
        self.assertFalse(contract["renderer_implementation_ready"])
        self.assertFalse(contract["rendering_equivalence_claimed"])
        self.assertFalse(contract["composite_separator_semantics_frozen"])
        self.assertFalse(contract["literary_body_count_and_digests_frozen"])
        self.assertFalse(contract["source_text_committed"])

    def test_render_profile_source_graph_is_synchronized_without_promoting_gates(self) -> None:
        boundary = self.render_source_graph["gate_boundary"]
        self.assertTrue(boundary["surface_inventory_frozen"])
        self.assertTrue(boundary["rendering_profile_frozen"])
        self.assertFalse(boundary["renderer_semantics_complete"])
        self.assertFalse(boundary["renderer_implementation_ready"])
        self.assertFalse(boundary["rendering_equivalence_claimed"])
        self.assertFalse(boundary["inter_page_composition_frozen"])
        self.assertFalse(boundary["literary_body_count_and_digests_frozen"])
        self.assertFalse(boundary["minimum_300k_proved"])
        self.assertFalse(boundary["admitted_for_calibration"])
        self.assertEqual(boundary["fantlab_source_edition_match"], "unknown")
        nodes = {node["id"]: node for node in self.render_source_graph["nodes"]}
        self.assertEqual(nodes["durable-render-profile"]["profile_sha256"], self.render_profile["profile_sha256"])
        self.assertFalse(nodes["durable-render-profile"]["source_text_included"])

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

    def test_next_evidence_starts_after_the_frozen_profile_boundary(self) -> None:
        next_evidence = self.trace["next_evidence"]
        self.assertIn("provider/template/reference/math semantics", next_evidence[0])
        self.assertIn("inter-page separator/composition semantics", next_evidence[0])
        self.assertFalse(any("Define and verify a candidate-specific fail-closed Page-wikitext-to-prose rendering profile" in item for item in next_evidence))
        self.assertFalse(any("retrieve one exact DjVu byte stream" in item for item in next_evidence))


if __name__ == "__main__":
    unittest.main()
