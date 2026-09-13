"""Freeze a revision-pinned Russian Wikisource composite without storing source prose."""

from __future__ import annotations

import argparse
from hashlib import sha256
import html
import json
from pathlib import Path
import re
from typing import Callable, Iterable
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

from .text import NORMALIZATION_PROFILE, normalize_text


API_URL = "https://ru.wikisource.org/w/api.php"
WORK_BASE_TITLE = "Анна Каренина (Толстой)"
PART_CHAPTER_COUNTS = (34, 35, 32, 23, 33, 32, 31, 19)
COMPOSITE_PROFILE = "scriptorium-wikisource-composite-v1"
EXTRACTION_PROFILE = "scriptorium-wikisource-body-v1"
USER_AGENT = "Scriptorium provenance research/1.0 (+https://github.com/drevendev/Scriptorium)"

_DIV_TEXT_RE = re.compile(
    r'<div\s+class=["\']text["\']\s*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
_NOINCLUDE_RE = re.compile(r"<noinclude>.*?</noinclude>", re.IGNORECASE | re.DOTALL)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_REF_RE = re.compile(r"<ref\b[^>]*>.*?</ref\s*>|<ref\b[^>]*/\s*>", re.IGNORECASE | re.DOTALL)
_LANG_RE = re.compile(r"\{\{lang\|[^|{}]+\|([^{}]*)\}\}", re.IGNORECASE)
_WIKILINK_RE = re.compile(r"\[\[(?:[^\[\]|]+\|)?([^\[\]]+)\]\]")
_EXTERNAL_LINK_RE = re.compile(r"\[(?:https?://\S+)\s+([^\]]+)\]")
_HTML_TAG_RE = re.compile(r"</?(?:span|small|big|i|b|em|strong|sup|sub|br)\b[^>]*>", re.IGNORECASE)
_BOLD_ITALIC_RE = re.compile(r"'{2,5}")
_TEMPLATE_RE = re.compile(r"\{\{[^{}]*\}\}")
_TABLE_OR_HEADING_RE = re.compile(r"(^|\n)\s*(?:\{\||\|-|\|\}|\|[^|]|!|={2,6}\s*)")


def roman(value: int) -> str:
    if not isinstance(value, int) or value <= 0 or value >= 4000:
        raise ValueError("roman value must be an integer in 1..3999")
    numerals = (
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    )
    parts: list[str] = []
    remainder = value
    for amount, glyph in numerals:
        while remainder >= amount:
            parts.append(glyph)
            remainder -= amount
    return "".join(parts)


def expected_chapters() -> tuple[dict[str, object], ...]:
    chapters: list[dict[str, object]] = []
    ordinal = 0
    for part, count in enumerate(PART_CHAPTER_COUNTS, start=1):
        for chapter in range(1, count + 1):
            ordinal += 1
            title = f"{WORK_BASE_TITLE}/Часть {roman(part)}/Глава {roman(chapter)}"
            chapters.append(
                {
                    "ordinal": ordinal,
                    "part": part,
                    "chapter": chapter,
                    "title": title,
                }
            )
    if ordinal != 239:
        raise AssertionError(f"chapter contract drift: expected 239, got {ordinal}")
    return tuple(chapters)


def _api_query(params: dict[str, str]) -> dict[str, object]:
    encoded = urlencode({**params, "format": "json", "formatversion": "2"})
    request = Request(
        f"{API_URL}?{encoded}",
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise ValueError("unexpected MediaWiki API response")
    return payload


def fetch_current_chapter_revisions(
    chapters: Iterable[dict[str, object]],
    *,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, dict[str, object]]:
    expected = tuple(chapters)
    records: dict[str, dict[str, object]] = {}
    for offset in range(0, len(expected), 40):
        batch = expected[offset : offset + 40]
        titles = [str(chapter["title"]) for chapter in batch]
        payload = query(
            {
                "action": "query",
                "prop": "revisions",
                "titles": "|".join(titles),
                "rvprop": "ids|timestamp|sha1|content",
                "rvslots": "main",
                "redirects": "0",
            }
        )
        query_obj = payload.get("query")
        if not isinstance(query_obj, dict):
            raise ValueError("MediaWiki response missing query")
        pages = query_obj.get("pages")
        if not isinstance(pages, list):
            raise ValueError("MediaWiki response missing pages")
        for page in pages:
            if not isinstance(page, dict):
                raise ValueError("unexpected page object")
            title = page.get("title")
            if not isinstance(title, str) or title not in titles:
                raise ValueError(f"unexpected chapter title from MediaWiki: {title!r}")
            if page.get("missing") is True:
                raise ValueError(f"missing Wikisource chapter: {title}")
            revisions = page.get("revisions")
            if not isinstance(revisions, list) or len(revisions) != 1:
                raise ValueError(f"expected one current revision for {title}")
            revision = revisions[0]
            if not isinstance(revision, dict):
                raise ValueError(f"unexpected revision object for {title}")
            slots = revision.get("slots")
            main = slots.get("main") if isinstance(slots, dict) else None
            content = main.get("content") if isinstance(main, dict) else None
            if not isinstance(content, str):
                raise ValueError(f"missing wikitext content for {title}")
            revid = revision.get("revid")
            timestamp = revision.get("timestamp")
            mw_sha1 = revision.get("sha1")
            if not isinstance(revid, int) or not isinstance(timestamp, str) or not isinstance(mw_sha1, str):
                raise ValueError(f"incomplete revision identity for {title}")
            if title in records:
                raise ValueError(f"duplicate chapter response: {title}")
            records[title] = {
                "revision_id": revid,
                "timestamp": timestamp,
                "mediawiki_sha1": mw_sha1,
                "wikitext": content,
            }
    expected_titles = {str(chapter["title"]) for chapter in expected}
    if set(records) != expected_titles:
        missing = sorted(expected_titles - set(records))
        extra = sorted(set(records) - expected_titles)
        raise ValueError(f"chapter inventory mismatch; missing={missing!r} extra={extra!r}")
    return records


def extract_transcription_body(wikitext: str) -> str:
    if not isinstance(wikitext, str):
        raise TypeError("wikitext must be str")
    text = _COMMENT_RE.sub("", wikitext)
    text = _NOINCLUDE_RE.sub("", text)
    matches = _DIV_TEXT_RE.findall(text)
    if len(matches) != 1:
        raise ValueError(f"expected exactly one <div class=\"text\"> body, got {len(matches)}")
    body = matches[0]
    body = _REF_RE.sub("", body)
    body = body.replace("{{СодержаниеБН}}", "")
    previous = None
    while previous != body:
        previous = body
        body = _LANG_RE.sub(lambda match: match.group(1), body)
        body = _WIKILINK_RE.sub(lambda match: match.group(1), body)
        body = _EXTERNAL_LINK_RE.sub(lambda match: match.group(1), body)
        body = _HTML_TAG_RE.sub("", body)
        body = _BOLD_ITALIC_RE.sub("", body)
        body = html.unescape(body)
    if _TEMPLATE_RE.search(body):
        raise ValueError("unsupported template remains inside transcription body")
    if _TABLE_OR_HEADING_RE.search(body):
        raise ValueError("unsupported table/heading markup remains inside transcription body")
    if "[[" in body or "]]" in body or "<" in body or ">" in body:
        raise ValueError("unsupported wiki/HTML markup remains inside transcription body")

    body = body.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not body:
        raise ValueError("empty transcription body")

    paragraphs = re.split(r"\n[ \t]*\n+", body)
    rendered: list[str] = []
    for paragraph in paragraphs:
        collapsed = re.sub(r"[ \t]*\n[ \t]*", " ", paragraph)
        collapsed = re.sub(r"[ \t]+", " ", collapsed).strip(" \t")
        if collapsed:
            rendered.append(collapsed)
    if not rendered:
        raise ValueError("empty rendered transcription body")
    return "\n\n".join(rendered)


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def build_manifest(
    *,
    fetcher: Callable[[Iterable[dict[str, object]]], dict[str, dict[str, object]]] = fetch_current_chapter_revisions,
) -> dict[str, object]:
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
    if len(rows) != 239:
        raise AssertionError(f"expected 239 chapters, got {len(rows)}")
    if len(composite) < 300_000:
        raise ValueError(f"composite below corpus threshold: {len(composite)} characters")
    normalized = normalize_text(composite)

    return {
        "manifest_version": "scriptorium-source-revision-manifest-v1",
        "candidate_id": "tolstoy-anna-karenina-ru",
        "provider": "Russian Wikisource",
        "source_work_url": "https://ru.wikisource.org/wiki/Анна_Каренина_(Толстой)",
        "source_work_index_revision_id": 3829834,
        "bibliographic_source": "ФЭБ. ЭНИ «Лев Толстой»; Толстой Л. Н. Анна Каренина. М.: Наука, 1970. С. 5–684.",
        "legal_basis": "public_domain",
        "composition": {
            "profile": COMPOSITE_PROFILE,
            "extraction_profile": EXTRACTION_PROFILE,
            "order": "part ascending, then chapter ascending, from the frozen 8-part/239-chapter contract",
            "chapter_separator": "\\n\\n",
            "source_text_committed": False,
            "part_chapter_counts": list(PART_CHAPTER_COUNTS),
        },
        "chapters": rows,
        "composite_identity": {
            "chapter_count": len(rows),
            "character_count_including_spaces": len(composite),
            "utf8_byte_count": len(composite.encode("utf-8")),
            "raw_sha256": _sha256_text(composite),
            "normalization_profile": NORMALIZATION_PROFILE,
            "normalized_character_count_including_spaces": len(normalized),
            "normalized_sha256": _sha256_text(normalized),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Freeze Anna Karenina Wikisource chapter revisions and derived identities."
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = build_manifest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
