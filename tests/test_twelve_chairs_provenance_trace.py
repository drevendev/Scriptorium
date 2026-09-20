import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-ru.json"
GRAPH = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json"
INDEX = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json"
SCAN = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.scan-identity.json"
GAPS = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.gap-audit.json"
PUBLIC = ROOT / "corpus/candidates/ilf-petrov-twelve-chairs-ru.md"


class TwelveChairsProvenanceTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace = json.loads(TRACE.read_text(encoding="utf-8"))
        cls.graph = json.loads(GRAPH.read_text(encoding="utf-8"))
        cls.index = json.loads(INDEX.read_text(encoding="utf-8"))
        cls.scan = json.loads(SCAN.read_text(encoding="utf-8"))
        cls.gaps = json.loads(GAPS.read_text(encoding="utf-8"))
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
            "route_graph_410_page_revision_identities_scan_binary_and_gap_surface_frozen_body_unfrozen",
        )
        self.assertEqual(self.family["gap_audit_manifest"], GAPS.name)
        self.assertTrue(self.family["route_graph"]["gap_page_revisions_inspected"])

    def test_scan_identity_is_exact_source_free_and_bound_to_trace(self):
        self.assertEqual(self.family["scan_identity_receipt"], SCAN.name)
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

    def test_source_graph_index_and_gap_audit_agree_without_changing_dependencies(self):
        self.assertTrue(self.graph["dependency_summary"]["underlying_page_revision_identities_frozen"])
        self.assertTrue(self.graph["dependency_summary"]["non_transcluded_gap_revisions_inspected"])
        self.assertFalse(self.graph["dependency_summary"]["literary_body_frozen"])
        self.assertEqual(self.graph["dependency_summary"]["referenced_page_namespace_count"], 410)
        self.assertEqual(self.index["page_identity_count"], 410)
        self.assertEqual(self.index["topology_contract"]["non_transcluded_gaps"], [[150, 151], [314, 315]])
        self.assertEqual(
            [[row["from_scan_page"], row["to_scan_page"]] for row in self.graph["non_transcluded_scan_gaps"]],
            [[150, 151], [314, 315]],
        )
        self.assertTrue(
            all(
                row["classification"] == "inspected_mixed_body_presence_not_composed"
                for row in self.graph["non_transcluded_scan_gaps"]
            )
        )
        self.assertTrue(self.gaps["dependency_inventory_unchanged"])
        self.assertEqual(self.gaps["gap_sequences"], [150, 151, 314, 315])
        self.assertEqual(
            [row["body_presence_class"] for row in self.gaps["gap_pages"]],
            [
                "nonempty_body_unclassified",
                "no_transcluded_body",
                "nonempty_body_unclassified",
                "no_transcluded_body",
            ],
        )
        self.assertFalse(self.scan["page_dependency_set_changed"])

    def test_gap_audit_is_source_free_and_keeps_membership_unfrozen(self):
        self.assertEqual(self.gaps["manifest_version"], "scriptorium-twelve-chairs-gap-audit-v1")
        self.assertFalse(self.gaps["source_text_included"])
        self.assertFalse(self.gaps["all_gap_pages_have_no_transcluded_body"])
        self.assertFalse(self.gaps["literary_membership_frozen"])
        self.assertFalse(self.gaps["literary_body_frozen"])
        self.assertFalse(self.gaps["admitted_for_calibration"])
        self.assertEqual(self.gaps["fantlab_source_edition_match"], "unknown")
        self.assertFalse(self.gaps["diagnostic_ready"])
        self.assertFalse(self.gaps["m2_parity_admissible"])
        self.assertEqual(self.gaps["gap_pages"][1]["transcluded_body_codepoints"], 0)
        self.assertEqual(self.gaps["gap_pages"][3]["transcluded_body_codepoints"], 0)
        self.assertGreater(self.gaps["gap_pages"][0]["transcluded_body_letter_codepoints"], 0)
        self.assertGreater(self.gaps["gap_pages"][2]["transcluded_body_letter_codepoints"], 0)

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
        self.assertFalse(self.gaps["literary_body_frozen"])
        self.assertFalse(self.gaps["admitted_for_calibration"])
        self.assertEqual(self.gaps["fantlab_source_edition_match"], "unknown")
        self.assertFalse(self.gaps["diagnostic_ready"])
        self.assertFalse(self.gaps["m2_parity_admissible"])

    def test_public_candidate_exposes_gap_evidence_without_promoting_body(self):
        self.assertIn("410 Page-namespace dependencies", self.public)
        self.assertIn("77,978,350 bytes", self.public)
        self.assertIn("5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4", self.public)
        self.assertIn("not a literary-body freeze", self.public)
        self.assertIn("nonempty_body_unclassified", self.public)
        self.assertIn("no_transcluded_body", self.public)
        self.assertIn("page **150**", self.public)
        self.assertIn("page **314**", self.public)
        self.assertIn("m2_parity_admissible=false", self.public)


if __name__ == "__main__":
    unittest.main()
