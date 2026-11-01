"""Probe two pinned Robinson Crusoe translation revisions without retaining prose.

This probes *revision wikitext*, not the literary body. A Wikisource oldid does
not freeze the historical revisions of transcluded templates or subpages.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence
from urllib.parse import parse_qs, urlsplit

from .single_page_revision import _api_query

SCHEMA = "scriptorium-robinson-revision-inventory-v1"
REVISION_BY_WORK = {
    "defoe-robinson-trusov-1775-vol1-ru": 5041937,
    "defoe-robinson-shishmareva-1935-vol1-ru": 5634933,
}
_HEX40 = re.compile(r"[0-9a-f]{40}\Z")
_HEADING = re.compile(r"^={2,6}[^\n]+={2,6}\s*$", re.M)
_TEMPLATE = re.compile(r"\{\{")
_CATEGORY = re.compile(r"\[\[\s*Категория\s*:", re.I)
_TRANSCLUSION = re.compile(r"\{\{\s*:")
_PAGES = re.compile(r"<\s*pages\b", re.I)
_PAGE_LINK = re.compile(r"\[\[\s*(?:Страница|Page)\s*:", re.I)
_INCLUSION = re.compile(r"<\s*/?\s*(?:includeonly|noinclude|onlyinclude)\b", re.I)


def _validate_screening(screening: Mapping[str, object]) -> list[dict[str, object]]:
    if screening.get("schema_version") != "scriptorium-translation-pair-screening-v1":
        raise ValueError("unrecognized translation-pair screening schema")
    rows = screening.get("witnesses")
    if not isinstance(rows, list) or len(rows) != len(REVISION_BY_WORK):
        raise ValueError("expected exactly two translation witnesses")
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("witness must be a JSON object")
        work_id = row.get("work_id")
        if not isinstance(work_id, str) or work_id not in REVISION_BY_WORK or work_id in seen:
            raise ValueError("unrecognized or duplicate translation witness")
        seen.add(work_id)
        revision = row.get("revision_oldid")
        if type(revision) is not int or revision != REVISION_BY_WORK[work_id]:
            raise ValueError("translation witness revision drift")
        url = row.get("source_revision")
        if not isinstance(url, str):
            raise ValueError("translation source URL missing")
        parsed = urlsplit(url)
        if (parsed.scheme, parsed.hostname, parsed.port, parsed.path, parsed.fragment,
            parsed.username, parsed.password) != (
            "https", "ru.wikisource.org", None, "/w/index.php", "", None, None
        ):
            raise ValueError("untrusted translation source URL")
        params = parse_qs(parsed.query, strict_parsing=True)
        if params != {"oldid": [str(revision)]}:
            raise ValueError("translation source URL oldid drift")
    if seen != set(REVISION_BY_WORK):
        raise ValueError("translation pair incomplete")
    return rows


def _observe_revision(
    revision_id: int,
    *,
    query: Callable[[dict[str, str]], dict[str, object]],
) -> dict[str, object]:
    payload = query({
        "action": "query",
        "prop": "revisions",
        "revids": str(revision_id),
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
    })
    if not isinstance(payload, dict) or "error" in payload:
        raise ValueError("MediaWiki revision query rejected")
    query_response = payload.get("query")
    pages = query_response.get("pages") if isinstance(query_response, dict) else None
    if not isinstance(pages, list) or len(pages) != 1:
        raise ValueError("expected one pinned revision page")
    page = pages[0]
    if not isinstance(page, dict):
        raise ValueError("invalid MediaWiki page")
    title = page.get("title")
    page_id = page.get("pageid")
    revisions = page.get("revisions")
    if not isinstance(title, str) or not title or type(page_id) is not int or page_id <= 0:
        raise ValueError("pinned page identity missing")
    if not isinstance(revisions, list) or len(revisions) != 1 or not isinstance(revisions[0], dict):
        raise ValueError("expected exactly one pinned revision")
    rev = revisions[0]
    if type(rev.get("revid")) is not int or rev["revid"] != revision_id:
        raise ValueError("MediaWiki returned wrong revision")
    timestamp = rev.get("timestamp")
    mediawiki_sha1 = rev.get("sha1")
    if not isinstance(timestamp, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", timestamp):
        raise ValueError("pinned revision UTC timestamp missing")
    if not isinstance(mediawiki_sha1, str) or not _HEX40.fullmatch(mediawiki_sha1):
        raise ValueError("MediaWiki revision SHA-1 invalid")
    slots = rev.get("slots")
    main = slots.get("main") if isinstance(slots, dict) else None
    wikitext = main.get("content") if isinstance(main, dict) else None
    if not isinstance(wikitext, str) or not wikitext:
        raise ValueError("missing pinned revision main-slot wikitext")
    if main.get("contentmodel", "wikitext") != "wikitext":
        raise ValueError("unsupported MediaWiki content model")
    encoded = wikitext.encode("utf-8")
    if len(encoded) > 8_000_000:
        raise ValueError("pinned revision exceeds bounded inventory limit")
    return {
        "revision_id": revision_id,
        "page_id": page_id,
        "title": title,
        "timestamp_utc": timestamp,
        "mediawiki_sha1": mediawiki_sha1,
        "wikitext_sha256": sha256(encoded).hexdigest(),
        "wikitext_utf8_bytes": len(encoded),
        "wikitext_characters_including_spaces": len(wikitext),
        "markup_inventory": {
            "headings": len(_HEADING.findall(wikitext)),
            "template_openers": len(_TEMPLATE.findall(wikitext)),
            "transclusion_openers": len(_TRANSCLUSION.findall(wikitext)),
            "pages_tags": len(_PAGES.findall(wikitext)),
            "page_namespace_links": len(_PAGE_LINK.findall(wikitext)),
            "category_links": len(_CATEGORY.findall(wikitext)),
            "inclusion_tags": len(_INCLUSION.findall(wikitext)),
        },
        "historical_transclusion_dependencies": "UNRESOLVED",
        "literary_body_sha256": None,
        "literary_characters_including_spaces": None,
        "body_extraction_status": "NOT_RUN",
        "corpus_threshold_verified": False,
        "admitted_for_calibration": False,
        "fantlab_input_identity": "UNKNOWN",
        "m2_parity_admissible": False,
    }


def probe_pair(
    screening: Mapping[str, object],
    *,
    query: Callable[[dict[str, str]], dict[str, object]] = _api_query,
) -> dict[str, object]:
    """Return only source-free identities/structure; never infer a full-book body."""
    rows = _validate_screening(screening)
    observed: list[dict[str, object]] = []
    for row in rows:
        work_id = str(row["work_id"])
        observed.append({"work_id": work_id, **_observe_revision(REVISION_BY_WORK[work_id], query=query)})
    return {
        "schema_version": SCHEMA,
        "input_screening_sha256": sha256(
            json.dumps(screening, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "witnesses": observed,
        "source_text_committed": False,
        "both_literary_bodies_frozen": False,
        "first_narrative_scope_match": "NOT_VERIFIED",
        "comparison_status": "NOT_RUN",
        "m2_contribution": 0,
        "status": "REVISION_WIKITEXT_INVENTORY_ONLY",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Source-free inventory of two pinned Robinson Crusoe translation revisions.")
    parser.add_argument("--screening", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.screening.resolve() == args.output.resolve():
        parser.error("output cannot replace the screening record")
    screening = json.loads(args.screening.read_text(encoding="utf-8"))
    if not isinstance(screening, dict):
        raise ValueError("screening JSON must be an object")
    inventory = probe_pair(screening, query=_api_query)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as dest:
        dest.write(json.dumps(inventory, sort_keys=True, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
