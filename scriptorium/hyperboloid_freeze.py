"""Freeze a source-free literary-body identity for the pinned Hyperboloid revision.

The source prose exists only in process memory. The durable artifact records the exact
already-frozen revision identity, a source-specific extraction profile, and raw/
normalized literary-body digests. It deliberately does not claim print-edition or
FantLab analyzer-input identity.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .single_page_revision import _api_query, validate_manifest as validate_revision_manifest
from .text import NORMALIZATION_PROFILE, normalize_text
from .wikisource_freeze import extract_transcription_body


CANDIDATE_ID = "tolstoy-hyperboloid-garin-wikisource-ru"
TITLE = "Гиперболоид инженера Гарина (Толстой)"
REVISION_ID = 5014458
BODY_MANIFEST_VERSION = "scriptorium-single-page-literary-body-v1"
EXTRACTION_PROFILE = "scriptorium-hyperboloid-wikisource-body-v1"

_EXPECTED_HEADING_COUNT = 132
_EXPECTED_CATEGORY_COUNT = 9
_EXPECTED_WIKILINK_COUNT = 13
_EXPECTED_COMMENT_COUNT = 2
_EXPECTED_BOLD_ITALIC_MARKER_COUNT = 44
_EXPECTED_TAG_COUNTS = {"br": 18, "sup": 18, "u": 18}
_EXPECTED_SUP_U_PAIR_COUNT = 9

_HEADING3_RE = re.compile(
    r"(?m)^[ \t]*===(?!=)[ \t]*(?P<text>[^\n=].*?)[ \t]*(?<![=])===(?![=])[ \t]*$"
)
_ANY_HEADING_RE = re.compile(r"(?m)^[ \t]*={2,6}.*?={2,6}[ \t]*$")
_CATEGORY_LINE_RE = re.compile(
    r"(?mi)^[ \t]*\[\[\s*Категория\s*:(?P<name>[^\]\n]+)\]\][ \t]*$"
)
_TAG_RE = re.compile(r"</?\s*(?P<name>[A-Za-z][A-Za-z0-9:-]*)\b[^>]*>")
_SUP_U_PAIR_RE = re.compile(r"<sup>\s*<u>.*?</u>\s*</sup>", re.IGNORECASE | re.DOTALL)
_U_TAG_RE = re.compile(r"</?u>", re.IGNORECASE)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def fetch_pinned_wikitext(
    *,
    title: str,
    revision_id: int,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, object]:
    """Fetch one exact revision including transient wikitext for extraction."""

    payload = query(
        {
            "action": "query",
            "prop": "revisions",
            "revids": str(revision_id),
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
        }
    )
    query_obj = payload.get("query")
    if not isinstance(query_obj, dict):
        raise ValueError("MediaWiki response missing query")
    pages = query_obj.get("pages")
    if not isinstance(pages, list) or len(pages) != 1:
        raise ValueError("expected exactly one MediaWiki page for pinned revision")
    page = pages[0]
    if not isinstance(page, dict) or page.get("title") != title:
        raise ValueError("pinned revision title drift")
    page_id = page.get("pageid")
    revisions = page.get("revisions")
    if not isinstance(page_id, int) or page_id <= 0:
        raise ValueError("pinned revision page id missing")
    if not isinstance(revisions, list) or len(revisions) != 1:
        raise ValueError("expected exactly one MediaWiki revision")
    revision = revisions[0]
    if not isinstance(revision, dict) or revision.get("revid") != revision_id:
        raise ValueError("pinned revision id drift")
    timestamp = revision.get("timestamp")
    mediawiki_sha1 = revision.get("sha1")
    slots = revision.get("slots")
    main = slots.get("main") if isinstance(slots, dict) else None
    wikitext = main.get("content") if isinstance(main, dict) else None
    if not isinstance(timestamp, str) or not isinstance(mediawiki_sha1, str):
        raise ValueError("pinned revision identity incomplete")
    if not isinstance(wikitext, str):
        raise ValueError("pinned revision wikitext missing")
    raw = wikitext.encode("utf-8")
    return {
        "title": title,
        "page_id": page_id,
        "revision_id": revision_id,
        "revision_timestamp": timestamp,
        "mediawiki_sha1": mediawiki_sha1,
        "wikitext_character_count": len(wikitext),
        "wikitext_utf8_byte_count": len(raw),
        "wikitext_sha256": sha256(raw).hexdigest(),
        "wikitext": wikitext,
    }


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


def _validate_observed_markup(source: str) -> None:
    if "{{" in source or "}}" in source:
        raise ValueError("unsupported template remains after leading Отексте scaffold")

    headings = _HEADING3_RE.findall(source)
    if len(headings) != _EXPECTED_HEADING_COUNT:
        raise ValueError(
            f"Hyperboloid level-three heading inventory drift: {len(headings)}"
        )
    if len(_ANY_HEADING_RE.findall(source)) != _EXPECTED_HEADING_COUNT:
        raise ValueError("unsupported Hyperboloid heading level or shape")

    category_matches = tuple(_CATEGORY_LINE_RE.finditer(source))
    if len(category_matches) != _EXPECTED_CATEGORY_COUNT:
        raise ValueError(
            f"Hyperboloid trailing category inventory drift: {len(category_matches)}"
        )

    if source.count("[[") != _EXPECTED_WIKILINK_COUNT or source.count("]]" ) != _EXPECTED_WIKILINK_COUNT:
        raise ValueError("Hyperboloid wikilink inventory drift")
    if source.count("<!--") != _EXPECTED_COMMENT_COUNT or source.count("-->") != _EXPECTED_COMMENT_COUNT:
        raise ValueError("Hyperboloid HTML comment inventory drift")
    if source.count("''") != _EXPECTED_BOLD_ITALIC_MARKER_COUNT:
        raise ValueError("Hyperboloid bold/italic marker inventory drift")

    tag_counts = Counter(match.group("name").casefold() for match in _TAG_RE.finditer(source))
    if dict(sorted(tag_counts.items())) != _EXPECTED_TAG_COUNTS:
        raise ValueError(f"Hyperboloid HTML tag inventory drift: {dict(tag_counts)!r}")
    if len(_SUP_U_PAIR_RE.findall(source)) != _EXPECTED_SUP_U_PAIR_COUNT:
        raise ValueError("Hyperboloid nested sup/u marker inventory drift")


def _strip_trailing_categories(source: str) -> str:
    matches = tuple(_CATEGORY_LINE_RE.finditer(source))
    if len(matches) != _EXPECTED_CATEGORY_COUNT:
        raise ValueError("Hyperboloid category inventory drift")
    first = matches[0].start()
    suffix = source[first:]
    if _CATEGORY_LINE_RE.sub("", suffix).strip():
        raise ValueError("unsupported content after Hyperboloid category block")
    literary = source[:first].rstrip()
    if not literary:
        raise ValueError("empty Hyperboloid literary body before categories")
    return literary


def _plain_heading(match: re.Match[str]) -> str:
    text = match.group("text").strip()
    if not text:
        raise ValueError("empty Hyperboloid literary heading")
    if "{{" in text or "}}" in text or "<" in text or ">" in text:
        raise ValueError("unsupported markup inside Hyperboloid heading")
    return f"\n\n{text}\n\n"


def extract_literary_body(wikitext: str) -> str:
    """Extract literary text under the exact observed single-page source contract.

    The frozen revision has one leading ``Отексте`` metadata template, direct page
    prose rather than a ``div.text`` wrapper, 132 level-three literary headings, and
    a trailing nine-category Wikisource block. The profile admits only the observed
    HTML/wikilink/comment formatting inventory. Visible contents of ``sup/u`` markers
    are preserved while the formatting tags are removed by the generic renderer.
    Any source-shape drift fails closed and requires a new extraction profile.
    """

    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    source = _strip_leading_template(wikitext, "Отексте")
    _validate_observed_markup(source)
    literary = _strip_trailing_categories(source)
    literary = _COMMENT_RE.sub("", literary)
    literary = _HEADING3_RE.sub(_plain_heading, literary)
    literary = _U_TAG_RE.sub("", literary)
    return extract_transcription_body(f'<div class="text">{literary}</div>')


def _body_identity(body: str) -> dict[str, object]:
    raw = body.encode("utf-8")
    normalized = normalize_text(body)
    return {
        "character_count_including_spaces": len(body),
        "utf8_byte_count": len(raw),
        "raw_sha256": sha256(raw).hexdigest(),
        "normalization_profile": NORMALIZATION_PROFILE,
        "normalized_character_count_including_spaces": len(normalized),
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
    }


def build_body_manifest(
    revision_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    validate_revision_manifest(revision_manifest)
    if revision_manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected candidate id")
    source_identity = revision_manifest.get("source_identity")
    if not isinstance(source_identity, dict):
        raise ValueError("revision manifest missing source identity")
    if source_identity.get("title") != TITLE or source_identity.get("revision_id") != REVISION_ID:
        raise ValueError("revision manifest does not identify the frozen Hyperboloid revision")

    observed = fetcher(title=TITLE, revision_id=REVISION_ID)
    wikitext = observed.pop("wikitext", None)
    if not isinstance(wikitext, str):
        raise ValueError("transient source prose missing")
    if observed != source_identity:
        differing = sorted(
            key
            for key in set(observed) | set(source_identity)
            if observed.get(key) != source_identity.get(key)
        )
        raise ValueError(f"pinned revision identity drift before extraction: {differing}")

    body = extract_literary_body(wikitext)
    identity = _body_identity(body)
    if int(identity["character_count_including_spaces"]) < 300_000:
        raise ValueError("extracted literary body is below the corpus threshold")

    return {
        "manifest_version": BODY_MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "source_revision": {
            "title": TITLE,
            "page_id": source_identity["page_id"],
            "revision_id": REVISION_ID,
            "revision_timestamp": source_identity["revision_timestamp"],
            "mediawiki_sha1": source_identity["mediawiki_sha1"],
            "wikitext_sha256": source_identity["wikitext_sha256"],
        },
        "extraction": {
            "profile": EXTRACTION_PROFILE,
            "source_text_committed": False,
            "scope": "literary body extracted from the exact pinned revision wikitext",
        },
        "literary_body_identity": identity,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_comparison_admissible": True,
        "m2_parity_admissible": False,
    }


def validate_body_manifest(manifest: Mapping[str, object]) -> None:
    if manifest.get("manifest_version") != BODY_MANIFEST_VERSION:
        raise ValueError("unsupported Hyperboloid body manifest version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Hyperboloid body candidate")
    source_revision = manifest.get("source_revision")
    if not isinstance(source_revision, dict):
        raise ValueError("body manifest missing source revision")
    if source_revision.get("title") != TITLE or source_revision.get("revision_id") != REVISION_ID:
        raise ValueError("body manifest source revision drift")
    extraction = manifest.get("extraction")
    if extraction != {
        "profile": EXTRACTION_PROFILE,
        "source_text_committed": False,
        "scope": "literary body extracted from the exact pinned revision wikitext",
    }:
        raise ValueError("body extraction contract drift")
    identity = manifest.get("literary_body_identity")
    if not isinstance(identity, dict):
        raise ValueError("body manifest missing literary body identity")
    for key in (
        "character_count_including_spaces",
        "utf8_byte_count",
        "normalized_character_count_including_spaces",
    ):
        value = identity.get(key)
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"invalid body identity {key}")
    for key in ("raw_sha256", "normalized_sha256"):
        value = identity.get(key)
        if not isinstance(value, str) or len(value) != 64:
            raise ValueError(f"invalid body identity {key}")
    if identity.get("normalization_profile") != NORMALIZATION_PROFILE:
        raise ValueError("body normalization profile drift")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")
    if manifest.get("diagnostic_comparison_admissible") is not True:
        raise ValueError("frozen public body should be diagnostic-admissible")
    if manifest.get("m2_parity_admissible") is not False:
        raise ValueError("public-source freezing cannot advance M2")
    forbidden = {"wikitext", "content", "body", "text", "source_text"}
    if forbidden.intersection(manifest):
        raise ValueError("source prose leaked into body manifest")


def replay_body_manifest(
    revision_manifest: Mapping[str, object],
    body_manifest: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    validate_body_manifest(body_manifest)
    observed = build_body_manifest(revision_manifest, fetcher=fetcher)
    if observed != body_manifest:
        raise ValueError("pinned Hyperboloid literary-body identity drift")
    identity = body_manifest["literary_body_identity"]
    assert isinstance(identity, dict)
    return {
        "receipt_version": "scriptorium-single-page-literary-body-replay-v1",
        "candidate_id": CANDIDATE_ID,
        "revision_id": REVISION_ID,
        "extraction_profile": EXTRACTION_PROFILE,
        "raw_sha256": identity["raw_sha256"],
        "normalized_sha256": identity["normalized_sha256"],
        "verified": True,
        "source_text_included": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze or replay Hyperboloid literary-body identity.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--revision-manifest", type=Path, required=True)
    capture.add_argument("--output", type=Path, required=True)
    replay = subparsers.add_parser("replay")
    replay.add_argument("--revision-manifest", type=Path, required=True)
    replay.add_argument("--body-manifest", type=Path, required=True)
    replay.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)

    revision_manifest = _load_json(args.revision_manifest)
    if args.command == "capture":
        manifest = build_body_manifest(revision_manifest)
        validate_body_manifest(manifest)
        _write_json(args.output, manifest)
        return 0

    body_manifest = _load_json(args.body_manifest)
    receipt = replay_body_manifest(revision_manifest, body_manifest)
    _write_json(args.receipt, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
