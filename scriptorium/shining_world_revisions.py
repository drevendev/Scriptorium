"""Freeze and replay the source identity of Grin's *Shining World* chapters.

This module deliberately persists only source-free revision metadata. It fetches
chapter wikitext transiently because MediaWiki returns content together with the
revision identity, but no literary prose is serialized. Literary-body extraction
and composite identity are separate follow-up work.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, Sequence

from .wikisource_freeze import fetch_current_chapter_revisions, roman
from .wikisource_replay import fetch_pinned_chapter_revisions


CANDIDATE_ID = "grin-shining-world-ru"
WORK_BASE_TITLE = "Блистающий мир (Грин)"
PART_CHAPTER_COUNTS = (16, 11, 7)
MANIFEST_VERSION = "scriptorium-shining-world-source-revision-manifest-v1"
SOURCE_WORK_URL = "https://ru.wikisource.org/wiki/Блистающий_мир_(Грин)"
SOURCE_WORK_INDEX_REVISION_ID = 4_186_047
BIBLIOGRAPHIC_SOURCE = (
    "А. С. Грин. Собрание сочинений в шести томах. — М.: Правда, 1965. "
    "— Т. 3. — С. 66–214."
)
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def expected_chapters() -> tuple[dict[str, object], ...]:
    """Return the ordered three-part / 34-chapter source-title contract."""

    rows: list[dict[str, object]] = []
    ordinal = 0
    for part, count in enumerate(PART_CHAPTER_COUNTS, start=1):
        for chapter in range(1, count + 1):
            ordinal += 1
            rows.append(
                {
                    "ordinal": ordinal,
                    "part": part,
                    "chapter": chapter,
                    "title": (
                        f"{WORK_BASE_TITLE}/Часть {roman(part)}/Глава {roman(chapter)}"
                    ),
                }
            )
    if ordinal != 34:
        raise AssertionError(f"chapter contract drift: expected 34, got {ordinal}")
    return tuple(rows)


def _validate_timestamp(value: object) -> str:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"invalid UTC revision timestamp {value!r}")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"invalid UTC revision timestamp {value!r}") from exc
    if parsed.tzinfo != timezone.utc or parsed.microsecond:
        raise ValueError(f"invalid UTC revision timestamp {value!r}")
    return value


def build_manifest(
    *,
    fetcher: Callable[
        [Iterable[dict[str, object]]], dict[str, dict[str, object]]
    ] = fetch_current_chapter_revisions,
) -> dict[str, object]:
    """Capture current chapter revision identities without serializing prose."""

    chapters = expected_chapters()
    revisions = fetcher(chapters)
    expected_titles = {str(row["title"]) for row in chapters}
    if set(revisions) != expected_titles:
        missing = sorted(expected_titles - set(revisions))
        extra = sorted(set(revisions) - expected_titles)
        raise ValueError(f"chapter inventory mismatch; missing={missing!r} extra={extra!r}")

    identities: list[dict[str, object]] = []
    seen_revision_ids: set[int] = set()
    for chapter in chapters:
        title = str(chapter["title"])
        revision = revisions[title]
        revision_id = revision.get("revision_id")
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError(f"invalid revision id for {title!r}")
        if revision_id in seen_revision_ids:
            raise ValueError(f"duplicate revision id {revision_id}")
        seen_revision_ids.add(revision_id)
        timestamp = _validate_timestamp(revision.get("timestamp"))
        mediawiki_sha1 = revision.get("mediawiki_sha1")
        if not isinstance(mediawiki_sha1, str):
            raise ValueError(f"missing MediaWiki SHA-1 for {title!r}")
        mediawiki_sha1 = mediawiki_sha1.lower()
        if not _HEX40_RE.fullmatch(mediawiki_sha1):
            raise ValueError(f"invalid MediaWiki SHA-1 for {title!r}")
        identities.append(
            {
                **chapter,
                "revision_id": revision_id,
                "revision_timestamp": timestamp,
                "mediawiki_sha1": mediawiki_sha1,
            }
        )

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_work_url": SOURCE_WORK_URL,
        "source_work_index_revision_id": SOURCE_WORK_INDEX_REVISION_ID,
        "bibliographic_source": BIBLIOGRAPHIC_SOURCE,
        "legal_basis": "public_domain_original_work_with_wikisource_reuse_terms",
        "capture_scope": {
            "chapter_revision_inventory_frozen": True,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "source_text_committed": False,
        },
        "composition_contract": {
            "parts": len(PART_CHAPTER_COUNTS),
            "part_chapter_counts": list(PART_CHAPTER_COUNTS),
            "order": "part ascending then chapter ascending",
        },
        "chapters": identities,
    }


def validate_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    """Validate a committed source-free manifest and return its pinned identities."""

    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Shining World revision-manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Shining World candidate id")
    if manifest.get("source_work_index_revision_id") != SOURCE_WORK_INDEX_REVISION_ID:
        raise ValueError("work-index revision drift")

    scope = manifest.get("capture_scope")
    expected_scope = {
        "chapter_revision_inventory_frozen": True,
        "literary_body_extraction_frozen": False,
        "composite_identity_frozen": False,
        "source_text_committed": False,
    }
    if scope != expected_scope:
        raise ValueError("source-identity capture scope drift")

    composition = manifest.get("composition_contract")
    if not isinstance(composition, dict):
        raise ValueError("revision manifest missing composition contract")
    if composition.get("parts") != 3:
        raise ValueError("part-count contract drift")
    if composition.get("part_chapter_counts") != list(PART_CHAPTER_COUNTS):
        raise ValueError("chapter-count contract drift")
    if composition.get("order") != "part ascending then chapter ascending":
        raise ValueError("chapter-order contract drift")

    expected = expected_chapters()
    rows = manifest.get("chapters")
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise ValueError("revision manifest must contain exactly 34 chapters")

    identities: list[dict[str, object]] = []
    seen_revision_ids: set[int] = set()
    for chapter, row in zip(expected, rows, strict=True):
        if not isinstance(row, dict):
            raise ValueError("chapter identity rows must be objects")
        for key in ("ordinal", "part", "chapter", "title"):
            if row.get(key) != chapter[key]:
                raise ValueError(
                    f"chapter identity drift at ordinal {chapter['ordinal']}: {key}"
                )
        revision_id = row.get("revision_id")
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError(f"invalid revision id for {chapter['title']!r}")
        if revision_id in seen_revision_ids:
            raise ValueError(f"duplicate revision id {revision_id}")
        seen_revision_ids.add(revision_id)
        timestamp = _validate_timestamp(row.get("revision_timestamp"))
        mediawiki_sha1 = row.get("mediawiki_sha1")
        if not isinstance(mediawiki_sha1, str) or not _HEX40_RE.fullmatch(mediawiki_sha1):
            raise ValueError(f"invalid MediaWiki SHA-1 for {chapter['title']!r}")
        identities.append(
            {
                **chapter,
                "revision_id": revision_id,
                "revision_timestamp": timestamp,
                "mediawiki_sha1": mediawiki_sha1,
            }
        )
    return tuple(identities)


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = (
        fetch_pinned_chapter_revisions
    ),
) -> dict[str, object]:
    """Re-fetch exact pinned revisions and verify identity without returning prose."""

    identities = validate_manifest(manifest)
    fetched = fetcher(identities)
    expected_titles = {str(row["title"]) for row in identities}
    if set(fetched) != expected_titles:
        missing = sorted(expected_titles - set(fetched))
        extra = sorted(set(fetched) - expected_titles)
        raise ValueError(f"pinned chapter inventory mismatch; missing={missing!r} extra={extra!r}")
    return {
        "verified": True,
        "candidate_id": CANDIDATE_ID,
        "chapter_count": len(identities),
        "source_text_committed": False,
    }


def canonical_json_text(value: Mapping[str, object]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze/replay Shining World revision identities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser("capture", help="capture current chapter identities")
    capture.add_argument("--output", type=Path, required=True)

    replay = subparsers.add_parser("replay", help="verify committed pinned identities")
    replay.add_argument("--manifest", type=Path, required=True)

    args = parser.parse_args(argv)
    if args.command == "capture":
        manifest = build_manifest()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(canonical_json_text(manifest), encoding="utf-8")
        return 0

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("revision manifest must be a JSON object")
    replay_manifest(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
