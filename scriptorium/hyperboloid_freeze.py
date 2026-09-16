"""Freeze a source-free literary-body identity for the pinned Hyperboloid revision.

The source prose exists only in process memory. The durable artifact records the exact
already-frozen revision identity, a source-specific extraction profile, and raw/
normalized literary-body digests. It deliberately does not claim print-edition or
FantLab analyzer-input identity.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Mapping, Sequence

from .single_page_revision import _api_query, validate_manifest as validate_revision_manifest
from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import extract_transcription_body


CANDIDATE_ID = "tolstoy-hyperboloid-garin-wikisource-ru"
TITLE = "Гиперболоид инженера Гарина (Толстой)"
REVISION_ID = 5014458
BODY_MANIFEST_VERSION = "scriptorium-single-page-literary-body-v1"
EXTRACTION_PROFILE = "scriptorium-hyperboloid-wikisource-body-v1"


def fetch_pinned_wikitext(
    *,
    title: str,
    revision_id: int,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, object]:
    """Fetch one exact revision including transient wikitext for extraction."""

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
    if not isinstance(page, dict) or page.get("title") != title:
        raise ValueError("pinned revision title drift")
    page_id = page.get("pageid")
    revisions = page.get("revisions")
    if not isinstance(page_id, int) or page_id <= 0:
        raise ValueError("pinned revision page id missing")
    if not isinstance(revisions, list) or len(revisions) != 1:
        raise ValueError("expected exactly one MediaWiki revision")
    revision = revisions[0]
    if not isinstance(revision, dict) or revision.get("revid") != revision_id:
        raise ValueError("pinned revision id drift")
    timestamp = revision.get("timestamp")
    mediawiki_sha1 = revision.get("sha1")
    slots = revision.get("slots")
    main = slots.get("main") if isinstance(slots, dict) else None
    wikitext = main.get("content") if isinstance(main, dict) else None
    if not isinstance(timestamp, str) or not isinstance(mediawiki_sha1, str):
        raise ValueError("pinned revision identity incomplete")
    if not isinstance(wikitext, str):
        raise ValueError("pinned revision wikitext missing")
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
        "wikitext": wikitext,
    }


def extract_literary_body(wikitext: str) -> str:
    """Extract only the literary body under the frozen source-specific profile.

    The current Hyperboloid transcription is admitted only while it satisfies the same
    fail-closed single-body contract used by Scriptorium's early Wikisource extractor:
    exactly one ``text``/``indent`` div and no unsupported residual template/table/
    heading markup after the documented reductions. A future source-shape change must
    version this profile rather than silently broadening it.
    """

    return extract_transcription_body(wikitext)


def _body_identity(body: str) -> dict[str, object]:
    raw = body.encode("utf-8")
    normalized = normalize_text(body)
    return {
        "character_count_including_spaces": len(body),
        "utf8_byte_count": len(raw),
        "raw_sha256": sha256(raw).hexdigest(),
        "normalization_profile": NORMALIZATION_PROFILE,
        "normalized_character_count_including_spaces": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }


def build_body_manifest(
    revision_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    validate_revision_manifest(revision_manifest)
    if revision_manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected candidate id")
    source_identity = revision_manifest.get("source_identity")
    if not isinstance(source_identity, dict):
        raise ValueError("revision manifest missing source identity")
    if source_identity.get("title") != TITLE or source_identity.get("revision_id") != REVISION_ID:
        raise ValueError("revision manifest does not identify the frozen Hyperboloid revision")

    observed = fetcher(title=TITLE, revision_id=REVISION_ID)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient source prose missing")
    if observed != source_identity:
        differing = sorted(
            key
            for key in set(observed) | set(source_identity)
            if observed.get(key) != source_identity.get(key)
        )
        raise ValueError(f"pinned revision identity drift before extraction: {differing}")

    body = extract_literary_body(wikitext)
    identity = _body_identity(body)
    if int(identity["character_count_including_spaces"]) < 300_000:
        raise ValueError("extracted literary body is below the corpus threshold")

    return {
        "manifest_version": BODY_MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_revision": {
            "title": TITLE,
            "page_id": source_identity["page_id"],
            "revision_id": REVISION_ID,
            "revision_timestamp": source_identity["revision_timestamp"],
            "mediawiki_sha1": source_identity["mediawiki_sha1"],
            "wikitext_sha256": source_identity["wikitext_sha256"],
        },
        "extraction": {
            "profile": EXTRACTION_PROFILE,
            "source_text_committed": False,
            "scope": "literary body extracted from the exact pinned revision wikitext",
        },
        "literary_body_identity": identity,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_comparison_admissible": True,
        "m2_parity_admissible": False,
    }


def validate_body_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("manifest_version") != BODY_MANIFEST_VERSION:
        raise ValueError("unsupported Hyperboloid body manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Hyperboloid body candidate")
    source_revision = manifest.get("source_revision")
    if not isinstance(source_revision, dict):
        raise ValueError("body manifest missing source revision")
    if source_revision.get("title") != TITLE or source_revision.get("revision_id") != REVISION_ID:
        raise ValueError("body manifest source revision drift")
    extraction = manifest.get("extraction")
    if extraction != {
        "profile": EXTRACTION_PROFILE,
        "source_text_committed": False,
        "scope": "literary body extracted from the exact pinned revision wikitext",
    }:
        raise ValueError("body extraction contract drift")
    identity = manifest.get("literary_body_identity")
    if not isinstance(identity, dict):
        raise ValueError("body manifest missing literary body identity")
    for key in (
        "character_count_including_spaces",
        "utf8_byte_count",
        "normalized_character_count_including_spaces",
    ):
        value = identity.get(key)
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"invalid body identity {key}")
    for key in ("raw_sha256", "normalized_sha256"):
        value = identity.get(key)
        if not isinstance(value, str) or len(value) != 64:
            raise ValueError(f"invalid body identity {key}")
    if identity.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError("body normalization profile drift")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")
    if manifest.get("diagnostic_comparison_admissible") is not True:
        raise ValueError("frozen public body should be diagnostic-admissible")
    if manifest.get("m2_parity_admissible") is not False:
        raise ValueError("public-source freezing cannot advance M2")
    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(manifest):
        raise ValueError("source prose leaked into body manifest")


def replay_body_manifest(
    revision_manifest: Mapping[str, object],
    body_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    validate_body_manifest(body_manifest)
    observed = build_body_manifest(revision_manifest, fetcher=fetcher)
    if observed != body_manifest:
        raise ValueError("pinned Hyperboloid literary-body identity drift")
    return {
        "receipt_version": "scriptorium-single-page-literary-body-replay-v1",
        "candidate_id": CANDIDATE_ID,
        "revision_id": REVISION_ID,
        "extraction_profile": EXTRACTION_PROFILE,
        "raw_sha256": body_manifest["literary_body_identity"]["raw_sha256"],
        "normalized_sha256": body_manifest["literary_body_identity"]["normalized_sha256"],
        "verified": True,
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze or replay Hyperboloid literary-body identity.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--revision-manifest", type=Path, required=True)
    capture.add_argument("--output", type=Path, required=True)
    replay = subparsers.add_parser("replay")
    replay.add_argument("--revision-manifest", type=Path, required=True)
    replay.add_argument("--body-manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)

    revision_manifest = _load_json(args.revision_manifest)
    if args.command == "capture":
        manifest = build_body_manifest(revision_manifest)
        validate_body_manifest(manifest)
        _write_json(args.output, manifest)
        return 0

    body_manifest = _load_json(args.body_manifest)
    receipt = replay_body_manifest(revision_manifest, body_manifest)
    _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
