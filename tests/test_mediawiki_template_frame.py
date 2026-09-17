from __future__ import annotations

import unittest

from scriptorium.mediawiki_template_frame import (
    MANIFEST_VERSION,
    PROFILE_VERSION,
    build_parameter_surface_manifest,
    expand_literal_template_parameters,
    parameter_reference_inventory,
)


class MediaWikiTemplateFrameTests(unittest.TestCase):
    def test_defined_and_defined_empty_values_suppress_defaults(self) -> None:
        text = "A={{{a|fallback}}};B={{{b|fallback}}}"
        self.assertEqual(
            expand_literal_template_parameters(text, {"a": "value", "b": ""}),
            "A=value;B=",
        )

    def test_missing_default_and_missing_bare_parameter_are_distinct(self) -> None:
        text = "A={{{a|fallback}}};B={{{b}}}"
        self.assertEqual(
            expand_literal_template_parameters(text, {}),
            "A=fallback;B={{{b}}}",
        )

    def test_nested_literal_parameter_default_is_expanded(self) -> None:
        text = "{{{a|{{{b|fallback}}}}}}"
        self.assertEqual(expand_literal_template_parameters(text, {"b": "nested"}), "nested")
        self.assertEqual(expand_literal_template_parameters(text, {}), "fallback")
        self.assertEqual(expand_literal_template_parameters(text, {"a": "outer"}), "outer")

    def test_inserted_value_is_not_recursively_expanded_by_parameter_layer(self) -> None:
        value = "{{#if:x|yes|no}}"
        self.assertEqual(expand_literal_template_parameters("{{{1|}}}", {"1": value}), value)

    def test_dynamic_or_malformed_parameter_name_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            expand_literal_template_parameters("{{{{{name}}}|fallback}}", {"name": "1"})

    def test_inventory_counts_nested_default_references_without_source_text(self) -> None:
        inventory = parameter_reference_inventory(
            "{{{1|}}} {{{1}}} {{{width|{{{fixed|12}}}}}} {{{small|}}}"
        )
        self.assertEqual(inventory["total_reference_count"], 5)
        self.assertEqual(
            inventory["parameter_reference_counts"],
            {"1": 2, "fixed": 1, "small": 1, "width": 1},
        )
        self.assertEqual(
            inventory["defaulted_reference_counts"],
            {"1": 1, "fixed": 1, "small": 1, "width": 1},
        )
        self.assertEqual(inventory["empty_default_reference_counts"], {"1": 1, "small": 1})
        self.assertEqual(inventory["bare_reference_counts"], {"1": 1})

    def test_manifest_is_source_free_and_stops_before_invocation_binding(self) -> None:
        transclusion_input = "{{#if:{{{1|}}}|{{{1}}}|}}{{#tag:poem|{{{2|}}}}}"
        manifest = build_parameter_surface_manifest(
            candidate_id="gorky-klim-samgin-ru-poemx1-template",
            revision_identity={
                "title": "Шаблон:Poemx1",
                "revision_id": 5142743,
                "wikitext_sha256": "f" * 64,
            },
            transclusion_input=transclusion_input,
            research_date="2026-09-17",
        )
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["parameter_profile"], PROFILE_VERSION)
        self.assertEqual(
            manifest["parameter_surface"]["parameter_reference_counts"],
            {"1": 2, "2": 1},
        )
        scope = manifest["capture_scope"]
        self.assertIs(scope["literal_parameter_default_semantics_reproduced"], True)
        self.assertIs(scope["invocation_argument_binding_reproduced"], False)
        self.assertIs(scope["parser_function_expansion_reproduced"], False)
        self.assertIs(scope["historical_render_equivalence_proven"], False)
        self.assertNotIn("transclusion_input", manifest)
        self.assertIs(manifest["source_text_included"], False)


if __name__ == "__main__":
    unittest.main()
