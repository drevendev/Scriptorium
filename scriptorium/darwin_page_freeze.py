"""Freeze source-free revision identities for Darwin/Rachinsky ProofreadPage pages.

Only Page-namespace identity metadata is persisted. Wikitext, OCR, rendered prose and
scan bytes are deliberately outside this unit; literary-body and corpus-admission gates
remain separate.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://ru.wikisource.org/w/api.php"
USER_AGENT = "Scriptorium provenance research/1.0 (+https://github.com/drevendev/Scriptorium)"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
FAMILY_ID = "wikisource-rachinsky-glazunov-1864-vt-yo"
PAGE_FILE = "Дарвин - О происхождении видов, 1864.djvu"
PAGE_TITLE_PREFIX = f"Страница:{PAGE_FILE}/"
MANIFEST_VERSION = "scriptorium-darwin-page-revision-manifest-v1"
RECEIPT_VERSION = "scriptorium-darwin-page-revision-replay-v1"
# Long Cyrillic Page titles expand heavily under URL encoding. Eight keeps every GET
# safely below the server URI limit; the first hosted capture proved 40 returns HTTP 414.
CAPTURE_BATCH_SIZE = 8

PARENT_RANGES = ((8, 21), (423, 427))
ROUTE_RANGES = (
    (22, 56, ()), (57, 69, ()), (70, 85, ()), (86, 131, (114,)),
    (132, 161, ()), (162, 190, ()), (191, 219, ()), (220, 245, ()),
    (246, 269, ()), (270, 297, ()), (298, 326, ()), (327, 348, ()),
    (349, 384, ()), (385, 410, ()), (412, 422, ()),
)
EXPLICIT_NO_TEXT_NON_DEPENDENCIES = (114, 411)
EXPECTED_PAGE_COUNT = 418


def _api_query(params: Mapping[str, str]) -> dict[str, object]:
    encoded = urlencode({**params, "format": "json", "formatversion": "2"})
    request = Request(
        f"{API_URL}?{encoded}",
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise ValueError("unexpected MediaWiki API response")
    return payload


def expected_page_sequences() -> tuple[int, ...]:
    sequences: set[int] = set()
    for start, end in PARENT_RANGES:
        sequences.update(range(start, end + 1))
    for start, end, excluded in ROUTE_RANGES:
        sequences.update(set(range(start, end + 1)) - set(excluded))
    ordered = tuple(sorted(sequences))
    if len(ordered) != EXPECTED_PAGE_COUNT:
        raise AssertionError(
            f"topology drift: expected {EXPECTED_PAGE_COUNT} pages, got {len(ordered)}"
        )
    if any(page in sequences for page in EXPLICIT_NO_TEXT_NON_DEPENDENCIES):
        raise AssertionError("source-declared no-text non-dependency entered included set")
    return ordered


def expected_pages() -> tuple[dict[str, object], ...]:
    return tuple(
        {"ordinal": ordinal, "page_sequence": sequence, "title": f"{PAGE_TITLE_PREFIX}{sequence}"}
        for ordinal, sequence in enumerate(expected_page_sequences(), start=1)
    )


def _current_revision_query(
    pages: Iterable[dict[str, object]],
    *,
    query: Callable[[Mapping[str, str]], dict[str, object]] = _api_query,
) -> dict[str, dict[str, object]]:
    expected = tuple(pages)
    records: dict[str, dict[str, object]] = {}
    for offset in range(0, len(expected), CAPTURE_BATCH_SIZE):
        batch = expected[offset : offset + CAPTURE_BATCH_SIZE]
        titles = [str(row["title"]) for row in batch]
        payload = query({
            "action": "query", "prop": "revisions", "titles": "|".join(titles),
            "rvprop": "ids|timestamp|sha1", "redirects": "0",
        })
        query_obj = payload.get("query")
        pages_obj = query_obj.get("pages") if isinstance(query_obj, dict) else None
        if not isinstance(pages_obj, list):
            raise ValueError("MediaWiki response missing pages")
        for page in pages_obj:
            if not isinstance(page, dict):
                raise ValueError("unexpected MediaWiki page object")
            title = page.get("title")
            if not isinstance(title, str) or title not in titles:
                raise ValueError(f"unexpected Page title from MediaWiki: {title!r}")
            if page.get("missing") is True:
                raise ValueError(f"missing Wikisource Page: {title}")
            revisions = page.get("revisions")
            if not isinstance(revisions, list) or len(revisions) != 1:
                raise ValueError(f"expected one current revision for {title}")
            revision = revisions[0]
            if not isinstance(revision, dict):
                raise ValueError(f"unexpected revision object for {title}")
            revid, timestamp, mediawiki_sha1 = (
                revision.get("revid"), revision.get("timestamp"), revision.get("sha1")
            )
            if not isinstance(revid, int):
                raise ValueError(f"missing revision ID for {title}")
            if not isinstance(timestamp, str) or not isinstance(mediawiki_sha1, str):
                raise ValueError(f"incomplete revision identity for {title}")
            if title in records:
                raise ValueError(f"duplicate Page response: {title}")
            records[title] = {
                "revision_id": revid, "timestamp": timestamp, "mediawiki_sha1": mediawiki_sha1
            }
    expected_titles = {str(row["title"]) for row in expected}
    if set(records) != expected_titles:
        raise ValueError(
            f"Page inventory mismatch; missing={sorted(expected_titles-set(records))!r} "
            f"extra={sorted(set(records)-expected_titles)!r}"
        )
    return records


def build_manifest(
    *,
    fetcher: Callable[[Iterable[dict[str, object]]], dict[str, dict[str, object]]] = _current_revision_query,
    captured_at: str | None = None,
) -> dict[str, object]:
    inventory = expected_pages()
    revisions = fetcher(inventory)
    rows: list[dict[str, object]] = []
    seen_revision_ids: set[int] = set()
    for expected in inventory:
        title = str(expected["title"])
        revision = revisions[title]
        revid = revision["revision_id"]
        if not isinstance(revid, int) or revid in seen_revision_ids:
            raise ValueError(f"duplicate/invalid revision ID for {title}")
        seen_revision_ids.add(revid)
        rows.append({
            "ordinal": expected["ordinal"],
            "page_sequence": expected["page_sequence"],
            "title": title,
            "revision_id": revid,
            "timestamp": revision["timestamp"],
            "mediawiki_sha1": revision["mediawiki_sha1"],
            "permanent_url": f"https://ru.wikisource.org/w/index.php?oldid={revid}",
        })
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "family_id": FAMILY_ID,
        "captured_at_utc": captured_at
        or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_text_included": False,
        "topology_contract": {
            "parent_ranges": [list(item) for item in PARENT_RANGES],
            "route_ranges": [
                {"from": start, "to": end, "excluded": list(excluded)}
                for start, end, excluded in ROUTE_RANGES
            ],
            "explicit_no_text_non_dependencies": list(EXPLICIT_NO_TEXT_NON_DEPENDENCIES),
            "included_page_count": EXPECTED_PAGE_COUNT,
        },
        "pages": rows,
        "literary_body_frozen": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def validate_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unexpected manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID or manifest.get("family_id") != FAMILY_ID:
        raise ValueError("manifest candidate/family mismatch")
    if manifest.get("source_text_included") is not False:
        raise ValueError("source_text_included must remain false")
    for key in ("literary_body_frozen", "admitted_for_calibration", "m2_parity_admissible"):
        if manifest.get(key) is not False:
            raise ValueError(f"{key} must remain false in Page-identity manifest")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source-edition match must remain unknown")
    pages = manifest.get("pages")
    if not isinstance(pages, list) or len(pages) != EXPECTED_PAGE_COUNT:
        raise ValueError(f"manifest must contain exactly {EXPECTED_PAGE_COUNT} pages")
    expected_by_sequence = {int(row["page_sequence"]): row for row in expected_pages()}
    seen_sequences: set[int] = set()
    seen_revision_ids: set[int] = set()
    normalized: list[dict[str, object]] = []
    allowed_keys = {
        "ordinal", "page_sequence", "title", "revision_id", "timestamp",
        "mediawiki_sha1", "permanent_url",
    }
    for raw in pages:
        if not isinstance(raw, dict) or set(raw) != allowed_keys:
            raise ValueError("Page row shape drift or source payload key detected")
        sequence, revid = raw.get("page_sequence"), raw.get("revision_id")
        if not isinstance(sequence, int) or sequence not in expected_by_sequence:
            raise ValueError(f"unexpected Page sequence: {sequence!r}")
        if sequence in seen_sequences:
            raise ValueError(f"duplicate Page sequence: {sequence}")
        if not isinstance(revid, int) or revid in seen_revision_ids:
            raise ValueError(f"duplicate/invalid revision ID for Page sequence {sequence}")
        expected = expected_by_sequence[sequence]
        if raw.get("ordinal") != expected["ordinal"] or raw.get("title") != expected["title"]:
            raise ValueError(f"Page inventory identity mismatch for sequence {sequence}")
        if raw.get("permanent_url") != f"https://ru.wikisource.org/w/index.php?oldid={revid}":
            raise ValueError(f"permanent URL mismatch for sequence {sequence}")
        if not isinstance(raw.get("timestamp"), str) or not isinstance(raw.get("mediawiki_sha1"), str):
            raise ValueError(f"incomplete identity metadata for sequence {sequence}")
        seen_sequences.add(sequence)
        seen_revision_ids.add(revid)
        normalized.append(dict(raw))
    if tuple(sorted(seen_sequences)) != expected_page_sequences():
        raise ValueError("manifest Page sequence set does not match frozen topology")
    return tuple(sorted(normalized, key=lambda row: int(row["ordinal"])))


def _pinned_revision_query(
    revision_ids: Sequence[int],
    *,
    query: Callable[[Mapping[str, str]], dict[str, object]] = _api_query,
) -> dict[int, dict[str, object]]:
    records: dict[int, dict[str, object]] = {}
    for offset in range(0, len(revision_ids), CAPTURE_BATCH_SIZE):
        batch = revision_ids[offset : offset + CAPTURE_BATCH_SIZE]
        payload = query({
            "action": "query", "prop": "revisions",
            "revids": "|".join(str(item) for item in batch), "rvprop": "ids|timestamp|sha1",
        })
        query_obj = payload.get("query")
        pages_obj = query_obj.get("pages") if isinstance(query_obj, dict) else None
        if not isinstance(pages_obj, list):
            raise ValueError("MediaWiki replay response missing pages")
        for page in pages_obj:
            if not isinstance(page, dict):
                raise ValueError("unexpected MediaWiki replay page object")
            title, revisions = page.get("title"), page.get("revisions")
            if not isinstance(title, str) or not isinstance(revisions, list) or len(revisions) != 1:
                raise ValueError("unexpected pinned revision response shape")
            revision = revisions[0]
            if not isinstance(revision, dict):
                raise ValueError("unexpected pinned revision object")
            revid, timestamp, mediawiki_sha1 = (
                revision.get("revid"), revision.get("timestamp"), revision.get("sha1")
            )
            if not isinstance(revid, int) or revid not in batch:
                raise ValueError(f"unexpected pinned revision ID: {revid!r}")
            if revid in records:
                raise ValueError(f"duplicate pinned revision response: {revid}")
            if not isinstance(timestamp, str) or not isinstance(mediawiki_sha1, str):
                raise ValueError(f"incomplete pinned revision identity for {revid}")
            records[revid] = {
                "title": title, "timestamp": timestamp, "mediawiki_sha1": mediawiki_sha1
            }
    if set(records) != set(revision_ids):
        raise ValueError(
            f"pinned revision inventory mismatch; missing={sorted(set(revision_ids)-set(records))!r} "
            f"extra={sorted(set(records)-set(revision_ids))!r}"
        )
    return records


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Sequence[int]], dict[int, dict[str, object]]] = _pinned_revision_query,
) -> dict[str, object]:
    rows = validate_manifest(manifest)
    revision_ids = [int(row["revision_id"]) for row in rows]
    fetched = fetcher(revision_ids)
    mismatches: list[dict[str, object]] = []
    for row in rows:
        revid = int(row["revision_id"])
        actual = fetched[revid]
        expected = {
            "title": row["title"], "timestamp": row["timestamp"],
            "mediawiki_sha1": row["mediawiki_sha1"],
        }
        if actual != expected:
            mismatches.append({"revision_id": revid, "expected": expected, "actual": actual})
    if mismatches:
        raise ValueError(f"pinned revision identity mismatch: {mismatches[:3]!r}")
    canonical = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "receipt_version": RECEIPT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "page_revision_count": len(rows),
        "manifest_sha256": sha256(canonical.encode("utf-8")).hexdigest(),
        "identity_replay_match": True,
        "source_text_included": False,
        "literary_body_frozen": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def _read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("JSON root must be an object")
    return payload


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--manifest", type=Path, required=True)
    replay = subparsers.add_parser("replay")
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "capture":
        manifest = build_manifest()
        validate_manifest(manifest)
        _write_json(args.manifest, manifest)
        print(f"captured {EXPECTED_PAGE_COUNT} source-free Page revision identities")
        return 0
    manifest = _read_json(args.manifest)
    receipt = replay_manifest(manifest)
    _write_json(args.receipt, receipt)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
