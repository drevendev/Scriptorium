from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import unittest

from scriptorium.perelman_pagination_evidence import (
    DJVU_PAGE_COUNT,
    EVIDENCE_VERSION,
    PDF_PAGE_COUNT,
    build_pagination_evidence,
    canonical_json_bytes,
    validate_pagination_evidence,
)


ARTIFACT = Path(
    "corpus/candidates/source-edition-traces/"
    "perelman-entertaining-physics-book1-1913-ru.pagination-evidence.json"
)


class PerelmanPaginationEvidenceTests(unittest.TestCase):
    def test_frozen_artifact_matches_builder_byte_for_byte(self) -> None:
        evidence = build_pagination_evidence()
        validate_pagination_evidence(evidence)
        self.assertEqual(evidence["evidence_version"], EVIDENCE_VERSION)
        self.assertEqual(ARTIFACT.read_bytes(), canonical_json_bytes(evidence))

    def test_evidence_keeps_mapping_and_parity_gates_closed(self) -> None:
        evidence = build_pagination_evidence()
        self.assertEqual(evidence["carrier_context"]["pdf"]["page_count"], PDF_PAGE_COUNT)
        self.assertEqual(evidence["carrier_context"]["djvu"]["page_count"], DJVU_PAGE_COUNT)
        rsl, google = evidence["bibliographic_surfaces"]
        self.assertEqual(rsl["collation_display"], "VIII, 211, [1] с.")
        self.assertIsNone(rsl["normalized_single_page_count"])
        self.assertEqual(google["displayed_page_count"], 212)
        self.assertFalse(evidence["decision"]["page_count_arithmetic_may_select_literary_pages"])
        self.assertFalse(evidence["literary_page_selection_frozen"])
        self.assertFalse(evidence["minimum_300k_proved_from_frozen_body"])
        self.assertFalse(evidence["admitted_for_calibration"])
        self.assertEqual(evidence["fantlab_source_edition_match"], "unknown")
        self.assertFalse(evidence["m2_parity_admissible"])

    def test_validator_rejects_carrier_or_bibliographic_drift(self) -> None:
        evidence = build_pagination_evidence()
        drifted = deepcopy(evidence)
        drifted["carrier_context"]["djvu"]["page_count"] = 212
        with self.assertRaisesRegex(ValueError, "DjVu carrier identity drift"):
            validate_pagination_evidence(drifted)

        drifted = deepcopy(evidence)
        drifted["bibliographic_surfaces"][0]["collation_display"] = "212 с."
        with self.assertRaisesRegex(ValueError, "RSL pagination evidence drift"):
            validate_pagination_evidence(drifted)

    def test_validator_rejects_count_arithmetic_and_gate_promotion(self) -> None:
        evidence = build_pagination_evidence()
        advanced = deepcopy(evidence)
        advanced["decision"]["page_count_arithmetic_may_select_literary_pages"] = True
        with self.assertRaisesRegex(ValueError, "page-count arithmetic"):
            validate_pagination_evidence(advanced)

        advanced = deepcopy(evidence)
        advanced["literary_page_selection_frozen"] = True
        with self.assertRaisesRegex(ValueError, "forbidden corpus/parity gate"):
            validate_pagination_evidence(advanced)

        advanced = deepcopy(evidence)
        advanced["fantlab_source_edition_match"] = "exact"
        with self.assertRaisesRegex(ValueError, "FantLab source identity"):
            validate_pagination_evidence(advanced)

    def test_validator_rejects_source_payload_keys(self) -> None:
        evidence = build_pagination_evidence()
        leaked = deepcopy(evidence)
        leaked["source_text"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "forbidden source payload key"):
            validate_pagination_evidence(leaked)

    def test_committed_artifact_is_source_free_json(self) -> None:
        evidence = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        validate_pagination_evidence(evidence)
        self.assertTrue(evidence["source_free"])
        self.assertNotIn("source_text", evidence)
        self.assertNotIn("literary_text", evidence)


if __name__ == "__main__":
    unittest.main()
