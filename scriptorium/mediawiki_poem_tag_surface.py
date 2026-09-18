"""Source-free ``#tag:poem`` argument/attribute evidence for Klim Samgin.

This module deliberately stops at the concrete top-level extension-tag call reached by
the already-frozen ``poemx1`` control flow.  It identifies the content argument and
literal attribute names/value-expression identities without evaluating nested parser
functions or reproducing Poem/MediaWiki rendering.  Literary prose is represented only
by the already-frozen parameter-2 digests.
"""
from __future__ import annotations

from hashlib import sha256
import re
from typing import Mapping

from .mediawiki_template_frame import parameter_reference_inventory
from .mediawiki_template_invocation import (
    _matching_brace_end,
    _split_top_level,
    _top_level_equals,
)
from .mediawiki_transclusion import (
    classify_effective_dependencies,
    preprocess_for_transclusion,
)

PROFILE_VERSION = "scriptorium-mediawiki-poem-tag-surface-v1"
MANIFEST_VERSION = "scriptorium-poem-tag-surface-v1"
MEDIAWIKI_MAGIC_WORDS = "https://www.mediawiki.org/wiki/Help:Magic_words"
MEDIAWIKI_TEMPLATE_EXPANSION = (
    "https://www.mediawiki.org/wiki/Manual:Template_expansion_process"
)

_TEMPLATE_REVISION_ID = 5142743
_TEMPLATE_WIKITEXT_SHA256 = (
    "fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db"
)
_TRANSCLUSION_INPUT_SHA256 = (
    "86ad628a9d8fc3d904fd513a1b4335f4e9f816ceedfa2af736e8e3a94e32ffbf"
)
_TAG_PREFIX_RE = re.compile(r"\{\{\s*#tag\s*:\s*poem(?=\s*[|}])", re.IGNORECASE)
_ATTRIBUTE_NAME_RE = re.compile(r"[A-Za-z_:][A-Za-z0-9_.:-]*\Z")


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _fragment_identity(value: str) -> dict[str, object]:
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


def extract_poem_tag_surface(transclusion_input: str) -> dict[str, object]:
    """Return a source-free structural surface for the single live ``#tag:poem`` call."""
    if not isinstance(transclusion_input, str):
        raise TypeError("transclusion_input must be str")
    matches = list(_TAG_PREFIX_RE.finditer(transclusion_input))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one #tag:poem call, observed {len(matches)}")

    start = matches[0].start()
    end = _matching_brace_end(transclusion_input, start)
    raw_call = transclusion_input[start:end]
    inner = raw_call[2:-2]
    parts = _split_top_level(inner, "|")
    if not parts or parts[0].strip().casefold() != "#tag:poem":
        raise ValueError("unexpected extension-tag target")
    if len(parts) < 2:
        raise ValueError("#tag:poem call has no content argument")

    content = parts[1]
    content_parameters = parameter_reference_inventory(content)
    attributes: list[dict[str, object]] = []
    names: list[str] = []
    for ordinal, segment in enumerate(parts[2:], start=1):
        equals = _top_level_equals(segment)
        if equals is None:
            raise ValueError("bounded #tag:poem profile requires named attributes")
        raw_name = segment[:equals].strip()
        if not raw_name or not _ATTRIBUTE_NAME_RE.fullmatch(raw_name):
            raise ValueError(f"unsupported #tag:poem attribute name: {raw_name!r}")
        name = raw_name.casefold()
        if name in names:
            raise ValueError(f"duplicate #tag:poem attribute: {name}")
        names.append(name)
        value = segment[equals + 1 :]
        attributes.append(
            {
                "attribute_ordinal": ordinal,
                "name": name,
                "value_expression_identity": _fragment_identity(value),
                "parameter_references": parameter_reference_inventory(value),
                "dependency_graph": classify_effective_dependencies(value),
            }
        )

    return {
        "call_identity": _fragment_identity(raw_call),
        "top_level_argument_count": len(parts) - 1,
        "content_argument": {
            "ordinal": 1,
            "expression_identity": _fragment_identity(content),
            "parameter_references": content_parameters,
            "dependency_graph": classify_effective_dependencies(content),
        },
        "attribute_count": len(attributes),
        "attribute_names": names,
        "attributes": attributes,
    }


def _validate_control_manifest(control_manifest: Mapping[str, object]) -> list[dict[str, object]]:
    if control_manifest.get("manifest_version") != "scriptorium-poemx1-control-flow-v1":
        raise ValueError("unexpected control manifest version")
    revision = _require_mapping(control_manifest.get("template_revision"), label="template_revision")
    if revision.get("revision_id") != _TEMPLATE_REVISION_ID:
        raise ValueError("control manifest template revision drifted")
    if revision.get("wikitext_sha256") != _TEMPLATE_WIKITEXT_SHA256:
        raise ValueError("control manifest template digest drifted")
    if revision.get("transclusion_input_sha256") != _TRANSCLUSION_INPUT_SHA256:
        raise ValueError("control manifest transclusion digest drifted")
    live = _require_mapping(control_manifest.get("live_extension_operation"), label="live_extension_operation")
    if live.get("function") != "#tag" or live.get("tag") != "poem":
        raise ValueError("control manifest does not reach #tag:poem")
    if live.get("content_parameter") != "2" or live.get("invocation_count") != 1:
        raise ValueError("unexpected live #tag:poem control surface")
    if control_manifest.get("invocation_count") != 6:
        raise ValueError("expected six frozen poemx1 frames")
    identities = control_manifest.get("invocation_identities")
    if not isinstance(identities, list) or len(identities) != 6:
        raise ValueError("missing six control invocation identities")
    return [dict(_require_mapping(item, label="control invocation")) for item in identities]


def _validate_content_manifest(content_manifest: Mapping[str, object]) -> list[dict[str, object]]:
    if content_manifest.get("manifest_version") != "scriptorium-poemx1-content-surface-v1":
        raise ValueError("unexpected content manifest version")
    dependency = _require_mapping(content_manifest.get("dependency_revision"), label="dependency_revision")
    if dependency.get("revision_id") != 2366546:
        raise ValueError("unexpected Part 2 dependency revision")
    invocations = content_manifest.get("invocations")
    if not isinstance(invocations, list) or len(invocations) != 6:
        raise ValueError("content manifest must contain six invocations")
    out: list[dict[str, object]] = []
    for expected_index, item in enumerate(invocations, start=1):
        record = _require_mapping(item, label=f"content invocation {expected_index}")
        if record.get("invocation_index") != expected_index:
            raise ValueError("content invocation order drifted")
        identity = _require_mapping(record.get("parameter_2_identity"), label="parameter_2_identity")
        digest = identity.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError("parameter-2 digest missing or malformed")
        out.append(
            {
                "invocation_index": expected_index,
                "invocation_sha256": record.get("invocation_sha256"),
                "parameter_2_identity": dict(identity),
            }
        )
    return out


def build_poem_tag_surface_manifest(
    *,
    revision_identity: Mapping[str, object],
    template_wikitext: str,
    control_manifest: Mapping[str, object],
    content_manifest: Mapping[str, object],
    research_date: str,
) -> dict[str, object]:
    """Freeze the reached top-level ``#tag:poem`` source surface for six frozen calls."""
    if not isinstance(revision_identity, Mapping):
        raise TypeError("revision_identity must be a mapping")
    if revision_identity.get("revision_id") != _TEMPLATE_REVISION_ID:
        raise ValueError("unexpected poemx1 template revision")
    if revision_identity.get("wikitext_sha256") != _TEMPLATE_WIKITEXT_SHA256:
        raise ValueError("unexpected poemx1 template digest")
    if not isinstance(template_wikitext, str):
        raise TypeError("template_wikitext must be str")
    if _sha256_text(template_wikitext) != _TEMPLATE_WIKITEXT_SHA256:
        raise ValueError("template source bytes do not match frozen revision")
    if not isinstance(research_date, str) or not research_date:
        raise ValueError("research_date must be non-empty")

    control_identities = _validate_control_manifest(control_manifest)
    concrete_content = _validate_content_manifest(content_manifest)
    if [row["invocation_sha256"] for row in control_identities] != [
        row["invocation_sha256"] for row in concrete_content
    ]:
        raise ValueError("control/content invocation identities disagree")

    transclusion_input, _ = preprocess_for_transclusion(template_wikitext)
    if _sha256_text(transclusion_input) != _TRANSCLUSION_INPUT_SHA256:
        raise ValueError("post-transclusion template identity drifted")
    surface = extract_poem_tag_surface(transclusion_input)

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": "gorky-klim-samgin-ru-poem-tag-surface",
        "research_date": research_date,
        "profile": PROFILE_VERSION,
        "template_revision": {
            "revision_id": _TEMPLATE_REVISION_ID,
            "wikitext_sha256": _TEMPLATE_WIKITEXT_SHA256,
            "transclusion_input_sha256": _TRANSCLUSION_INPUT_SHA256,
        },
        "tag_surface": surface,
        "concrete_invocations": concrete_content,
        "semantics_evidence": [
            {
                "url": MEDIAWIKI_MAGIC_WORDS,
                "claim": "#tag invokes an XML-style parser/extension tag; the first argument is tag content and later named arguments are tag attributes",
            },
            {
                "url": MEDIAWIKI_TEMPLATE_EXPANSION,
                "claim": "template parameters and parser functions are expansion layers distinct from the top-level #tag call surface frozen here",
            },
        ],
        "capture_scope": {
            "single_reached_tag_poem_call_source_frozen": True,
            "content_argument_source_surface_frozen": True,
            "literal_attribute_names_frozen": True,
            "attribute_value_expression_identities_frozen": True,
            "six_content_identities_bound_to_reached_call": True,
            "nested_parser_function_values_evaluated": False,
            "mediawiki_core_recursive_parse_reproduced": False,
            "poem_extension_rendering_reproduced": False,
            "resolved_part2_identity_frozen": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This source-free artifact freezes the exact top-level #tag:poem content/attribute "
            "source surface reached by the pinned poemx1 revision and binds the six already-frozen "
            "parameter-2 content identities to it. Attribute value expressions remain source-free "
            "digests/dependency inventories; nested parser-function evaluation, MediaWiki core "
            "recursive parsing, Poem rendering, resolved Part 2 bytes and historical render "
            "equivalence remain unresolved."
        ),
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }
