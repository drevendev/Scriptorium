"""Conservative source-free Trusov standalone-template projection experiment.

This is NOT a literary-body extractor: most MediaWiki rendering, Page joining,
variant selection, and historical parser identity remain unknown. The projected
wikitext stays transient and only digests/counts are eligible for publication.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .robinson_trusov_pages import verify_frozen_graph
from .robinson_trusov_template_shapes import capture_shapes, invocation_shapes, validate_shapes
from .single_page_revision import _api_query

SCHEMA = "scriptorium-trusov-standalone-projection-v1"
HEX = re.compile(r"[a-f0-9]{64}\Z")
STYLE = re.compile(r"[A-Za-z0-9.% -]{1,20}\Z")


class ProjectedPageJoin:
    """Streaming identity for a synthetic-LF Page join, never a literary body.

    No Page text leaves transient process memory. The alphabetic-edge counter
    signals seams that *may* need historical ProofreadPage hyphenation rules;
    it does not attempt word restoration or normalize manuscript spelling.
    """

    PROFILE = "one_LF_between_projected_Page_inputs_diagnostic_only"

    def __init__(self) -> None:
        self._digest = sha256()
        self._pages = 0
        self._characters = 0
        self._alphabetic_edges = 0
        self._previous_last: str | None = None

    def add(self, page: str) -> None:
        if not isinstance(page, str) or not page:
            raise ValueError("empty or non-text projected Page")
        if self._pages:
            self._digest.update(b"\n")
            self._characters += 1
            if self._previous_last and self._previous_last.isalpha() and page[0].isalpha():
                self._alphabetic_edges += 1
        self._digest.update(page.encode("utf-8"))
        self._characters += len(page)
        self._pages += 1
        self._previous_last = page[-1]

    def source_free_identity(self) -> dict[str, str | int]:
        if not self._pages:
            raise ValueError("no projected Pages to join")
        return {
            "projected_page_join_profile": self.PROFILE,
            "joined_projected_wikitext_sha256": self._digest.hexdigest(),
            "joined_projected_wikitext_characters_including_spaces": self._characters,
            "projected_page_join_seams": self._pages - 1,
            "alphabetic_page_edge_seams": self._alphabetic_edges,
        }


def project_page(candidate: str) -> tuple[str, int, int, int, int]:
    """Only unwrap isolated, literal nop and plain two-field heading lines.

    Do not expand VAR, parser functions, nested or inline templates. This
    projection preserves other wikitext verbatim, including unresolved calls.
    """
    calls, residual = invocation_shapes(candidate)
    out: list[str] = []
    handled_nop = handled_heading = 0
    for line in candidate.splitlines(keepends=True):
        value = line.strip()
        # An entire standalone line must be one flat, exact double-brace call.
        if not (value.startswith("{{") and value.endswith("}}") and
                not value.startswith("{{{") and "{{" not in value[2:] and
                "}}" not in value[:-2]):
            out.append(line)
            continue
        fields = value[2:-2].split("|")
        title = fields[0].strip().casefold()
        ending = "\r\n" if line.endswith("\r\n") else "\n"
        if title == "nop" and len(fields) == 1:
            # A blank line retains a paragraph break at a page boundary.
            out.append(ending)
            handled_nop += 1
        elif (title == "heading" and len(fields) == 3 and
              STYLE.fullmatch(fields[1].strip()) and fields[2].strip() and
              not any(c in fields[2] for c in "<>[]{}") and
              not any(ord(c) < 32 for c in fields[2])):
            # Plain heading label only; CSS and rendering are not reproduced.
            out.append(fields[2].strip() + ending)
            handled_heading += 1
        else:
            out.append(line)
    if handled_nop + handled_heading > len(calls):
        raise ValueError("projection counts exceed source invocation inventory")
    return ("".join(out), handled_nop, handled_heading,
            len(calls) - handled_nop - handled_heading, residual)


def capture_projection(graph: Mapping[str, object], graph_sha256: str, *,
                       query: Callable[..., dict] = _api_query, delay: float = 0.75,
                       preflight_output: dict | None = None,
                       shapes_output: dict | None = None) -> dict:
    """Reuse one exact-identity fetch for original preflight, shapes and probe."""
    pages: list[dict] = []
    joined = ProjectedPageJoin()

    def observe(identity: dict, candidate: str) -> None:
        projected, nop, heading, unresolved, residual = project_page(candidate)
        joined.add(projected)
        pages.append({
            "page_sequence": identity["page_sequence"],
            "revision_id": identity["revision_id"],
            "projected_wikitext_sha256": sha256(projected.encode("utf-8")).hexdigest(),
            "projected_wikitext_characters_including_spaces": len(projected),
            "handled_nop": nop, "handled_heading": heading,
            "unresolved_invocations": unresolved,
            "unclassified_openers": residual,
        })

    preflight: dict = {}
    shapes = capture_shapes(graph, graph_sha256, query=query, delay=delay,
                            preflight_output=preflight, projection_observer=observe)
    result = {
        "schema_version": SCHEMA,
        "candidate_id": graph["candidate_id"],
        "page_count": len(pages),
        "source_page_graph_sha256": graph_sha256,
        "transclusion_input_candidate_sha256": preflight["transclusion_input_candidate_sha256"],
        **joined.source_free_identity(),
        "pages": pages,
        "handled_nop": sum(p["handled_nop"] for p in pages),
        "handled_heading": sum(p["handled_heading"] for p in pages),
        "unresolved_invocations": sum(p["unresolved_invocations"] for p in pages),
        "unclassified_openers": sum(p["unclassified_openers"] for p in pages),
        "source_text_committed": False,
        "literary_body_sha256": None,
        "corpus_threshold_verified": False,
        "historical_render_equivalence_proven": False,
        "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False,
        "status": "PARTIAL_TEMPLATE_PROJECTION_NOT_BODY",
    }
    validate_projection(result, graph, preflight, shapes)
    if preflight_output is not None:
        preflight_output.update(preflight)
    if shapes_output is not None:
        shapes_output.update(shapes)
    return result


def validate_projection(report: Mapping[str, object], graph: Mapping[str, object],
                        preflight: Mapping[str, object], shapes: Mapping[str, object]) -> None:
    """Strict schema prevents evidence inflation or accidentally persisting prose."""
    expected = {"schema_version", "candidate_id", "page_count",
                "source_page_graph_sha256", "transclusion_input_candidate_sha256",
                "projected_page_join_profile", "joined_projected_wikitext_sha256",
                "joined_projected_wikitext_characters_including_spaces",
                "projected_page_join_seams", "alphabetic_page_edge_seams",
                "pages", "handled_nop", "handled_heading", "unresolved_invocations",
                "unclassified_openers", "source_text_committed", "literary_body_sha256",
                "corpus_threshold_verified", "historical_render_equivalence_proven",
                "fantlab_input_identity", "m2_parity_admissible", "status"}
    if set(report) != expected or report["schema_version"] != SCHEMA:
        raise ValueError("invalid projection schema or source text leakage")
    for key, value in {
        "source_text_committed": False, "literary_body_sha256": None,
        "corpus_threshold_verified": False, "historical_render_equivalence_proven": False,
        "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False,
        "status": "PARTIAL_TEMPLATE_PROJECTION_NOT_BODY",
    }.items():
        if report[key] != value:
            raise ValueError("false scientific claim")
    if (report["candidate_id"] != graph["candidate_id"] or
        report["source_page_graph_sha256"] != preflight["source_page_graph_sha256"] or
        report["transclusion_input_candidate_sha256"] != preflight["transclusion_input_candidate_sha256"] or
        report["page_count"] != len(graph["pages"])):
        raise ValueError("frozen source identity mismatch")
    validate_shapes(shapes, graph, preflight)
    if (report["projected_page_join_profile"] != ProjectedPageJoin.PROFILE or
        not HEX.fullmatch(str(report["joined_projected_wikitext_sha256"]))):
        raise ValueError("unrecognized projected Page join identity")
    pages = report["pages"]
    if not isinstance(pages, list) or len(pages) != len(graph["pages"]):
        raise ValueError("incomplete Page projection")
    counters = {k: 0 for k in ("handled_nop", "handled_heading", "unresolved_invocations", "unclassified_openers")}
    for row, identity, shape in zip(pages, graph["pages"], shapes["pages"]):
        if set(row) != {"page_sequence", "revision_id", "projected_wikitext_sha256",
                        "projected_wikitext_characters_including_spaces", *counters}:
            raise ValueError("unrecognized Page projection field / prose leakage")
        if (row["page_sequence"], row["revision_id"]) != (identity["page_sequence"], identity["revision_id"]):
            raise ValueError("Page revision order drift")
        if not HEX.fullmatch(str(row["projected_wikitext_sha256"])):
            raise ValueError("invalid projection digest")
        if type(row["projected_wikitext_characters_including_spaces"]) is not int or row["projected_wikitext_characters_including_spaces"] < 0:
            raise ValueError("invalid projection character count")
        for k in counters:
            if type(row[k]) is not int or row[k] < 0:
                raise ValueError("invalid projection counter")
            counters[k] += row[k]
        if (row["handled_nop"] + row["handled_heading"] + row["unresolved_invocations"] !=
                len(shape["invocations"]) or row["unclassified_openers"] != shape["unclassified_openers"]):
            raise ValueError("projection versus pinned shape count drift")
    expected_join_characters = (
        sum(row["projected_wikitext_characters_including_spaces"] for row in pages)
        + len(pages) - 1
    )
    if (type(report["joined_projected_wikitext_characters_including_spaces"]) is not int or
        report["joined_projected_wikitext_characters_including_spaces"] != expected_join_characters):
        raise ValueError("projected Page join character count mismatch")
    if (type(report["projected_page_join_seams"]) is not int or
        report["projected_page_join_seams"] != len(pages) - 1):
        raise ValueError("projected Page seam count mismatch")
    if (type(report["alphabetic_page_edge_seams"]) is not int or
        not 0 <= report["alphabetic_page_edge_seams"] <= report["projected_page_join_seams"]):
        raise ValueError("invalid alphabetic Page edge counter")
    if any(report[k] != counters[k] for k in counters):
        raise ValueError("projection total mismatch")
    if (report["handled_nop"] > 28 or report["handled_heading"] > 30 or
        report["unresolved_invocations"] + report["handled_nop"] + report["handled_heading"] != shapes["total_invocations"] or
        report["unclassified_openers"] != shapes["unclassified_openers"]):
        raise ValueError("projection exceeds pinned template classes")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Source-free historical Trusov template projection probe")
    parser.add_argument("--graph", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--preflight-output", required=True, type=Path)
    parser.add_argument("--shapes-output", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--delay", type=float, default=0.75)
    args = parser.parse_args(argv)
    outs = (args.output, args.preflight_output, args.shapes_output)
    if len({x.resolve() for x in outs}) != len(outs) or any(
            x.exists() or x.resolve() in (args.graph.resolve(), args.receipt.resolve()) for x in outs):
        parser.error("outputs must be distinct, new, and outside frozen inputs")
    graph = verify_frozen_graph(args.graph, args.receipt)
    preflight, shapes = {}, {}
    report = capture_projection(graph, sha256(args.graph.read_bytes()).hexdigest(),
                                delay=args.delay, preflight_output=preflight, shapes_output=shapes)
    for output, data in ((args.preflight_output, preflight), (args.shapes_output, shapes), (args.output, report)):
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as writer:
            json.dump(data, writer, sort_keys=True, indent=2, ensure_ascii=False)
            writer.write("\n")
    print(f"Pinned Trusov 150-page provisional projection: {report['handled_nop']} nop, "
          f"{report['handled_heading']} plain heading, {report['unresolved_invocations']} "
          f"unresolved; literary body NOT_RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
