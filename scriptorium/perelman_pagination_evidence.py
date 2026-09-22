from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any


EVIDENCE_VERSION = "scriptorium-perelman-1913-pagination-evidence-v1"
CANDIDATE_ID = "perelman-entertaining-physics-book1-1913-ru"
RESEARCH_DATE = "2026-09-22"
PDF_PAGE_COUNT = 223
PDF_SHA256 = "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61"
DJVU_PAGE_COUNT = 218
DJVU_SHA256 = "f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462"
RSL_URL = "https://search.rsl.ru/ru/record/01004016163"
GOOGLE_BOOKS_URL = "https://play.google.com/store/books/details?id=8hBN2yBtlkIC"

_CLOSED_BOOLEAN_GATES = (
    "page_equivalence_to_pdf_verified",
    "literary_page_selection_frozen",
    "canonical_ocr_extraction_carrier_changed",
    "literary_body_count_and_digests_frozen",
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
}


def build_pagination_evidence() -> dict[str, Any]:
    """Return the frozen source-free pagination evidence snapshot.

    This is intentionally a research snapshot, not a network scraper.  The URLs and
    observed values are reviewed evidence inputs; exact carrier identities are already
    frozen elsewhere and are repeated here only to prevent accidental cross-edition use.
    """

    evidence: dict[str, Any] = {
        "evidence_version": EVIDENCE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "research_date": RESEARCH_DATE,
        "source_free": True,
        "carrier_context": {
            "pdf": {
                "page_count": PDF_PAGE_COUNT,
                "sha256": PDF_SHA256,
                "current_file_revision_timestamp": "2021-09-03T09:12:00Z",
                "current_file_revision_note": "added pages 193-194 (without text layout)",
            },
            "djvu": {
                "page_count": DJVU_PAGE_COUNT,
                "sha256": DJVU_SHA256,
            },
        },
        "bibliographic_surfaces": [
            {
                "provider": "Russian State Library",
                "url": RSL_URL,
                "authority_class": "primary_library_catalogue",
                "observed_on": RESEARCH_DATE,
                "edition_identity": "Санкт-Петербург : П. П. Сойкин, 1913",
                "collation_display": "VIII, 211, [1] с.",
                "preliminary_roman_pages": 8,
                "numbered_pages": 211,
                "bracketed_unnumbered_pages": 1,
                "normalized_single_page_count": None,
                "carrier_page_mapping_disclosed": False,
            },
            {
                "provider": "Google Books / Google Play Books",
                "url": GOOGLE_BOOKS_URL,
                "authority_class": "independent_book_metadata_surface",
                "observed_on": RESEARCH_DATE,
                "edition_identity": "Сойкин, 1913",
                "displayed_page_count": 212,
                "collation_display": None,
                "carrier_page_mapping_disclosed": False,
            },
        ],
        "decision": {
            "status": "pagination_evidence_frozen_mapping_unresolved",
            "page_count_arithmetic_may_select_literary_pages": False,
            "rejected_inference": (
                "218 DjVu carrier pages - 212 displayed book pages = "
                "6 non-literary carrier pages"
            ),
            "reason": (
                "The RSL catalogue describes the same 1913 Book 1 as VIII preliminary "
                "pages, 211 numbered pages and 1 bracketed unnumbered page, while Google "
                "exposes a normalized 212-page display. These metadata surfaces use "
                "different pagination conventions and neither maps bibliographic pages "
                "to exact Commons carrier pages. Carrier-page selection therefore "
                "requires page-label/facsimile evidence rather than count subtraction."
            ),
            "next_evidence": (
                "Establish an exact page-level mapping on a deliberately chosen frozen "
                "carrier from facsimile/page-label evidence, then bind that mapping under "
                "a new contract version before freezing a literary body."
            ),
        },
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
    validate_pagination_evidence(evidence)
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


def validate_pagination_evidence(evidence: dict[str, Any]) -> None:
    if evidence.get("evidence_version") != EVIDENCE_VERSION:
        raise ValueError("pagination evidence version drift")
    if evidence.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("candidate identity drift")
    if evidence.get("research_date") != RESEARCH_DATE:
        raise ValueError("research date drift")
    if evidence.get("source_free") is not True:
        raise ValueError("source-free boundary drift")

    carrier_context = evidence.get("carrier_context")
    if not isinstance(carrier_context, dict):
        raise ValueError("carrier context missing")
    pdf = carrier_context.get("pdf")
    djvu = carrier_context.get("djvu")
    if not isinstance(pdf, dict) or not isinstance(djvu, dict):
        raise ValueError("carrier context shape drift")
    if pdf.get("page_count") != PDF_PAGE_COUNT or pdf.get("sha256") != PDF_SHA256:
        raise ValueError("PDF carrier identity drift")
    if djvu.get("page_count") != DJVU_PAGE_COUNT or djvu.get("sha256") != DJVU_SHA256:
        raise ValueError("DjVu carrier identity drift")

    surfaces = evidence.get("bibliographic_surfaces")
    if not isinstance(surfaces, list) or len(surfaces) != 2:
        raise ValueError("bibliographic surface shape drift")
    rsl, google = surfaces
    if not isinstance(rsl, dict) or not isinstance(google, dict):
        raise ValueError("bibliographic surface shape drift")
    if (
        rsl.get("provider") != "Russian State Library"
        or rsl.get("url") != RSL_URL
        or rsl.get("collation_display") != "VIII, 211, [1] с."
        or rsl.get("preliminary_roman_pages") != 8
        or rsl.get("numbered_pages") != 211
        or rsl.get("bracketed_unnumbered_pages") != 1
        or rsl.get("normalized_single_page_count") is not None
        or rsl.get("carrier_page_mapping_disclosed") is not False
    ):
        raise ValueError("RSL pagination evidence drift")
    if (
        google.get("provider") != "Google Books / Google Play Books"
        or google.get("url") != GOOGLE_BOOKS_URL
        or google.get("displayed_page_count") != 212
        or google.get("carrier_page_mapping_disclosed") is not False
    ):
        raise ValueError("Google pagination evidence drift")

    decision = evidence.get("decision")
    if not isinstance(decision, dict):
        raise ValueError("pagination decision missing")
    if decision.get("status") != "pagination_evidence_frozen_mapping_unresolved":
        raise ValueError("pagination decision status drift")
    if decision.get("page_count_arithmetic_may_select_literary_pages") is not False:
        raise ValueError("page-count arithmetic must not select literary pages")
    if decision.get("rejected_inference") != (
        "218 DjVu carrier pages - 212 displayed book pages = 6 non-literary carrier pages"
    ):
        raise ValueError("rejected pagination inference drift")

    for key in _CLOSED_BOOLEAN_GATES:
        if evidence.get(key) is not False:
            raise ValueError(f"forbidden corpus/parity gate promotion: {key}")
    if evidence.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source identity must remain unknown")

    _walk_forbidden_keys(evidence)


def canonical_json_bytes(evidence: dict[str, Any]) -> bytes:
    validate_pagination_evidence(evidence)
    return (json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_pagination_evidence(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(build_pagination_evidence()))
