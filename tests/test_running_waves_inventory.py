import copy
import json
from pathlib import Path
import unittest

from scriptorium.running_waves_inventory import (
    CATEGORY_PAGE_COUNT,
    CATEGORY_REVISION_ID,
    EXCLUDED_ROUTE_REVISION_ID,
    EXCLUDED_ROUTE_TITLE,
    MANIFEST_VERSION,
    build_manifest,
    expected_literary_titles,
    validate_manifest,
)


MANIFEST_PATH = (
    Path(__file__).resolve().parents[1]
    / "corpus"
    / "candidates"
    / "source-edition-traces"
    / "grin-running-on-waves-ru.route-inventory.json"
)


class RunningWavesInventoryTests(unittest.TestCase):
    def test_expected_route_has_exact_35_chapters_plus_epilogue(self):
        titles = expected_literary_titles()
        self.assertEqual(len(titles), 36)
        self.assertEqual(titles[0], "Бегущая по волнам (Грин)/1")
        self.assertEqual(titles[34], "Бегущая по волнам (Грин)/35")
        self.assertEqual(titles[-1], "Бегущая по волнам (Грин)/Эпилог")
        self.assertEqual(len(set(titles)), 36)

    def test_build_manifest_freezes_route_topology_not_page_revisions_or_body(self):
        manifest = build_manifest()
        titles = validate_manifest(manifest)
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(
            manifest["route_inventory_witness"]["category_revision_id"],
            CATEGORY_REVISION_ID,
        )
        self.assertEqual(
            manifest["route_inventory_witness"]["listed_page_count"],
            CATEGORY_PAGE_COUNT,
        )
        self.assertEqual(len(titles), 36)
        scope = manifest["capture_scope"]
        self.assertTrue(scope["route_inventory_frozen"])
        self.assertFalse(scope["literary_page_revisions_frozen"])
        self.assertFalse(scope["literary_body_extraction_frozen"])
        self.assertFalse(scope["composite_identity_frozen"])
        self.assertFalse(scope["source_text_committed"])
        serialized = json.dumps(manifest, ensure_ascii=False)
        for forbidden in ("wikitext", "source_prose", "literary_text", "content_sha256"):
            self.assertNotIn(forbidden, serialized)

    def test_distinct_1980_route_is_explicitly_excluded(self):
        manifest = build_manifest()
        route = manifest["excluded_distinct_routes"][0]
        self.assertEqual(route["title"], EXCLUDED_ROUTE_TITLE)
        self.assertEqual(route["revision_id"], EXCLUDED_ROUTE_REVISION_ID)
        self.assertEqual(route["source"], "az.lib.ru")
        self.assertEqual(
            route["relationship"],
            "distinct_transcription_route_not_composed_into_primary",
        )

    def test_validate_manifest_fails_closed_on_title_or_boundary_drift(self):
        manifest = build_manifest()
        drifted = copy.deepcopy(manifest)
        drifted["route_inventory_witness"]["literary_titles"][2] = "wrong title"
        with self.assertRaisesRegex(ValueError, "title inventory drift"):
            validate_manifest(drifted)

        drifted = copy.deepcopy(manifest)
        drifted["excluded_distinct_routes"][0]["revision_id"] += 1
        with self.assertRaisesRegex(ValueError, "excluded route boundary drift"):
            validate_manifest(drifted)

        drifted = copy.deepcopy(manifest)
        drifted["capture_scope"]["literary_page_revisions_frozen"] = True
        with self.assertRaisesRegex(ValueError, "capture scope drift"):
            validate_manifest(drifted)

    def test_committed_manifest_matches_deterministic_builder(self):
        committed = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(committed, build_manifest())
        self.assertEqual(validate_manifest(committed), expected_literary_titles())


if __name__ == "__main__":
    unittest.main()
