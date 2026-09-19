"""Capture and replay source-free revision identities for Grin's *Running on Waves*.

This module freezes only the 36 literary subpages in the already retained 1965-source
Russian Wikisource route. It never serializes source prose and deliberately leaves
literary-body extraction/composition for a later unit.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, Sequence

from .running_waves_inventory import (
    CANDIDATE_ID,
    CATEGORY_REVISION_ID,
    PRIMARY_BIBLIOGRAPHIC_SOURCE,
    WORK_INDEX_REVISION_ID,
    WORK_URL,
    expected_literary_titles,
)
from .wikisource_freeze import _api_query
from .wikisource_replay import fetch_pinned_chapter_revisions

MANIFEST_VERSION = "scriptorium-running-waves-source-revisions-v1"
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def expected_pages() -> tuple[dict[str, object], ...]:
    return tuple(
        {"ordinal": ordinal, "title": title}
        for ordinal, title in enumerate(expected_literary_titles(), start=1)
    )


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


def fetch_page_revisions(
    pages: Iterable[dict[str, object]],
    *,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, dict[str, object]]:
    """Fetch current page identities without requesting literary content."""

    expected = tuple(pages)
    records: dict[str, dict[str, object]] = {}
    for offset in range(0, len(expected), 40):
        batch = expected[offset : offset + 40]
        titles = [str(page["title"]) for page in batch]
        payload = query(
            {
                "action": "query",
                "prop": "info|revisions",
                "titles": "|".join(titles),
                "rvprop": "ids|timestamp|sha1",
            }
        )
        query_obj = payload.get("query")
        pages_obj = query_obj.get("pages") if isinstance(query_obj, dict) else None
        if not isinstance(pages_obj, list):
            raise ValueError("MediaWiki response missing pages")
        for page in pages_obj:
            if not isinstance(page, dict):
                raise ValueError("unexpected page object")
            title = page.get("title")
            if not isinstance(title, str) or title not in titles:
                raise ValueError(f"unexpected literary title from MediaWiki: {title!r}")
            if title in records:
                raise ValueError(f"duplicate literary page response: {title}")
            if page.get("missing") is True:
                raise ValueError(f"expected literary page is missing: {title}")
            if page.get("redirect") is True:
                raise ValueError(f"expected literary page became a redirect: {title}")
            page_id = page.get("pageid")
            if not isinstance(page_id, int) or page_id <= 0:
                raise ValueError(f"invalid page id for {title!r}")
            revisions = page.get("revisions")
            if not isinstance(revisions, list) or len(revisions) != 1:
                raise ValueError(f"expected one current revision for {title!r}")
            revision = revisions[0]
            if not isinstance(revision, dict):
                raise ValueError(f"unexpected revision object for {title!r}")
            revision_id = revision.get("revid")
            timestamp = _validate_timestamp(revision.get("timestamp"))
            mediawiki_sha1 = revision.get("sha1")
            if not isinstance(revision_id, int) or revision_id <= 0:
                raise ValueError(f"invalid revision id for {title!r}")
            if not isinstance(mediawiki_sha1, str):
                raise ValueError(f"missing MediaWiki SHA-1 for {title!r}")
            mediawiki_sha1 = mediawiki_sha1.lower()
            if not _HEX40_RE.fullmatch(mediawiki_sha1):
                raise ValueError(f"invalid MediaWiki SHA-1 for {title!r}")
            records[title] = {
                "page_id": page_id,
                "revision_id": revision_id,
                "revision_timestamp": timestamp,
                "mediawiki_sha1": mediawiki_sha1,
            }
    expected_titles = {str(page["title"]) for page in expected}
    if set(records) != expected_titles:
        raise ValueError("literary page inventory mismatch")
    return records


def build_manifest(
    *,
    fetcher: Callable[
        [Iterable[dict[str, object]]], dict[str, dict[str, object]]
    ] = fetch_page_revisions,
) -> dict[str, object]:
    pages = expected_pages()
    observed = fetcher(pages)
    rows: list[dict[str, object]] = []
    revision_ids: set[int] = set()
    page_ids: set[int] = set()
    for page in pages:
        title = str(page["title"])
        identity = observed[title]
        revision_id = int(identity["revision_id"])
        page_id = int(identity["page_id"])
        if revision_id in revision_ids:
            raise ValueError(f"duplicate revision id {revision_id}")
        if page_id in page_ids:
            raise ValueError(f"duplicate page id {page_id}")
        revision_ids.add(revision_id)
        page_ids.add(page_id)
        rows.append({**page, **identity})
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_work_url": WORK_URL,
        "source_work_index_revision_id": WORK_INDEX_REVISION_ID,
        "route_inventory_revision_id": CATEGORY_REVISION_ID,
        "bibliographic_source": PRIMARY_BIBLIOGRAPHIC_SOURCE,
        "legal_basis": "public_domain_original_russian_work_with_wikisource_reuse_terms",
        "composition_contract": {
            "literary_page_count": len(rows),
            "order": "exact route order /1 through /35 then /Эпилог",
        },
        "capture_scope": {
            "route_inventory_frozen": True,
            "literary_page_revisions_frozen": True,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "source_text_committed": False,
            "fantlab_source_edition_match": "unknown",
        },
        "pages": rows,
    }


def validate_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Running on Waves revision-manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected candidate id")
    if manifest.get("source_work_index_revision_id") != WORK_INDEX_REVISION_ID:
        raise ValueError("work-index revision drift")
    if manifest.get("route_inventory_revision_id") != CATEGORY_REVISION_ID:
        raise ValueError("route-inventory revision drift")
    if manifest.get("bibliographic_source") != PRIMARY_BIBLIOGRAPHIC_SOURCE:
        raise ValueError("bibliographic source drift")

    composition = manifest.get("composition_contract")
    if composition != {
        "literary_page_count": 36,
        "order": "exact route order /1 through /35 then /Эпилог",
    }:
        raise ValueError("composition contract drift")
    scope = manifest.get("capture_scope")
    if scope != {
        "route_inventory_frozen": True,
        "literary_page_revisions_frozen": True,
        "literary_body_extraction_frozen": False,
        "composite_identity_frozen": False,
        "source_text_committed": False,
        "fantlab_source_edition_match": "unknown",
    }:
        raise ValueError("capture scope drift")

    expected = expected_pages()
    rows = manifest.get("pages")
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise ValueError("revision manifest must contain exactly 36 literary pages")
    revision_ids: set[int] = set()
    page_ids: set[int] = set()
    identities: list[dict[str, object]] = []
    for expected_page, row in zip(expected, rows, strict=True):
        if not isinstance(row, dict):
            raise ValueError("revision manifest rows must be objects")
        if row.get("ordinal") != expected_page["ordinal"] or row.get("title") != expected_page["title"]:
            raise ValueError(f"literary page identity drift at ordinal {expected_page['ordinal']}")
        page_id = row.get("page_id")
        revision_id = row.get("revision_id")
        if not isinstance(page_id, int) or page_id <= 0 or page_id in page_ids:
            raise ValueError(f"invalid/duplicate page id at {row.get('title')!r}")
        if not isinstance(revision_id, int) or revision_id <= 0 or revision_id in revision_ids:
            raise ValueError(f"invalid/duplicate revision id at {row.get('title')!r}")
        page_ids.add(page_id)
        revision_ids.add(revision_id)
        timestamp = _validate_timestamp(row.get("revision_timestamp"))
        mediawiki_sha1 = row.get("mediawiki_sha1")
        if not isinstance(mediawiki_sha1, str) or not _HEX40_RE.fullmatch(mediawiki_sha1):
            raise ValueError(f"invalid MediaWiki SHA-1 at {row.get('title')!r}")
        identities.append(
            {
                "ordinal": row["ordinal"],
                "title": row["title"],
                "revision_id": revision_id,
                "revision_timestamp": timestamp,
                "mediawiki_sha1": mediawiki_sha1,
            }
        )
    return tuple(identities)


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    identities = validate_manifest(manifest)
    fetched = fetcher(identities)
    expected_titles = {str(row["title"]) for row in identities}
    if set(fetched) != expected_titles:
        raise ValueError("pinned literary page replay inventory mismatch")
    return {
        "verified": True,
        "candidate_id": CANDIDATE_ID,
        "verified_literary_page_count": len(identities),
        "source_text_committed": False,
        "literary_body_extraction_frozen": False,
        "composite_identity_frozen": False,
        "fantlab_source_edition_match": "unknown",
    }


def canonical_json_text(value: Mapping[str, object]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Capture/replay Running on Waves revision identities.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--output", type=Path, required=True)
    replay = subparsers.add_parser("replay")
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
