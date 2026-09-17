"""Bounded source-free control-flow evidence for the pinned Klim Samgin ``poemx1`` frame.

This is deliberately not a generic MediaWiki parser. It validates the already-frozen
historical template/source manifests and the six concrete invocation bindings, then
resolves only the ``#if``/``#ifeq`` branch decisions that are determined by that exact
frame shape. Arithmetic/error parser functions are recorded as unreachable; the live
``#tag:poem`` call and recursive expansion of parameter 2 remain outside this profile.
"""
from __future__ import annotations

from typing import Mapping


PROFILE_VERSION = "scriptorium-mediawiki-poemx1-control-v1"
MANIFEST_VERSION = "scriptorium-poemx1-control-flow-v1"
MEDIAWIKI_PARSER_FUNCTIONS = (
    "https://www.mediawiki.org/wiki/Help:Extension:ParserFunctions"
)
MEDIAWIKI_MAGIC_WORDS = "https://www.mediawiki.org/wiki/Help:Magic_words"

_TEMPLATE_REVISION_ID = 5142743
_TEMPLATE_WIKITEXT_SHA256 = (
    "fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db"
)
_TRANSCLUSION_INPUT_SHA256 = (
    "86ad628a9d8fc3d904fd513a1b4335f4e9f816ceedfa2af736e8e3a94e32ffbf"
)
_EXPECTED_PARSER_COUNTS = {
    "#expr": 2,
    "#if": 5,
    "#ifeq": 5,
    "#iferror": 1,
    "#tag": 1,
}
_EXPECTED_EXTENSION_TARGETS = {"poem": 1}
_EXPECTED_PARAMETER_COUNTS = {
    "1": 2,
    "2": 1,
    "3": 2,
    "fixed": 6,
    "poem": 1,
    "small": 6,
    "width": 3,
}
_EXPECTED_FRAME_STATES = {
    "1": "defined_empty",
    "2": "defined_nonempty",
    "3": "omitted",
    "fixed": "omitted",
    "poem": "omitted",
    "small": "omitted",
    "width": "omitted",
}


def _require_mapping(value: object, *, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _validate_source_manifests(
    transclusion_manifest: Mapping[str, object],
    parameter_manifest: Mapping[str, object],
) -> None:
    if (
        transclusion_manifest.get("manifest_version")
        != "scriptorium-template-transclusion-shape-v1"
    ):
        raise ValueError("unexpected transclusion manifest version")
    source_revision = _require_mapping(
        transclusion_manifest.get("source_revision"),
        label="transclusion source_revision",
    )
    if source_revision.get("revision_id") != _TEMPLATE_REVISION_ID:
        raise ValueError("unexpected poemx1 template revision")
    if source_revision.get("wikitext_sha256") != _TEMPLATE_WIKITEXT_SHA256:
        raise ValueError("unexpected poemx1 template digest")

    graph = _require_mapping(
        transclusion_manifest.get("effective_dependency_graph"),
        label="effective_dependency_graph",
    )
    if graph.get("parser_function_counts") != _EXPECTED_PARSER_COUNTS:
        raise ValueError("unexpected parser-function inventory")
    if graph.get("extension_tag_targets") != _EXPECTED_EXTENSION_TARGETS:
        raise ValueError("unexpected extension-tag inventory")

    if (
        parameter_manifest.get("manifest_version")
        != "scriptorium-template-parameter-surface-v1"
    ):
        raise ValueError("unexpected parameter manifest version")
    if parameter_manifest.get("transclusion_input_sha256") != _TRANSCLUSION_INPUT_SHA256:
        raise ValueError("unexpected post-inclusion template digest")
    parameter_revision = _require_mapping(
        parameter_manifest.get("source_revision"), label="parameter source_revision"
    )
    if parameter_revision.get("revision_id") != _TEMPLATE_REVISION_ID:
        raise ValueError("parameter surface revision mismatch")
    if parameter_revision.get("wikitext_sha256") != _TEMPLATE_WIKITEXT_SHA256:
        raise ValueError("parameter surface digest mismatch")
    surface = _require_mapping(
        parameter_manifest.get("parameter_surface"), label="parameter_surface"
    )
    if surface.get("parameter_reference_counts") != _EXPECTED_PARAMETER_COUNTS:
        raise ValueError("unexpected parameter-reference inventory")


def _validate_bindings(binding_manifest: Mapping[str, object]) -> list[dict[str, object]]:
    if (
        binding_manifest.get("manifest_version")
        != "scriptorium-template-invocation-bindings-v1"
    ):
        raise ValueError("unexpected binding manifest version")
    if binding_manifest.get("expected_invocation_count") != 6:
        raise ValueError("expected exactly six poemx1 invocations")

    invocations = binding_manifest.get("invocations")
    if not isinstance(invocations, list) or len(invocations) != 6:
        raise ValueError("binding manifest must contain six invocations")

    identities: list[dict[str, object]] = []
    for expected_index, record_obj in enumerate(invocations, start=1):
        record = _require_mapping(record_obj, label=f"invocation {expected_index}")
        if record.get("invocation_index") != expected_index:
            raise ValueError("poemx1 invocation order drifted")
        if record.get("argument_count") != 2:
            raise ValueError("poemx1 invocation argument count drifted")
        if (
            record.get("anonymous_argument_count") != 2
            or record.get("named_argument_count") != 0
        ):
            raise ValueError("poemx1 invocation binding shape drifted")
        if record.get("duplicate_assignment_counts") != {}:
            raise ValueError("duplicate poemx1 assignment observed")

        effective = _require_mapping(
            record.get("effective_bindings"),
            label=f"invocation {expected_index} bindings",
        )
        if set(effective) != {"1", "2"}:
            raise ValueError("unexpected effective poemx1 binding names")
        first = _require_mapping(effective["1"], label="parameter 1")
        second = _require_mapping(effective["2"], label="parameter 2")
        if first.get("defined_empty") is not True:
            raise ValueError("parameter 1 must be explicitly defined empty")
        if second.get("defined_empty") is not False:
            raise ValueError("parameter 2 must be defined non-empty")
        invocation_sha256 = record.get("invocation_sha256")
        if not isinstance(invocation_sha256, str) or len(invocation_sha256) != 64:
            raise ValueError("invocation digest missing or malformed")
        identities.append(
            {
                "invocation_index": expected_index,
                "invocation_sha256": invocation_sha256,
            }
        )
    return identities


def _if_branch(state: str) -> bool:
    """Return the documented ``#if`` truth value for a source-free frame state."""
    if state == "defined_nonempty":
        return True
    if state in {"defined_empty", "omitted"}:
        return False
    raise ValueError(f"unsupported source-free #if state: {state!r}")


def _ifeq_literal(left: str, right: str) -> bool:
    """Compare the bounded non-numeric literal operands used by this poemx1 revision."""
    if not isinstance(left, str) or not isinstance(right, str):
        raise TypeError("#ifeq operands must be strings")
    # ParserFunctions trims leading/trailing whitespace from its arguments. Numeric
    # coercion is intentionally out of scope because the only reached operands here
    # are the non-numeric literals "+" and "-".
    left = left.strip()
    right = right.strip()
    if left not in {"+", "-"} or right not in {"+", "-"}:
        raise ValueError("operand outside bounded non-numeric poemx1 #ifeq profile")
    return left == right


def build_poemx1_control_flow_manifest(
    *,
    transclusion_manifest: Mapping[str, object],
    parameter_manifest: Mapping[str, object],
    binding_manifest: Mapping[str, object],
    research_date: str,
) -> dict[str, object]:
    """Resolve the reachable parser-control graph for the six frozen Klim invocations."""
    if not isinstance(research_date, str) or not research_date:
        raise ValueError("research_date must be non-empty")
    _validate_source_manifests(transclusion_manifest, parameter_manifest)
    invocation_identities = _validate_bindings(binding_manifest)

    # The six calls have one shared source-free frame class, validated above.
    frame = dict(_EXPECTED_FRAME_STATES)

    title_if = _if_branch(frame["1"])
    fixed_centering_ifeq = _ifeq_literal("+", "-")
    fixed_width_ifeq = _ifeq_literal("+", "-")
    width_if = _if_branch(frame["width"])
    poem_if = _if_branch(frame["poem"])
    small_ifeq = _ifeq_literal("+", "-")
    signature_if = _if_branch(frame["3"])

    if any(
        (
            title_if,
            fixed_centering_ifeq,
            fixed_width_ifeq,
            width_if,
            poem_if,
            small_ifeq,
            signature_if,
        )
    ):
        raise AssertionError("frozen poemx1 default/empty control profile unexpectedly changed")

    reached_counts = {
        "#expr": 0,
        "#if": 4,
        "#ifeq": 3,
        "#iferror": 0,
        "#tag": 1,
    }
    unreachable_counts = {
        name: _EXPECTED_PARSER_COUNTS[name] - reached_counts[name]
        for name in _EXPECTED_PARSER_COUNTS
    }

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": "gorky-klim-samgin-ru-poemx1-control-flow",
        "research_date": research_date,
        "control_profile": PROFILE_VERSION,
        "template_revision": {
            "revision_id": _TEMPLATE_REVISION_ID,
            "wikitext_sha256": _TEMPLATE_WIKITEXT_SHA256,
            "transclusion_input_sha256": _TRANSCLUSION_INPUT_SHA256,
        },
        "binding_manifest_version": binding_manifest["manifest_version"],
        "invocation_count": 6,
        "invocation_identities": invocation_identities,
        "shared_source_free_frame": frame,
        "static_construct_counts": dict(_EXPECTED_PARSER_COUNTS),
        "reachable_construct_counts": reached_counts,
        "unreachable_construct_counts": unreachable_counts,
        "branch_decisions": [
            {
                "decision": "title_if",
                "function": "#if",
                "selected_branch": "false",
                "effect": "title_block_omitted",
            },
            {
                "decision": "fixed_centering_ifeq",
                "function": "#ifeq",
                "selected_branch": "unequal",
                "effect": "automatic_centering_and_fit_content_path_selected",
            },
            {
                "decision": "fixed_width_ifeq",
                "function": "#ifeq",
                "selected_branch": "unequal",
                "effect": "conditional_width_path_selected",
            },
            {
                "decision": "width_if",
                "function": "#if",
                "selected_branch": "false",
                "effect": "width_arithmetic_path_omitted",
            },
            {
                "decision": "poem_if",
                "function": "#if",
                "selected_branch": "false",
                "effect": "alternate_poem_font_path_omitted",
            },
            {
                "decision": "small_ifeq",
                "function": "#ifeq",
                "selected_branch": "unequal",
                "effect": "small_font_path_omitted",
            },
            {
                "decision": "signature_if",
                "function": "#if",
                "selected_branch": "false",
                "effect": "signature_block_omitted",
            },
        ],
        "live_extension_operation": {
            "function": "#tag",
            "tag": "poem",
            "content_parameter": "2",
            "invocation_count": 1,
            "content_recursive_expansion_reproduced": False,
            "extension_rendering_reproduced": False,
        },
        "semantics_evidence": [
            {
                "url": MEDIAWIKI_PARSER_FUNCTIONS,
                "claim": (
                    "#if treats empty or whitespace-only input as false; ParserFunctions trims "
                    "leading/trailing whitespace; #ifeq compares non-numeric operands as "
                    "case-sensitive text"
                ),
            },
            {
                "url": MEDIAWIKI_MAGIC_WORDS,
                "claim": (
                    "#tag invokes XML-style parser/extension tags and avoids parsing tag calls "
                    "in conditional paths that are not executed"
                ),
            },
        ],
        "capture_scope": {
            "frozen_frame_validated": True,
            "reachable_if_branch_selection_resolved": True,
            "reachable_ifeq_branch_selection_resolved": True,
            "expr_reachable_for_frozen_frame": False,
            "iferror_reachable_for_frozen_frame": False,
            "expr_evaluation_reproduced": False,
            "iferror_evaluation_reproduced": False,
            "tag_poem_operation_reachable": True,
            "extension_tag_expansion_reproduced": False,
            "inserted_parameter_value_recursive_expansion_reproduced": False,
            "resolved_part2_identity_frozen": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This source-free artifact resolves only the documented #if/#ifeq branch "
            "choices for the exact six frozen poemx1 frames. It demonstrates that both "
            "#expr calls and the #iferror call are unreachable under those frames. The live "
            "#tag:poem operation, recursive expansion of parameter 2, extension rendering, "
            "resolved Part 2 bytes and historical render equivalence remain unresolved."
        ),
        "source_text_included": False,
    }
