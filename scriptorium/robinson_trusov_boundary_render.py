"""Observe today's parser output for seven pinned Trusov Page revisions.

This is a Page-view diagnostic, not historical transclusion or scan collation.
Only hashes, counts and fixed status labels leave memory.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path

from .robinson_trusov_pages import verify_frozen_graph
from .single_page_revision import _api_query

BOUNDARIES = (2, 148, 149, 150, 151)
CONTROLS = (3, 147)
SELECTED = (2, 3, 147, 148, 149, 150, 151)
SCHEMA = "scriptorium-trusov-boundary-render-v1"
_VOID = set("area base br col embed hr img input link meta param source track wbr".split())
_BLOCK = set("p div h1 h2 h3 h4 h5 h6 li br hr td tr blockquote".split())
_SKIP = {"prp-page-qualityheader", "prp-page-image", "mw-editsection",
         "reference", "references", "noprint", "pagenum"}


def digest(text):
    return sha256(text.encode("utf-8")).hexdigest()


class PageView(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.parts = []
        self.containers = 0
        self.errors = 0
        self.bad = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set((attrs.get("class") or "").split())
        inside, skip = self.stack[-1][1:] if self.stack else (False, False)
        if "pagetext" in classes:
            inside = True
            self.containers += 1
        skip = (skip or bool(classes & _SKIP) or tag in
                {"script", "style", "template", "noscript"} or
                "hidden" in attrs or attrs.get("aria-hidden") == "true")
        if inside and classes & {"error", "mw-error", "scribunto-error",
                                 "mw-ext-cite-error"}:
            self.errors += 1
        if inside and not skip and tag in _BLOCK:
            self.parts.append(" ")
        if tag not in _VOID:
            self.stack.append((tag, inside, skip))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in _VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in _VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.bad = True
            return
        _, inside, skip = self.stack.pop()
        if inside and not skip and tag in _BLOCK:
            self.parts.append(" ")

    def handle_data(self, data):
        if self.stack and self.stack[-1][1] and not self.stack[-1][2]:
            self.parts.append(data)


def observe(html):
    if not isinstance(html, str) or len(html.encode("utf-8")) > 1_000_000:
        raise ValueError("missing or oversized Page render")
    p = PageView()
    p.feed(html)
    p.close()
    text = " ".join("".join(p.parts).split())
    if p.bad or p.stack:
        status = "UNBALANCED_HTML"
    elif p.containers != 1:
        status = "BODY_CONTAINER_COUNT"
    elif p.errors:
        status = "PARSER_ERROR_ELEMENT"
    elif not text:
        status = "EMPTY_CANDIDATE"
    elif "{{" in text or "}}" in text:
        status = "UNEXPANDED_BRACES"
    else:
        status = "PAGE_VIEW_CANDIDATE"
    return {"status": status, "html_sha256": digest(html),
            "html_utf8_bytes": len(html.encode("utf-8")),
            "pagetext_containers": p.containers, "parser_error_elements": p.errors,
            "candidate_sha256": digest(text) if status == "PAGE_VIEW_CANDIDATE" else None,
            "candidate_characters": len(text) if status == "PAGE_VIEW_CANDIDATE" else None}


def capture(graph, projection, *, graph_sha256, query=_api_query):
    if projection.get("source_page_graph_sha256") != graph_sha256:
        raise ValueError("projection graph identity drift")
    pages = graph["pages"]
    projected = projection["pages"]
    if [p["page_sequence"] for p in pages] != list(range(2, 152)):
        raise ValueError("unexpected frozen Page coverage")
    if len(projected) != len(pages):
        raise ValueError("incomplete projection coverage")
    rows = []
    for p, prior in zip(pages, projected, strict=True):
        identity = (p["page_sequence"], p["revision_id"], p["mediawiki_sha1"])
        if identity != (prior["page_sequence"], prior["revision_id"],
                        prior["source_mediawiki_sha1"]):
            raise ValueError("projection Page identity drift")
    for p in pages:
        seq = p["page_sequence"]
        if seq not in SELECTED:
            continue
        result = query({"action": "parse", "oldid": str(p["revision_id"]),
                        "prop": "text|revid|templates", "disableeditsection": "1"}).get("parse", {})
        if (result.get("revid") != p["revision_id"] or
                result.get("title") != p["title"] or
                result.get("pageid") != p["page_id"]):
            raise ValueError("rendered Page identity drift")
        deps = result.get("templates")
        if not isinstance(deps, list) or any(
            not isinstance(d, dict) or type(d.get("ns")) is not int or
            not isinstance(d.get("title"), str) for d in deps
        ):
            raise ValueError("invalid dependency metadata")
        deps_key = sorted((d["ns"], d["title"]) for d in deps)
        obs = observe(result.get("text"))
        rows.append({"page_sequence": seq, "revision_id": p["revision_id"],
                     "source_mediawiki_sha1": p["mediawiki_sha1"],
                     "role": "BOUNDARY" if seq in BOUNDARIES else "INTERIOR_CONTROL",
                     "template_dependency_count": len(deps),
                     "template_dependency_names_sha256": digest(
                         json.dumps(deps_key, ensure_ascii=False, separators=(",", ":"))),
                     **obs})
    return {"schema_version": SCHEMA, "scope": "CURRENT_PARSER_PINNED_PAGE_VIEW_ONLY",
            "source_page_graph_sha256": graph_sha256, "pages": rows,
            "historical_dependencies_pinned": False, "scan_collation_verified": False,
            "full_literary_body": "NOT_VERIFIED", "corpus_admitted": False,
            "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False,
            "source_text_committed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("graph", "receipt", "projection", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    graph = verify_frozen_graph(args.graph, args.receipt)
    report = capture(graph, json.loads(args.projection.read_text(encoding="utf-8")),
                     graph_sha256=sha256(args.graph.read_bytes()).hexdigest())
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
