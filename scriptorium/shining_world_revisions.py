"""Audit and replay Grin's *Shining World* Wikisource chapter inventory.

The reviewed work index advertises a three-part / 34-chapter structure, but an
exact source probe may reveal red links. This module records that distinction
fail-closed: present chapter revisions are frozen source-free, missing advertised
chapter titles are recorded explicitly, and no literary prose is serialized.
Literary-body extraction/composition remains separate follow-up work.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, Sequence

from .wikisource_freeze import _api_query, roman
from .wikisource_replay import fetch_pinned_chapter_revisions


CANDIDATE_ID = "grin-shining-world-ru"
WORK_BASE_TITLE = "Блистающий мир (Грин)"
PART_CHAPTER_COUNTS = (16, 11, 7)
MANIFEST_VERSION = "scriptorium-shining-world-source-inventory-v1"
SOURCE_WORK_URL = "https://ru.wikisource.org/wiki/Блистающий_мир_(Грин)"
SOURCE_WORK_INDEX_REVISION_ID = 4_186_047
BIBLIOGRAPHIC_SOURCE = (
    "А. С. Грин. Собрание сочинений в шести томах. — М.: Правда, 1965. "
    "— Т. 3. — С. 66–214."
)
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def expected_chapters() -> tuple[dict[str, object], ...]:
    """Return the ordered 34 chapter titles advertised by the reviewed index."""

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


def fetch_chapter_inventory(
    chapters: Iterable[dict[str, object]],
    *,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, dict[str, object]]:
    """Probe advertised chapter titles without requesting or returning source prose."""

    expected = tuple(chapters)
    records: dict[str, dict[str, object]] = {}
    for offset in range(0, len(expected), 40):
        batch = expected[offset : offset + 40]
        titles = [str(chapter["title"]) for chapter in batch]
        payload = query(
            {
                "action": "query",
                "prop": "revisions",
                "titles": "|".join(titles),
                "rvprop": "ids|timestamp|sha1",
                "redirects": "0",
            }
        )
        query_obj = payload.get("query")
        if not isinstance(query_obj, dict):
            raise ValueError("MediaWiki response missing query")
        pages = query_obj.get("pages")
        if not isinstance(pages, list):
            raise ValueError("MediaWiki response missing pages")
        for page in pages:
            if not isinstance(page, dict):
                raise ValueError("unexpected page object")
            title = page.get("title")
            if not isinstance(title, str) or title not in titles:
                raise ValueError(f"unexpected chapter title from MediaWiki: {title!r}")
            if title in records:
                raise ValueError(f"duplicate chapter response: {title}")
            if page.get("missing") is True:
                records[title] = {"status": "missing"}
                continue
            revisions = page.get("revisions")
            if not isinstance(revisions, list) or len(revisions) != 1:
                raise ValueError(f"expected one current revision for {title}")
            revision = revisions[0]
            if not isinstance(revision, dict):
                raise ValueError(f"unexpected revision object for {title!r}")
            revid = revision.get("revid")
            timestamp = revision.get("timestamp")
            mediawiki_sha1 = revision.get("sha1")
            if not isinstance(revid, int) or revid <= 0:
                raise ValueError(f"invalid revision id for {title!r}")
            timestamp = _validate_timestamp(timestamp)
            if not isinstance(mediawiki_sha1, str):
                raise ValueError(f"missing MediaWiki SHA-1 for {title!r}")
            mediawiki_sha1 = mediawiki_sha1.lower()
            if not _HEX40_RE.fullmatch(mediawiki_sha1):
                raise ValueError(f"invalid MediaWiki SHA-1 for {title!r}")
            records[title] = {
                "status": "present",
                "revision_id": revid,
                "revision_timestamp": timestamp,
                "mediawiki_sha1": mediawiki_sha1,
            }

    expected_titles = {str(chapter["title"]) for chapter in expected}
    if set(records) != expected_titles:
        missing = sorted(expected_titles - set(records))
        extra = sorted(set(records) - expected_titles)
        raise ValueError(f"chapter query inventory mismatch; missing={missing!r} extra={extra!r}")
    return records


def build_manifest(
    *,
    fetcher: Callable[
        [Iterable[dict[str, object]]], dict[str, dict[str, object]]
    ] = fetch_chapter_inventory,
) -> dict[str, object]:
    """Audit advertised titles and freeze identities for every page that exists."""

    chapters = expected_chapters()
    observed = fetcher(chapters)
    expected_titles = {str(row["title"]) for row in chapters}
    if set(observed) != expected_titles:
        missing = sorted(expected_titles - set(observed))
        extra = sorted(set(observed) - expected_titles)
        raise ValueError(f"chapter inventory mismatch; missing={missing!r} extra={extra!r}")

    rows: list[dict[str, object]] = []
    seen_revision_ids: set[int] = set()
    missing_titles: list[str] = []
    for chapter in chapters:
        title = str(chapter["title"])
        record = observed[title]
        status = record.get("status")
        if status == "missing":
            rows.append({**chapter, "status": "missing"})
            missing_titles.append(title)
            continue
        if status != "present":
            raise ValueError(f"invalid inventory status for {title!r}: {status!r}")
        revision_id = record.get("revision_id")
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError(f"invalid revision id for {title!r}")
        if revision_id in seen_revision_ids:
            raise ValueError(f"duplicate revision id {revision_id}")
        seen_revision_ids.add(revision_id)
        timestamp = _validate_timestamp(record.get("revision_timestamp"))
        mediawiki_sha1 = record.get("mediawiki_sha1")
        if not isinstance(mediawiki_sha1, str):
            raise ValueError(f"missing MediaWiki SHA-1 for {title!r}")
        mediawiki_sha1 = mediawiki_sha1.lower()
        if not _HEX40_RE.fullmatch(mediawiki_sha1):
            raise ValueError(f"invalid MediaWiki SHA-1 for {title!r}")
        rows.append(
            {
                **chapter,
                "status": "present",
                "revision_id": revision_id,
                "revision_timestamp": timestamp,
                "mediawiki_sha1": mediawiki_sha1,
            }
        )

    present_count = len(rows) - len(missing_titles)
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_work_url": SOURCE_WORK_URL,
        "source_work_index_revision_id": SOURCE_WORK_INDEX_REVISION_ID,
        "bibliographic_source": BIBLIOGRAPHIC_SOURCE,
        "legal_basis": "public_domain_original_work_with_wikisource_reuse_terms",
        "capture_scope": {
            "chapter_navigation_inventory_audited": True,
            "complete_chapter_revision_inventory_frozen": not missing_titles,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "source_text_committed": False,
        },
        "composition_contract": {
            "parts": len(PART_CHAPTER_COUNTS),
            "part_chapter_counts": list(PART_CHAPTER_COUNTS),
            "order": "part ascending then chapter ascending",
        },
        "inventory_summary": {
            "advertised_chapter_count": len(chapters),
            "present_chapter_count": present_count,
            "missing_chapter_count": len(missing_titles),
            "missing_titles": missing_titles,
        },
        "chapters": rows,
    }


def validate_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    """Validate an inventory manifest and return only its frozen present identities."""

    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Shining World source-inventory version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Shining World candidate id")
    if manifest.get("source_work_index_revision_id") != SOURCE_WORK_INDEX_REVISION_ID:
        raise ValueError("work-index revision drift")

    composition = manifest.get("composition_contract")
    if not isinstance(composition, dict):
        raise ValueError("inventory manifest missing composition contract")
    if composition.get("parts") != 3:
        raise ValueError("part-count contract drift")
    if composition.get("part_chapter_counts") != list(PART_CHAPTER_COUNTS):
        raise ValueError("chapter-count contract drift")
    if composition.get("order") != "part ascending then chapter ascending":
        raise ValueError("chapter-order contract drift")

    expected = expected_chapters()
    rows = manifest.get("chapters")
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise ValueError("inventory manifest must contain exactly 34 advertised chapters")

    identities: list[dict[str, object]] = []
    missing_titles: list[str] = []
    seen_revision_ids: set[int] = set()
    for chapter, row in zip(expected, rows, strict=True):
        if not isinstance(row, dict):
            raise ValueError("chapter inventory rows must be objects")
        for key in ("ordinal", "part", "chapter", "title"):
            if row.get(key) != chapter[key]:
                raise ValueError(
                    f"chapter identity drift at ordinal {chapter['ordinal']}: {key}"
                )
        status = row.get("status")
        if status == "missing":
            forbidden = {"revision_id", "revision_timestamp", "mediawiki_sha1"}
            if forbidden.intersection(row):
                raise ValueError(f"missing chapter has revision identity: {chapter['title']!r}")
            missing_titles.append(str(chapter["title"]))
            continue
        if status != "present":
            raise ValueError(f"invalid inventory status for {chapter['title']!r}")
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

    summary = manifest.get("inventory_summary")
    if not isinstance(summary, dict):
        raise ValueError("inventory manifest missing summary")
    if summary.get("advertised_chapter_count") != 34:
        raise ValueError("advertised chapter-count drift")
    if summary.get("present_chapter_count") != len(identities):
        raise ValueError("present chapter-count drift")
    if summary.get("missing_chapter_count") != len(missing_titles):
        raise ValueError("missing chapter-count drift")
    if summary.get("missing_titles") != missing_titles:
        raise ValueError("missing chapter-title inventory drift")

    scope = manifest.get("capture_scope")
    expected_scope = {
        "chapter_navigation_inventory_audited": True,
        "complete_chapter_revision_inventory_frozen": not missing_titles,
        "literary_body_extraction_frozen": False,
        "composite_identity_frozen": False,
        "source_text_committed": False,
    }
    if scope != expected_scope:
        raise ValueError("source-inventory capture scope drift")
    return tuple(identities)


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = (
        fetch_pinned_chapter_revisions
    ),
) -> dict[str, object]:
    """Re-fetch exact present revisions; missing advertised titles remain explicit gaps."""

    identities = validate_manifest(manifest)
    fetched = fetcher(identities)
    expected_titles = {str(row["title"]) for row in identities}
    if set(fetched) != expected_titles:
        missing = sorted(expected_titles - set(fetched))
        extra = sorted(set(fetched) - expected_titles)
        raise ValueError(f"pinned chapter inventory mismatch; missing={missing!r} extra={extra!r}")
    summary = manifest["inventory_summary"]
    assert isinstance(summary, dict)
    return {
        "verified": True,
        "candidate_id": CANDIDATE_ID,
        "verified_present_chapter_count": len(identities),
        "missing_advertised_chapter_count": summary["missing_chapter_count"],
        "complete_chapter_revision_inventory_frozen": False if summary["missing_chapter_count"] else True,
        "source_text_committed": False,
    }


def canonical_json_text(value: Mapping[str, object]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit/replay Shining World chapter identities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser("capture", help="audit advertised chapter identities")
    capture.add_argument("--output", type=Path, required=True)

    replay = subparsers.add_parser("replay", help="verify present pinned identities")
    replay.add_argument("--manifest", type=Path, required=True)

    args = parser.parse_args(argv)
    if args.command == "capture":
        manifest = build_manifest()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(canonical_json_text(manifest), encoding="utf-8")
        return 0

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("inventory manifest must be a JSON object")
    replay_manifest(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
