from __future__ import annotations

import copy
import unittest

from scriptorium.mediawiki_part2_resolution import (
    EXPECTED_REACHED_COUNTS,
    _identity,
    _split_top_level,
    expand_poemx1_for_frozen_frame,
    validate_part2_resolution_manifest,
)


def _synthetic_reached_surface() -> str:
    value = "{{#tag:poem|{{{2|}}}}}"
    value = "{{#if:{{{3|}}}|bad|" + value + "}}"
    value = "{{#if:{{{poem|}}}|bad|" + value + "}}"
    value = "{{#if:{{{width|}}}|bad|" + value + "}}"
    for _ in range(3):
        value = "{{#ifeq:{{{fixed|+}}}|-|bad|" + value + "}}"
    return "{{#if:{{{1|}}}|{{#expr:1+1}}|" + value + "}}"


class BoundedExpansionTests(unittest.TestCase):
    def test_split_top_level_preserves_nested_parser_pipes(self) -> None:
        value = "#if:{{{1|}}}|A{{#ifeq:+|-|x|y}}|B"
        self.assertEqual(
            _split_top_level(value),
            ["#if:{{{1|}}}", "A{{#ifeq:+|-|x|y}}", "B"],
        )

    def test_lazy_if_does_not_reach_expr(self) -> None:
        expanded, trace = expand_poemx1_for_frozen_frame(
            _synthetic_reached_surface(), parameter_2_value="alpha\nbeta"
        )
        self.assertEqual(
            expanded, '<div class="poem">\nalpha<br />\nbeta\n</div>'
        )
        self.assertEqual(trace["reachable_construct_counts"], EXPECTED_REACHED_COUNTS)
        self.assertEqual(trace["rendered_poem_fragment_sha256"], _identity(expanded)["sha256"])

    def test_active_poem_syntax_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "brace syntax|active syntax"):
            expand_poemx1_for_frozen_frame(
                _synthetic_reached_surface(), parameter_2_value="{{danger}}"
            )

    def test_validator_keeps_gate_closed(self) -> None:
        rows = []
        for index in range(1, 7):
            rows.append(
                {
                    "invocation_index": index,
                    "expanded_template_output": {
                        "character_count": 10,
                        "utf8_byte_count": 10,
                        "sha256": "a" * 64,
                    },
                    "reachable_construct_counts": dict(EXPECTED_REACHED_COUNTS),
                }
            )
        manifest = {
            "manifest_version": "scriptorium-klim-samgin-part2-resolution-v1",
            "candidate_id": "gorky-klim-samgin-ru-part-2",
            "profile": "scriptorium-klim-samgin-bounded-template-expansion-v1",
            "evidence_class": "candidate_specific_inferred_reconstruction",
            "poemx1_expansions": rows,
            "expanded_dependency_identity": {
                "character_count": 100,
                "utf8_byte_count": 100,
                "sha256": "b" * 64,
            },
            "resolved_parent_part2_identity": {
                "character_count": 200,
                "utf8_byte_count": 200,
                "sha256": "c" * 64,
            },
            "remaining_expansion_surface": {
                "poemx1_invocation_count": 0,
                "double_brace_open_count": 0,
                "double_brace_close_count": 0,
            },
            "capture_scope": {
                "resolved_part2_wikitext_identity_frozen": True,
                "candidate_specific_literary_body_extraction_frozen": False,
                "four_part_literary_body_composite_frozen": False,
                "historical_render_equivalence_proven": False,
                "source_text_committed": False,
            },
            "source_text_included": False,
            "fantlab_source_edition_match": "unknown",
            "diagnostic_ready": False,
            "gate_ready": False,
            "m2_parity_admissible": False,
        }
        validate_part2_resolution_manifest(manifest)
        bad = copy.deepcopy(manifest)
        bad["m2_parity_admissible"] = True
        with self.assertRaisesRegex(ValueError, "advance M2"):
            validate_part2_resolution_manifest(bad)


if __name__ == "__main__":
    unittest.main()
