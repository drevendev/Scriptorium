from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.darwin_semantic_backlog import build_backlog, build_backlog_from_paths, validate_backlog


ROOT = Path(__file__).resolve().parents[1]
SURFACE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-surface.json"
PROFILE = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile.json"
BACKLOG = ROOT / "corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json"


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class DarwinSemanticBacklogTests(unittest.TestCase):
    def test_committed_backlog_rebuilds_exactly_from_reviewed_profile(self) -> None:
        expected = build_backlog_from_paths(PROFILE, SURFACE)
        committed = load(BACKLOG)
        self.assertEqual(committed, expected)
        validate_backlog(committed, load(PROFILE), load(SURFACE))

    def test_all_unresolved_shapes_are_preserved_and_grouped(self) -> None:
        backlog = build_backlog(load(PROFILE), load(SURFACE))
        self.assertEqual(
            backlog["unresolved_totals"],
            {
                "tag_shape_count": 5,
                "tag_token_count": 518,
                "template_shape_count": 38,
                "template_invocation_count": 4583,
            },
        )
        self.assertEqual(
            backlog["resolution_tracks"],
            [
                {"track": "provider_template", "shape_count": 37, "occurrence_count": 4579},
                {"track": "provider_reference", "shape_count": 3, "occurrence_count": 466},
                {"track": "provider_math", "shape_count": 2, "occurrence_count": 52},
                {"track": "inter_page", "shape_count": 1, "occurrence_count": 4},
            ],
        )
        items = backlog["prioritized_items"]
        self.assertEqual(len(items), 43)
        self.assertTrue(all(row["semantic_status"] == "unresolved" for row in items))

    def test_next_slice_is_mechanical_not_a_semantics_claim(self) -> None:
        backlog = build_backlog(load(PROFILE), load(SURFACE))
        next_slice = backlog["next_research_slice"]
        self.assertEqual(next_slice["source_kind"], "template")
        self.assertEqual(next_slice["name"], "ё")
        self.assertEqual(next_slice["count"], 2227)
        self.assertEqual(next_slice["share_of_unresolved_template_invocations"], {"numerator": 2227, "denominator": 4583})
        self.assertEqual(next_slice["semantic_status"], "unresolved")
        self.assertEqual(backlog["prioritized_items"][0]["priority_rank"], 1)

    def test_profile_drift_fails_before_backlog_derivation(self) -> None:
        profile = deepcopy(load(PROFILE))
        profile["template_rules"] = [dict(row) for row in profile["template_rules"]]
        profile["template_rules"][-1]["count"] += 1
        with self.assertRaisesRegex(ValueError, "profile digest drift"):
            build_backlog(profile, load(SURFACE))

    def test_backlog_keeps_source_and_downstream_gates_closed(self) -> None:
        backlog = build_backlog(load(PROFILE), load(SURFACE))
        self.assertFalse(backlog["source_text_included"])
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
