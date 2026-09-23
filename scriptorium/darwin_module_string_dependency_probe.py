"""Probe exact Darwin/Rachinsky Module:String dependency surface without retaining source."""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha1, sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from scriptorium.darwin_dependency_revision_observation import (
    DEPENDENCY_TITLE,
    load_object,
    observation_sha256,
    validate_observation,
)

SCHEMA_VERSION = "scriptorium-darwin-module-string-dependency-probe-v1"
LOADER_NAMES = ("require", "mw.loadData", "mw.loadJsonData")
FORBIDDEN_SOURCE_KEYS = {"content", "text", "wikitext", "body", "source_text"}


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def probe_sha256(probe: Mapping[str, object]) -> str:
    payload = deepcopy(dict(probe))
    payload.pop("probe_sha256", None)
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _long_bracket_end(source: str, start: int) -> int | None:
    if start >= len(source) or source[start] != "[":
        return None
    i = start + 1
    while i < len(source) and source[i] == "=":
        i += 1
    if i >= len(source) or source[i] != "[":
        return None
    marker = "]" + "=" * (i - start - 1) + "]"
    end = source.find(marker, i + 1)
    return len(source) if end < 0 else end + len(marker)


def _skip_lua_comment(source: str, start: int) -> int | None:
    if not source.startswith("--", start):
        return None
    long_end = _long_bracket_end(source, start + 2)
    if long_end is not None:
        return long_end
    end = source.find("\n", start + 2)
    return len(source) if end < 0 else end + 1


def _skip_trivia(source: str, start: int) -> int:
    pos = start
    while pos < len(source):
        while pos < len(source) and source[pos].isspace():
            pos += 1
        comment_end = _skip_lua_comment(source, pos)
        if comment_end is None:
            break
        pos = comment_end
    return pos


def _parse_quoted_literal(source: str, start: int) -> tuple[str, int] | None:
    if start >= len(source) or source[start] not in {"'", '"'}:
        return None
    quote = source[start]
    out: list[str] = []
    i = start + 1
    while i < len(source):
        ch = source[i]
        if ch == "\\":
            if i + 1 >= len(source):
                return None
            out.append(source[i + 1])
            i += 2
            continue
        if ch == quote:
            return "".join(out), i + 1
        out.append(ch)
        i += 1
    return None


def _skip_quoted_literal(source: str, start: int) -> int | None:
    parsed = _parse_quoted_literal(source, start)
    return None if parsed is None else parsed[1]


def _iter_loader_calls(source: str) -> list[tuple[str, str | None]]:
    """Lex direct Lua loader calls while ignoring comments and string bodies.

    Literal single/double-quoted arguments are captured both in parenthesized
    calls and Lua's bare-string call form. Long-string/table/dynamic arguments
    are recorded as unsupported so the derived scan fails closed rather than
    silently claiming completeness.
    """

    calls: list[tuple[str, str | None]] = []
    i = 0
    while i < len(source):
        comment_end = _skip_lua_comment(source, i)
        if comment_end is not None:
            i = comment_end
            continue
        if source[i] in {"'", '"'}:
            end = _skip_quoted_literal(source, i)
            i = len(source) if end is None else end
            continue
        long_end = _long_bracket_end(source, i)
        if long_end is not None:
            i = long_end
            continue
        if source[i].isalpha() or source[i] == "_":
            start = i
            i += 1
            while i < len(source) and (source[i].isalnum() or source[i] in {"_", "."}):
                i += 1
            name = source[start:i]
            if name not in LOADER_NAMES:
                continue
            pos = _skip_trivia(source, i)
            if pos >= len(source):
                continue

            if source[pos] in {"'", '"'}:
                parsed = _parse_quoted_literal(source, pos)
                calls.append((name, None if parsed is None else parsed[0]))
                i = len(source) if parsed is None else parsed[1]
                continue

            if source[pos] in {"[", "{"}:
                calls.append((name, None))
                i = pos + 1
                continue

            if source[pos] != "(":
                continue

            pos = _skip_trivia(source, pos + 1)
            if pos >= len(source):
                calls.append((name, None))
                break
            parsed = _parse_quoted_literal(source, pos)
            if parsed is None:
                calls.append((name, None))
                i = pos + 1
                continue
            literal, end = parsed
            pos = _skip_trivia(source, end)
            calls.append((name, literal if pos < len(source) and source[pos] == ")" else None))
            i = pos + 1 if pos < len(source) else pos
            continue
        i += 1
    return calls


def _normalize_wiki_module_literal(value: str) -> str | None:
    raw = value.strip()
    if ":" not in raw:
        return None
    prefix, rest = raw.split(":", 1)
    rest = rest.strip()
    if prefix.casefold() not in {"module", "модуль"} or not rest:
        return None
    return "Модуль:" + rest


def scan_lua_dependency_surface(source: str) -> dict[str, object]:
    """Return only source-free direct-loader metadata from transient Lua source."""
    wiki_dependencies: set[str] = set()
    non_wiki_literals: set[str] = set()
    dynamic_or_unsupported: list[str] = []

    for loader, literal in _iter_loader_calls(source):
        if literal is None:
            dynamic_or_unsupported.append(loader)
            continue
        dependency = _normalize_wiki_module_literal(literal)
        if dependency is not None:
            wiki_dependencies.add(dependency)
        else:
            non_wiki_literals.add(literal)

    raw = source.encode("utf-8")
    return {
        "scan_method": "scriptorium-darwin-lua-loader-scan-v1",
        "scan_scope": "direct require/mw.loadData/mw.loadJsonData calls; alias/computed semantic analysis not attempted",
        "source_utf8_bytes": len(raw),
        "source_sha1": sha1(raw).hexdigest(),
        "source_sha256": sha256(raw).hexdigest(),
        "static_wiki_module_dependencies": sorted(wiki_dependencies),
        "non_wiki_require_literals": sorted(non_wiki_literals),
        "dynamic_or_unsupported_loader_calls": sorted(dynamic_or_unsupported),
        "scan_complete": not dynamic_or_unsupported,
        "semantic_dependency_closure_proved": False,
    }


def _assert_source_free(value: object, *, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_SOURCE_KEYS:
                raise ValueError(f"source content key {key!r} forbidden at {path}")
            _assert_source_free(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_source_free(child, path=f"{path}[{index}]")


def build_probe(api_response: Mapping[str, object], observation: Mapping[str, object]) -> dict[str, object]:
    identity = observation.get("identity")
    if not isinstance(identity, dict):
        raise ValueError("committed Module:String observation identity missing")
    if observation.get("observation_sha256") != observation_sha256(observation):
        raise ValueError("committed Module:String observation digest drift")

    query = api_response.get("query")
    if not isinstance(query, dict):
        raise ValueError("MediaWiki exact-revision query payload missing")
    pages = query.get("pages")
    if not isinstance(pages, list) or len(pages) != 1 or not isinstance(pages[0], dict):
        raise ValueError("expected exactly one MediaWiki page")
    page = pages[0]
    if page.get("title") != identity.get("canonical_title") or page.get("title") != DEPENDENCY_TITLE:
        raise ValueError("Module:String canonical title drift")
    revisions = page.get("revisions")
    if not isinstance(revisions, list) or len(revisions) != 1 or not isinstance(revisions[0], dict):
        raise ValueError("expected exactly one exact dependency revision")
    revision = revisions[0]
    for key, observed_key in (("revid", "revision_id"), ("timestamp", "revision_timestamp"), ("sha1", "mediawiki_sha1")):
        if revision.get(key) != identity.get(observed_key):
            raise ValueError(f"Module:String exact revision {key} drift")
    slots = revision.get("slots")
    if not isinstance(slots, dict) or not isinstance(slots.get("main"), dict):
        raise ValueError("Module:String exact revision main slot missing")
    content = slots["main"].get("content")
    if not isinstance(content, str):
        raise ValueError("Module:String exact revision source missing")
    surface = scan_lua_dependency_surface(content)
    if surface["source_sha1"] != identity.get("mediawiki_sha1"):
        raise ValueError("Module:String transient source SHA-1 does not match observed MediaWiki SHA-1")

    probe: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": "darwin-origin-species-rachinsky-1864-ru",
        "dependency_title": DEPENDENCY_TITLE,
        "bound_observation": {
            "schema_version": observation.get("schema_version"),
            "observation_sha256": observation.get("observation_sha256"),
        },
        "identity": dict(identity),
        "exact_revision_query": {
            "provider": "Russian Wikisource Action API",
            "endpoint": "https://ru.wikisource.org/w/api.php",
            "selection": "exact_revision_id_from_reviewed_observation",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "source_content_requested_transiently": True,
        },
        "dependency_surface": surface,
        "gates": {
            "module_string_dependency_surface_probed": True,
            "module_string_identity_bound": False,
            "dependency_closure_complete": False,
            "outputs_verified": False,
            "render_profile_rule_promoted": False,
            "literary_body_count_and_digests_frozen": False,
            "minimum_300k_proved": False,
            "fantlab_source_edition_match": "unknown",
            "m2_parity_admissible": False,
        },
        "source_text_included": False,
    }
    _assert_source_free(probe)
    probe["probe_sha256"] = probe_sha256(probe)
    return probe


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-response", type=Path, required=True)
    parser.add_argument("--observation", type=Path, required=True)
    parser.add_argument("--predecessor-contract", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    observation = load_object(args.observation)
    predecessor = load_object(args.predecessor_contract)
    policy = load_object(args.policy)
    validate_observation(observation, predecessor, policy)
    probe = build_probe(load_object(args.api_response), observation)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(probe, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    surface = probe["dependency_surface"]
    print(
        "SCRIPTORIUM_DARWIN_MODULE_STRING_PROBE="
        f"{probe['identity']['canonical_title']}@{probe['identity']['revision_id']} "
        f"scan_complete={surface['scan_complete']} "
        f"dependencies={surface['static_wiki_module_dependencies']} "
        f"probe_sha256={probe['probe_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
