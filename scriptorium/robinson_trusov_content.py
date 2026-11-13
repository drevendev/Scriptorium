"""Inspect frozen Trusov Page revision contents without publishing prose.

This diagnostic captures a transclusion-input candidate, NOT a rendered
literary body: unexpanded templates, links and page joins remain unresolved.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from time import sleep
from typing import Callable, Mapping, Sequence
from .robinson_trusov_pages import WORK_ID, validate, verify_frozen_graph
from .single_page_revision import _api_query

SCHEMA = "scriptorium-robinson-trusov-page-content-preflight-v1"
_INCLUSION_MARKUP_TOKEN = re.compile(\n    r"<!--|-->|<(/?)(noinclude|includeonly|onlyinclude)\\b([^>]*)>", re.I\n)
_HTML = re.compile(r"<[a-zA-Z/][^>]*>")
_HEX = re.compile(r"[a-f0-9]{64}\Z")


def transclusion_input(wikitext: str) -> str:
    """Remove explicit noinclude and unwrap includeonly; keep all other markup."""
    out, stack, offset = [], [], 0
    in_comment = False
    # Inclusion-looking tags inside HTML comments are literal wikitext,
    # not ProofreadPage transclusion directives. Keep comments unchanged.
    for tag in _INCLUSION_MARKUP_TOKEN.finditer(wikitext):
        token = tag.group(0)
        if token == "<!--":
            if in_comment:
                raise ValueError("nested Page HTML comment")
            in_comment = True
            continue
        if token == "-->":
            in_comment = False
            continue
        if in_comment:
            continue
        if "noinclude" not in stack:
            out.append(wikitext[offset:tag.start()])
        closing, name, attrs = tag.groups()
        name = name.lower()
        if name == "onlyinclude" or attrs.strip():
            raise ValueError("unsupported inclusion selector/attributes")
        if closing:
            if not stack or stack[-1] != name:
                raise ValueError("unbalanced Page inclusion tags")
            stack.pop()
        else:
            stack.append(name)
        offset = tag.end()
    if in_comment:
        raise ValueError("unclosed Page HTML comment")
    if stack:
        raise ValueError("unclosed Page inclusion tags")
    out.append(wikitext[offset:])
    candidate = "".join(out)
    if not candidate.strip():
        raise ValueError("empty Page transclusion input")
    return candidate


def capture(graph: Mapping[str, object], *, graph_sha256: str,
            query: Callable[..., dict] = _api_query,
            batch_size: int = 20, delay: float = 0,
            observer: Callable[[dict, str], None] | None = None) -> dict:
    """Fetch each pinned oldid (batched), verify identity and retain hashes only."""
    validate(graph)
    if not isinstance(graph_sha256, str) or not _HEX.fullmatch(graph_sha256):
        raise ValueError("invalid frozen graph SHA-256")
    if not 1 <= batch_size <= 30 or not 0 <= delay <= 5:
        raise ValueError("unbounded API parameters")
    records = graph["pages"]
    pages = []
    digest = sha256()
    chars = 0
    for start in range(0, len(records), batch_size):
        chunk = records[start:start + batch_size]
        if start and delay:
            sleep(delay)
        expected = {x["revision_id"]: x for x in chunk}
        payload = query({"action":"query", "prop":"revisions",
                         "revids":"|".join(str(x) for x in expected),
                         "rvprop":"ids|timestamp|sha1|content", "rvslots":"main"})
        response = payload.get("query") if isinstance(payload, dict) and "error" not in payload else None
        rows = response.get("pages") if isinstance(response, dict) else None
        if not isinstance(rows, list) or len(rows) != len(chunk):
            raise ValueError("incomplete pinned Page content batch")
        seen = {}
        for page in rows:
            if not isinstance(page, dict) or "missing" in page:
                raise ValueError("missing pinned Page")
            revs = page.get("revisions")
            if not isinstance(revs, list) or len(revs) != 1 or not isinstance(revs[0], dict):
                raise ValueError("ambiguous pinned Page revision")
            rev = revs[0]
            rid = rev.get("revid")
            if type(rid) is not int or rid not in expected or rid in seen:
                raise ValueError("unexpected/duplicate Page oldid")
            identity = expected[rid]
            if (page.get("pageid") != identity["page_id"]
                or page.get("title") != identity["title"]
                or rev.get("timestamp") != identity["timestamp_utc"]
                or rev.get("sha1") != identity["mediawiki_sha1"]):
                raise ValueError("historical Page source identity drift")
            main = rev.get("slots", {}).get("main") if isinstance(rev.get("slots"), dict) else None
            source = main.get("content") if isinstance(main, dict) else None
            model = main.get("contentmodel", "wikitext") if isinstance(main, dict) else None
            if model not in ("wikitext", "proofread-page"):
                raise ValueError(f"unsupported historical Page content model for oldid {rid}: {model!r}")
            if not isinstance(source, str):
                raise ValueError(f"missing historical Page source text for oldid {rid}")
            if not source.strip():
                raise ValueError(f"empty historical Page source for oldid {rid}; body coverage unknown")
            if len(source.encode("utf-8")) > 200_000:
                raise ValueError(f"oversized historical Page source for oldid {rid}")
            seen[rid] = source
        if set(seen) != set(expected):
            raise ValueError("incomplete pinned oldid coverage")
        for identity in chunk:
            raw = seen[identity["revision_id"]]
            candidate = transclusion_input(raw)
            if pages:
                digest.update(b"\n")
                chars += 1
            digest.update(candidate.encode("utf-8"))
            chars += len(candidate)
            if observer is not None:
                observer(identity, candidate)
            pages.append({
                "page_sequence":identity["page_sequence"],
                "revision_id":identity["revision_id"],
                "wikitext_sha256":sha256(raw.encode("utf-8")).hexdigest(),
                "wikitext_utf8_bytes":len(raw.encode("utf-8")),
                "transclusion_input_sha256":sha256(candidate.encode("utf-8")).hexdigest(),
                "transclusion_input_characters_including_spaces":len(candidate),
                "template_openers":candidate.count("{{"),
                "wikilink_openers":candidate.count("[["),
                "unexpanded_html_tags":len(_HTML.findall(candidate)),
            })
    result = {
        "schema_version":SCHEMA, "candidate_id":WORK_ID,
        "source_page_graph_sha256":graph_sha256, "page_count":len(pages),
        "pages":pages,
        "transclusion_profile":"strip-noinclude-unbox-includeonly-v1",
        "page_join_policy":"one_LF_between_raw_Page_inputs_diagnostic_only",
        "transclusion_input_candidate_sha256":digest.hexdigest(),
        "transclusion_input_candidate_characters_including_spaces":chars,
        "pages_with_unresolved_templates":sum(x["template_openers"] > 0 for x in pages),
        "pages_with_unresolved_links":sum(x["wikilink_openers"] > 0 for x in pages),
        "pages_with_unrendered_html":sum(x["unexpanded_html_tags"] > 0 for x in pages),
        "source_text_committed":False, "literary_body_sha256":None,
        "literary_characters_including_spaces":None, "literary_coverage_verified":False,
        "corpus_threshold_verified":False, "admitted_for_calibration":False,
        "historical_render_equivalence_proven":False, "fantlab_input_identity":"UNKNOWN",
        "m2_parity_admissible":False, "status":"TRANSCLUSION_INPUT_PREFLIGHT_ONLY"}
    validate_preflight(result, graph)
    return result


def validate_preflight(result: Mapping[str, object], graph: Mapping[str, object]) -> None:
    validate(graph)
    allowed = {"schema_version", "candidate_id", "source_page_graph_sha256", "page_count",
               "pages", "transclusion_profile", "page_join_policy",
               "transclusion_input_candidate_sha256",
               "transclusion_input_candidate_characters_including_spaces",
               "pages_with_unresolved_templates", "pages_with_unresolved_links",
               "pages_with_unrendered_html", "source_text_committed",
               "literary_body_sha256", "literary_characters_including_spaces",
               "literary_coverage_verified", "corpus_threshold_verified",
               "admitted_for_calibration", "historical_render_equivalence_proven",
               "fantlab_input_identity", "m2_parity_admissible", "status"}
    if set(result) != allowed or result.get("schema_version") != SCHEMA or result.get("candidate_id") != WORK_ID:
        raise ValueError("unexpected preflight shape or source prose leakage")
    for key, val in {
        "source_text_committed":False, "literary_body_sha256":None,
        "literary_characters_including_spaces":None, "literary_coverage_verified":False,
        "corpus_threshold_verified":False, "admitted_for_calibration":False,
        "historical_render_equivalence_proven":False, "fantlab_input_identity":"UNKNOWN",
        "m2_parity_admissible":False, "status":"TRANSCLUSION_INPUT_PREFLIGHT_ONLY",
        "transclusion_profile":"strip-noinclude-unbox-includeonly-v1",
        "page_join_policy":"one_LF_between_raw_Page_inputs_diagnostic_only"}.items():
        if result.get(key, object()) != val:
            raise ValueError("false scientific claim or unsupported profile")
    if not all(_HEX.fullmatch(str(result.get(key))) for key in
               ("source_page_graph_sha256", "transclusion_input_candidate_sha256")):
        raise ValueError("invalid preflight SHA-256")
    rows = result.get("pages")
    if not isinstance(rows, list) or result["page_count"] != len(graph["pages"]) or len(rows) != len(graph["pages"]):
        raise ValueError("incomplete preflight")
    keys = {"page_sequence", "revision_id", "wikitext_sha256", "wikitext_utf8_bytes",
            "transclusion_input_sha256", "transclusion_input_characters_including_spaces",
            "template_openers", "wikilink_openers", "unexpanded_html_tags"}
    for row, identity in zip(rows, graph["pages"]):
        if not isinstance(row, dict) or set(row) != keys:
            raise ValueError("unrecognized Page diagnostic or prose leakage")
        if row["page_sequence"] != identity["page_sequence"] or row["revision_id"] != identity["revision_id"]:
            raise ValueError("Page content order drift")
        if not all(_HEX.fullmatch(str(row[k])) for k in ("wikitext_sha256", "transclusion_input_sha256")):
            raise ValueError("invalid Page source digest")
        if not all(type(row[k]) is int and row[k] >= 0 for k in
                   ("wikitext_utf8_bytes", "transclusion_input_characters_including_spaces",
                    "template_openers", "wikilink_openers", "unexpanded_html_tags")):
            raise ValueError("invalid Page derived count")
    if result["transclusion_input_candidate_characters_including_spaces"] != (
        sum(x["transclusion_input_characters_including_spaces"] for x in rows) + len(rows) - 1):
        raise ValueError("candidate character count inconsistency")
    for metric, key in (("pages_with_unresolved_templates","template_openers"),
                        ("pages_with_unresolved_links","wikilink_openers"),
                        ("pages_with_unrendered_html","unexpanded_html_tags")):
        if result[metric] != sum(row[key] > 0 for row in rows):
            raise ValueError("unresolved markup counter mismatch")



def verify_receipt(report_file: Path, receipt_file: Path, graph: Mapping[str, object]) -> dict:
    """Validate a reproducible, source-free report against its retained digest receipt."""
    raw = report_file.read_bytes()
    report = json.loads(raw)
    validate_preflight(report, graph)
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))
    expected_keys = {
        "schema_version", "candidate_id", "page_graph_sha256",
        "source_free_report_sha256", "source_free_report_bytes", "page_count",
        "transclusion_input_profile", "transclusion_input_candidate_sha256",
        "transclusion_input_candidate_characters_including_spaces",
        "pages_with_unresolved_templates", "pages_with_unresolved_links",
        "pages_with_unrendered_html", "source_text_committed", "literary_body_sha256",
        "literary_characters_including_spaces", "literary_coverage_verified",
        "corpus_threshold_verified", "admitted_for_calibration",
        "historical_render_equivalence_proven", "fantlab_input_identity",
        "m2_parity_admissible", "evidence_workflow_run", "evidence_workflow_head_sha",
        "status",
    }
    if set(receipt) != expected_keys or receipt["schema_version"] != (
            "scriptorium-robinson-trusov-page-content-preflight-receipt-v1"):
        raise ValueError("unrecognized source-free Page content receipt")
    if (sha256(raw).hexdigest() != receipt["source_free_report_sha256"]
        or len(raw) != receipt["source_free_report_bytes"]):
        raise ValueError("source-free report receipt digest or size mismatch")
    mapping = {
        "candidate_id": "candidate_id",
        "source_page_graph_sha256": "page_graph_sha256",
        "page_count": "page_count",
        "transclusion_profile": "transclusion_input_profile",
        "transclusion_input_candidate_sha256": "transclusion_input_candidate_sha256",
        "transclusion_input_candidate_characters_including_spaces":
            "transclusion_input_candidate_characters_including_spaces",
        "pages_with_unresolved_templates": "pages_with_unresolved_templates",
        "pages_with_unresolved_links": "pages_with_unresolved_links",
        "pages_with_unrendered_html": "pages_with_unrendered_html",
        "source_text_committed": "source_text_committed",
        "literary_body_sha256": "literary_body_sha256",
        "literary_characters_including_spaces": "literary_characters_including_spaces",
        "literary_coverage_verified": "literary_coverage_verified",
        "corpus_threshold_verified": "corpus_threshold_verified",
        "admitted_for_calibration": "admitted_for_calibration",
        "historical_render_equivalence_proven": "historical_render_equivalence_proven",
        "fantlab_input_identity": "fantlab_input_identity",
        "m2_parity_admissible": "m2_parity_admissible",
        "status": "status",
    }
    if any(report.get(key) != receipt.get(target) for key, target in mapping.items()):
        raise ValueError("source-free report differs from committed receipt")
    if (receipt["evidence_workflow_run"] !=
        "https://github.com/drevendev/Scriptorium/actions/runs/41390834128"
        or receipt["evidence_workflow_head_sha"] !=
        "71ba78b664def7a04ead31d01b158532109515c2"):
        raise ValueError("unexpected primary source-capture evidence")
    return report

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect exact historical Page contents without prose.")
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--delay", type=float, default=0.75)
    args = parser.parse_args(argv)
    if args.output.exists() or args.output.resolve() in (args.graph.resolve(), args.receipt.resolve()):
        parser.error("output already exists or conflicts with evidence")
    graph = verify_frozen_graph(args.graph, args.receipt)
    result = capture(graph, graph_sha256=sha256(args.graph.read_bytes()).hexdigest(), delay=args.delay)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as destination:
        json.dump(result, destination, sort_keys=True, ensure_ascii=False, indent=2)
        destination.write("\n")
    print("Verified", result["page_count"], "Page contents; literary body NOT_RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
