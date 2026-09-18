"""Bounded MediaWiki/Poem render reconstruction for Klim Samgin ``poemx1``.

The retained Part 2 dependency contains six exact, source-frozen ``poemx1`` calls.
Earlier slices proved that their live template branch is a single ``#tag:poem`` call,
that it has one content argument and no attributes, and that the six inserted values
contain no nested template/tag/link/apostrophe markup.  This module closes the next
candidate-specific rendering prerequisite without pretending to implement MediaWiki.

It re-opens the six exact parameter-2 values only in memory, scans the additional
``Parser::internalParse`` surfaces that could change those values, and reproduces the
Poem transformations that are actually reached when every active-syntax count is zero.
Only source-free identities, counts and branch facts are emitted.  The upstream Poem
commit remains an inferred reconstruction anchor: this code does not prove the exact
Poem or MediaWiki-core revision deployed by Russian Wikisource in November 2024.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import re
from typing import Mapping

from .mediawiki_poemx1_content import (
    _parameter_two_value,
    _validate_binding_manifest,
)

PROFILE_VERSION = "scriptorium-mediawiki-poem-render-surface-v1"
MANIFEST_VERSION = "scriptorium-poem-render-surface-v1"

_DEPENDENCY_REVISION_ID = 2366546
_DEPENDENCY_WIKITEXT_SHA256 = (
    "173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996"
)
_EXPECTED_INVOCATION_COUNT = 6
_EXPECTED_CONTENT_MANIFEST = "scriptorium-poemx1-content-surface-v1"
_EXPECTED_TAG_MANIFEST = "scriptorium-poem-tag-surface-v1"
_EXPECTED_ANCHOR_MANIFEST = "scriptorium-poem-extension-source-anchor-v1"
_EXPECTED_ANCHOR_COMMIT = "03b3694613e23efa1254d8bbbb98121efaef2cb0"

MEDIAWIKI_PARSER_SOURCE = (
    "https://github.com/wikimedia/mediawiki/blob/"
    "7e904064193fa67ee1ef8e9aed0f631b42d2c26f/includes/Parser/Parser.php"
)
MEDIAWIKI_POEM_SOURCE = (
    "https://github.com/wikimedia/mediawiki-extensions-Poem/blob/"
    "03b3694613e23efa1254d8bbbb98121efaef2cb0/includes/Poem.php"
)

# Conservative triggers for the Parser::internalParse stages that are materially
# relevant to these tiny values.  We fail closed if one appears instead of claiming
# that a generic MediaWiki parser has been reproduced.
_HORIZONTAL_RULE_RE = re.compile(r"(?m)^----+")
_TABLE_START_RE = re.compile(r"(?m)^\{\|")
_HEADING_RE = re.compile(r"(?m)^={1,6}[^\n]*={1,6}[ \t]*$")
_APOSTROPHE_RE = re.compile(r"'{2,}")
_EXTERNAL_LINK_RE = re.compile(r"(?<!\[)\[(?:https?://|//)", re.IGNORECASE)
_PROTOCOL_RE = re.compile(r"(?i)\b(?:https?|ftp|mailto):")
_MAGIC_LINK_RE = re.compile(r"(?i)\b(?:ISBN(?:-1[03])?|RFC|PMID)\b")
_ENTITY_RE = re.compile(r"&(?:#[0-9]+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);")


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _require_mapping(value: object, *, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _core_sensitive_surface(text: str) -> dict[str, int]:
    """Inventory conservative MediaWiki-core constructs without exposing prose."""
    if not isinstance(text, str):
        raise TypeError("text must be str")
    return {
        "template_open_count": text.count("{{"),
        "template_parameter_open_count": text.count("{{{"),
        "html_angle_bracket_count": text.count("<") + text.count(">"),
        "table_start_line_count": len(_TABLE_START_RE.findall(text)),
        "horizontal_rule_line_count": len(_HORIZONTAL_RULE_RE.findall(text)),
        "behavior_switch_delimiter_count": text.count("__"),
        "heading_line_count": len(_HEADING_RE.findall(text)),
        "internal_link_open_count": text.count("[["),
        "apostrophe_markup_run_count": len(_APOSTROPHE_RE.findall(text)),
        "external_link_open_count": len(_EXTERNAL_LINK_RE.findall(text)),
        "raw_protocol_count": len(_PROTOCOL_RE.findall(text)),
        "magic_link_token_count": len(_MAGIC_LINK_RE.findall(text)),
        "language_converter_open_count": text.count("-{"),
        "entity_reference_count": len(_ENTITY_RE.findall(text)),
    }


def _active_construct_total(surface: Mapping[str, object]) -> int:
    return sum(int(value) for value in surface.values())


def _poem_branch_surface(text: str) -> dict[str, object]:
    """Return only the Poem branches reached before recursiveTagParse."""
    if not isinstance(text, str):
        raise TypeError("text must be str")
    lines = text.split("\n")
    leading_colons = sum(1 for line in lines if re.match(r"^:+.+", line))
    leading_spaces = sum(1 for line in lines if line.startswith(" "))
    horizontal_rules = sum(1 for line in lines if re.match(r"^----+", line))
    edge_whitespace = bool(text) and (text[0].isspace() or text[-1].isspace())
    return {
        "line_count": len(lines),
        "newline_count": text.count("\n"),
        "leading_colon_line_count": leading_colons,
        "leading_space_line_count": leading_spaces,
        "horizontal_rule_line_count": horizontal_rules,
        "edge_whitespace_present": edge_whitespace,
    }


def _render_plain_poem_fragment(text: str) -> str:
    """Reproduce the post-unstrip Poem fragment for the proven plain-value surface."""
    core = _core_sensitive_surface(text)
    branch = _poem_branch_surface(text)
    if _active_construct_total(core):
        active = sorted(name for name, value in core.items() if int(value))
        raise ValueError(f"MediaWiki-core active syntax remains in poem value: {active}")
    if branch["leading_colon_line_count"]:
        raise ValueError("poem indentation branch is outside the plain-value profile")
    if branch["leading_space_line_count"]:
        raise ValueError("poem leading-space branch is outside the plain-value profile")
    if branch["horizontal_rule_line_count"]:
        raise ValueError("poem horizontal-rule branch is outside the plain-value profile")
    if branch["edge_whitespace_present"]:
        raise ValueError("Poem trim would change an observed value")

    # The inferred upstream Poem anchor inserts a protected <br /> strip item for
    # each interior newline.  With no active core syntax, recursiveTagParse is an
    # identity for the literary characters; after MediaWiki unstrips the protected
    # item, the observable fragment is equivalent to the literal form below.
    transformed = text.replace("\n", "<br />\n")
    return '<div class="poem">\n' + transformed + "\n</div>"


def _validate_source_free_manifests(
    *,
    content_manifest: Mapping[str, object],
    tag_manifest: Mapping[str, object],
    poem_anchor_manifest: Mapping[str, object],
) -> list[Mapping[str, object]]:
    if content_manifest.get("manifest_version") != _EXPECTED_CONTENT_MANIFEST:
        raise ValueError("unexpected parameter-2 content manifest")
    dependency = _require_mapping(
        content_manifest.get("dependency_revision"), label="dependency_revision"
    )
    if dependency.get("revision_id") != _DEPENDENCY_REVISION_ID:
        raise ValueError("unexpected dependency revision")
    if dependency.get("wikitext_sha256") != _DEPENDENCY_WIKITEXT_SHA256:
        raise ValueError("unexpected dependency wikitext digest")
    content_rows = content_manifest.get("invocations")
    if not isinstance(content_rows, list) or len(content_rows) != _EXPECTED_INVOCATION_COUNT:
        raise ValueError("content manifest must contain six invocations")

    if tag_manifest.get("manifest_version") != _EXPECTED_TAG_MANIFEST:
        raise ValueError("unexpected #tag:poem surface manifest")
    tag_surface = _require_mapping(tag_manifest.get("tag_surface"), label="tag_surface")
    if tag_surface.get("top_level_argument_count") != 1:
        raise ValueError("reached #tag:poem call must have one content argument")
    if tag_surface.get("attribute_count") != 0 or tag_surface.get("attribute_names") != []:
        raise ValueError("bounded render profile requires zero #tag:poem attributes")
    concrete = tag_manifest.get("concrete_invocations")
    if not isinstance(concrete, list) or len(concrete) != _EXPECTED_INVOCATION_COUNT:
        raise ValueError("tag manifest must bind six concrete invocations")

    if poem_anchor_manifest.get("manifest_version") != _EXPECTED_ANCHOR_MANIFEST:
        raise ValueError("unexpected Poem source-anchor manifest")
    if poem_anchor_manifest.get("evidence_class") != "inferred_reconstruction_anchor":
        raise ValueError("Poem source anchor lost inferred-evidence classification")
    anchor = _require_mapping(poem_anchor_manifest.get("anchor"), label="anchor")
    if anchor.get("upstream_commit") != _EXPECTED_ANCHOR_COMMIT:
        raise ValueError("unexpected Poem upstream anchor commit")
    semantics = _require_mapping(
        poem_anchor_manifest.get("bounded_source_semantics"), label="bounded_source_semantics"
    )
    required_semantics = {
        "compact_parameter_controls_wrapper_newlines",
        "interior_newlines_become_breaks",
        "leading_colons_become_indented_spans",
        "leading_spaces_become_nbsp_entities",
        "line_break_strip_item_inserted",
        "recursive_tag_parse_applied",
        "output_wrapped_in_div",
        "poem_css_class_forced",
    }
    missing = sorted(name for name in required_semantics if semantics.get(name) is not True)
    if missing:
        raise ValueError(f"Poem source anchor lost required semantics: {missing}")

    return [
        _require_mapping(item, label=f"content invocation {index}")
        for index, item in enumerate(content_rows, start=1)
    ]


def build_poem_render_surface_manifest(
    *,
    dependency_wikitext: str,
    binding_manifest: Mapping[str, object],
    content_manifest: Mapping[str, object],
    tag_manifest: Mapping[str, object],
    poem_anchor_manifest: Mapping[str, object],
    research_date: str,
) -> dict[str, object]:
    """Freeze the executable plain-value recursive-parse/Poem reconstruction surface."""
    if not isinstance(dependency_wikitext, str):
        raise TypeError("dependency_wikitext must be str")
    if _sha256_text(dependency_wikitext) != _DEPENDENCY_WIKITEXT_SHA256:
        raise ValueError("dependency wikitext does not match frozen revision")
    if not isinstance(binding_manifest, Mapping):
        raise TypeError("binding_manifest must be a mapping")
    if not isinstance(content_manifest, Mapping):
        raise TypeError("content_manifest must be a mapping")
    if not isinstance(tag_manifest, Mapping):
        raise TypeError("tag_manifest must be a mapping")
    if not isinstance(poem_anchor_manifest, Mapping):
        raise TypeError("poem_anchor_manifest must be a mapping")
    if not isinstance(research_date, str) or not research_date:
        raise ValueError("research_date must be non-empty")

    bindings = _validate_binding_manifest(binding_manifest)
    content_rows = _validate_source_free_manifests(
        content_manifest=content_manifest,
        tag_manifest=tag_manifest,
        poem_anchor_manifest=poem_anchor_manifest,
    )

    records: list[dict[str, object]] = []
    aggregate: Counter[str] = Counter()
    for index, (binding, content_row) in enumerate(zip(bindings, content_rows), start=1):
        if content_row.get("invocation_index") != index:
            raise ValueError("content invocation order drifted")
        if content_row.get("invocation_sha256") != binding.get("invocation_sha256"):
            raise ValueError("binding/content invocation identity mismatch")
        value, identity = _parameter_two_value(dependency_wikitext, binding)
        expected_identity = _require_mapping(
            content_row.get("parameter_2_identity"), label="parameter_2_identity"
        )
        if identity != dict(expected_identity):
            raise ValueError("live parameter-2 identity disagrees with frozen content manifest")

        core = _core_sensitive_surface(value)
        branch = _poem_branch_surface(value)
        rendered = _render_plain_poem_fragment(value)
        rendered_bytes = rendered.encode("utf-8")
        active_total = _active_construct_total(core)
        if active_total != 0:
            raise AssertionError("plain render helper accepted active core syntax")

        aggregate["input_character_count"] += int(identity["character_count"])
        aggregate["input_utf8_byte_count"] += int(identity["utf8_byte_count"])
        aggregate["newline_count"] += int(branch["newline_count"])
        aggregate["inserted_break_count"] += int(branch["newline_count"])
        aggregate["core_active_construct_count"] += active_total
        aggregate["rendered_fragment_character_count"] += len(rendered)
        aggregate["rendered_fragment_utf8_byte_count"] += len(rendered_bytes)

        records.append(
            {
                "invocation_index": index,
                "invocation_sha256": binding["invocation_sha256"],
                "parameter_2_identity": identity,
                "core_sensitive_surface": core,
                "poem_branch_surface": branch,
                "reconstruction": {
                    "core_recursive_parse_identity_for_observed_value": True,
                    "inserted_break_count": int(branch["newline_count"]),
                    "attribute_count": 0,
                    "compact_attribute_present": False,
                    "wrapper_class": "poem",
                    "post_unstrip_fragment_character_count": len(rendered),
                    "post_unstrip_fragment_utf8_byte_count": len(rendered_bytes),
                    "post_unstrip_fragment_sha256": sha256(rendered_bytes).hexdigest(),
                },
            }
        )

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": "gorky-klim-samgin-ru-poem-render-surface",
        "research_date": research_date,
        "profile": PROFILE_VERSION,
        "evidence_class": "candidate_specific_inferred_reconstruction",
        "dependency_revision": {
            "revision_id": _DEPENDENCY_REVISION_ID,
            "wikitext_sha256": _DEPENDENCY_WIKITEXT_SHA256,
        },
        "poem_source_anchor_commit": _EXPECTED_ANCHOR_COMMIT,
        "invocation_count": len(records),
        "invocations": records,
        "aggregate": dict(sorted(aggregate.items())),
        "semantics_evidence": [
            {
                "url": MEDIAWIKI_POEM_SOURCE,
                "claim": (
                    "the inferred Poem anchor inserts protected line breaks, applies "
                    "indent/leading-space transforms, calls recursiveTagParse, and wraps "
                    "the result in a poem div"
                ),
            },
            {
                "url": MEDIAWIKI_PARSER_SOURCE,
                "claim": (
                    "official MediaWiki core source shows recursiveTagParse delegating to "
                    "internalParse and enumerates the parser stages conservatively screened "
                    "by this candidate-specific profile"
                ),
            },
        ],
        "capture_scope": {
            "six_parameter_2_identities_revalidated": True,
            "core_parser_sensitive_surface_frozen": True,
            "core_recursive_parse_identity_reproduced_for_observed_plain_values": True,
            "bounded_poem_transform_reproduced_against_inferred_anchor": True,
            "post_unstrip_fragment_identities_frozen": True,
            "generic_mediawiki_parser_implemented": False,
            "historical_wikisource_mediawiki_core_revision_proven": False,
            "historical_wikisource_poem_deployment_equivalence_proven": False,
            "resolved_part2_identity_frozen": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This source-free artifact reproduces only the MediaWiki-core identity path and "
            "Poem branches materially reached by the six exact plain parameter-2 values. "
            "It fails closed on parser-sensitive syntax rather than implementing generic "
            "MediaWiki. The Poem source commit is an inferred reconstruction anchor, and the "
            "MediaWiki-core source is semantic guidance rather than deployment identity; "
            "therefore historical Wikisource render equivalence remains unproven. No literary "
            "prose is persisted and no resolved Part 2 body is claimed here."
        ),
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }
