"""Observe today's parser output for seven pinned Trusov Page revisions.

This is a Page-view diagnostic, not historical transclusion or scan collation.
Only hashes, counts and fixed status labels leave memory.
"""
from __future__ import annotations

import argparse
from difflib import SequenceMatcher
from hashlib import sha256
from unicodedata import category
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
        self.skipped_nonspace = 0

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
        if self.stack and self.stack[-1][1]:
            if self.stack[-1][2]:
                self.skipped_nonspace += sum(not c.isspace() for c in data)
            else:
                self.parts.append(data)


def _observe(html, *, scope_counts=False):
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
    row = {"status": status, "html_sha256": digest(html),
            "html_utf8_bytes": len(html.encode("utf-8")),
            "pagetext_containers": p.containers, "parser_error_elements": p.errors,
            "candidate_sha256": digest(text) if status == "PAGE_VIEW_CANDIDATE" else None,
            "candidate_characters": len(text) if status == "PAGE_VIEW_CANDIDATE" else None}
    if scope_counts:
        row["skipped_body_nonspace_characters"] = p.skipped_nonspace
    return row, text if status == "PAGE_VIEW_CANDIDATE" else None


def observe(html):
    return _observe(html)[0]


def nonspace_edit_summary(projected, rendered):
    """Aggregate alignment only: no excerpts, positions, or changed-span hashes.

    SequenceMatcher is a deterministic heuristic, not a minimal edit distance
    or evidence of historical parser equivalence. Bound quadratic worst cases.
    """
    left, right = ("".join(value.split()) for value in (projected, rendered))
    if max(len(left), len(right)) > 8192:
        return {"status": "SIZE_LIMIT"}
    categories = ("L", "M", "N", "P", "S", "Z", "C")
    removed = dict.fromkeys(categories, 0)
    added = dict.fromkeys(categories, 0)
    runs = dict.fromkeys(("replace", "delete", "insert"), 0)
    matching = removed_apostrophes = added_apostrophes = 0
    for op, i, j, k, l in SequenceMatcher(None, left, right, autojunk=False).get_opcodes():
        if op == "equal":
            matching += j - i
            continue
        runs[op] += 1
        for char in left[i:j]:
            removed[category(char)[0]] += 1
            removed_apostrophes += char == "'"
        for char in right[k:l]:
            added[category(char)[0]] += 1
            added_apostrophes += char == "'"
    return {
        "status": "ALIGNED",
        "method": "sequence-matcher-nonspace-autojunk-false-v1",
        "matching_characters": matching,
        "edit_runs": runs,
        "projected_changed_unicode_categories": removed,
        "rendered_changed_unicode_categories": added,
        "projected_changed_ascii_apostrophes": removed_apostrophes,
        "rendered_changed_ascii_apostrophes": added_apostrophes,
    }


def compare_control(projected, prior, candidate):
    """Distinguish whitespace-only drift without stripping markup or spelling."""
    if (digest(projected) != prior["projected_wikitext_sha256"] or
            len(projected) != prior["projected_wikitext_characters_including_spaces"] or
            prior["unresolved_invocations"] != 0 or prior["unclassified_openers"] != 0):
        raise ValueError("control projection identity or unresolved markup drift")
    collapsed = " ".join(projected.split())
    nonspace = "".join(projected.split())
    result = {
        "projected_collapsed_sha256": digest(collapsed),
        "projected_collapsed_characters": len(collapsed),
        "projected_nonspace_sha256": digest(nonspace),
        "projected_nonspace_characters": len(nonspace),
        "rendered_nonspace_sha256": None,
        "rendered_nonspace_characters": None,
        "classification": "RENDER_REFUSED",
        "nonspace_edit_summary": {"status": "RENDER_REFUSED"},
    }
    if candidate is not None:
        rendered = "".join(candidate.split())
        result["nonspace_edit_summary"] = nonspace_edit_summary(projected, candidate)
        result.update(rendered_nonspace_sha256=digest(rendered),
                      rendered_nonspace_characters=len(rendered))
        result["classification"] = (
            "COLLAPSED_EQUAL" if collapsed == candidate else
            "NONSPACE_EQUAL_ONLY" if nonspace == rendered else
            "NONSPACE_DIFFERS")
    return result


def capture(graph, projection, *, graph_sha256, query=_api_query,
            projected_controls=None):
    if projected_controls is not None and set(projected_controls) != set(CONTROLS):
        raise ValueError("exactly two projected controls required")
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
    for p, prior in zip(pages, projected, strict=True):
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
        obs, candidate = _observe(result.get("text"), scope_counts=
                                  projected_controls is not None and seq in CONTROLS)
        if projected_controls is not None and seq in CONTROLS:
            obs["whitespace_control"] = compare_control(projected_controls[seq], prior, candidate)
        rows.append({"page_sequence": seq, "revision_id": p["revision_id"],
                     "source_mediawiki_sha1": p["mediawiki_sha1"],
                     "role": "BOUNDARY" if seq in BOUNDARIES else "INTERIOR_CONTROL",
                     "template_dependency_count": len(deps),
                     "template_dependency_names_sha256": digest(
                         json.dumps(deps_key, ensure_ascii=False, separators=(",", ":"))),
                     **obs})
    return {"schema_version": SCHEMA if projected_controls is None else
            "scriptorium-trusov-boundary-render-v3",
            "scope": "CURRENT_PARSER_PINNED_PAGE_VIEW_ONLY",
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
