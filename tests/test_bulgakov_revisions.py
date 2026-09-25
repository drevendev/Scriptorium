from __future__ import annotations

import copy
import unittest

from scriptorium.white_guard_revisions import (
    SOURCE_FAMILY_1927,
    SOURCE_FAMILY_1989,
    build_manifest,
    expected_pages,
    replay_manifest,
    validate_manifest,
)


def _fake_identity_fetcher(pages):
    return {
        str(page["title"]): {
            "page_id": 1000 + int(page["chapter"]),
            "revision_id": 2000 + int(page["chapter"]),
            "revision_timestamp": "2026-09-24T00:00:00Z",
            "mediawiki_sha1": f"{int(page['chapter']):040x}",
        }
        for page in pages
    }


class BulgakovRevisionTests(unittest.TestCase):
    def test_expected_inventory_and_source_partition(self):
        pages = expected_pages()

        self.assertEqual(20, len(pages))
        self.assertEqual(list(range(1, 21)), [page["chapter"] for page in pages])
        self.assertEqual(list(range(1, 21)), [page["ordinal"] for page in pages])
        self.assertEqual(
            [SOURCE_FAMILY_1927] * 11 + [SOURCE_FAMILY_1989] * 9,
            [page["source_family_id"] for page in pages],
        )
        self.assertTrue(all(str(page["title"]).endswith(f"Глава {page['chapter']}") for page in pages))

    def test_build_manifest_is_source_free_and_fail_closed_by_default(self):
        manifest = build_manifest(fetcher=_fake_identity_fetcher)

        self.assertEqual(20, len(manifest["pages"]))
        self.assertEqual(
            {
                "literary_page_count": 20,
                "order": "chapter-number order 1 through 20",
                "single_edition_identity": False,
            },
            manifest["composition_contract"],
        )
        self.assertEqual(
            {
                "literary_page_revisions_frozen": True,
                "source_partition_frozen": True,
                "literary_body_extraction_frozen": False,
                "composite_identity_frozen": False,
                "single_edition_identity": False,
                "source_text_committed": False,
                "fantlab_source_edition_match": "unknown",
            },
            manifest["capture_scope"],
        )
        self.assertFalse(any("text" in key or "prose" in key for row in manifest["pages"] for key in row))

    def test_validate_manifest_preserves_order_and_identity(self):
        manifest = build_manifest(fetcher=_fake_identity_fetcher)
        identities = validate_manifest(manifest)

        self.assertEqual(20, len(identities))
        self.assertEqual(list(range(1, 21)), [identity["ordinal"] for identity in identities])
        self.assertEqual(2001, identities[0]["revision_id"])
        self.assertEqual(2020, identities[-1]["revision_id"])

    def test_validate_manifest_rejects_partition_drift(self):
        manifest = build_manifest(fetcher=_fake_identity_fetcher)
        manifest["pages"][11]["source_family_id"] = SOURCE_FAMILY_1927

        with self.assertRaisesRegex(ValueError, "source-partition drift"):
            validate_manifest(manifest)

    def test_validate_manifest_rejects_boolean_provider_identity(self):
        for field in ("page_id", "revision_id"):
            with self.subTest(field=field):
                manifest = build_manifest(fetcher=_fake_identity_fetcher)
                manifest["pages"][0][field] = True

                with self.assertRaises(ValueError):
                    validate_manifest(manifest)

    def test_validate_manifest_rejects_duplicate_provider_identity(self):
        manifest = build_manifest(fetcher=_fake_identity_fetcher)
        manifest["pages"][1]["page_id"] = manifest["pages"][0]["page_id"]

        with self.assertRaisesRegex(ValueError, "invalid/duplicate page id"):
            validate_manifest(manifest)

    def test_validate_manifest_rejects_composition_contract_drift(self):
        manifest = build_manifest(fetcher=_fake_identity_fetcher)
        manifest["composition_contract"] = copy.deepcopy(manifest["composition_contract"])
        manifest["composition_contract"]["single_edition_identity"] = True

        with self.assertRaisesRegex(ValueError, "composition contract drift"):
            validate_manifest(manifest)

    def test_validate_manifest_rejects_promotion_scope_drift(self):
        manifest = build_manifest(fetcher=_fake_identity_fetcher)
        manifest["capture_scope"] = copy.deepcopy(manifest["capture_scope"])
        manifest["capture_scope"]["literary_body_extraction_frozen"] = True

        with self.assertRaisesRegex(ValueError, "capture scope drift"):
            validate_manifest(manifest)

    def test_replay_manifest_keeps_body_and_parity_gates_closed(self):
        manifest = build_manifest(fetcher=_fake_identity_fetcher)

        replay_identities = []

        def replay_fetcher(identities):
            rows = tuple(identities)
            replay_identities.extend(rows)
            return {str(identity["title"]): "transient provider payload" for identity in rows}

        receipt = replay_manifest(manifest, fetcher=replay_fetcher)

        self.assertEqual(1001, replay_identities[0]["page_id"])
        self.assertEqual(1020, replay_identities[-1]["page_id"])
        self.assertEqual(
            {
                "verified": True,
                "candidate_id": "bulgakov-white-guard-ru",
                "verified_literary_page_count": 20,
                "source_partition_frozen": True,
                "literary_body_extraction_frozen": False,
                "composite_identity_frozen": False,
                "single_edition_identity": False,
                "source_text_committed": False,
                "fantlab_source_edition_match": "unknown",
            },
            receipt,
        )


if __name__ == "__main__":
    unittest.main()
