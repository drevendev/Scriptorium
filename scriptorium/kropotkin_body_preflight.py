"""Source-free body and dependency preflight for the accepted 1907 Mutual Aid routes."""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

from .kropotkin_revisions import ROUTES, SCAN_TITLE, _identities
from .wikisource_freeze import (
    BODY_FAILURE_CODES, BodyExtractionError, _api_query, extract_transcription_body,
)

# Accepted #628 receipt, not current-title lookup. Historical appendix III is excluded.
REVISION_IDS = (
    5712799, 3485537, 3485535, 3485534, 3485533, 3485532, 3485531,
    3485530, 3485529, 909443, 3485528, 3485527, 3485526, 3485525,
    3485524, 3485523, 3485522, 3485521, 3485520, 3485519, 3485518,
    3485516, 3485515, 3485514, 3485513, 3485512, 3485511, 3485510, 3485509,
)
EXPECTED = dict(zip(ROUTES, REVISION_IDS, strict=True))
SCAN = SCAN_TITLE.removeprefix("Индекс:")
SCHEMA = "scriptorium-kropotkin-body-preflight-v2"


# Literal selector plan only, not a claim about effective MediaWiki expansion.
# The hash of a decoded label allows matching exact section markers later without
# retaining arbitrary attribute values (which may themselves contain source text).
_SECTION = {"fromsection", "tosection", "onlysection"}
_PRESENTATION = {"header", "current", "prev", "next"}
_KNOWN = {"index", "from", "to", "step", "include", "exclude"} | _SECTION | _PRESENTATION


def classify_pages(attrs):
    fields = dict(attrs)
    names = set(fields)
    result = {
        "known_attributes": sorted(names & _KNOWN),
        "unknown_attribute_count": len(names - _KNOWN),
        "duplicate_attribute_count": len(attrs) - len(fields),
        "section_label_sha256": {},
        "candidate_scan_pages": [],
        "status": "UNRESOLVED",
        "reason": None,
    }
    def reject(reason):
        result["reason"] = reason
        return result

    if result["duplicate_attribute_count"]:
        return reject("DUPLICATE_ATTRIBUTE")
    if names - _KNOWN:
        return reject("UNKNOWN_ATTRIBUTE")
    if fields.get("index") != SCAN:
        return reject("INDEX_MISMATCH")
    # Do not infer the semantics of mixed include/exclude/range expressions.
    if names & {"include", "exclude"}:
        return reject("INCLUDE_EXCLUDE_UNSUPPORTED")
    if "onlysection" in names and names & {"fromsection", "tosection"}:
        return reject("MIXED_SECTION_SELECTORS")
    first, last, step = (fields.get("from"), fields.get("to"), fields.get("step", "1"))
    if not all(isinstance(v, str) and re.fullmatch(r"[0-9]{1,4}", v)
               for v in (first, last, step)):
        return reject("NON_LITERAL_NUMERIC_RANGE")
    first, last, step = int(first), int(last), int(step)
    if not 1 <= first <= last <= 4000 or not 1 <= step <= 4000:
        return reject("INVALID_RANGE_OR_STEP")
    labels = {}
    for key in sorted(names & _SECTION):
        label = fields[key]
        if (not isinstance(label, str) or not label.strip() or len(label) > 256
                or any(c in label for c in "{}<>|")
                or any(ord(c) < 32 for c in label)):
            return reject("NON_LITERAL_SECTION_LABEL")
        labels[key] = sha256(label.encode("utf-8")).hexdigest()
    result["section_label_sha256"] = labels
    result["candidate_scan_pages"] = list(range(first, last + 1, step))
    result["status"] = "LITERAL_CANDIDATE"
    return result


class _PagesProbe(HTMLParser):
    """Observe literal tags only; not a MediaWiki expansion or boundary proof."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ranges = []
        self.unresolved = 0
        self.selectors = []

    def handle_starttag(self, tag, attrs):
        if tag != "pages":
            return
        self.selectors.append(classify_pages(attrs))
        fields = dict(attrs)
        first, last = fields.get("from"), fields.get("to")
        if (len(fields) != len(attrs) or set(fields) != {"index", "from", "to"}
                or fields.get("index") != SCAN
                or not all(isinstance(x, str) and re.fullmatch(r"[0-9]{1,4}", x)
                           for x in (first, last))):
            self.unresolved += 1
            return
        first, last = int(first), int(last)
        if not 1 <= first <= last <= 4000:
            self.unresolved += 1
            return
        self.ranges.append({"first_page": first, "last_page": last})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def observe(source):
    raw = source.encode("utf-8")
    # This is a lexical preflight. Comments, nowiki and templates can change
    # effective inclusion; never interpret a literal range as a complete graph.
    probe = _PagesProbe()
    probe.feed(source)
    probe.close()
    row = {
        "wikitext_sha256": sha256(raw).hexdigest(),
        "wikitext_utf8_bytes": len(raw),
        "literal_pages_ranges": probe.ranges,
        "unresolved_pages_tags": probe.unresolved,
        "literal_page_selectors": probe.selectors,
        "raw_pages_openings": len(re.findall(r"<\s*pages\b", source, re.I)),
        "raw_template_openings": source.count("{{"),
        "raw_ref_openings": len(re.findall(r"<\s*ref\b", source, re.I)),
        "raw_nowiki_openings": len(re.findall(r"<\s*nowiki\b", source, re.I)),
        "candidate_body_characters": None,
        "candidate_body_sha256": None,
        "extraction_status": "NOT_RUN_DEPENDENCIES",
    }
    if row["raw_pages_openings"] or row["raw_nowiki_openings"]:
        return row
    try:
        body = extract_transcription_body(source)
    except BodyExtractionError as exc:
        row["extraction_status"] = exc.code if exc.code in BODY_FAILURE_CODES else "UNCLASSIFIED_ERROR"
    else:
        row["extraction_status"] = "CANDIDATE_ONLY"
        row["candidate_body_characters"] = len(body)
        row["candidate_body_sha256"] = sha256(body.encode("utf-8")).hexdigest()
    return row


def capture(query=_api_query):
    rows = []
    # Small sequential exact-revision GETs; no giant title URL or source on disk.
    for offset in range(0, len(ROUTES), 4):
        expected = {title: EXPECTED[title] for title in ROUTES[offset:offset + 4]}
        payload = query({"action": "query", "prop": "revisions",
                         "revids": "|".join(map(str, expected.values())),
                         "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
        identities = _identities(payload, expected)
        pages = {page["title"]: page for page in payload["query"]["pages"]}
        for identity in identities:
            rev = pages[identity["title"]]["revisions"][0]
            source = rev.get("slots", {}).get("main", {}).get("content")
            if not isinstance(source, str) or not source:
                raise ValueError("missing pinned route source")
            if sha1(source.encode("utf-8")).hexdigest() != identity["mediawiki_sha1"]:
                raise ValueError("pinned route source digest mismatch")
            rows.append({**identity, **observe(source)})
    selector_routes = [r for r in rows if r["raw_pages_openings"] == 1
                       and len(r["literal_page_selectors"]) == 1
                       and not r["raw_nowiki_openings"]
                       and r["literal_page_selectors"][0]["status"] == "LITERAL_CANDIDATE"]
    candidate_pages = sorted({p for r in selector_routes
                              for p in r["literal_page_selectors"][0]["candidate_scan_pages"]})
    return {
        "schema": SCHEMA, "candidate_id": "kropotkin-mutual-aid-baturinsky-1907-ru",
        "route_identity_acceptance_pr": 628,
        "routes": rows, "route_count": len(rows),
        "literal_selector_route_count": len(selector_routes),
        "candidate_scan_page_union": candidate_pages,
        "effective_page_graph_verified": False,
        "candidate_route_count": sum(r["extraction_status"] == "CANDIDATE_ONLY" for r in rows),
        "body_frozen": False, "body_characters": None,
        "transclusion_dependencies_frozen": False, "notes_boundary_verified": False,
        "source_text_retained": False, "fantlab_input_identity": "unknown",
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
        print("Pinned Kropotkin body preflight failed; no verified receipt.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
