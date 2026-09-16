"""Capture an immutable Wikisource page revision identity without storing source prose."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://ru.wikisource.org/w/api.php"
USER_AGENT = "Scriptorium provenance research/1.0 (+https://github.com/drevendev/Scriptorium)"
MANIFEST_VERSION = "scriptorium-single-page-source-revision-v1"
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def _api_query(params: dict[str, str]) -> dict[str, object]:
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


def fetch_pinned_revision(
    *,
    title: str,
    revision_id: int,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, object]:
    """Fetch exactly one pinned revision and retain prose only in process memory."""

    if not title:
        raise ValueError("title must be non-empty")
    if not isinstance(revision_id, int) or revision_id <= 0:
        raise ValueError("revision_id must be a positive integer")

    payload = query(
        {
            "action": "query",
            "prop": "revisions",
            "revids": str(revision_id),
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
        }
    )
    query_obj = payload.get("query")
    if not isinstance(query_obj, dict):
        raise ValueError("MediaWiki response missing query")
    pages = query_obj.get("pages")
    if not isinstance(pages, list) or len(pages) != 1:
        raise ValueError("expected exactly one MediaWiki page for pinned revision")
    page = pages[0]
    if not isinstance(page, dict):
        raise ValueError("unexpected MediaWiki page object")
    observed_title = page.get("title")
    if observed_title != title:
        raise ValueError(
            f"pinned revision title drift: observed {observed_title!r}, expected {title!r}"
        )
    page_id = page.get("pageid")
    if not isinstance(page_id, int) or page_id <= 0:
        raise ValueError("MediaWiki page id missing for pinned revision")

    revisions = page.get("revisions")
    if not isinstance(revisions, list) or len(revisions) != 1:
        raise ValueError("expected exactly one revision object")
    revision = revisions[0]
    if not isinstance(revision, dict):
        raise ValueError("unexpected MediaWiki revision object")
    observed_revision_id = revision.get("revid")
    if observed_revision_id != revision_id:
        raise ValueError(
            "pinned revision id drift: "
            f"observed {observed_revision_id!r}, expected {revision_id!r}"
        )
    timestamp = revision.get("timestamp")
    mediawiki_sha1 = revision.get("sha1")
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        raise ValueError("pinned revision timestamp missing or not UTC")
    if not isinstance(mediawiki_sha1, str) or not _HEX40_RE.fullmatch(mediawiki_sha1):
        raise ValueError("pinned revision MediaWiki SHA-1 missing or invalid")

    slots = revision.get("slots")
    main = slots.get("main") if isinstance(slots, dict) else None
    wikitext = main.get("content") if isinstance(main, dict) else None
    if not isinstance(wikitext, str):
        raise ValueError("pinned revision main-slot wikitext missing")

    raw = wikitext.encode("utf-8")
    return {
        "title": title,
        "page_id": page_id,
        "revision_id": revision_id,
        "revision_timestamp": timestamp,
        "mediawiki_sha1": mediawiki_sha1,
        "wikitext_character_count": len(wikitext),
        "wikitext_utf8_byte_count": len(raw),
        "wikitext_sha256": sha256(raw).hexdigest(),
    }


def build_manifest(
    *,
    candidate_id: str,
    title: str,
    revision_id: int,
    source_work_url: str,
    permanent_source_url: str,
    bibliographic_source: str,
    legal_basis: str,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_revision,
) -> dict[str, object]:
    if not candidate_id:
        raise ValueError("candidate_id must be non-empty")
    if not source_work_url.startswith("https://") or not permanent_source_url.startswith("https://"):
        raise ValueError("source URLs must use HTTPS")
    if not bibliographic_source:
        raise ValueError("bibliographic_source must be non-empty")
    if not legal_basis:
        raise ValueError("legal_basis must be non-empty")

    identity = fetcher(title=title, revision_id=revision_id)
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": candidate_id,
        "provider": "Russian Wikisource",
        "source_work_url": source_work_url,
        "permanent_source_url": permanent_source_url,
        "bibliographic_source": bibliographic_source,
        "legal_basis": legal_basis,
        "source_identity": identity,
        "capture_scope": {
            "revision_wikitext_identity_frozen": True,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "source_text_committed": False,
        },
    }


def validate_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported single-page revision manifest version")
    if not isinstance(manifest.get("candidate_id"), str) or not manifest["candidate_id"]:
        raise ValueError("manifest candidate_id missing")
    identity = manifest.get("source_identity")
    if not isinstance(identity, dict):
        raise ValueError("manifest source_identity missing")
    if not isinstance(identity.get("page_id"), int) or int(identity["page_id"]) <= 0:
        raise ValueError("invalid source page_id")
    if not isinstance(identity.get("revision_id"), int) or int(identity["revision_id"]) <= 0:
        raise ValueError("invalid source revision_id")
    timestamp = identity.get("revision_timestamp")
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        raise ValueError("invalid source revision timestamp")
    mediawiki_sha1 = identity.get("mediawiki_sha1")
    if not isinstance(mediawiki_sha1, str) or not _HEX40_RE.fullmatch(mediawiki_sha1):
        raise ValueError("invalid source MediaWiki SHA-1")
    for key in ("wikitext_character_count", "wikitext_utf8_byte_count"):
        value = identity.get(key)
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"invalid source {key}")
    wikitext_sha256 = identity.get("wikitext_sha256")
    if not isinstance(wikitext_sha256, str) or not _HEX64_RE.fullmatch(wikitext_sha256):
        raise ValueError("invalid source wikitext SHA-256")
    scope = manifest.get("capture_scope")
    if scope != {
        "revision_wikitext_identity_frozen": True,
        "literary_body_extraction_frozen": False,
        "composite_identity_frozen": False,
        "source_text_committed": False,
    }:
        raise ValueError("single-page capture scope drift")
    # Source prose must never become a durable field by accident.
    if "wikitext" in identity or "content" in identity:
        raise ValueError("source prose leaked into source_identity")


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_revision,
) -> dict[str, object]:
    """Re-fetch the pinned revision and fail if any source-free identity field drifts."""

    validate_manifest(manifest)
    identity = manifest["source_identity"]
    assert isinstance(identity, dict)
    title = identity["title"]
    revision_id = identity["revision_id"]
    assert isinstance(title, str)
    assert isinstance(revision_id, int)
    observed = fetcher(title=title, revision_id=revision_id)
    if observed != identity:
        differing = sorted(key for key in set(observed) | set(identity) if observed.get(key) != identity.get(key))
        raise ValueError(f"pinned revision identity drift: {differing}")
    return {
        "receipt_version": "scriptorium-single-page-source-replay-v1",
        "candidate_id": manifest["candidate_id"],
        "revision_id": revision_id,
        "wikitext_sha256": identity["wikitext_sha256"],
        "verified": True,
        "source_text_committed": False,
    }


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Capture or replay a source-free identity for one pinned Wikisource revision."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser("capture")
    capture.add_argument("--candidate-id", required=True)
    capture.add_argument("--title", required=True)
    capture.add_argument("--revision-id", type=int, required=True)
    capture.add_argument("--source-work-url", required=True)
    capture.add_argument("--permanent-source-url", required=True)
    capture.add_argument("--bibliographic-source", required=True)
    capture.add_argument("--legal-basis", required=True)
    capture.add_argument("--output", type=Path, required=True)

    replay = subparsers.add_parser("replay")
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path)

    args = parser.parse_args(argv)
    if args.command == "capture":
        manifest = build_manifest(
            candidate_id=args.candidate_id,
            title=args.title,
            revision_id=args.revision_id,
            source_work_url=args.source_work_url,
            permanent_source_url=args.permanent_source_url,
            bibliographic_source=args.bibliographic_source,
            legal_basis=args.legal_basis,
        )
        validate_manifest(manifest)
        _write_json(args.output, manifest)
        return 0

    manifest_obj = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest_obj, dict):
        raise ValueError("manifest must be a JSON object")
    receipt = replay_manifest(manifest_obj)
    if args.receipt is not None:
        _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
