from __future__ import annotations

import json
from pathlib import Path
import unittest

from scriptorium.petersburg_ocr_contract import (
    CANDIDATE_ID,
    CONTRACT_VERSION,
    SCAN_IDENTITY,
    canonical_sha256,
    load_contract,
    validate_contract,
)

CONTRACT_PATH = Path(
    "corpus/candidates/source-edition-traces/"
    "bely-petersburg-1916-ru.ocr-contract.json"
)
EXPECTED_CONTRACT_SHA256 = "d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2"


def production_contract() -> dict[str, object]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


class PetersburgOcrContractTests(unittest.TestCase):
    def test_committed_contract_validates_and_has_stable_digest(self) -> None:
        contract = load_contract(CONTRACT_PATH)
        self.assertEqual(contract["candidate_id"], CANDIDATE_ID)
        self.assertEqual(contract["contract_version"], CONTRACT_VERSION)
        self.assertEqual(contract["scan_identity"], SCAN_IDENTITY)
        self.assertEqual(canonical_sha256(contract), EXPECTED_CONTRACT_SHA256)

    def test_scan_identity_drift_fails_closed(self) -> None:
        contract = production_contract()
        contract["scan_identity"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "scan identity drift"):
            validate_contract(contract)

    def test_page_selection_cannot_be_silently_bound_in_v1(self) -> None:
        contract = production_contract()
        contract["page_selection"]["status"] = "bound"
        contract["page_selection"]["included_pdf_pages"] = [5, 6]
        with self.assertRaisesRegex(ValueError, "page_selection"):
            validate_contract(contract)

    def test_ocr_or_rasterizer_identity_cannot_be_invented_in_v1(self) -> None:
        contract = production_contract()
        contract["rasterization"]["engine"] = "pdftoppm"
        with self.assertRaisesRegex(ValueError, "rasterization"):
            validate_contract(contract)

        contract = production_contract()
        contract["ocr"]["engine"] = "tesseract"
        with self.assertRaisesRegex(ValueError, "ocr"):
            validate_contract(contract)

    def test_body_outputs_and_gates_cannot_advance_without_new_evidence_version(self) -> None:
        contract = production_contract()
        contract["outputs"]["normalized_character_count"] = 300001
        with self.assertRaisesRegex(ValueError, "outputs"):
            validate_contract(contract)

        contract = production_contract()
        contract["gates"]["minimum_300k_proved_from_frozen_body"] = True
        with self.assertRaisesRegex(ValueError, "premature gate"):
            validate_contract(contract)

    def test_source_payload_keys_are_rejected_recursively(self) -> None:
        contract = production_contract()
        contract["page_selection"]["evidence"] = {"ocr_text": "forbidden"}
        with self.assertRaisesRegex(ValueError, "source payload key forbidden"):
            validate_contract(contract)

    def test_composition_policy_is_versioned_and_fail_closed(self) -> None:
        contract = production_contract()
        contract["composition"]["page_joiner"] = "\n"
        with self.assertRaisesRegex(ValueError, "composition policy drift"):
            validate_contract(contract)


if __name__ == "__main__":
    unittest.main()
