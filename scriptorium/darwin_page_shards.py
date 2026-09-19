"""Validate and replay the committed source-free Darwin/Rachinsky Page identity shards."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from .darwin_page_freeze import (
    CANDIDATE_ID,
    EXPECTED_PAGE_COUNT,
    FAMILY_ID,
    PAGE_TITLE_PREFIX,
    _pinned_revision_query,
    expected_page_sequences,
)

INDEX_VERSION = "scriptorium-darwin-page-revision-sharded-manifest-v1"
SHARD_VERSION = "scriptorium-darwin-page-revision-shard-v1"
FIELDS = ["page_sequence", "revision_id", "timestamp", "mediawiki_sha1"]


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
    if index.get("title_prefix") != PAGE_TITLE_PREFIX:
        raise ValueError("Page title prefix drift")
    if index.get("page_identity_fields") != FIELDS:
        raise ValueError("Page identity field contract drift")
    if index.get("page_identity_count") != EXPECTED_PAGE_COUNT:
        raise ValueError("Page identity count drift")
    if index.get("source_text_included") is not False:
        raise ValueError("source_text_included must remain false")
    for key in ("literary_body_frozen", "admitted_for_calibration", "m2_parity_admissible"):
        if index.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if index.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source-edition match must remain unknown")

    shard_specs = index.get("shards")
    if not isinstance(shard_specs, list) or len(shard_specs) != 4:
        raise ValueError("expected exactly four identity shards")

    repo_root = index_path.parents[3]
    rows: list[dict[str, object]] = []
    seen_sequences: set[int] = set()
    seen_revisions: set[int] = set()
    for spec in shard_specs:
        if not isinstance(spec, dict):
            raise ValueError("invalid shard specification")
        relative = spec.get("path")
        digest = spec.get("sha256")
        if not isinstance(relative, str) or not relative.startswith(
            "corpus/candidates/source-edition-traces/"
        ):
            raise ValueError("unsafe shard path")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError("invalid shard SHA-256")
        shard_path = repo_root / relative
        raw = shard_path.read_bytes()
        if sha256(raw).hexdigest() != digest:
            raise ValueError(f"shard digest mismatch: {relative}")
        shard = json.loads(raw)
        if not isinstance(shard, dict):
            raise ValueError(f"invalid shard JSON: {relative}")
        if set(shard) != {
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
        if identities and (
            identities[0][0] != spec.get("first_page_sequence")
            or identities[-1][0] != spec.get("last_page_sequence")
        ):
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
        raise ValueError("committed shard inventory does not match frozen 418-Page topology")
    if len(rows) != EXPECTED_PAGE_COUNT:
        raise ValueError("committed shard inventory is not exactly 418 rows")
    return tuple(rows)


def replay_sharded_manifest(index_path: Path) -> dict[str, object]:
    rows = load_sharded_manifest(index_path)
    revision_ids = [int(row["revision_id"]) for row in rows]
    fetched = _pinned_revision_query(revision_ids)
    mismatches: list[int] = []
    for row in rows:
        revid = int(row["revision_id"])
        actual = fetched[revid]
        expected = {
            "title": row["title"],
            "timestamp": row["timestamp"],
            "mediawiki_sha1": row["mediawiki_sha1"],
        }
        if actual != expected:
            mismatches.append(revid)
    if mismatches:
        raise ValueError(f"pinned Page identity mismatch: {mismatches[:5]!r}")
    index_bytes = index_path.read_bytes()
    return {
        "receipt_version": "scriptorium-darwin-page-revision-sharded-replay-v1",
        "candidate_id": CANDIDATE_ID,
        "page_revision_count": EXPECTED_PAGE_COUNT,
        "index_sha256": sha256(index_bytes).hexdigest(),
        "identity_replay_match": True,
        "source_text_included": False,
        "literary_body_frozen": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    receipt = replay_sharded_manifest(args.index)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
