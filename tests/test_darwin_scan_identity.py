from __future__ import annotations

from copy import deepcopy
from hashlib import sha1, sha256
import unittest

from scriptorium.darwin_scan_identity import (
    CANDIDATE_ID,
    EXPECTED_PROVIDER_BYTE_COUNT,
    EXPECTED_PROVIDER_SHA1,
    FILE_PAGE_URL,
    RECEIPT_VERSION,
    SCAN_URL,
    compute_identity,
    validate_provider_identity,
    validate_receipt,
    verify_receipt,
)


class DarwinScanIdentityTests(unittest.TestCase):
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

    def test_provider_crosscheck_fails_closed(self) -> None:
        valid_shape = {
            "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
            "sha1": EXPECTED_PROVIDER_SHA1,
            "sha256": "0" * 64,
        }
        validate_provider_identity(valid_shape)
        wrong_count = dict(valid_shape, byte_count=EXPECTED_PROVIDER_BYTE_COUNT + 1)
        with self.assertRaisesRegex(ValueError, "byte-count drift"):
            validate_provider_identity(wrong_count)
        wrong_sha1 = dict(valid_shape, sha1="0" * 40)
        with self.assertRaisesRegex(ValueError, "SHA-1 drift"):
            validate_provider_identity(wrong_sha1)

    def test_receipt_validator_keeps_downstream_gates_closed(self) -> None:
        receipt = self._synthetic_receipt()
        validate_receipt(receipt)
        self.assertFalse(receipt["binary_bytes_committed"])
        self.assertFalse(receipt["source_text_included"])
        self.assertFalse(receipt["literary_body_count_and_digests_frozen"])
        self.assertFalse(receipt["minimum_300k_proved"])
        self.assertFalse(receipt["admitted_for_calibration"])
        self.assertEqual(receipt["fantlab_source_edition_match"], "unknown")
        self.assertFalse(receipt["m2_parity_admissible"])

    def test_receipt_validator_rejects_payload_or_gate_drift(self) -> None:
        receipt = self._synthetic_receipt()
        leaked = deepcopy(receipt)
        leaked["djvu_bytes"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "shape drift"):
            validate_receipt(leaked)
        advanced = deepcopy(receipt)
        advanced["admitted_for_calibration"] = True
        with self.assertRaisesRegex(ValueError, "forbidden gate"):
            validate_receipt(advanced)

    def test_verify_receipt_rejects_observed_binary_drift(self) -> None:
        receipt = self._synthetic_receipt()
        with self.assertRaisesRegex(ValueError, "byte-count drift"):
            verify_receipt(receipt, chunks=[b"different"])

    @staticmethod
    def _synthetic_receipt() -> dict[str, object]:
        return {
            "receipt_version": RECEIPT_VERSION,
            "candidate_id": CANDIDATE_ID,
            "provider": "Wikimedia Commons",
            "file_page_url": FILE_PAGE_URL,
            "exact_original_url": SCAN_URL,
            "identity": {
                "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
                "sha1": EXPECTED_PROVIDER_SHA1,
                "sha256": "0" * 64,
            },
            "provider_metadata_crosscheck": {
                "expected_byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
                "expected_sha1": EXPECTED_PROVIDER_SHA1,
                "byte_count_match": True,
                "sha1_match": True,
            },
            "binary_bytes_retrieved_transiently": True,
            "binary_bytes_committed": False,
            "source_text_included": False,
            "literary_body_count_and_digests_frozen": False,
            "minimum_300k_proved": False,
            "admitted_for_calibration": False,
            "fantlab_source_edition_match": "unknown",
            "diagnostic_ready": False,
            "m2_parity_admissible": False,
        }


if __name__ == "__main__":
    unittest.main()
