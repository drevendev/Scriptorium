from __future__ import annotations

import json
from pathlib import Path
import unittest

from scriptorium.petersburg_scan_identity import validate_receipt


ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT / "corpus/candidates/source-edition-traces/bely-petersburg-1916-ru.json"
RECEIPT_PATH = ROOT / "corpus/candidates/source-edition-traces/bely-petersburg-1916-ru.scan-identity.json"
CANDIDATE_PAGE = ROOT / "corpus/candidates/bely-petersburg-1916-ru.md"

EXPECTED_BYTES = 3_621_459
EXPECTED_SHA1 = "682476934dd6ed49c6bbcdb0720127c1812ff477"
EXPECTED_SHA256 = "b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5"


class PetersburgProvenanceTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
        self.receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
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

    def test_binary_freeze_does_not_promote_text_or_fantlab_gates(self) -> None:
        identity = self.trace["public_edition"]["immutable_identity"]
        self.assertEqual(identity["status"], "scan_binary_frozen_text_body_unfrozen")
        unfrozen = "\n".join(identity["unfrozen_components"])
        self.assertIn("OCR", unfrozen)
        self.assertIn("literary-text", unfrozen)
        self.assertIn("FantLab", unfrozen)

        admissibility = self.trace["admissibility"]
        self.assertEqual(admissibility["status"], "scan_binary_frozen_ocr_body_unfrozen")
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

    def test_next_evidence_starts_after_binary_freeze(self) -> None:
        next_evidence = "\n".join(self.trace["admissibility"]["next_evidence"])
        self.assertIn("OCR extraction contract", next_evidence)
        self.assertIn("literary-body character count", next_evidence)
        self.assertNotIn("Retrieve one specific Commons PDF snapshot", next_evidence)

    def test_public_candidate_page_exposes_identity_without_source_payload(self) -> None:
        page = CANDIDATE_PAGE.read_text(encoding="utf-8")
        self.assertIn(f"**{EXPECTED_BYTES:,}**", page)
        self.assertIn(EXPECTED_SHA1, page)
        self.assertIn(EXPECTED_SHA256, page)
        self.assertIn("No PDF bytes", page)
        self.assertIn("m2_parity_admissible=false", page)


if __name__ == "__main__":
    unittest.main()
