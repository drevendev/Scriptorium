from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CONTRACT_VERSION = "scriptorium-perelman-1913-ocr-body-contract-v1"
CANDIDATE_ID = "perelman-entertaining-physics-book1-1913-ru"
SOURCE_PDF_PAGE_COUNT = 223
SCAN_IDENTITY = {
    "byte_count": 28_168_847,
    "sha1": "3c616f547ff283a2cafd1ac26b448a8e8013f648",
    "sha256": "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61",
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

FORBIDDEN_SOURCE_KEYS = {
    "pdf_bytes",
    "page_image",
    "page_images",
    "ocr_text",
    "source_text",
    "literary_text",
    "literary_source_text",
}

_TOP_LEVEL_KEYS = {
    "contract_version",
    "candidate_id",
    "purpose",
    "scan_identity",
    "source_pdf_page_count",
    "page_selection",
    "rasterization",
    "ocr",
    "composition",
    "outputs",
    "gates",
    "publication",
}


def _require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"{label} shape drift: missing={missing}, extra={extra}")


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
    """Validate the source-free v1 promotion boundary.

    Version 1 intentionally represents the state before page selection and OCR
    toolchain binding. A future bound extraction profile must use a new contract
    version and independent evidence instead of mutating this record in place.
    """

    if not isinstance(contract, dict):
        raise TypeError("contract must be a JSON object")
    _reject_source_payload(contract)
    _require_exact_keys(contract, _TOP_LEVEL_KEYS, "contract")

    if contract["contract_version"] != CONTRACT_VERSION:
        raise ValueError("contract version drift")
    if contract["candidate_id"] != CANDIDATE_ID:
        raise ValueError("candidate identity drift")
    if not isinstance(contract["purpose"], str) or not contract["purpose"].strip():
        raise ValueError("purpose must be non-empty")

    scan_identity = contract["scan_identity"]
    if not isinstance(scan_identity, dict):
        raise TypeError("scan_identity must be an object")
    _require_exact_keys(scan_identity, set(SCAN_IDENTITY), "scan_identity")
    if scan_identity != SCAN_IDENTITY:
        raise ValueError("frozen scan identity drift")

    if contract["source_pdf_page_count"] != SOURCE_PDF_PAGE_COUNT:
        raise ValueError("source PDF page-count drift")

    page_selection = contract["page_selection"]
    if not isinstance(page_selection, dict):
        raise TypeError("page_selection must be an object")
    _require_exact_keys(
        page_selection,
        {"status", "included_pdf_pages", "excluded_pdf_pages", "evidence"},
        "page_selection",
    )
    if page_selection != {
        "status": "unbound",
        "included_pdf_pages": [],
        "excluded_pdf_pages": [],
        "evidence": None,
    }:
        raise ValueError("v1 page selection must remain unbound")

    rasterization = contract["rasterization"]
    if not isinstance(rasterization, dict):
        raise TypeError("rasterization must be an object")
    _require_exact_keys(
        rasterization,
        {"status", "engine", "version", "artifact_sha256", "settings"},
        "rasterization",
    )
    if rasterization != {
        "status": "unbound",
        "engine": None,
        "version": None,
        "artifact_sha256": None,
        "settings": None,
    }:
        raise ValueError("v1 rasterization toolchain must remain unbound")

    ocr = contract["ocr"]
    if not isinstance(ocr, dict):
        raise TypeError("ocr must be an object")
    _require_exact_keys(
        ocr,
        {
            "status",
            "engine",
            "version",
            "engine_artifact_sha256",
            "language_data",
            "language_data_sha256",
            "settings",
        },
        "ocr",
    )
    if ocr != {
        "status": "unbound",
        "engine": None,
        "version": None,
        "engine_artifact_sha256": None,
        "language_data": [],
        "language_data_sha256": None,
        "settings": None,
    }:
        raise ValueError("v1 OCR toolchain must remain unbound")

    composition = contract["composition"]
    if not isinstance(composition, dict):
        raise TypeError("composition must be an object")
    _require_exact_keys(composition, set(EXPECTED_COMPOSITION), "composition")
    if composition != EXPECTED_COMPOSITION:
        raise ValueError("composition policy drift")

    outputs = contract["outputs"]
    if not isinstance(outputs, dict):
        raise TypeError("outputs must be an object")
    _require_exact_keys(
        outputs,
        {
            "raw_character_count",
            "raw_sha256",
            "normalized_character_count",
            "normalized_sha256",
        },
        "outputs",
    )
    if any(value is not None for value in outputs.values()):
        raise ValueError("v1 body outputs must remain unverified/null")

    gates = contract["gates"]
    if not isinstance(gates, dict):
        raise TypeError("gates must be an object")
    _require_exact_keys(gates, set(EXPECTED_GATES), "gates")
    if gates != EXPECTED_GATES:
        raise ValueError("premature gate promotion")

    publication = contract["publication"]
    if not isinstance(publication, dict):
        raise TypeError("publication must be an object")
    _require_exact_keys(publication, set(EXPECTED_PUBLICATION), "publication")
    if publication != EXPECTED_PUBLICATION:
        raise ValueError("source-publication boundary drift")


def canonical_sha256(contract: dict[str, Any]) -> str:
    validate_contract(contract)
    payload = json.dumps(
        contract,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_contract(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("contract file must contain a JSON object")
    validate_contract(data)
    return data


def _command_validate(path: str) -> int:
    contract = load_contract(path)
    result = {
        "candidate_id": CANDIDATE_ID,
        "contract_version": CONTRACT_VERSION,
        "contract_sha256": canonical_sha256(contract),
        "scan_sha256": SCAN_IDENTITY["sha256"],
        "page_selection_status": contract["page_selection"]["status"],
        "rasterization_status": contract["rasterization"]["status"],
        "ocr_status": contract["ocr"]["status"],
        "literary_body_frozen": contract["gates"]["literary_body_frozen"],
        "minimum_300k_proved_from_frozen_body": contract["gates"][
            "minimum_300k_proved_from_frozen_body"
        ],
        "m2_parity_admissible": contract["gates"]["m2_parity_admissible"],
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the source-free Perelman 1913 OCR/body promotion contract."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("path")
    args = parser.parse_args(argv)

    if args.command == "validate":
        return _command_validate(args.path)
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
