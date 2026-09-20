from __future__ import annotations

from copy import deepcopy
from hashlib import sha1, sha256
import unittest

from scriptorium.petersburg_scan_identity import (
    CANDIDATE_ID,
    EDITION_IDENTITY,
    FILE_PAGE_URL,
    RECEIPT_VERSION,
    SCAN_URL,
    build_receipt,
    compute_identity,
    validate_identity,
    validate_receipt,
    verify_receipt,
)


class PetersburgScanIdentityTests(unittest.TestCase):
    def test_compute_identity_streams_chunks_deterministically(self) -> None:
        chunks = [b"abc", b"", b"def"]
        identity = compute_identity(chunks)
        payload = b"abcdef"
        self.assertEqual(identity["byte_count"], len(payload))
        self.assertEqual(identity["sha1"], sha1(payload).hexdigest())
        self.assertEqual(identity["sha256"], sha256(payload).hexdigest())

    def test_compute_identity_rejects_empty_and_non_bytes(self) -> None:
        with self.assertRaisesRegex(ValueError, "empty"):
            compute_identity([])
        with self.assertRaisesRegex(TypeError, "bytes"):
            compute_identity([b"ok", "not-bytes"])  # type: ignore[list-item]

    def test_identity_validator_fails_closed(self) -> None:
        identity = {
            "byte_count": 6,
            "sha1": sha1(b"abcdef").hexdigest(),
            "sha256": sha256(b"abcdef").hexdigest(),
        }
        validate_identity(identity)
        with self.assertRaisesRegex(ValueError, "byte count"):
            validate_identity(dict(identity, byte_count=0))
        with self.assertRaisesRegex(ValueError, "sha1"):
            validate_identity(dict(identity, sha1="not-a-digest"))
        extra = dict(identity)
        extra["pdf_bytes"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "shape drift"):
            validate_identity(extra)

    def test_build_and_validate_receipt_keep_downstream_gates_closed(self) -> None:
        receipt = build_receipt([b"abc", b"def"])
        validate_receipt(receipt)
        self.assertEqual(receipt["candidate_id"], CANDIDATE_ID)
        self.assertEqual(receipt["receipt_version"], RECEIPT_VERSION)
        self.assertEqual(receipt["edition_identity"], EDITION_IDENTITY)
        self.assertEqual(receipt["file_page_url"], FILE_PAGE_URL)
        self.assertEqual(receipt["exact_original_url"], SCAN_URL)
        self.assertFalse(receipt["binary_bytes_committed"])
        self.assertFalse(receipt["ocr_included"])
        self.assertFalse(receipt["literary_source_text_included"])
        self.assertFalse(receipt["ocr_extraction_profile_frozen"])
        self.assertFalse(receipt["literary_body_count_and_digests_frozen"])
        self.assertFalse(receipt["minimum_300k_proved_from_frozen_body"])
        self.assertFalse(receipt["admitted_for_calibration"])
        self.assertEqual(receipt["fantlab_source_edition_match"], "unknown")
        self.assertFalse(receipt["diagnostic_ready"])
        self.assertFalse(receipt["m2_parity_admissible"])

    def test_receipt_validator_rejects_payload_or_gate_drift(self) -> None:
        receipt = build_receipt([b"abcdef"])
        leaked = deepcopy(receipt)
        leaked["pdf_bytes"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "shape drift"):
            validate_receipt(leaked)
        advanced = deepcopy(receipt)
        advanced["admitted_for_calibration"] = True
        with self.assertRaisesRegex(ValueError, "forbidden gate"):
            validate_receipt(advanced)
        wrong_edition = deepcopy(receipt)
        wrong_edition["edition_identity"] = "1922_revision"
        with self.assertRaisesRegex(ValueError, "provider/edition drift"):
            validate_receipt(wrong_edition)

    def test_verify_receipt_accepts_exact_replay_and_rejects_drift(self) -> None:
        receipt = build_receipt([b"abcdef"])
        result = verify_receipt(receipt, chunks=[b"abc", b"def"])
        self.assertTrue(result["verified"])
        self.assertEqual(result["sha256"], sha256(b"abcdef").hexdigest())
        with self.assertRaisesRegex(ValueError, "no longer matches"):
            verify_receipt(receipt, chunks=[b"different"])


if __name__ == "__main__":
    unittest.main()
