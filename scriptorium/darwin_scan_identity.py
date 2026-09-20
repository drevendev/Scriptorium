"""Independently freeze the Darwin/Rachinsky 1864 DjVu byte identity.

The remote Commons DjVu is streamed transiently. Durable output contains only the
source locator, byte count and checksums; scan bytes are never written by this module.
"""

from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence
from urllib.request import Request, urlopen

CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
RECEIPT_VERSION = "scriptorium-darwin-scan-identity-v1"
SCAN_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/2/2f/"
    "%D0%94%D0%B0%D1%80%D0%B2%D0%B8%D0%BD_-_%D0%9E_%D0%BF%D1%80%D0%BE%D0%B8%D1%81%D1%85%D0%BE%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B8_"
    "%D0%B2%D0%B8%D0%B4%D0%BE%D0%B2%2C_1864.djvu"
)
FILE_PAGE_URL = (
    "https://commons.wikimedia.org/wiki/File:"
    "%D0%94%D0%B0%D1%80%D0%B2%D0%B8%D0%BD_-_%D0%9E_%D0%BF%D1%80%D0%BE%D0%B8%D1%81%D1%85%D0%BE%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B8_"
    "%D0%B2%D0%B8%D0%B4%D0%BE%D0%B2%2C_1864.djvu"
)
EXPECTED_PROVIDER_BYTE_COUNT = 27_368_263
EXPECTED_PROVIDER_SHA1 = "75ef508588194ae74874272ce290f3ec1043ea9b"
USER_AGENT = "Scriptorium provenance research/1.0 (+https://github.com/drevendev/Scriptorium)"
CHUNK_SIZE = 1024 * 1024


def _remote_chunks() -> Iterator[bytes]:
    request = Request(SCAN_URL, headers={"User-Agent": USER_AGENT, "Accept": "image/vnd.djvu,*/*"})
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


def validate_provider_identity(identity: Mapping[str, object]) -> None:
    if identity.get("byte_count") != EXPECTED_PROVIDER_BYTE_COUNT:
        raise ValueError(
            "Darwin scan byte-count drift: "
            f"expected {EXPECTED_PROVIDER_BYTE_COUNT}, got {identity.get('byte_count')!r}"
        )
    if identity.get("sha1") != EXPECTED_PROVIDER_SHA1:
        raise ValueError(
            "Darwin scan SHA-1 drift: "
            f"expected {EXPECTED_PROVIDER_SHA1}, got {identity.get('sha1')!r}"
        )
    digest = identity.get("sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ValueError("Darwin scan SHA-256 is missing or malformed")
    try:
        int(digest, 16)
    except ValueError as exc:
        raise ValueError("Darwin scan SHA-256 is not hexadecimal") from exc


def build_receipt(chunks: Iterable[bytes] | None = None) -> dict[str, object]:
    identity = compute_identity(_remote_chunks() if chunks is None else chunks)
    validate_provider_identity(identity)
    return {
        "receipt_version": RECEIPT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Wikimedia Commons",
        "file_page_url": FILE_PAGE_URL,
        "exact_original_url": SCAN_URL,
        "identity": identity,
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


def validate_receipt(receipt: Mapping[str, object]) -> None:
    required = {
        "receipt_version",
        "candidate_id",
        "provider",
        "file_page_url",
        "exact_original_url",
        "identity",
        "provider_metadata_crosscheck",
        "binary_bytes_retrieved_transiently",
        "binary_bytes_committed",
        "source_text_included",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "admitted_for_calibration",
        "fantlab_source_edition_match",
        "diagnostic_ready",
        "m2_parity_admissible",
    }
    if set(receipt) != required:
        raise ValueError("Darwin scan receipt shape drift or unexpected payload key")
    if receipt.get("receipt_version") != RECEIPT_VERSION or receipt.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin scan receipt identity drift")
    if receipt.get("provider") != "Wikimedia Commons":
        raise ValueError("Darwin scan provider drift")
    if receipt.get("file_page_url") != FILE_PAGE_URL or receipt.get("exact_original_url") != SCAN_URL:
        raise ValueError("Darwin scan locator drift")
    identity = receipt.get("identity")
    if not isinstance(identity, Mapping) or set(identity) != {"byte_count", "sha1", "sha256"}:
        raise ValueError("Darwin scan identity shape drift")
    validate_provider_identity(identity)
    if receipt.get("provider_metadata_crosscheck") != {
        "expected_byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
        "expected_sha1": EXPECTED_PROVIDER_SHA1,
        "byte_count_match": True,
        "sha1_match": True,
    }:
        raise ValueError("Darwin scan provider cross-check drift")
    expected_false = (
        "binary_bytes_committed",
        "source_text_included",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    )
    if receipt.get("binary_bytes_retrieved_transiently") is not True:
        raise ValueError("Darwin scan receipt must record transient binary retrieval")
    if any(receipt.get(key) is not False for key in expected_false):
        raise ValueError("Darwin scan receipt advanced a forbidden gate or persisted source")
    if receipt.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("Darwin scan receipt advanced FantLab source identity")


def verify_receipt(receipt: Mapping[str, object], chunks: Iterable[bytes] | None = None) -> dict[str, object]:
    validate_receipt(receipt)
    observed = build_receipt(chunks)
    if observed != dict(receipt):
        raise ValueError("Darwin scan byte identity no longer matches frozen receipt")
    return {
        "verified": True,
        "candidate_id": CANDIDATE_ID,
        "byte_count": observed["identity"]["byte_count"],
        "sha1": observed["identity"]["sha1"],
        "sha256": observed["identity"]["sha256"],
        "binary_bytes_committed": False,
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
