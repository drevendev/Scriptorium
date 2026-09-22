from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import unittest

from scriptorium.perelman_djvu_text_layer import (
    DIAGNOSTIC_VERSION,
    EXPECTED_CARRIER_SHA256,
    EXPECTED_PACKAGE_VERSION,
    EXPECTED_PROVIDER_PAGE_COUNT,
    build_diagnostic,
    validate_diagnostic,
)


class PerelmanDjvuTextLayerTests(unittest.TestCase):
    def _diagnostic(self) -> dict[str, object]:
        pages = [b""] * EXPECTED_PROVIDER_PAGE_COUNT
        pages[2] = "Пример\n".encode("utf-8")
        pages[3] = "Текст\r\n".encode("utf-8")
        return build_diagnostic(b"".join(pages), pages, package_version=EXPECTED_PACKAGE_VERSION)

    def test_build_diagnostic_is_source_free_and_keeps_gates_closed(self) -> None:
        diagnostic = self._diagnostic()
        validate_diagnostic(diagnostic)
        self.assertEqual(diagnostic["diagnostic_version"], DIAGNOSTIC_VERSION)
        carrier = diagnostic["carrier"]
        assert isinstance(carrier, dict)
        self.assertEqual(carrier["sha256"], EXPECTED_CARRIER_SHA256)
        hidden = diagnostic["hidden_text"]
        assert isinstance(hidden, dict)
        self.assertTrue(hidden["present"])
        self.assertEqual(hidden["pages_with_nonempty_output"], 2)
        self.assertEqual(hidden["pages_without_output"][:3], [1, 2, 5])
        self.assertEqual(hidden["first_page_with_output"], 3)
        self.assertEqual(hidden["last_page_with_output"], 4)
        self.assertNotIn("text", hidden)
        self.assertFalse(diagnostic["source_text_included"])
        self.assertFalse(diagnostic["literary_page_selection_frozen"])
        self.assertFalse(diagnostic["literary_body_count_and_digests_frozen"])
        self.assertFalse(diagnostic["minimum_300k_proved_from_frozen_body"])
        self.assertFalse(diagnostic["admitted_for_calibration"])
        self.assertFalse(diagnostic["diagnostic_ready"])
        self.assertFalse(diagnostic["m2_parity_admissible"])

    def test_page_count_and_package_version_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "page-output count"):
            build_diagnostic(b"x", [b"x"], package_version=EXPECTED_PACKAGE_VERSION)
        with self.assertRaisesRegex(ValueError, "package version"):
            build_diagnostic(b"", [b""] * EXPECTED_PROVIDER_PAGE_COUNT, package_version="")
        diagnostic = self._diagnostic()
        assert isinstance(diagnostic["extractor"], dict)
        diagnostic["extractor"]["package_version"] = "different"
        with self.assertRaisesRegex(ValueError, "package version drift"):
            validate_diagnostic(diagnostic)

    def test_normalization_identity_is_explicit(self) -> None:
        pages = [b""] * EXPECTED_PROVIDER_PAGE_COUNT
        raw = "е\u0308\r\n".encode("utf-8")
        pages[0] = raw
        diagnostic = build_diagnostic(raw, pages, package_version=EXPECTED_PACKAGE_VERSION)
        hidden = diagnostic["hidden_text"]
        assert isinstance(hidden, dict)
        self.assertEqual(hidden["character_count"], 4)
        self.assertEqual(hidden["normalized_character_count"], 2)
        self.assertEqual(hidden["sha256"], sha256(raw).hexdigest())
        self.assertEqual(hidden["normalized_sha256"], sha256("ё\n".encode("utf-8")).hexdigest())

    def test_validator_rejects_source_payload_and_gate_promotion(self) -> None:
        diagnostic = self._diagnostic()
        leaked = deepcopy(diagnostic)
        hidden = leaked["hidden_text"]
        assert isinstance(hidden, dict)
        hidden["source_text"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "summary shape drift"):
            validate_diagnostic(leaked)

        advanced = deepcopy(diagnostic)
        advanced["minimum_300k_proved_from_frozen_body"] = True
        with self.assertRaisesRegex(ValueError, "forbidden corpus/parity gate"):
            validate_diagnostic(advanced)

        source_match = deepcopy(diagnostic)
        source_match["fantlab_source_edition_match"] = "exact"
        with self.assertRaisesRegex(ValueError, "FantLab source identity"):
            validate_diagnostic(source_match)

    def test_validator_rejects_page_accounting_contradiction(self) -> None:
        diagnostic = self._diagnostic()
        hidden = diagnostic["hidden_text"]
        assert isinstance(hidden, dict)
        hidden["pages_without_output"] = [1]
        with self.assertRaisesRegex(ValueError, "page accounting"):
            validate_diagnostic(diagnostic)


if __name__ == "__main__":
    unittest.main()
