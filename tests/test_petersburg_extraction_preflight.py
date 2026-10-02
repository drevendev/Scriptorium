from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "corpus/candidates/source-edition-traces/bely-petersburg-1916-ru.extraction-preflight.json"
CANDIDATE_PAGE = ROOT / "corpus/candidates/bely-petersburg-1916-ru.md"
EXPECTED_PHYSICAL_SHA256 = "093f251cb8d03846a5158a1ac29d4b66e1796a7cc2bc65a77ade3d9e3cebcff1"
EXPECTED_SCAN_SHA256 = "b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5"


class PetersburgExtractionPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = EVIDENCE.read_bytes()
        cls.data = json.loads(cls.raw)

    def test_source_free_artifact_is_frozen(self) -> None:
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), EXPECTED_PHYSICAL_SHA256)
        self.assertTrue(self.data["publication"]["source_free"])
        self.assertFalse(self.data["publication"]["pdf_bytes_committed"])
        self.assertFalse(self.data["publication"]["page_images_committed"])
        self.assertFalse(self.data["publication"]["extracted_text_committed"])
        self.assertFalse(self.data["publication"]["literary_source_text_committed"])

    def test_exact_carrier_identity_is_preserved(self) -> None:
        carrier = self.data["carrier"]
        self.assertEqual(carrier["page_count"], 632)
        self.assertEqual(carrier["byte_count"], 3621459)
        self.assertEqual(carrier["sha1"], "682476934dd6ed49c6bbcdb0720127c1812ff477")
        self.assertEqual(carrier["sha256"], EXPECTED_SCAN_SHA256)

    def test_preflight_does_not_guess_text_layer_or_ocr_strategy(self) -> None:
        decision = self.data["decision"]
        self.assertEqual(decision["embedded_text_layer_status"], "unverified")
        self.assertFalse(decision["provider_metadata_proves_embedded_text_layer"])
        self.assertFalse(decision["visual_facsimile_preview_proves_absence_of_text_layer"])
        self.assertFalse(decision["direct_pdf_text_extraction_admissible"])
        self.assertFalse(decision["raster_ocr_required"])
        self.assertIn("text-layer probe", decision["next_required_evidence"])

    def test_existing_promotion_contract_remains_unbound(self) -> None:
        contract = self.data["existing_promotion_contract"]
        self.assertEqual(
            contract["canonical_sha256"],
            "d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2",
        )
        self.assertFalse(contract["page_selection_bound"])
        self.assertFalse(contract["rasterization_toolchain_bound"])
        self.assertFalse(contract["ocr_toolchain_bound"])
        self.assertFalse(contract["body_outputs_frozen"])

    def test_downstream_gates_remain_closed(self) -> None:
        gates = self.data["gates"]
        self.assertFalse(gates["literary_page_selection_bound"])
        self.assertFalse(gates["extraction_profile_frozen"])
        self.assertFalse(gates["literary_body_frozen"])
        self.assertFalse(gates["minimum_300k_proved_from_frozen_body"])
        self.assertEqual(gates["fantlab_source_edition_match"], "unknown")
        self.assertFalse(gates["diagnostic_ready"])
        self.assertFalse(gates["m2_parity_admissible"])
        self.assertFalse(gates["admitted_for_calibration"])

    def test_public_candidate_exposes_preflight_without_promotion(self) -> None:
        page = CANDIDATE_PAGE.read_text(encoding="utf-8")
        self.assertIn("Extraction-strategy preflight", page)
        self.assertIn(EXPECTED_PHYSICAL_SHA256, page)
        self.assertIn("embedded text layer remains **unverified**", page)
        self.assertIn("does not prove that the PDF lacks a hidden text layer", page)


if __name__ == "__main__":
    unittest.main()
