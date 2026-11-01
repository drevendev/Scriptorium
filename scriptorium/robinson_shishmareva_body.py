"""Source-free literary-body freeze for the exact 1935 Shishmareva Wikisource page.

The oldid freezes page wikitext only. This page carries prose directly (unlike
Trusov's <pages> scan transclusion), so the entire narrative can be selected with
strict metadata/footnote/category boundaries. No source text is ever persisted.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .single_page_body import fetch_pinned_wikitext, _body_identity
from .wikisource_freeze import extract_transcription_body

CANDIDATE_ID = "defoe-robinson-shishmareva-1935-vol1-ru"
REVISION_ID = 5634933
PAGE_ID = 946454
TITLE = "Робинзон Крузо (Дефо; Шишмарёва)"
WIKITEXT_SHA256 = "784584e78e13f3941c8f9b128e26d1704b95040e430761329cb0b93fcdb92258"
MEDIAWIKI_SHA1 = "65380366cfbd0039de07a2920bb3ad057422b733"
EXPECTED_WIKITEXT_CHARACTERS = 575_223
EXPECTED_WIKITEXT_BYTES = 1_036_654
EXTRACTION_PROFILE = "scriptorium-robinson-shishmareva-first-narrative-v1"
SCHEMA = "scriptorium-robinson-shishmareva-literary-body-v1"

_CATEGORY = re.compile(r"\[\[\s*Категория\s*:[^\[\]]+\]\]", re.IGNORECASE)
_INLINE_TEMPLATE = re.compile(r"\{\{(?P<name>[A-Za-zА-Яа-яёЁ0-9]+)\|(?P<arg>[^{}|]*)(?P<tail>\|[^{}]*)?\}\}")
_PLAIN_HEADING = re.compile(r"(?m)^[ \t]*(?P<marks>={2,3})[ \t]*(?P<label>[^=\n][^\n]*?)[ \t]*(?P=marks)[ \t]*$")
_BQ_TAG = re.compile(r"</?blockquote\s*>", re.IGNORECASE)
_REF_TAG = re.compile(r"<ref\b", re.IGNORECASE)
_NONBODY_MARKUP = re.compile(r"<\s*pages\b|\{\{\s*:|<\s*/?\s*(?:includeonly|noinclude|onlyinclude)\b", re.I)


def _take_template(source: str, offset: int = 0) -> tuple[str, int]:
    """Consume one balanced template, including nested metadata templates."""
    if not source.startswith("{{", offset):
        raise ValueError("expected template at boundary")
    pos = offset
    depth = 0
    while pos < len(source) - 1:
        token = source[pos : pos + 2]
        if token == "{{":
            depth += 1
            pos += 2
        elif token == "}}":
            depth -= 1
            pos += 2
            if depth == 0:
                return source[offset:pos], pos
            if depth < 0:
                raise ValueError("unbalanced template")
        else:
            pos += 1
    raise ValueError("unterminated template")


def _trim_scaffolding(source: str) -> tuple[str, str]:
    source = source.lstrip("\ufeff \t\r\n")
    if not re.match(r"\{\{\s*Отексте\s*(?:\||\n)", source, re.I):
        raise ValueError("expected leading Отексте metadata template")
    metadata, stop = _take_template(source)
    if "Шишмарёва" not in metadata or "1935" not in metadata:
        raise ValueError("unexpected translator/edition in metadata")
    narrative = source[stop:].lstrip(" \t\r\n")
    epigraph, end = _take_template(narrative)
    if not re.match(r"\{\{\s*эпиграф\s*\|\|", epigraph, re.I):
        raise ValueError("expected opening literary subtitle epigraph")
    epigraph_text = re.sub(r"^\{\{\s*эпиграф\s*\|\|", "", epigraph, flags=re.I)[:-2].strip()
    if not epigraph_text or "{{" in epigraph_text or "}}" in epigraph_text:
        raise ValueError("unexpected nested epigraph content")
    narrative = narrative[end:].strip()
    notes = list(re.finditer(r"\{\{\s*примечания\s*\|\s*title\s*=\s*\}\}", narrative, re.I))
    if len(notes) != 1:
        raise ValueError("expected exactly one trailing Примечания template")
    suffix = narrative[notes[0].end():]
    categories = _CATEGORY.findall(suffix)
    if len(categories) != 5 or _CATEGORY.sub("", suffix).strip():
        raise ValueError("unexpected trailing category or postscript content")
    story = narrative[:notes[0].start()].strip()
    if not story:
        raise ValueError("empty novel before notes")
    if _NONBODY_MARKUP.search(story):
        raise ValueError("unexpected transclusion or proofread-page markup")
    return epigraph_text, story


def _replace_template(match: re.Match[str]) -> str:
    name = match.group("name").casefold()
    arg = match.group("arg")
    tail = match.group("tail") or ""
    if name == "razr2" and not tail and arg.strip():
        return arg.strip()
    if name in {"h", "h3"} and arg.strip() and (not tail or tail.casefold().replace(" ", "") == "|caps=1"):
        return "\n\n" + arg.strip() + "\n\n"
    raise ValueError(f"unsupported inline template: {name}")


def extract_literary_body(source: str) -> str:
    """Select the original first-narrative prose without editor/footnotes.

    Whitelisted inline templates are rendered locally; unknown syntax fails closed.
    An extracted body is *not* evidence of print-edition collation or FantLab parity.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    subtitle, story = _trim_scaffolding(source)
    if "{{" in subtitle or "}}" in subtitle:
        raise ValueError("unresolved epigraph markup")
    # Direct-prose witness uses plain chapter headings. Preserve their labels
    # as literary structure, but never strip arbitrary tables or other markup.
    def plain_heading(match: re.Match[str]) -> str:
        label = match.group("label").strip()
        if not label or "{{" in label or "}}" in label or "[[" in label:
            raise ValueError("unsupported chapter heading content")
        return "\\n\\n" + label + "\\n\\n"

    story = _PLAIN_HEADING.sub(plain_heading, story)
    story = _INLINE_TEMPLATE.sub(_replace_template, story)
    if "{{" in story or "}}" in story:
        raise ValueError("unresolved nested/body template")
    if story.count("<blockquote>") != story.count("</blockquote>"):
        raise ValueError("unbalanced blockquote tag")
    story = _BQ_TAG.sub("\n\n", story)
    if _REF_TAG.search(story) and story.lower().count("<ref") != story.lower().count("</ref>"):
        raise ValueError("unsupported or unbalanced editorial notes")
    body = extract_transcription_body(f'<div class="text">{subtitle}\n\n{story}</div>')
    if len(body) < 300_000:
        raise ValueError("actual literary body below 300000-character threshold")
    return body


def _check_inventory(inventory: Mapping[str, object]) -> dict[str, object]:
    if inventory.get("schema_version") != "scriptorium-robinson-revision-inventory-v1":
        raise ValueError("unsupported revision inventory")
    witnesses = inventory.get("witnesses")
    if not isinstance(witnesses, list) or len(witnesses) != 2:
        raise ValueError("expected two already-screened witnesses")
    matches = [w for w in witnesses if isinstance(w, dict) and w.get("work_id") == CANDIDATE_ID]
    if len(matches) != 1:
        raise ValueError("Shishmareva witness missing or duplicated")
    row = matches[0]
    expected = {
        "revision_id": REVISION_ID,
        "page_id": PAGE_ID,
        "title": TITLE,
        "mediawiki_sha1": MEDIAWIKI_SHA1,
        "wikitext_sha256": WIKITEXT_SHA256,
        "wikitext_characters_including_spaces": EXPECTED_WIKITEXT_CHARACTERS,
        "wikitext_utf8_bytes": EXPECTED_WIKITEXT_BYTES,
        "body_extraction_status": "NOT_RUN",
        "corpus_threshold_verified": False,
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"pinned inventory identity/assumption drift: {key}")
    return row


def build_manifest(
    inventory: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext,
) -> dict[str, object]:
    """Fetch exact oldid and return just a digest/count witness, never prose."""
    pinned = _check_inventory(inventory)
    observed = fetcher(title=TITLE, revision_id=REVISION_ID)
    source = observed.pop("wikitext", None)
    if not isinstance(source, str):
        raise ValueError("missing transient pinned source text")
    identity = {
        "revision_id": observed.get("revision_id"),
        "page_id": observed.get("page_id"),
        "title": observed.get("title"),
        "mediawiki_sha1": observed.get("mediawiki_sha1"),
        "timestamp_utc": observed.get("revision_timestamp"),
        "wikitext_sha256": observed.get("wikitext_sha256"),
        "wikitext_utf8_bytes": observed.get("wikitext_utf8_byte_count"),
        "wikitext_characters_including_spaces": observed.get("wikitext_character_count"),
    }
    for key, value in identity.items():
        if value != pinned.get(key):
            raise ValueError(f"exact source identity drift before extraction: {key}")
    if sha256(source.encode("utf-8")).hexdigest() != WIKITEXT_SHA256:
        raise ValueError("source content hash changed before extraction")
    if len(source) != EXPECTED_WIKITEXT_CHARACTERS:
        raise ValueError("source character count drift")
    body = extract_literary_body(source)
    body_identity = _body_identity(body)
    return {
        "schema_version": SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_revision": identity,
        "extraction": {
            "profile": EXTRACTION_PROFILE,
            "scope": "1935 volume 1, first narrative; subtitle and direct novel prose only; metadata, editorial foreword link, trailing notes and categories excluded",
            "source_text_committed": False,
            "transcluded_literary_body": False,
        },
        "literary_body_identity": body_identity,
        "corpus_character_threshold_including_spaces": 300_000,
        "corpus_threshold_verified": True,
        "admitted_for_calibration": False,
        "fantlab_analyzer_input_identity": "UNKNOWN",
        "m2_parity_admissible": False,
        "m2_contribution": 0,
        "print_edition_collation": "NOT_RUN",
        "comparison_with_trusov": "NOT_RUN",
    }


def replay_manifest(inventory: Mapping[str, object], saved: Mapping[str, object], *,
                    fetcher: Callable[..., dict[str, object]] = fetch_pinned_wikitext) -> None:
    if saved.get("schema_version") != SCHEMA or saved.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unsupported Shishmareva body manifest")
    if saved.get("m2_contribution") != 0 or saved.get("m2_parity_admissible") is not False:
        raise ValueError("invalid FantLab parity claim")
    if saved != build_manifest(inventory, fetcher=fetcher):
        raise ValueError("Shishmareva body identity differs on deterministic replay")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freeze/replay exact Shishmareva literary body, source-free.")
    sub = parser.add_subparsers(dest="command", required=True)
    capture = sub.add_parser("capture")
    capture.add_argument("--inventory", required=True, type=Path)
    capture.add_argument("--output", required=True, type=Path)
    replay = sub.add_parser("replay")
    replay.add_argument("--inventory", required=True, type=Path)
    replay.add_argument("--body-manifest", required=True, type=Path)
    args = parser.parse_args(argv)
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    if args.command == "capture":
        if args.inventory.resolve() == args.output.resolve():
            parser.error("output may not replace the inventory")
        manifest = build_manifest(inventory)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as out:
            out.write(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    else:
        saved = json.loads(args.body_manifest.read_text(encoding="utf-8"))
        replay_manifest(inventory, saved)
        print("Exact source and literary-body SHA-256 identities replayed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
