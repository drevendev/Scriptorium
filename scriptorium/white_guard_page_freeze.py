"""Capture and verify 185 Paris White Guard ProofreadPage revision identities.

These Page: revisions are a CURRENT snapshot, not the transclusion content as of
any historical parent oldid. Only identity metadata leaves this module; source
text, literary-body selection, edition collation, and parity remain separate.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from typing import Callable, Iterable, Mapping, Sequence

from .darwin_page_freeze import _current_revision_query, _pinned_revision_query
from .white_guard_body_preflight import PROOFREADPAGE_INDEX
from .white_guard_revisions import CANDIDATE_ID, SOURCE_FAMILY_1927

MANIFEST_VERSION = "scriptorium-white-guard-paris-page-identities-v1"
REPLAY_VERSION = "scriptorium-white-guard-paris-page-replay-v1"
PAGE_TITLE_PREFIX = f"Страница:{PROOFREADPAGE_INDEX}/"
CHAPTER_RANGES = (
    (5, 9), (10, 32), (33, 52), (53, 61), (62, 80), (81, 112),
    (113, 124), (125, 138), (139, 148), (149, 164), (165, 189),
)
EXPECTED_PAGE_COUNT = 185
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_ROW_KEYS = frozenset({
    "ordinal", "chapter", "page_sequence", "title", "revision_id",
    "timestamp", "mediawiki_sha1", "permanent_url",
})
_TOP_KEYS = frozenset({
    "manifest_version", "candidate_id", "source_family_id", "index_title",
    "captured_at_utc", "capture_basis", "chapter_ranges", "page_count",
    "pages", "source_text_included", "literary_body_frozen",
    "single_edition_body_ready", "fantlab_input_identity", "m2_parity_admissible",
})


def _positive_int(value: object) -> bool:
    return type(value) is int and value > 0


def _timestamp(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value
    ):
        raise ValueError("invalid UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        raise ValueError("invalid UTC timestamp") from None
    if parsed.tzinfo != timezone.utc:
        raise ValueError("UTC timestamp required")
    return value


def expected_pages() -> tuple[dict[str, object], ...]:
    """Exact chapter/scan-page mapping observed in the 20-revision v3 replay."""
    expected_sequence = 5
    pages: list[dict[str, object]] = []
    for chapter, (first, last) in enumerate(CHAPTER_RANGES, start=1):
        if first != expected_sequence or last < first:
            raise AssertionError("Paris chapter dependency topology drift")
        for sequence in range(first, last + 1):
            pages.append({
                "ordinal": len(pages) + 1,
                "chapter": chapter,
                "page_sequence": sequence,
                "title": f"{PAGE_TITLE_PREFIX}{sequence}",
            })
        expected_sequence = last + 1
    if expected_sequence != 190 or len(pages) != EXPECTED_PAGE_COUNT:
        raise AssertionError("Paris Page dependency inventory drift")
    return tuple(pages)


def validate_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    if not isinstance(manifest, Mapping) or set(manifest) != _TOP_KEYS:
        raise ValueError("Page manifest schema drift")
    if (manifest["manifest_version"] != MANIFEST_VERSION
            or manifest["candidate_id"] != CANDIDATE_ID
            or manifest["source_family_id"] != SOURCE_FAMILY_1927
            or manifest["index_title"] != PROOFREADPAGE_INDEX):
        raise ValueError("Page manifest identity drift")
    if manifest["capture_basis"] != "CURRENT_PAGE_REVISIONS":
        raise ValueError("unsupported Page capture basis")
    if manifest["chapter_ranges"] != [list(pair) for pair in CHAPTER_RANGES]:
        raise ValueError("Page chapter topology drift")
    if type(manifest["page_count"]) is not int or manifest["page_count"] != EXPECTED_PAGE_COUNT:
        raise ValueError("Page count drift")
    _timestamp(manifest["captured_at_utc"])
    for key in ("source_text_included", "literary_body_frozen",
                "single_edition_body_ready", "m2_parity_admissible"):
        if manifest[key] is not False:
            raise ValueError("Page capture cannot claim body or parity")
    if manifest["fantlab_input_identity"] != "unknown":
        raise ValueError("Page capture cannot claim FantLab input identity")
    rows = manifest["pages"]
    if not isinstance(rows, list) or len(rows) != EXPECTED_PAGE_COUNT:
        raise ValueError("Page manifest must have exactly 185 rows")
    expected = expected_pages()
    seen_revisions: set[int] = set()
    normalized: list[dict[str, object]] = []
    for index, (row, target) in enumerate(zip(rows, expected, strict=True)):
        if not isinstance(row, dict) or set(row) != _ROW_KEYS:
            raise ValueError("Page row schema drift")
        if any(type(row[key]) is not int or row[key] != target[key]
               for key in ("ordinal", "chapter", "page_sequence")):
            raise ValueError("Page order or chapter mapping drift")
        if row["title"] != target["title"]:
            raise ValueError("Page title drift")
        revid = row["revision_id"]
        if not _positive_int(revid) or revid in seen_revisions:
            raise ValueError("duplicate or invalid Page revision")
        seen_revisions.add(revid)
        _timestamp(row["timestamp"])
        sha1 = row["mediawiki_sha1"]
        if not isinstance(sha1, str) or not _SHA1.fullmatch(sha1):
            raise ValueError("invalid Page SHA-1")
        if row["permanent_url"] != f"https://ru.wikisource.org/w/index.php?oldid={revid}":
            raise ValueError("Page permanent URL mismatch")
        normalized.append(dict(row))
    return tuple(normalized)


def build_manifest(
    *,
    fetcher: Callable[[Iterable[dict[str, object]]], Mapping[str, Mapping[str, object]]] = _current_revision_query,
    captured_at: str | None = None,
) -> dict[str, object]:
    inventory = expected_pages()
    captured = fetcher(inventory)
    if not isinstance(captured, Mapping) or set(captured) != {
        str(row["title"]) for row in inventory
    }:
        raise ValueError("Page identity provider inventory mismatch")
    rows: list[dict[str, object]] = []
    for target in inventory:
        identity = captured[str(target["title"])]
        if not isinstance(identity, Mapping) or set(identity) != {
            "revision_id", "timestamp", "mediawiki_sha1"
        }:
            raise ValueError("Page provider identity schema drift")
        revid = identity["revision_id"]
        rows.append({
            **target,
            "revision_id": revid,
            "timestamp": identity["timestamp"],
            "mediawiki_sha1": identity["mediawiki_sha1"],
            "permanent_url": f"https://ru.wikisource.org/w/index.php?oldid={revid}",
        })
    result: dict[str, object] = {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_family_id": SOURCE_FAMILY_1927,
        "index_title": PROOFREADPAGE_INDEX,
        "captured_at_utc": captured_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "capture_basis": "CURRENT_PAGE_REVISIONS",
        "chapter_ranges": [list(pair) for pair in CHAPTER_RANGES],
        "page_count": EXPECTED_PAGE_COUNT,
        "pages": rows,
        "source_text_included": False,
        "literary_body_frozen": False,
        "single_edition_body_ready": False,
        "fantlab_input_identity": "unknown",
        "m2_parity_admissible": False,
    }
    validate_manifest(result)
    return result


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Sequence[int]], Mapping[int, Mapping[str, object]]] = _pinned_revision_query,
) -> dict[str, object]:
    rows = validate_manifest(manifest)
    revids = tuple(int(row["revision_id"]) for row in rows)
    actual = fetcher(revids)
    if not isinstance(actual, Mapping) or set(actual) != set(revids):
        raise ValueError("Page replay revision inventory mismatch")
    for row in rows:
        identity = actual[row["revision_id"]]
        if not isinstance(identity, Mapping) or set(identity) != {
            "title", "timestamp", "mediawiki_sha1"
        }:
            raise ValueError("Page replay identity schema drift")
        if any(identity[key] != row[key] for key in ("title", "timestamp", "mediawiki_sha1")):
            raise ValueError("Page pinned revision identity drift")
    canonical = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "receipt_version": REPLAY_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_family_id": SOURCE_FAMILY_1927,
        "page_revision_count": len(rows),
        "manifest_sha256": sha256(canonical.encode("utf-8")).hexdigest(),
        "identity_replay_match": True,
        "source_text_included": False,
        "literary_body_frozen": False,
        "single_edition_body_ready": False,
        "fantlab_input_identity": "unknown",
        "m2_parity_admissible": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    capture = commands.add_parser("capture")
    capture.add_argument("--manifest", type=Path, required=True)
    replay = commands.add_parser("replay")
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "capture":
            payload = build_manifest()
            destination = args.manifest
        else:
            payload = replay_manifest(json.loads(args.manifest.read_text(encoding="utf-8")))
            destination = args.receipt
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except Exception:
        # No exception string/traceback: provider errors can contain sensitive text.
        print("Paris Page identity operation failed; no validated receipt.", file=sys.stderr)
        return 2
    print(f"Validated Paris Page revision identities: {EXPECTED_PAGE_COUNT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
