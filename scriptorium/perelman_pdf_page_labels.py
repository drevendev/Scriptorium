"""Inspect the exact Perelman 1913 PDF for internal PDF page labels.

The carrier is downloaded and inspected only in a transient workspace. Durable output
contains the frozen carrier identity, qpdf package identity, and qpdf's source-free
page-label summary. It never contains PDF bytes, page images, OCR, or literary text.
"""

from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path
import subprocess
from typing import Any, Mapping, Sequence

from scriptorium.perelman_scan_identity import (
    CANDIDATE_ID,
    EXPECTED_PROVIDER_BYTE_COUNT,
    EXPECTED_PROVIDER_SHA1,
)

EVIDENCE_VERSION = "scriptorium-perelman-1913-pdf-page-labels-v1"
EXPECTED_PDF_SHA256 = "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61"
EXPECTED_PDF_PAGE_COUNT = 223
QPDF_PACKAGE = "qpdf=11.9.0-1.1ubuntu0.1"

_CLOSED_BOOLEAN_GATES = (
    "pdf_djvu_page_equivalence_verified",
    "literary_page_selection_bound",
    "canonical_extraction_carrier_selected",
    "ocr_correctness_verified",
    "literary_body_frozen",
    "minimum_300k_proved_from_frozen_body",
    "admitted_for_calibration",
    "diagnostic_ready",
    "m2_parity_admissible",
)
_FORBIDDEN_PAYLOAD_KEYS = {
    "source_text",
    "literary_text",
    "ocr_text",
    "text_content",
    "page_image",
    "page_image_bytes",
    "pdf_bytes",
}


def compute_file_identity(path: Path) -> dict[str, object]:
    sha1_hash = sha1()
    sha256_hash = sha256()
    byte_count = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            byte_count += len(chunk)
            sha1_hash.update(chunk)
            sha256_hash.update(chunk)
    return {
        "byte_count": byte_count,
        "sha1": sha1_hash.hexdigest(),
        "sha256": sha256_hash.hexdigest(),
    }


def validate_exact_carrier(identity: Mapping[str, object]) -> None:
    expected = {
        "byte_count": EXPECTED_PROVIDER_BYTE_COUNT,
        "sha1": EXPECTED_PROVIDER_SHA1,
        "sha256": EXPECTED_PDF_SHA256,
    }
    if dict(identity) != expected:
        raise ValueError("Perelman PDF does not match the frozen exact carrier identity")


def parse_qpdf_pagelabels(payload: Mapping[str, object]) -> list[dict[str, object]]:
    raw = payload.get("pagelabels")
    if not isinstance(raw, list):
        raise ValueError("qpdf JSON is missing pagelabels array")
    labels: list[dict[str, object]] = []
    previous_index = -1
    for item in raw:
        if not isinstance(item, Mapping) or set(item) != {"index", "label"}:
            raise ValueError("qpdf pagelabel entry shape drift")
        index = item.get("index")
        label = item.get("label")
        if not isinstance(index, int) or isinstance(index, bool) or index < 0:
            raise ValueError("qpdf page-label index is invalid")
        if index <= previous_index:
            raise ValueError("qpdf page-label indexes must be strictly increasing")
        if index >= EXPECTED_PDF_PAGE_COUNT:
            raise ValueError("qpdf page-label index exceeds frozen PDF page count")
        if not isinstance(label, str):
            raise ValueError("qpdf page-label value is invalid")
        labels.append({"index": index, "label": label})
        previous_index = index
    return labels


def run_qpdf_pagelabels(pdf_path: Path, qpdf: str = "qpdf") -> list[dict[str, object]]:
    completed = subprocess.run(
        [qpdf, "--json", "--json-key=pagelabels", str(pdf_path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    payload = json.loads(completed.stdout)
    if not isinstance(payload, dict):
        raise ValueError("qpdf JSON root must be an object")
    return parse_qpdf_pagelabels(payload)


def build_evidence(
    identity: Mapping[str, object],
    pagelabels: list[dict[str, object]],
    *,
    qpdf_package: str = QPDF_PACKAGE,
) -> dict[str, Any]:
    validate_exact_carrier(identity)
    normalized_labels = parse_qpdf_pagelabels({"pagelabels": pagelabels})
    has_explicit_labels = bool(normalized_labels)
    status = (
        "internal_page_labels_observed_mapping_unresolved"
        if has_explicit_labels
        else "no_internal_page_labels_observed_mapping_unresolved"
    )
    evidence: dict[str, Any] = {
        "evidence_version": EVIDENCE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_free": True,
        "carrier": {
            "kind": "pdf",
            "page_count": EXPECTED_PDF_PAGE_COUNT,
            "byte_count": identity["byte_count"],
            "sha1": identity["sha1"],
            "sha256": identity["sha256"],
        },
        "probe": {
            "tool": "qpdf",
            "tool_package": qpdf_package,
            "json_surface": "pagelabels",
            "page_labels": normalized_labels,
            "page_label_entry_count": len(normalized_labels),
            "has_explicit_internal_page_labels": has_explicit_labels,
        },
        "decision": {
            "status": status,
            "internal_page_labels_establish_bibliographic_mapping": False,
            "internal_page_labels_may_select_literary_pages": False,
            "reason": (
                "PDF page-label metadata is an internal carrier surface only. "
                "Absent labels cannot map bibliographic pages, while present labels "
                "still require independent facsimile/bibliographic validation before "
                "they may select literary carrier pages."
            ),
            "next_evidence": (
                "Use exact-carrier facsimile evidence to establish bibliographic-to-carrier "
                "page mapping; treat internal page labels only as corroborating evidence."
            ),
        },
        "binary_bytes_committed": False,
        "page_images_committed": False,
        "ocr_included": False,
        "literary_source_text_included": False,
        "pdf_djvu_page_equivalence_verified": False,
        "literary_page_selection_bound": False,
        "canonical_extraction_carrier_selected": False,
        "ocr_correctness_verified": False,
        "literary_body_frozen": False,
        "minimum_300k_proved_from_frozen_body": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    validate_evidence(evidence)
    return evidence


def _walk_forbidden_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in _FORBIDDEN_PAYLOAD_KEYS:
                raise ValueError(f"forbidden source payload key: {key}")
            _walk_forbidden_keys(child)
    elif isinstance(value, list):
        for child in value:
            _walk_forbidden_keys(child)


def validate_evidence(evidence: Mapping[str, object]) -> None:
    if evidence.get("evidence_version") != EVIDENCE_VERSION:
        raise ValueError("page-label evidence version drift")
    if evidence.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("candidate identity drift")
    if evidence.get("source_free") is not True:
        raise ValueError("source-free boundary drift")

    carrier = evidence.get("carrier")
    if not isinstance(carrier, Mapping):
        raise ValueError("carrier evidence missing")
    validate_exact_carrier(
        {
            "byte_count": carrier.get("byte_count"),
            "sha1": carrier.get("sha1"),
            "sha256": carrier.get("sha256"),
        }
    )
    if carrier.get("kind") != "pdf" or carrier.get("page_count") != EXPECTED_PDF_PAGE_COUNT:
        raise ValueError("PDF carrier context drift")

    probe = evidence.get("probe")
    if not isinstance(probe, Mapping):
        raise ValueError("page-label probe missing")
    if probe.get("tool") != "qpdf" or probe.get("tool_package") != QPDF_PACKAGE:
        raise ValueError("qpdf tool identity drift")
    if probe.get("json_surface") != "pagelabels":
        raise ValueError("qpdf JSON surface drift")
    labels = probe.get("page_labels")
    if not isinstance(labels, list):
        raise ValueError("page-label array missing")
    normalized_labels = parse_qpdf_pagelabels({"pagelabels": labels})
    if probe.get("page_label_entry_count") != len(normalized_labels):
        raise ValueError("page-label count drift")
    if probe.get("has_explicit_internal_page_labels") is not bool(normalized_labels):
        raise ValueError("page-label presence flag drift")

    decision = evidence.get("decision")
    if not isinstance(decision, Mapping):
        raise ValueError("page-label decision missing")
    expected_status = (
        "internal_page_labels_observed_mapping_unresolved"
        if normalized_labels
        else "no_internal_page_labels_observed_mapping_unresolved"
    )
    if decision.get("status") != expected_status:
        raise ValueError("page-label decision status drift")
    if decision.get("internal_page_labels_establish_bibliographic_mapping") is not False:
        raise ValueError("internal page labels cannot establish mapping in this unit")
    if decision.get("internal_page_labels_may_select_literary_pages") is not False:
        raise ValueError("internal page labels cannot select literary pages in this unit")

    for key in (
        "binary_bytes_committed",
        "page_images_committed",
        "ocr_included",
        "literary_source_text_included",
        *_CLOSED_BOOLEAN_GATES,
    ):
        if evidence.get(key) is not False:
            raise ValueError(f"forbidden page-label/corpus gate promotion: {key}")
    if evidence.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source identity must remain unknown")
    _walk_forbidden_keys(evidence)


def canonical_json_bytes(evidence: Mapping[str, object]) -> bytes:
    validate_evidence(evidence)
    return (
        json.dumps(dict(evidence), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def capture(pdf_path: Path, output: Path, *, qpdf_package: str = QPDF_PACKAGE) -> dict[str, Any]:
    identity = compute_file_identity(pdf_path)
    validate_exact_carrier(identity)
    labels = run_qpdf_pagelabels(pdf_path)
    evidence = build_evidence(identity, labels, qpdf_package=qpdf_package)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_json_bytes(evidence))
    return evidence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--qpdf-package", default=QPDF_PACKAGE)
    args = parser.parse_args(argv)
    evidence = capture(args.pdf, args.output, qpdf_package=args.qpdf_package)
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
