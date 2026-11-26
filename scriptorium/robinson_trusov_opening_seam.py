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


def capture(graph, preflight, *, query=_api_query):
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
    args = parser.parse_args()
    if args.output.exists() or args.output.resolve() in {
            p.resolve() for p in (args.graph, args.receipt, args.preflight, args.preflight_receipt)}:
        parser.error("output must be new and distinct")
    graph = verify_frozen_graph(args.graph, args.receipt)
    preflight = verify_receipt(args.preflight, args.preflight_receipt, graph)
    if sha256(args.graph.read_bytes()).hexdigest() != preflight["source_page_graph_sha256"]:
        raise ValueError("opening Page graph digest drift")
    report = capture(graph, preflight)
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")
    print("Opening seam:", report["seam"], "; full body NOT_VERIFIED")


if __name__ == "__main__":
    main()
