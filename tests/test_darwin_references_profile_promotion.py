from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_references_profile_promotion import (
    BACKLOG_SCHEMA,
    EFFECTIVE_PROFILE_VERSION,
    PROMOTION_SCHEMA,
    build_backlog_v3,
    build_from_paths,
    build_profile_promotion,
    validate_promotion,
)

ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "corpus/candidates/source-edition-traces"
YO_PROMOTION = TRACE / "darwin-origin-species-rachinsky-1864-ru.render-profile-yo-promotion-v1.json"
BACKLOG_V2 = TRACE / "darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v2.json"
PROBE = TRACE / "darwin-origin-species-rachinsky-1864-ru.references-containment-v1.json"
PROMOTION = TRACE / "darwin-origin-species-rachinsky-1864-ru.render-profile-references-promotion-v1.json"
BACKLOG_V3 = TRACE / "darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v3.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinReferencesProfilePromotionTests(unittest.TestCase):
    def test_committed_successors_rebuild_exactly(self) -> None:
        promotion, backlog = build_from_paths(YO_PROMOTION, BACKLOG_V2, PROBE)
        self.assertEqual(load(PROMOTION), promotion)
        self.assertEqual(load(BACKLOG_V3), backlog)
        validate_promotion(promotion, backlog, load(YO_PROMOTION), load(BACKLOG_V2), load(PROBE))

    def test_promotes_only_candidate_local_references_shape(self) -> None:
        promotion = build_profile_promotion(load(YO_PROMOTION), load(BACKLOG_V2), load(PROBE))
        self.assertEqual(promotion["schema_version"], PROMOTION_SCHEMA)
        self.assertEqual(
            promotion["promoted_rule"],
            {
                "source_kind": "tag",
                "name": "references",
                "kind": "self_closing",
                "count": 388,
                "predecessor_handling": "provider_reference_semantics_required",
                "predecessor_semantic_status": "unresolved",
                "handling": "drop_via_existing_strip_nontranscluded_region",
                "semantic_status": "defined_candidate_local",
            },
        )
        effective = promotion["effective_profile"]
        self.assertEqual(effective["profile_version"], EFFECTIVE_PROFILE_VERSION)
        self.assertEqual((effective["unresolved_tag_shape_count"], effective["unresolved_tag_token_count"]), (4, 130))
        self.assertEqual((effective["unresolved_template_shape_count"], effective["unresolved_template_invocation_count"]), (37, 2356))

    def test_backlog_removes_exactly_references_and_advances_to_var(self) -> None:
        promotion = build_profile_promotion(load(YO_PROMOTION), load(BACKLOG_V2), load(PROBE))
        backlog = build_backlog_v3(promotion, load(YO_PROMOTION), load(BACKLOG_V2), load(PROBE))
        self.assertEqual(backlog["schema_version"], BACKLOG_SCHEMA)
        self.assertEqual(backlog["remaining_priority_count"], 41)
        self.assertEqual(
            backlog["unresolved_totals"],
            {"tag_shape_count": 4, "tag_token_count": 130, "template_shape_count": 37, "template_invocation_count": 2356},
        )
        self.assertEqual(
            backlog["resolution_tracks"],
            [
                {"track": "provider_template", "shape_count": 36, "occurrence_count": 2352},
                {"track": "provider_reference", "shape_count": 2, "occurrence_count": 78},
                {"track": "provider_math", "shape_count": 2, "occurrence_count": 52},
                {"track": "inter_page", "shape_count": 1, "occurrence_count": 4},
            ],
        )
        self.assertEqual(backlog["next_research_slice"]["name"], "ВАР")
        self.assertEqual(backlog["next_research_slice"]["count"], 388)
        self.assertEqual(backlog["next_research_slice"]["priority_rank"], 1)

    def test_containment_or_probe_digest_drift_fails_closed(self) -> None:
        probe = deepcopy(load(PROBE))
        probe["containment_evidence"] = deepcopy(probe["containment_evidence"])
        probe["containment_evidence"]["references_outside_noinclude"] = 1
        with self.assertRaises(ValueError):
            build_profile_promotion(load(YO_PROMOTION), load(BACKLOG_V2), probe)

    def test_cite_semantics_claim_drift_fails_closed(self) -> None:
        probe = deepcopy(load(PROBE))
        probe["promotion_decision"] = deepcopy(probe["promotion_decision"])
        probe["promotion_decision"]["provider_cite_semantics_replayed"] = True
        with self.assertRaises(ValueError):
            build_profile_promotion(load(YO_PROMOTION), load(BACKLOG_V2), probe)

    def test_downstream_gates_and_provenance_boundaries_remain_closed(self) -> None:
        promotion = build_profile_promotion(load(YO_PROMOTION), load(BACKLOG_V2), load(PROBE))
        backlog = build_backlog_v3(promotion, load(YO_PROMOTION), load(BACKLOG_V2), load(PROBE))
        self.assertFalse(promotion["source_text_included"])
        self.assertFalse(promotion["semantic_evidence"]["provider_cite_semantics_replayed"])
        self.assertFalse(promotion["semantic_evidence"]["historical_transclusion_provenance_proved"])
        self.assertFalse(promotion["semantic_evidence"]["offline_version_pinned_mediawiki_environment_claimed"])
        for key in (
            "renderer_semantics_complete",
            "renderer_implementation_ready",
            "inter_page_composition_frozen",
            "literary_body_count_and_digests_frozen",
            "minimum_300k_proved",
            "admitted_for_calibration",
            "diagnostic_ready",
            "m2_parity_admissible",
        ):
            self.assertFalse(backlog[key], key)
        self.assertEqual(backlog["fantlab_source_edition_match"], "unknown")


if __name__ == "__main__":
    unittest.main()
