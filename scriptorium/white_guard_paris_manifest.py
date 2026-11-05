"""Reviewable, source-free snapshot of 185 Paris 1927 ProofreadPage identities.

The hosted current-revision capture is non-atomic and does not establish the
historical parent transclusion, literary body, corpus admission or FantLab parity.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
from io import StringIO
from pathlib import Path
import re
import sys
from typing import Callable, Mapping

from .white_guard_page_identities import EXPECTED_RANGES, PAGE_PREFIX
from .white_guard_revisions import SOURCE_FAMILY_1927, canonical_json_text, fetch_pinned_revision_identities

SCHEMA_VERSION = "scriptorium-white-guard-paris-page-manifest-v1"
CSV_PATH = Path(__file__).resolve().parent.parent / "corpus/candidates/white_guard_paris_1927_pages.csv"
CSV_SHA256 = "f2f2ea90a65ffb99b5cd12e64f20c15f16f6a2d7ca600cd7084488f311f81c02"
SOURCE_JSON_SHA256 = "baf64a30cad23740dd0a6a1d51599f6bb7343f99922cf87efcd658f08042dc0f"
CAPTURE_RUN = 41959859796
CAPTURE_ARTIFACT = 13383909900
CAPTURE_COMMIT = "1eb66bc069a02c3997b65330930931e29aacf88b"
COLUMNS = ("page_number", "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1")
_TIMESTAMP = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\Z")
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")


def parse_rows(raw: str) -> tuple[dict[str, object], ...]:
    """Validate exact layout and immutable identity fields; no book content."""
    rows = list(csv.reader(StringIO(raw, newline=""), strict=True))
    if not rows or tuple(rows[0]) != COLUMNS or len(rows) != 186:
        raise ValueError("Paris snapshot columns or length mismatch")
    chapters = {n: chapter for chapter, (first, last) in enumerate(EXPECTED_RANGES, 1)
                for n in range(first, last + 1)}
    if set(chapters) != set(range(5, 190)):
        raise ValueError("unexpected Paris dependency topology")
    result = []
    for n, values in enumerate(rows[1:], start=5):
        if len(values) != len(COLUMNS):
            raise ValueError("invalid Page snapshot row width")
        page_number, page_id, revision_id, timestamp, digest = values
        if (page_number != str(n) or not page_id.isascii() or not page_id.isdecimal()
                or not revision_id.isascii() or not revision_id.isdecimal()
                or not int(page_id) > 0 or not int(revision_id) > 0
                or not _TIMESTAMP.fullmatch(timestamp) or not _SHA1.fullmatch(digest)):
            raise ValueError("invalid Page snapshot identity")
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if parsed.tzinfo != timezone.utc:
                raise ValueError("non-UTC Page timestamp")
        except ValueError:
            raise ValueError("invalid Page snapshot timestamp") from None
        result.append({"chapter": chapters[n], "page_number": n,
                       "title": f"{PAGE_PREFIX}{n}", "page_id": int(page_id),
                       "revision_id": int(revision_id), "revision_timestamp": timestamp,
                       "mediawiki_sha1": digest})
    if (len({r["page_id"] for r in result}) != 185
            or len({r["revision_id"] for r in result}) != 185):
        raise ValueError("duplicate Page identity")
    return tuple(result)


def load_rows(path: Path = CSV_PATH) -> tuple[dict[str, object], ...]:
    raw = path.read_bytes()
    if len(raw) > 20_000 or sha256(raw).hexdigest() != CSV_SHA256:
        raise ValueError("Paris Page snapshot hash mismatch")
    try:
        decoded = raw.decode("utf-8", "strict")
    except UnicodeError:
        raise ValueError("invalid Page snapshot encoding") from None
    return parse_rows(decoded)


def verify_rows(
    rows: tuple[dict[str, object], ...],
    *, replayer: Callable[..., Mapping[str, Mapping[str, object]]] = fetch_pinned_revision_identities,
) -> None:
    """Replay immutable oldids only; the provider requests no source text."""
    expected = tuple({key: r[key] for key in (
        "title", "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1"
    )} for r in rows)
    observed = replayer(expected)
    if not isinstance(observed, Mapping) or set(observed) != {r["title"] for r in expected}:
        raise ValueError("incomplete pinned Page replay")
    for row in expected:
        if observed[row["title"]] != {k: row[k] for k in (
                "page_id", "revision_id", "revision_timestamp", "mediawiki_sha1")}:
            raise ValueError("pinned Page replay drift")


def build_receipt(*, verify_provider: bool = False,
                  loader: Callable[[], tuple[dict[str, object], ...]] = load_rows,
                  verifier: Callable[[tuple[dict[str, object], ...]], None] = verify_rows,
                  ) -> dict[str, object]:
    rows = loader()
    if verify_provider:
        verifier(rows)
    return {
        "schema_version": SCHEMA_VERSION,
        "source_family_id": SOURCE_FAMILY_1927,
        "page_count": len(rows),
        "chapter_count": len(EXPECTED_RANGES),
        "page_manifest_sha256": CSV_SHA256,
        "original_capture_json_sha256": SOURCE_JSON_SHA256,
        "capture_workflow_run": CAPTURE_RUN,
        "capture_artifact_id": CAPTURE_ARTIFACT,
        "capture_commit": CAPTURE_COMMIT,
        "captured_page_replay": "VERIFIED_AT_CAPTURE",
        "recheck": "VERIFIED_IDENTITIES" if verify_provider else "NOT_RUN",
        "historical_transclusion_proven": False,
        "single_edition_body_frozen": False,
        "fantlab_input_identity": "unknown",
        "m2_parity_admissible": False,
        "source_text_committed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-provider", action="store_true", help="replay 185 oldids without fetching prose")
    args = parser.parse_args(argv)
    try:
        receipt = build_receipt(verify_provider=args.verify_provider)
    except Exception:
        print("Pinned Paris Page manifest validation failed; no receipt issued.", file=sys.stderr)
        return 2
    print(canonical_json_text(receipt), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
