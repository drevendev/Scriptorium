"""Capture source-free route identities for the 1907 Baturinsky translation."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re

TITLE = "Взаимная помощь как фактор эволюции (Кропоткин 1907)"
INDEX_ID = 5808217
SCAN_ID = 5571086
SCAN_TITLE = f"Индекс:{TITLE}.pdf"
SUFFIXES = ("Предисловие", "Введение", *(str(i) for i in range(1, 9)),
            "Заключение", *(f"Приложение/{i}" for i in range(1, 19)))
ROUTES = tuple(f"{TITLE}/{suffix}" for suffix in SUFFIXES)
# The pinned modern index links appendix III to the pre-reform variant.
# Keep the advertised target distinct from the modern route selected for analysis.
MODERN_III = f"{TITLE}/Приложение/3"
ADVERTISED_III = f"{MODERN_III}/ДО"
ADVERTISED_ROUTES = tuple(ADVERTISED_III if title == MODERN_III else title for title in ROUTES)
EXCLUDED = f"{TITLE}/Алфавитный указатель"
# Cyrillic titles expand substantially in the shared GET transport.
ROUTE_BATCH_SIZE = 4


def _identities(payload, expected):
    """Project only exact metadata, in contract order rather than API order."""
    pages = payload.get("query", {}).get("pages")
    if not isinstance(pages, list) or payload.get("continue"):
        raise ValueError("incomplete revision response")
    rows = {}
    seen = set()
    for page in pages:
        title = page.get("title")
        revs = page.get("revisions")
        if (title not in expected or title in rows or "missing" in page
                or not isinstance(revs, list) or len(revs) != 1):
            raise ValueError("missing, duplicate or unexpected source route")
        rev = revs[0]
        rid, ts, sha = rev.get("revid"), rev.get("timestamp"), rev.get("sha1")
        if (type(rid) is not int or rid <= 0 or rid in seen
                or (expected[title] is not None and rid != expected[title])
                or not isinstance(ts, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", ts)
                or not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha)):
            raise ValueError("invalid or drifting revision identity")
        datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        rows[title] = {"title": title, "revision_id": rid,
                       "revision_timestamp": ts, "mediawiki_sha1": sha}
        seen.add(rid)
    if set(rows) != set(expected):
        raise ValueError("incomplete source inventory")
    return [rows[title] for title in expected]


def _pinned_links(query, revision_id):
    parsed = query({"action": "parse", "oldid": str(revision_id), "prop": "links|revid"}).get("parse", {})
    links = parsed.get("links")
    if parsed.get("revid") != revision_id or not isinstance(links, list):
        raise ValueError("pinned link inventory not returned")
    return {row.get("title") for row in links if row.get("ns") == 0}


def capture(query):
    """Capture 29 modern routes and separately identify the advertised historical variant."""
    titles = _pinned_links(query, INDEX_ID)
    missing = [title.removeprefix(TITLE + "/") for title in (*ADVERTISED_ROUTES, EXCLUDED)
               if title not in titles]
    if missing:
        raise ValueError("pinned work index missing advertised routes: " + ", ".join(missing))
    anchors = _identities(query({"action": "query", "prop": "revisions",
                                "revids": f"{INDEX_ID}|{SCAN_ID}",
                                "rvprop": "ids|timestamp|sha1"}),
                          {TITLE: INDEX_ID, SCAN_TITLE: SCAN_ID})
    route_titles = (*ROUTES, ADVERTISED_III)
    rows = []
    for offset in range(0, len(route_titles), ROUTE_BATCH_SIZE):
        batch = route_titles[offset:offset + ROUTE_BATCH_SIZE]
        rows.extend(_identities(query({"action": "query", "prop": "revisions",
                                       "titles": "|".join(batch), "rvprop": "ids|timestamp|sha1"}),
                                dict.fromkeys(batch)))
    if len({row["revision_id"] for row in anchors + rows}) != len(anchors + rows):
        raise ValueError("duplicate identity across anchors and routes")
    modern = next(row for row in rows if row["title"] == MODERN_III)
    historical = rows.pop()
    if ADVERTISED_III not in _pinned_links(query, modern["revision_id"]):
        raise ValueError("modern appendix III lacks link to the advertised historical variant")
    return {"schema": "scriptorium-kropotkin-route-identities-v2",
            "candidate_id": "kropotkin-mutual-aid-baturinsky-1907-ru",
            "edition": "St Petersburg, Znanie, 1907; V. Baturinsky; modern orthography surface",
            "anchors": anchors, "routes": rows, "excluded_route": EXCLUDED,
            "index_route_exception": {"selected_modern_title": MODERN_III,
                                      "advertised_historical_identity": historical,
                                      "modern_revision_links_to_historical": True},
            "body_frozen": False, "transclusion_dependencies_frozen": False,
            "body_characters": None, "source_text_retained": False,
            "fantlab_input_identity": "unknown", "m2_parity_admissible": False}


def main(argv=None):
    from .wikisource_freeze import _api_query
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = capture(_api_query)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
