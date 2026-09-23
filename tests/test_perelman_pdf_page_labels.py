from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from scriptorium.perelman_pdf_page_labels import (
    EXPECTED_PDF_PAGE_COUNT,
    EXPECTED_PDF_SHA256,
    QPDF_PACKAGE,
    build_evidence,
    canonical_json_bytes,
    compute_file_identity,
    parse_qpdf_pagelabels,
    validate_evidence,
)


ARTIFACT = Path(
    "corpus/candidates/source-edition-traces/"
    "perelman-entertaining-physics-book1-1913-ru.pdf-page-labels.json"
)

EXACT_IDENTITY = {
    "byte_count": 28_168_847,
    "sha1": "3c616f547ff283a2cafd1ac26b448a8e8013f648",
    "sha256": EXPECTED_PDF_SHA256,
}


class PerelmanPdfPageLabelTests(unittest.TestCase):
    def test_parse_accepts_qpdf_pagelabel_shape(self) -> None:
        labels = parse_qpdf_pagelabels(
            {"pagelabels": [{"index": 0, "label": "i"}, {"index": 8, "label": "1"}]}
        )
        self.assertEqual(labels, [{"index": 0, "label": "i"}, {"index": 8, "label": "1"}])

    def test_parse_rejects_shape_or_index_drift(self) -> None:
        with self.assertRaisesRegex(ValueError, "shape drift"):
            parse_qpdf_pagelabels({"pagelabels": [{"index": 0, "label": "i", "style": "r"}]})
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            parse_qpdf_pagelabels(
                {"pagelabels": [{"index": 8, "label": "1"}, {"index": 8, "label": "2"}]}
            )
        with self.assertRaisesRegex(ValueError, "exceeds frozen PDF"):
            parse_qpdf_pagelabels(
                {"pagelabels": [{"index": EXPECTED_PDF_PAGE_COUNT, "label": "224"}]}
            )

    def test_empty_labels_remain_fail_closed(self) -> None:
        evidence = build_evidence(EXACT_IDENTITY, [])
        validate_evidence(evidence)
        self.assertFalse(evidence["probe"]["has_explicit_internal_page_labels"])
        self.assertEqual(
            evidence["decision"]["status"],
            "no_internal_page_labels_observed_mapping_unresolved",
        )
        self.assertFalse(evidence["decision"]["internal_page_labels_establish_bibliographic_mapping"])
        self.assertFalse(evidence["literary_page_selection_bound"])
        self.assertFalse(evidence["minimum_300k_proved_from_frozen_body"])
        self.assertEqual(evidence["fantlab_source_edition_match"], "unknown")
        self.assertFalse(evidence["m2_parity_admissible"])

    def test_present_labels_still_remain_fail_closed(self) -> None:
        evidence = build_evidence(
            EXACT_IDENTITY,
            [{"index": 0, "label": "i"}, {"index": 8, "label": "1"}],
        )
        validate_evidence(evidence)
        self.assertTrue(evidence["probe"]["has_explicit_internal_page_labels"])
        self.assertEqual(evidence["probe"]["tool_package"], QPDF_PACKAGE)
        self.assertEqual(
            evidence["decision"]["status"],
            "internal_page_labels_observed_mapping_unresolved",
        )
        self.assertFalse(evidence["decision"]["internal_page_labels_may_select_literary_pages"])
        self.assertFalse(evidence["canonical_extraction_carrier_selected"])

    def test_committed_zero_label_artifact_matches_builder_byte_for_byte(self) -> None:
        expected = build_evidence(EXACT_IDENTITY, [])
        validate_evidence(expected)
        self.assertEqual(ARTIFACT.read_bytes(), canonical_json_bytes(expected))
        self.assertFalse(expected["probe"]["has_explicit_internal_page_labels"])
        self.assertEqual(expected["probe"]["page_label_entry_count"], 0)

    def test_validator_rejects_gate_or_source_payload_promotion(self) -> None:
        evidence = build_evidence(EXACT_IDENTITY, [])
        advanced = deepcopy(evidence)
        advanced["literary_page_selection_bound"] = True
        with self.assertRaisesRegex(ValueError, "forbidden page-label/corpus gate"):
            validate_evidence(advanced)

        leaked = deepcopy(evidence)
        leaked["source_text"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "forbidden source payload key"):
            validate_evidence(leaked)

    def test_file_identity_is_byte_exact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tiny.pdf"
            path.write_bytes(b"%PDF-source-free-test")
            identity = compute_file_identity(path)
        self.assertEqual(identity["byte_count"], 21)
        self.assertEqual(len(identity["sha1"]), 40)
        self.assertEqual(len(identity["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
