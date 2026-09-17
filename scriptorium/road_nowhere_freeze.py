"""Freeze the literary body of the pinned alternate Road to Nowhere revision.

The retained alternate route is the az.lib-derived single-page Russian Wikisource
transcription at oldid 5585836. The exact observed source shape is deliberately
narrow: one leading ``Отексте`` scaffold, direct prose, 27 level-three literary
headings, then five category links. Any shape drift fails closed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .single_page_body import (
    BODY_MANIFEST_VERSION,
    build_body_manifest as build_generic_body_manifest,
    fetch_pinned_wikitext,
    replay_body_manifest as replay_generic_body_manifest,
    validate_body_manifest as validate_generic_body_manifest,
)
from .single_page_revision import validate_manifest as validate_revision_manifest
from .wikisource_freeze import extract_transcription_body


CANDIDATE_ID = "grin-road-nowhere-ru"
TITLE = "Дорога в никуда (Грин)"
REVISION_ID = 5585836
EXTRACTION_PROFILE = "scriptorium-road-nowhere-alt-wikisource-body-v1"
_EXPECTED_HEADING_COUNT = 27
_EXPECTED_CATEGORY_COUNT = 5
_EXPECTED_COMMENT_COUNT_AFTER_SCAFFOLD = 0

_HEADING3_RE = re.compile(
    r"(?m)^[ \t]*===(?!=)[ \t]*(?P<text>[^\n=].*?)[ \t]*(?<![=])===(?![=])[ \t]*$"
)
_ANY_HEADING_RE = re.compile(r"(?m)^[ \t]*={2,6}.*?={2,6}[ \t]*$")
_CATEGORY_LINE_RE = re.compile(
    r"(?mi)^[ \t]*\[\[\s*Категория\s*:(?P<name>[^\]\n]+)\]\][ \t]*$"
)
_EXTERNAL_LINK_RE = re.compile(r"\[(?:https?|ftp)://", re.IGNORECASE)
_TABLE_MARKER_RE = re.compile(r"(?m)^[ \t]*(?:\{\||\|-|\|\}|!|\|)")
_HTML_TAG_RE = re.compile(r"</?[A-Za-z][^>]*>")


def _strip_leading_template(source: str, name: str) -> str:
    stripped = source.lstrip()
    marker = "{{" + name
    if not stripped.casefold().startswith(marker.casefold()):
        raise ValueError(f"expected leading {name} template")
    depth = 0
    index = 0
    while index < len(stripped) - 1:
        pair = stripped[index : index + 2]
        if pair == "{{":
            depth += 1
            index += 2
            continue
        if pair == "}}":
            depth -= 1
            index += 2
            if depth == 0:
                return stripped[index:]
            if depth < 0:
                break
            continue
        index += 1
    raise ValueError(f"unterminated leading {name} template")


def _strip_trailing_categories(source: str) -> str:
    matches = tuple(_CATEGORY_LINE_RE.finditer(source))
    if len(matches) != _EXPECTED_CATEGORY_COUNT:
        raise ValueError(f"Road to Nowhere category inventory drift: {len(matches)}")
    first = matches[0].start()
    suffix = source[first:]
    if _CATEGORY_LINE_RE.sub("", suffix).strip():
        raise ValueError("unsupported content after Road to Nowhere category block")
    literary = source[:first].rstrip()
    if not literary:
        raise ValueError("empty Road to Nowhere literary body before categories")
    return literary


def _plain_heading(match: re.Match[str]) -> str:
    text = match.group("text").strip()
    if not text:
        raise ValueError("empty Road to Nowhere literary heading")
    if any(marker in text for marker in ("{{", "}}", "[[", "]]", "<", ">")):
        raise ValueError("unsupported markup inside Road to Nowhere heading")
    return f"\n\n{text}\n\n"


def extract_literary_body(wikitext: str) -> str:
    """Extract the exact observed alternate single-page transcription fail-closed."""

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    source = _strip_leading_template(wikitext, "Отексте")

    if "{{" in source or "}}" in source:
        raise ValueError("unsupported template remains after Road to Nowhere scaffold")
    headings = _HEADING3_RE.findall(source)
    if len(headings) != _EXPECTED_HEADING_COUNT:
        raise ValueError(f"Road to Nowhere heading inventory drift: {len(headings)}")
    if len(_ANY_HEADING_RE.findall(source)) != _EXPECTED_HEADING_COUNT:
        raise ValueError("unsupported Road to Nowhere heading level or shape")
    if source.count("[[") != _EXPECTED_CATEGORY_COUNT or source.count("]]" ) != _EXPECTED_CATEGORY_COUNT:
        raise ValueError("Road to Nowhere wikilink inventory drift")
    if source.count("<!--") != _EXPECTED_COMMENT_COUNT_AFTER_SCAFFOLD or source.count("-->") != _EXPECTED_COMMENT_COUNT_AFTER_SCAFFOLD:
        raise ValueError("Road to Nowhere HTML comment inventory drift")
    if source.count("''") != 0:
        raise ValueError("Road to Nowhere bold/italic inventory drift")
    if _HTML_TAG_RE.search(source):
        raise ValueError("unsupported Road to Nowhere HTML tag")
    if _EXTERNAL_LINK_RE.search(source):
        raise ValueError("unsupported Road to Nowhere external link")
    if _TABLE_MARKER_RE.search(source):
        raise ValueError("unsupported Road to Nowhere table markup")

    literary = _strip_trailing_categories(source)
    literary = _HEADING3_RE.sub(_plain_heading, literary)
    return extract_transcription_body(f'<div class="text">{literary}</div>')


def _validate_revision_target(revision_manifest: Mapping[str, object]) -> None:
    validate_revision_manifest(revision_manifest)
    if revision_manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Road to Nowhere candidate id")
    identity = revision_manifest.get("source_identity")
    if not isinstance(identity, dict):
        raise ValueError("Road to Nowhere revision identity missing")
    if identity.get("title") != TITLE or identity.get("revision_id") != REVISION_ID:
        raise ValueError("revision manifest does not identify the frozen Road to Nowhere alternate revision")


def build_body_manifest(
    revision_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    _validate_revision_target(revision_manifest)
    return build_generic_body_manifest(
        revision_manifest,
        fetcher=fetcher,
        extractor=extract_literary_body,
        extraction_profile=EXTRACTION_PROFILE,
    )


def validate_body_manifest(
    body_manifest: Mapping[str, object],
    *,
    revision_manifest: Mapping[str, object] | None = None,
) -> None:
    validate_generic_body_manifest(
        body_manifest,
        revision_manifest=revision_manifest,
        extraction_profile=EXTRACTION_PROFILE,
    )
    if body_manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Road to Nowhere body candidate")
    source_revision = body_manifest.get("source_revision")
    if not isinstance(source_revision, dict):
        raise ValueError("Road to Nowhere body source revision missing")
    if source_revision.get("title") != TITLE or source_revision.get("revision_id") != REVISION_ID:
        raise ValueError("Road to Nowhere body source revision drift")
    if revision_manifest is not None:
        _validate_revision_target(revision_manifest)


def replay_body_manifest(
    revision_manifest: Mapping[str, object],
    body_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    _validate_revision_target(revision_manifest)
    validate_body_manifest(body_manifest, revision_manifest=revision_manifest)
    return replay_generic_body_manifest(
        revision_manifest,
        body_manifest,
        fetcher=fetcher,
        extractor=extract_literary_body,
        extraction_profile=EXTRACTION_PROFILE,
    )


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze or replay the alternate Road to Nowhere Wikisource literary body.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--revision-manifest", type=Path, required=True)
    capture.add_argument("--output", type=Path, required=True)
    replay = subparsers.add_parser("replay")
    replay.add_argument("--revision-manifest", type=Path, required=True)
    replay.add_argument("--body-manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)

    revision_manifest = _load_json(args.revision_manifest)
    if args.command == "capture":
        body_manifest = build_body_manifest(revision_manifest)
        validate_body_manifest(body_manifest, revision_manifest=revision_manifest)
        _write_json(args.output, body_manifest)
        return 0
    body_manifest = _load_json(args.body_manifest)
    receipt = replay_body_manifest(revision_manifest, body_manifest)
    if args.receipt is not None:
        _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
