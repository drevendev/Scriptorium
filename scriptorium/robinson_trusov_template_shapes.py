"""Audit unresolved Trusov template invocations from pinned Pages, without prose.

Shares the exact oldid/identity verifier used for the accepted preflight.  Only
template titles passing a strict metadata allow-list, cryptographic digests and
parameter *shapes* leave process memory. This is not MediaWiki expansion or a
literary-text measurement.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .mediawiki_template_invocation import (
    _matching_brace_end, _split_top_level, _top_level_equals,
)
from .robinson_trusov_content import capture
from .robinson_trusov_pages import verify_frozen_graph
from .single_page_revision import _api_query

SCHEMA = "scriptorium-trusov-template-shapes-v1"
OPEN = re.compile(r"(?<!\{)\{\{(?!\{)")
# A template title is navigation metadata, not a passage of source text.
SAFE_TITLE = re.compile(r"[A-Za-zА-Яа-яЁё][A-Za-zА-Яа-яЁё0-9 _./-]{0,63}\Z")
HEX = re.compile(r"[a-f0-9]{64}\Z")


def invocation_shapes(candidate: str) -> tuple[list[dict], int]:
    """Record balanced brace-call identities, NEVER argument values or prose."""
    if not isinstance(candidate, str):
        raise TypeError("Page input must be text")
    calls = []
    for match in OPEN.finditer(candidate):
        start = match.start()
        end = _matching_brace_end(candidate, start)
        literal = candidate[start:end]
        fields = _split_top_level(literal[2:-2], "|")
        title = fields[0].strip()
        args = fields[1:]
        safe = bool(SAFE_TITLE.fullmatch(title))
        named = sum(_top_level_equals(a) is not None for a in args)
        calls.append({
            "invocation_sha256": sha256(literal.encode("utf-8")).hexdigest(),
            "template_title": title if safe else None,
            "title_sha256": sha256(title.encode("utf-8")).hexdigest(),
            "classification": "literal_template" if safe else (
                "parser_or_dynamic_template"),
            "argument_count": len(args),
            "named_argument_count": named,
            "anonymous_argument_count": len(args) - named,
            "nested_brace_groups": literal.count("{{") - 1,
        })
    # Triple-brace placeholders or unsupported openers remain explicitly unresolved.
    residual = candidate.count("{{") - len(calls)
    if residual < 0:
        raise ValueError("template opener inventory overflow")
    return calls, residual


def validate_shapes(report: Mapping[str, object], graph: Mapping[str, object],
                    preflight: Mapping[str, object]) -> None:
    """Reject claimed body readiness, altered page identities or source prose."""
    expected = {"schema_version", "candidate_id", "page_count", "page_graph_sha256",
                "transclusion_input_candidate_sha256", "pages", "total_invocations",
                "unclassified_openers", "pages_with_invocations", "source_text_committed",
                "literary_body_sha256", "corpus_threshold_verified",
                "historical_render_equivalence_proven", "fantlab_input_identity",
                "m2_parity_admissible", "status"}
    if set(report) != expected or report["schema_version"] != SCHEMA:
        raise ValueError("unexpected shape inventory fields or source prose")
    if report["candidate_id"] != graph["candidate_id"] or report["page_count"] != len(graph["pages"]):
        raise ValueError("incomplete template inventory")
    if report["page_graph_sha256"] != preflight["source_page_graph_sha256"]:
        raise ValueError("source graph changed")
    if report["transclusion_input_candidate_sha256"] != preflight["transclusion_input_candidate_sha256"]:
        raise ValueError("transclusion candidate changed")
    for k, v in {"source_text_committed": False, "literary_body_sha256": None,
                 "corpus_threshold_verified": False,
                 "historical_render_equivalence_proven": False,
                 "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False,
                 "status": "UNRESOLVED_TEMPLATE_SHAPES_ONLY"}.items():
        if report[k] != v:
            raise ValueError("false scientific claim")
    pages = report["pages"]
    if not isinstance(pages, list) or len(pages) != len(graph["pages"]):
        raise ValueError("incomplete historical Page inventory")
    total = residuals = with_calls = 0
    for row, frozen, earlier in zip(pages, graph["pages"], preflight["pages"]):
        if set(row) != {"page_sequence", "revision_id", "invocations", "unclassified_openers"}:
            raise ValueError("unexpected Page shape fields")
        if (row["page_sequence"], row["revision_id"]) != (
                frozen["page_sequence"], frozen["revision_id"]):
            raise ValueError("historical Page order or oldid drift")
        calls = row["invocations"]
        residual = row["unclassified_openers"]
        if not isinstance(calls, list) or type(residual) is not int or residual < 0:
            raise ValueError("invalid invocation totals")
        if len(calls) + residual != earlier["template_openers"]:
            raise ValueError("preflight template counts differ")
        for call in calls:
            if set(call) != {"invocation_sha256", "template_title", "title_sha256",
                             "classification", "argument_count", "named_argument_count",
                             "anonymous_argument_count", "nested_brace_groups"}:
                raise ValueError("source prose or unknown invocation shape")
            if not HEX.fullmatch(str(call["invocation_sha256"])) or not HEX.fullmatch(str(call["title_sha256"])):
                raise ValueError("invalid source-free digest")
            name = call["template_title"]
            if name is not None and (not isinstance(name, str) or not SAFE_TITLE.fullmatch(name)
                    or sha256(name.encode("utf-8")).hexdigest() != call["title_sha256"]):
                raise ValueError("unsafe template title")
            if call["classification"] != ("literal_template" if name is not None else "parser_or_dynamic_template"):
                raise ValueError("incorrect template class")
            a, b, c = (call[k] for k in ("argument_count", "named_argument_count", "anonymous_argument_count"))
            if not all(type(v) is int and v >= 0 for v in (a,b,c,call["nested_brace_groups"])) or a != b+c:
                raise ValueError("invalid argument shape")
        total += len(calls)
        residuals += residual
        with_calls += bool(calls or residual)
    if (report["total_invocations"], report["unclassified_openers"],
            report["pages_with_invocations"]) != (total, residuals, with_calls):
        raise ValueError("aggregate shape inventory mismatch")


def capture_shapes(graph: Mapping[str, object], graph_sha256: str,
                   *, query: Callable[..., dict] = _api_query,
                   delay: float = 0.75,
                   preflight_output: dict | None = None) -> dict:
    """One historical source fetch; preserve accepted preflight and output shapes."""
    pages: list[dict] = []
    def observe(identity: dict, candidate: str) -> None:
        calls, residual = invocation_shapes(candidate)
        pages.append({"page_sequence": identity["page_sequence"],
                      "revision_id": identity["revision_id"],
                      "invocations": calls, "unclassified_openers": residual})
    preflight = capture(graph, graph_sha256=graph_sha256, query=query,
                        delay=delay, observer=observe)
    result = {
        "schema_version": SCHEMA, "candidate_id": graph["candidate_id"],
        "page_count": len(pages), "page_graph_sha256": graph_sha256,
        "transclusion_input_candidate_sha256":
            preflight["transclusion_input_candidate_sha256"],
        "pages": pages,
        "total_invocations": sum(len(p["invocations"]) for p in pages),
        "unclassified_openers": sum(p["unclassified_openers"] for p in pages),
        "pages_with_invocations": sum(bool(p["invocations"] or p["unclassified_openers"])
                                      for p in pages),
        "source_text_committed": False, "literary_body_sha256": None,
        "corpus_threshold_verified": False,
        "historical_render_equivalence_proven": False,
        "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False,
        "status": "UNRESOLVED_TEMPLATE_SHAPES_ONLY",
    }
    validate_shapes(result, graph, preflight)
    if preflight_output is not None:
        preflight_output.update(preflight)
    return result



def verify_observation(report: Mapping[str, object], summary: Mapping[str, object]) -> None:
    """Bind a retained source-free class histogram to exact live JSON bytes."""
    expected_keys = {
        "schema_version", "candidate_id", "source_page_graph_sha256",
        "transclusion_input_candidate_sha256", "full_source_free_report_sha256",
        "full_source_free_report_bytes", "primary_workflow_run",
        "primary_workflow_head_sha", "page_count", "pages_with_invocations",
        "total_invocations", "unclassified_openers", "literal_template_counts",
        "parser_or_dynamic_template_count", "source_text_committed",
        "literary_body_sha256", "corpus_threshold_verified",
        "historical_render_equivalence_proven", "fantlab_input_identity",
        "m2_parity_admissible", "status",
    }
    if set(summary) != expected_keys or summary["schema_version"] != (
            "scriptorium-trusov-template-shape-observation-v1"):
        raise ValueError("unrecognized Trusov template observation")
    encoded = (json.dumps(report, sort_keys=True, indent=2,
                          ensure_ascii=False) + "\n").encode("utf-8")
    if (summary["full_source_free_report_sha256"] != sha256(encoded).hexdigest()
            or summary["full_source_free_report_bytes"] != len(encoded)):
        raise ValueError("template report byte digest drift")
    from collections import Counter
    observed = Counter(
        call["template_title"]
        for row in report["pages"]
        for call in row["invocations"]
    )
    if (summary["literal_template_counts"] != {
            name: count for name, count in observed.items() if name is not None
        } or summary["parser_or_dynamic_template_count"] != observed[None]):
        raise ValueError("template title classification drift")
    if summary["source_page_graph_sha256"] != report["page_graph_sha256"]:
        raise ValueError("template source graph digest mismatch")
    for key in ("candidate_id", "page_count",
                "transclusion_input_candidate_sha256", "pages_with_invocations",
                "total_invocations", "unclassified_openers",
                "source_text_committed", "literary_body_sha256",
                "corpus_threshold_verified",
                "historical_render_equivalence_proven", "fantlab_input_identity",
                "m2_parity_admissible", "status"):
        if summary[key] != report[key]:
            raise ValueError(f"template observation mismatch: {key}")
    if (summary["primary_workflow_run"] !=
            "https://github.com/drevendev/Scriptorium/actions/runs/41402787490"
        or summary["primary_workflow_head_sha"] !=
            "f91fd2dfe011f6dce171bac099d89b758fd7a5f9"):
        raise ValueError("unverified primary template-shape capture provenance")

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Source-free pinned Trusov Page template inventory")
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--preflight-output", type=Path)
    parser.add_argument("--delay", type=float, default=0.75)
    args = parser.parse_args(argv)
    outputs = [args.output] + ([args.preflight_output] if args.preflight_output else [])
    if len({x.resolve() for x in outputs}) != len(outputs) or any(
            x.exists() or x.resolve() in (args.graph.resolve(), args.receipt.resolve())
            for x in outputs):
        parser.error("output exists or would overwrite frozen evidence")
    graph = verify_frozen_graph(args.graph, args.receipt)
    preflight: dict = {}
    report = capture_shapes(graph, sha256(args.graph.read_bytes()).hexdigest(),
                            delay=args.delay, preflight_output=preflight)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2, ensure_ascii=False)
        stream.write("\n")
    if args.preflight_output:
        args.preflight_output.parent.mkdir(parents=True, exist_ok=True)
        with args.preflight_output.open("x", encoding="utf-8") as stream:
            json.dump(preflight, stream, sort_keys=True, indent=2, ensure_ascii=False)
            stream.write("\n")
    print(f"Audited {report['page_count']} pinned Pages, "
          f"{report['total_invocations']} unresolved invocations; literary body NOT_RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
