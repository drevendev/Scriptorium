from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_yo_render_profile_promotion import (
    BACKLOG_SCHEMA,
    EFFECTIVE_PROFILE_VERSION,
    PROMOTION_SCHEMA,
    build_backlog_v2,
    build_from_paths,
    build_profile_promotion,
    validate_promotion,
)


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "corpus/candidates/source-edition-traces"
SURFACE = TRACE / "darwin-origin-species-rachinsky-1864-ru.render-surface.json"
PROFILE_V1 = TRACE / "darwin-origin-species-rachinsky-1864-ru.render-profile.json"
BACKLOG_V1 = TRACE / "darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json"
REPLAY_V6 = TRACE / "darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v6.json"
PROMOTION = TRACE / "darwin-origin-species-rachinsky-1864-ru.render-profile-yo-promotion-v1.json"
BACKLOG_V2 = TRACE / "darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v2.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinYoRenderProfilePromotionTests(unittest.TestCase):
    def test_committed_successors_rebuild_exactly_from_reviewed_predecessors(self) -> None:
        expected_promotion, expected_backlog = build_from_paths(PROFILE_V1, BACKLOG_V1, SURFACE, REPLAY_V6)
        self.assertEqual(load(PROMOTION), expected_promotion)
        self.assertEqual(load(BACKLOG_V2), expected_backlog)
        validate_promotion(
            load(PROMOTION),
            load(BACKLOG_V2),
            load(PROFILE_V1),
            load(BACKLOG_V1),
            load(SURFACE),
            load(REPLAY_V6),
        )

    def test_only_zero_argument_yo_is_promoted(self) -> None:
        promotion = build_profile_promotion(load(PROFILE_V1), load(BACKLOG_V1), load(SURFACE), load(REPLAY_V6))
        self.assertEqual(promotion["schema_version"], PROMOTION_SCHEMA)
        rule = promotion["promoted_rule"]
        self.assertEqual((rule["name"], rule["positional"], rule["named"], rule["count"]), ("ё", 0, 0, 2227))
        self.assertEqual(rule["predecessor_semantic_status"], "unresolved")
        self.assertEqual(rule["semantic_status"], "defined")
        self.assertEqual(rule["outputs"]["forced_yoification"]["value"], "ё")
        self.assertEqual(rule["outputs"]["non_forced_yoification"]["value"], "е")
        effective = promotion["effective_profile"]
        self.assertEqual(effective["profile_version"], EFFECTIVE_PROFILE_VERSION)
        self.assertEqual(effective["unresolved_template_shape_count"], 37)
        self.assertEqual(effective["unresolved_template_invocation_count"], 2356)
        self.assertEqual(effective["unresolved_tag_shape_count"], 5)
        self.assertEqual(effective["unresolved_tag_token_count"], 518)

    def test_backlog_removes_exactly_one_shape_and_reranks_mechanically(self) -> None:
        promotion = build_profile_promotion(load(PROFILE_V1), load(BACKLOG_V1), load(SURFACE), load(REPLAY_V6))
        backlog = build_backlog_v2(promotion, load(PROFILE_V1), load(BACKLOG_V1), load(SURFACE), load(REPLAY_V6))
        self.assertEqual(backlog["schema_version"], BACKLOG_SCHEMA)
        self.assertEqual(backlog["remaining_priority_count"], 42)
        self.assertEqual(
            backlog["unresolved_totals"],
            {"tag_shape_count": 5, "tag_token_count": 518, "template_shape_count": 37, "template_invocation_count": 2356},
        )
        self.assertEqual(
            backlog["resolution_tracks"],
            [
                {"track": "provider_template", "shape_count": 36, "occurrence_count": 2352},
                {"track": "provider_reference", "shape_count": 3, "occurrence_count": 466},
                {"track": "provider_math", "shape_count": 2, "occurrence_count": 52},
                {"track": "inter_page", "shape_count": 1, "occurrence_count": 4},
            ],
        )
        self.assertEqual(
            backlog["next_research_slice"],
            {
                "source_kind": "tag",
                "name": "references",
                "kind": "self_closing",
                "count": 388,
                "predecessor_priority_rank": 2,
                "priority_rank": 1,
                "semantic_status": "unresolved",
                "reason": "highest remaining unresolved occurrence count after reviewed {{ё}} promotion; ties preserve deterministic predecessor ordering",
            },
        )

    def test_replay_digest_or_semantic_output_drift_fails_closed(self) -> None:
        replay = deepcopy(load(REPLAY_V6))
        replay["mode_verification"] = deepcopy(replay["mode_verification"])
        replay["mode_verification"]["forced_yoification"] = deepcopy(replay["mode_verification"]["forced_yoification"])
        replay["mode_verification"]["forced_yoification"]["verified_semantic_output"] = "е"
        with self.assertRaisesRegex(ValueError, "self-digest drift"):
            build_profile_promotion(load(PROFILE_V1), load(BACKLOG_V1), load(SURFACE), replay)

    def test_historical_or_offline_claim_drift_fails_closed(self) -> None:
        for key in ("historical_transclusion_provenance_proved", "offline_version_pinned_mediawiki_environment_claimed"):
            replay = deepcopy(load(REPLAY_V6))
            replay["replay_environment"] = deepcopy(replay["replay_environment"])
            replay["replay_environment"][key] = True
            replay["contract_sha256"] = "0" * 64
            with self.assertRaises(ValueError):
                build_profile_promotion(load(PROFILE_V1), load(BACKLOG_V1), load(SURFACE), replay)

    def test_predecessor_backlog_drift_fails_before_promotion(self) -> None:
        backlog = deepcopy(load(BACKLOG_V1))
        backlog["prioritized_items"] = [dict(row) for row in backlog["prioritized_items"]]
        backlog["prioritized_items"][0]["count"] -= 1
        with self.assertRaisesRegex(ValueError, "semantic backlog drift"):
            build_profile_promotion(load(PROFILE_V1), backlog, load(SURFACE), load(REPLAY_V6))

    def test_downstream_gates_and_provenance_boundaries_remain_closed(self) -> None:
        promotion = build_profile_promotion(load(PROFILE_V1), load(BACKLOG_V1), load(SURFACE), load(REPLAY_V6))
        backlog = build_backlog_v2(promotion, load(PROFILE_V1), load(BACKLOG_V1), load(SURFACE), load(REPLAY_V6))
        self.assertFalse(promotion["source_text_included"])
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
