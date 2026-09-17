"""Freeze a source-free literary-body identity for one pinned Wikisource revision.

The shared machinery verifies an already-frozen revision before extraction and persists
only counts/digests. Candidate-specific modules may supply a stricter extraction
function/profile; source prose exists only in process memory.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Mapping, Sequence

from .single_page_revision import _api_query, validate_manifest as validate_revision_manifest
from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import EXTRACTION_PROFILE, extract_transcription_body


BODY_MANIFEST_VERSION = "scriptorium-single-page-literary-body-v1"
BodyExtractor = Callable[[str], str]


def fetch_pinned_wikitext(
    *,
    title: str,
    revision_id: int,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, object]:
    """Fetch one exact revision, retaining source prose only in process memory."""

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
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        raise ValueError("pinned revision timestamp missing or not UTC")
    if not isinstance(mediawiki_sha1, str) or len(mediawiki_sha1) != 40:
        raise ValueError("pinned revision MediaWiki SHA-1 missing or invalid")
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
    extractor: BodyExtractor = extract_transcription_body,
    extraction_profile: str = EXTRACTION_PROFILE,
    minimum_characters: int = 300_000,
) -> dict[str, object]:
    """Re-fetch, verify and extract one pinned transcription without retaining prose."""

    validate_revision_manifest(revision_manifest)
    if not callable(extractor):
        raise TypeError("extractor must be callable")
    if not isinstance(extraction_profile, str) or not extraction_profile:
        raise ValueError("extraction_profile must be non-empty")
    if not isinstance(minimum_characters, int) or minimum_characters < 1:
        raise ValueError("minimum_characters must be a positive integer")
    source_identity = revision_manifest.get("source_identity")
    assert isinstance(source_identity, dict)
    title = source_identity.get("title")
    revision_id = source_identity.get("revision_id")
    if not isinstance(title, str) or not isinstance(revision_id, int):
        raise ValueError("revision manifest source identity incomplete")

    observed = fetcher(title=title, revision_id=revision_id)
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

    body = extractor(wikitext)
    if not isinstance(body, str) or not body:
        raise ValueError("extractor returned empty or non-string literary body")
    identity = _body_identity(body)
    if int(identity["character_count_including_spaces"]) < minimum_characters:
        raise ValueError("extracted literary body is below the corpus threshold")

    return {
        "manifest_version": BODY_MANIFEST_VERSION,
        "candidate_id": revision_manifest["candidate_id"],
        "provider": revision_manifest.get("provider"),
        "source_revision": {
            "title": title,
            "page_id": source_identity["page_id"],
            "revision_id": revision_id,
            "revision_timestamp": source_identity["revision_timestamp"],
            "mediawiki_sha1": source_identity["mediawiki_sha1"],
            "wikitext_sha256": source_identity["wikitext_sha256"],
        },
        "extraction": {
            "profile": extraction_profile,
            "source_text_committed": False,
            "scope": "literary body extracted from the exact pinned revision wikitext",
        },
        "literary_body_identity": identity,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_comparison_admissible": True,
        "m2_parity_admissible": False,
    }


def validate_body_manifest(
    manifest: Mapping[str, object],
    *,
    revision_manifest: Mapping[str, object] | None = None,
    extraction_profile: str = EXTRACTION_PROFILE,
) -> None:
    if manifest.get("manifest_version") != BODY_MANIFEST_VERSION:
        raise ValueError("unsupported single-page body manifest version")
    candidate_id = manifest.get("candidate_id")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("body manifest candidate id missing")
    source_revision = manifest.get("source_revision")
    if not isinstance(source_revision, dict):
        raise ValueError("body manifest missing source revision")
    if not isinstance(source_revision.get("revision_id"), int):
        raise ValueError("body manifest revision id missing")
    extraction = manifest.get("extraction")
    if extraction != {
        "profile": extraction_profile,
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

    if revision_manifest is not None:
        validate_revision_manifest(revision_manifest)
        if revision_manifest.get("candidate_id") != candidate_id:
            raise ValueError("body/revision candidate mismatch")
        expected = revision_manifest.get("source_identity")
        assert isinstance(expected, dict)
        for key in (
            "title",
            "page_id",
            "revision_id",
            "revision_timestamp",
            "mediawiki_sha1",
            "wikitext_sha256",
        ):
            if source_revision.get(key) != expected.get(key):
                raise ValueError(f"body/revision source identity mismatch: {key}")


def replay_body_manifest(
    revision_manifest: Mapping[str, object],
    body_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
    extractor: BodyExtractor = extract_transcription_body,
    extraction_profile: str = EXTRACTION_PROFILE,
    minimum_characters: int = 300_000,
) -> dict[str, object]:
    validate_body_manifest(
        body_manifest,
        revision_manifest=revision_manifest,
        extraction_profile=extraction_profile,
    )
    observed = build_body_manifest(
        revision_manifest,
        fetcher=fetcher,
        extractor=extractor,
        extraction_profile=extraction_profile,
        minimum_characters=minimum_characters,
    )
    if observed != body_manifest:
        raise ValueError("pinned single-page literary-body identity drift")
    identity = body_manifest["literary_body_identity"]
    source_revision = body_manifest["source_revision"]
    assert isinstance(identity, dict) and isinstance(source_revision, dict)
    return {
        "receipt_version": "scriptorium-single-page-literary-body-replay-v1",
        "candidate_id": body_manifest["candidate_id"],
        "revision_id": source_revision["revision_id"],
        "extraction_profile": extraction_profile,
        "raw_sha256": identity["raw_sha256"],
        "normalized_sha256": identity["normalized_sha256"],
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
    parser = argparse.ArgumentParser(
        description="Capture or replay a generic source-free literary-body identity for one pinned Wikisource page."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--revision-manifest", type=Path, required=True)
    capture.add_argument("--output", type=Path, required=True)
    replay = subparsers.add_parser("replay")
    replay.add_argument("--revision-manifest", type=Path, required=True)
    replay.add_argument("--body-manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)

    revision_manifest = _load_json(args.revision_manifest)
    if args.command == "capture":
        manifest = build_body_manifest(revision_manifest)
        validate_body_manifest(manifest, revision_manifest=revision_manifest)
        _write_json(args.output, manifest)
        return 0

    body_manifest = _load_json(args.body_manifest)
    receipt = replay_body_manifest(revision_manifest, body_manifest)
    if args.receipt is not None:
        _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
