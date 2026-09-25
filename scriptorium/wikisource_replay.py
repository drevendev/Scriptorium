"""Replay an immutable Russian Wikisource composite from a packed revision manifest."""

from __future__ import annotations

from hashlib import sha256
from typing import Callable, Iterable, Mapping

from .source_revision_manifest import decode_chapter_identities
from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import _api_query, extract_transcription_body


def fetch_pinned_chapter_revisions(
    identities: Iterable[Mapping[str, object]],
    *,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, str]:
    """Fetch the exact recorded revisions and fail closed on identity drift."""

    expected = tuple(identities)
    records: dict[str, str] = {}
    by_revision_id = {int(row["revision_id"]): row for row in expected}
    if len(by_revision_id) != len(expected):
        raise ValueError("packed manifest contains duplicate revision ids")

    for offset in range(0, len(expected), 40):
        batch = expected[offset : offset + 40]
        requested_ids = [int(row["revision_id"]) for row in batch]
        payload = query(
            {
                "action": "query",
                "prop": "revisions",
                "revids": "|".join(str(value) for value in requested_ids),
                "rvprop": "ids|timestamp|sha1|content",
                "rvslots": "main",
                "redirects": "0",
            }
        )
        query_obj = payload.get("query")
        if not isinstance(query_obj, dict):
            raise ValueError("MediaWiki response missing query")
        pages = query_obj.get("pages")
        if not isinstance(pages, list):
            raise ValueError("MediaWiki response missing pages")

        seen_batch: set[int] = set()
        for page in pages:
            if not isinstance(page, dict):
                raise ValueError("unexpected page object")
            title = page.get("title")
            revisions = page.get("revisions")
            if not isinstance(title, str):
                raise ValueError("MediaWiki revision response missing page title")
            if not isinstance(revisions, list) or len(revisions) != 1:
                raise ValueError(f"expected one pinned revision for {title!r}")
            revision = revisions[0]
            if not isinstance(revision, dict):
                raise ValueError(f"unexpected revision object for {title!r}")
            revision_id = revision.get("revid")
            if not isinstance(revision_id, int) or revision_id not in by_revision_id:
                raise ValueError(f"unexpected revision id from MediaWiki: {revision_id!r}")
            if revision_id not in requested_ids:
                raise ValueError(f"revision {revision_id} returned outside requested batch")
            if revision_id in seen_batch:
                raise ValueError(f"duplicate revision response: {revision_id}")
            seen_batch.add(revision_id)

            identity = by_revision_id[revision_id]
            expected_title = str(identity["title"])
            if "page_id" in identity:
                expected_page_id = identity["page_id"]
                if not isinstance(expected_page_id, int) or expected_page_id <= 0:
                    raise ValueError(f"invalid expected page id for revision {revision_id}")
                if page.get("pageid") != expected_page_id:
                    raise ValueError(f"revision {revision_id} page ID drift")
            if title != expected_title:
                raise ValueError(
                    f"revision {revision_id} title drift: {title!r}, expected {expected_title!r}"
                )
            if revision.get("timestamp") != identity["revision_timestamp"]:
                raise ValueError(f"revision {revision_id} timestamp drift")
            if revision.get("sha1") != identity["mediawiki_sha1"]:
                raise ValueError(f"revision {revision_id} MediaWiki SHA-1 drift")
            slots = revision.get("slots")
            main = slots.get("main") if isinstance(slots, dict) else None
            content = main.get("content") if isinstance(main, dict) else None
            if not isinstance(content, str):
                raise ValueError(f"missing wikitext content for revision {revision_id}")
            if expected_title in records:
                raise ValueError(f"duplicate chapter response: {expected_title}")
            records[expected_title] = content

        if seen_batch != set(requested_ids):
            missing = sorted(set(requested_ids) - seen_batch)
            raise ValueError(f"MediaWiki omitted pinned revisions: {missing!r}")

    expected_titles = {str(row["title"]) for row in expected}
    if set(records) != expected_titles:
        missing = sorted(expected_titles - set(records))
        extra = sorted(set(records) - expected_titles)
        raise ValueError(f"pinned chapter inventory mismatch; missing={missing!r} extra={extra!r}")
    return records


def replay_packed_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = fetch_pinned_chapter_revisions,
) -> str:
    """Rebuild and verify the frozen composite text without persisting source prose."""

    identities = decode_chapter_identities(manifest)
    revisions = fetcher(identities)
    bodies = [extract_transcription_body(revisions[str(row["title"])]) for row in identities]
    composite = "\n\n".join(bodies)

    composite_identity = manifest.get("composite_identity")
    if not isinstance(composite_identity, dict):
        raise ValueError("packed manifest missing composite_identity")

    raw = composite.encode("utf-8")
    normalized = normalize_text(composite)
    observed = {
        "chapter_count": len(identities),
        "character_count_including_spaces": len(composite),
        "utf8_byte_count": len(raw),
        "raw_sha256": sha256(raw).hexdigest(),
        "normalization_profile": NORMALIZATION_PROFILE,
        "normalized_character_count_including_spaces": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }
    for key, value in observed.items():
        if composite_identity.get(key) != value:
            raise ValueError(
                f"frozen composite identity drift for {key}: "
                f"observed {value!r}, expected {composite_identity.get(key)!r}"
            )
    return composite
