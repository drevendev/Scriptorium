from __future__ import annotations

import json
from pathlib import Path
import unittest

from scriptorium.perelman_djvu_identity import validate_receipt as validate_djvu_receipt
from scriptorium.perelman_ocr_contract import canonical_sha256, load_contract
from scriptorium.perelman_scan_identity import validate_receipt


ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT / "corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.json"
RECEIPT_PATH = ROOT / "corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.scan-identity.json"
DJVU_RECEIPT_PATH = ROOT / "corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.djvu-identity.json"
CONTRACT_PATH = ROOT / "corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.ocr-contract.json"
CANDIDATE_PAGE = ROOT / "corpus/candidates/perelman-entertaining-physics-book1-1913-ru.md"

EXPECTED_BYTES = 28_168_847
EXPECTED_SHA1 = "3c616f547ff283a2cafd1ac26b448a8e8013f648"
EXPECTED_SHA256 = "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61"
EXPECTED_DJVU_BYTES = 2_982_171
EXPECTED_DJVU_SHA1 = "05c29d01c5dde91bfcfbb6b7ea7f0ea3dba43a12"
EXPECTED_DJVU_SHA256 = "f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462"
EXPECTED_CONTRACT_SHA256 = "f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5"
EXPECTED_STATUS = "scan_binary_frozen_ocr_contract_defined_body_unverified"


class PerelmanProvenanceTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
        self.receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
        self.djvu_receipt = json.loads(DJVU_RECEIPT_PATH.read_text(encoding="utf-8"))
        self.contract = load_contract(CONTRACT_PATH)
        validate_receipt(self.receipt)
        validate_djvu_receipt(self.djvu_receipt)

    def test_structured_trace_is_bound_to_frozen_binary_receipt_and_contract(self) -> None:
        self.assertEqual(self.trace["candidate_id"], "perelman-entertaining-physics-book1-1913-ru")
        boundary = self.trace["public_edition"]["provider_binary_metadata"]
        self.assertTrue(boundary["scriptorium_independently_streamed_binary"])
        self.assertEqual(boundary["scriptorium_byte_count"], EXPECTED_BYTES)
        self.assertEqual(boundary["sha1"], EXPECTED_SHA1)
        self.assertEqual(boundary["scriptorium_sha256"], EXPECTED_SHA256)
        self.assertEqual(boundary["source_free_receipt"], RECEIPT_PATH.name)
        self.assertEqual(
            self.receipt["identity"],
            {
                "byte_count": EXPECTED_BYTES,
                "sha1": EXPECTED_SHA1,
                "sha256": EXPECTED_SHA256,
            },
        )

        contract_boundary = self.trace["public_edition"]["ocr_body_promotion_contract"]
        self.assertEqual(contract_boundary["contract_version"], self.contract["contract_version"])
        self.assertEqual(contract_boundary["source_free_contract"], CONTRACT_PATH.name)
        self.assertEqual(contract_boundary["canonical_sha256"], EXPECTED_CONTRACT_SHA256)
        self.assertEqual(canonical_sha256(self.contract), EXPECTED_CONTRACT_SHA256)
        self.assertEqual(contract_boundary["status"], "defined_unbound")
        self.assertTrue(contract_boundary["scan_identity_bound"])
        self.assertFalse(contract_boundary["page_selection_bound"])
        self.assertFalse(contract_boundary["rasterization_toolchain_bound"])
        self.assertFalse(contract_boundary["ocr_toolchain_bound"])
        self.assertFalse(contract_boundary["body_outputs_frozen"])
        self.assertFalse(contract_boundary["companion_djvu_changes_canonical_carrier"])

    def test_djvu_companion_is_exact_but_not_page_or_ocr_equivalence(self) -> None:
        companions = self.trace["public_edition"]["companion_carriers"]
        self.assertEqual(len(companions), 1)
        djvu = companions[0]
        self.assertEqual(djvu["carrier_format"], "DjVu")
        self.assertEqual(djvu["provider_observed_page_count"], 218)
        self.assertEqual(djvu["provider_reported_byte_count"], EXPECTED_DJVU_BYTES)
        self.assertEqual(djvu["provider_reported_sha1"], EXPECTED_DJVU_SHA1)
        self.assertEqual(djvu["scriptorium_sha256"], EXPECTED_DJVU_SHA256)
        self.assertEqual(djvu["source_free_receipt"], DJVU_RECEIPT_PATH.name)
        self.assertTrue(djvu["scriptorium_independently_streamed_binary"])
        self.assertFalse(djvu["page_equivalence_verified"])
        self.assertFalse(djvu["embedded_text_or_ocr_inspected"])
        self.assertFalse(djvu["canonical_ocr_extraction_carrier_changed"])
        self.assertEqual(
            self.djvu_receipt["identity"],
            {
                "byte_count": EXPECTED_DJVU_BYTES,
                "sha1": EXPECTED_DJVU_SHA1,
                "sha256": EXPECTED_DJVU_SHA256,
            },
        )
        self.assertEqual(self.djvu_receipt["frozen_pdf_sha256"], EXPECTED_SHA256)
        self.assertFalse(self.djvu_receipt["page_equivalence_verified"])
        self.assertFalse(self.djvu_receipt["embedded_text_or_ocr_inspected"])
        self.assertFalse(self.djvu_receipt["canonical_ocr_extraction_carrier_changed"])

    def test_contract_definition_does_not_promote_text_or_fantlab_gates(self) -> None:
        identity = self.trace["public_edition"]["immutable_identity"]
        self.assertEqual(identity["status"], EXPECTED_STATUS)
        unfrozen = "\n".join(identity["unfrozen_components"])
        self.assertIn("OCR", unfrozen)
        self.assertIn("300,000", unfrozen)
        self.assertIn("FantLab", unfrozen)
        self.assertIn("page-level equivalence", unfrozen)

        admissibility = self.trace["admissibility"]
        self.assertEqual(admissibility["status"], EXPECTED_STATUS)
        self.assertFalse(admissibility["minimum_300k_proved_from_frozen_body"])
        self.assertFalse(admissibility["admitted_for_calibration"])
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
        self.assertFalse(self.djvu_receipt["ocr_extraction_profile_frozen"])
        self.assertFalse(self.djvu_receipt["literary_body_count_and_digests_frozen"])
        self.assertFalse(self.djvu_receipt["minimum_300k_proved_from_frozen_body"])
        self.assertFalse(self.djvu_receipt["admitted_for_calibration"])
        self.assertFalse(self.djvu_receipt["diagnostic_ready"])
        self.assertFalse(self.djvu_receipt["m2_parity_admissible"])

    def test_next_evidence_starts_after_unbound_contract(self) -> None:
        next_evidence = "\n".join(self.trace["admissibility"]["next_evidence"])
        self.assertIn("OCR", next_evidence)
        self.assertIn("counts and digests", next_evidence)
        self.assertIn("new independently evidenced contract version", next_evidence)
        self.assertIn("choose and bind the extraction carrier", next_evidence)
        self.assertNotIn("stream and hash", next_evidence)

    def test_public_candidate_page_exposes_identities_without_source_payload(self) -> None:
        page = CANDIDATE_PAGE.read_text(encoding="utf-8")
        self.assertIn(f"**{EXPECTED_BYTES:,} bytes**", page)
        self.assertIn(EXPECTED_SHA1, page)
        self.assertIn(EXPECTED_SHA256, page)
        self.assertIn(f"**{EXPECTED_DJVU_BYTES:,} bytes**", page)
        self.assertIn(EXPECTED_DJVU_SHA1, page)
        self.assertIn(EXPECTED_DJVU_SHA256, page)
        self.assertIn(EXPECTED_CONTRACT_SHA256, page)
        self.assertIn("No PDF/DjVu bytes", page)
        self.assertIn("does **not** change", page)
        self.assertIn("m2_parity_admissible=false", page)


if __name__ == "__main__":
    unittest.main()
