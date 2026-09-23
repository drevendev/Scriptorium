from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest


ARTIFACT = Path(
    "corpus/candidates/source-edition-traces/"
    "perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-transition-tail.json"
)
EXPECTED_PHYSICAL_SHA256 = "d518b8f3a00511cf3b7c0199923705c0df9339004be0d759198a5f72cb5a79e5"
EXPECTED_CARRIER = {
    "kind": "pdf",
    "page_count": 223,
    "byte_count": 28_168_847,
    "sha1": "3c616f547ff283a2cafd1ac26b448a8e8013f648",
    "sha256": "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61",
}
EXPECTED_LABELS = {
    9: None,
    10: "1",
    11: "2",
    12: "3",
    13: "4",
    217: "208",
    218: "209",
    219: "210",
    220: "211",
    221: None,
    222: None,
    223: None,
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


class PerelmanPdfFacsimileTransitionTailTests(unittest.TestCase):
    def test_artifact_physical_digest_is_frozen(self) -> None:
        self.assertEqual(sha256(ARTIFACT.read_bytes()).hexdigest(), EXPECTED_PHYSICAL_SHA256)

    def test_artifact_is_bound_to_exact_frozen_pdf(self) -> None:
        payload = load_artifact()
        self.assertEqual(payload["candidate_id"], "perelman-entertaining-physics-book1-1913-ru")
        self.assertEqual(payload["carrier"], EXPECTED_CARRIER)
        self.assertEqual(
            payload["evidence_version"],
            "scriptorium-perelman-1913-pdf-facsimile-transition-tail-v1",
        )

    def test_only_bounded_direct_observations_are_retained(self) -> None:
        payload = load_artifact()
        pages = payload["observation"]["pages"]
        labels = {page["carrier_page"]: page["visible_printed_page_label"] for page in pages}
        self.assertEqual(labels, EXPECTED_LABELS)
        self.assertEqual(
            [page["carrier_page"] for page in pages],
            [9, 10, 11, 12, 13, 217, 218, 219, 220, 221, 222, 223],
        )
        for page in pages:
            self.assertEqual(len(page["rendered_image_sha256"]), 64)

    def test_direct_boundaries_advance_without_claiming_complete_mapping(self) -> None:
        payload = load_artifact()
        decision = payload["decision"]
        self.assertEqual(
            decision["status"],
            "numbered_body_transition_and_tail_anchors_observed_mapping_still_incomplete",
        )
        self.assertTrue(decision["body_start_carrier_page_proved"])
        self.assertEqual(decision["body_start_carrier_page"], 10)
        self.assertTrue(decision["numbered_body_end_carrier_page_proved"])
        self.assertEqual(decision["numbered_body_end_carrier_page"], 220)
        self.assertEqual(decision["last_directly_observed_printed_number"], 211)
        self.assertTrue(decision["tail_boundary_directly_observed"])
        self.assertFalse(decision["bibliographic_to_carrier_mapping_complete"])
        self.assertFalse(decision["complete_numbered_body_range_proved"])
        self.assertFalse(decision["literary_body_end_carrier_page_proved"])
        self.assertFalse(decision["mapping_may_be_extrapolated_between_observed_anchors"])

    def test_tail_surfaces_keep_literary_selection_fail_closed(self) -> None:
        payload = load_artifact()
        pages = {page["carrier_page"]: page for page in payload["observation"]["pages"]}
        self.assertEqual(
            pages[221]["surface_kind"],
            "unnumbered_concluding_body_text_with_end_ornament",
        )
        self.assertEqual(pages[222]["surface_kind"], "publisher_advertisement")
        self.assertEqual(pages[223]["surface_kind"], "publisher_advertisement")
        self.assertEqual(payload["fantlab_source_edition_match"], "unknown")
        for key in CLOSED_BOOLEAN_GATES:
            self.assertFalse(payload[key], key)

    def test_source_free_boundary_and_transient_artifact_are_explicit(self) -> None:
        payload = load_artifact()
        observation = payload["observation"]
        self.assertTrue(payload["source_free"])
        self.assertFalse(payload["binary_bytes_committed"])
        self.assertFalse(payload["page_images_committed"])
        self.assertFalse(payload["ocr_included"])
        self.assertFalse(payload["literary_source_text_included"])
        self.assertFalse(observation["rendered_page_bytes_committed"])
        self.assertTrue(observation["pdf_bytes_deleted_before_artifact_upload"])
        self.assertTrue(observation["transient_review_artifact_uploaded"])
        self.assertEqual(observation["artifact_retention_days"], 1)
        self.assertEqual(observation["authoring_workflow_run_id"], 35905965911)
        self.assertEqual(observation["authoring_artifact_id"], 10771380564)
        self.assertEqual(
            observation["authoring_artifact_digest"],
            "sha256:ae4ac27bca4d1e2ffc0d75df3b9dab155d7a946a86b70b9a84b60894b4767fed",
        )
        self.assertEqual(
            observation["render_manifest_sha256"],
            "dedd68c23385b457e9630404022757b1f5a6a4bc5cfb6e74c364e93c28470fec",
        )
        self.assertTrue(FORBIDDEN_PAYLOAD_KEYS.isdisjoint(walk_keys(payload)))


if __name__ == "__main__":
    unittest.main()
