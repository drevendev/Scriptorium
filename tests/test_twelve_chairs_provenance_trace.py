import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-ru.json"
GRAPH = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json"
INDEX = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json"
SCAN = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.scan-identity.json"
PUBLIC = ROOT / "corpus/candidates/ilf-petrov-twelve-chairs-ru.md"


class TwelveChairsProvenanceTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace = json.loads(TRACE.read_text(encoding="utf-8"))
        cls.graph = json.loads(GRAPH.read_text(encoding="utf-8"))
        cls.index = json.loads(INDEX.read_text(encoding="utf-8"))
        cls.scan = json.loads(SCAN.read_text(encoding="utf-8"))
        cls.public = PUBLIC.read_text(encoding="utf-8")
        cls.family = next(
            row
            for row in cls.trace["public_text_families"]
            if row["family_id"] == "wikisource-zif-1928-first-standalone-edition"
        )

    def test_structured_trace_binds_exact_410_page_identity_manifest(self):
        self.assertEqual(self.family["page_revision_identity_manifest"], INDEX.name)
        self.assertTrue(self.family["route_graph"]["page_revision_identities_frozen"])
        self.assertEqual(self.family["route_graph"]["referenced_page_namespace_count"], 410)
        self.assertEqual(self.index["page_identity_count"], 410)
        self.assertEqual(
            self.family["immutable_identity"]["status"],
            "route_graph_410_page_revision_identities_and_scan_binary_frozen_body_unfrozen",
        )

    def test_scan_identity_is_exact_source_free_and_bound_to_trace(self):
        self.assertEqual(
            self.family["scan_identity_receipt"],
            SCAN.name,
        )
        self.assertEqual(self.trace["facsimile_lead"]["byte_snapshot_status"], "frozen_exact_binary_identity")
        self.assertEqual(self.trace["facsimile_lead"]["scriptorium_binary_sha256"], self.scan["identity"]["sha256"])
        self.assertEqual(self.scan["identity"]["byte_count"], 77978350)
        self.assertEqual(self.scan["identity"]["sha1"], "4ab6aa42c3517169e99c1177b6fb6412cfe9187d")
        self.assertEqual(self.scan["identity"]["sha256"], "5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4")
        self.assertFalse(self.scan["binary_bytes_committed"])
        self.assertFalse(self.scan["ocr_included"])
        self.assertFalse(self.scan["literary_source_text_included"])
        self.assertEqual(self.graph["proofread_index"]["binary_identity_status"], "frozen_exact_commons_original")
        self.assertEqual(self.graph["scan_identity_receipt"], SCAN.name)

    def test_source_graph_and_index_agree_on_topology_and_gaps(self):
        self.assertTrue(self.graph["dependency_summary"]["underlying_page_revision_identities_frozen"])
        self.assertFalse(self.graph["dependency_summary"]["literary_body_frozen"])
        self.assertEqual(self.graph["dependency_summary"]["referenced_page_namespace_count"], 410)
        self.assertEqual(self.index["topology_contract"]["non_transcluded_gaps"], [[150, 151], [314, 315]])
        self.assertEqual(
            [[row["from_scan_page"], row["to_scan_page"]] for row in self.graph["non_transcluded_scan_gaps"]],
            [[150, 151], [314, 315]],
        )
        self.assertTrue(all(row["classification"] == "unclassified_non_transcluded_gap" for row in self.graph["non_transcluded_scan_gaps"]))
        self.assertFalse(self.scan["page_dependency_set_changed"])
        self.assertFalse(self.scan["gap_pages_classified"])

    def test_downstream_gates_remain_closed(self):
        admissibility = self.trace["admissibility"]
        self.assertEqual(admissibility["fantlab_source_edition_match"], "unknown")
        self.assertFalse(admissibility["diagnostic_ready"])
        self.assertFalse(admissibility["gate_ready"])
        self.assertFalse(admissibility["m2_parity_admissible"])
        self.assertFalse(self.index["literary_body_frozen"])
        self.assertFalse(self.index["admitted_for_calibration"])
        self.assertFalse(self.index["diagnostic_ready"])
        self.assertFalse(self.index["m2_parity_admissible"])
        self.assertFalse(self.scan["literary_body_count_and_digests_frozen"])
        self.assertFalse(self.scan["minimum_300k_proved_from_frozen_body"])
        self.assertFalse(self.scan["admitted_for_calibration"])
        self.assertEqual(self.scan["fantlab_source_edition_match"], "unknown")
        self.assertFalse(self.scan["diagnostic_ready"])
        self.assertFalse(self.scan["m2_parity_admissible"])

    def test_public_candidate_exposes_scan_identity_without_promoting_body(self):
        self.assertIn("410 exact Page revision identities frozen", self.public)
        self.assertIn("77,978,350 bytes", self.public)
        self.assertIn("5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4", self.public)
        self.assertIn("not a literary-body freeze", self.public)
        self.assertIn("150–151", self.public)
        self.assertIn("314–315", self.public)
        self.assertIn("m2_parity_admissible=false", self.public)


if __name__ == "__main__":
    unittest.main()
