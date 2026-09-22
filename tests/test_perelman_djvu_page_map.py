from __future__ import annotations

from copy import deepcopy
import unittest

from scriptorium.perelman_djvu_page_map import (
    EXPECTED_PACKAGE_VERSION,
    EXPECTED_PROVIDER_PAGE_COUNT,
    PAGE_MAP_VERSION,
    build_page_map,
    validate_page_map,
)


class PerelmanDjvuPageMapTests(unittest.TestCase):
    def _page_map(self) -> dict[str, object]:
        pages = [f"Страница {page}\n".encode("utf-8") for page in range(1, EXPECTED_PROVIDER_PAGE_COUNT + 1)]
        return build_page_map(pages, package_version=EXPECTED_PACKAGE_VERSION)

    def test_build_page_map_is_source_free_and_keeps_gates_closed(self) -> None:
        page_map = self._page_map()
        validate_page_map(page_map)
        self.assertEqual(page_map["page_map_version"], PAGE_MAP_VERSION)
        pages = page_map["pages"]
        assert isinstance(pages, list)
        self.assertEqual(len(pages), EXPECTED_PROVIDER_PAGE_COUNT)
        self.assertEqual(pages[0]["page"], 1)
        self.assertEqual(pages[-1]["page"], EXPECTED_PROVIDER_PAGE_COUNT)
        self.assertNotIn("text", pages[0])
        self.assertFalse(page_map["source_text_included"])
        self.assertFalse(page_map["page_images_committed"])
        self.assertFalse(page_map["literary_page_selection_frozen"])
        self.assertFalse(page_map["literary_body_count_and_digests_frozen"])
        self.assertFalse(page_map["minimum_300k_proved_from_frozen_body"])
        self.assertFalse(page_map["admitted_for_calibration"])
        self.assertFalse(page_map["diagnostic_ready"])
        self.assertFalse(page_map["m2_parity_admissible"])

    def test_build_rejects_page_count_and_package_drift(self) -> None:
        with self.assertRaisesRegex(ValueError, "page-output count"):
            build_page_map([b"x"], package_version=EXPECTED_PACKAGE_VERSION)
        with self.assertRaisesRegex(ValueError, "package version drift"):
            build_page_map([b""] * EXPECTED_PROVIDER_PAGE_COUNT, package_version="different")

    def test_validator_rejects_page_ordering_and_record_digest_drift(self) -> None:
        page_map = self._page_map()
        pages = page_map["pages"]
        assert isinstance(pages, list)
        pages[0]["page"] = 2
        with self.assertRaisesRegex(ValueError, "page ordering drift"):
            validate_page_map(page_map)

        page_map = self._page_map()
        page_map["page_records_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "records digest drift"):
            validate_page_map(page_map)

    def test_validator_rejects_source_payload_and_gate_promotion(self) -> None:
        page_map = self._page_map()
        leaked = deepcopy(page_map)
        pages = leaked["pages"]
        assert isinstance(pages, list)
        pages[0]["source_text"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "record shape drift"):
            validate_page_map(leaked)

        advanced = deepcopy(page_map)
        advanced["literary_page_selection_frozen"] = True
        with self.assertRaisesRegex(ValueError, "forbidden corpus/parity gate"):
            validate_page_map(advanced)

        matched = deepcopy(page_map)
        matched["fantlab_source_edition_match"] = "exact"
        with self.assertRaisesRegex(ValueError, "FantLab source identity"):
            validate_page_map(matched)

    def test_normalization_is_explicit_per_page(self) -> None:
        pages = [b""] * EXPECTED_PROVIDER_PAGE_COUNT
        pages[0] = "е\u0308\r\n".encode("utf-8")
        page_map = build_page_map(pages, package_version=EXPECTED_PACKAGE_VERSION)
        records = page_map["pages"]
        assert isinstance(records, list)
        first = records[0]
        self.assertEqual(first["character_count"], 4)
        self.assertEqual(first["normalized_character_count"], 2)
        self.assertNotEqual(first["sha256"], first["normalized_sha256"])


if __name__ == "__main__":
    unittest.main()
