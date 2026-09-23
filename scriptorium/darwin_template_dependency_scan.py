"""Source-free direct-dependency discovery for the Darwin/Rachinsky ``{{ё}}`` roots.

This module deliberately implements only the bounded MediaWiki syntax needed by the two
exact Russian Wikisource root revisions used by Scriptorium. It is fail-closed: dynamic
or unsupported invocation names raise instead of being guessed. Callers may fetch exact
revision content transiently, but committed artifacts retain only digests, byte counts
and dependency titles.
"""

from __future__ import annotations

from hashlib import sha1, sha256
import re
from typing import Iterable


SCAN_METHOD = (
    "scriptorium-darwin-transclusion-scan-v1: exact revision source; MediaWiki "
    "noinclude/includeonly/onlyinclude filtering; redirect target plus static "
    "template/#invoke module names; fail closed on dynamic or unsupported names"
)

_STRIP_TAGS = ("nowiki", "pre", "syntaxhighlight", "source")
_REDIRECT_RE = re.compile(
    r"^\s*#(?:redirect|перенаправление)\s*\[\[\s*([^\]|#]+)",
    flags=re.IGNORECASE,
)


def _normalize_explicit_title(raw: str) -> str:
    title = raw.strip().lstrip(":").strip()
    if not title:
        raise ValueError("empty MediaWiki dependency title")
    if ":" not in title:
        return "Шаблон:" + title
    prefix, rest = title.split(":", 1)
    rest = rest.strip()
    if not rest:
        raise ValueError("empty MediaWiki dependency page name")
    if prefix.casefold() in {"шаблон", "template"}:
        return "Шаблон:" + rest
    if prefix.casefold() in {"модуль", "module"}:
        return "Модуль:" + rest
    raise ValueError(f"unsupported MediaWiki dependency namespace: {prefix!r}")


def transclusion_source(text: str) -> str:
    """Return the bounded transclusion-visible source used for dependency scanning."""

    value = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    for tag in _STRIP_TAGS:
        value = re.sub(
            rf"<{tag}\b[^>]*>.*?</{tag}\s*>",
            "",
            value,
            flags=re.IGNORECASE | re.DOTALL,
        )
        value = re.sub(rf"<{tag}\b[^>]*/\s*>", "", value, flags=re.IGNORECASE | re.DOTALL)

    only = re.findall(
        r"<onlyinclude\b[^>]*>(.*?)</onlyinclude\s*>",
        value,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if only:
        value = "".join(only)
    else:
        value = re.sub(
            r"<noinclude\b[^>]*>.*?</noinclude\s*>",
            "",
            value,
            flags=re.IGNORECASE | re.DOTALL,
        )
        value = re.sub(r"<noinclude\b[^>]*/\s*>", "", value, flags=re.IGNORECASE | re.DOTALL)
        value = re.sub(r"</?includeonly\b[^>]*>", "", value, flags=re.IGNORECASE)
        value = re.sub(r"</?onlyinclude\b[^>]*>", "", value, flags=re.IGNORECASE)
    return value


def _invocation_heads(text: str) -> list[str]:
    heads: list[str] = []
    i = 0
    while i < len(text) - 1:
        if text.startswith("{{{{{", i):
            raise ValueError("dynamic template name requires explicit evidence")
        if text.startswith("{{{", i):
            i += 3
            continue
        if not text.startswith("{{", i):
            i += 1
            continue

        start = i + 2
        depth = 1
        j = start
        while j < len(text):
            if text.startswith("{{{", j):
                end = text.find("}}}", j + 3)
                if end < 0:
                    raise ValueError("unclosed MediaWiki parameter syntax")
                j = end + 3
                continue
            if text.startswith("{{", j):
                depth += 1
                j += 2
                continue
            if text.startswith("}}", j):
                depth -= 1
                if depth == 0:
                    raw = text[start:j].strip()
                    heads.append(raw.split("|", 1)[0].strip())
                    break
                j += 2
                continue
            j += 1
        if depth != 0:
            raise ValueError("unclosed MediaWiki template syntax")
        i += 2
    return heads


def _dependency_from_head(head: str) -> str | None:
    if not head:
        return None
    lowered = head.casefold()
    if lowered.startswith("#invoke:"):
        module = head.split(":", 1)[1].strip()
        if not module or "{{" in module or "}}" in module:
            raise ValueError("dynamic or empty #invoke module name")
        return _normalize_explicit_title("Модуль:" + module)
    if head.startswith("#") or lowered.startswith(("int:", "msg:", "msgnw:", "raw:")):
        return None
    if head.startswith("{") or "{{" in head or "}}" in head:
        raise ValueError(f"dynamic template name requires explicit evidence: {head!r}")
    if ":" in head:
        return _normalize_explicit_title(head)
    if head.isupper() and re.fullmatch(r"[A-ZА-ЯЁ0-9_]+", head):
        return None
    return _normalize_explicit_title(head)


def discover_direct_dependencies(text: str) -> tuple[str, ...]:
    """Discover static direct template/module dependencies in transclusion context."""

    visible = transclusion_source(text)
    redirect = _REDIRECT_RE.match(visible)
    if redirect:
        return (_normalize_explicit_title(redirect.group(1)),)

    dependencies = {
        dependency
        for head in _invocation_heads(visible)
        if (dependency := _dependency_from_head(head)) is not None
    }
    return tuple(sorted(dependencies))


def source_free_scan_observation(text: str) -> dict[str, object]:
    """Return source-free reproducibility metadata for one transient exact source body."""

    raw = text.encode("utf-8")
    visible = transclusion_source(text)
    redirect = _REDIRECT_RE.match(visible)
    return {
        "scan_method": SCAN_METHOD,
        "source_utf8_bytes": len(raw),
        "source_sha1": sha1(raw).hexdigest(),
        "transclusion_sha256": sha256(visible.encode("utf-8")).hexdigest(),
        "redirect_target": _normalize_explicit_title(redirect.group(1)) if redirect else None,
        "direct_dependencies": list(discover_direct_dependencies(text)),
    }


def ensure_expected_dependencies(actual: Iterable[str], expected: Iterable[str]) -> None:
    if tuple(actual) != tuple(expected):
        raise ValueError("Darwin {{ё}} direct dependency discovery drift")
