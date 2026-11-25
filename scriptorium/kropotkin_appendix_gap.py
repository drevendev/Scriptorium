"""Exact-revision Appendix XIII gap diagnosis; never repair or compose a body."""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
import json
from pathlib import Path
import sys

from .kropotkin_body_preflight import SCAN, observe as route_observe
from .kropotkin_page_witnesses import (
    ACCEPTED_RECEIPT_SHA256, FRONT_SELECTOR_SHA256, PAGES, PINNED_PAGE_IDS, _Markers,
)
from .kropotkin_revisions import TITLE, _identities
from .kropotkin_rendered import extract
from .wikisource_freeze import _api_query

MODERN = f"{TITLE}/Приложение/13"
HISTORICAL = f"{MODERN}/ДО"
PAGE = f"Страница:{SCAN}/335"
PINS = {MODERN: 3485514, HISTORICAL: 3485499, PAGE: 5800299}


def digest(value):
    return sha256(value.encode("utf-8")).hexdigest()


class _Offsets(_Markers):
    """Locate lexical markers; offsets do not establish MediaWiki semantics."""

    def __init__(self, source):
        super().__init__()
        self.starts = [0]
        for line in source.split("\n")[:-1]:
            self.starts.append(self.starts[-1] + len(line) + 1)
        self.offsets = []

    def handle_starttag(self, tag, attrs):
        before = len(self.markers)
        super().handle_starttag(tag, attrs)
        if len(self.markers) != before:
            line, column = self.getpos()
            start = self.starts[line - 1] + column
            self.offsets.append((start, start + len(self.get_starttag_text())))


def section_probe(source, selector):
    labels = selector["section_label_sha256"]
    label = labels.get("onlysection")
    if label is None and set(labels) == {"fromsection", "tosection"}:
        if labels["fromsection"] == labels["tosection"]:
            label = labels["fromsection"]
    if selector["candidate_scan_pages"] != [335] or not label:
        return {"status": "NOT_SINGLE_SECTION"}
    parser = _Offsets(source)
    parser.feed(source)
    parser.close()
    matches = [(m["kind"], pos) for m, pos in zip(parser.markers, parser.offsets, strict=True)
               if m["label_sha256"] == label]
    if parser.unresolved or [kind for kind, _ in matches] != ["begin", "end"]:
        return {"status": "AMBIGUOUS_LEXICAL_MARKERS", "matching_marker_count": len(matches)}
    span = source[matches[0][1][1]:matches[1][1][0]]
    return {"status": "LEXICAL_SPAN", "section_label_sha256": label,
            "raw_span_sha256": digest(span), "raw_span_characters": len(span),
            "raw_non_whitespace_characters": sum(not c.isspace() for c in span)}


def capture(selectors, witnesses, query=_api_query):
    if dict(zip(PAGES, PINNED_PAGE_IDS, strict=True)).get(335) != PINS[PAGE]:
        raise ValueError("accepted scan pin drift")
    payload = query({"action": "query", "prop": "revisions",
                     "revids": "|".join(map(str, PINS.values())),
                     "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
    identities = _identities(payload, PINS)
    sources = {}
    for identity in identities:
        title = identity["title"]
        page = next(p for p in payload["query"]["pages"] if p["title"] == title)
        source = page["revisions"][0].get("slots", {}).get("main", {}).get("content")
        if (page.get("ns") != (104 if title == PAGE else 0) or "redirect" in page
                or not isinstance(source, str) or not source
                or sha1(source.encode("utf-8")).hexdigest() != identity["mediawiki_sha1"]):
            raise ValueError("invalid exact source witness")
        sources[title] = source
    page_row = next(row for row in witnesses["pages"] if row["scan_page"] == 335)
    modern_row = next(row for row in selectors["routes"] if row["title"] == MODERN)
    for row, title in ((page_row, PAGE), (modern_row, MODERN)):
        if row["revision_id"] != PINS[title] or row["wikitext_sha256"] != digest(sources[title]):
            raise ValueError("accepted witness digest drift")
    rows = []
    for title in (MODERN, HISTORICAL):
        observed = route_observe(sources[title])
        plans = observed["literal_page_selectors"]
        span = {"status": "UNRESOLVED_ROUTE_SELECTOR"}
        if len(plans) == 1 and plans[0]["status"] == "LITERAL_CANDIDATE":
            span = section_probe(sources[PAGE], plans[0])
        parsed = query({"action": "parse", "oldid": str(PINS[title]),
                        "prop": "text|revid|templates", "disableeditsection": "1"}).get("parse", {})
        if (parsed.get("title") != title or parsed.get("revid") != PINS[title]
                or not isinstance(parsed.get("text"), str)
                or not isinstance(parsed.get("templates"), list)):
            raise ValueError("rendered variant identity drift")
        status, body, notes, note_items = extract(parsed["text"])
        rows.append({"revision_id": PINS[title], "variant": "modern" if title == MODERN else "historical",
                     "source_sha256": digest(sources[title]), "literal_selectors": plans,
                     "lexical_section": span, "rendered_status": status,
                     "rendered_html_sha256": digest(parsed["text"]),
                     "rendered_body_sha256": digest(body) if body is not None else None,
                     "rendered_body_characters": len(body) if body is not None else None,
                     "note_item_count": note_items,
                     "reported_scan_335": any(d.get("ns") == 104 and d.get("title") == PAGE
                                              for d in parsed["templates"])})
    return {"schema": "scriptorium-kropotkin-appendix-xiii-gap-v1",
            "identities": identities, "page_sha256": digest(sources[PAGE]), "variants": rows,
            "accepted_page_and_modern_route_replayed": True,
            "effective_page_graph_verified": False, "notes_boundary_verified": False,
            "normalization_performed": False, "body_frozen": False,
            "body_characters": None, "source_text_retained": False,
            "fantlab_input_identity": "unknown", "m2_parity_admissible": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selectors", type=Path, required=True)
    parser.add_argument("--witnesses", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        inputs = []
        for path, expected in ((args.selectors, FRONT_SELECTOR_SHA256),
                               (args.witnesses, ACCEPTED_RECEIPT_SHA256)):
            raw = path.read_bytes()
            if sha256(raw).hexdigest() != expected:
                raise ValueError("accepted receipt digest drift")
            inputs.append(json.loads(raw))
        report = capture(*inputs)
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
    except Exception:
        print("Appendix XIII gap capture failed; no verified receipt.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
