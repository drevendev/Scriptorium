import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "corpus" / "candidates" / "source-edition-traces" / "perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-midbody.json"
EXPECTED_PHYSICAL_SHA256 = "26291c4add9272fa2572425597deb99ec8b431cffb374119c134867aca9e02ea"


class PerelmanPdfFacsimileMidbodyEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = EVIDENCE.read_bytes()
        cls.data = json.loads(cls.raw)

    def test_physical_digest_is_frozen(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), EXPECTED_PHYSICAL_SHA256)

    def test_exact_carrier_and_source_free_boundary(self):
        carrier = self.data["carrier"]
        self.assertEqual(carrier["page_count"], 223)
        self.assertEqual(carrier["byte_count"], 28168847)
        self.assertEqual(carrier["sha1"], "3c616f547ff283a2cafd1ac26b448a8e8013f648")
        self.assertEqual(carrier["sha256"], "3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61")
        self.assertTrue(self.data["source_free"])
        self.assertFalse(self.data["binary_bytes_committed"])
        self.assertFalse(self.data["page_images_committed"])
        self.assertFalse(self.data["ocr_included"])
        self.assertFalse(self.data["literary_source_text_included"])

    def test_direct_midbody_observations_are_frozen(self):
        rows = {row["carrier_page"]: row for row in self.data["observation"]["pages"]}
        self.assertEqual(
            {page: row["visible_printed_page_label"] for page, row in rows.items()},
            {59: "50", 60: None, 61: "52", 109: "100", 110: "101", 111: "102", 159: "150", 160: "151", 161: "152"},
        )
        self.assertEqual(rows[60]["label_observation"], "not_visible")
        self.assertEqual(
            {page: row["rendered_image_sha256"] for page, row in rows.items()},
            {
                59: "f707d612d9b9dc864d4436ee4d48e09d9c15f0c9d2588e8af36f835501f1af86",
                60: "cbbb8fdd29d66db5338fc0ce704114f05d52d52ef844450718a65f80f1b9610b",
                61: "ca527025615d4c1549112fbb9fbab4603c5589f3385c6d439befa19717cdc599",
                109: "a9a5334648e69304fa522bfc88345a979b7566b52c9be4f9c8e318e0b65dbb55",
                110: "5928c72fd85f1c5ac2c00949c54d9096b103dc164bc0f7f802054761f36c0891",
                111: "8cd80aad72d1739193563d3c5fa8d1dc5af1219b26e8b1dc461a18e51d633c0e",
                159: "b970d5e0aa4fcbc2b99f8176485f9a320d3bcfc4e4cb53d5831d1b1562143d8a",
                160: "aa609387b556626706c33187e24025040deba5c49e512c1a5fee39c6ebded4e2",
                161: "0c26242896309e5d0e9a476570014e251ed40223f3289cdcd2a8fe31f43daf61",
            },
        )

    def test_visible_labels_support_only_scoped_plus_nine_hypothesis(self):
        visible = [
            row for row in self.data["observation"]["pages"]
            if row["visible_printed_page_label"] is not None
        ]
        self.assertTrue(visible)
        self.assertTrue(all(row["carrier_page"] - int(row["visible_printed_page_label"]) == 9 for row in visible))
        decision = self.data["decision"]
        self.assertEqual(decision["all_directly_visible_labels_match_carrier_minus_printed_offset"], 9)
        self.assertTrue(decision["page_without_visible_folio_directly_observed"])
        self.assertEqual(decision["page_without_visible_folio_carrier_page"], 60)
        self.assertFalse(decision["printed_label_for_unlabelled_page_inferred"])
        self.assertFalse(decision["global_carrier_minus_printed_offset_asserted"])
        self.assertFalse(decision["mapping_may_be_extrapolated_between_observed_anchors"])

    def test_downstream_gates_remain_closed(self):
        decision = self.data["decision"]
        self.assertFalse(decision["bibliographic_to_carrier_mapping_complete"])
        self.assertFalse(decision["complete_numbered_body_range_proved"])
        self.assertFalse(self.data["pdf_djvu_page_equivalence_verified"])
        self.assertFalse(self.data["canonical_extraction_carrier_selected"])
        self.assertFalse(self.data["ocr_correctness_verified"])
        self.assertFalse(self.data["literary_page_selection_bound"])
        self.assertFalse(self.data["literary_body_frozen"])
        self.assertFalse(self.data["minimum_300k_proved_from_frozen_body"])
        self.assertEqual(self.data["fantlab_source_edition_match"], "unknown")
        self.assertFalse(self.data["diagnostic_ready"])
        self.assertFalse(self.data["m2_parity_admissible"])
        self.assertFalse(self.data["admitted_for_calibration"])


if __name__ == "__main__":
    unittest.main()
