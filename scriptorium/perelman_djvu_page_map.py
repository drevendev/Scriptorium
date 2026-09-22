"""Freeze source-free per-page fingerprints for the Perelman 1913 DjVu text layer.

The exact Commons DjVu is retrieved transiently and verified before ``djvutxt`` runs.
Durable output contains page numbers, counts and cryptographic digests only. Hidden
text, page images and literary source bytes are never retained by this module.

This is provenance evidence for a later literary-page selection. It deliberately does
not choose literary pages, bind a canonical extraction carrier, freeze a literary body,
or advance corpus/FantLab parity gates.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Mapping, Sequence

from .perelman_djvu_identity import (
    CANDIDATE_ID,
    DJVU_URL,
    EXPECTED_PROVIDER_BYTE_COUNT,
    EXPECTED_PROVIDER_PAGE_COUNT,
    EXPECTED_PROVIDER_SHA1,
)
from .perelman_djvu_text_layer import (
    EXPECTED_CARRIER_SHA256,
    EXPECTED_PACKAGE_VERSION,
    TOOL_NAME,
    TOOL_PACKAGE,
    _download_verified_djvu,
    _run_djvutxt,
)
from .text import NORMALIZATION_PROFILE, normalize_text

PAGE_MAP_VERSION = "scriptorium-perelman-1913-djvu-page-map-v1"


def _digest_json(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(payload).hexdigest()


def _page_record(page: int, payload: bytes) -> dict[str, object]:
    text = payload.decode("utf-8", errors="strict")
    normalized = normalize_text(text)
    return {
        "page": page,
        "utf8_byte_count": len(payload),
        "character_count": len(text),
        "sha256": sha256(payload).hexdigest(),
        "normalized_profile": NORMALIZATION_PROFILE,
        "normalized_character_count": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }


def build_page_map(page_outputs: Sequence[bytes], *, package_version: str) -> dict[str, object]:
    if len(page_outputs) != EXPECTED_PROVIDER_PAGE_COUNT:
        raise ValueError("Perelman DjVu page-output count does not match frozen carrier")
    if package_version != EXPECTED_PACKAGE_VERSION:
        raise ValueError("Perelman DjVu page-map package version drift")

    pages = [_page_record(index + 1, payload) for index, payload in enumerate(page_outputs)]
    result = {
        "page_map_version": PAGE_MAP_VERSION,
        "candidate_id": CANDIDATE_ID,
        "carrier": {
            "format": "DjVu",
            "exact_original_url": DJVU_URL,
            "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
            "sha1": EXPECTED_PROVIDER_SHA1,
            "sha256": EXPECTED_CARRIER_SHA256,
            "page_count": EXPECTED_PROVIDER_PAGE_COUNT,
            "identity_reverified_before_extraction": True,
        },
        "extractor": {
            "tool": TOOL_NAME,
            "package": TOOL_PACKAGE,
            "package_version": package_version,
            "mode": "hidden_text_utf8_per_page",
        },
        "pages": pages,
        "page_records_sha256": _digest_json(pages),
        "source_text_included": False,
        "page_images_committed": False,
        "binary_bytes_committed": False,
        "page_equivalence_to_pdf_verified": False,
        "literary_page_selection_frozen": False,
        "canonical_ocr_extraction_carrier_changed": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved_from_frozen_body": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    validate_page_map(result)
    return result


def _validate_digest(value: object, *, name: str) -> None:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"Perelman DjVu page-map {name} is malformed")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(f"Perelman DjVu page-map {name} is not hexadecimal") from exc


def validate_page_map(page_map: Mapping[str, object]) -> None:
    required = {
        "page_map_version",
        "candidate_id",
        "carrier",
        "extractor",
        "pages",
        "page_records_sha256",
        "source_text_included",
        "page_images_committed",
        "binary_bytes_committed",
        "page_equivalence_to_pdf_verified",
        "literary_page_selection_frozen",
        "canonical_ocr_extraction_carrier_changed",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved_from_frozen_body",
        "admitted_for_calibration",
        "fantlab_source_edition_match",
        "diagnostic_ready",
        "m2_parity_admissible",
    }
    if set(page_map) != required:
        raise ValueError("Perelman DjVu page-map shape drift")
    if page_map.get("page_map_version") != PAGE_MAP_VERSION or page_map.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Perelman DjVu page-map identity drift")

    carrier = page_map.get("carrier")
    if not isinstance(carrier, Mapping) or set(carrier) != {
        "format", "exact_original_url", "byte_count", "sha1", "sha256", "page_count", "identity_reverified_before_extraction"
    }:
        raise ValueError("Perelman DjVu page-map carrier shape drift")
    if carrier.get("format") != "DjVu" or carrier.get("exact_original_url") != DJVU_URL:
        raise ValueError("Perelman DjVu page-map carrier locator drift")
    if carrier.get("byte_count") != EXPECTED_PROVIDER_BYTE_COUNT or carrier.get("sha1") != EXPECTED_PROVIDER_SHA1:
        raise ValueError("Perelman DjVu page-map provider identity drift")
    if carrier.get("sha256") != EXPECTED_CARRIER_SHA256 or carrier.get("page_count") != EXPECTED_PROVIDER_PAGE_COUNT:
        raise ValueError("Perelman DjVu page-map frozen carrier identity drift")
    if carrier.get("identity_reverified_before_extraction") is not True:
        raise ValueError("Perelman DjVu page-map requires carrier re-verification")

    extractor = page_map.get("extractor")
    if not isinstance(extractor, Mapping) or set(extractor) != {"tool", "package", "package_version", "mode"}:
        raise ValueError("Perelman DjVu page-map extractor shape drift")
    if (
        extractor.get("tool") != TOOL_NAME
        or extractor.get("package") != TOOL_PACKAGE
        or extractor.get("package_version") != EXPECTED_PACKAGE_VERSION
        or extractor.get("mode") != "hidden_text_utf8_per_page"
    ):
        raise ValueError("Perelman DjVu page-map extractor identity drift")

    pages = page_map.get("pages")
    if not isinstance(pages, list) or len(pages) != EXPECTED_PROVIDER_PAGE_COUNT:
        raise ValueError("Perelman DjVu page-map page count drift")
    expected_keys = {
        "page", "utf8_byte_count", "character_count", "sha256", "normalized_profile",
        "normalized_character_count", "normalized_sha256"
    }
    for expected_page, record in enumerate(pages, start=1):
        if not isinstance(record, Mapping) or set(record) != expected_keys:
            raise ValueError("Perelman DjVu page-map record shape drift")
        if record.get("page") != expected_page:
            raise ValueError("Perelman DjVu page-map page ordering drift")
        for key in ("utf8_byte_count", "character_count", "normalized_character_count"):
            value = record.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"Perelman DjVu page-map {key} is invalid")
        if record.get("normalized_profile") != NORMALIZATION_PROFILE:
            raise ValueError("Perelman DjVu page-map normalization profile drift")
        _validate_digest(record.get("sha256"), name="page SHA-256")
        _validate_digest(record.get("normalized_sha256"), name="normalized page SHA-256")

    page_records_sha256 = page_map.get("page_records_sha256")
    _validate_digest(page_records_sha256, name="page-records SHA-256")
    if page_records_sha256 != _digest_json(pages):
        raise ValueError("Perelman DjVu page-map records digest drift")

    false_gates = (
        "source_text_included",
        "page_images_committed",
        "binary_bytes_committed",
        "page_equivalence_to_pdf_verified",
        "literary_page_selection_frozen",
        "canonical_ocr_extraction_carrier_changed",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved_from_frozen_body",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    )
    if any(page_map.get(key) is not False for key in false_gates):
        raise ValueError("Perelman DjVu page-map advanced a forbidden corpus/parity gate")
    if page_map.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("Perelman DjVu page-map advanced FantLab source identity")


def probe_remote(*, package_version: str) -> dict[str, object]:
    with TemporaryDirectory(prefix="scriptorium-perelman-djvu-page-map-") as directory:
        path = Path(directory) / "carrier.djvu"
        _download_verified_djvu(path)
        page_outputs = [_run_djvutxt(path, page=page) for page in range(1, EXPECTED_PROVIDER_PAGE_COUNT + 1)]
        return build_page_map(page_outputs, package_version=package_version)


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_object(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    probe = subparsers.add_parser("probe")
    probe.add_argument("--package-version", required=True)
    probe.add_argument("--output", type=Path, required=True)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--package-version", required=True)
    verify.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)

    observed = probe_remote(package_version=args.package_version)
    if args.command == "probe":
        _write_object(args.output, observed)
        print(json.dumps({
            "page_map_version": PAGE_MAP_VERSION,
            "page_count": len(observed["pages"]),
            "page_records_sha256": observed["page_records_sha256"],
        }, sort_keys=True))
        return 0

    expected = _load_object(args.receipt)
    validate_page_map(expected)
    if observed != expected:
        raise ValueError("Perelman DjVu page map no longer matches frozen receipt")
    print(json.dumps({"verified": True, "page_records_sha256": observed["page_records_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
