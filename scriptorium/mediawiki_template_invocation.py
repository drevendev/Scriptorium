"""Source-free binding evidence for bounded MediaWiki template invocations.

This module models the argument-binding layer that occurs when a concrete template
invocation creates a MediaWiki frame.  It intentionally stops before recursive
expansion of inserted argument wikitext, parser functions, extension tags, or render
output.  The committed evidence contains only offsets, parameter names, counts and
cryptographic digests; invocation/source prose is never persisted.

The bounded semantics are taken from MediaWiki's template documentation:

* anonymous arguments are numbered in anonymous-argument order only;
* explicitly named/numbered arguments bind by name and are whitespace-trimmed;
* anonymous argument whitespace is preserved;
* if a parameter is assigned more than once, the last assignment wins.

The parser is deliberately conservative.  It understands nested ``{{...}}`` /
``{{{...}}}`` groups and ``[[...|...]]`` links while splitting invocation arguments.
Unsupported literal parameter names fail closed rather than being guessed.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import re
from typing import Mapping, Sequence


PROFILE_VERSION = "scriptorium-mediawiki-template-invocation-bindings-v1"
MANIFEST_VERSION = "scriptorium-template-invocation-bindings-v1"
MEDIAWIKI_HELP_TEMPLATES = "https://www.mediawiki.org/wiki/Help:Templates"
MEDIAWIKI_TEMPLATE_EXPANSION = (
    "https://www.mediawiki.org/wiki/Manual:Template_expansion_process"
)
_LITERAL_NAME_RE = re.compile(r"[A-Za-z0-9_]+\Z")


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _matching_brace_end(text: str, start: int) -> int:
    """Return the exclusive end of one balanced MediaWiki brace construct."""
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


def _top_level_delimiters(text: str, delimiter: str) -> list[int]:
    """Return delimiter offsets outside nested braces and wikilinks."""
    if len(delimiter) != 1:
        raise ValueError("delimiter must be one character")
    offsets: list[int] = []
    cursor = 0
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
            offsets.append(cursor)
        cursor += 1
    if brace_stack:
        raise ValueError("unclosed nested brace construct in template invocation")
    if link_depth:
        raise ValueError("unclosed wikilink in template invocation")
    return offsets


def _split_top_level(text: str, delimiter: str) -> list[str]:
    offsets = _top_level_delimiters(text, delimiter)
    if not offsets:
        return [text]
    out: list[str] = []
    start = 0
    for offset in offsets:
        out.append(text[start:offset])
        start = offset + 1
    out.append(text[start:])
    return out


def _top_level_equals(text: str) -> int | None:
    offsets = _top_level_delimiters(text, "=")
    return offsets[0] if offsets else None


def _literal_parameter_name(raw_name: str) -> str:
    name = raw_name.strip()
    if not name or not _LITERAL_NAME_RE.fullmatch(name):
        raise ValueError(
            "dynamic or unsupported MediaWiki invocation parameter name outside literal profile"
        )
    return name


def _fragment_identity(fragment: str) -> dict[str, object]:
    raw = fragment.encode("utf-8")
    return {
        "character_count": len(fragment),
        "utf8_byte_count": len(raw),
        "sha256": sha256(raw).hexdigest(),
        "defined_empty": fragment == "",
    }


def parse_template_invocation(raw_invocation: str, *, template_name: str) -> dict[str, object]:
    """Bind one exact literal template invocation without expanding argument values."""
    if not isinstance(raw_invocation, str) or not raw_invocation.startswith("{{"):
        raise ValueError("template invocation must start with {{")
    if raw_invocation.startswith("{{{") or not raw_invocation.endswith("}}"):
        raise ValueError("template invocation must be a balanced double-brace group")
    if _matching_brace_end(raw_invocation, 0) != len(raw_invocation):
        raise ValueError("template invocation contains trailing material")

    inner = raw_invocation[2:-2]
    parts = _split_top_level(inner, "|")
    observed_title = parts[0].strip()
    if observed_title.casefold() != template_name.casefold():
        raise ValueError(f"unexpected template title {observed_title!r}")

    anonymous_index = 0
    assignments: list[dict[str, object]] = []
    effective: dict[str, dict[str, object]] = {}
    assignment_counts: Counter[str] = Counter()
    anonymous_count = 0
    named_count = 0

    for argument_ordinal, segment in enumerate(parts[1:], start=1):
        equals = _top_level_equals(segment)
        if equals is None:
            anonymous_count += 1
            anonymous_index += 1
            name = str(anonymous_index)
            argument = segment
            assignment_kind = "anonymous"
        else:
            named_count += 1
            name = _literal_parameter_name(segment[:equals])
            argument = segment[equals + 1 :].strip()
            assignment_kind = "named"

        identity = _fragment_identity(argument)
        assignment = {
            "argument_ordinal": argument_ordinal,
            "parameter_name": name,
            "assignment_kind": assignment_kind,
            **identity,
        }
        assignments.append(assignment)
        assignment_counts[name] += 1
        effective[name] = assignment

    duplicate_names = {
        name: count for name, count in sorted(assignment_counts.items()) if count > 1
    }
    return {
        "argument_count": len(parts) - 1,
        "anonymous_argument_count": anonymous_count,
        "named_argument_count": named_count,
        "duplicate_assignment_counts": duplicate_names,
        "assignments": assignments,
        "effective_bindings": {name: effective[name] for name in sorted(effective)},
    }


def find_template_invocations(wikitext: str, *, template_name: str) -> list[dict[str, object]]:
    """Locate exact literal invocations and return source-free binding records."""
    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    if not isinstance(template_name, str) or not template_name:
        raise ValueError("template_name must be non-empty")
    prefix = re.compile(
        r"\{\{\s*" + re.escape(template_name) + r"(?=\s*[|}])",
        re.IGNORECASE,
    )
    records: list[dict[str, object]] = []
    for index, match in enumerate(prefix.finditer(wikitext), start=1):
        start = match.start()
        end = _matching_brace_end(wikitext, start)
        raw = wikitext[start:end]
        binding = parse_template_invocation(raw, template_name=template_name)
        records.append(
            {
                "invocation_index": index,
                "parent_start_offset": start,
                "parent_end_offset": end,
                "invocation_character_count": len(raw),
                "invocation_utf8_byte_count": len(raw.encode("utf-8")),
                "invocation_sha256": _sha256_text(raw),
                **binding,
            }
        )
    return records


def build_invocation_binding_manifest(
    *,
    candidate_id: str,
    dependency_revision_identity: Mapping[str, object],
    dependency_wikitext: str,
    parameter_surface_names: Sequence[str],
    research_date: str,
    template_name: str = "poemx1",
    expected_invocation_count: int = 6,
) -> dict[str, object]:
    """Freeze source-free concrete invocation/frame bindings for Klim's poemx1 calls."""
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("candidate_id must be non-empty")
    if not isinstance(dependency_revision_identity, Mapping):
        raise TypeError("dependency_revision_identity must be a mapping")
    for key in ("title", "revision_id", "wikitext_sha256"):
        if key not in dependency_revision_identity:
            raise ValueError(f"dependency revision identity missing {key}")
    expected_digest = dependency_revision_identity["wikitext_sha256"]
    if _sha256_text(dependency_wikitext) != expected_digest:
        raise ValueError("dependency wikitext does not match frozen revision identity")
    if not isinstance(expected_invocation_count, int) or expected_invocation_count <= 0:
        raise ValueError("expected_invocation_count must be positive")

    surface_names = tuple(parameter_surface_names)
    if not surface_names or any(not isinstance(name, str) or not name for name in surface_names):
        raise ValueError("parameter surface names must be non-empty strings")
    if len(set(surface_names)) != len(surface_names):
        raise ValueError("parameter surface names must be unique")

    invocations = find_template_invocations(dependency_wikitext, template_name=template_name)
    if len(invocations) != expected_invocation_count:
        raise ValueError(
            f"expected {expected_invocation_count} {template_name} invocations, observed {len(invocations)}"
        )

    defined_counts: Counter[str] = Counter()
    empty_counts: Counter[str] = Counter()
    effective_binding_counts: Counter[str] = Counter()
    assignments_total = 0
    duplicates_total = 0
    for record in invocations:
        effective = record["effective_bindings"]
        assert isinstance(effective, dict)
        assignments = record["assignments"]
        assert isinstance(assignments, list)
        assignments_total += len(assignments)
        duplicate_counts = record["duplicate_assignment_counts"]
        assert isinstance(duplicate_counts, dict)
        duplicates_total += sum(int(count) - 1 for count in duplicate_counts.values())
        for name, binding in effective.items():
            effective_binding_counts[name] += 1
            if name in surface_names:
                defined_counts[name] += 1
                assert isinstance(binding, dict)
                if binding["defined_empty"] is True:
                    empty_counts[name] += 1

    surface_status = {
        name: {
            "defined_invocation_count": defined_counts[name],
            "defined_empty_invocation_count": empty_counts[name],
            "omitted_invocation_count": len(invocations) - defined_counts[name],
        }
        for name in sorted(surface_names)
    }
    outside_surface = sorted(set(effective_binding_counts) - set(surface_names))
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": candidate_id,
        "research_date": research_date,
        "template_name": template_name,
        "binding_profile": PROFILE_VERSION,
        "dependency_revision": {
            "title": dependency_revision_identity["title"],
            "revision_id": dependency_revision_identity["revision_id"],
            "wikitext_sha256": dependency_revision_identity["wikitext_sha256"],
        },
        "expected_invocation_count": expected_invocation_count,
        "invocations": invocations,
        "summary": {
            "invocation_count": len(invocations),
            "assignment_count": assignments_total,
            "duplicate_effective_assignment_count": duplicates_total,
            "effective_binding_name_counts": dict(sorted(effective_binding_counts.items())),
            "parameter_surface_status": surface_status,
            "effective_binding_names_outside_parameter_surface": outside_surface,
        },
        "semantics_evidence": [
            {
                "url": MEDIAWIKI_HELP_TEMPLATES,
                "claim": (
                    "anonymous arguments are numbered in anonymous-argument order; named/numbered "
                    "arguments bind by name; named values are trimmed while anonymous whitespace is "
                    "preserved; later duplicate assignments win"
                ),
            },
            {
                "url": MEDIAWIKI_TEMPLATE_EXPANSION,
                "claim": (
                    "template-call parts distinguish implicitly numbered from named parameters; "
                    "recursive argument expansion is a later layer and is not reproduced here"
                ),
            },
        ],
        "capture_scope": {
            "concrete_invocation_shapes_frozen": True,
            "invocation_argument_binding_reproduced": True,
            "literal_parameter_surface_binding_frozen": True,
            "inserted_parameter_value_recursive_expansion_reproduced": False,
            "parser_function_expansion_reproduced": False,
            "extension_tag_expansion_reproduced": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False,
        },
        "boundary": (
            "This artifact binds the six frozen poemx1 invocation argument shapes to MediaWiki frame "
            "parameter names and to the already-frozen literal template-parameter surface. Argument "
            "prose is represented only by counts and SHA-256 digests. Recursive expansion of inserted "
            "argument wikitext, parser functions, #tag:poem, resolved Part 2 bytes and historical render "
            "equivalence remain unresolved."
        ),
        "source_text_included": False,
    }
