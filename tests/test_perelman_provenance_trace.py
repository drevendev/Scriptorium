from __future__ import annotations

import json
from pathlib import Path
import unittest

from scriptorium.perelman_scan_identity import validate_receipt


ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT / "corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.json"
RECEIPT_PATH = ROOT / "corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.scan-identity.json"
CANDIDATE_PAGE = ROOT / "corpus/candidates/perelman-entertaining-physics-book1-1913-ru.md"

EXPECTED_BYTES = 28_168_847
EXPECTED_SHA1 = "3c616f547ff283a2cafd1ac26b448a8e8013f648"
EXPECTED_SHA256 = "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61"


class PerelmanProvenanceTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
        self.receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
        validate_receipt(self.receipt)

    def test_structured_trace_is_bound_to_frozen_binary_receipt(self) -> None:
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

    def test_binary_freeze_does_not_promote_text_or_fantlab_gates(self) -> None:
        identity = self.trace["public_edition"]["immutable_identity"]
        self.assertEqual(identity["status"], "scan_binary_frozen_ocr_body_unverified")
        unfrozen = "\n".join(identity["unfrozen_components"])
        self.assertIn("OCR", unfrozen)
        self.assertIn("300,000", unfrozen)
        self.assertIn("FantLab", unfrozen)

        admissibility = self.trace["admissibility"]
        self.assertEqual(admissibility["status"], "scan_binary_frozen_ocr_body_unverified")
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

    def test_next_evidence_starts_after_binary_freeze(self) -> None:
        next_evidence = "\n".join(self.trace["admissibility"]["next_evidence"])
        self.assertIn("OCR", next_evidence)
        self.assertIn("character count", next_evidence)
        self.assertNotIn("stream and hash", next_evidence)

    def test_public_candidate_page_exposes_identity_without_source_payload(self) -> None:
        page = CANDIDATE_PAGE.read_text(encoding="utf-8")
        self.assertIn(f"**{EXPECTED_BYTES:,} bytes**", page)
        self.assertIn(EXPECTED_SHA1, page)
        self.assertIn(EXPECTED_SHA256, page)
        self.assertIn("No PDF bytes", page)
        self.assertIn("m2_parity_admissible=false", page)


if __name__ == "__main__":
    unittest.main()
