"""Prepare a source-verified, ephemeral pylem request for Grin's Running on Waves.

The original prose is downloaded from 36 pinned Wikisource revisions, checked
against every frozen page hash and the whole-book identity, then written only to
an ephemeral local request. No literary source is included in published results.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from .analyze import _write_new
from .pylem_transport import build_sidecar_request
from .running_waves_body import (
    CHAPTER_SEPARATOR,
    _extract_bodies,
    replay_manifest,
)
from .wikisource_replay import fetch_pinned_chapter_revisions


def prepare_running_waves_request(
    source_manifest: Mapping[str, object],
    body_manifest: Mapping[str, object],
    *,
    fetcher: Callable[
        [Iterable[Mapping[str, object]]], dict[str, str]
    ] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Return a request only after the *complete* frozen source has replayed.

    Reuse the exact data returned to the trusted replay, without making a
    second network request or trusting a partially verified book.
    """
    captured: dict[str, str] | None = None

    def capture(identities: Iterable[Mapping[str, object]]) -> dict[str, str]:
        nonlocal captured
        if captured is not None:
            raise ValueError("Running on Waves fetch repeated unexpectedly")
        records = fetcher(identities)
        if not isinstance(records, dict) or any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in records.items()
        ):
            raise ValueError("invalid pinned Running on Waves page inventory")
        captured = records
        return records

    witness = replay_manifest(body_manifest, source_manifest, fetcher=capture)
    if witness.get("verified") is not True or captured is None:
        raise ValueError("frozen Running on Waves replay was not verified")
    _, bodies = _extract_bodies(
        source_manifest,
        fetcher=lambda _identities: captured,
    )
    request = build_sidecar_request(CHAPTER_SEPARATOR.join(bodies))
    expected = body_manifest["composite_identity"]
    if (
        request["normalized_sha256"] != expected["normalized_sha256"]
        or len(request["normalized_text"]) != expected["normalized_character_count_including_spaces"]
    ):
        raise ValueError("Running on Waves pinned normalized body identity drift")
    if not request["tokens"]:
        raise ValueError("verified book has no Scriptorium word tokens")
    return request


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("pinned Running on Waves manifest must be a JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prepare a verified, ephemeral full-work pylem request; do not upload it"
    )
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--body-manifest", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args(argv)

    request = prepare_running_waves_request(
        _load_object(args.source_manifest), _load_object(args.body_manifest)
    )
    # Create-only: never overwrite an earlier native input or symlink.
    rendered = json.dumps(request, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    try:
        _write_new(args.request, rendered)
    except FileExistsError:
        parser.error("ephemeral request already exists; choose a fresh path")
    except OSError:
        parser.error("ephemeral request destination unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
