from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

from scriptorium.twelve_chairs_page_freeze import EXPECTED_PAGE_COUNT, load_sharded_manifest
from scriptorium.twelve_chairs_render_surface import build_audit_manifest, validate_audit_manifest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json"


class TwelveChairsRenderSurfaceTests(unittest.TestCase):
    def _synthetic_fetcher(self, selected):
        result = {}
        for row in selected:
            result[int(row["revision_id"])] = (
                "<noinclude><pagequality level=\"4\" /></noinclude>"
                "{{razr|synthetic}} [[Example|label]]<br />"
                "<noinclude>footer</noinclude>"
            )
        return result

    def test_build_audits_exactly_410_pinned_dependencies(self) -> None:
        rows = load_sharded_manifest(INDEX)
        self.assertEqual(len(rows), EXPECTED_PAGE_COUNT)
        self.assertEqual(EXPECTED_PAGE_COUNT, 410)
        self.assertNotIn(150, {int(row["page_sequence"]) for row in rows})
        self.assertNotIn(151, {int(row["page_sequence"]) for row in rows})
        self.assertNotIn(314, {int(row["page_sequence"]) for row in rows})
        self.assertNotIn(315, {int(row["page_sequence"]) for row in rows})

        manifest = build_audit_manifest(INDEX, fetcher=self._synthetic_fetcher)
        validate_audit_manifest(manifest)
        self.assertEqual(manifest["dependency_count"], 410)
        self.assertEqual(len(manifest["page_surface_receipts"]), 410)
        self.assertTrue(manifest["identity_replay_match"])
        self.assertFalse(manifest["source_text_included"])

    def test_manifest_keeps_all_downstream_gates_closed(self) -> None:
        manifest = build_audit_manifest(INDEX, fetcher=self._synthetic_fetcher)
        validate_audit_manifest(manifest)
        for key in (
            "rendering_profile_frozen",
            "inter_page_composition_frozen",
            "literary_body_count_and_digests_frozen",
            "minimum_300k_proved",
            "admitted_for_calibration",
            "diagnostic_ready",
            "m2_parity_admissible",
        ):
            self.assertFalse(manifest[key], key)
        self.assertEqual(manifest["fantlab_source_edition_match"], "unknown")

    def test_receipts_do_not_serialize_source_payload(self) -> None:
        manifest = build_audit_manifest(INDEX, fetcher=self._synthetic_fetcher)
        serialized = str(manifest)
        self.assertNotIn("synthetic", serialized)
        self.assertNotIn("Example", serialized)
        self.assertNotIn("footer", serialized)
        receipt = manifest["page_surface_receipts"][0]
        self.assertEqual(
            set(receipt),
            {
                "page_sequence",
                "revision_id",
                "mediawiki_sha1",
                "wikitext_sha256",
                "surface_signature_sha256",
                "template_invocation_count",
                "tag_token_count",
            },
        )

    def test_validator_rejects_source_payload_key(self) -> None:
        manifest = build_audit_manifest(INDEX, fetcher=self._synthetic_fetcher)
        leaked = deepcopy(manifest)
        leaked["wikitext"] = "forbidden"
        with self.assertRaisesRegex(ValueError, "source payload key"):
            validate_audit_manifest(leaked)

    def test_validator_rejects_gate_promotion(self) -> None:
        manifest = build_audit_manifest(INDEX, fetcher=self._synthetic_fetcher)
        promoted = deepcopy(manifest)
        promoted["rendering_profile_frozen"] = True
        with self.assertRaisesRegex(ValueError, "rendering_profile_frozen must remain false"):
            validate_audit_manifest(promoted)


if __name__ == "__main__":
    unittest.main()
