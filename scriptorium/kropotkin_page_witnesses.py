"""Capture source-free Page revision witnesses for the accepted partial scan union."""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

from .kropotkin_body_preflight import SCAN, REVISION_IDS
from .kropotkin_revisions import _identities
from .wikisource_freeze import _api_query

# Independently accepted #630: 27 literal routes, not full book coverage.
PAGES = tuple(range(23, 348))
BATCH_SIZE = 4
SCHEMA = "scriptorium-kropotkin-page-witnesses-v1"


class _Markers(HTMLParser):
    """Lexical observation only, not proof of effective section transclusion."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.markers = []
        self.unresolved = 0

    def handle_starttag(self, tag, attrs):
        if tag != "section":
            return
        if len(attrs) != 1:
            self.unresolved += 1
            return
        kind, label = attrs[0]
        if (kind not in {"begin", "end"} or not isinstance(label, str)
                or not label.strip() or len(label) > 256
                or any(c in label for c in "{}<>|")
                or any(ord(c) < 32 for c in label)):
            self.unresolved += 1
            return
        self.markers.append({"kind": kind, "label_sha256":
                             sha256(label.encode("utf-8")).hexdigest()})


def observe(source):
    raw = source.encode("utf-8")
    parser = _Markers()
    parser.feed(source)
    parser.close()
    return {
        "wikitext_sha256": sha256(raw).hexdigest(),
        "wikitext_utf8_bytes": len(raw),
        "literal_section_markers": parser.markers,
        "unresolved_section_tags": parser.unresolved,
        "raw_section_openings": len(re.findall(r"<\s*section\b", source, re.I)),
        "raw_nowiki_openings": len(re.findall(r"<\s*nowiki\b", source, re.I)),
        "raw_template_openings": source.count("{{"),
        "raw_ref_openings": len(re.findall(r"<\s*ref\b", source, re.I)),
    }


def capture(query=_api_query):
    rows = []
    seen = set(REVISION_IDS)
    for offset in range(0, len(PAGES), BATCH_SIZE):
        expected = {f"Страница:{SCAN}/{n}": n
                    for n in PAGES[offset:offset + BATCH_SIZE]}
        payload = query({"action": "query", "prop": "revisions",
                         "titles": "|".join(expected),
                         "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
        identities = _identities(payload, dict.fromkeys(expected))
        pages = {p["title"]: p for p in payload["query"]["pages"]}
        for row in identities:
            rid = row["revision_id"]
            if rid in seen:
                raise ValueError("duplicate Page revision identity")
            seen.add(rid)
            page = pages[row["title"]]
            if page.get("ns") != 104 or "redirect" in page:
                raise ValueError("unexpected Page namespace or redirect")
            rev = page["revisions"][0]
            source = rev.get("slots", {}).get("main", {}).get("content")
            if not isinstance(source, str) or not source:
                raise ValueError("missing Page source")
            if sha1(source.encode("utf-8")).hexdigest() != row["mediawiki_sha1"]:
                raise ValueError("Page source digest mismatch")
            rows.append({**row, "scan_page": expected[row["title"]], **observe(source)})
    return {
        "schema": SCHEMA,
        "candidate_id": "kropotkin-mutual-aid-baturinsky-1907-ru",
        "selector_acceptance_pr": 630,
        "selector_receipt_sha256": "264c6cfc876c5e03d8948f19d96c19911db300349b18dc20621bc667f84a05c7",
        "candidate_scan_pages": list(PAGES),
        "page_count": len(rows),
        "pages": rows,
        "unresolved_route_count": 2,
        "complete_page_inventory": False,
        "effective_page_graph_verified": False,
        "transclusion_dependencies_frozen": False,
        "notes_boundary_verified": False,
        "body_frozen": False,
        "body_characters": None,
        "source_text_retained": False,
        "fantlab_input_identity": "unknown",
        "m2_parity_admissible": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = capture()
        serialized = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
    except Exception:
        print("Partial Kropotkin Page capture failed; no verified receipt.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
