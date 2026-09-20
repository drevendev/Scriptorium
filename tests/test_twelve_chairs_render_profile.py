from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from scriptorium.twelve_chairs_render_profile import (
    build_profile,
    build_profile_from_path,
    validate_profile,
)


ROOT = Path(__file__).resolve().parents[1]
SURFACE = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.render-surface.json"
PROFILE = ROOT / "corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.render-profile.json"


def load_surface() -> dict[str, object]:
    value = json.loads(SURFACE.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class TwelveChairsRenderProfileTests(unittest.TestCase):
    def test_committed_profile_rebuilds_exactly_from_reviewed_surface(self) -> None:
        expected = build_profile_from_path(SURFACE)
        committed = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(committed, expected)
        validate_profile(committed, load_surface())

    def test_profile_classifies_all_shapes_but_keeps_semantics_incomplete(self) -> None:
        profile = build_profile(load_surface())
        coverage = profile["coverage"]
        self.assertEqual(coverage["observed_tag_shape_count"], 12)
        self.assertEqual(coverage["observed_tag_token_count"], 3488)
        self.assertEqual(coverage["observed_template_shape_count"], 30)
        self.assertEqual(coverage["observed_template_invocation_count"], 602)
        self.assertEqual(coverage["unresolved_tag_shape_count"], 1)
        self.assertEqual(coverage["unresolved_tag_token_count"], 410)
        self.assertEqual(coverage["unresolved_template_shape_count"], 30)
        self.assertEqual(coverage["unresolved_template_invocation_count"], 602)
        self.assertTrue(coverage["all_observed_shapes_classified"])
        self.assertTrue(profile["rendering_profile_frozen"])
        self.assertFalse(profile["renderer_semantics_complete"])
        self.assertFalse(profile["renderer_implementation_ready"])
        self.assertFalse(profile["rendering_equivalence_claimed"])

    def test_profile_fails_closed_on_new_template_shape(self) -> None:
        surface = deepcopy(load_surface())
        surface["template_shapes"] = list(surface["template_shapes"])
        surface["template_shapes"].append({"name": "unexpected", "positional": 0, "named": 0, "count": 1})
        with self.assertRaisesRegex(ValueError, "template decision coverage drift"):
            build_profile(surface)

    def test_profile_fails_closed_on_missing_tag_shape(self) -> None:
        surface = deepcopy(load_surface())
        surface["tag_shapes"] = list(surface["tag_shapes"])[1:]
        with self.assertRaisesRegex(ValueError, "tag decision coverage drift"):
            build_profile(surface)

    def test_profile_keeps_composition_body_and_parity_gates_closed(self) -> None:
        profile = build_profile(load_surface())
        for key in (
            "inter_page_composition_frozen",
            "literary_body_count_and_digests_frozen",
            "minimum_300k_proved",
            "admitted_for_calibration",
            "diagnostic_ready",
            "m2_parity_admissible",
        ):
            self.assertFalse(profile[key], key)
        self.assertEqual(profile["fantlab_source_edition_match"], "unknown")
        self.assertFalse(profile["source_text_included"])
        self.assertFalse(profile["extraction_policy"]["persist_source_wikitext"])
        self.assertFalse(profile["extraction_policy"]["persist_rendered_prose"])


if __name__ == "__main__":
    unittest.main()
