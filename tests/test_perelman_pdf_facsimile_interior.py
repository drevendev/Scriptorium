import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "corpus" / "candidates" / "source-edition-traces" / "perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-interior.json"
EXPECTED_PHYSICAL_SHA256 = "b19be5e8b3fe83546dd65a73770b91f71124b13c709de8142ead29cb78fbc319"


class PerelmanPdfFacsimileInteriorEvidenceTest(unittest.TestCase):
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

    def test_direct_interior_anchors_are_exact(self):
        observed = {
            row["carrier_page"]: row["visible_printed_page_label"]
            for row in self.data["observation"]["pages"]
        }
        self.assertEqual(
            observed,
            {199: "190", 200: "191", 201: "192", 202: "193", 203: "194", 204: "195", 205: "196", 206: "197"},
        )
        self.assertEqual(
            {row["carrier_page"]: row["rendered_image_sha256"] for row in self.data["observation"]["pages"]},
            {
                199: "23e55ac4525eae5512099465eaad02685c4d1295cbaa67b1c4a973b760c522d9",
                200: "7d8f87dc9c3c4351bbe1a2d915ac801872319a2bda5902396f6cd05b7c64b4d4",
                201: "653f85f61b2579532720231620b5ca1d498e8a800126ebc8eed343121e5da9db",
                202: "79390f88ec549eaf55870c882440018d18a04ff3869ff7a7fcf13607d4aa8085",
                203: "b0ceb61bf6272c7eaa54d073bd3e85133dc4130fc43705dfa7f4f7c589c786bc",
                204: "19e5cc06b4cafc6aa3fb0cb81cd42dc74826c699f1a3e1e24c4e8f8ed9395fb4",
                205: "eb6f73b22d5ec476d19e75fea4a8eac20109d7a16300fff62957569b6d263d4e",
                206: "fd914d50e51983beea35b6c7b78abf5b61a6f8604f9f418c41fb6c1f931a75f9",
            },
        )

    def test_restored_pages_are_locally_bound_without_global_offset_claim(self):
        decision = self.data["decision"]
        self.assertTrue(decision["restored_printed_pages_directly_observed"])
        self.assertEqual(decision["restored_printed_pages_carrier_pages"], {"193": 202, "194": 203})
        self.assertTrue(decision["local_window_continuity_directly_observed"])
        self.assertEqual(decision["local_carrier_minus_printed_offset_observed"], 9)
        self.assertEqual(decision["local_offset_scope_carrier_pages"], [199, 206])
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
