"""Freeze and replay the Russian Wikisource Silver Dove candidate.

The public candidate is a single revision-pinned Wikisource page. The
extraction contract is deliberately source-specific and fail-closed: it removes
only the observed page/bibliographic scaffolding and trailing Wikisource
editorial publication note, preserves authorial front matter/headings, and then
reuses the generic transcription-body renderer. No source prose is serialized
into the durable manifest or replay receipt.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, Sequence

from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import extract_transcription_body, fetch_current_chapter_revisions
from .wikisource_replay import fetch_pinned_chapter_revisions


CANDIDATE_ID = "bely-silver-dove-ru"
WORK_TITLE = "Серебряный голубь (Белый)"
SOURCE_REVISION_ID = 5588003
SOURCE_WORK_URL = "https://ru.wikisource.org/wiki/Серебряный_голубь_(Белый)"
PERMANENT_SOURCE_URL = (
    "https://ru.wikisource.org/w/index.php?title=Серебряный_голубь_(Белый)&oldid=5588003"
)
BIBLIOGRAPHIC_SOURCE = (
    "Андрей Белый. Сочинения в двух томах. М.: Художественная литература, 1990. "
    "Том 1, стр. 377–642."
)
MANIFEST_VERSION = "scriptorium-silver-dove-source-revision-manifest-v1"
EXTRACTION_PROFILE = "scriptorium-wikisource-silver-dove-body-v1"

_LITERARY_START = "<center>ВМЕСТО ПРЕДИСЛОВИЯ</center>"
_EDITORIAL_NOTE_START = "''Роман был опубликован впервые отдельными частями"
_EXPECTED_SCAFFOLD = (
    "=== СЕРЕБРЯНЫЙ ГОЛУБЬ === "
    "=== ''Повесть в семи главах'' === "
    "================================== ================================== "
    "Источник: Андрей Белый. Сочинения в двух томах. М.: Художественная литература, "
    "1990. Том 1, стр. 377 −642. Эл. версия: В. Есаулов, 19 августа 2006 г. "
    "================================== =================================="
)
_EXPECTED_EDITORIAL_NOTE = (
    "''Роман был опубликован впервые отдельными частями в журнале «Весы» "
    "(NN 3,4,6,7,10,11 и 12за 1909 г.), отдельным изданием впервые — "
    "издательство «Скорпион» в 1910 году.''"
)
_EXPECTED_CATEGORIES = (
    "Импорт/lib.ru/Страницы с не вики-сносками или с тегом sup",
    "Импорт/lib.ru/Длина текста более 500 Кб",
    "Романы",
    "Андрей Белый",
    "Литература 1909 года",
    "Импорт/lib.ru",
    "Импорт/az.lib.ru/Андрей Белый",
)
_HEADING3_RE = re.compile(
    r"(?m)^[ \t]*===(?!=)[ \t]*(?P<text>[^\n=].*?)[ \t]*(?<![=])===(?![=])[ \t]*$"
)
_CENTER_RE = re.compile(r"<center>(?P<text>.*?)</center>", re.IGNORECASE | re.DOTALL)
_CATEGORY_RE = re.compile(r"\[\[Категория:(?P<name>[^\]]+)\]\]", re.IGNORECASE)
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def _space_fold(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u00a0", " ")).strip()


def _strip_leading_template(source: str, name: str) -> str:
    stripped = source.lstrip()
    marker = "{{" + name
    if not stripped.casefold().startswith(marker.casefold()):
        raise ValueError(f"expected leading {name} template")
    depth = 0
    index = 0
    while index < len(stripped) - 1:
        pair = stripped[index : index + 2]
        if pair == "{{":
            depth += 1
            index += 2
            continue
        if pair == "}}":
            depth -= 1
            index += 2
            if depth == 0:
                return stripped[index:]
            if depth < 0:
                break
            continue
        index += 1
    raise ValueError(f"unterminated leading {name} template")


def _plain_heading(match: re.Match[str]) -> str:
    text = match.group("text").strip()
    # The frozen page contains empty level-three markup used only as layout.
    # It renders no literary characters, so strip only that observed empty shape.
    if not text:
        return ""
    if "{{" in text or "}}" in text or "<" in text or ">" in text:
        raise ValueError("unsupported markup inside Silver Dove heading")
    return f"\n\n{text}\n\n"


def _plain_center(match: re.Match[str]) -> str:
    text = match.group("text").strip()
    if "{{" in text or "}}" in text or "<" in text or ">" in text:
        raise ValueError("unsupported markup inside Silver Dove center block")
    if not text:
        raise ValueError("empty Silver Dove center block")
    return f"\n\n{text}\n\n"


def _split_editorial_suffix(source: str) -> str:
    marker_index = source.rfind(_EDITORIAL_NOTE_START)
    if marker_index < 0:
        raise ValueError("Silver Dove trailing editorial publication note not found")
    literary = source[:marker_index].rstrip()
    suffix = source[marker_index:].strip()

    first_category = suffix.find("[[Категория:")
    if first_category < 0:
        raise ValueError("Silver Dove trailing category block not found")
    note = suffix[:first_category].strip()
    if _space_fold(note) != _EXPECTED_EDITORIAL_NOTE:
        raise ValueError("Silver Dove trailing editorial publication note drift")

    category_block = suffix[first_category:]
    categories = tuple(match.group("name") for match in _CATEGORY_RE.finditer(category_block))
    if categories != _EXPECTED_CATEGORIES:
        raise ValueError("Silver Dove trailing category inventory drift")
    if _CATEGORY_RE.sub("", category_block).strip():
        raise ValueError("unsupported content after Silver Dove literary body")
    if not literary:
        raise ValueError("empty Silver Dove literary body before editorial suffix")
    return literary


def extract_silver_dove_body(wikitext: str) -> str:
    """Extract the literary body from the exact observed single-page source shape."""

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    source = _strip_leading_template(wikitext, "Отексте")
    start = source.find(_LITERARY_START)
    if start < 0:
        raise ValueError("Silver Dove authorial preface boundary not found")
    scaffold = source[:start]
    if _space_fold(scaffold) != _EXPECTED_SCAFFOLD:
        raise ValueError("Silver Dove page/bibliographic scaffolding drift")

    literary = _split_editorial_suffix(source[start:])
    literary = _CENTER_RE.sub(_plain_center, literary)
    literary = _HEADING3_RE.sub(_plain_heading, literary)
    return extract_transcription_body(f'<div class="text">{literary}</div>')


def _identity(body: str) -> dict[str, object]:
    normalized = normalize_text(body)
    raw = body.encode("utf-8")
    return {
        "character_count_including_spaces": len(body),
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
    request = ({"ordinal": 1, "title": WORK_TITLE},)
    records = fetcher(request)
    if set(records) != {WORK_TITLE}:
        raise ValueError("Silver Dove source inventory mismatch")
    revision = records[WORK_TITLE]
    revision_id = int(revision["revision_id"])
    if revision_id != SOURCE_REVISION_ID:
        raise ValueError(
            f"Silver Dove current revision drift: observed {revision_id}, expected {SOURCE_REVISION_ID}"
        )
    timestamp = str(revision["timestamp"])
    if not timestamp:
        raise ValueError("Silver Dove source revision timestamp missing")
    wikitext = str(revision["wikitext"])
    body = extract_silver_dove_body(wikitext)
    identity = _identity(body)
    if int(identity["character_count_including_spaces"]) < 300_000:
        raise ValueError("Silver Dove public candidate fell below corpus threshold")

    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_work_url": SOURCE_WORK_URL,
        "permanent_source_url": PERMANENT_SOURCE_URL,
        "bibliographic_source": BIBLIOGRAPHIC_SOURCE,
        "legal_basis": "public_domain",
        "source_identity": {
            "title": WORK_TITLE,
            "revision_id": revision_id,
            "revision_timestamp": timestamp,
            "mediawiki_sha1": str(revision["mediawiki_sha1"]),
            "wikitext_sha256": sha256(wikitext.encode("utf-8")).hexdigest(),
        },
        "composition": {
            "profile": "scriptorium-wikisource-single-page-v1",
            "extraction_profile": EXTRACTION_PROFILE,
            "source_page_count": 1,
            "authorial_preface_included": True,
            "literary_headings_included": True,
            "empty_level3_heading_markup_included": False,
            "page_bibliographic_scaffolding_included": False,
            "wikisource_editorial_publication_note_included": False,
            "category_links_included": False,
            "source_text_committed": False,
        },
        "composite_identity": identity,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_comparison_admissible": False,
        "m2_parity_admissible": False,
    }


def _validate_manifest(manifest: Mapping[str, object]) -> dict[str, object]:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Silver Dove revision-manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Silver Dove candidate id")
    if manifest.get("legal_basis") != "public_domain":
        raise ValueError("Silver Dove legal-basis drift")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("Silver Dove source-match gate drift")
    if manifest.get("diagnostic_comparison_admissible") is not False:
        raise ValueError("Silver Dove diagnostic gate drift")
    if manifest.get("m2_parity_admissible") is not False:
        raise ValueError("Silver Dove M2 gate drift")

    composition = manifest.get("composition")
    if not isinstance(composition, dict):
        raise ValueError("Silver Dove manifest missing composition")
    expected_composition = {
        "profile": "scriptorium-wikisource-single-page-v1",
        "extraction_profile": EXTRACTION_PROFILE,
        "source_page_count": 1,
        "authorial_preface_included": True,
        "literary_headings_included": True,
        "empty_level3_heading_markup_included": False,
        "page_bibliographic_scaffolding_included": False,
        "wikisource_editorial_publication_note_included": False,
        "category_links_included": False,
        "source_text_committed": False,
    }
    if composition != expected_composition:
        raise ValueError("Silver Dove composition contract drift")

    source_identity = manifest.get("source_identity")
    if not isinstance(source_identity, dict):
        raise ValueError("Silver Dove manifest missing source identity")
    if source_identity.get("title") != WORK_TITLE:
        raise ValueError("Silver Dove source title drift")
    if source_identity.get("revision_id") != SOURCE_REVISION_ID:
        raise ValueError("Silver Dove source revision drift")
    timestamp = source_identity.get("revision_timestamp")
    if not isinstance(timestamp, str) or not timestamp:
        raise ValueError("invalid Silver Dove source timestamp")
    for key in ("mediawiki_sha1", "wikitext_sha256"):
        value = source_identity.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"invalid Silver Dove source identity field {key}")
    wikitext_sha = source_identity["wikitext_sha256"]
    if not isinstance(wikitext_sha, str) or not _HEX64_RE.fullmatch(wikitext_sha):
        raise ValueError("invalid Silver Dove wikitext SHA-256")

    composite = manifest.get("composite_identity")
    if not isinstance(composite, dict):
        raise ValueError("Silver Dove manifest missing composite identity")
    if composite.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError("Silver Dove normalization profile drift")
    for key in (
        "character_count_including_spaces",
        "normalized_character_count_including_spaces",
        "utf8_byte_count",
    ):
        value = composite.get(key)
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"invalid Silver Dove composite {key}")
    if int(composite["character_count_including_spaces"]) < 300_000:
        raise ValueError("frozen Silver Dove candidate fell below corpus threshold")
    for key in ("raw_sha256", "normalized_sha256"):
        value = composite.get(key)
        if not isinstance(value, str) or not _HEX64_RE.fullmatch(value):
            raise ValueError(f"invalid Silver Dove composite {key}")
    return source_identity


def replay_manifest(
    manifest: Mapping[str, object],
    *,
    fetcher: Callable[
        [Iterable[Mapping[str, object]]], dict[str, str]
    ] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    source_identity = _validate_manifest(manifest)
    identities = (source_identity,)
    revisions = fetcher(identities)
    if set(revisions) != {WORK_TITLE}:
        raise ValueError("Silver Dove pinned source inventory mismatch")
    wikitext = revisions[WORK_TITLE]
    if sha256(wikitext.encode("utf-8")).hexdigest() != source_identity["wikitext_sha256"]:
        raise ValueError("Silver Dove pinned wikitext SHA-256 drift")
    observed = _identity(extract_silver_dove_body(wikitext))
    expected = manifest["composite_identity"]
    assert isinstance(expected, dict)
    for key, value in observed.items():
        if expected.get(key) != value:
            raise ValueError(
                f"Silver Dove frozen composite identity drift for {key}: "
                f"observed {value!r}, expected {expected.get(key)!r}"
            )
    return {
        "receipt_version": "scriptorium-silver-dove-replay-receipt-v1",
        "candidate_id": CANDIDATE_ID,
        "source_page_count": 1,
        "composite_identity": observed,
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_comparison_admissible": False,
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
    capture = subparsers.add_parser("capture", help="capture the source-free pinned manifest")
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
        raise ValueError("Silver Dove revision manifest must be a JSON object")
    _write_json(args.receipt, replay_manifest(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
