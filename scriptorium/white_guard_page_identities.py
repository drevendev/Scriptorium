"""Capture replayable Page: revision identities for the Paris 1927 White Guard route.

Metadata only. The eleven pinned chapter parents are not the transcluded text;
current Page: revisions cannot establish a historical rendered edition or parity.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import re
import sys
from typing import Callable, Iterable, Mapping

from .white_guard_body_preflight import PROOFREADPAGE_INDEX, build_preflight
from .white_guard_delivery import MANIFEST_SHA256
from .white_guard_revisions import CANDIDATE_ID, SOURCE_FAMILY_1927, canonical_json_text
from .white_guard_revisions import fetch_pinned_revision_identities
from .wikisource_freeze import _api_query

SCHEMA_VERSION = "scriptorium-white-guard-paris-page-identities-v1"
PAGE_NAMESPACE = 104
PAGE_PREFIX = f"Страница:{PROOFREADPAGE_INDEX}/"
# The exact route topology observed by the pinned-parent replay in #430.
EXPECTED_RANGES = ((5, 9), (10, 32), (33, 52), (53, 61), (62, 80),
                   (81, 112), (113, 124), (125, 138), (139, 148),
                   (149, 164), (165, 189))
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_TIMESTAMP = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\Z")


def expected_page_rows(preflight: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    """Trust only an exact historical-parent replay with the reviewed route topology."""
    if (not isinstance(preflight, Mapping)
            or preflight.get("provider_replay") != "VERIFIED_IDENTITIES"
            or preflight.get("manifest_sha256") != MANIFEST_SHA256
            or preflight.get("chapter_count") != 20
            or not isinstance(preflight.get("chapters"), list)
            or len(preflight["chapters"]) != 20):
        raise ValueError("verified White Guard parent replay required")
    result = []
    for chapter, bounds in enumerate(EXPECTED_RANGES, start=1):
        row = preflight["chapters"][chapter - 1]
        first, last = bounds
        if (not isinstance(row, dict) or type(row.get("chapter")) is not int
                or row["chapter"] != chapter
                or row.get("source_family_id") != SOURCE_FAMILY_1927
                or row.get("extraction_status") != "UNSUPPORTED_MARKUP"
                or row.get("extraction_failure_code") != "PROOFREADPAGE_UNPINNED"
                or row.get("proofreadpage_page_plan") != {
                    "index_title": PROOFREADPAGE_INDEX,
                    "first_page": first, "last_page": last,
                    "page_count": last - first + 1,
                }):
            raise ValueError("pinned Paris chapter range drift")
        for number in range(first, last + 1):
            result.append({"chapter": chapter, "page_number": number,
                           "title": f"{PAGE_PREFIX}{number}"})
    if len(result) != 185 or [r["page_number"] for r in result] != list(range(5, 190)):
        raise ValueError("Paris Page-namespace topology is incomplete")
    return tuple(result)


def fetch_current_page_identities(
    pages: Iterable[Mapping[str, object]],
    *, query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, dict[str, object]]:
    """Bounded current metadata capture; never request Page: content or redirects."""
    expected = tuple(pages)
    titles = [row["title"] for row in expected]
    if not expected or len(expected) > 185 or len(set(titles)) != len(titles):
        raise ValueError("invalid Page dependency inventory")
    results: dict[str, dict[str, object]] = {}
    for offset in range(0, len(titles), 25):
        batch = titles[offset:offset + 25]
        payload = query({"action": "query", "prop": "info|revisions",
                         "titles": "|".join(batch), "rvprop": "ids|timestamp|sha1",
                         "redirects": "0"})
        query_result = payload.get("query") if isinstance(payload, dict) else None
        if (not isinstance(query_result, dict)
                or "normalized" in query_result or "redirects" in query_result
                or not isinstance(query_result.get("pages"), list)):
            raise ValueError("unsafe MediaWiki Page identity response")
        seen: set[str] = set()
        for page in query_result["pages"]:
            if not isinstance(page, dict):
                raise ValueError("invalid Page identity row")
            title = page.get("title")
            revisions = page.get("revisions")
            if (not isinstance(title, str) or title not in batch or title in seen
                    or type(page.get("ns")) is not int or page["ns"] != PAGE_NAMESPACE
                    or type(page.get("pageid")) is not int or page["pageid"] <= 0
                    or "missing" in page or "redirect" in page
                    or not isinstance(revisions, list) or len(revisions) != 1
                    or not isinstance(revisions[0], dict)):
                raise ValueError("Page identity or namespace mismatch")
            rev = revisions[0]
            rid, stamp, digest = rev.get("revid"), rev.get("timestamp"), rev.get("sha1")
            if (type(rid) is not int or rid <= 0 or not isinstance(stamp, str)
                    or not _TIMESTAMP.fullmatch(stamp) or not isinstance(digest, str)
                    or not _SHA1.fullmatch(digest)):
                raise ValueError("invalid Page revision identity")
            try:
                parsed = datetime.fromisoformat(stamp[:-1] + "+00:00")
                if parsed.tzinfo != timezone.utc:
                    raise ValueError("invalid timestamp timezone")
            except ValueError:
                raise ValueError("invalid Page revision timestamp") from None
            seen.add(title)
            results[title] = {"page_id": page["pageid"], "revision_id": rid,
                              "revision_timestamp": stamp, "mediawiki_sha1": digest}
        if seen != set(batch):
            raise ValueError("incomplete Page revision batch")
    if len({row["page_id"] for row in results.values()}) != len(results) or len({row["revision_id"] for row in results.values()}) != len(results):
        raise ValueError("duplicate Page or revision ID")
    return results


def build_inventory(
    *,
    previewer: Callable[[], Mapping[str, object]] = build_preflight,
    fetcher: Callable[[tuple[dict[str, object], ...]], Mapping[str, Mapping[str, object]]] = fetch_current_page_identities,
    replayer: Callable[[tuple[dict[str, object], ...]], object] = fetch_pinned_revision_identities,
) -> dict[str, object]:
    """Capture metadata, then verify the captured exact oldids before issuing a receipt."""
    rows = expected_page_rows(previewer())
    observed = fetcher(rows)
    if not isinstance(observed, Mapping) or set(observed) != {row["title"] for row in rows}:
        raise ValueError("incomplete current Page identity capture")
    identities = []
    for row in rows:
        value = observed[row["title"]]
        if not isinstance(value, Mapping) or set(value) != {
            "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1"
        }:
            raise ValueError("unexpected Page identity shape")
        identities.append({**row, **value})
    replay_rows = tuple({k: row[k] for k in (
        "title", "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1"
    )} for row in identities)
    # Re-query exactly those oldids, not live transclusion. A failed replay aborts.
    verified = replayer(replay_rows)
    if not isinstance(verified, Mapping) or set(verified) != {row["title"] for row in rows}:
        raise ValueError("captured Page revisions could not be replayed")
    for row in replay_rows:
        if verified[row["title"]] != {key: row[key] for key in (
            "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1"
        )}:
            raise ValueError("captured Page identity replay drift")
    return {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": CANDIDATE_ID,
        "parent_manifest_sha256": MANIFEST_SHA256,
        "source_family_id": SOURCE_FAMILY_1927,
        "capture_semantics": "CURRENT_PAGE_REVISIONS_NOT_ATOMIC_HISTORICAL_TRANSCLUSION",
        "pinned_parent_replay": "VERIFIED_IDENTITIES",
        "captured_page_replay": "VERIFIED_IDENTITIES",
        "page_count": len(identities),
        "chapter_count": len(EXPECTED_RANGES),
        "pages": identities,
        "source_text_committed": False,
        "single_edition_body_frozen": False,
        "fantlab_input_identity": "unknown",
        "m2_parity_admissible": False,
    }


def main(argv: list[str] | None = None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    try:
        report = build_inventory()
    except Exception:
        print("White Guard Paris Page identity capture failed; no receipt issued.", file=sys.stderr)
        return 2
    print(canonical_json_text(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
