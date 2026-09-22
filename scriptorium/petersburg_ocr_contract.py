from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CONTRACT_VERSION = "scriptorium-petersburg-1916-ocr-body-contract-v1"
CANDIDATE_ID = "bely-petersburg-1916-ru"
SCAN_IDENTITY = {
    "byte_count": 3_621_459,
    "sha1": "682476934dd6ed49c6bbcdb0720127c1812ff477",
    "sha256": "b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5",
}
SOURCE_PDF_PAGE_COUNT = 632
FORBIDDEN_SOURCE_KEYS = {
    "pdf_bytes", "page_image", "page_images", "ocr_text",
    "source_text", "literary_text", "literary_source_text",
}
EXPECTED_UNBOUND = {
    "page_selection": {
        "status": "unbound", "included_pdf_pages": [],
        "excluded_pdf_pages": [], "evidence": None,
    },
    "rasterization": {
        "status": "unbound", "engine": None, "version": None,
        "artifact_sha256": None, "settings": None,
    },
    "ocr": {
        "status": "unbound", "engine": None, "version": None,
        "engine_artifact_sha256": None, "language_data": [],
        "language_data_sha256": None, "settings": None,
    },
    "outputs": {
        "raw_character_count": None, "raw_sha256": None,
        "normalized_character_count": None, "normalized_sha256": None,
    },
}
EXPECTED_COMPOSITION = {
    "status": "defined",
    "page_order": "ascending_pdf_page_number",
    "per_page_trailing_newlines": "strip_all",
    "page_joiner": "\n\n",
    "raw_body_encoding": "utf-8",
    "normalized_profile": "scriptorium-text-v1",
}
EXPECTED_GATES = {
    "extraction_profile_frozen": False,
    "literary_body_frozen": False,
    "minimum_300k_proved_from_frozen_body": False,
    "admitted_for_calibration": False,
    "fantlab_source_edition_match": "unknown",
    "diagnostic_ready": False,
    "m2_parity_admissible": False,
}
EXPECTED_PUBLICATION = {
    "pdf_bytes_committed": False,
    "page_images_committed": False,
    "ocr_text_committed": False,
    "literary_source_text_committed": False,
}
EXPECTED_KEYS = {
    "contract_version", "candidate_id", "purpose", "scan_identity",
    "source_pdf_page_count", *EXPECTED_UNBOUND, "composition", "gates", "publication",
}


def _reject_source_payload(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_SOURCE_KEYS:
                raise ValueError(f"source payload key forbidden at {path}.{key}")
            _reject_source_payload(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_source_payload(child, f"{path}[{index}]")


def validate_contract(contract: dict[str, Any]) -> None:
    if not isinstance(contract, dict):
        raise TypeError("contract must be a JSON object")
    _reject_source_payload(contract)
    if set(contract) != EXPECTED_KEYS:
        raise ValueError("contract shape drift")
    if contract["contract_version"] != CONTRACT_VERSION:
        raise ValueError("contract version drift")
    if contract["candidate_id"] != CANDIDATE_ID:
        raise ValueError("candidate identity drift")
    if not isinstance(contract["purpose"], str) or not contract["purpose"].strip():
        raise ValueError("purpose must be non-empty")
    if contract["scan_identity"] != SCAN_IDENTITY:
        raise ValueError("frozen scan identity drift")
    if contract["source_pdf_page_count"] != SOURCE_PDF_PAGE_COUNT:
        raise ValueError("source PDF page-count drift")
    for key, expected in EXPECTED_UNBOUND.items():
        if contract[key] != expected:
            raise ValueError(f"v1 {key} must remain unbound/unverified")
    if contract["composition"] != EXPECTED_COMPOSITION:
        raise ValueError("composition policy drift")
    if contract["gates"] != EXPECTED_GATES:
        raise ValueError("premature gate promotion")
    if contract["publication"] != EXPECTED_PUBLICATION:
        raise ValueError("source-publication boundary drift")


def load_contract(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_contract(data)
    return data


def canonical_sha256(contract: dict[str, Any]) -> str:
    validate_contract(contract)
    payload = json.dumps(
        contract, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the source-free Petersburg 1916 OCR/body promotion contract."
    )
    parser.add_argument("path")
    args = parser.parse_args(argv)
    contract = load_contract(args.path)
    print(json.dumps({
        "candidate_id": CANDIDATE_ID,
        "contract_version": CONTRACT_VERSION,
        "contract_sha256": canonical_sha256(contract),
        "scan_sha256": SCAN_IDENTITY["sha256"],
        "page_selection_status": contract["page_selection"]["status"],
        "rasterization_status": contract["rasterization"]["status"],
        "ocr_status": contract["ocr"]["status"],
        "literary_body_frozen": contract["gates"]["literary_body_frozen"],
        "minimum_300k_proved_from_frozen_body":
            contract["gates"]["minimum_300k_proved_from_frozen_body"],
        "m2_parity_admissible": contract["gates"]["m2_parity_admissible"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
