"""Freeze source-free Page revision identities for the 1928 Twelve Chairs route.

This unit persists only Page-namespace identity metadata. Wikitext, OCR, rendered prose,
scan bytes, literary-body composition and corpus-admission claims remain out of scope.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .darwin_page_freeze import _current_revision_query, _pinned_revision_query

CANDIDATE_ID = "ilf-petrov-twelve-chairs-ru"
FAMILY_ID = "wikisource-zif-1928-first-standalone-edition"
PAGE_FILE = "Ильф И. Петров Е. Двенадцать стульев (ЗиФ, 1928).pdf"
PAGE_TITLE_PREFIX = f"Страница:{PAGE_FILE}/"
PAGE_RANGES = ((8, 149), (152, 313), (316, 421))
NON_TRANSCLUDED_GAPS = ((150, 151), (314, 315))
EXPECTED_PAGE_COUNT = 410
CAPTURE_VERSION = "scriptorium-twelve-chairs-page-revision-capture-v1"
INDEX_VERSION = "scriptorium-twelve-chairs-page-revision-sharded-manifest-v1"
SHARD_VERSION = "scriptorium-twelve-chairs-page-revision-shard-v1"
REPLAY_VERSION = "scriptorium-twelve-chairs-page-revision-sharded-replay-v1"
FIELDS = ["page_sequence", "revision_id", "timestamp", "mediawiki_sha1"]


def expected_page_sequences() -> tuple[int, ...]:
    sequences: list[int] = []
    for start, end in PAGE_RANGES:
        sequences.extend(range(start, end + 1))
    ordered = tuple(sequences)
    if len(ordered) != EXPECTED_PAGE_COUNT or len(set(ordered)) != EXPECTED_PAGE_COUNT:
        raise AssertionError("Twelve Chairs Page topology drift")
    for start, end in NON_TRANSCLUDED_GAPS:
        if any(page in ordered for page in range(start, end + 1)):
            raise AssertionError("non-transcluded gap entered frozen dependency set")
    return ordered


def expected_pages() -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "ordinal": ordinal,
            "page_sequence": sequence,
            "title": f"{PAGE_TITLE_PREFIX}{sequence}",
        }
        for ordinal, sequence in enumerate(expected_page_sequences(), start=1)
    )


def build_capture_manifest(*, fetcher=_current_revision_query, captured_at: str | None = None) -> dict[str, object]:
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
        rows.append(
            {
                "ordinal": expected["ordinal"],
                "page_sequence": expected["page_sequence"],
                "title": title,
                "revision_id": revid,
                "timestamp": revision["timestamp"],
                "mediawiki_sha1": revision["mediawiki_sha1"],
                "permanent_url": f"https://ru.wikisource.org/w/index.php?oldid={revid}",
            }
        )
    return {
        "manifest_version": CAPTURE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "family_id": FAMILY_ID,
        "captured_at_utc": captured_at
        or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_text_included": False,
        "topology_contract": {
            "ranges": [list(item) for item in PAGE_RANGES],
            "non_transcluded_gaps": [list(item) for item in NON_TRANSCLUDED_GAPS],
            "page_identity_count": EXPECTED_PAGE_COUNT,
        },
        "pages": rows,
        "literary_body_frozen": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }


def validate_capture_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    if manifest.get("manifest_version") != CAPTURE_VERSION:
        raise ValueError("unexpected capture manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID or manifest.get("family_id") != FAMILY_ID:
        raise ValueError("capture manifest candidate/family mismatch")
    if manifest.get("source_text_included") is not False:
        raise ValueError("source_text_included must remain false")
    for key in ("literary_body_frozen", "admitted_for_calibration", "diagnostic_ready", "m2_parity_admissible"):
        if manifest.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source-edition match must remain unknown")
    topology = manifest.get("topology_contract")
    if topology != {
        "ranges": [list(item) for item in PAGE_RANGES],
        "non_transcluded_gaps": [list(item) for item in NON_TRANSCLUDED_GAPS],
        "page_identity_count": EXPECTED_PAGE_COUNT,
    }:
        raise ValueError("topology contract drift")
    pages = manifest.get("pages")
    if not isinstance(pages, list) or len(pages) != EXPECTED_PAGE_COUNT:
        raise ValueError(f"capture manifest must contain exactly {EXPECTED_PAGE_COUNT} pages")
    expected_by_sequence = {int(row["page_sequence"]): row for row in expected_pages()}
    seen_sequences: set[int] = set()
    seen_revisions: set[int] = set()
    allowed_keys = {
        "ordinal", "page_sequence", "title", "revision_id", "timestamp", "mediawiki_sha1", "permanent_url"
    }
    normalized: list[dict[str, object]] = []
    for raw in pages:
        if not isinstance(raw, dict) or set(raw) != allowed_keys:
            raise ValueError("Page row shape drift or source payload key detected")
        sequence, revid = raw.get("page_sequence"), raw.get("revision_id")
        if not isinstance(sequence, int) or sequence not in expected_by_sequence or sequence in seen_sequences:
            raise ValueError(f"duplicate/unexpected Page sequence: {sequence!r}")
        if not isinstance(revid, int) or revid in seen_revisions:
            raise ValueError(f"duplicate/invalid revision ID for Page sequence {sequence}")
        expected = expected_by_sequence[sequence]
        if raw.get("ordinal") != expected["ordinal"] or raw.get("title") != expected["title"]:
            raise ValueError(f"Page inventory identity mismatch for sequence {sequence}")
        if raw.get("permanent_url") != f"https://ru.wikisource.org/w/index.php?oldid={revid}":
            raise ValueError(f"permanent URL mismatch for sequence {sequence}")
        if not isinstance(raw.get("timestamp"), str) or not isinstance(raw.get("mediawiki_sha1"), str):
            raise ValueError(f"incomplete identity for sequence {sequence}")
        seen_sequences.add(sequence)
        seen_revisions.add(revid)
        normalized.append(dict(raw))
    if tuple(sorted(seen_sequences)) != expected_page_sequences():
        raise ValueError("capture Page sequence set does not match frozen topology")
    return tuple(sorted(normalized, key=lambda row: int(row["ordinal"])))


def _load_object(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def load_sharded_manifest(index_path: Path) -> tuple[dict[str, object], ...]:
    index = _load_object(index_path)
    if index.get("manifest_version") != INDEX_VERSION:
        raise ValueError("unexpected sharded manifest version")
    if index.get("candidate_id") != CANDIDATE_ID or index.get("family_id") != FAMILY_ID:
        raise ValueError("sharded manifest candidate/family mismatch")
    if index.get("title_prefix") != PAGE_TITLE_PREFIX or index.get("page_identity_fields") != FIELDS:
        raise ValueError("Page identity contract drift")
    if index.get("page_identity_count") != EXPECTED_PAGE_COUNT:
        raise ValueError("Page identity count drift")
    if index.get("topology_contract") != {
        "ranges": [list(item) for item in PAGE_RANGES],
        "non_transcluded_gaps": [list(item) for item in NON_TRANSCLUDED_GAPS],
    }:
        raise ValueError("sharded topology contract drift")
    if index.get("source_text_included") is not False:
        raise ValueError("source_text_included must remain false")
    for key in ("literary_body_frozen", "admitted_for_calibration", "diagnostic_ready", "m2_parity_admissible"):
        if index.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if index.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source-edition match must remain unknown")
    shard_specs = index.get("shards")
    if not isinstance(shard_specs, list) or not shard_specs:
        raise ValueError("sharded manifest must name at least one shard")

    repo_root = index_path.parents[3]
    rows: list[dict[str, object]] = []
    seen_sequences: set[int] = set()
    seen_revisions: set[int] = set()
    for spec in shard_specs:
        if not isinstance(spec, dict):
            raise ValueError("invalid shard specification")
        relative, digest = spec.get("path"), spec.get("sha256")
        if not isinstance(relative, str) or not relative.startswith("corpus/candidates/source-edition-traces/"):
            raise ValueError("unsafe shard path")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError("invalid shard SHA-256")
        shard_path = repo_root / relative
        raw = shard_path.read_bytes()
        if sha256(raw).hexdigest() != digest:
            raise ValueError(f"shard digest mismatch: {relative}")
        shard = json.loads(raw)
        if not isinstance(shard, dict) or set(shard) != {
            "shard_version", "candidate_id", "fields", "page_identities", "source_text_included"
        }:
            raise ValueError(f"shard shape drift or source payload key: {relative}")
        if shard.get("shard_version") != SHARD_VERSION or shard.get("candidate_id") != CANDIDATE_ID:
            raise ValueError(f"shard identity mismatch: {relative}")
        if shard.get("fields") != FIELDS or shard.get("source_text_included") is not False:
            raise ValueError(f"shard field/source boundary drift: {relative}")
        identities = shard.get("page_identities")
        if not isinstance(identities, list) or len(identities) != spec.get("row_count"):
            raise ValueError(f"shard row count mismatch: {relative}")
        if identities and (identities[0][0] != spec.get("first_page_sequence") or identities[-1][0] != spec.get("last_page_sequence")):
            raise ValueError(f"shard boundary mismatch: {relative}")
        for identity in identities:
            if not isinstance(identity, list) or len(identity) != 4:
                raise ValueError(f"invalid identity tuple: {relative}")
            sequence, revid, timestamp, mediawiki_sha1 = identity
            if not isinstance(sequence, int) or sequence in seen_sequences:
                raise ValueError(f"duplicate/invalid Page sequence: {sequence!r}")
            if not isinstance(revid, int) or revid in seen_revisions:
                raise ValueError(f"duplicate/invalid revision ID: {revid!r}")
            if not isinstance(timestamp, str) or not isinstance(mediawiki_sha1, str):
                raise ValueError(f"incomplete identity for Page sequence {sequence}")
            seen_sequences.add(sequence)
            seen_revisions.add(revid)
            rows.append({
                "page_sequence": sequence,
                "title": f"{PAGE_TITLE_PREFIX}{sequence}",
                "revision_id": revid,
                "timestamp": timestamp,
                "mediawiki_sha1": mediawiki_sha1,
            })
    rows.sort(key=lambda row: int(row["page_sequence"]))
    if tuple(row["page_sequence"] for row in rows) != expected_page_sequences():
        raise ValueError("committed shard inventory does not match frozen 410-Page topology")
    return tuple(rows)


def replay_sharded_manifest(index_path: Path, *, fetcher=_pinned_revision_query) -> dict[str, object]:
    rows = load_sharded_manifest(index_path)
    revision_ids = [int(row["revision_id"]) for row in rows]
    fetched = fetcher(revision_ids)
    mismatches: list[int] = []
    for row in rows:
        revid = int(row["revision_id"])
        expected = {
            "title": row["title"],
            "timestamp": row["timestamp"],
            "mediawiki_sha1": row["mediawiki_sha1"],
        }
        if fetched[revid] != expected:
            mismatches.append(revid)
    if mismatches:
        raise ValueError(f"pinned Page identity mismatch: {mismatches[:5]!r}")
    return {
        "receipt_version": REPLAY_VERSION,
        "candidate_id": CANDIDATE_ID,
        "page_revision_count": EXPECTED_PAGE_COUNT,
        "index_sha256": sha256(index_path.read_bytes()).hexdigest(),
        "identity_replay_match": True,
        "source_text_included": False,
        "literary_body_frozen": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    capture = sub.add_parser("capture")
    capture.add_argument("--manifest", type=Path, required=True)
    replay = sub.add_parser("replay")
    replay.add_argument("--index", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "capture":
        payload = build_capture_manifest()
        validate_capture_manifest(payload)
        _write_json(args.manifest, payload)
    else:
        payload = replay_sharded_manifest(args.index)
        _write_json(args.receipt, payload)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
