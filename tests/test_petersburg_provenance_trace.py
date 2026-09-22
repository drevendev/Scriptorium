from __future__ import annotations

import json
from pathlib import Path
import unittest

from scriptorium.petersburg_ocr_contract import canonical_sha256, load_contract
from scriptorium.petersburg_scan_identity import validate_receipt


ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT / "corpus/candidates/source-edition-traces/bely-petersburg-1916-ru.json"
RECEIPT_PATH = ROOT / "corpus/candidates/source-edition-traces/bely-petersburg-1916-ru.scan-identity.json"
CONTRACT_PATH = ROOT / "corpus/candidates/source-edition-traces/bely-petersburg-1916-ru.ocr-contract.json"
CANDIDATE_PAGE = ROOT / "corpus/candidates/bely-petersburg-1916-ru.md"

EXPECTED_BYTES = 3_621_459
EXPECTED_SHA1 = "682476934dd6ed49c6bbcdb0720127c1812ff477"
EXPECTED_SHA256 = "b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5"
EXPECTED_CONTRACT_SHA256 = "d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2"


class PetersburgProvenanceTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
        self.receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
        self.contract = load_contract(CONTRACT_PATH)
        validate_receipt(self.receipt)

    def test_structured_trace_is_bound_to_frozen_binary_receipt(self) -> None:
        self.assertEqual(self.trace["candidate_id"], "bely-petersburg-1916-ru")
        boundary = self.trace["public_edition"]["commons_binary_identity_boundary"]
        self.assertEqual(boundary["byte_snapshot_status"], "frozen")
        self.assertEqual(boundary["scriptorium_pdf_byte_count"], EXPECTED_BYTES)
        self.assertEqual(boundary["scriptorium_pdf_sha1"], EXPECTED_SHA1)
        self.assertEqual(boundary["scriptorium_pdf_sha256"], EXPECTED_SHA256)
        self.assertEqual(boundary["source_free_receipt"], RECEIPT_PATH.name)
        self.assertEqual(boundary["page_information_hash"], EXPECTED_SHA1)
        self.assertEqual(self.receipt["identity"], {
            "byte_count": EXPECTED_BYTES,
            "sha1": EXPECTED_SHA1,
            "sha256": EXPECTED_SHA256,
        })

    def test_trace_is_bound_to_source_free_ocr_contract(self) -> None:
        promotion = self.trace["public_edition"]["ocr_body_promotion_contract"]
        self.assertEqual(promotion["contract_version"], self.contract["contract_version"])
        self.assertEqual(promotion["source_free_contract"], CONTRACT_PATH.name)
        self.assertEqual(promotion["canonical_sha256"], EXPECTED_CONTRACT_SHA256)
        self.assertEqual(canonical_sha256(self.contract), EXPECTED_CONTRACT_SHA256)
        self.assertTrue(promotion["scan_identity_bound"])
        self.assertFalse(promotion["page_selection_bound"])
        self.assertFalse(promotion["rasterization_toolchain_bound"])
        self.assertFalse(promotion["ocr_toolchain_bound"])
        self.assertFalse(promotion["body_outputs_frozen"])

    def test_contract_does_not_promote_text_or_fantlab_gates(self) -> None:
        identity = self.trace["public_edition"]["immutable_identity"]
        self.assertEqual(identity["status"], "scan_binary_frozen_ocr_contract_defined_body_unverified")
        unfrozen = "\n".join(identity["unfrozen_components"])
        self.assertIn("page selection", unfrozen)
        self.assertIn("OCR", unfrozen)
        self.assertIn("literary-text", unfrozen)
        self.assertIn("FantLab", unfrozen)

        admissibility = self.trace["admissibility"]
        self.assertEqual(admissibility["status"], "scan_binary_frozen_ocr_contract_defined_body_unverified")
        self.assertTrue(admissibility["length_threshold_met_from_fantlab"])
        self.assertEqual(admissibility["fantlab_source_edition_match"], "unknown")
        self.assertFalse(admissibility["diagnostic_ready"])
        self.assertFalse(admissibility["gate_ready"])
        self.assertFalse(admissibility["m2_parity_admissible"])

        self.assertFalse(self.receipt["ocr_extraction_profile_frozen"])
        self.assertFalse(self.receipt["literary_body_count_and_digests_frozen"])
        self.assertFalse(self.receipt["minimum_300k_proved_from_frozen_body"])
        self.assertFalse(self.receipt["admitted_for_calibration"])
        self.assertFalse(self.receipt["diagnostic_ready"])
        self.assertFalse(self.receipt["m2_parity_admissible"])

    def test_next_evidence_starts_after_contract_definition(self) -> None:
        next_evidence = "\n".join(self.trace["admissibility"]["next_evidence"])
        self.assertIn("new independently evidenced contract version", next_evidence)
        self.assertIn("literary-body character count", next_evidence)
        self.assertNotIn("Define and verify a deterministic", next_evidence)

    def test_public_candidate_page_exposes_contract_without_source_payload(self) -> None:
        page = CANDIDATE_PAGE.read_text(encoding="utf-8")
        self.assertIn(f"**{EXPECTED_BYTES:,}**", page)
        self.assertIn(EXPECTED_SHA1, page)
        self.assertIn(EXPECTED_SHA256, page)
        self.assertIn(EXPECTED_CONTRACT_SHA256, page)
        self.assertIn("No PDF bytes", page)
        self.assertIn("m2_parity_admissible=false", page)


if __name__ == "__main__":
    unittest.main()
