"""Freeze and replay the 129-chapter Russian Wikisource Resurrection candidate.

The committed manifest produced by this module is source-free: source wikitext and
rendered prose are used transiently to derive immutable identities but are never
serialized into the repository artifact.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence
from urllib.parse import quote

from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import (
    COMPOSITE_PROFILE,
    EXTRACTION_PROFILE,
    extract_transcription_body,
    fetch_current_chapter_revisions,
    roman,
)
from .wikisource_replay import fetch_pinned_chapter_revisions


CANDIDATE_ID = "tolstoy-resurrection-ru"
WORK_BASE_TITLE = "Воскресение (Толстой)"
PART_CHAPTER_COUNTS = (59, 42, 28)
MANIFEST_VERSION = "scriptorium-source-revision-manifest-v1"
SOURCE_WORK_URL = "https://ru.wikisource.org/wiki/Воскресение_(Толстой)"
SOURCE_WORK_INDEX_REVISION_ID = 5614128
BIBLIOGRAPHIC_SOURCE = (
    "Л. Н. Толстой. Собрание сочинений в восьми томах. Т. 6. "
    "М., \"Лексика\", 1996."
)


def expected_chapters() -> tuple[dict[str, object], ...]:
    chapters: list[dict[str, object]] = []
    ordinal = 0
    for part, count in enumerate(PART_CHAPTER_COUNTS, start=1):
        for chapter in range(1, count + 1):
            ordinal += 1
            chapters.append(
                {
                    "ordinal": ordinal,
                    "part": part,
                    "chapter": chapter,
                    "title": (
                        f"{WORK_BASE_TITLE}/Часть {roman(part)}/Глава {roman(chapter)}"
                    ),
                }
            )
    if ordinal != 129:
        raise AssertionError(f"chapter contract drift: expected 129, got {ordinal}")
    return tuple(chapters)


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def _composite_identity(composite: str) -> dict[str, object]:
    normalized = normalize_text(composite)
    raw = composite.encode("utf-8")
    return {
        "chapter_count": 129,
        "character_count_including_spaces": len(composite),
        "utf8_byte_count": len(raw),
        "raw_sha256": sha256(raw).hexdigest(),
        "normalization_profile": NORMALIZATION_PROFILE,
        "normalized_character_count_including_spaces": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }


def build_manifest(
    *,
    fetcher: Callable[
        [Iterable[dict[str, object]]], dict[str, dict[str, object]]
    ] = fetch_current_chapter_revisions,
) -> dict[str, object]:
    """Capture current chapter identities and immutable derived hashes."""

    chapters = expected_chapters()
    revisions = fetcher(chapters)
    rows: list[dict[str, object]] = []
    bodies: list[str] = []
    revision_ids: set[int] = set()

    for chapter in chapters:
        title = str(chapter["title"])
        revision = revisions[title]
        revision_id = int(revision["revision_id"])
        if revision_id in revision_ids:
            raise ValueError(f"duplicate revision id {revision_id}")
        revision_ids.add(revision_id)
        wikitext = str(revision["wikitext"])
        body = extract_transcription_body(wikitext)
        bodies.append(body)
        rows.append(
            {
                **chapter,
                "revision_id": revision_id,
                "revision_timestamp": str(revision["timestamp"]),
                "permanent_url": (
                    "https://ru.wikisource.org/w/index.php?title="
                    f"{quote(title.replace(' ', '_'), safe='()/_')}&oldid={revision_id}"
                ),
                "mediawiki_sha1": str(revision["mediawiki_sha1"]),
                "wikitext_sha256": _sha256_text(wikitext),
                "extracted_character_count": len(body),
                "extracted_sha256": _sha256_text(body),
            }
        )

    composite = "\n\n".join(bodies)
    if len(rows) != 129:
        raise AssertionError(f"expected 129 chapters, got {len(rows)}")
    if len(composite) < 300_000:
        raise ValueError(f"composite below corpus threshold: {len(composite)} characters")

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_work_url": SOURCE_WORK_URL,
        "source_work_index_revision_id": SOURCE_WORK_INDEX_REVISION_ID,
        "bibliographic_source": BIBLIOGRAPHIC_SOURCE,
        "legal_basis": "public_domain",
        "composition": {
            "profile": COMPOSITE_PROFILE,
            "extraction_profile": EXTRACTION_PROFILE,
            "order": "part ascending, then chapter ascending, from the frozen 3-part/129-chapter contract",
            "chapter_separator": "\\n\\n",
            "source_text_committed": False,
            "part_chapter_counts": list(PART_CHAPTER_COUNTS),
        },
        "chapters": rows,
        "composite_identity": _composite_identity(composite),
    }


def _validated_rows(manifest: Mapping[str, object]) -> tuple[Mapping[str, object], ...]:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Resurrection revision-manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Resurrection candidate id")
    composition = manifest.get("composition")
    if not isinstance(composition, dict):
        raise ValueError("revision manifest missing composition")
    if composition.get("profile") != COMPOSITE_PROFILE:
        raise ValueError("unexpected composite profile")
    if composition.get("extraction_profile") != EXTRACTION_PROFILE:
        raise ValueError("unexpected extraction profile")
    if composition.get("part_chapter_counts") != list(PART_CHAPTER_COUNTS):
        raise ValueError("Resurrection chapter-count contract drift")
    if composition.get("source_text_committed") is not False:
        raise ValueError("source-text boundary drift")

    rows = manifest.get("chapters")
    if not isinstance(rows, list):
        raise ValueError("revision manifest missing chapters")
    expected = expected_chapters()
    if len(rows) != len(expected):
        raise ValueError(f"expected {len(expected)} chapter rows, got {len(rows)}")

    revision_ids: set[int] = set()
    validated: list[Mapping[str, object]] = []
    for expected_row, row in zip(expected, rows, strict=True):
        if not isinstance(row, dict):
            raise ValueError("chapter rows must be objects")
        for key in ("ordinal", "part", "chapter", "title"):
            if row.get(key) != expected_row[key]:
                raise ValueError(
                    f"chapter contract drift at ordinal {expected_row['ordinal']}: {key}"
                )
        revision_id = row.get("revision_id")
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError(f"invalid revision id at {expected_row['title']!r}")
        if revision_id in revision_ids:
            raise ValueError(f"duplicate revision id {revision_id}")
        revision_ids.add(revision_id)
        for key, width in (
            ("mediawiki_sha1", 40),
            ("wikitext_sha256", 64),
            ("extracted_sha256", 64),
        ):
            value = row.get(key)
            if not isinstance(value, str) or len(value) != width:
                raise ValueError(f"invalid {key} at {expected_row['title']!r}")
            try:
                int(value, 16)
            except ValueError as exc:
                raise ValueError(f"invalid {key} at {expected_row['title']!r}") from exc
        if not isinstance(row.get("revision_timestamp"), str):
            raise ValueError(f"missing revision timestamp at {expected_row['title']!r}")
        if not isinstance(row.get("extracted_character_count"), int):
            raise ValueError(f"missing extracted character count at {expected_row['title']!r}")
        validated.append(row)
    return tuple(validated)


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Replay exact recorded revisions and return a source-free verification receipt."""

    rows = _validated_rows(manifest)
    identities = tuple(
        {
            "title": row["title"],
            "revision_id": row["revision_id"],
            "revision_timestamp": row["revision_timestamp"],
            "mediawiki_sha1": row["mediawiki_sha1"],
        }
        for row in rows
    )
    revisions = fetcher(identities)
    bodies: list[str] = []
    for row in rows:
        title = str(row["title"])
        wikitext = revisions[title]
        if _sha256_text(wikitext) != row["wikitext_sha256"]:
            raise ValueError(f"wikitext SHA-256 drift for {title!r}")
        body = extract_transcription_body(wikitext)
        if len(body) != row["extracted_character_count"]:
            raise ValueError(f"extracted character-count drift for {title!r}")
        if _sha256_text(body) != row["extracted_sha256"]:
            raise ValueError(f"extracted SHA-256 drift for {title!r}")
        bodies.append(body)

    composite = "\n\n".join(bodies)
    observed = _composite_identity(composite)
    expected_identity = manifest.get("composite_identity")
    if not isinstance(expected_identity, dict):
        raise ValueError("revision manifest missing composite_identity")
    for key, value in observed.items():
        if expected_identity.get(key) != value:
            raise ValueError(
                f"frozen composite identity drift for {key}: "
                f"observed {value!r}, expected {expected_identity.get(key)!r}"
            )

    return {
        "receipt_version": "scriptorium-resurrection-replay-receipt-v1",
        "candidate_id": CANDIDATE_ID,
        "chapter_count": len(rows),
        "composite_identity": observed,
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser("capture", help="capture current source-free revision manifest")
    capture.add_argument("--output", type=Path, required=True)

    replay = subparsers.add_parser("replay", help="replay an existing pinned manifest")
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)

    args = parser.parse_args(argv)
    if args.command == "capture":
        _write_json(args.output, build_manifest())
        return 0

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("revision manifest must be a JSON object")
    _write_json(args.receipt, replay_manifest(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
