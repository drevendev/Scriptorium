"""Freeze the Petersburg 1916 Commons PDF byte identity without persisting scan bytes.

The remote Commons PDF is streamed transiently. Durable output contains only the
source locator, byte count and cryptographic digests; PDF bytes and OCR are never
written by this module.
"""

from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence
from urllib.request import Request, urlopen

CANDIDATE_ID = "bely-petersburg-1916-ru"
RECEIPT_VERSION = "scriptorium-petersburg-scan-identity-v1"
SCAN_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/3/3c/"
    "%D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B9_%D0%91%D0%B5%D0%BB%D1%8B%D0%B9._"
    "%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3_%281916%29.pdf"
)
FILE_PAGE_URL = (
    "https://commons.wikimedia.org/wiki/File:"
    "%D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B9_%D0%91%D0%B5%D0%BB%D1%8B%D0%B9._"
    "%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3_%281916%29.pdf"
)
EDITION_IDENTITY = "1916_first_book_edition_facsimile"
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
        raise ValueError("Petersburg scan identity shape drift")
    byte_count = identity.get("byte_count")
    if not isinstance(byte_count, int) or isinstance(byte_count, bool) or byte_count <= 0:
        raise ValueError("Petersburg scan byte count is invalid")
    for name, length in (("sha1", 40), ("sha256", 64)):
        digest = identity.get(name)
        if not isinstance(digest, str) or len(digest) != length:
            raise ValueError(f"Petersburg scan {name} is missing or malformed")
        try:
            int(digest, 16)
        except ValueError as exc:
            raise ValueError(f"Petersburg scan {name} is not hexadecimal") from exc


def build_receipt(chunks: Iterable[bytes] | None = None) -> dict[str, object]:
    identity = compute_identity(_remote_chunks() if chunks is None else chunks)
    validate_identity(identity)
    return {
        "receipt_version": RECEIPT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Wikimedia Commons",
        "edition_identity": EDITION_IDENTITY,
        "file_page_url": FILE_PAGE_URL,
        "exact_original_url": SCAN_URL,
        "identity": identity,
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
        "identity",
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
        raise ValueError("Petersburg scan receipt shape drift or unexpected payload key")
    if receipt.get("receipt_version") != RECEIPT_VERSION or receipt.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Petersburg scan receipt identity drift")
    if receipt.get("provider") != "Wikimedia Commons" or receipt.get("edition_identity") != EDITION_IDENTITY:
        raise ValueError("Petersburg scan provider/edition drift")
    if receipt.get("file_page_url") != FILE_PAGE_URL or receipt.get("exact_original_url") != SCAN_URL:
        raise ValueError("Petersburg scan locator drift")
    identity = receipt.get("identity")
    if not isinstance(identity, Mapping):
        raise ValueError("Petersburg scan identity is missing")
    validate_identity(identity)
    if receipt.get("binary_bytes_retrieved_transiently") is not True:
        raise ValueError("Petersburg scan receipt must record transient binary retrieval")
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
        raise ValueError("Petersburg scan receipt advanced a forbidden gate or persisted source")
    if receipt.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("Petersburg scan receipt advanced FantLab source identity")


def verify_receipt(receipt: Mapping[str, object], chunks: Iterable[bytes] | None = None) -> dict[str, object]:
    validate_receipt(receipt)
    observed = build_receipt(chunks)
    if observed != dict(receipt):
        raise ValueError("Petersburg scan byte identity no longer matches frozen receipt")
    identity = observed["identity"]
    assert isinstance(identity, Mapping)
    return {
        "verified": True,
        "candidate_id": CANDIDATE_ID,
        "byte_count": identity["byte_count"],
        "sha1": identity["sha1"],
        "sha256": identity["sha256"],
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
