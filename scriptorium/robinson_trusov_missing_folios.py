"""Source-free replay of the two noinclude markers on pinned Trusov Page 107."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from .robinson_trusov_content import transclusion_input, verify_receipt
from .robinson_trusov_projection import project_page
from .robinson_trusov_interior import _UNRENDERED_MARKUP
from .robinson_trusov_pages import verify_frozen_graph
from .robinson_trusov_errata import digest
from .robinson_trusov_boundary_render import PageView
from .single_page_revision import _api_query

PINS = {106: 4958613, 107: 4958614, 108: 4958615}
LABELS = ("Текст со страниц 210-211 ---", "Конец текста со страниц 210-211 ---")
WRAPPERS = tuple("<noinclude> ;" + label + " </noinclude>" for label in LABELS)


def normalized(text):
    return " ".join(text.split())


def markers(text):
    # Count the end marker separately: the initial marker is case-sensitive.
    return [text.count(label) for label in LABELS]


# Marker whitespace is layout inside an exact, attribute-free noinclude block.
# Do not normalize any of the surrounding narrative or the marker label itself.
_MARKER_PATTERNS = tuple(
    re.compile(r"<noinclude>[ \t\r\n]*;[ \t]*" + re.escape(label)
               + r"[ \t\r\n]*</noinclude>")
    for label in LABELS
)
_PLAIN_NOINCLUDE = re.compile(r"<noinclude>([^<>]*)</noinclude>")


def marker_shape(raw):
    """Bounded structural evidence only; never include text or excerpts."""
    def classes(value):
        return {"characters": len(value), "space": value.count(" "),
                "tab": value.count("\t"), "lf": value.count("\n"),
                "cr": value.count("\r"), "semicolon": value.count(";"),
                "other": sum(c not in " \t\r\n;" for c in value)}

    blocks = _PLAIN_NOINCLUDE.findall(raw)
    result = {"page_sequence": 107, "revision_id": PINS[107],
              "exact_open_count": raw.count("<noinclude>"),
              "exact_close_count": raw.count("</noinclude>"),
              "plain_block_count": len(blocks),
              "label_counts": markers(raw), "labels": []}
    for label, pattern in zip(LABELS, _MARKER_PATTERNS):
        containing = [b for b in blocks if label in b]
        row = {"exact_block_matches": len(list(pattern.finditer(raw))),
               "plain_blocks_containing_label": len(containing)}
        if len(containing) == 1 and containing[0].count(label) == 1:
            prefix, suffix = containing[0].split(label)
            row.update(prefix=classes(prefix), suffix=classes(suffix))
        result["labels"].append(row)
    return result


def partition(raw):
    matches = [list(pattern.finditer(raw)) for pattern in _MARKER_PATTERNS]
    if markers(raw) != [1, 1] or any(len(group) != 1 for group in matches):
        raise ValueError("missing-folio marker shape drift: "
                         + json.dumps(marker_shape(raw), sort_keys=True))
    first, second = (group[0] for group in matches)
    if first.end() > second.start():
        raise ValueError("missing-folio marker order drift")
    before = raw[:first.start()]
    middle = raw[first.end():second.start()]
    after = raw[second.end():]
    if transclusion_input(before + "X") != "X":
        raise ValueError("unexpected narrative before first marker")
    tail = transclusion_input(after)
    if not middle.strip() or _UNRENDERED_MARKUP.search(middle):
        raise ValueError("unexpected middle markup")
    if not tail.strip() or _UNRENDERED_MARKUP.search(tail):
        raise ValueError("unexpected tail markup")
    if normalized(middle)[-1].isspace() or not middle[-1].isspace():
        raise ValueError("missing preserved separator at second marker")
    if normalized(tail)[0].isupper() or tail[0].isspace():
        raise ValueError("unexpected second marker continuation")
    # Never derive a new body by global string replacement.
    if transclusion_input(raw) != middle + tail:
        raise ValueError("noinclude removal changed narrative bytes")
    return middle, tail


def occurrences(text, passage):
    if not passage:
        raise ValueError("empty witness")
    # Count overlapping matches too; a repeated passage cannot qualify.
    start = count = 0
    while (pos := text.find(passage, start)) != -1:
        count += 1
        start = pos + 1
    return count


def paragraph_intersections(rendered, spans, middle):
    """Intersect a unique literal slice with actual visible HTML paragraph spans."""
    if spans is None:
        return {"status": "NOT_RUN"}, []
    window = normalized(rendered)
    passage = normalized(middle)
    if occurrences(window, passage) != 1:
        return {"status": "SLICE_NOT_UNIQUE"}, []
    start = window.index(passage)
    end = start + len(passage)
    pieces, partials = [], []
    previous_end = 0
    for a, b in spans:
        if not previous_end <= a <= b <= len(rendered):
            raise ValueError("invalid rendered paragraph spans")
        previous_end = b
        paragraph = normalized(rendered[a:b])
        if not paragraph:
            continue
        prefix = normalized(rendered[:a])
        # PageView inserts block separators; verify the offset rather than
        # finding repeated paragraph text elsewhere in the carrier.
        p_start = len(prefix) + bool(prefix)
        p_end = p_start + len(paragraph)
        if window[p_start:p_end] != paragraph:
            raise ValueError("rendered paragraph offset drift")
        lo, hi = max(start, p_start), min(end, p_end)
        if lo < hi:
            piece = window[lo:hi]
            if piece.strip():
                pieces.append(piece)
                partials.append((lo > p_start, hi < p_end))
    covered = normalized(" ".join(pieces)) == passage
    return {
        "status": "COVERED" if covered else "INCOMPLETE_PARAGRAPH_COVERAGE",
        "intersected_count": len(pieces),
        "complete_count": sum(not a and not b for a, b in partials),
        "leading_partial": bool(partials and partials[0][0]),
        "trailing_partial": bool(partials and partials[-1][1]),
        "intersection_characters": [len(p) for p in pieces],
    }, pieces


def edge_candidates(left, right, rendered):
    # A physical page edge can bisect a word. Test both literal joins against
    # the current carrier, never infer historical whitespace from the winner.
    variants = {"DIRECT": left + right, "SPACE": left + " " + right}
    counts = {key: occurrences(rendered, needle) for key, needle in variants.items()}
    winners = [key for key, count in counts.items() if count == 1]
    selected = (winners[0] if len(winners) == 1 and sum(counts.values()) == 1
                else None)
    return {"matches": counts, "selected": selected}, variants.get(selected)


def compare(raw, scoped, projected, left, right, rendered, *, paragraph_spans=None):
    middle, tail = partition(raw)
    if scoped != middle + tail or projected != scoped:
        raise ValueError("projection changed pinned plain body")
    paragraphs = [normalized(p) for p in re.split(r"\n[ \t\r]*\n", middle) if p.strip()]
    if not paragraphs:
        raise ValueError("empty missing-folio slice")
    breaks = [m.group().count("\n") for m in re.finditer(r"\n(?:[ \t\r]*\n)*", middle)]
    body = normalized(middle + tail)
    render_window = normalized(rendered)
    html_paragraphs, intersections = paragraph_intersections(rendered, paragraph_spans, middle)
    l = " ".join(normalized(left).split()[-8:])
    r = " ".join(normalized(right).split()[:8])
    l_body = " ".join(body.split()[:8])
    r_body = " ".join(body.split()[-8:])
    left_join, left_needle = edge_candidates(l, l_body, render_window)
    right_join, right_needle = edge_candidates(r_body, r, render_window)
    continuation = " ".join(normalized(middle).split()[-8:] + normalized(tail).split()[:8])
    lanes = {"raw": raw, "transclusion": scoped, "projected": projected,
             "rendered": rendered}
    out = {}
    for name, text in lanes.items():
        window = normalized(text)
        if name in ("transclusion", "projected"):
            # Use the explicitly observed current-render join, not a guessed
            # universal separator. Unknown joins stay unknown in all lanes.
            sep_l = "" if left_join["selected"] == "DIRECT" else " "
            sep_r = "" if right_join["selected"] == "DIRECT" else " "
            window = normalized(left) + sep_l + window + sep_r + normalized(right)
        out[name] = {
            "marker_counts": markers(text),
            "paragraph_matches": [occurrences(window, p) for p in paragraphs],
            "rendered_intersection_matches": [occurrences(window, p) for p in intersections],
            "whole_page_matches": occurrences(window, body),
            "left_edge_matches": occurrences(window, left_needle) if name != "raw" and left_needle else None,
            "right_edge_matches": occurrences(window, right_needle) if name != "raw" and right_needle else None,
            "second_marker_continuation_matches": occurrences(window, continuation),
        }
    return {"lanes": out, "raw_blank_line_pieces": len(paragraphs),
            "raw_lf_break_runs": breaks,
            "rendered_paragraphs": html_paragraphs,
            "current_render_edge_joins": {"left": left_join, "right": right_join},
            "middle_characters_including_spaces": len(middle),
            "middle_sha256": digest(middle),
            "projected_body_sha256": digest(projected),
            "scope_projection_byte_equal": True,
            "marker_shape": marker_shape(raw)}


class CarrierView(PageView):
    def __init__(self):
        super().__init__()
        self._paragraph_start = None
        self._paragraph_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = list(attrs)
        # The volume parser output is not a standalone ProofreadPage.
        for i, (name, value) in enumerate(attrs):
            if name == "class" and "mw-parser-output" in (value or "").split():
                attrs[i] = (name, value + " pagetext")
        super().handle_starttag(tag, attrs)
        if tag == "p" and self.stack[-1][1:] == (True, False):
            if self._paragraph_start is not None:
                raise ValueError("nested rendered paragraph")
            self._paragraph_start = len(self.parts)

    def handle_endtag(self, tag):
        if (tag == "p" and self.stack and
                self.stack[-1] == ("p", True, False)):
            if self._paragraph_start is None:
                raise ValueError("unopened rendered paragraph")
            self._paragraph_parts.append((self._paragraph_start, len(self.parts)))
            self._paragraph_start = None
        super().handle_endtag(tag)

    def paragraph_spans(self):
        if self._paragraph_start is not None:
            raise ValueError("unclosed rendered paragraph")
        offsets = [0]
        for part in self.parts:
            offsets.append(offsets[-1] + len(part))
        return [(offsets[a], offsets[b]) for a, b in self._paragraph_parts]


def capture(graph, preflight, projection, *, query=_api_query):
    selected = [p for p in graph["pages"] if p["page_sequence"] in PINS]
    if {p["page_sequence"]: p["revision_id"] for p in selected} != PINS or len(selected) != 3:
        raise ValueError("missing-folio Page pins drift")
    if (projection["source_page_graph_sha256"] != preflight["source_page_graph_sha256"]
            or projection["transclusion_input_candidate_sha256"] !=
            preflight["transclusion_input_candidate_sha256"]):
        raise ValueError("projection/preflight identity drift")
    expected = {p["revision_id"]: p for p in selected}
    prior = {p["page_sequence"]: p for p in preflight["pages"]}
    projected_prior = {p["page_sequence"]: p for p in projection["pages"]}
    rows = query({"action": "query", "prop": "revisions",
                  "revids": "|".join(map(str, expected)),
                  "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"}).get("query", {}).get("pages")
    if not isinstance(rows, list) or len(rows) != 3:
        raise ValueError("missing-folio response incomplete")
    sources, identities = {}, []
    for page in rows:
        revs = page.get("revisions")
        if not isinstance(revs, list) or len(revs) != 1:
            raise ValueError("unexpected revision count")
        rev = revs[0]
        pin = expected.get(rev.get("revid"))
        if pin is None or pin["page_sequence"] in sources or (
                page.get("pageid"), page.get("title"), rev.get("timestamp"), rev.get("sha1")
        ) != (pin["page_id"], pin["title"], pin["timestamp_utc"], pin["mediawiki_sha1"]):
            raise ValueError("missing-folio Page identity drift")
        n = pin["page_sequence"]
        slot = rev.get("slots", {}).get("main", {})
        raw = slot.get("content")
        if (not isinstance(raw, str) or not raw.strip() or len(raw.encode("utf-8")) > 200_000
                or slot.get("contentmodel", "wikitext") not in ("wikitext", "proofread-page")):
            raise ValueError("invalid Page source")
        scoped = transclusion_input(raw)
        old = prior[n]
        if (old["revision_id"], old["wikitext_sha256"], old["wikitext_utf8_bytes"],
                old["transclusion_input_sha256"], old["transclusion_input_characters_including_spaces"]
        ) != (pin["revision_id"], digest(raw), len(raw.encode("utf-8")), digest(scoped), len(scoped)):
            raise ValueError("missing-folio preflight byte drift")
        projected, _, _, unresolved, residual = project_page(scoped)
        known = projected_prior[n]
        if (unresolved or residual or _UNRENDERED_MARKUP.search(projected)
                or (known["revision_id"], known["source_mediawiki_sha1"],
                    known["projected_wikitext_sha256"], known["projected_wikitext_characters_including_spaces"])
                != (pin["revision_id"], pin["mediawiki_sha1"], digest(projected), len(projected))):
            raise ValueError("missing-folio projection drift")
        sources[n] = raw, scoped, projected
        identities.append({"page_sequence": n, "revision_id": pin["revision_id"],
                           "raw_sha256": digest(raw), "projected_sha256": digest(projected)})
    carrier = graph["carrier"]
    if carrier["revision_id"] != 5041937:
        raise ValueError("carrier revision drift")
    parsed = query({"action": "parse", "oldid": "5041937",
                    "prop": "text|revid", "disableeditsection": "1"}).get("parse", {})
    if (parsed.get("revid"), parsed.get("pageid"), parsed.get("title")) != (
            carrier["revision_id"], carrier["page_id"], carrier["title"]):
        raise ValueError("rendered carrier identity drift")
    html = parsed.get("text")
    if not isinstance(html, str) or len(html.encode("utf-8")) > 3_000_000:
        raise ValueError("invalid carrier HTML")
    view = CarrierView()
    view.feed(html)
    view.close()
    if view.bad or view.stack or view.errors or view.containers != 1:
        raise ValueError("unverified rendered carrier structure")
    evidence = compare(*sources[107], sources[106][2], sources[108][2],
                       "".join(view.parts), paragraph_spans=view.paragraph_spans())
    return {"schema_version": "scriptorium-trusov-missing-folios-v2",
            "source_page_graph_sha256": preflight["source_page_graph_sha256"],
            "pages": sorted(identities, key=lambda p: p["page_sequence"]),
            "carrier_revision_id": 5041937, "carrier_html_sha256": digest(html),
            **evidence, "physical_scan_collation": "NOT_VERIFIED",
            "historical_render_equivalence_proven": False, "full_literary_body": "NOT_VERIFIED",
            "source_text_committed": False, "corpus_admitted": False,
            "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("graph", "receipt", "preflight", "preflight-receipt", "projection", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    graph = verify_frozen_graph(args.graph, args.receipt)
    preflight = verify_receipt(args.preflight, args.preflight_receipt, graph)
    from hashlib import sha256
    if sha256(args.graph.read_bytes()).hexdigest() != preflight["source_page_graph_sha256"]:
        raise ValueError("graph digest drift")
    report = capture(graph, preflight, json.loads(args.projection.read_text(encoding="utf-8")))
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
