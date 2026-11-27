"""Check three scan-derived errata controls against exact Trusov source bytes.

No correction text is stored, logged or applied. Token-window SHA-256 witnesses
are derived from the facing errata on leaf 151, not from an assumed correction
rule. The controls are local editorial diagnostics, not complete print collation.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from .robinson_trusov_content import transclusion_input, verify_receipt
from .robinson_trusov_interior import _UNRENDERED_MARKUP
from .robinson_trusov_pages import verify_frozen_graph
from .robinson_trusov_projection import project_page
from .single_page_revision import _api_query

SCHEMA = "scriptorium-trusov-errata-controls-v1"
PINS = {21: 4958671, 60: 4958715}
# Each witness is (whitespace-delimited token count, SHA-256 of exact tokens
# joined by single ASCII spaces). Case, historical letters and punctuation
# are deliberately significant. Both readings include their printed context.
# Manual scan evidence: issue #511 comment 7217506928, leaf 151 right side.
CONTROLS = (
    ("p38_l17", 21,
     (4, "1c14ec225b7b8f1617847e16cd74ac924361664482d6540f0e8c0e4dbe1eb4b3"),
     (2, "2602a9ea658c2f4f5c5dc7cac73ed55b1c21e2e828a94b99718d3768d74cc715")),
    ("p116_l19", 60,
     (3, "bfd93f9158613a00723f10d853d221b327b6ef5807b0193025b55739d8eab3a4"),
     (3, "a27d0f20e6f8abd9c5b4b29bd4d1d309ffb1ef09316667f2c00f1ae5d3f61c38")),
    ("p116_l20", 60,
     (3, "03e949e92977d633b13dcc16d0e37ed52375f94ee390715d5a86397c860c0cf8"),
     (3, "1fa7ff39ada0993f364871e837f398bd91c9e0f4006c1c008d90b3110f14191d")),
)


def digest(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def classify(text: str, printed: tuple[int, str], corrected: tuple[int, str]) -> dict:
    """Count exact token windows; duplicates or both alternatives are ambiguous."""
    if printed == corrected or any(not 1 <= width <= 8 for width, _ in (printed, corrected)):
        raise ValueError("invalid or indistinguishable errata witnesses")
    tokens = text.split()

    def matches(witness):
        width, expected = witness
        return sum(digest(" ".join(tokens[i:i + width])) == expected
                   for i in range(len(tokens) - width + 1))

    p, c = matches(printed), matches(corrected)
    status = ("PRINTED_READING_PRESENT" if (p, c) == (1, 0)
              else "CORRECTED_READING_PRESENT" if (p, c) == (0, 1)
              else "NEITHER" if (p, c) == (0, 0)
              else "AMBIGUOUS")
    return {"printed_matches": p, "corrected_matches": c, "classification": status}


def capture(graph, preflight, projection, *, query=_api_query):
    selected = [p for p in graph["pages"] if p["page_sequence"] in PINS]
    if len(selected) != 2 or {p["page_sequence"]: p["revision_id"] for p in selected} != PINS:
        raise ValueError("errata Page graph identity drift")
    if (projection["source_page_graph_sha256"] != preflight["source_page_graph_sha256"]
            or projection["transclusion_input_candidate_sha256"] !=
            preflight["transclusion_input_candidate_sha256"]):
        raise ValueError("errata projection/preflight identity drift")
    expected = {p["revision_id"]: p for p in selected}
    prior = {p["page_sequence"]: p for p in preflight["pages"]}
    projected_prior = {p["page_sequence"]: p for p in projection["pages"]}
    payload = query({"action": "query", "prop": "revisions",
                     "revids": "|".join(map(str, expected)),
                     "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
    rows = payload.get("query", {}).get("pages")
    if not isinstance(rows, list) or len(rows) != 2:
        raise ValueError("errata Page response incomplete")
    sources = {}
    identities = []
    for page in rows:
        revisions = page.get("revisions")
        if not isinstance(revisions, list) or len(revisions) != 1:
            raise ValueError("ambiguous errata Page revision")
        rev = revisions[0]
        pin = expected.get(rev.get("revid"))
        if pin is None or pin["page_sequence"] in sources or (
                page.get("pageid"), page.get("title"), rev.get("timestamp"), rev.get("sha1")
        ) != (pin["page_id"], pin["title"], pin["timestamp_utc"], pin["mediawiki_sha1"]):
            raise ValueError("errata Page identity drift")
        n = pin["page_sequence"]
        main = rev.get("slots", {}).get("main", {})
        raw = main.get("content")
        if (not isinstance(raw, str) or not raw.strip() or len(raw.encode("utf-8")) > 200_000
                or main.get("contentmodel", "wikitext") not in ("wikitext", "proofread-page")):
            raise ValueError("invalid errata Page bytes")
        scoped = transclusion_input(raw)
        old = prior[n]
        if (old["revision_id"], old["wikitext_sha256"], old["wikitext_utf8_bytes"],
                old["transclusion_input_sha256"],
                old["transclusion_input_characters_including_spaces"]) != (
                pin["revision_id"], digest(raw), len(raw.encode("utf-8")),
                digest(scoped), len(scoped)):
            raise ValueError("errata Page preflight byte drift")
        projected, _, _, unresolved, residual = project_page(scoped)
        known = projected_prior[n]
        if (unresolved or residual or _UNRENDERED_MARKUP.search(projected)
                or (known["revision_id"], known["source_mediawiki_sha1"],
                    known["projected_wikitext_sha256"],
                    known["projected_wikitext_characters_including_spaces"]) !=
                (pin["revision_id"], pin["mediawiki_sha1"], digest(projected), len(projected))):
            raise ValueError("errata Page projection drift or unresolved markup")
        sources[n] = (raw, projected)
        identities.append({"page_sequence": n, "revision_id": pin["revision_id"],
                           "wikitext_sha256": digest(raw),
                           "projected_wikitext_sha256": digest(projected)})
    results = []
    for name, n, printed, corrected in CONTROLS:
        raw, projected = sources[n]
        results.append({"control": name, "page_sequence": n,
                        "raw": classify(raw, printed, corrected),
                        "projected": classify(projected, printed, corrected)})
    return {"schema_version": SCHEMA,
            "source_page_graph_sha256": preflight["source_page_graph_sha256"],
            "pages": sorted(identities, key=lambda p: p["page_sequence"]),
            "controls": results,
            "all_three_projected_corrected": all(
                x["projected"]["classification"] == "CORRECTED_READING_PRESENT" for x in results),
            "all_three_raw_corrected": all(
                x["raw"]["classification"] == "CORRECTED_READING_PRESENT" for x in results),
            "scan_evidence": "MANUAL_THREE_CONTROLS_ONLY",
            "full_errata_coverage": "UNKNOWN", "full_literary_body": "NOT_VERIFIED",
            "historical_render_equivalence_proven": False, "source_text_committed": False,
            "corpus_admitted": False, "m2_parity_admissible": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("graph", "receipt", "preflight", "preflight-receipt", "projection", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.resolve() in {
            p.resolve() for p in (args.graph, args.receipt, args.preflight,
                                  args.preflight_receipt, args.projection)}:
        parser.error("output must be new and distinct")
    graph = verify_frozen_graph(args.graph, args.receipt)
    preflight = verify_receipt(args.preflight, args.preflight_receipt, graph)
    if sha256(args.graph.read_bytes()).hexdigest() != preflight["source_page_graph_sha256"]:
        raise ValueError("errata Page graph digest drift")
    projection = json.loads(args.projection.read_text(encoding="utf-8"))
    report = capture(graph, preflight, projection)
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")
    print("Errata controls:", report["controls"], "; full errata coverage UNKNOWN")


if __name__ == "__main__":
    main()
