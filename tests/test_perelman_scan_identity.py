from __future__ import annotations

from copy import deepcopy
from hashlib import sha1, sha256
import unittest

from scriptorium.perelman_scan_identity import (
    CANDIDATE_ID,
    CURRENT_FILE_REVISION_TIMESTAMP,
    EDITION_IDENTITY,
    EXPECTED_PROVIDER_BYTE_COUNT,
    EXPECTED_PROVIDER_SHA1,
    FILE_PAGE_URL,
    RECEIPT_VERSION,
    SCAN_URL,
    compute_identity,
    crosscheck_provider_identity,
    validate_identity,
    validate_receipt,
    verify_identity,
)


def production_receipt() -> dict[str, object]:
    return {
        "receipt_version": RECEIPT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Wikimedia Commons",
        "edition_identity": EDITION_IDENTITY,
        "file_page_url": FILE_PAGE_URL,
        "exact_original_url": SCAN_URL,
        "current_file_revision_timestamp": CURRENT_FILE_REVISION_TIMESTAMP,
        "provider_expected_identity": {
            "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
            "sha1": EXPECTED_PROVIDER_SHA1,
        },
        "identity": {
            "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
            "sha1": EXPECTED_PROVIDER_SHA1,
            "sha256": "1" * 64,
        },
        "provider_metadata_crosscheck_passed": True,
        "binary_bytes_retrieved_transiently": True,
        "binary_bytes_committed": False,
        "ocr_included": False,
        "literary_source_text_included": False,
        "ocr_extraction_profile_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved_from_frozen_body": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }


class PerelmanScanIdentityTests(unittest.TestCase):
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

    def test_provider_crosscheck_rejects_byte_or_sha1_drift(self) -> None:
        identity = production_receipt()["identity"]
        assert isinstance(identity, dict)
        crosscheck_provider_identity(identity)
        with self.assertRaisesRegex(ValueError, "byte count"):
            crosscheck_provider_identity(dict(identity, byte_count=EXPECTED_PROVIDER_BYTE_COUNT - 1))
        with self.assertRaisesRegex(ValueError, "SHA-1"):
            crosscheck_provider_identity(dict(identity, sha1="0" * 40))

    def test_receipt_validator_keeps_downstream_gates_closed(self) -> None:
        receipt = production_receipt()
        validate_receipt(receipt)
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

    def test_receipt_validator_rejects_payload_provider_or_gate_drift(self) -> None:
        receipt = production_receipt()
        leaked = deepcopy(receipt)
        leaked["pdf_bytes"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "shape drift"):
            validate_receipt(leaked)

        provider_drift = deepcopy(receipt)
        provider_drift["provider_expected_identity"]["byte_count"] = EXPECTED_PROVIDER_BYTE_COUNT - 1
        with self.assertRaisesRegex(ValueError, "provider expectation"):
            validate_receipt(provider_drift)

        advanced = deepcopy(receipt)
        advanced["admitted_for_calibration"] = True
        with self.assertRaisesRegex(ValueError, "forbidden gate"):
            validate_receipt(advanced)

    def test_verify_identity_accepts_exact_replay_and_rejects_drift(self) -> None:
        payload = b"abcdef"
        identity = compute_identity([payload])
        self.assertEqual(verify_identity(identity, [b"abc", b"def"]), identity)
        with self.assertRaisesRegex(ValueError, "no longer matches"):
            verify_identity(identity, [b"different"])


if __name__ == "__main__":
    unittest.main()
