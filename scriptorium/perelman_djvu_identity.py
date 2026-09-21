"""Freeze the Perelman 1913 Commons DjVu companion byte identity.

The remote Commons DjVu is streamed transiently. Durable output contains only the
source locator, provider cross-check metadata, byte count and cryptographic digests;
DjVu bytes, embedded text/OCR and literary source text are never written by this
module.

This carrier is provenance evidence for the same bibliographic edition as the already
frozen PDF. It is not evidence of page-level equivalence and does not change the
unbound OCR/body extraction contract.
"""

from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence
from urllib.request import Request, urlopen

CANDIDATE_ID = "perelman-entertaining-physics-book1-1913-ru"
RECEIPT_VERSION = "scriptorium-perelman-1913-djvu-companion-identity-v1"
DJVU_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/d/dd/"
    "%D0%9F%D0%B5%D1%80%D0%B5%D0%BB%D1%8C%D0%BC%D0%B0%D0%BD_%D0%AF.%D0%98._"
    "%D0%97%D0%B0%D0%BD%D0%B8%D0%BC%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_"
    "%D1%84%D0%B8%D0%B7%D0%B8%D0%BA%D0%B0._%D0%9A%D0%BD%D0%B8%D0%B3%D0%B0_1_%281913%29.djvu"
)
FILE_PAGE_URL = (
    "https://commons.wikimedia.org/wiki/File:"
    "%D0%9F%D0%B5%D1%80%D0%B5%D0%BB%D1%8C%D0%BC%D0%B0%D0%BD_%D0%AF.%D0%98._"
    "%D0%97%D0%B0%D0%BD%D0%B8%D0%BC%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_"
    "%D1%84%D0%B8%D0%B7%D0%B8%D0%BA%D0%B0._%D0%9A%D0%BD%D0%B8%D0%B3%D0%B0_1_%281913%29.djvu"
)
EDITION_IDENTITY = "1913_first_edition_facsimile_current_2021_djvu_revision"
CURRENT_FILE_REVISION_TIMESTAMP = "2021-08-24T09:31:00Z"
EXPECTED_PROVIDER_PAGE_COUNT = 218
EXPECTED_PROVIDER_BYTE_COUNT = 2_982_171
EXPECTED_PROVIDER_SHA1 = "05c29d01c5dde91bfcfbb6b7ea7f0ea3dba43a12"
FROZEN_PDF_SHA256 = "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61"
CARRIER_RELATIONSHIP = "same_bibliographic_edition_provider_asserted_page_equivalence_unverified"
USER_AGENT = "Scriptorium provenance research/1.0 (+https://github.com/drevendev/Scriptorium)"
CHUNK_SIZE = 1024 * 1024


def _remote_chunks() -> Iterator[bytes]:
    request = Request(
        DJVU_URL,
        headers={"User-Agent": USER_AGENT, "Accept": "image/vnd.djvu,application/octet-stream,*/*"},
    )
    with urlopen(request, timeout=60) as response:
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            yield chunk


def compute_identity(chunks: Iterable[bytes]) -> dict[str, object]:
    sha1_hash = sha1()
    sha256_hash = sha256()
    byte_count = 0
    for chunk in chunks:
        if not isinstance(chunk, bytes):
            raise TypeError("DjVu chunks must be bytes")
        if not chunk:
            continue
        byte_count += len(chunk)
        sha1_hash.update(chunk)
        sha256_hash.update(chunk)
    if byte_count == 0:
        raise ValueError("empty DjVu byte stream")
    return {
        "byte_count": byte_count,
        "sha1": sha1_hash.hexdigest(),
        "sha256": sha256_hash.hexdigest(),
    }


def validate_identity(identity: Mapping[str, object]) -> None:
    if set(identity) != {"byte_count", "sha1", "sha256"}:
        raise ValueError("Perelman DjVu identity shape drift")
    byte_count = identity.get("byte_count")
    if not isinstance(byte_count, int) or isinstance(byte_count, bool) or byte_count <= 0:
        raise ValueError("Perelman DjVu byte count is invalid")
    for name, length in (("sha1", 40), ("sha256", 64)):
        digest = identity.get(name)
        if not isinstance(digest, str) or len(digest) != length:
            raise ValueError(f"Perelman DjVu {name} is missing or malformed")
        try:
            int(digest, 16)
        except ValueError as exc:
            raise ValueError(f"Perelman DjVu {name} is not hexadecimal") from exc


def crosscheck_provider_identity(identity: Mapping[str, object]) -> None:
    validate_identity(identity)
    if identity["byte_count"] != EXPECTED_PROVIDER_BYTE_COUNT:
        raise ValueError("Perelman DjVu byte count no longer matches observed Commons metadata")
    if identity["sha1"] != EXPECTED_PROVIDER_SHA1:
        raise ValueError("Perelman DjVu SHA-1 no longer matches observed Commons metadata")


def verify_identity(expected: Mapping[str, object], chunks: Iterable[bytes]) -> dict[str, object]:
    validate_identity(expected)
    observed = compute_identity(chunks)
    if observed != dict(expected):
        raise ValueError("Perelman DjVu byte identity no longer matches frozen receipt")
    return observed


def build_receipt(chunks: Iterable[bytes] | None = None) -> dict[str, object]:
    identity = compute_identity(_remote_chunks() if chunks is None else chunks)
    crosscheck_provider_identity(identity)
    return {
        "receipt_version": RECEIPT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Wikimedia Commons",
        "carrier_format": "DjVu",
        "media_type": "image/vnd.djvu",
        "edition_identity": EDITION_IDENTITY,
        "file_page_url": FILE_PAGE_URL,
        "exact_original_url": DJVU_URL,
        "current_file_revision_timestamp": CURRENT_FILE_REVISION_TIMESTAMP,
        "provider_observed_page_count": EXPECTED_PROVIDER_PAGE_COUNT,
        "provider_expected_identity": {
            "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
            "sha1": EXPECTED_PROVIDER_SHA1,
        },
        "identity": identity,
        "provider_metadata_crosscheck_passed": True,
        "binary_bytes_retrieved_transiently": True,
        "binary_bytes_committed": False,
        "embedded_text_or_ocr_inspected": False,
        "literary_source_text_included": False,
        "relationship_to_frozen_pdf": CARRIER_RELATIONSHIP,
        "frozen_pdf_sha256": FROZEN_PDF_SHA256,
        "page_equivalence_verified": False,
        "canonical_ocr_extraction_carrier_changed": False,
        "ocr_extraction_profile_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved_from_frozen_body": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }


def validate_receipt(receipt: Mapping[str, object]) -> None:
    required = {
        "receipt_version",
        "candidate_id",
        "provider",
        "carrier_format",
        "media_type",
        "edition_identity",
        "file_page_url",
        "exact_original_url",
        "current_file_revision_timestamp",
        "provider_observed_page_count",
        "provider_expected_identity",
        "identity",
        "provider_metadata_crosscheck_passed",
        "binary_bytes_retrieved_transiently",
        "binary_bytes_committed",
        "embedded_text_or_ocr_inspected",
        "literary_source_text_included",
        "relationship_to_frozen_pdf",
        "frozen_pdf_sha256",
        "page_equivalence_verified",
        "canonical_ocr_extraction_carrier_changed",
        "ocr_extraction_profile_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved_from_frozen_body",
        "admitted_for_calibration",
        "fantlab_source_edition_match",
        "diagnostic_ready",
        "m2_parity_admissible",
    }
    if set(receipt) != required:
        raise ValueError("Perelman DjVu receipt shape drift or unexpected payload key")
    if receipt.get("receipt_version") != RECEIPT_VERSION or receipt.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Perelman DjVu receipt identity drift")
    if receipt.get("provider") != "Wikimedia Commons":
        raise ValueError("Perelman DjVu provider drift")
    if receipt.get("carrier_format") != "DjVu" or receipt.get("media_type") != "image/vnd.djvu":
        raise ValueError("Perelman DjVu carrier-format drift")
    if receipt.get("edition_identity") != EDITION_IDENTITY:
        raise ValueError("Perelman DjVu edition drift")
    if receipt.get("file_page_url") != FILE_PAGE_URL or receipt.get("exact_original_url") != DJVU_URL:
        raise ValueError("Perelman DjVu locator drift")
    if receipt.get("current_file_revision_timestamp") != CURRENT_FILE_REVISION_TIMESTAMP:
        raise ValueError("Perelman DjVu file revision timestamp drift")
    if receipt.get("provider_observed_page_count") != EXPECTED_PROVIDER_PAGE_COUNT:
        raise ValueError("Perelman DjVu provider page-count drift")
    if receipt.get("provider_expected_identity") != {
        "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
        "sha1": EXPECTED_PROVIDER_SHA1,
    }:
        raise ValueError("Perelman DjVu provider expectation drift")
    identity = receipt.get("identity")
    if not isinstance(identity, Mapping):
        raise ValueError("Perelman DjVu identity is missing")
    crosscheck_provider_identity(identity)
    if receipt.get("provider_metadata_crosscheck_passed") is not True:
        raise ValueError("Perelman DjVu receipt must record provider cross-check")
    if receipt.get("binary_bytes_retrieved_transiently") is not True:
        raise ValueError("Perelman DjVu receipt must record transient binary retrieval")
    if receipt.get("relationship_to_frozen_pdf") != CARRIER_RELATIONSHIP:
        raise ValueError("Perelman DjVu/PDF relationship claim drift")
    if receipt.get("frozen_pdf_sha256") != FROZEN_PDF_SHA256:
        raise ValueError("Perelman frozen PDF identity drift")
    expected_false = (
        "binary_bytes_committed",
        "embedded_text_or_ocr_inspected",
        "literary_source_text_included",
        "page_equivalence_verified",
        "canonical_ocr_extraction_carrier_changed",
        "ocr_extraction_profile_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved_from_frozen_body",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    )
    if any(receipt.get(key) is not False for key in expected_false):
        raise ValueError("Perelman DjVu receipt advanced a forbidden equivalence, OCR/body or corpus gate")
    if receipt.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("Perelman DjVu receipt advanced FantLab source identity")


def verify_receipt(receipt: Mapping[str, object], chunks: Iterable[bytes] | None = None) -> dict[str, object]:
    validate_receipt(receipt)
    identity = receipt["identity"]
    assert isinstance(identity, Mapping)
    observed = verify_identity(identity, _remote_chunks() if chunks is None else chunks)
    crosscheck_provider_identity(observed)
    return {
        "verified": True,
        "candidate_id": CANDIDATE_ID,
        "carrier_format": "DjVu",
        "byte_count": observed["byte_count"],
        "sha1": observed["sha1"],
        "sha256": observed["sha256"],
        "provider_metadata_crosscheck_passed": True,
        "page_equivalence_verified": False,
        "embedded_text_or_ocr_inspected": False,
        "binary_bytes_committed": False,
        "admitted_for_calibration": False,
        "m2_parity_admissible": False,
    }


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_object(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--output", type=Path, required=True)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)

    if args.command == "capture":
        receipt = build_receipt()
        validate_receipt(receipt)
        _write_object(args.output, receipt)
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
        return 0

    receipt = _load_object(args.receipt)
    result = verify_receipt(receipt)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
