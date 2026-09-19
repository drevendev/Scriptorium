"""Freeze and replay the literary-body identity for Grin's *Running on Waves*.

The source text is fetched only transiently from the 36 exact revisions already
frozen by ``running_waves_revisions``. Durable output contains only source
identities, derived counts/digests, and the versioned extraction/composition
contract; literary prose is never serialized.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, Sequence

from .running_waves_inventory import CANDIDATE_ID, PRIMARY_BIBLIOGRAPHIC_SOURCE
from .running_waves_revisions import canonical_json_text, validate_manifest as validate_source_manifest
from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import COMPOSITE_PROFILE, extract_transcription_body, roman
from .wikisource_replay import fetch_pinned_chapter_revisions

MANIFEST_VERSION = "scriptorium-running-waves-literary-body-v1"
EXTRACTION_PROFILE = "scriptorium-running-waves-wikisource-body-v1"
CHAPTER_SEPARATOR = "\n\n"
MINIMUM_CORPUS_CHARACTERS = 300_000

_INNER_TEMPLATE_RE = re.compile(r"\{\{([^{}]*)\}\}")


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


def _split_template_fields(inner: str) -> list[str]:
    """Split an innermost template while preserving pipes inside wikilinks."""

    parts: list[str] = []
    start = 0
    bracket_depth = 0
    index = 0
    while index < len(inner):
        pair = inner[index : index + 2]
        if pair == "[[":
            bracket_depth += 1
            index += 2
            continue
        if pair == "]]" and bracket_depth:
            bracket_depth -= 1
            index += 2
            continue
        if inner[index] == "|" and bracket_depth == 0:
            parts.append(inner[start:index])
            start = index + 1
        index += 1
    if bracket_depth:
        raise ValueError("unbalanced wikilink inside Running on Waves template")
    parts.append(inner[start:])
    return parts


def _render_running_waves_template(inner: str) -> str | None:
    """Render only the template shapes observed in the 36 frozen 1965 pages.

    The contract is intentionally narrower than general MediaWiki expansion. CI first
    recorded source-free template names/arities from the exact pinned revisions; this
    renderer accepts only those shapes and preserves only visible literary content.
    Unknown names or unexpected arities are left for the generic extractor to reject.
    """

    parts = _split_template_fields(inner)
    name = parts[0].strip()
    args = parts[1:]

    if name == "^":
        return "" if not args else None

    if name == "roman":
        if len(args) != 1 or not re.fullmatch(r"[0-9]+", args[0].strip()):
            return None
        try:
            return roman(int(args[0].strip()))
        except ValueError:
            return None

    if name in {"razr", "razr2"}:
        return args[0] if len(args) == 1 else None

    if name == "акут":
        return "\u0301" if not args else None

    if name == "Гравис":
        return "\u0300" if not args else None

    if name == "Так в тексте":
        # The optional second parameter is a tooltip/comment; rendered literary text
        # is the first parameter. Exact pinned pages use one parameter except one
        # two-parameter invocation.
        return args[0] if len(args) in {1, 2} else None

    if name == "опечатка2":
        # In main-namespace transclusion Wikisource displays the corrected second
        # parameter. The pinned Running on Waves pages use exactly two parameters.
        return args[1] if len(args) == 2 else None

    if name == "poem1":
        # Source-free CI established that every pinned invocation has exactly three
        # positional parameters with empty title/signature slots. Preserve only the
        # literary poem body in the middle slot; reject any other shape.
        if len(args) == 3 and not args[0].strip() and not args[2].strip():
            return args[1]
        return None

    return None


def expand_running_waves_templates(wikitext: str) -> str:
    """Resolve the frozen candidate's formatting templates without remote expansion."""

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")

    current = wikitext
    while True:
        changed = False

        def replace(match: re.Match[str]) -> str:
            nonlocal changed
            rendered = _render_running_waves_template(match.group(1))
            if rendered is None:
                return match.group(0)
            changed = True
            return rendered

        updated = _INNER_TEMPLATE_RE.sub(replace, current)
        if not changed:
            return current
        current = updated


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
            candidate_wikitext = expand_running_waves_templates(fetched[title])
            body = extract_transcription_body(candidate_wikitext)
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
