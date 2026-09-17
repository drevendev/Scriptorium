from __future__ import annotations

import unittest

from scriptorium.mediawiki_poemx1_control import (
    MANIFEST_VERSION,
    PROFILE_VERSION,
    build_poemx1_control_flow_manifest,
)


def _transclusion_manifest() -> dict[str, object]:
    return {
        "manifest_version": "scriptorium-template-transclusion-shape-v1",
        "source_revision": {
            "revision_id": 5142743,
            "wikitext_sha256": "fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db",
        },
        "effective_dependency_graph": {
            "parser_function_counts": {
                "#expr": 2,
                "#if": 5,
                "#ifeq": 5,
                "#iferror": 1,
                "#tag": 1,
            },
            "extension_tag_targets": {"poem": 1},
        },
    }


def _parameter_manifest() -> dict[str, object]:
    return {
        "manifest_version": "scriptorium-template-parameter-surface-v1",
        "transclusion_input_sha256": "86ad628a9d8fc3d904fd513a1b4335f4e9f816ceedfa2af736e8e3a94e32ffbf",
        "source_revision": {
            "revision_id": 5142743,
            "wikitext_sha256": "fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db",
        },
        "parameter_surface": {
            "parameter_reference_counts": {
                "1": 2,
                "2": 1,
                "3": 2,
                "fixed": 6,
                "poem": 1,
                "small": 6,
                "width": 3,
            }
        },
    }


def _binding_manifest() -> dict[str, object]:
    invocations = []
    for index in range(1, 7):
        invocations.append(
            {
                "invocation_index": index,
                "invocation_sha256": f"{index:064x}",
                "argument_count": 2,
                "anonymous_argument_count": 2,
                "named_argument_count": 0,
                "duplicate_assignment_counts": {},
                "effective_bindings": {
                    "1": {"defined_empty": True},
                    "2": {"defined_empty": False},
                },
            }
        )
    return {
        "manifest_version": "scriptorium-template-invocation-bindings-v1",
        "expected_invocation_count": 6,
        "invocations": invocations,
    }


class MediaWikiPoemx1ControlTests(unittest.TestCase):
    def test_frozen_frame_resolves_control_flow_without_rendering_poem(self) -> None:
        manifest = build_poemx1_control_flow_manifest(
            transclusion_manifest=_transclusion_manifest(),
            parameter_manifest=_parameter_manifest(),
            binding_manifest=_binding_manifest(),
            research_date="2026-09-17",
        )
        self.assertEqual(manifest["manifest_version"], MANIFEST_VERSION)
        self.assertEqual(manifest["control_profile"], PROFILE_VERSION)
        self.assertEqual(
            manifest["shared_source_free_frame"],
            {
                "1": "defined_empty",
                "2": "defined_nonempty",
                "3": "omitted",
                "fixed": "omitted",
                "poem": "omitted",
                "small": "omitted",
                "width": "omitted",
            },
        )
        self.assertEqual(
            manifest["reachable_construct_counts"],
            {"#expr": 0, "#if": 4, "#ifeq": 3, "#iferror": 0, "#tag": 1},
        )
        self.assertEqual(
            manifest["unreachable_construct_counts"],
            {"#expr": 2, "#if": 1, "#ifeq": 2, "#iferror": 1, "#tag": 0},
        )
        scope = manifest["capture_scope"]
        self.assertIs(scope["expr_reachable_for_frozen_frame"], False)
        self.assertIs(scope["iferror_reachable_for_frozen_frame"], False)
        self.assertIs(scope["tag_poem_operation_reachable"], True)
        self.assertIs(scope["extension_tag_expansion_reproduced"], False)
        self.assertIs(scope["resolved_part2_identity_frozen"], False)
        self.assertIs(manifest["source_text_included"], False)

    def test_each_branch_decision_is_deterministic_for_the_frozen_frame(self) -> None:
        manifest = build_poemx1_control_flow_manifest(
            transclusion_manifest=_transclusion_manifest(),
            parameter_manifest=_parameter_manifest(),
            binding_manifest=_binding_manifest(),
            research_date="2026-09-17",
        )
        selected = {
            item["decision"]: item["selected_branch"]
            for item in manifest["branch_decisions"]
        }
        self.assertEqual(
            selected,
            {
                "title_if": "false",
                "fixed_centering_ifeq": "unequal",
                "fixed_width_ifeq": "unequal",
                "width_if": "false",
                "poem_if": "false",
                "small_ifeq": "unequal",
                "signature_if": "false",
            },
        )

    def test_binding_shape_drift_fails_closed(self) -> None:
        bindings = _binding_manifest()
        bindings["invocations"][2]["effective_bindings"]["fixed"] = {
            "defined_empty": False
        }
        with self.assertRaisesRegex(
            ValueError, "unexpected effective poemx1 binding names"
        ):
            build_poemx1_control_flow_manifest(
                transclusion_manifest=_transclusion_manifest(),
                parameter_manifest=_parameter_manifest(),
                binding_manifest=bindings,
                research_date="2026-09-17",
            )

    def test_template_graph_drift_fails_closed(self) -> None:
        transclusion = _transclusion_manifest()
        transclusion["effective_dependency_graph"]["parser_function_counts"][
            "#expr"
        ] = 3
        with self.assertRaisesRegex(ValueError, "unexpected parser-function inventory"):
            build_poemx1_control_flow_manifest(
                transclusion_manifest=transclusion,
                parameter_manifest=_parameter_manifest(),
                binding_manifest=_binding_manifest(),
                research_date="2026-09-17",
            )


if __name__ == "__main__":
    unittest.main()
