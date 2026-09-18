"""Candidate-specific target-only Part 2 expansion for Klim Samgin.

This module resolves only the exact source graph already frozen by SCRIP-CORPUS-020:
the pinned Part 2 parent contains one target-only ``#lst`` call, the pinned target
contains exactly six ``poemx1`` invocations, and the pinned ``poemx1`` revision has
a source-free control/render surface that is already reproduced for those six frames.

It is deliberately not a generic MediaWiki parser. The evaluator supports only the
literal template-parameter, ``#if``, ``#ifeq`` and zero-attribute ``#tag:poem``
operations reached by the frozen frames. Unreached ``#expr``/``#iferror`` and every
ordinary template/magic-word path fail closed if they become reachable. Literary
source text is transient input only; the output manifest stores counts, digests and
branch facts, never prose.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import re
from typing import Mapping, MutableMapping

from .mediawiki_poem_render_surface import _render_plain_poem_fragment
from .mediawiki_poemx1_content import _parameter_two_value
from .mediawiki_template_invocation import find_template_invocations
from .mediawiki_transclusion import preprocess_for_transclusion

MANIFEST_VERSION = "scriptorium-klim-samgin-part2-resolution-v1"
PROFILE_VERSION = "scriptorium-klim-samgin-bounded-template-expansion-v1"
EXPECTED_LST_CONTRACT = "scriptorium-klim-samgin-lst-contract-v2"
EXPECTED_TRANSCLUSION_MANIFEST = "scriptorium-template-transclusion-shape-v1"
EXPECTED_PARAMETER_MANIFEST = "scriptorium-template-parameter-surface-v1"
EXPECTED_BINDING_MANIFEST = "scriptorium-template-invocation-bindings-v1"
EXPECTED_CONTROL_MANIFEST = "scriptorium-poemx1-control-flow-v1"
EXPECTED_RENDER_MANIFEST = "scriptorium-poem-render-surface-v1"
EXPECTED_TEMPLATE_REVISION_ID = 5142743
EXPECTED_DEPENDENCY_REVISION_ID = 2366546
EXPECTED_INVOCATION_COUNT = 6
EXPECTED_REACHED_COUNTS = {"#expr": 0, "#if": 4, "#ifeq": 3, "#iferror": 0, "#tag": 1}

_FUNCTION_RE = re.compile(r"^\s*#(?P<name>[A-Za-z]+)\s*:(?P<head>.*)$", re.DOTALL)
_LITERAL_PARAMETER_RE = re.compile(r"[A-Za-z0-9_]+\Z")


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _identity(value: str) -> dict[str, object]:
    raw = value.encode("utf-8")
    return {
        "character_count": len(value),
        "utf8_byte_count": len(raw),
        "sha256": sha256(raw).hexdigest(),
    }


def _require_mapping(value: object, *, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _matching_brace_end(text: str, start: int) -> int:
    if text.startswith("{{{", start):
        stack = [3]
        cursor = start + 3
    elif text.startswith("{{", start):
        stack = [2]
        cursor = start + 2
    else:
        raise ValueError("braced group must start with {{ or {{{")
    while cursor < len(text):
        if text.startswith("{{{", cursor):
            stack.append(3)
            cursor += 3
            continue
        if text.startswith("{{", cursor):
            stack.append(2)
            cursor += 2
            continue
        if stack[-1] == 3 and text.startswith("}}}", cursor):
            stack.pop()
            cursor += 3
            if not stack:
                return cursor
            continue
        if stack[-1] == 2 and text.startswith("}}", cursor):
            stack.pop()
            cursor += 2
            if not stack:
                return cursor
            continue
        cursor += 1
    raise ValueError("unclosed MediaWiki brace construct")


def _split_top_level(text: str, delimiter: str = "|") -> list[str]:
    if len(delimiter) != 1:
        raise ValueError("delimiter must be one character")
    out: list[str] = []
    cursor = 0
    start = 0
    brace_stack: list[int] = []
    link_depth = 0
    while cursor < len(text):
        if text.startswith("{{{", cursor):
            brace_stack.append(3)
            cursor += 3
            continue
        if text.startswith("{{", cursor):
            brace_stack.append(2)
            cursor += 2
            continue
        if brace_stack and brace_stack[-1] == 3 and text.startswith("}}}", cursor):
            brace_stack.pop()
            cursor += 3
            continue
        if brace_stack and brace_stack[-1] == 2 and text.startswith("}}", cursor):
            brace_stack.pop()
            cursor += 2
            continue
        if not brace_stack and text.startswith("[[", cursor):
            link_depth += 1
            cursor += 2
            continue
        if not brace_stack and link_depth and text.startswith("]]", cursor):
            link_depth -= 1
            cursor += 2
            continue
        if text[cursor] == delimiter and not brace_stack and link_depth == 0:
            out.append(text[start:cursor])
            start = cursor + 1
        cursor += 1
    if brace_stack or link_depth:
        raise ValueError("unbalanced nested construct while splitting MediaWiki expression")
    out.append(text[start:])
    return out


def _split_parameter(inner: str) -> tuple[str, str | None]:
    parts = _split_top_level(inner)
    if len(parts) == 1:
        return parts[0], None
    return parts[0], "|".join(parts[1:])


def _expand_bounded(
    text: str,
    *,
    frame: Mapping[str, str],
    trace: MutableMapping[str, int],
    rendered_poem_digests: list[str],
) -> str:
    """Expand the exact reached poemx1 subset with lazy parser-function branches."""
    out: list[str] = []
    cursor = 0
    while cursor < len(text):
        start = text.find("{{", cursor)
        if start < 0:
            out.append(text[cursor:])
            break
        out.append(text[cursor:start])
        triple = text.startswith("{{{", start)
        end = _matching_brace_end(text, start)
        raw = text[start:end]
        if triple:
            inner = raw[3:-3]
            raw_name, default = _split_parameter(inner)
            name = raw_name.strip()
            if not _LITERAL_PARAMETER_RE.fullmatch(name):
                raise ValueError("dynamic template parameter name outside bounded profile")
            if name in frame:
                replacement = frame[name]
            elif default is not None:
                replacement = _expand_bounded(
                    default,
                    frame=frame,
                    trace=trace,
                    rendered_poem_digests=rendered_poem_digests,
                )
            else:
                raise ValueError(f"undefined bare parameter {name!r} reached")
            if "{{" in replacement or "}}" in replacement:
                raise ValueError("inserted parameter value acquired brace syntax")
            out.append(replacement)
            cursor = end
            continue

        inner = raw[2:-2]
        parts = _split_top_level(inner)
        function = _FUNCTION_RE.match(parts[0])
        if function is None:
            raise ValueError("ordinary template or magic word reached bounded poemx1 evaluator")
        name = function.group("name").casefold()
        head_arg = function.group("head")

        if name == "if":
            trace["#if"] += 1
            if len(parts) not in {2, 3}:
                raise ValueError("bounded #if requires then and optional else branches")
            condition = _expand_bounded(
                head_arg, frame=frame, trace=trace, rendered_poem_digests=rendered_poem_digests
            ).strip()
            selected = parts[1] if condition else (parts[2] if len(parts) == 3 else "")
            replacement = _expand_bounded(
                selected, frame=frame, trace=trace, rendered_poem_digests=rendered_poem_digests
            )
        elif name == "ifeq":
            trace["#ifeq"] += 1
            if len(parts) not in {3, 4}:
                raise ValueError("bounded #ifeq requires right/equal and optional unequal branches")
            left = _expand_bounded(
                head_arg, frame=frame, trace=trace, rendered_poem_digests=rendered_poem_digests
            ).strip()
            right = _expand_bounded(
                parts[1], frame=frame, trace=trace, rendered_poem_digests=rendered_poem_digests
            ).strip()
            if left not in {"+", "-"} or right not in {"+", "-"}:
                raise ValueError("reached #ifeq operands left bounded +/- literal profile")
            selected = parts[2] if left == right else (parts[3] if len(parts) == 4 else "")
            replacement = _expand_bounded(
                selected, frame=frame, trace=trace, rendered_poem_digests=rendered_poem_digests
            )
        elif name == "tag":
            trace["#tag"] += 1
            target = _expand_bounded(
                head_arg, frame=frame, trace=trace, rendered_poem_digests=rendered_poem_digests
            ).strip().casefold()
            if target != "poem":
                raise ValueError(f"unexpected reached extension tag {target!r}")
            if len(parts) != 2:
                raise ValueError("bounded #tag:poem profile requires one content argument and zero attributes")
            content = _expand_bounded(
                parts[1], frame=frame, trace=trace, rendered_poem_digests=rendered_poem_digests
            )
            replacement = _render_plain_poem_fragment(content)
            rendered_poem_digests.append(_sha256_text(replacement))
        elif name in {"expr", "iferror"}:
            trace[f"#{name}"] += 1
            raise ValueError(f"unreachable #{name} became reachable")
        else:
            raise ValueError(f"unsupported parser function #{name} became reachable")

        out.append(replacement)
        cursor = end
    return "".join(out)


def expand_poemx1_for_frozen_frame(
    transclusion_input: str, *, parameter_2_value: str
) -> tuple[str, dict[str, object]]:
    if not isinstance(transclusion_input, str) or not isinstance(parameter_2_value, str):
        raise TypeError("transclusion input and parameter 2 value must be strings")
    trace: Counter[str] = Counter({name: 0 for name in EXPECTED_REACHED_COUNTS})
    rendered: list[str] = []
    expanded = _expand_bounded(
        transclusion_input,
        frame={"1": "", "2": parameter_2_value},
        trace=trace,
        rendered_poem_digests=rendered,
    )
    observed = {name: int(trace[name]) for name in EXPECTED_REACHED_COUNTS}
    if observed != EXPECTED_REACHED_COUNTS:
        raise ValueError(f"poemx1 reached-control drift: {observed!r}")
    if len(rendered) != 1:
        raise ValueError("bounded poemx1 expansion must render exactly one poem fragment")
    if "{{" in expanded or "}}" in expanded:
        raise ValueError("poemx1 expansion left unresolved brace constructs")
    return expanded, {
        "reachable_construct_counts": observed,
        "rendered_poem_fragment_sha256": rendered[0],
    }


def _validate_manifests(
    *,
    lst_contract: Mapping[str, object],
    transclusion_manifest: Mapping[str, object],
    parameter_manifest: Mapping[str, object],
    binding_manifest: Mapping[str, object],
    control_manifest: Mapping[str, object],
    render_manifest: Mapping[str, object],
) -> tuple[list[Mapping[str, object]], list[Mapping[str, object]]]:
    if lst_contract.get("contract_version") != EXPECTED_LST_CONTRACT:
        raise ValueError("unexpected target-only #lst contract")
    dependency = _require_mapping(lst_contract.get("dependency_revision"), label="lst dependency")
    if dependency.get("revision_id") != EXPECTED_DEPENDENCY_REVISION_ID:
        raise ValueError("unexpected Part 2 dependency revision")
    invocation = _require_mapping(lst_contract.get("invocation"), label="lst invocation")
    if invocation.get("argument_count") != 1 or invocation.get("section_label") is not None:
        raise ValueError("Part 2 #lst call is no longer target-only")

    if transclusion_manifest.get("manifest_version") != EXPECTED_TRANSCLUSION_MANIFEST:
        raise ValueError("unexpected poemx1 transclusion manifest")
    source_revision = _require_mapping(
        transclusion_manifest.get("source_revision"), label="template source revision"
    )
    if source_revision.get("revision_id") != EXPECTED_TEMPLATE_REVISION_ID:
        raise ValueError("unexpected poemx1 template revision")
    graph = _require_mapping(
        transclusion_manifest.get("effective_dependency_graph"), label="dependency graph"
    )
    if graph.get("ordinary_template_counts") != {} or graph.get("magic_word_counts") != {}:
        raise ValueError("poemx1 acquired ordinary-template or magic-word dependencies")

    if parameter_manifest.get("manifest_version") != EXPECTED_PARAMETER_MANIFEST:
        raise ValueError("unexpected poemx1 parameter manifest")
    if binding_manifest.get("manifest_version") != EXPECTED_BINDING_MANIFEST:
        raise ValueError("unexpected poemx1 binding manifest")
    if control_manifest.get("manifest_version") != EXPECTED_CONTROL_MANIFEST:
        raise ValueError("unexpected poemx1 control manifest")
    if control_manifest.get("reachable_construct_counts") != EXPECTED_REACHED_COUNTS:
        raise ValueError("poemx1 control reachability drift")
    if render_manifest.get("manifest_version") != EXPECTED_RENDER_MANIFEST:
        raise ValueError("unexpected poem render manifest")

    bindings_obj = binding_manifest.get("invocations")
    renders_obj = render_manifest.get("invocations")
    if (
        not isinstance(bindings_obj, list)
        or not isinstance(renders_obj, list)
        or len(bindings_obj) != EXPECTED_INVOCATION_COUNT
        or len(renders_obj) != EXPECTED_INVOCATION_COUNT
    ):
        raise ValueError("expected six frozen binding/render rows")
    bindings = [
        _require_mapping(row, label=f"binding {index}")
        for index, row in enumerate(bindings_obj, start=1)
    ]
    renders = [
        _require_mapping(row, label=f"render {index}")
        for index, row in enumerate(renders_obj, start=1)
    ]
    return bindings, renders


def build_part2_resolution_manifest(
    *,
    parent_wikitext: str,
    dependency_wikitext: str,
    template_wikitext: str,
    lst_contract: Mapping[str, object],
    transclusion_manifest: Mapping[str, object],
    parameter_manifest: Mapping[str, object],
    binding_manifest: Mapping[str, object],
    control_manifest: Mapping[str, object],
    render_manifest: Mapping[str, object],
    research_date: str,
) -> dict[str, object]:
    """Resolve the target-only Part 2 source graph without persisting literary prose."""
    if not all(isinstance(value, str) for value in (parent_wikitext, dependency_wikitext, template_wikitext)):
        raise TypeError("source wikitext inputs must be strings")
    if not isinstance(research_date, str) or not research_date:
        raise ValueError("research_date must be non-empty")

    bindings, renders = _validate_manifests(
        lst_contract=lst_contract,
        transclusion_manifest=transclusion_manifest,
        parameter_manifest=parameter_manifest,
        binding_manifest=binding_manifest,
        control_manifest=control_manifest,
        render_manifest=render_manifest,
    )

    parent_revision = _require_mapping(lst_contract.get("parent_revision"), label="parent revision")
    dependency_revision = _require_mapping(
        lst_contract.get("dependency_revision"), label="dependency revision"
    )
    if _sha256_text(parent_wikitext) != parent_revision.get("wikitext_sha256"):
        raise ValueError("parent Part 2 wikitext digest drift")
    if _sha256_text(dependency_wikitext) != dependency_revision.get("wikitext_sha256"):
        raise ValueError("target dependency wikitext digest drift")

    template_revision = _require_mapping(
        transclusion_manifest.get("source_revision"), label="template source revision"
    )
    if _sha256_text(template_wikitext) != template_revision.get("wikitext_sha256"):
        raise ValueError("poemx1 template wikitext digest drift")
    transclusion_input, control_counts = preprocess_for_transclusion(template_wikitext)
    if _sha256_text(transclusion_input) != parameter_manifest.get("transclusion_input_sha256"):
        raise ValueError("poemx1 post-inclusion source digest drift")

    observed_invocations = find_template_invocations(dependency_wikitext, template_name="poemx1")
    if len(observed_invocations) != EXPECTED_INVOCATION_COUNT:
        raise ValueError("dependency no longer contains exactly six poemx1 calls")

    replacements: list[tuple[int, int, str]] = []
    expansion_rows: list[dict[str, object]] = []
    for index, (observed, binding, render_row) in enumerate(
        zip(observed_invocations, bindings, renders), start=1
    ):
        if observed.get("invocation_index") != index or binding.get("invocation_index") != index:
            raise ValueError("poemx1 invocation order drift")
        if observed.get("invocation_sha256") != binding.get("invocation_sha256"):
            raise ValueError("live poemx1 invocation disagrees with frozen binding")
        value, value_identity = _parameter_two_value(dependency_wikitext, binding)
        expected_value = _require_mapping(
            render_row.get("parameter_2_identity"), label=f"render parameter 2 row {index}"
        )
        if value_identity != dict(expected_value):
            raise ValueError("parameter-2 identity drift before full template expansion")

        expanded, trace = expand_poemx1_for_frozen_frame(
            transclusion_input, parameter_2_value=value
        )
        reconstruction = _require_mapping(
            render_row.get("reconstruction"), label=f"render reconstruction {index}"
        )
        if trace["rendered_poem_fragment_sha256"] != reconstruction.get(
            "post_unstrip_fragment_sha256"
        ):
            raise ValueError("full template expansion disagrees with frozen Poem fragment")
        start = observed.get("parent_start_offset")
        end = observed.get("parent_end_offset")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("poemx1 invocation offsets missing")
        replacements.append((start, end, expanded))
        expansion_rows.append(
            {
                "invocation_index": index,
                "invocation_sha256": observed["invocation_sha256"],
                "parameter_2_sha256": value_identity["sha256"],
                "expanded_template_output": _identity(expanded),
                "reachable_construct_counts": trace["reachable_construct_counts"],
                "rendered_poem_fragment_sha256": trace["rendered_poem_fragment_sha256"],
            }
        )

    expanded_dependency = dependency_wikitext
    for start, end, replacement in reversed(replacements):
        expanded_dependency = expanded_dependency[:start] + replacement + expanded_dependency[end:]
    if find_template_invocations(expanded_dependency, template_name="poemx1"):
        raise ValueError("resolved dependency still contains poemx1 invocations")
    if "{{" in expanded_dependency or "}}" in expanded_dependency:
        raise ValueError("resolved dependency still contains brace expansion syntax")

    lst_invocation = _require_mapping(lst_contract.get("invocation"), label="lst invocation")
    lst_start = lst_invocation.get("parent_start_offset")
    lst_end = lst_invocation.get("parent_end_offset")
    if not isinstance(lst_start, int) or not isinstance(lst_end, int):
        raise ValueError("frozen #lst offsets missing")
    raw_lst = parent_wikitext[lst_start:lst_end]
    if _sha256_text(raw_lst) != lst_invocation.get("invocation_sha256"):
        raise ValueError("frozen #lst parent placement drift")
    resolved_parent = parent_wikitext[:lst_start] + expanded_dependency + parent_wikitext[lst_end:]

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": "gorky-klim-samgin-ru-part-2",
        "research_date": research_date,
        "profile": PROFILE_VERSION,
        "evidence_class": "candidate_specific_inferred_reconstruction",
        "source_revisions": {
            "parent_revision_id": parent_revision["revision_id"],
            "parent_wikitext_sha256": parent_revision["wikitext_sha256"],
            "dependency_revision_id": dependency_revision["revision_id"],
            "dependency_wikitext_sha256": dependency_revision["wikitext_sha256"],
            "poemx1_template_revision_id": template_revision["revision_id"],
            "poemx1_template_wikitext_sha256": template_revision["wikitext_sha256"],
        },
        "transclusion_control_counts": control_counts,
        "lst_invocation": {
            "parent_start_offset": lst_start,
            "parent_end_offset": lst_end,
            "invocation_sha256": lst_invocation["invocation_sha256"],
            "target_title": lst_invocation["target_title"],
            "section_label": None,
        },
        "poemx1_expansions": expansion_rows,
        "expanded_dependency_identity": _identity(expanded_dependency),
        "resolved_parent_part2_identity": _identity(resolved_parent),
        "remaining_expansion_surface": {
            "poemx1_invocation_count": 0,
            "double_brace_open_count": expanded_dependency.count("{{"),
            "double_brace_close_count": expanded_dependency.count("}}"),
        },
        "capture_scope": {
            "target_only_lst_full_target_substitution_reproduced": True,
            "six_poemx1_full_template_expansions_reproduced": True,
            "resolved_part2_wikitext_identity_frozen": True,
            "candidate_specific_literary_body_extraction_frozen": False,
            "four_part_literary_body_composite_frozen": False,
            "historical_wikisource_mediawiki_core_revision_proven": False,
            "historical_wikisource_poem_deployment_equivalence_proven": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This source-free artifact resolves the exact target-only Part 2 #lst substitution "
            "under the already-frozen candidate-specific poemx1 control and inferred Poem render "
            "profile. It is not proof of the historical Russian Wikisource MediaWiki/Poem "
            "deployment. Literary-body extraction and four-part composition remain separate "
            "fail-closed prerequisites, and no source prose is persisted."
        ),
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "gate_ready": False,
        "m2_parity_admissible": False,
    }


def validate_part2_resolution_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Klim Samgin Part 2 resolution manifest")
    if manifest.get("candidate_id") != "gorky-klim-samgin-ru-part-2":
        raise ValueError("unexpected Part 2 resolution candidate")
    if manifest.get("profile") != PROFILE_VERSION:
        raise ValueError("unexpected Part 2 resolution profile")
    if manifest.get("evidence_class") != "candidate_specific_inferred_reconstruction":
        raise ValueError("Part 2 resolution evidence class drift")
    rows = manifest.get("poemx1_expansions")
    if not isinstance(rows, list) or len(rows) != EXPECTED_INVOCATION_COUNT:
        raise ValueError("Part 2 resolution must contain six source-free expansion rows")
    for index, row_obj in enumerate(rows, start=1):
        row = _require_mapping(row_obj, label=f"expansion row {index}")
        if row.get("invocation_index") != index:
            raise ValueError("Part 2 expansion order drift")
        identity = _require_mapping(
            row.get("expanded_template_output"), label=f"expanded output {index}"
        )
        for key in ("character_count", "utf8_byte_count"):
            if not isinstance(identity.get(key), int) or int(identity[key]) <= 0:
                raise ValueError(f"invalid expanded-template {key}")
        digest = identity.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError("invalid expanded-template digest")
        if row.get("reachable_construct_counts") != EXPECTED_REACHED_COUNTS:
            raise ValueError("Part 2 expansion reached-control counts drift")

    for name in ("expanded_dependency_identity", "resolved_parent_part2_identity"):
        identity = _require_mapping(manifest.get(name), label=name)
        for key in ("character_count", "utf8_byte_count"):
            if not isinstance(identity.get(key), int) or int(identity[key]) <= 0:
                raise ValueError(f"invalid {name} {key}")
        digest = identity.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError(f"invalid {name} digest")

    remaining = _require_mapping(
        manifest.get("remaining_expansion_surface"), label="remaining expansion surface"
    )
    if remaining != {
        "poemx1_invocation_count": 0,
        "double_brace_open_count": 0,
        "double_brace_close_count": 0,
    }:
        raise ValueError("resolved dependency retains unsupported expansion syntax")
    scope = _require_mapping(manifest.get("capture_scope"), label="capture scope")
    if scope.get("resolved_part2_wikitext_identity_frozen") is not True:
        raise ValueError("resolved Part 2 identity must be frozen")
    if scope.get("candidate_specific_literary_body_extraction_frozen") is not False:
        raise ValueError("literary extraction must remain unresolved")
    if scope.get("four_part_literary_body_composite_frozen") is not False:
        raise ValueError("four-part literary composite must remain unresolved")
    if scope.get("historical_render_equivalence_proven") is not False:
        raise ValueError("historical render equivalence must remain unproven")
    if scope.get("source_text_committed") is not False or manifest.get("source_text_included") is not False:
        raise ValueError("source prose must not be persisted")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source identity must remain unknown")
    if manifest.get("diagnostic_ready") is not False or manifest.get("gate_ready") is not False:
        raise ValueError("Part 2 resolution alone cannot open diagnostics/gate")
    if manifest.get("m2_parity_admissible") is not False:
        raise ValueError("Part 2 resolution alone cannot advance M2")

    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(manifest):
        raise ValueError("source prose key leaked into Part 2 resolution manifest")
