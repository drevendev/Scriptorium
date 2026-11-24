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
EXCLUDED = f"{TITLE}/Алфавитный указатель"


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


def capture(query):
    """Read index anchors and 29 current route revisions, never prose or page content."""
    parsed = query({"action": "parse", "oldid": str(INDEX_ID), "prop": "links|revid"}).get("parse", {})
    links = parsed.get("links")
    if parsed.get("revid") != INDEX_ID or not isinstance(links, list):
        raise ValueError("pinned work index not returned")
    titles = {row.get("title") for row in links if row.get("ns") == 0}
    if not set((*ROUTES, EXCLUDED)).issubset(titles):
        raise ValueError("pinned work index missing advertised routes")
    anchors = _identities(query({"action": "query", "prop": "revisions",
                                "revids": f"{INDEX_ID}|{SCAN_ID}",
                                "rvprop": "ids|timestamp|sha1"}),
                          {TITLE: INDEX_ID, SCAN_TITLE: SCAN_ID})
    rows = _identities(query({"action": "query", "prop": "revisions",
                             "titles": "|".join(ROUTES), "rvprop": "ids|timestamp|sha1"}),
                       dict.fromkeys(ROUTES))
    if len({row["revision_id"] for row in anchors + rows}) != len(anchors + rows):
        raise ValueError("duplicate identity across anchors and routes")
    return {"schema": "scriptorium-kropotkin-route-identities-v1",
            "candidate_id": "kropotkin-mutual-aid-baturinsky-1907-ru",
            "edition": "St Petersburg, Znanie, 1907; V. Baturinsky; modern orthography surface",
            "anchors": anchors, "routes": rows, "excluded_route": EXCLUDED,
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
