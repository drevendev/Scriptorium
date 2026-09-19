"""Freeze the literary body of the pinned Beketova Captain Grant revision.

The retained Russian Wikisource revision is one large direct transcription rather
than the ``<div class=\"text\">`` shape used by the generic single-page helper.
The exact observed revision has 36 lines of bibliographic/title-page scaffold,
then a three-part / seventy-chapter literary body, followed by eight category
links.  The source revision identity is verified before this extractor runs; this
module additionally freezes that observed markup topology and fails closed on
shape drift.  Source prose is never persisted by this module.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .single_page_body import (
    build_body_manifest as build_generic_body_manifest,
    fetch_pinned_wikitext,
    replay_body_manifest as replay_generic_body_manifest,
    validate_body_manifest as validate_generic_body_manifest,
)
from .single_page_revision import validate_manifest as validate_revision_manifest
from .wikisource_freeze import extract_transcription_body


CANDIDATE_ID = "verne-children-captain-grant-beketova-ru"
TITLE = "Дети капитана Гранта (Верн; Бекетова)"
REVISION_ID = 5304880
EXTRACTION_PROFILE = "scriptorium-beketova-captain-grant-wikisource-body-v1"

_EXPECTED_LINE_COUNT = 11_028
_BODY_START_LINE = 37
_EXPECTED_CATEGORY_COUNT = 8
_EXPECTED_PART_HEADING_COUNT = 3
_EXPECTED_CHAPTER_HEADING_COUNT = 140
_EXPECTED_TEMPLATE_INVENTORY = ("Отексте", "книга", "uc", "h")
_EXPECTED_CENTER_TAG_COUNT = 6

_TEMPLATE_NAME_RE = re.compile(r"\{\{\s*([^|{}\n]+)")
_HTML_TAG_RE = re.compile(r"</?\s*([A-Za-z][A-Za-z0-9]*)\b[^>]*>")
_HEADING_RE = re.compile(r"^[ \t]*(={2,6})(.*?)(\1)[ \t]*$")
_CATEGORY_LINE_RE = re.compile(r"(?i)^[ \t]*\[\[\s*Категория\s*:[^\]\n]+\]\][ \t]*$")
_EXTERNAL_LINK_RE = re.compile(r"\[(?:https?|ftp)://", re.IGNORECASE)
_TABLE_MARKER_RE = re.compile(r"^[ \t]*(?:\{\||\|-|\|\}|!|\|)")


def _validate_source_shape(wikitext: str) -> tuple[list[str], list[str]]:
    lines = wikitext.splitlines()
    if len(lines) != _EXPECTED_LINE_COUNT:
        raise ValueError(f"Beketova line inventory drift: {len(lines)}")

    template_names = tuple(match.group(1).strip() for match in _TEMPLATE_NAME_RE.finditer(wikitext))
    if template_names != _EXPECTED_TEMPLATE_INVENTORY:
        raise ValueError(f"Beketova template inventory drift: {template_names!r}")

    tag_names = tuple(match.group(1).lower() for match in _HTML_TAG_RE.finditer(wikitext))
    if tag_names != ("center",) * _EXPECTED_CENTER_TAG_COUNT:
        raise ValueError(f"Beketova HTML tag inventory drift: {tag_names!r}")

    category_lines = [index for index, line in enumerate(lines, start=1) if _CATEGORY_LINE_RE.fullmatch(line.strip())]
    expected_categories = list(range(_EXPECTED_LINE_COUNT - _EXPECTED_CATEGORY_COUNT + 1, _EXPECTED_LINE_COUNT + 1))
    if category_lines != expected_categories:
        raise ValueError(f"Beketova category boundary drift: {category_lines!r}")

    literary_lines = lines[_BODY_START_LINE - 1 : -_EXPECTED_CATEGORY_COUNT]
    if not literary_lines:
        raise ValueError("empty Beketova literary body")

    heading_levels: list[int] = []
    for line in literary_lines:
        match = _HEADING_RE.fullmatch(line)
        if match:
            heading_levels.append(len(match.group(1)))
    if heading_levels.count(3) != _EXPECTED_PART_HEADING_COUNT:
        raise ValueError("Beketova part-heading inventory drift")
    if heading_levels.count(4) != _EXPECTED_CHAPTER_HEADING_COUNT:
        raise ValueError("Beketova chapter-heading inventory drift")
    if len(heading_levels) != _EXPECTED_PART_HEADING_COUNT + _EXPECTED_CHAPTER_HEADING_COUNT:
        raise ValueError("unsupported Beketova heading level or shape")

    body_source = "\n".join(literary_lines)
    if "{{" in body_source or "}}" in body_source:
        raise ValueError("unsupported template inside Beketova literary body")
    if _HTML_TAG_RE.search(body_source):
        raise ValueError("unsupported HTML tag inside Beketova literary body")
    if _EXTERNAL_LINK_RE.search(body_source):
        raise ValueError("unsupported external link inside Beketova literary body")
    if any(_TABLE_MARKER_RE.match(line) for line in literary_lines):
        raise ValueError("unsupported table markup inside Beketova literary body")
    return lines, literary_lines


def _render_heading(line: str) -> str:
    match = _HEADING_RE.fullmatch(line)
    if not match:
        return line
    value = match.group(2).strip()
    if not value:
        raise ValueError("empty Beketova literary heading")
    if any(marker in value for marker in ("{{", "}}", "[[", "]]", "<", ">")):
        raise ValueError("unsupported markup inside Beketova literary heading")
    return value


def extract_literary_body(wikitext: str) -> str:
    """Extract the exact observed direct-transcription body, failing closed."""

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    _, literary_lines = _validate_source_shape(wikitext)
    rendered = "\n".join(_render_heading(line) for line in literary_lines)
    return extract_transcription_body(f'<div class="text">{rendered}</div>')


def _validate_revision_target(revision_manifest: Mapping[str, object]) -> None:
    validate_revision_manifest(revision_manifest)
    if revision_manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Beketova candidate id")
    identity = revision_manifest.get("source_identity")
    if not isinstance(identity, dict):
        raise ValueError("Beketova revision identity missing")
    if identity.get("title") != TITLE or identity.get("revision_id") != REVISION_ID:
        raise ValueError("revision manifest does not identify the frozen Beketova revision")


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
        raise ValueError("unexpected Beketova body candidate")
    source_revision = body_manifest.get("source_revision")
    if not isinstance(source_revision, dict):
        raise ValueError("Beketova body source revision missing")
    if source_revision.get("title") != TITLE or source_revision.get("revision_id") != REVISION_ID:
        raise ValueError("Beketova body source revision drift")
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
    parser = argparse.ArgumentParser(description="Freeze or replay the Beketova Captain Grant literary body.")
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
