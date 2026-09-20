from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

from scriptorium.twelve_chairs_render_surface import build_audit_manifest
from scriptorium.twelve_chairs_render_surface_freeze import build_freeze_manifest, validate_freeze_manifest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json"


def synthetic_fetcher(selected):
    return {
        int(row["revision_id"]): (
            "<noinclude><pagequality level=\"4\" /></noinclude>"
            "{{razr|synthetic}}<br /><references />"
            "<noinclude>footer</noinclude>"
        )
        for row in selected
    }


class TwelveChairsRenderSurfaceFreezeTests(unittest.TestCase):
    def test_freeze_reduces_receipts_without_source_payload(self) -> None:
        audit = build_audit_manifest(INDEX, fetcher=synthetic_fetcher)
        freeze = build_freeze_manifest(audit)
        validate_freeze_manifest(freeze)
        self.assertEqual(freeze["dependency_count"], 410)
        self.assertEqual(freeze["page_surface_receipts_count"], 410)
        self.assertNotIn("page_surface_receipts", freeze)
        self.assertFalse(freeze["source_text_included"])
        self.assertEqual(len(freeze["page_surface_receipts_sha256"]), 64)
        self.assertEqual(len(freeze["freeze_manifest_sha256"]), 64)

    def test_freeze_keeps_renderer_body_and_parity_gates_closed(self) -> None:
        audit = build_audit_manifest(INDEX, fetcher=synthetic_fetcher)
        freeze = build_freeze_manifest(audit)
        validate_freeze_manifest(freeze)
        for key in (
            "rendering_profile_frozen",
            "inter_page_composition_frozen",
            "literary_body_count_and_digests_frozen",
            "minimum_300k_proved",
            "admitted_for_calibration",
            "diagnostic_ready",
            "m2_parity_admissible",
        ):
            self.assertFalse(freeze[key], key)
        self.assertEqual(freeze["fantlab_source_edition_match"], "unknown")

    def test_validator_rejects_digest_drift(self) -> None:
        audit = build_audit_manifest(INDEX, fetcher=synthetic_fetcher)
        freeze = build_freeze_manifest(audit)
        drifted = deepcopy(freeze)
        drifted["construct_totals"] = dict(drifted["construct_totals"])
        drifted["construct_totals"]["comment_count"] += 1
        with self.assertRaisesRegex(ValueError, "digest drift"):
            validate_freeze_manifest(drifted)


if __name__ == "__main__":
    unittest.main()
