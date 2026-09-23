from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest


ARTIFACT = Path(
    "corpus/candidates/source-edition-traces/"
    "perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-frontmatter.json"
)
EXPECTED_PHYSICAL_SHA256 = "12bf560c02b66275a30331cf0274a410041ac916ef21c4ff840d0e55524b7ff8"
EXPECTED_CARRIER = {
    "kind": "pdf",
    "page_count": 223,
    "byte_count": 28_168_847,
    "sha1": "3c616f547ff283a2cafd1ac26b448a8e8013f648",
    "sha256": "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61",
}
CLOSED_BOOLEAN_GATES = (
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
FORBIDDEN_PAYLOAD_KEYS = {
    "source_text",
    "literary_text",
    "ocr_text",
    "hidden_text",
    "text_content",
    "page_image",
    "page_image_bytes",
    "pdf_bytes",
}


def load_artifact() -> dict[str, object]:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(walk_keys(child))
    return keys


class PerelmanPdfFacsimileFrontmatterTests(unittest.TestCase):
    def test_artifact_physical_digest_is_frozen(self) -> None:
        self.assertEqual(sha256(ARTIFACT.read_bytes()).hexdigest(), EXPECTED_PHYSICAL_SHA256)

    def test_artifact_is_bound_to_exact_frozen_pdf(self) -> None:
        payload = load_artifact()
        self.assertEqual(payload["candidate_id"], "perelman-entertaining-physics-book1-1913-ru")
        self.assertEqual(payload["carrier"], EXPECTED_CARRIER)
        self.assertEqual(
            payload["evidence_version"],
            "scriptorium-perelman-1913-pdf-facsimile-frontmatter-v1",
        )

    def test_only_directly_observed_anchor_pages_are_retained(self) -> None:
        payload = load_artifact()
        pages = payload["observation"]["pages"]
        self.assertEqual([page["carrier_page"] for page in pages], [4, 5, 6, 8, 9])
        labels = {page["carrier_page"]: page["visible_printed_page_label"] for page in pages}
        self.assertEqual(labels, {4: None, 5: None, 6: "V", 8: "VII", 9: None})
        self.assertNotIn(7, labels)
        self.assertNotIn(10, labels)

    def test_partial_mapping_remains_fail_closed(self) -> None:
        payload = load_artifact()
        decision = payload["decision"]
        self.assertEqual(decision["status"], "partial_front_matter_facsimile_anchors_only")
        self.assertFalse(decision["bibliographic_to_carrier_mapping_complete"])
        self.assertFalse(decision["body_start_carrier_page_proved"])
        self.assertFalse(decision["mapping_may_be_extrapolated_between_observed_anchors"])
        self.assertEqual(payload["fantlab_source_edition_match"], "unknown")
        for key in CLOSED_BOOLEAN_GATES:
            self.assertFalse(payload[key], key)

    def test_source_free_boundary_is_explicit(self) -> None:
        payload = load_artifact()
        self.assertTrue(payload["source_free"])
        self.assertFalse(payload["binary_bytes_committed"])
        self.assertFalse(payload["page_images_committed"])
        self.assertFalse(payload["ocr_included"])
        self.assertFalse(payload["literary_source_text_included"])
        self.assertFalse(payload["observation"]["preview_bytes_frozen"])
        self.assertTrue(FORBIDDEN_PAYLOAD_KEYS.isdisjoint(walk_keys(payload)))


if __name__ == "__main__":
    unittest.main()
