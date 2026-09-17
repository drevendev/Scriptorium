"""Fail-closed MediaWiki template-parameter evidence for pinned template sources.

This module intentionally implements only literal triple-brace parameter references.
It preserves the distinction between an undefined parameter and a parameter defined as
an empty string, supports defaults (including nested literal parameter defaults), and
leaves an undefined parameter without a default as its original triple-brace spelling.

It does *not* parse template invocations, bind the six Klim Samgin ``poemx1`` calls,
expand parser functions, render extension tags, or claim historical MediaWiki render
equivalence. Dynamic parameter names are rejected rather than guessed.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import re
from typing import Mapping

PROFILE_VERSION = "scriptorium-mediawiki-template-parameters-v1"
MANIFEST_VERSION = "scriptorium-template-parameter-surface-v1"
MEDIAWIKI_HELP_TEMPLATES = "https://www.mediawiki.org/wiki/Help:Templates"
MEDIAWIKI_HELP_PARSER_PARAMETERS = (
    "https://www.mediawiki.org/wiki/Help:Parser_functions_in_templates"
)
MEDIAWIKI_TEMPLATE_EXPANSION = (
    "https://www.mediawiki.org/wiki/Manual:Template_expansion_process"
)
_LITERAL_NAME_RE = re.compile(r"[A-Za-z0-9_]+\Z")


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _matching_brace_end(text: str, start: int) -> int:
    """Return the exclusive end of a balanced ``{{...}}``/``{{{...}}}`` group."""
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


def _split_parameter_inner(inner: str) -> tuple[str, str | None]:
    """Split ``name|default`` on the first top-level pipe."""
    cursor = 0
    while cursor < len(inner):
        if inner.startswith("{{", cursor):
            cursor = _matching_brace_end(inner, cursor)
            continue
        if inner[cursor] == "|":
            return inner[:cursor], inner[cursor + 1 :]
        cursor += 1
    return inner, None


def _literal_parameter_name(raw_name: str) -> str:
    name = raw_name.strip()
    if not name or not _LITERAL_NAME_RE.fullmatch(name):
        raise ValueError(
            "dynamic or unsupported MediaWiki parameter name outside literal profile"
        )
    return name


def expand_literal_template_parameters(
    text: str, parameters: Mapping[str, str]
) -> str:
    """Expand the bounded literal triple-brace parameter layer.

    A provided empty string is a defined value and therefore suppresses a default.
    Missing parameters use their default when one exists; a missing parameter with no
    default is preserved verbatim. Inserted argument values are not recursively parsed
    by this layer because later MediaWiki expansion remains outside this profile.
    """
    if not isinstance(text, str):
        raise TypeError("text must be str")
    if not isinstance(parameters, Mapping):
        raise TypeError("parameters must be a mapping")
    for key, value in parameters.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("parameter names and values must be strings")

    out: list[str] = []
    cursor = 0
    while cursor < len(text):
        start = text.find("{{{", cursor)
        if start < 0:
            out.append(text[cursor:])
            break
        out.append(text[cursor:start])
        end = _matching_brace_end(text, start)
        raw = text[start:end]
        inner = raw[3:-3]
        raw_name, default = _split_parameter_inner(inner)
        name = _literal_parameter_name(raw_name)
        if name in parameters:
            out.append(parameters[name])
        elif default is not None:
            out.append(expand_literal_template_parameters(default, parameters))
        else:
            out.append(raw)
        cursor = end
    return "".join(out)


def parameter_reference_inventory(text: str) -> dict[str, object]:
    """Return a source-free inventory of literal parameter references."""
    counts: Counter[str] = Counter()
    defaulted: Counter[str] = Counter()
    empty_defaults: Counter[str] = Counter()
    bare: Counter[str] = Counter()
    cursor = 0
    total = 0
    while cursor < len(text):
        start = text.find("{{{", cursor)
        if start < 0:
            break
        end = _matching_brace_end(text, start)
        inner = text[start + 3 : end - 3]
        raw_name, default = _split_parameter_inner(inner)
        name = _literal_parameter_name(raw_name)
        counts[name] += 1
        total += 1
        if default is None:
            bare[name] += 1
        else:
            defaulted[name] += 1
            if default == "":
                empty_defaults[name] += 1
            nested = parameter_reference_inventory(default)
            for nested_name, nested_count in nested["parameter_reference_counts"].items():
                counts[nested_name] += nested_count
            for nested_name, nested_count in nested["defaulted_reference_counts"].items():
                defaulted[nested_name] += nested_count
            for nested_name, nested_count in nested["empty_default_reference_counts"].items():
                empty_defaults[nested_name] += nested_count
            for nested_name, nested_count in nested["bare_reference_counts"].items():
                bare[nested_name] += nested_count
            total += nested["total_reference_count"]
        cursor = end
    return {
        "total_reference_count": total,
        "parameter_reference_counts": dict(sorted(counts.items())),
        "defaulted_reference_counts": dict(sorted(defaulted.items())),
        "empty_default_reference_counts": dict(sorted(empty_defaults.items())),
        "bare_reference_counts": dict(sorted(bare.items())),
    }


def build_parameter_surface_manifest(
    *,
    candidate_id: str,
    revision_identity: Mapping[str, object],
    transclusion_input: str,
    research_date: str,
) -> dict[str, object]:
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("candidate_id must be non-empty")
    if not isinstance(revision_identity, Mapping):
        raise TypeError("revision_identity must be a mapping")
    for key in ("title", "revision_id", "wikitext_sha256"):
        if key not in revision_identity:
            raise ValueError(f"revision identity missing {key}")
    if not isinstance(transclusion_input, str):
        raise TypeError("transclusion_input must be str")

    inventory = parameter_reference_inventory(transclusion_input)
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": candidate_id,
        "research_date": research_date,
        "source_revision": {
            "title": revision_identity["title"],
            "revision_id": revision_identity["revision_id"],
            "wikitext_sha256": revision_identity["wikitext_sha256"],
        },
        "parameter_profile": PROFILE_VERSION,
        "transclusion_input_sha256": _sha256_text(transclusion_input),
        "parameter_surface": inventory,
        "semantics_evidence": [
            {
                "url": MEDIAWIKI_HELP_TEMPLATES,
                "claim": (
                    "template parameters use triple braces; omitted parameters may use defaults; "
                    "an explicitly empty parameter is defined and does not trigger its default"
                ),
            },
            {
                "url": MEDIAWIKI_HELP_PARSER_PARAMETERS,
                "claim": (
                    "undefined parameters differ from defined empty parameters; empty defaults are "
                    "commonly used to collapse undefined parameters to empty text"
                ),
            },
            {
                "url": MEDIAWIKI_TEMPLATE_EXPANSION,
                "claim": (
                    "template-argument titles/default branches participate in MediaWiki's expansion "
                    "process; this bounded profile supports only literal parameter names"
                ),
            },
        ],
        "capture_scope": {
            "literal_parameter_reference_surface_frozen": True,
            "literal_parameter_default_semantics_reproduced": True,
            "dynamic_parameter_names_supported": False,
            "invocation_argument_binding_reproduced": False,
            "inserted_parameter_value_recursive_expansion_reproduced": False,
            "parser_function_expansion_reproduced": False,
            "extension_tag_expansion_reproduced": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This artifact freezes the literal triple-brace parameter reference/default surface after "
            "the already-frozen partial-transclusion selection. It does not bind the six poemx1 calls, "
            "expand inserted argument wikitext, execute parser functions/#tag, or prove historical render equivalence."
        ),
        "source_text_included": False,
    }
