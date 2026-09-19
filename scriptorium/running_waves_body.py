"""Freeze and replay the literary-body identity for Grin's *Running on Waves*.

The source text is fetched only transiently from the 36 exact revisions already
frozen by ``running_waves_revisions``.  Durable output contains only source
identities, derived counts/digests, and the versioned extraction/composition
contract; literary prose is never serialized.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from .running_waves_inventory import CANDIDATE_ID, PRIMARY_BIBLIOGRAPHIC_SOURCE
from .running_waves_revisions import canonical_json_text, validate_manifest as validate_source_manifest
from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import COMPOSITE_PROFILE, extract_transcription_body
from .wikisource_replay import fetch_pinned_chapter_revisions

MANIFEST_VERSION = "scriptorium-running-waves-literary-body-v1"
EXTRACTION_PROFILE = "scriptorium-running-waves-wikisource-body-v1"
CHAPTER_SEPARATOR = "\n\n"
MINIMUM_CORPUS_CHARACTERS = 300_000


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def source_manifest_sha256(source_manifest: Mapping[str, object]) -> str:
    """Bind the body identity to the canonical source-revision manifest."""

    return _sha256_text(canonical_json_text(source_manifest))


def _text_identity(text: str) -> dict[str, object]:
    raw = text.encode("utf-8")
    normalized = normalize_text(text)
    return {
        "character_count_including_spaces": len(text),
        "utf8_byte_count": len(raw),
        "raw_sha256": sha256(raw).hexdigest(),
        "normalization_profile": NORMALIZATION_PROFILE,
        "normalized_character_count_including_spaces": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }


def _extract_bodies(
    source_manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]],
) -> tuple[tuple[dict[str, object], ...], list[str]]:
    identities = validate_source_manifest(source_manifest)
    fetched = fetcher(identities)
    expected_titles = {str(row["title"]) for row in identities}
    if set(fetched) != expected_titles:
        raise ValueError("pinned literary-page replay inventory mismatch")

    bodies: list[str] = []
    for row in identities:
        title = str(row["title"])
        try:
            body = extract_transcription_body(fetched[title])
        except ValueError as exc:
            raise ValueError(f"failed to extract literary body for {title!r}: {exc}") from exc
        bodies.append(body)
    return identities, bodies


def build_manifest(
    source_manifest: Mapping[str, object],
    *,
    fetcher: Callable[
        [Iterable[Mapping[str, object]]], dict[str, str]
    ] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Build a source-free literary-body manifest from exact pinned revisions."""

    identities, bodies = _extract_bodies(source_manifest, fetcher=fetcher)
    per_page: list[dict[str, object]] = []
    for identity, body in zip(identities, bodies, strict=True):
        per_page.append(
            {
                "ordinal": identity["ordinal"],
                "title": identity["title"],
                "revision_id": identity["revision_id"],
                **_text_identity(body),
            }
        )

    composite = CHAPTER_SEPARATOR.join(bodies)
    composite_identity = {
        "literary_page_count": len(bodies),
        **_text_identity(composite),
    }
    character_count = int(composite_identity["character_count_including_spaces"])
    if character_count < MINIMUM_CORPUS_CHARACTERS:
        raise ValueError(
            "Running on Waves literary body is below the calibration threshold: "
            f"{character_count} < {MINIMUM_CORPUS_CHARACTERS}"
        )

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "bibliographic_source": PRIMARY_BIBLIOGRAPHIC_SOURCE,
        "source_revision_manifest_version": source_manifest.get("manifest_version"),
        "source_revision_manifest_sha256": source_manifest_sha256(source_manifest),
        "composition": {
            "profile": COMPOSITE_PROFILE,
            "extraction_profile": EXTRACTION_PROFILE,
            "order": "exact frozen route order /1 through /35 then /Эпилог",
            "literary_page_count": len(bodies),
            "chapter_separator": "\\n\\n",
            "source_text_committed": False,
        },
        "per_page_identities": per_page,
        "composite_identity": composite_identity,
        "corpus_admission": {
            "minimum_character_count_including_spaces": MINIMUM_CORPUS_CHARACTERS,
            "character_threshold_met": True,
            "general_calibration_profile_admissible": True,
            "fantlab_source_edition_match": "unknown",
            "m2_parity_admissible": False,
        },
    }


def validate_manifest(
    manifest: Mapping[str, object], source_manifest: Mapping[str, object]
) -> tuple[dict[str, object], ...]:
    """Validate source binding and all source-free body-manifest invariants."""

    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Running on Waves literary-body manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected candidate id")
    if manifest.get("bibliographic_source") != PRIMARY_BIBLIOGRAPHIC_SOURCE:
        raise ValueError("bibliographic source drift")
    if manifest.get("source_revision_manifest_version") != source_manifest.get("manifest_version"):
        raise ValueError("source revision manifest version drift")
    if manifest.get("source_revision_manifest_sha256") != source_manifest_sha256(source_manifest):
        raise ValueError("source revision manifest digest drift")

    source_identities = validate_source_manifest(source_manifest)
    composition = manifest.get("composition")
    if composition != {
        "profile": COMPOSITE_PROFILE,
        "extraction_profile": EXTRACTION_PROFILE,
        "order": "exact frozen route order /1 through /35 then /Эпилог",
        "literary_page_count": 36,
        "chapter_separator": "\\n\\n",
        "source_text_committed": False,
    }:
        raise ValueError("literary-body composition contract drift")

    rows = manifest.get("per_page_identities")
    if not isinstance(rows, list) or len(rows) != 36:
        raise ValueError("literary-body manifest must contain exactly 36 page identities")
    for source, row in zip(source_identities, rows, strict=True):
        if not isinstance(row, dict):
            raise ValueError("per-page identity must be an object")
        for key in ("ordinal", "title", "revision_id"):
            if row.get(key) != source.get(key):
                raise ValueError(f"per-page source binding drift for {key}")
        _validate_text_identity(row, label=str(source["title"]))

    composite = manifest.get("composite_identity")
    if not isinstance(composite, dict) or composite.get("literary_page_count") != 36:
        raise ValueError("invalid composite identity")
    _validate_text_identity(composite, label="composite")
    count = composite.get("character_count_including_spaces")
    if not isinstance(count, int) or count < MINIMUM_CORPUS_CHARACTERS:
        raise ValueError("composite no longer clears the corpus character threshold")

    admission = manifest.get("corpus_admission")
    if admission != {
        "minimum_character_count_including_spaces": MINIMUM_CORPUS_CHARACTERS,
        "character_threshold_met": True,
        "general_calibration_profile_admissible": True,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }:
        raise ValueError("corpus-admission boundary drift")
    return source_identities


def _validate_text_identity(identity: Mapping[str, object], *, label: str) -> None:
    integer_keys = (
        "character_count_including_spaces",
        "utf8_byte_count",
        "normalized_character_count_including_spaces",
    )
    for key in integer_keys:
        value = identity.get(key)
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"invalid {label} {key}")
    if identity.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError(f"unexpected {label} normalization profile")
    for key in ("raw_sha256", "normalized_sha256"):
        value = identity.get(key)
        if not isinstance(value, str) or len(value) != 64:
            raise ValueError(f"invalid {label} {key}")
        try:
            int(value, 16)
        except ValueError as exc:
            raise ValueError(f"invalid {label} {key}") from exc


def replay_manifest(
    manifest: Mapping[str, object],
    source_manifest: Mapping[str, object],
    *,
    fetcher: Callable[
        [Iterable[Mapping[str, object]]], dict[str, str]
    ] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Re-fetch exact revisions and verify every derived body identity."""

    identities = validate_manifest(manifest, source_manifest)
    _, bodies = _extract_bodies(source_manifest, fetcher=fetcher)
    expected_rows = manifest["per_page_identities"]
    assert isinstance(expected_rows, list)
    for identity, body, expected in zip(identities, bodies, expected_rows, strict=True):
        observed = {
            "ordinal": identity["ordinal"],
            "title": identity["title"],
            "revision_id": identity["revision_id"],
            **_text_identity(body),
        }
        if observed != expected:
            raise ValueError(f"frozen literary-page identity drift for {identity['title']!r}")

    composite = CHAPTER_SEPARATOR.join(bodies)
    observed_composite = {
        "literary_page_count": len(bodies),
        **_text_identity(composite),
    }
    if observed_composite != manifest.get("composite_identity"):
        raise ValueError("frozen Running on Waves composite identity drift")

    return {
        "verified": True,
        "candidate_id": CANDIDATE_ID,
        "verified_literary_page_count": len(bodies),
        "character_count_including_spaces": len(composite),
        "source_text_committed": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze/replay Running on Waves literary body.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--source-manifest", type=Path, required=True)
    capture.add_argument("--output", type=Path, required=True)
    replay = subparsers.add_parser("replay")
    replay.add_argument("--source-manifest", type=Path, required=True)
    replay.add_argument("--body-manifest", type=Path, required=True)
    args = parser.parse_args(argv)

    source_manifest = _load_object(args.source_manifest)
    if args.command == "capture":
        manifest = build_manifest(source_manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return 0

    body_manifest = _load_object(args.body_manifest)
    replay_manifest(body_manifest, source_manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
