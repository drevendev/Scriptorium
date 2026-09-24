"""Freeze source-free revision identities for the retained Bulgakov corpus candidate.

The retained transcription is explicitly mixed-source: chapters 1-11 and 12-20
belong to distinct bibliographic source families. This module freezes page/revision
identity only; it does not extract or serialize literary prose.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, Sequence

from .wikisource_freeze import _api_query
from .wikisource_replay import fetch_pinned_chapter_revisions

CANDIDATE_ID = "bulgakov-white-guard-ru"
WORK_TITLE = "\u0411\u0435\u043b\u0430\u044f \u0433\u0432\u0430\u0440\u0434\u0438\u044f (\u0411\u0443\u043b\u0433\u0430\u043a\u043e\u0432)"
WORK_URL = "https://ru.wikisource.org/wiki/%D0%91%D0%B5%D0%BB%D0%B0%D1%8F_%D0%B3%D0%B2%D0%B0%D1%80%D0%B4%D0%B8%D1%8F_(%D0%91%D1%83%D0%BB%D0%B3%D0%B0%D0%BA%D0%BE%D0%B2)"
WORK_INDEX_REVISION_ID = 4715350
MANIFEST_VERSION = "scriptorium-bulgakov-source-revisions-v1"
SOURCE_FAMILY_1927 = "paris-concorde-1927"
SOURCE_FAMILY_1989 = "moscow-pravda-1989"
SOURCE_1927 = "\u041c. \u0411\u0443\u043b\u0433\u0430\u043a\u043e\u0432. \u0414\u043d\u0438 \u0422\u0443\u0440\u0431\u0438\u043d\u044b\u0445 (\u0411\u0435\u043b\u0430\u044f \u0433\u0432\u0430\u0440\u0434\u0438\u044f). \u2014 \u041f\u0430\u0440\u0438\u0436: Concorde, 1927."
SOURCE_1989 = "\u0411\u0443\u043b\u0433\u0430\u043a\u043e\u0432 \u041c. \u0410. \u0411\u0435\u043b\u0430\u044f \u0433\u0432\u0430\u0440\u0434\u0438\u044f. \u0416\u0438\u0437\u043d\u044c \u0433\u043e\u0441\u043f\u043e\u0434\u0438\u043d\u0430 \u0434\u0435 \u041c\u043e\u043b\u044c\u0435\u0440\u0430. \u0420\u0430\u0441\u0441\u043a\u0430\u0437\u044b. \u2014 \u041c.: \u041f\u0440\u0430\u0432\u0434\u0430, 1989."
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def expected_pages() -> tuple[dict[str, object], ...]:
    rows = []
    for chapter in range(1, 21):
        rows.append(
            {
                "ordinal": chapter,
                "chapter": chapter,
                "title": f"{WORK_TITLE}/\u0413\u043b\u0430\u0432\u0430 {chapter}",
                "source_family_id": SOURCE_FAMILY_1927 if chapter <= 11 else SOURCE_FAMILY_1989,
                "bibliographic_source": SOURCE_1927 if chapter <= 11 else SOURCE_1989,
            }
        )
    return tuple(rows)


def _validate_timestamp(value: object) -> str:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"invalid UTC revision timestamp {value!r}")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    if parsed.tzinfo != timezone.utc or parsed.microsecond:
        raise ValueError(f"invalid UTC revision timestamp {value!r}")
    return value


def fetch_page_revisions(
    pages: Iterable[dict[str, object]],
    *,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, dict[str, object]]:
    expected = tuple(pages)
    titles = [str(page["title"]) for page in expected]
    payload = query({
        "action": "query",
        "prop": "info|revisions",
        "titles": "|".join(titles),
        "rvprop": "ids|timestamp|sha1",
    })
    query_obj = payload.get("query")
    pages_obj = query_obj.get("pages") if isinstance(query_obj, dict) else None
    if not isinstance(pages_obj, list):
        raise ValueError("MediaWiki response missing pages")
    records: dict[str, dict[str, object]] = {}
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
        revisions = page.get("revisions")
        if not isinstance(page_id, int) or page_id <= 0:
            raise ValueError(f"invalid page id for {title!r}")
        if not isinstance(revisions, list) or len(revisions) != 1 or not isinstance(revisions[0], dict):
            raise ValueError(f"expected one current revision for {title!r}")
        revision = revisions[0]
        revision_id = revision.get("revid")
        timestamp = _validate_timestamp(revision.get("timestamp"))
        mediawiki_sha1 = revision.get("sha1")
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError(f"invalid revision id for {title!r}")
        if not isinstance(mediawiki_sha1, str) or not _HEX40_RE.fullmatch(mediawiki_sha1.lower()):
            raise ValueError(f"invalid MediaWiki SHA-1 for {title!r}")
        records[title] = {
            "page_id": page_id,
            "revision_id": revision_id,
            "revision_timestamp": timestamp,
            "mediawiki_sha1": mediawiki_sha1.lower(),
        }
    if set(records) != set(titles):
        raise ValueError("literary page inventory mismatch")
    return records


def build_manifest(
    *,
    fetcher: Callable[[Iterable[dict[str, object]]], dict[str, dict[str, object]]] = fetch_page_revisions,
) -> dict[str, object]:
    pages = expected_pages()
    observed = fetcher(pages)
    rows = []
    revision_ids: set[int] = set()
    page_ids: set[int] = set()
    for page in pages:
        identity = observed[str(page["title"])]
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
        "legal_basis": "public_domain_original_russian_work_with_wikisource_reuse_terms",
        "source_partition": [
            {"source_family_id": SOURCE_FAMILY_1927, "chapter_range": "1-11", "bibliographic_source": SOURCE_1927},
            {"source_family_id": SOURCE_FAMILY_1989, "chapter_range": "12-20", "bibliographic_source": SOURCE_1989},
        ],
        "composition_contract": {
            "literary_page_count": 20,
            "order": "chapter-number order 1 through 20",
            "single_edition_identity": False,
        },
        "capture_scope": {
            "literary_page_revisions_frozen": True,
            "source_partition_frozen": True,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "single_edition_identity": False,
            "source_text_committed": False,
            "fantlab_source_edition_match": "unknown",
        },
        "pages": rows,
    }


def validate_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    expected_partition = [
        {"source_family_id": SOURCE_FAMILY_1927, "chapter_range": "1-11", "bibliographic_source": SOURCE_1927},
        {"source_family_id": SOURCE_FAMILY_1989, "chapter_range": "12-20", "bibliographic_source": SOURCE_1989},
    ]
    expected_scope = {
        "literary_page_revisions_frozen": True,
        "source_partition_frozen": True,
        "literary_body_extraction_frozen": False,
        "composite_identity_frozen": False,
        "single_edition_identity": False,
        "source_text_committed": False,
        "fantlab_source_edition_match": "unknown",
    }
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Bulgakov revision-manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected candidate id")
    if manifest.get("source_work_index_revision_id") != WORK_INDEX_REVISION_ID:
        raise ValueError("work-index revision drift")
    if manifest.get("source_partition") != expected_partition:
        raise ValueError("source partition drift")
    if manifest.get("capture_scope") != expected_scope:
        raise ValueError("capture scope drift")
    rows = manifest.get("pages")
    expected = expected_pages()
    if not isinstance(rows, list) or len(rows) != 20:
        raise ValueError("revision manifest must contain exactly 20 literary pages")
    revision_ids: set[int] = set()
    page_ids: set[int] = set()
    identities = []
    for expected_page, row in zip(expected, rows, strict=True):
        if not isinstance(row, dict):
            raise ValueError("revision manifest rows must be objects")
        for key in ("ordinal", "chapter", "title", "source_family_id", "bibliographic_source"):
            if row.get(key) != expected_page[key]:
                raise ValueError(f"literary page/source-partition drift at chapter {expected_page['chapter']}")
        page_id = row.get("page_id")
        revision_id = row.get("revision_id")
        if not isinstance(page_id, int) or page_id <= 0 or page_id in page_ids:
            raise ValueError("invalid/duplicate page id")
        if not isinstance(revision_id, int) or revision_id <= 0 or revision_id in revision_ids:
            raise ValueError("invalid/duplicate revision id")
        page_ids.add(page_id)
        revision_ids.add(revision_id)
        timestamp = _validate_timestamp(row.get("revision_timestamp"))
        mediawiki_sha1 = row.get("mediawiki_sha1")
        if not isinstance(mediawiki_sha1, str) or not _HEX40_RE.fullmatch(mediawiki_sha1):
            raise ValueError("invalid MediaWiki SHA-1")
        identities.append({
            "ordinal": row["ordinal"],
            "title": row["title"],
            "revision_id": revision_id,
            "revision_timestamp": timestamp,
            "mediawiki_sha1": mediawiki_sha1,
        })
    return tuple(identities)


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    identities = validate_manifest(manifest)
    fetched = fetcher(identities)
    if set(fetched) != {str(row["title"]) for row in identities}:
        raise ValueError("pinned literary page replay inventory mismatch")
    return {
        "verified": True,
        "candidate_id": CANDIDATE_ID,
        "verified_literary_page_count": 20,
        "source_partition_frozen": True,
        "literary_body_extraction_frozen": False,
        "composite_identity_frozen": False,
        "single_edition_identity": False,
        "source_text_committed": False,
        "fantlab_source_edition_match": "unknown",
    }


def canonical_json_text(value: Mapping[str, object]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Capture/replay Bulgakov candidate revision identities.")
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
