"""Exact pinned opening-seam scope diagnostic; never a historical renderer."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata

from .robinson_trusov_content import transclusion_input, verify_receipt
from .robinson_trusov_pages import verify_frozen_graph
from .single_page_revision import _api_query

SCHEMA = "scriptorium-trusov-opening-seam-v1"
# Only the initial structural noinclude block followed by a separate
# plain continuation is eligible. Do not search arbitrary excluded notes.
PREFIX = re.compile(
    r"\A\s*<noinclude>(?:(?!</?noinclude\b).)*</noinclude>"
    r"\s*<noinclude>([^<>{}\[\]\r\n]+)</noinclude>", re.S | re.I
)


def digest(text):
    return sha256(text.encode("utf-8")).hexdigest()


def diagnose(first, second):
    """Return counts and booleans, never the continuation or its digest."""
    left, right = transclusion_input(first), transclusion_input(second)
    match = PREFIX.match(second)
    result = {"classification": "NO_ELIGIBLE_LEADING_SPAN",
              "excluded_letters": None, "excluded_punctuation": None,
              "left_suffix_matches": None, "right_prefix_repeats": None}
    if match is None:
        return result
    token = match.group(1).strip()
    if not token or len(token) > 32 or any(
            unicodedata.category(c)[0] not in "LP" for c in token):
        return result
    letters = sum(c.isalpha() for c in token)
    punctuation = sum(unicodedata.category(c).startswith("P") for c in token)
    suffix = left.rstrip().endswith(token)
    repeats = right.lstrip().startswith(token)
    result.update(excluded_letters=letters, excluded_punctuation=punctuation,
                  left_suffix_matches=suffix, right_prefix_repeats=repeats)
    result["classification"] = (
        "PAGE_BOUNDARY_CONTINUATION_NOINCLUDE"
        if letters and suffix and not repeats else "SCOPE_HYPOTHESIS_REFUSED"
    )
    return result



def opening_layout(candidate):
    """Partition only the observed six-call opening prefix; never render it.

    Scope candidate based on the printed title/narrative boundary. Counts only;
    do not treat historical redirect bytes or complete body as verified.
    """
    prefix = re.match(
        r"\A\s*\{\{\^\}\}\s*"
        + "".join(r"\{\{heading\|" + size + r"\|([^{}|\r\n]+)\}\}\s*"
                  for size in ("36", "36", "36", "38"))
        + r"\{\{\^\}\}", candidate
    )
    if prefix is None or any(
            not title.strip() or not all(ch.isupper() or ch.isspace()
                                        for ch in title)
            for title in prefix.groups()):
        raise ValueError("opening title layout differs from observed scope")
    raw_body = candidate[prefix.end():]
    body = raw_body.strip()
    if not body or any(ch in body for ch in "{}<>[]") or "''" in body:
        raise ValueError("opening narrative candidate has unresolved markup")
    return {
        "classification": "TITLE_PREFIX_PARTITION_CANDIDATE",
        "spacing_calls": 2, "heading_calls": 4,
        "title_nonspace_characters": sum(not ch.isspace()
                                         for title in prefix.groups() for ch in title),
        "layout_prefix_characters": prefix.end(),
        "body_candidate_characters_including_spaces": len(body),
        "body_candidate_nonspace_characters": sum(not ch.isspace() for ch in body),
        "body_edge_whitespace_characters": len(raw_body) - len(body),
        "input_characters_including_spaces": len(candidate),
    }


def spacing_target_observation(*, query=_api_query):
    """Compare exact target revisions, not the overwritten 2023 redirect.

    Move history: ^ -> Dhr 2023-07-23; Dhr -> ^ 2024-10-03.
    The old redirect was overwritten. Only target bytes can be verified here.
    """
    pins = {4937800: "2023-07-23T15:49:", 5183352: "2024-10-03T16:40:"}
    response = query({"action": "query", "prop": "revisions",
                      "revids": "4937800|5183352",
                      "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
    pages = response.get("query", {}).get("pages")
    if not isinstance(pages, list) or len(pages) != 1:
        raise ValueError("spacing target history response incomplete")
    page = pages[0]
    if (page.get("title") != "Шаблон:^" or type(page.get("pageid")) is not int
            or page["pageid"] <= 0):
        raise ValueError("spacing target title or page identity drift")
    revisions = page.get("revisions")
    if not isinstance(revisions, list) or len(revisions) != 2:
        raise ValueError("spacing target revision coverage incomplete")
    records, texts = {}, {}
    for rev in revisions:
        rid = rev.get("revid")
        if (rid not in pins or rid in records
                or not str(rev.get("timestamp", "")).startswith(pins[rid])
                or not re.fullmatch(r"[a-z0-9]{31,40}", str(rev.get("sha1", "")))):
            raise ValueError("spacing target revision identity drift")
        main = rev.get("slots", {}).get("main", {})
        raw = main.get("content")
        if (not isinstance(raw, str) or not raw or len(raw.encode("utf-8")) > 4096
                or main.get("contentmodel", "wikitext") != "wikitext"):
            raise ValueError("invalid spacing target bytes")
        scoped = transclusion_input(raw).strip()
        # Strict known zero-argument surface; no recursive renderer or CSS inference.
        if scoped != "<div style=margin-top:{{#if:{{{1|}}}|{{{1}}}|2em}}></div>":
            raise ValueError("spacing target transclusion surface differs")
        texts[rid] = raw
        records[rid] = {"revision_id": rid, "timestamp_utc": rev["timestamp"],
                        "mediawiki_sha1": rev["sha1"], "wikitext_sha256": digest(raw),
                        "wikitext_utf8_bytes": len(raw.encode("utf-8"))}
    if texts[4937800] != texts[5183352]:
        raise ValueError("spacing target revision bytes differ")
    return {
        "page_id": page["pageid"], "current_title": page["title"],
        "target_revisions": [records[rid] for rid in pins],
        "target_bytes_equal": True, "zero_argument_surface": "EMPTY_VISUAL_DIV_2EM",
        "historical_redirect_bytes": "NOT_VERIFIED",
        "historical_render_equivalence_proven": False,
    }


def capture(graph, preflight, *, query=_api_query, layout_output=None, body_observer=None):
    """One additional two-oldid request; compare raw and candidate bytes to
    the previously verified preflight before inspecting a literal seam.
    """
    selected = [p for p in graph["pages"] if p["page_sequence"] in (2, 3)]
    prior = {p["page_sequence"]: p for p in preflight["pages"]}
    if [p["page_sequence"] for p in selected] != [2, 3]:
        raise ValueError("opening Page graph incomplete")
    expected = {p["revision_id"]: p for p in selected}
    response = query({"action": "query", "prop": "revisions",
                      "revids": "|".join(map(str, expected)),
                      "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
    rows = response.get("query", {}).get("pages")
    if not isinstance(rows, list) or len(rows) != 2:
        raise ValueError("opening Page response incomplete")
    texts, identities = {}, []
    for page in rows:
        revs = page.get("revisions")
        if not isinstance(revs, list) or len(revs) != 1:
            raise ValueError("ambiguous opening Page revision")
        rev = revs[0]
        pin = expected.get(rev.get("revid"))
        if pin is None or pin["page_sequence"] in texts or (
                page.get("pageid"), page.get("title"), rev.get("timestamp"), rev.get("sha1")
        ) != (pin["page_id"], pin["title"], pin["timestamp_utc"], pin["mediawiki_sha1"]):
            raise ValueError("opening Page identity drift")
        n = pin["page_sequence"]
        main = rev.get("slots", {}).get("main", {})
        raw = main.get("content")
        if not isinstance(raw, str) or len(raw.encode("utf-8")) > 200_000:
            raise ValueError("invalid opening Page bytes")
        candidate = transclusion_input(raw)
        old = prior[n]
        if (old["revision_id"], old["wikitext_sha256"], old["wikitext_utf8_bytes"],
                old["transclusion_input_sha256"],
                old["transclusion_input_characters_including_spaces"]) != (
                pin["revision_id"], digest(raw), len(raw.encode("utf-8")),
                digest(candidate), len(candidate)):
            raise ValueError("opening Page preflight byte drift")
        texts[n] = raw
        identities.append({"page_sequence": n, "revision_id": pin["revision_id"],
                           "source_mediawiki_sha1": pin["mediawiki_sha1"],
                           "wikitext_sha256": digest(raw),
                           "transclusion_input_sha256": digest(candidate)})
    if body_observer is not None and layout_output is None:
        raise ValueError("opening body observation requires layout proof")
    if layout_output is not None:
        page = next(p for p in identities if p["page_sequence"] == 2)
        layout_output.update({
            "schema_version": "scriptorium-trusov-opening-layout-v1",
            "source_page_graph_sha256": preflight["source_page_graph_sha256"],
            "page": page,
            "layout": opening_layout(transclusion_input(texts[2])),
            "spacing_target": spacing_target_observation(query=query),
            "full_literary_body": "NOT_VERIFIED", "corpus_admitted": False,
            "historical_render_equivalence_proven": False,
            "source_text_committed": False, "m2_parity_admissible": False,
        })
    if body_observer is not None:
        seam = diagnose(texts[2], texts[3])
        if (seam != {"classification": "PAGE_BOUNDARY_CONTINUATION_NOINCLUDE",
                     "excluded_letters": 4, "excluded_punctuation": 1,
                     "left_suffix_matches": True, "right_prefix_repeats": False}
                or [p["revision_id"] for p in selected] != [4958669, 4958680]):
            raise ValueError("opening body seam proof differs")
        layout = layout_output["layout"]
        body = transclusion_input(texts[2])[layout["layout_prefix_characters"]:].strip()
        if len(body) != layout["body_candidate_characters_including_spaces"]:
            raise ValueError("opening body partition drift")
        body_observer(2, body)
    return {"schema_version": SCHEMA,
            "source_page_graph_sha256": preflight["source_page_graph_sha256"],
            "pages": sorted(identities, key=lambda p: p["page_sequence"]),
            "seam": diagnose(texts[2], texts[3]),
            "historical_render_equivalence_proven": False,
            "full_literary_body": "NOT_VERIFIED", "source_text_committed": False,
            "corpus_admitted": False, "m2_parity_admissible": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("graph", "receipt", "preflight", "preflight-receipt", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--layout-output", type=Path)
    args = parser.parse_args()
    inputs = {p.resolve() for p in (args.graph, args.receipt, args.preflight, args.preflight_receipt)}
    outputs = [args.output] + ([args.layout_output] if args.layout_output else [])
    if (len({p.resolve() for p in outputs}) != len(outputs)
            or any(p.exists() or p.resolve() in inputs for p in outputs)):
        parser.error("outputs must be new and distinct")
    graph = verify_frozen_graph(args.graph, args.receipt)
    preflight = verify_receipt(args.preflight, args.preflight_receipt, graph)
    if sha256(args.graph.read_bytes()).hexdigest() != preflight["source_page_graph_sha256"]:
        raise ValueError("opening Page graph digest drift")
    layout = {} if args.layout_output else None
    report = capture(graph, preflight, layout_output=layout)
    if args.layout_output:
        with args.layout_output.open("x", encoding="utf-8") as out:
            json.dump(layout, out, ensure_ascii=False, sort_keys=True, indent=2)
            out.write("\n")
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")
    print("Opening seam:", report["seam"], "; full body NOT_VERIFIED")


if __name__ == "__main__":
    main()
