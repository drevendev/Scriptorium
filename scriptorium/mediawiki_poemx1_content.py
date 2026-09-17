"""Source-free parameter-2 expansion-surface evidence for Klim Samgin ``poemx1``.

The six concrete ``poemx1`` invocations and their frame bindings are already frozen.
This module re-opens only the exact parameter-2 values in memory, cross-checks them
against the committed binding identities, and records whether the values contain
MediaWiki brace-expansion constructs or other render-sensitive markup.

The resulting manifest never persists literary prose.  In particular, proving that
the observed values contain no ``{{...}}`` / ``{{{...}}}`` constructs only closes the
template-expansion prerequisite for those exact values; it does not reproduce
``#tag:poem``, recursive wikitext rendering, or historical MediaWiki output.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import re
from typing import Mapping

from .mediawiki_template_invocation import (
    _split_top_level,
    parse_template_invocation,
)

PROFILE_VERSION = "scriptorium-mediawiki-poemx1-content-surface-v1"
MANIFEST_VERSION = "scriptorium-poemx1-content-surface-v1"
MEDIAWIKI_TEMPLATE_EXPANSION = (
    "https://www.mediawiki.org/wiki/Manual:Template_expansion_process"
)
MEDIAWIKI_POEM_EXTENSION = "https://www.mediawiki.org/wiki/Extension:Poem"

_DEPENDENCY_REVISION_ID = 2366546
_DEPENDENCY_WIKITEXT_SHA256 = (
    "173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996"
)
_TEMPLATE_NAME = "poemx1"
_EXPECTED_INVOCATION_COUNT = 6
_TAG_RE = re.compile(r"</?\s*([A-Za-z][A-Za-z0-9:_-]*)\b[^>]*>")
_EXTERNAL_LINK_RE = re.compile(r"(?<!\[)\[(?:https?://|//)", re.IGNORECASE)
_APOSTROPHE_MARKUP_RE = re.compile(r"'{2,}")


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _require_mapping(value: object, *, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _validate_binding_manifest(binding_manifest: Mapping[str, object]) -> list[Mapping[str, object]]:
    if (
        binding_manifest.get("manifest_version")
        != "scriptorium-template-invocation-bindings-v1"
    ):
        raise ValueError("unexpected binding manifest version")
    dependency = _require_mapping(
        binding_manifest.get("dependency_revision"), label="dependency_revision"
    )
    if dependency.get("revision_id") != _DEPENDENCY_REVISION_ID:
        raise ValueError("unexpected dependency revision")
    if dependency.get("wikitext_sha256") != _DEPENDENCY_WIKITEXT_SHA256:
        raise ValueError("unexpected dependency digest")

    invocations = binding_manifest.get("invocations")
    if not isinstance(invocations, list) or len(invocations) != _EXPECTED_INVOCATION_COUNT:
        raise ValueError("binding manifest must contain exactly six invocations")
    out: list[Mapping[str, object]] = []
    for expected_index, record_obj in enumerate(invocations, start=1):
        record = _require_mapping(record_obj, label=f"binding invocation {expected_index}")
        if record.get("invocation_index") != expected_index:
            raise ValueError("binding invocation order drifted")
        if (
            record.get("argument_count") != 2
            or record.get("anonymous_argument_count") != 2
            or record.get("named_argument_count") != 0
        ):
            raise ValueError("poemx1 binding shape drifted")
        effective = _require_mapping(
            record.get("effective_bindings"), label=f"invocation {expected_index} bindings"
        )
        if set(effective) != {"1", "2"}:
            raise ValueError("unexpected effective binding names")
        first = _require_mapping(effective["1"], label="parameter 1")
        second = _require_mapping(effective["2"], label="parameter 2")
        if first.get("defined_empty") is not True:
            raise ValueError("parameter 1 must remain explicitly empty")
        if second.get("defined_empty") is not False:
            raise ValueError("parameter 2 must remain defined non-empty")
        out.append(record)
    return out


def _brace_inventory(text: str) -> dict[str, int]:
    """Count balanced double/triple-brace constructs without exposing their contents."""
    stack: list[int] = []
    template_count = 0
    tplarg_count = 0
    cursor = 0
    while cursor < len(text):
        if text.startswith("{{{", cursor):
            stack.append(3)
            tplarg_count += 1
            cursor += 3
            continue
        if text.startswith("{{", cursor):
            stack.append(2)
            template_count += 1
            cursor += 2
            continue
        if text.startswith("}}}", cursor):
            if not stack or stack[-1] != 3:
                raise ValueError("unmatched triple-brace close in parameter 2")
            stack.pop()
            cursor += 3
            continue
        if text.startswith("}}", cursor):
            if not stack or stack[-1] != 2:
                raise ValueError("unmatched double-brace close in parameter 2")
            stack.pop()
            cursor += 2
            continue
        cursor += 1
    if stack:
        raise ValueError("unclosed brace construct in parameter 2")
    return {
        "template_or_parser_construct_count": template_count,
        "template_parameter_construct_count": tplarg_count,
        "brace_expansion_construct_count": template_count + tplarg_count,
    }


def _render_surface(text: str) -> dict[str, object]:
    braces = _brace_inventory(text)
    tags = Counter(match.group(1).casefold() for match in _TAG_RE.finditer(text))
    lines = text.split("\n")
    leading_colon_lines = sum(1 for line in lines if line.startswith(":"))
    leading_space_lines = sum(1 for line in lines if line.startswith(" "))
    blank_lines = sum(1 for line in lines if line == "")
    wikilink_count = text.count("[[")
    external_link_count = len(_EXTERNAL_LINK_RE.findall(text))
    apostrophe_markup_run_count = len(_APOSTROPHE_MARKUP_RE.findall(text))
    return {
        **braces,
        "xml_like_tag_count": sum(tags.values()),
        "xml_like_tag_name_counts": dict(sorted(tags.items())),
        "wikilink_open_count": wikilink_count,
        "external_link_open_count": external_link_count,
        "apostrophe_markup_run_count": apostrophe_markup_run_count,
        "newline_count": text.count("\n"),
        "line_count": len(lines),
        "blank_line_count": blank_lines,
        "leading_colon_line_count": leading_colon_lines,
        "leading_space_line_count": leading_space_lines,
        "template_expansion_identity_for_observed_value": (
            braces["brace_expansion_construct_count"] == 0
        ),
    }


def _parameter_two_value(
    dependency_wikitext: str,
    binding_record: Mapping[str, object],
) -> tuple[str, dict[str, object]]:
    start = binding_record.get("parent_start_offset")
    end = binding_record.get("parent_end_offset")
    if not isinstance(start, int) or not isinstance(end, int) or not (0 <= start < end):
        raise ValueError("invalid invocation offsets")
    raw_invocation = dependency_wikitext[start:end]
    if _sha256_text(raw_invocation) != binding_record.get("invocation_sha256"):
        raise ValueError("invocation digest drifted")

    parsed = parse_template_invocation(raw_invocation, template_name=_TEMPLATE_NAME)
    if (
        parsed["argument_count"] != 2
        or parsed["anonymous_argument_count"] != 2
        or parsed["named_argument_count"] != 0
    ):
        raise ValueError("live invocation no longer matches frozen two-anonymous-argument shape")

    inner = raw_invocation[2:-2]
    parts = _split_top_level(inner, "|")
    if len(parts) != 3 or parts[0].strip().casefold() != _TEMPLATE_NAME:
        raise ValueError("unable to recover bounded poemx1 parameter 2")
    first_value, second_value = parts[1], parts[2]

    effective = _require_mapping(
        binding_record.get("effective_bindings"), label="effective_bindings"
    )
    first = _require_mapping(effective["1"], label="parameter 1 identity")
    second = _require_mapping(effective["2"], label="parameter 2 identity")
    if (
        len(first_value) != first.get("character_count")
        or len(first_value.encode("utf-8")) != first.get("utf8_byte_count")
        or _sha256_text(first_value) != first.get("sha256")
    ):
        raise ValueError("parameter 1 identity drifted")
    if (
        len(second_value) != second.get("character_count")
        or len(second_value.encode("utf-8")) != second.get("utf8_byte_count")
        or _sha256_text(second_value) != second.get("sha256")
    ):
        raise ValueError("parameter 2 identity drifted")
    return second_value, {
        "character_count": len(second_value),
        "utf8_byte_count": len(second_value.encode("utf-8")),
        "sha256": _sha256_text(second_value),
    }


def build_poemx1_content_surface_manifest(
    *,
    dependency_wikitext: str,
    binding_manifest: Mapping[str, object],
    research_date: str,
) -> dict[str, object]:
    """Freeze source-free recursive-expansion/render surface for parameter 2."""
    if not isinstance(dependency_wikitext, str):
        raise TypeError("dependency_wikitext must be str")
    if _sha256_text(dependency_wikitext) != _DEPENDENCY_WIKITEXT_SHA256:
        raise ValueError("dependency wikitext does not match frozen revision identity")
    if not isinstance(binding_manifest, Mapping):
        raise TypeError("binding_manifest must be a mapping")
    if not isinstance(research_date, str) or not research_date:
        raise ValueError("research_date must be non-empty")

    bindings = _validate_binding_manifest(binding_manifest)
    records: list[dict[str, object]] = []
    aggregate: Counter[str] = Counter()
    all_template_identity = True

    for index, binding in enumerate(bindings, start=1):
        value, identity = _parameter_two_value(dependency_wikitext, binding)
        surface = _render_surface(value)
        all_template_identity = (
            all_template_identity
            and bool(surface["template_expansion_identity_for_observed_value"])
        )
        for key in (
            "template_or_parser_construct_count",
            "template_parameter_construct_count",
            "brace_expansion_construct_count",
            "xml_like_tag_count",
            "wikilink_open_count",
            "external_link_open_count",
            "apostrophe_markup_run_count",
            "newline_count",
            "line_count",
            "blank_line_count",
            "leading_colon_line_count",
            "leading_space_line_count",
        ):
            aggregate[key] += int(surface[key])
        records.append(
            {
                "invocation_index": index,
                "invocation_sha256": binding["invocation_sha256"],
                "parameter_2_identity": identity,
                "surface": surface,
            }
        )

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": "gorky-klim-samgin-ru-poemx1-parameter-2-content",
        "research_date": research_date,
        "profile": PROFILE_VERSION,
        "dependency_revision": {
            "revision_id": _DEPENDENCY_REVISION_ID,
            "wikitext_sha256": _DEPENDENCY_WIKITEXT_SHA256,
        },
        "binding_manifest_version": binding_manifest["manifest_version"],
        "invocation_count": len(records),
        "invocations": records,
        "aggregate_surface": dict(sorted(aggregate.items())),
        "observed_parameter_2_template_expansion_identity": all_template_identity,
        "requires_additional_template_dependency_resolution": not all_template_identity,
        "semantics_evidence": [
            {
                "url": MEDIAWIKI_TEMPLATE_EXPANSION,
                "claim": (
                    "template argument values may contain nested templates, parser functions, "
                    "variables, or template parameters and are recursively expanded when needed"
                ),
            },
            {
                "url": MEDIAWIKI_POEM_EXTENSION,
                "claim": (
                    "Poem preserves line structure and supports ordinary wikitext markup; "
                    "closing template expansion does not reproduce poem rendering"
                ),
            },
        ],
        "capture_scope": {
            "parameter_2_identities_revalidated": True,
            "parameter_2_brace_expansion_surface_frozen": True,
            "parameter_2_render_markup_surface_frozen": True,
            "parameter_2_template_expansion_identity_for_observed_values": all_template_identity,
            "poem_extension_rendering_reproduced": False,
            "resolved_part2_identity_frozen": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This source-free artifact revalidates the exact six parameter-2 values and "
            "freezes only their brace-expansion and render-markup surface. If the observed "
            "values contain no brace expansion constructs, that closes only the template-"
            "expansion prerequisite for those exact values. Wikilinks, apostrophe markup, "
            "line structure, XML-like tags and #tag:poem rendering remain part of the "
            "historical rendering boundary. No literary prose is persisted."
        ),
        "source_text_included": False,
    }
