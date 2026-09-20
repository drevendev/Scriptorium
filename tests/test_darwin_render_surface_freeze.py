from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import unittest

from scriptorium.darwin_render_surface_freeze import build_freeze_manifest, validate_freeze_manifest


def _canonical_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


class DarwinRenderSurfaceFreezeTests(unittest.TestCase):
    def _audit(self) -> dict[str, object]:
        pages = [
            {
                "page_sequence": index,
                "revision_id": 100000 + index,
                "mediawiki_sha1": f"sha1-{index}",
                "wikitext_sha256": f"raw-{index}",
                "surface_signature_sha256": f"surface-{index}",
                "template_invocation_count": index % 3,
                "tag_token_count": 4,
            }
            for index in range(1, 389)
        ]
        audit: dict[str, object] = {
            "audit_version": "scriptorium-darwin-render-surface-audit-v1",
            "candidate_id": "darwin-origin-species-rachinsky-1864-ru",
            "status": "surface_inventory_frozen_renderer_unfrozen",
            "source_revision_index_sha256": "index-digest",
            "literary_dependency_count": 388,
            "identity_replay_match": True,
            "source_text_included": False,
            "template_shapes": [{"name": "ё", "positional": 0, "named": 0, "count": 12}],
            "tag_shapes": [{"name": "ref", "kind": "open", "count": 2}],
            "construct_totals": {"comment_count": 1},
            "page_surface_receipts": pages,
            "rendering_profile_frozen": False,
            "literary_body_count_and_digests_frozen": False,
            "minimum_300k_proved": False,
            "admitted_for_calibration": False,
            "fantlab_source_edition_match": "unknown",
            "diagnostic_ready": False,
            "m2_parity_admissible": False,
        }
        audit["audit_sha256"] = _canonical_sha256(audit)
        return audit

    def test_freeze_is_compact_deterministic_and_keeps_gates_closed(self) -> None:
        audit = self._audit()
        freeze = build_freeze_manifest(audit)
        validate_freeze_manifest(freeze)
        self.assertEqual(freeze["page_surface_receipts_count"], 388)
        self.assertNotIn("page_surface_receipts", freeze)
        self.assertEqual(freeze["page_surface_receipts_sha256"], _canonical_sha256(audit["page_surface_receipts"]))
        self.assertFalse(freeze["rendering_profile_frozen"])
        self.assertFalse(freeze["minimum_300k_proved"])
        self.assertFalse(freeze["m2_parity_admissible"])
        self.assertEqual(build_freeze_manifest(audit), freeze)

    def test_freeze_validator_rejects_gate_promotion_and_digest_drift(self) -> None:
        freeze = build_freeze_manifest(self._audit())
        promoted = deepcopy(freeze)
        promoted["rendering_profile_frozen"] = True
        with self.assertRaisesRegex(ValueError, "must remain false"):
            validate_freeze_manifest(promoted)

        drifted = deepcopy(freeze)
        drifted["construct_totals"] = {"comment_count": 999}
        with self.assertRaisesRegex(ValueError, "digest drift"):
            validate_freeze_manifest(drifted)


if __name__ == "__main__":
    unittest.main()
