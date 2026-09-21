"""Freeze the Perelman 1913 Commons PDF byte identity without persisting scan bytes.

The remote Commons PDF is streamed transiently. Durable output contains only the
source locator, provider cross-check metadata, byte count and cryptographic digests;
PDF bytes and OCR are never written by this module.
"""

from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence
from urllib.request import Request, urlopen

CANDIDATE_ID = "perelman-entertaining-physics-book1-1913-ru"
RECEIPT_VERSION = "scriptorium-perelman-1913-scan-identity-v1"
SCAN_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/8/8c/"
    "%D0%9F%D0%B5%D1%80%D0%B5%D0%BB%D1%8C%D0%BC%D0%B0%D0%BD_%D0%AF.%D0%98._"
    "%D0%97%D0%B0%D0%BD%D0%B8%D0%BC%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_"
    "%D1%84%D0%B8%D0%B7%D0%B8%D0%BA%D0%B0._%D0%9A%D0%BD%D0%B8%D0%B3%D0%B0_1_%281913%29.pdf"
)
FILE_PAGE_URL = (
    "https://commons.wikimedia.org/wiki/File:"
    "%D0%9F%D0%B5%D1%80%D0%B5%D0%BB%D1%8C%D0%BC%D0%B0%D0%BD_%D0%AF.%D0%98._"
    "%D0%97%D0%B0%D0%BD%D0%B8%D0%BC%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_"
    "%D1%84%D0%B8%D0%B7%D0%B8%D0%BA%D0%B0._%D0%9A%D0%BD%D0%B8%D0%B3%D0%B0_1_%281913%29.pdf"
)
EDITION_IDENTITY = "1913_first_edition_facsimile_current_2021_revision"
CURRENT_FILE_REVISION_TIMESTAMP = "2021-09-03T09:12:00Z"
EXPECTED_PROVIDER_BYTE_COUNT = 28_168_847
EXPECTED_PROVIDER_SHA1 = "3c616f547ff283a2cafd1ac26b448a8e8013f648"
USER_AGENT = "Scriptorium provenance research/1.0 (+https://github.com/drevendev/Scriptorium)"
CHUNK_SIZE = 1024 * 1024


def _remote_chunks() -> Iterator[bytes]:
    request = Request(SCAN_URL, headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*"})
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
            raise TypeError("scan chunks must be bytes")
        if not chunk:
            continue
        byte_count += len(chunk)
        sha1_hash.update(chunk)
        sha256_hash.update(chunk)
    if byte_count == 0:
        raise ValueError("empty scan byte stream")
    return {
        "byte_count": byte_count,
        "sha1": sha1_hash.hexdigest(),
        "sha256": sha256_hash.hexdigest(),
    }


def validate_identity(identity: Mapping[str, object]) -> None:
    if set(identity) != {"byte_count", "sha1", "sha256"}:
        raise ValueError("Perelman scan identity shape drift")
    byte_count = identity.get("byte_count")
    if not isinstance(byte_count, int) or isinstance(byte_count, bool) or byte_count <= 0:
        raise ValueError("Perelman scan byte count is invalid")
    for name, length in (("sha1", 40), ("sha256", 64)):
        digest = identity.get(name)
        if not isinstance(digest, str) or len(digest) != length:
            raise ValueError(f"Perelman scan {name} is missing or malformed")
        try:
            int(digest, 16)
        except ValueError as exc:
            raise ValueError(f"Perelman scan {name} is not hexadecimal") from exc


def crosscheck_provider_identity(identity: Mapping[str, object]) -> None:
    validate_identity(identity)
    if identity["byte_count"] != EXPECTED_PROVIDER_BYTE_COUNT:
        raise ValueError("Perelman scan byte count no longer matches observed Commons metadata")
    if identity["sha1"] != EXPECTED_PROVIDER_SHA1:
        raise ValueError("Perelman scan SHA-1 no longer matches observed Commons metadata")


def verify_identity(expected: Mapping[str, object], chunks: Iterable[bytes]) -> dict[str, object]:
    validate_identity(expected)
    observed = compute_identity(chunks)
    if observed != dict(expected):
        raise ValueError("Perelman scan byte identity no longer matches frozen receipt")
    return observed


def build_receipt(chunks: Iterable[bytes] | None = None) -> dict[str, object]:
    identity = compute_identity(_remote_chunks() if chunks is None else chunks)
    crosscheck_provider_identity(identity)
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
        "identity": identity,
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


def validate_receipt(receipt: Mapping[str, object]) -> None:
    required = {
        "receipt_version",
        "candidate_id",
        "provider",
        "edition_identity",
        "file_page_url",
        "exact_original_url",
        "current_file_revision_timestamp",
        "provider_expected_identity",
        "identity",
        "provider_metadata_crosscheck_passed",
        "binary_bytes_retrieved_transiently",
        "binary_bytes_committed",
        "ocr_included",
        "literary_source_text_included",
        "ocr_extraction_profile_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved_from_frozen_body",
        "admitted_for_calibration",
        "fantlab_source_edition_match",
        "diagnostic_ready",
        "m2_parity_admissible",
    }
    if set(receipt) != required:
        raise ValueError("Perelman scan receipt shape drift or unexpected payload key")
    if receipt.get("receipt_version") != RECEIPT_VERSION or receipt.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Perelman scan receipt identity drift")
    if receipt.get("provider") != "Wikimedia Commons" or receipt.get("edition_identity") != EDITION_IDENTITY:
        raise ValueError("Perelman scan provider/edition drift")
    if receipt.get("file_page_url") != FILE_PAGE_URL or receipt.get("exact_original_url") != SCAN_URL:
        raise ValueError("Perelman scan locator drift")
    if receipt.get("current_file_revision_timestamp") != CURRENT_FILE_REVISION_TIMESTAMP:
        raise ValueError("Perelman scan file revision timestamp drift")
    expected_provider = receipt.get("provider_expected_identity")
    if expected_provider != {
        "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
        "sha1": EXPECTED_PROVIDER_SHA1,
    }:
        raise ValueError("Perelman scan provider expectation drift")
    identity = receipt.get("identity")
    if not isinstance(identity, Mapping):
        raise ValueError("Perelman scan identity is missing")
    crosscheck_provider_identity(identity)
    if receipt.get("provider_metadata_crosscheck_passed") is not True:
        raise ValueError("Perelman scan receipt must record provider cross-check")
    if receipt.get("binary_bytes_retrieved_transiently") is not True:
        raise ValueError("Perelman scan receipt must record transient binary retrieval")
    expected_false = (
        "binary_bytes_committed",
        "ocr_included",
        "literary_source_text_included",
        "ocr_extraction_profile_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved_from_frozen_body",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    )
    if any(receipt.get(key) is not False for key in expected_false):
        raise ValueError("Perelman scan receipt advanced a forbidden gate or persisted source")
    if receipt.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("Perelman scan receipt advanced FantLab source identity")


def verify_receipt(receipt: Mapping[str, object], chunks: Iterable[bytes] | None = None) -> dict[str, object]:
    validate_receipt(receipt)
    identity = receipt["identity"]
    assert isinstance(identity, Mapping)
    observed = verify_identity(identity, _remote_chunks() if chunks is None else chunks)
    crosscheck_provider_identity(observed)
    return {
        "verified": True,
        "candidate_id": CANDIDATE_ID,
        "byte_count": observed["byte_count"],
        "sha1": observed["sha1"],
        "sha256": observed["sha256"],
        "provider_metadata_crosscheck_passed": True,
        "binary_bytes_committed": False,
        "ocr_extraction_profile_frozen": False,
        "admitted_for_calibration": False,
        "m2_parity_admissible": False,
    }


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


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
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
        return 0

    receipt = _load_object(args.receipt)
    result = verify_receipt(receipt)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
