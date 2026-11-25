"""Diagnostic modern-route rendered extraction; oldid does not pin dependencies."""
from __future__ import annotations

import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

from .kropotkin_body_preflight import REVISION_IDS, SCAN
from .kropotkin_revisions import ROUTES
from .wikisource_freeze import _api_query

_VOID = set("area base br col embed hr img input link meta param source track wbr".split())
_BLOCK = set("p div h1 h2 h3 h4 h5 h6 li dt dd tr td th blockquote br hr".split())
_SKIP = {"reference", "references", "mw-editsection", "mw-cite-backlink",
         "pagenum", "prp-page-number", "ws-pagenum", "noprint"}
_HIDDEN = {"script", "style", "noscript", "template"}


def _digest(value):
    return sha256(value.encode("utf-8")).hexdigest()


def _clean(parts):
    return "\n".join(line for line in
                     (" ".join(line.split()) for line in "".join(parts).split("\n"))
                     if line)


class _Rendered(HTMLParser):
    """Only the ProofreadPage output container, plus separately observed notes."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.containers = 0
        self.body = []
        self.notes = []
        self.note_items = 0
        self.bad = False

    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        classes = set((fields.get("class") or "").split())
        body, note, skip = self.stack[-1][1:] if self.stack else (False, False, False)
        if "prp-pages-output" in classes:
            self.containers += 1
            body = True
        if tag == "li" and (fields.get("id") or "").startswith("cite_note-"):
            self.note_items += 1
            note = True
            body = False
            self.notes.append("\n")
        # Reference lists are excluded from body, but note text is captured separately.
        skip = skip or tag in _HIDDEN or "hidden" in fields or fields.get("aria-hidden") == "true"
        if classes & (_SKIP - {"references"}) or ("references" in classes and not note):
            if "references" in classes and not note:
                body = False
            else:
                skip = True
        if tag in _BLOCK and not skip:
            if note:
                self.notes.append("\n")
            elif body:
                self.body.append("\n")
        if tag not in _VOID:
            self.stack.append((tag, body, note, skip))

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
        _, body, note, skip = self.stack.pop()
        if tag in _BLOCK and not skip:
            if note:
                self.notes.append("\n")
            elif body:
                self.body.append("\n")

    def handle_data(self, data):
        if self.stack:
            _, body, note, skip = self.stack[-1]
            if not skip:
                if note:
                    self.notes.append(data)
                elif body:
                    self.body.append(data)


def extract(html):
    parser = _Rendered()
    parser.feed(html)
    parser.close()
    if parser.bad or parser.stack:
        return "UNBALANCED_HTML", None, None, parser.note_items
    if parser.containers != 1:
        return "BODY_CONTAINER_COUNT", None, None, parser.note_items
    body, notes = _clean(parser.body), _clean(parser.notes)
    if not body:
        return "EMPTY_BODY", None, None, parser.note_items
    return "RENDERED_CANDIDATE", body, notes, parser.note_items


def capture(selectors, query=_api_query):
    expected = list(zip(ROUTES, REVISION_IDS, strict=True))
    routes = selectors.get("routes", [])
    if [(r["title"], r["revision_id"]) for r in routes] != expected:
        raise ValueError("selector route identity drift")
    rows, bodies = [], []
    for (title, revision), route in zip(expected, routes, strict=True):
        plans = route["literal_page_selectors"]
        if len(plans) != 1 or plans[0]["status"] != "LITERAL_CANDIDATE":
            raise ValueError("unresolved literal selector")
        candidates = set(plans[0]["candidate_scan_pages"])
        result = query({"action": "parse", "oldid": str(revision),
                        "prop": "text|revid|templates", "disableeditsection": "1"}).get("parse", {})
        html, deps = result.get("text"), result.get("templates")
        if (result.get("revid") != revision or result.get("title") != title
                or not isinstance(html, str) or not isinstance(deps, list)):
            raise ValueError("rendered route identity or response drift")
        scans = set()
        other_pages = 0
        for dep in deps:
            if type(dep.get("ns")) is not int or not isinstance(dep.get("title"), str):
                raise ValueError("invalid rendered dependency metadata")
            if dep["ns"] == 104:
                prefix = f"Страница:{SCAN}/"
                name = dep["title"]
                if name.startswith(prefix) and re.fullmatch(r"[0-9]+", name[len(prefix):]):
                    scans.add(int(name[len(prefix):]))
                else:
                    other_pages += 1
        status, body, notes, note_items = extract(html)
        if body is not None:
            bodies.append(body)
        rows.append({
            "revision_id": revision, "title": title, "status": status,
            "rendered_html_sha256": _digest(html),
            "body_sha256": _digest(body) if body is not None else None,
            "body_characters": len(body) if body is not None else None,
            "notes_sha256": _digest(notes) if notes is not None else None,
            "notes_characters": len(notes) if notes is not None else None,
            "note_item_count": note_items,
            "historical_letter_count": sum(c in "ѣѢіІѳѲѵѴ" for c in body) if body is not None else None,
            "reported_page_scans": sorted(scans),
            "missing_candidate_scans": sorted(candidates - scans),
            "unexpected_reported_scans": sorted(scans - candidates),
            "other_page_dependency_count": other_pages,
            "reported_dependency_count": len(deps),
        })
    combined = "\n\n".join(bodies) if len(bodies) == len(expected) else None
    return {
        "schema": "scriptorium-kropotkin-rendered-diagnostic-v1",
        "route_count": len(rows), "extracted_route_count": len(bodies), "routes": rows,
        "candidate_composite_sha256": _digest(combined) if combined is not None else None,
        "candidate_composite_characters": len(combined) if combined is not None else None,
        "candidate_meets_size_threshold": len(combined) >= 300000 if combined is not None else None,
        "effective_page_graph_verified": False, "transclusion_dependencies_frozen": False,
        "notes_boundary_verified": False, "body_frozen": False, "source_text_retained": False,
        "fantlab_input_identity": "unknown", "m2_parity_admissible": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selectors", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        raw = args.selectors.read_bytes()
        from .kropotkin_page_witnesses import FRONT_SELECTOR_SHA256
        if sha256(raw).hexdigest() != FRONT_SELECTOR_SHA256:
            raise ValueError("selector receipt digest drift")
        report = capture(json.loads(raw))
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
    except Exception:
        print("Rendered candidate capture failed; no verified diagnostic.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
