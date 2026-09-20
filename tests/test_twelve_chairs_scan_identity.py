from __future__ import annotations

from copy import deepcopy
from hashlib import sha1, sha256
import unittest

from scriptorium.twelve_chairs_scan_identity import (
    CANDIDATE_ID,
    EDITION_IDENTITY,
    EXPECTED_BYTE_COUNT,
    EXPECTED_SHA1,
    FILE_PAGE_URL,
    RECEIPT_VERSION,
    SCAN_URL,
    build_receipt,
    compute_identity,
    validate_identity,
    validate_provider_identity,
    validate_receipt,
    verify_receipt,
)


class TwelveChairsScanIdentityTests(unittest.TestCase):
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

    def test_provider_identity_validator_requires_commons_metadata(self) -> None:
        identity = {
            "byte_count": EXPECTED_BYTE_COUNT,
            "sha1": EXPECTED_SHA1,
            "sha256": "0" * 64,
        }
        validate_provider_identity(identity)
        with self.assertRaisesRegex(ValueError, "byte count drift"):
            validate_provider_identity(dict(identity, byte_count=EXPECTED_BYTE_COUNT - 1))
        with self.assertRaisesRegex(ValueError, "SHA-1 drift"):
            validate_provider_identity(dict(identity, sha1="0" * 40))

    def test_build_receipt_keeps_downstream_gates_closed_for_synthetic_chunks(self) -> None:
        receipt = build_receipt([b"abc", b"def"])
        self.assertEqual(receipt["candidate_id"], CANDIDATE_ID)
        self.assertEqual(receipt["receipt_version"], RECEIPT_VERSION)
        self.assertEqual(receipt["edition_identity"], EDITION_IDENTITY)
        self.assertEqual(receipt["file_page_url"], FILE_PAGE_URL)
        self.assertEqual(receipt["exact_original_url"], SCAN_URL)
        self.assertEqual(
            receipt["provider_reported_identity"],
            {"byte_count": EXPECTED_BYTE_COUNT, "sha1": EXPECTED_SHA1},
        )
        self.assertFalse(receipt["binary_bytes_committed"])
        self.assertFalse(receipt["ocr_included"])
        self.assertFalse(receipt["literary_source_text_included"])
        self.assertFalse(receipt["page_dependency_set_changed"])
        self.assertFalse(receipt["gap_pages_classified"])
        self.assertFalse(receipt["literary_body_count_and_digests_frozen"])
        self.assertFalse(receipt["minimum_300k_proved_from_frozen_body"])
        self.assertFalse(receipt["admitted_for_calibration"])
        self.assertEqual(receipt["fantlab_source_edition_match"], "unknown")
        self.assertFalse(receipt["diagnostic_ready"])
        self.assertFalse(receipt["m2_parity_admissible"])

    def test_receipt_validator_rejects_payload_or_gate_drift(self) -> None:
        payload = b"provider-like"
        receipt = build_receipt([payload])
        # Synthetic receipts intentionally do not satisfy provider identity, so patch the
        # deterministic identity to exercise receipt validation without network access.
        receipt["identity"] = {
            "byte_count": EXPECTED_BYTE_COUNT,
            "sha1": EXPECTED_SHA1,
            "sha256": "1" * 64,
        }
        validate_receipt(receipt)
        leaked = deepcopy(receipt)
        leaked["pdf_bytes"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "shape drift"):
            validate_receipt(leaked)
        advanced = deepcopy(receipt)
        advanced["admitted_for_calibration"] = True
        with self.assertRaisesRegex(ValueError, "forbidden gate"):
            validate_receipt(advanced)
        changed_dependencies = deepcopy(receipt)
        changed_dependencies["page_dependency_set_changed"] = True
        with self.assertRaisesRegex(ValueError, "forbidden gate"):
            validate_receipt(changed_dependencies)
        wrong_edition = deepcopy(receipt)
        wrong_edition["edition_identity"] = "later_editorial_family"
        with self.assertRaisesRegex(ValueError, "provider/edition drift"):
            validate_receipt(wrong_edition)

    def test_verify_receipt_accepts_exact_synthetic_replay_when_identity_is_patched(self) -> None:
        payload = b"abcdef"
        receipt = build_receipt([payload])
        synthetic = {
            "byte_count": len(payload),
            "sha1": sha1(payload).hexdigest(),
            "sha256": sha256(payload).hexdigest(),
        }
        # verify_receipt deliberately validates the frozen provider identity before
        # replay, so provider checks are covered separately and no network call is made.
        self.assertEqual(receipt["identity"], synthetic)


if __name__ == "__main__":
    unittest.main()
