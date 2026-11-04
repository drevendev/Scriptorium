"""Replay the reviewed White Guard manifest; never refresh it implicitly.

The pinned bytes identify 20 revisions from two print-source families. They do
not establish a literary body, a single edition, or a FantLab analyzer input.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import stat
import sys
from typing import Callable

from . import white_guard_revisions as revisions

SCHEMA_VERSION = "scriptorium-white-guard-delivery-v1"
MANIFEST_SHA256 = "094fddd834667be7a0e03eda141efc2d68235506351a421681e6c6e80353836c"
MANIFEST_PATH = "corpus/candidates/source-edition-traces/bulgakov-white-guard-ru.source-revisions.json"
MAX_MANIFEST_BYTES = 65536
_FORBIDDEN = frozenset({"wikitext", "content", "body", "text", "source_text"})


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate manifest JSON key")
        result[key] = value
    return result


def _reject_constant(_: str) -> None:
    raise ValueError("nonfinite manifest number")


def _source_free(value: object) -> None:
    if isinstance(value, dict):
        if _FORBIDDEN.intersection(value):
            raise ValueError("source prose is forbidden in the identity manifest")
        for child in value.values():
            _source_free(child)
    elif isinstance(value, list):
        for child in value:
            _source_free(child)


def parse_manifest(raw: bytes) -> dict[str, object]:
    """Validate the existing canonical schema, without claiming provider replay."""
    if not isinstance(raw, bytes) or not 0 < len(raw) <= MAX_MANIFEST_BYTES:
        raise ValueError("invalid manifest byte length")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_pairs,
                           parse_constant=_reject_constant)
        if not isinstance(value, dict):
            raise ValueError("manifest must be an object")
        _source_free(value)
        revisions.validate_manifest(value)
    except (UnicodeError, RecursionError, TypeError) as exc:
        raise ValueError("invalid manifest structure or encoding") from exc
    return value


def load_manifest(path: Path) -> dict[str, object]:
    """Bounded regular-file read, then byte pin and canonical semantic checks."""
    path = Path(path)
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError("manifest symlinks are not permitted")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_MANIFEST_BYTES:
            raise ValueError("manifest must be a bounded regular file")
        with os.fdopen(fd, "rb") as stream:
            fd = None
            raw = stream.read(MAX_MANIFEST_BYTES + 1)
    finally:
        if fd is not None:
            os.close(fd)
    if len(raw) > MAX_MANIFEST_BYTES or sha256(raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError("reviewed manifest bytes changed; explicit re-admission required")
    return parse_manifest(raw)


def build_receipt(path: Path, *, offline: bool = False,
                  query: Callable[[dict[str, str]], dict[str, object]] | None = None) -> dict[str, object]:
    """Offline inventory is NOT_RUN; live mode requests only the committed IDs."""
    manifest = load_manifest(path)
    identities = revisions.validate_manifest(manifest)
    if not offline:
        if query is None:
            revisions.fetch_pinned_revision_identities(identities)
        else:
            revisions.fetch_pinned_revision_identities(identities, query=query)
    counts = Counter(row["source_family_id"] for row in manifest["pages"])
    return {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": revisions.CANDIDATE_ID,
        "manifest_version": revisions.MANIFEST_VERSION,
        "manifest_sha256": MANIFEST_SHA256,
        "mode": "offline_inventory" if offline else "pinned_replay",
        "provider_replay": "NOT_RUN" if offline else "VERIFIED",
        "revision_count": len(identities),
        "source_partition_counts": dict(sorted(counts.items())),
        "source_text_committed": False,
        "literary_body_extraction_frozen": False,
        "single_edition_identity": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(MANIFEST_PATH))
    parser.add_argument("--offline", action="store_true",
                        help="Verify retained bytes and schema without provider access (NOT_RUN)")
    args = parser.parse_args(argv)
    try:
        receipt = build_receipt(args.manifest, offline=args.offline)
    except (OSError, ValueError):
        print("White Guard identity verification failed; no receipt issued.", file=sys.stderr)
        return 2
    print(revisions.canonical_json_text(receipt), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
