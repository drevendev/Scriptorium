"""Freeze and replay the 129-chapter Russian Wikisource Resurrection candidate.

The durable manifest is deliberately source-free. Current wikitext and extracted
prose are used transiently during capture to derive immutable identities but are
never serialized. Replay fetches the exact pinned revisions, verifies MediaWiki
identity, reconstructs the text with the versioned extraction contract and checks
one immutable composite identity.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, Sequence

from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import (
    COMPOSITE_PROFILE,
    extract_transcription_body,
    fetch_current_chapter_revisions,
    roman,
)
from .wikisource_replay import fetch_pinned_chapter_revisions


CANDIDATE_ID = "tolstoy-resurrection-ru"
WORK_BASE_TITLE = "Воскресение (Толстой)"
PART_CHAPTER_COUNTS = (59, 42, 28)
MANIFEST_VERSION = "scriptorium-resurrection-source-revision-packed-manifest-v1"
EXTRACTION_PROFILE = "scriptorium-wikisource-resurrection-body-v1"
SOURCE_WORK_URL = "https://ru.wikisource.org/wiki/Воскресение_(Толстой)"
SOURCE_WORK_INDEX_REVISION_ID = 5614128
BIBLIOGRAPHIC_SOURCE = (
    "Л. Н. Толстой. Собрание сочинений в восьми томах. Т. 6. "
    "М., \"Лексика\", 1996."
)
_BODY_DIV_RE = re.compile(
    r'<div\s+class=["\'](?:text|indent)["\']\s*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
_NOINCLUDE_RE = re.compile(r"<noinclude>.*?</noinclude>", re.IGNORECASE | re.DOTALL)
_HEADER_TEMPLATE_RE = re.compile(r"^\s*\{\{Отексте\b.*?\}\}", re.IGNORECASE | re.DOTALL)
_HEADING_RE = re.compile(r"={2,6}\s*[^=\n]+?\s*={2,6}")
_CATEGORY_RE = re.compile(r"\[\[Категория:[^\]]+\]\]\s*$", re.IGNORECASE | re.DOTALL)
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def expected_chapters() -> tuple[dict[str, object], ...]:
    """Return the frozen three-part / 129-chapter title contract."""

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


def _strip_page_scaffolding(wikitext: str) -> str:
    source = _NOINCLUDE_RE.sub("", wikitext)
    source = _HEADER_TEMPLATE_RE.sub("", source, count=1)
    source = source.replace("__NOEDITSECTION__", "")
    source = _HEADING_RE.sub("", source)
    source = _CATEGORY_RE.sub("", source)
    return source.strip()


def extract_resurrection_body(wikitext: str) -> str:
    """Render one chapter across the two observed Resurrection page shapes.

    The transcription mixes pages that wrap prose in one or more ``text``/``indent``
    divs with pages whose prose follows the ``Отексте`` header directly. Both routes
    reuse the existing fail-closed Wikisource sanitizer after the page scaffolding is
    selected explicitly.
    """

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    source = _NOINCLUDE_RE.sub("", wikitext)
    matches = _BODY_DIV_RE.findall(source)
    if matches:
        rendered = [
            extract_transcription_body(f'<div class="text">{fragment}</div>')
            for fragment in matches
        ]
        return "\n\n".join(rendered)

    plain = _strip_page_scaffolding(source)
    if not plain:
        raise ValueError("empty Resurrection transcription after page-scaffolding removal")
    return extract_transcription_body(f'<div class="text">{plain}</div>')


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
    """Capture source identities and a composite text identity without source prose."""

    chapters = expected_chapters()
    revisions = fetcher(chapters)
    revision_ids: list[int] = []
    revision_timestamps: list[str] = []
    mediawiki_sha1s: list[str] = []
    bodies: list[str] = []
    seen_revision_ids: set[int] = set()

    for chapter in chapters:
        title = str(chapter["title"])
        revision = revisions[title]
        revision_id = int(revision["revision_id"])
        if revision_id <= 0 or revision_id in seen_revision_ids:
            raise ValueError(f"invalid or duplicate revision id {revision_id}")
        seen_revision_ids.add(revision_id)
        timestamp = str(revision["timestamp"])
        mediawiki_sha1 = str(revision["mediawiki_sha1"]).lower()
        if not _HEX40_RE.fullmatch(mediawiki_sha1):
            raise ValueError(f"invalid MediaWiki SHA-1 for {title!r}")
        try:
            body = extract_resurrection_body(str(revision["wikitext"]))
        except ValueError as exc:
            raise ValueError(f"failed to extract {title!r}: {exc}") from exc

        revision_ids.append(revision_id)
        revision_timestamps.append(timestamp)
        mediawiki_sha1s.append(mediawiki_sha1)
        bodies.append(body)

    composite = "\n\n".join(bodies)
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
        "chapter_identity_encoding": {
            "chapter_count": len(chapters),
            "titles": "deterministic_from_part_chapter_counts",
            "revision_ids": revision_ids,
            "revision_timestamps": revision_timestamps,
            "mediawiki_sha1_hex_concat": "".join(mediawiki_sha1s),
        },
        "composite_identity": _composite_identity(composite),
    }


def _validate_manifest(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
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
    if composition.get("chapter_separator") != "\\n\\n":
        raise ValueError("unexpected chapter separator")
    if composition.get("source_text_committed") is not False:
        raise ValueError("source-text boundary drift")

    chapters = expected_chapters()
    encoding = manifest.get("chapter_identity_encoding")
    if not isinstance(encoding, dict):
        raise ValueError("revision manifest missing chapter_identity_encoding")
    count = len(chapters)
    if encoding.get("chapter_count") != count:
        raise ValueError("packed chapter count drift")
    if encoding.get("titles") != "deterministic_from_part_chapter_counts":
        raise ValueError("packed title encoding drift")

    revision_ids = encoding.get("revision_ids")
    timestamps = encoding.get("revision_timestamps")
    sha_concat = encoding.get("mediawiki_sha1_hex_concat")
    if not isinstance(revision_ids, list) or len(revision_ids) != count:
        raise ValueError("invalid packed revision_ids")
    if not isinstance(timestamps, list) or len(timestamps) != count:
        raise ValueError("invalid packed revision_timestamps")
    if not isinstance(sha_concat, str) or len(sha_concat) != count * 40:
        raise ValueError("invalid packed mediawiki_sha1 length")
    if not re.fullmatch(r"[0-9a-f]+", sha_concat):
        raise ValueError("invalid packed mediawiki_sha1 hex")

    seen_revision_ids: set[int] = set()
    identities: list[dict[str, object]] = []
    for index, chapter in enumerate(chapters):
        revision_id = revision_ids[index]
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError("invalid packed revision id")
        if revision_id in seen_revision_ids:
            raise ValueError(f"duplicate revision id {revision_id}")
        seen_revision_ids.add(revision_id)
        timestamp = timestamps[index]
        if not isinstance(timestamp, str) or not timestamp:
            raise ValueError("invalid packed revision timestamp")
        mediawiki_sha1 = sha_concat[index * 40 : (index + 1) * 40]
        identities.append(
            {
                "title": chapter["title"],
                "revision_id": revision_id,
                "revision_timestamp": timestamp,
                "mediawiki_sha1": mediawiki_sha1,
            }
        )

    composite = manifest.get("composite_identity")
    if not isinstance(composite, dict):
        raise ValueError("revision manifest missing composite_identity")
    if composite.get("chapter_count") != count:
        raise ValueError("composite chapter-count drift")
    if composite.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError("unexpected normalization profile")
    for key in (
        "character_count_including_spaces",
        "normalized_character_count_including_spaces",
        "utf8_byte_count",
    ):
        value = composite.get(key)
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"invalid composite {key}")
    if int(composite["character_count_including_spaces"]) < 300_000:
        raise ValueError("frozen candidate fell below corpus threshold")
    for key in ("raw_sha256", "normalized_sha256"):
        value = composite.get(key)
        if not isinstance(value, str) or not _HEX64_RE.fullmatch(value):
            raise ValueError(f"invalid composite {key}")

    return tuple(identities)


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Replay exact revisions and return only source-free verification evidence."""

    identities = _validate_manifest(manifest)
    revisions = fetcher(identities)
    bodies = [extract_resurrection_body(revisions[str(row["title"])]) for row in identities]
    observed = _composite_identity("\n\n".join(bodies))
    expected = manifest["composite_identity"]
    assert isinstance(expected, dict)
    for key, value in observed.items():
        if expected.get(key) != value:
            raise ValueError(
                f"frozen composite identity drift for {key}: "
                f"observed {value!r}, expected {expected.get(key)!r}"
            )

    return {
        "receipt_version": "scriptorium-resurrection-replay-receipt-v1",
        "candidate_id": CANDIDATE_ID,
        "chapter_count": len(identities),
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
