"""Freeze and replay the Russian Wikisource Brothers Karamazov candidate.

The durable manifest is source-free. Capture transiently reads current Russian
Wikisource wikitext, records exact revision identities, extracts the public-domain
transcription under a versioned source-specific contract, and stores only immutable
identities plus composite hashes. Replay fetches only those pinned revisions and must
reproduce the same composite identity.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import html
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, Sequence

from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import (
    COMPOSITE_PROFILE,
    extract_transcription_body,
    fetch_current_chapter_revisions,
    roman,
)
from .wikisource_replay import fetch_pinned_chapter_revisions


CANDIDATE_ID = "dostoevsky-brothers-karamazov-ru"
WORK_BASE_TITLE = "Братья Карамазовы (Достоевский)"
BOOK_NAMES = (
    "Книга первая",
    "Книга вторая",
    "Книга третья",
    "Книга четвёртая",
    "Книга пятая",
    "Книга шестая",
    "Книга седьмая",
    "Книга восьмая",
    "Книга девятая",
    "Книга десятая",
    "Книга одиннадцатая",
    "Книга двенадцатая",
)
BOOK_CHAPTER_COUNTS = (5, 8, 11, 7, 7, 3, 4, 8, 9, 7, 10, 14)
EPILOGUE_CHAPTER_COUNT = 3
SOURCE_SEGMENT_COUNT = 98
CAPTURE_BATCH_SIZE = 8
MANIFEST_VERSION = "scriptorium-karamazov-source-revision-packed-manifest-v1"
EXTRACTION_PROFILE = "scriptorium-wikisource-karamazov-body-v3"
SOURCE_WORK_URL = "https://ru.wikisource.org/wiki/Братья_Карамазовы_(Достоевский)"
SOURCE_WORK_INDEX_REVISION_ID = 5616907
BIBLIOGRAPHIC_SOURCE = (
    "Достоевский Ф. М. Собрание сочинений: в 15 т. Л.: Наука, 1991. Т. 9-10."
)

_BODY_DIV_RE = re.compile(
    r'<div\b(?=[^>]*\bclass=["\'](?:text|indent)["\'])[^>]*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
_ONLYINCLUDE_RE = re.compile(r"<onlyinclude>(.*?)</onlyinclude>", re.IGNORECASE | re.DOTALL)
_NOINCLUDE_RE = re.compile(r"<noinclude>.*?</noinclude>", re.IGNORECASE | re.DOTALL)
_HEADING_RE = re.compile(r"={2,6}\s*[^=\n]+?\s*={2,6}")
_CENTER_RE = re.compile(r"<center>.*?</center>", re.IGNORECASE | re.DOTALL)
_CATEGORY_RE = re.compile(r"\[\[Категория:[^\]]+\]\]\s*$", re.IGNORECASE | re.DOTALL)
_RIGHT_RE = re.compile(r"\{\{right\|(?P<text>.*?)\}\}", re.IGNORECASE | re.DOTALL)
_EPIGRAPH_RE = re.compile(
    r"\{\{эпиграф2\|(?P<quote>.*?)\|(?P<source>.*?)\|(?P<width>[^{}|]*)\}\}",
    re.IGNORECASE | re.DOTALL,
)
_WIKILINK_RE = re.compile(r"\[\[(?:[^\[\]|]+\|)?([^\[\]]+)\]\]")
_FORMATTING_RE = re.compile(r"'{2,5}")
_POEM_TAG_RE = re.compile(r"<poem\b[^>]*>\s*(.*?)\s*</poem>", re.IGNORECASE | re.DOTALL)
_EDITOR_NOTE_START_RE = re.compile(
    r"\{\{\s*(?:примечание\s+вт|примечания\s+вт)(?=\s*[|}])",
    re.IGNORECASE,
)
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def expected_segments() -> tuple[dict[str, object], ...]:
    """Return the exact 98-segment text-bearing inventory in composition order."""

    segments: list[dict[str, object]] = [
        {"ordinal": 1, "kind": "front_matter", "title": WORK_BASE_TITLE},
        {"ordinal": 2, "kind": "author_preface", "title": f"{WORK_BASE_TITLE}/От автора"},
    ]
    ordinal = 2
    for book_index, (book_name, count) in enumerate(
        zip(BOOK_NAMES, BOOK_CHAPTER_COUNTS, strict=True), start=1
    ):
        for chapter in range(1, count + 1):
            ordinal += 1
            segments.append(
                {
                    "ordinal": ordinal,
                    "kind": "book_chapter",
                    "book": book_index,
                    "chapter": chapter,
                    "title": f"{WORK_BASE_TITLE}/{book_name}/{roman(chapter)}",
                }
            )
    for chapter in range(1, EPILOGUE_CHAPTER_COUNT + 1):
        ordinal += 1
        segments.append(
            {
                "ordinal": ordinal,
                "kind": "epilogue_chapter",
                "chapter": chapter,
                "title": f"{WORK_BASE_TITLE}/Эпилог/{roman(chapter)}",
            }
        )
    if ordinal != SOURCE_SEGMENT_COUNT:
        raise AssertionError(
            f"source inventory drift: expected {SOURCE_SEGMENT_COUNT}, got {ordinal}"
        )
    return tuple(segments)


def fetch_current_segment_revisions(
    segments: Iterable[dict[str, object]],
) -> dict[str, dict[str, object]]:
    """Fetch current identities in small batches to keep long Cyrillic URLs bounded."""

    expected = tuple(segments)
    records: dict[str, dict[str, object]] = {}
    for offset in range(0, len(expected), CAPTURE_BATCH_SIZE):
        batch = expected[offset : offset + CAPTURE_BATCH_SIZE]
        fetched = fetch_current_chapter_revisions(batch)
        overlap = set(records).intersection(fetched)
        if overlap:
            raise ValueError(f"duplicate source-segment responses: {sorted(overlap)!r}")
        records.update(fetched)
    expected_titles = {str(segment["title"]) for segment in expected}
    if set(records) != expected_titles:
        missing = sorted(expected_titles - set(records))
        extra = sorted(set(records) - expected_titles)
        raise ValueError(f"source inventory mismatch; missing={missing!r} extra={extra!r}")
    return records


def _strip_leading_template(source: str, name: str) -> str:
    """Remove one leading MediaWiki template while respecting nested templates."""

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


def _split_template_parts(inner: str) -> list[str]:
    """Split a template invocation on top-level pipes only."""

    parts: list[str] = []
    buffer: list[str] = []
    template_depth = 0
    link_depth = 0
    index = 0
    while index < len(inner):
        pair = inner[index : index + 2]
        if pair == "{{":
            template_depth += 1
            buffer.append(pair)
            index += 2
            continue
        if pair == "}}":
            template_depth -= 1
            if template_depth < 0:
                raise ValueError("unbalanced nested template")
            buffer.append(pair)
            index += 2
            continue
        if pair == "[[":
            link_depth += 1
            buffer.append(pair)
            index += 2
            continue
        if pair == "]]":
            link_depth -= 1
            if link_depth < 0:
                raise ValueError("unbalanced wikilink")
            buffer.append(pair)
            index += 2
            continue
        if inner[index] == "|" and template_depth == 0 and link_depth == 0:
            parts.append("".join(buffer))
            buffer = []
            index += 1
            continue
        buffer.append(inner[index])
        index += 1
    if template_depth or link_depth:
        raise ValueError("unbalanced nested markup")
    parts.append("".join(buffer))
    return parts


def _find_balanced_template_end(source: str, start: int) -> int:
    depth = 0
    index = start
    while index < len(source) - 1:
        pair = source[index : index + 2]
        if pair == "{{":
            depth += 1
            index += 2
            continue
        if pair == "}}":
            depth -= 1
            index += 2
            if depth == 0:
                return index
            if depth < 0:
                break
            continue
        index += 1
    raise ValueError("unterminated balanced template")


def _strip_wikisource_editor_notes(source: str) -> str:
    """Remove Wikisource-editor notes, which are explicitly not literary source text.

    Russian Wikisource documents ``Примечание ВТ`` / ``Примечания ВТ`` as a paired
    facility for comments made by Wikisource contributors, visually separated from
    authorial notes. The full balanced invocation is removed so nested formatting or
    language templates inside an editor comment cannot leak into the literary composite.
    """

    output: list[str] = []
    cursor = 0
    while True:
        match = _EDITOR_NOTE_START_RE.search(source, cursor)
        if match is None:
            output.append(source[cursor:])
            return "".join(output)
        output.append(source[cursor : match.start()])
        end = _find_balanced_template_end(source, match.start())
        raw = source[match.start() : end]
        parts = _split_template_parts(raw[2:-2])
        if not parts:
            raise ValueError("empty Wikisource editor-note template")
        name = re.sub(r"\s+", " ", parts[0].strip()).casefold()
        if name not in {"примечание вт", "примечания вт"}:
            raise ValueError("unexpected template while stripping Wikisource editor note")
        if name == "примечание вт" and len(parts) < 2:
            raise ValueError("Wikisource editor note is missing its note argument")
        output.append("")
        cursor = end


def _unwrap_poem1_templates(source: str) -> str:
    """Replace only the two source-observed Poem1 shapes, fail closed on all others.

    A source-free hosted probe observed eight invocations in Book III chapter III:
    six had ``{{Poem1||<poem>...</poem>|}}`` and two had
    ``{{Poem1||plain text|}}``. Both render the middle positional argument. This parser
    accepts exactly that three-argument blank/middle/blank contract and refuses nested
    templates or malformed poem tags.
    """

    output: list[str] = []
    cursor = 0
    start_re = re.compile(r"\{\{\s*poem1\b", re.IGNORECASE)
    while True:
        match = start_re.search(source, cursor)
        if match is None:
            output.append(source[cursor:])
            return "".join(output)
        output.append(source[cursor : match.start()])
        end = _find_balanced_template_end(source, match.start())
        raw = source[match.start() : end]
        parts = _split_template_parts(raw[2:-2])
        if not parts or parts[0].strip().casefold() != "poem1":
            raise ValueError("unexpected template while unwrapping Poem1")
        args = parts[1:]
        if len(args) != 3 or args[0].strip() or args[2].strip():
            raise ValueError("unsupported Poem1 argument shape")
        middle = args[1].strip()
        if not middle:
            raise ValueError("empty Poem1 text argument")
        if "{{" in middle or "}}" in middle:
            raise ValueError("nested template inside Poem1 text is unsupported")

        poem = _POEM_TAG_RE.fullmatch(middle)
        if poem is not None:
            replacement = poem.group(1).strip()
        elif re.search(r"</?poem\b", middle, re.IGNORECASE):
            raise ValueError("malformed Poem1 poem-tag shape")
        else:
            replacement = middle
        if not replacement:
            raise ValueError("empty rendered Poem1 text")
        output.append(replacement)
        cursor = end


def _plain_inline(value: str) -> str:
    value = _WIKILINK_RE.sub(lambda match: match.group(1), value)
    value = _FORMATTING_RE.sub("", value)
    value = html.unescape(value)
    return re.sub(r"[ \t]*\n[ \t]*", " ", value).strip()


def extract_index_front_matter(wikitext: str) -> str:
    """Extract only the authorial dedication and epigraph from the work index."""

    source = _NOINCLUDE_RE.sub("", wikitext)
    source = _strip_leading_template(source, "Отексте")
    source = source.replace("__NOEDITSECTION__", "", 1).lstrip()
    toc_match = re.search(r"={2,6}\s*Оглавление\s*={2,6}", source, re.IGNORECASE)
    if toc_match is None:
        raise ValueError("Karamazov work index missing Оглавление boundary")
    front = source[: toc_match.start()].strip()
    right = _RIGHT_RE.fullmatch(front.splitlines()[0].strip()) if front else None
    epigraph = _EPIGRAPH_RE.search(front)
    if right is None or epigraph is None:
        raise ValueError("unexpected Karamazov index front-matter shape")

    remainder = _RIGHT_RE.sub("", front, count=1)
    remainder = _EPIGRAPH_RE.sub("", remainder, count=1)
    if remainder.strip():
        raise ValueError("unsupported content in Karamazov index front matter")

    dedication = _plain_inline(right.group("text"))
    quote_text = _plain_inline(epigraph.group("quote"))
    source_text = _plain_inline(epigraph.group("source"))
    if not dedication or not quote_text or not source_text:
        raise ValueError("empty Karamazov index front-matter component")
    return "\n\n".join((dedication, quote_text, source_text))


def _strip_page_scaffolding(wikitext: str) -> str:
    source = _NOINCLUDE_RE.sub("", wikitext)
    source = _strip_leading_template(source, "Отексте")
    source = source.replace("__NOTOC__", "").replace("__NOEDITSECTION__", "")
    source = _CENTER_RE.sub("", source)
    source = _HEADING_RE.sub("", source)
    source = _CATEGORY_RE.sub("", source)
    return source.strip()


def extract_karamazov_body(wikitext: str, *, kind: str) -> str:
    """Extract one admitted segment under the observed Karamazov page-shape contract."""

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    if kind == "front_matter":
        return extract_index_front_matter(wikitext)

    source = _NOINCLUDE_RE.sub("", wikitext)
    source = _strip_wikisource_editor_notes(source)
    source = _unwrap_poem1_templates(source)

    onlyinclude = _ONLYINCLUDE_RE.findall(source)
    if onlyinclude:
        if len(onlyinclude) != 1:
            raise ValueError(f"expected one onlyinclude body, got {len(onlyinclude)}")
        return extract_transcription_body(f'<div class="text">{onlyinclude[0]}</div>')

    divs = _BODY_DIV_RE.findall(source)
    if divs:
        rendered = [
            extract_transcription_body(f'<div class="text">{fragment}</div>')
            for fragment in divs
        ]
        return "\n\n".join(rendered)

    plain = _strip_page_scaffolding(source)
    if not plain:
        raise ValueError("empty Karamazov transcription after page-scaffolding removal")
    return extract_transcription_body(f'<div class="text">{plain}</div>')


def _composite_identity(composite: str) -> dict[str, object]:
    normalized = normalize_text(composite)
    raw = composite.encode("utf-8")
    return {
        "source_segment_count": SOURCE_SEGMENT_COUNT,
        "character_count_including_spaces": len(composite),
        "utf8_byte_count": len(raw),
        "raw_sha256": sha256(raw).hexdigest(),
        "normalization_profile": NORMALIZATION_PROFILE,
        "normalized_character_count_including_spaces": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }


def build_manifest(
    *,
    fetcher: Callable[
        [Iterable[dict[str, object]]], dict[str, dict[str, object]]
    ] = fetch_current_segment_revisions,
) -> dict[str, object]:
    """Capture source identities and composite hashes without serializing source prose."""

    segments = expected_segments()
    revisions = fetcher(segments)
    revision_ids: list[int] = []
    revision_timestamps: list[str] = []
    mediawiki_sha1s: list[str] = []
    bodies: list[str] = []
    seen_revision_ids: set[int] = set()

    for segment in segments:
        title = str(segment["title"])
        revision = revisions[title]
        revision_id = int(revision["revision_id"])
        if revision_id <= 0 or revision_id in seen_revision_ids:
            raise ValueError(f"invalid or duplicate revision id {revision_id}")
        if segment["kind"] == "front_matter" and revision_id != SOURCE_WORK_INDEX_REVISION_ID:
            raise ValueError(
                "work-index revision drift: "
                f"observed {revision_id}, expected {SOURCE_WORK_INDEX_REVISION_ID}"
            )
        seen_revision_ids.add(revision_id)
        timestamp = str(revision["timestamp"])
        mediawiki_sha1 = str(revision["mediawiki_sha1"]).lower()
        if not _HEX40_RE.fullmatch(mediawiki_sha1):
            raise ValueError(f"invalid MediaWiki SHA-1 for {title!r}")
        try:
            body = extract_karamazov_body(
                str(revision["wikitext"]), kind=str(segment["kind"])
            )
        except ValueError as exc:
            raise ValueError(f"failed to extract {title!r}: {exc}") from exc

        revision_ids.append(revision_id)
        revision_timestamps.append(timestamp)
        mediawiki_sha1s.append(mediawiki_sha1)
        bodies.append(body)

    composite = "\n\n".join(bodies)
    if len(composite) < 300_000:
        raise ValueError(f"composite below corpus threshold: {len(composite)} characters")

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_work_url": SOURCE_WORK_URL,
        "source_work_index_revision_id": SOURCE_WORK_INDEX_REVISION_ID,
        "bibliographic_source": BIBLIOGRAPHIC_SOURCE,
        "legal_basis": "public_domain",
        "composition": {
            "profile": COMPOSITE_PROFILE,
            "extraction_profile": EXTRACTION_PROFILE,
            "order": (
                "work-index authorial front matter, author preface, books 1-12 in order "
                "with chapters ascending, then epilogue chapters I-III"
            ),
            "segment_separator": "\\n\\n",
            "source_text_committed": False,
            "front_matter_segments": 1,
            "author_preface_segments": 1,
            "book_chapter_counts": list(BOOK_CHAPTER_COUNTS),
            "epilogue_chapter_count": EPILOGUE_CHAPTER_COUNT,
            "navigation_wrappers_included": False,
            "wikisource_editor_notes_included": False,
        },
        "source_identity_encoding": {
            "source_segment_count": len(segments),
            "titles": "deterministic_from_karamazov_inventory_contract",
            "revision_ids": revision_ids,
            "revision_timestamps": revision_timestamps,
            "mediawiki_sha1_hex_concat": "".join(mediawiki_sha1s),
        },
        "composite_identity": _composite_identity(composite),
    }


def _validate_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Karamazov revision-manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Karamazov candidate id")
    if manifest.get("source_work_index_revision_id") != SOURCE_WORK_INDEX_REVISION_ID:
        raise ValueError("Karamazov work-index revision drift")
    if manifest.get("legal_basis") != "public_domain":
        raise ValueError("Karamazov legal-basis drift")

    composition = manifest.get("composition")
    if not isinstance(composition, dict):
        raise ValueError("revision manifest missing composition")
    if composition.get("profile") != COMPOSITE_PROFILE:
        raise ValueError("unexpected composite profile")
    if composition.get("extraction_profile") != EXTRACTION_PROFILE:
        raise ValueError("unexpected extraction profile")
    if composition.get("book_chapter_counts") != list(BOOK_CHAPTER_COUNTS):
        raise ValueError("Karamazov book/chapter contract drift")
    if composition.get("epilogue_chapter_count") != EPILOGUE_CHAPTER_COUNT:
        raise ValueError("Karamazov epilogue contract drift")
    if composition.get("front_matter_segments") != 1:
        raise ValueError("Karamazov front-matter contract drift")
    if composition.get("author_preface_segments") != 1:
        raise ValueError("Karamazov author-preface contract drift")
    if composition.get("segment_separator") != "\\n\\n":
        raise ValueError("unexpected segment separator")
    if composition.get("navigation_wrappers_included") is not False:
        raise ValueError("navigation-wrapper boundary drift")
    if composition.get("wikisource_editor_notes_included") is not False:
        raise ValueError("Wikisource editor-note boundary drift")
    if composition.get("source_text_committed") is not False:
        raise ValueError("source-text boundary drift")

    segments = expected_segments()
    encoding = manifest.get("source_identity_encoding")
    if not isinstance(encoding, dict):
        raise ValueError("revision manifest missing source_identity_encoding")
    count = len(segments)
    if encoding.get("source_segment_count") != count:
        raise ValueError("packed source-segment count drift")
    if encoding.get("titles") != "deterministic_from_karamazov_inventory_contract":
        raise ValueError("packed title encoding drift")

    revision_ids = encoding.get("revision_ids")
    timestamps = encoding.get("revision_timestamps")
    sha_concat = encoding.get("mediawiki_sha1_hex_concat")
    if not isinstance(revision_ids, list) or len(revision_ids) != count:
        raise ValueError("invalid packed revision_ids")
    if not isinstance(timestamps, list) or len(timestamps) != count:
        raise ValueError("invalid packed revision_timestamps")
    if not isinstance(sha_concat, str) or len(sha_concat) != count * 40:
        raise ValueError("invalid packed mediawiki_sha1 length")
    if not re.fullmatch(r"[0-9a-f]+", sha_concat):
        raise ValueError("invalid packed mediawiki_sha1 hex")

    seen_revision_ids: set[int] = set()
    identities: list[dict[str, object]] = []
    for index, segment in enumerate(segments):
        revision_id = revision_ids[index]
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError("invalid packed revision id")
        if revision_id in seen_revision_ids:
            raise ValueError(f"duplicate revision id {revision_id}")
        if index == 0 and revision_id != SOURCE_WORK_INDEX_REVISION_ID:
            raise ValueError("packed work-index revision drift")
        seen_revision_ids.add(revision_id)

        timestamp = timestamps[index]
        if not isinstance(timestamp, str) or not timestamp:
            raise ValueError("invalid packed revision timestamp")
        mediawiki_sha1 = sha_concat[index * 40 : (index + 1) * 40]
        identities.append(
            {
                "title": segment["title"],
                "kind": segment["kind"],
                "revision_id": revision_id,
                "revision_timestamp": timestamp,
                "mediawiki_sha1": mediawiki_sha1,
            }
        )

    composite = manifest.get("composite_identity")
    if not isinstance(composite, dict):
        raise ValueError("revision manifest missing composite_identity")
    if composite.get("source_segment_count") != count:
        raise ValueError("composite source-segment count drift")
    if composite.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError("unexpected normalization profile")
    for key in (
        "character_count_including_spaces",
        "normalized_character_count_including_spaces",
        "utf8_byte_count",
    ):
        value = composite.get(key)
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"invalid composite {key}")
    if int(composite["character_count_including_spaces"]) < 300_000:
        raise ValueError("frozen candidate fell below corpus threshold")
    for key in ("raw_sha256", "normalized_sha256"):
        value = composite.get(key)
        if not isinstance(value, str) or not _HEX64_RE.fullmatch(value):
            raise ValueError(f"invalid composite {key}")

    return tuple(identities)


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[
        [Iterable[Mapping[str, object]]], dict[str, str]
    ] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Replay exact revisions and return only source-free verification evidence."""

    identities = _validate_manifest(manifest)
    revisions = fetcher(identities)
    bodies = [
        extract_karamazov_body(
            revisions[str(identity["title"])], kind=str(identity["kind"])
        )
        for identity in identities
    ]
    observed = _composite_identity("\n\n".join(bodies))
    expected = manifest["composite_identity"]
    assert isinstance(expected, dict)
    for key, value in observed.items():
        if expected.get(key) != value:
            raise ValueError(
                f"frozen composite identity drift for {key}: "
                f"observed {value!r}, expected {expected.get(key)!r}"
            )

    return {
        "receipt_version": "scriptorium-karamazov-replay-receipt-v1",
        "candidate_id": CANDIDATE_ID,
        "source_segment_count": len(identities),
        "composite_identity": observed,
        "source_text_included": False,
        "diagnostic_comparison_admissible": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser(
        "capture", help="capture current source-free revision manifest"
    )
    capture.add_argument("--output", type=Path, required=True)

    replay = subparsers.add_parser("replay", help="replay an existing pinned manifest")
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)

    args = parser.parse_args(argv)
    if args.command == "capture":
        _write_json(args.output, build_manifest())
        return 0

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("revision manifest must be a JSON object")
    _write_json(args.receipt, replay_manifest(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
