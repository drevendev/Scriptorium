"""Measure a pinned Trusov interior Page sample without claiming a complete book.

The selected Page interval deliberately excludes the unresolved opening Page and
all four VAR-bearing ending Pages. Synthetic LF joins and conservative heading/
nop projection are *inferred*, not historical ProofreadPage rendering. Only
source-free measurements can leave memory; this is never corpus admission.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import isfinite
from pathlib import Path
import re
from typing import Callable, Mapping, Sequence

from .metrics import METRIC_CONTRACT_ID, SCHEMA_VERSION, analyze_deterministic_metrics
from .robinson_trusov_pages import WORK_ID, verify_frozen_graph
from .robinson_trusov_projection import ProjectedPageJoin, capture_projection
from .text import normalize_text

SCHEMA = "scriptorium-trusov-interior-measurement-v1"
SEAM_SCHEMA = "scriptorium-trusov-page-join-sensitivity-v2"
PROFILE = "inferred_projected_Page_3_to_147_excerpt_v1"
FIRST, LAST = 3, 147
EXCLUDED = [2, 148, 149, 150, 151]
_UNRENDERED_MARKUP = re.compile(r"\{\{|\}\}|\[\[|\]\]|<!--|-->|</?[A-Za-z][^>]*>|(?m:^\s*\{\|)")
_UNBOUND = frozenset({
    "fantlab.vocabulary.active_dictionary",
    "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000",
    "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})


class InteriorCollector:
    """Hold transient projected Page text until full pinned replay validates."""

    def __init__(self) -> None:
        self.selected: dict[int, tuple[dict, str]] = {}

    def observe(self, identity: dict, projected: str, unresolved: int, residual: int) -> None:
        n = identity["page_sequence"]
        if not FIRST <= n <= LAST:
            return
        if (n in self.selected or unresolved or residual or not projected.strip()
                or _UNRENDERED_MARKUP.search(projected)):
            raise ValueError(f"interior Page {n} not safely projected; no measurement")
        self.selected[n] = (identity, projected)

    def build(self, graph: Mapping[str, object], graph_sha256: str,
              projection: Mapping[str, object]) -> dict[str, object]:
        """Emit only metrics/identities. Never return the transient Page texts."""
        selected = self.selected
        sequence = list(range(FIRST, LAST + 1))
        if (graph.get("candidate_id") != WORK_ID
                or graph.get("selection", {}).get("from") != 2
                or graph.get("selection", {}).get("to") != 151
                or set(selected) != set(sequence)
                or projection.get("page_count") != 150):
            raise ValueError("incomplete or unexpected Trusov interior selection")
        by_page = {row["page_sequence"]: row for row in projection["pages"]}
        join = ProjectedPageJoin()
        revision_rows: list[list[object]] = []
        chunks: list[str] = []
        for n in sequence:
            identity, projected = selected[n]
            verified = by_page[n]
            if (sha256(projected.encode("utf-8")).hexdigest() != verified["projected_wikitext_sha256"]
                    or len(projected) != verified["projected_wikitext_characters_including_spaces"]
                    or identity["revision_id"] != verified["revision_id"]
                    or identity["mediawiki_sha1"] != verified["source_mediawiki_sha1"]
                    or verified["unresolved_invocations"] != 0
                    or verified["unclassified_openers"] != 0):
                raise ValueError(f"interior Page {n} identity/projection mismatch")
            join.add(projected)
            chunks.append(projected)
            revision_rows.append([n, identity["revision_id"], identity["mediawiki_sha1"]])
        # Deliberate diagnostic joining rule, NOT historical ProofreadPage rendering.
        excerpt = "\n".join(chunks)
        joined = join.source_free_identity()
        if (sha256(excerpt.encode("utf-8")).hexdigest() != joined["joined_projected_wikitext_sha256"]
                or len(excerpt) != joined["joined_projected_wikitext_characters_including_spaces"]
                or len(excerpt) < 1000):
            raise ValueError("interior Page join drift or unusably short sample")
        normalized = normalize_text(excerpt)
        measured = analyze_deterministic_metrics(excerpt)
        metric_map = measured.get("metrics")
        if (measured.get("schema_version") != SCHEMA_VERSION
                or measured.get("metric_contract_id") != METRIC_CONTRACT_ID
                or measured.get("normalized_sha256") != sha256(normalized.encode("utf-8")).hexdigest()
                or measured.get("dependencies", {}).get("vocabulary_dictionary") is not None
                or not isinstance(metric_map, dict) or len(metric_map) != 29
                or metric_map.get("fantlab.general.characters", {}).get("value") != len(normalized)):
            raise ValueError("unexpected deterministic metric/normalization contract")
        rows = []
        for metric_id, metric in sorted(metric_map.items()):
            value = metric["value"]
            if (value is not None and (type(value) not in (int, float) or not isfinite(value))
                    or metric_id in _UNBOUND and value is not None):
                raise ValueError("unbound/nonfinite metric invalid")
            rows.append({
                "metric_id": metric_id,
                "actual": value,
                "unit": metric["unit"],
                "compatibility_status": metric["compatibility_status"],
                "result": ("NOT_RUN_DICTIONARY_UNBOUND" if metric_id in _UNBOUND
                           else "UNAVAILABLE_NO_OBSERVATIONS" if value is None
                           else "MEASURED_INTERIOR_EXCERPT_ONLY"),
                "fantlab_display": None,
            })
        result = {
            "schema_version": SCHEMA,
            "version": PROFILE,
            "candidate_id": WORK_ID,
            "status": "INCOMPLETE_INTERIOR_EXCERPT_NOT_CORPUS_OR_PARITY",
            "source_page_graph_sha256": graph_sha256,
            "carrier_revision_id": graph["carrier"]["revision_id"],
            "page_interval": {"from": FIRST, "to": LAST, "count": len(sequence),
                              "excluded_pages": EXCLUDED, "opening_truncated": True,
                              "ending_truncated": True},
            "source_revision_list_sha256": sha256(json.dumps(revision_rows, separators=(",", ":"),
                                                           ensure_ascii=False).encode("utf-8")).hexdigest(),
            "join": joined,
            "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
            "normalized_characters_including_spaces": len(normalized),
            "scriptorium": {"schema_version": SCHEMA_VERSION,
                            "metric_contract_id": METRIC_CONTRACT_ID,
                            "profiles": measured["profiles"], "vocabulary_dictionary_dependency": None},
            "metric_rows": rows,
            "numeric_metric_count": sum(row["actual"] is not None for row in rows),
            "unavailable_metric_count": sum(row["actual"] is None for row in rows),
            "gates": {"pinned_150_page_source_replay": True,
                      "full_literary_body": "NOT_RUN",
                      "historical_proofreadpage_rendering": "NOT_VERIFIED",
                      "page_join_historical_identity": "UNKNOWN",
                      "aligned_translation_coverage": "NOT_RUN",
                      "print_edition_collation": "NOT_RUN",
                      "fantlab_analyzer_input_identity": "UNKNOWN",
                      "corpus_admitted_for_calibration": False,
                      "author_profile_admissible": False,
                      "m2_parity_admissible": False,
                      "source_text_committed": False},
        }
        return result


    def seam_sensitivity(self, baseline: Mapping[str, object]) -> dict[str, object]:
        """Compare synthetic Page separators against the frozen one-LF excerpt.

        This is *not* an alternative historical transcription. In addition to
        stress extremes, test a single ASCII space: MediaWiki documents it as
        the default ProofreadPage separator, but the site's 2023 configuration
        and historical hyphenation/transclusion behavior are NOT verified.
        Only source-free 29-field deltas leave transient memory.
        """
        sequence = list(range(FIRST, LAST + 1))
        if (set(self.selected) != set(sequence)
                or baseline.get("schema_version") != SCHEMA
                or baseline.get("version") != PROFILE
                or baseline.get("candidate_id") != WORK_ID
                or baseline.get("status") != "INCOMPLETE_INTERIOR_EXCERPT_NOT_CORPUS_OR_PARITY"
                or baseline.get("page_interval", {}).get("count") != len(sequence)
                or baseline.get("page_interval", {}).get("excluded_pages") != EXCLUDED
                or baseline.get("gates", {}).get("full_literary_body") != "NOT_RUN"
                or baseline.get("gates", {}).get("corpus_admitted_for_calibration") is not False):
            raise ValueError("join sensitivity requires a verified incomplete interior")
        chunks = [self.selected[n][1] for n in sequence]
        original = "\n".join(chunks)
        if (sha256(original.encode("utf-8")).hexdigest()
                != baseline["join"]["joined_projected_wikitext_sha256"]
                or len(original) != baseline["join"]["joined_projected_wikitext_characters_including_spaces"]
                or sha256(normalize_text(original).encode("utf-8")).hexdigest()
                != baseline["normalized_sha256"]):
            raise ValueError("join sensitivity baseline/source identity mismatch")
        rows = baseline["metric_rows"]
        if (not isinstance(rows, list) or len(rows) != 29
                or len({r["metric_id"] for r in rows}) != 29):
            raise ValueError("invalid 29-field baseline")
        reference = {r["metric_id"]: r for r in rows}
        # The Page/hash checks above bind source bytes, not the numeric claims
        # in a supplied baseline report. Recompute the exact one-LF metrics
        # before calculating signed deltas; otherwise a modified prior value
        # silently makes the derived sensitivity report scientifically false.
        replay = analyze_deterministic_metrics(original)
        observed = replay.get("metrics")
        expected_profile = {
            "schema_version": SCHEMA_VERSION,
            "metric_contract_id": METRIC_CONTRACT_ID,
            "profiles": replay.get("profiles"),
            "vocabulary_dictionary_dependency": None,
        }
        if (replay.get("schema_version") != SCHEMA_VERSION
                or replay.get("metric_contract_id") != METRIC_CONTRACT_ID
                or replay.get("normalized_sha256") != baseline["normalized_sha256"]
                or replay.get("dependencies", {}).get("vocabulary_dictionary") is not None
                or not isinstance(observed, dict) or set(observed) != set(reference)
                or baseline.get("scriptorium") != expected_profile
                or baseline.get("normalized_characters_including_spaces")
                != len(normalize_text(original))
                or baseline.get("numeric_metric_count")
                != sum(metric["value"] is not None for metric in observed.values())
                or baseline.get("unavailable_metric_count")
                != sum(metric["value"] is None for metric in observed.values())):
            raise ValueError("join sensitivity baseline metric replay mismatch")
        for metric_id, previous in reference.items():
            measured = observed[metric_id]
            value = measured["value"]
            expected_result = (
                "NOT_RUN_DICTIONARY_UNBOUND" if metric_id in _UNBOUND
                else "UNAVAILABLE_NO_OBSERVATIONS" if value is None
                else "MEASURED_INTERIOR_EXCERPT_ONLY"
            )
            if (set(previous) != {"metric_id", "actual", "unit",
                                  "compatibility_status", "result", "fantlab_display"}
                    or type(previous["actual"]) is not type(value)
                    or previous["actual"] != value
                    or previous["unit"] != measured["unit"]
                    or previous["compatibility_status"] != measured["compatibility_status"]
                    or previous["result"] != expected_result
                    or previous["fantlab_display"] is not None):
                raise ValueError(f"join sensitivity baseline metric drift: {metric_id}")
        variants = []
        for profile, separator in (("direct_concatenation_stress_test", ""),
                                   ("one_space_ProofreadPage_default_hypothesis", " "),
                                   ("two_LF_paragraph_stress_test", "\n\n")):
            text = separator.join(chunks)
            normalized = normalize_text(text)
            measurement = analyze_deterministic_metrics(text)
            measures = measurement.get("metrics")
            if (measurement.get("schema_version") != SCHEMA_VERSION
                    or measurement.get("metric_contract_id") != METRIC_CONTRACT_ID
                    or measurement.get("normalized_sha256")
                    != sha256(normalized.encode("utf-8")).hexdigest()
                    or not isinstance(measures, dict)
                    or set(measures) != set(reference)):
                raise ValueError("join sensitivity metric contract drift")
            deltas = []
            for metric_id, prior in sorted(reference.items()):
                current = measures[metric_id]
                a, b = prior["actual"], current["value"]
                if (current["unit"] != prior["unit"]
                        or (a is not None and (type(a) not in (int, float) or not isfinite(a)))
                        or (b is not None and (type(b) not in (int, float) or not isfinite(b)))
                        or (metric_id in _UNBOUND and b is not None)):
                    raise ValueError("invalid join sensitivity metric value")
                delta = b - a if a is not None and b is not None else None
                deltas.append({
                    "metric_id": metric_id,
                    "unit": prior["unit"],
                    "alternate_value": b,
                    "delta_from_one_LF": delta,
                    "status": ("UNAVAILABLE" if delta is None else
                               "CHANGED" if delta != 0 else "UNCHANGED"),
                })
            variants.append({
                "join_profile": profile,
                "joined_sha256": sha256(text.encode("utf-8")).hexdigest(),
                "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
                "normalized_characters_including_spaces": len(normalized),
                "changed_numeric_metrics": sum(d["status"] == "CHANGED" for d in deltas),
                "metrics": deltas,
            })
        return {
            "schema_version": SEAM_SCHEMA,
            "candidate_id": WORK_ID,
            "source_page_graph_sha256": baseline["source_page_graph_sha256"],
            "source_revision_list_sha256": baseline["source_revision_list_sha256"],
            "interval": baseline["page_interval"],
            "baseline_profile": baseline["join"]["projected_page_join_profile"],
            "baseline_normalized_sha256": baseline["normalized_sha256"],
            "baseline_numeric_metrics": baseline["numeric_metric_count"],
            "alternatives": variants,
            "scope": "SYNTHETIC_PAGE_JOIN_SENSITIVITY_ONLY",
            "historical_page_join_verified": False,
            "complete_literary_body": False,
            "corpus_admitted": False,
            "m2_parity_admissible": False,
            "source_text_committed": False,
        }


def folio_join_variants(chunks: Sequence[str]) -> tuple[str, str, dict[str, int]]:
    """Change only the /106→107 edge; retain all other synthetic LF joins."""
    if len(chunks) != LAST - FIRST + 1:
        raise ValueError("folio sensitivity requires all interior Pages")
    i = 106 - FIRST
    left, right = chunks[i], chunks[i + 1]
    # Preserve and account for edge whitespace separately from the one hyphen.
    a, b = left.rstrip(), right.lstrip()
    if (len(a) < 2 or not a.endswith("-") or not a[-2].isalpha()
            or not b or not b[0].isalpha() or not b[0].islower()):
        raise ValueError("pinned folio edge shape drift")
    prefix = "\n".join(chunks[:i]) + "\n"
    suffix = "\n" + "\n".join(chunks[i + 2:])
    literal = prefix + a + b + suffix
    omitted = prefix + a[:-1] + b + suffix
    return literal, omitted, {"left_edge_whitespace_removed": len(left) - len(a),
                              "right_edge_whitespace_removed": len(right) - len(b),
                              "synthetic_LF_removed": 1, "ascii_hyphen_removed": 1}


def folio_metric_sensitivity(collector, baseline, proof):
    """Measure an observed carrier-only join hypothesis, not a new text edition."""
    from .robinson_trusov_missing_folios import PINS
    if (proof.get("schema_version") != "scriptorium-trusov-missing-folios-v3"
            or proof.get("source_page_graph_sha256") != baseline["source_page_graph_sha256"]
            or proof.get("carrier_revision_id") != 5041937
            or proof.get("left_edge_comparison") != "SOURCE_LITERAL_CARRIER_OMISSION"
            or proof.get("scope_projection_byte_equal") is not True
            or proof.get("current_render_edge_joins", {}).get("left") != {
                "matches": {"DIRECT": 0, "SPACE": 0, "HYPHEN_OMITTED_DIRECT": 1,
                            "HYPHEN_OMITTED_SPACE": 0}, "selected": "HYPHEN_OMITTED_DIRECT"}
            or proof.get("pinned_left_hyphen") != {
                "left_revision_id": PINS[106], "right_revision_id": PINS[107],
                "terminal_ascii_hyphen_count": 1, "raw_before_terminal_noinclude": True,
                "scoped_retained": True, "projected_retained": True}):
        raise ValueError("unverified pinned folio join evidence")
    selected = collector.selected
    if set(selected) != set(range(FIRST, LAST + 1)):
        raise ValueError("incomplete interior")
    expected = [{"page_sequence": n, "revision_id": PINS[n],
                 "projected_sha256": sha256(selected[n][1].encode("utf-8")).hexdigest()}
                for n in sorted(PINS)]
    actual = [{k: row[k] for k in ("page_sequence", "revision_id", "projected_sha256")}
              for row in proof["pages"]]
    if actual != expected or any(selected[n][0]["revision_id"] != PINS[n] for n in PINS):
        raise ValueError("folio receipt/source identity mismatch")
    chunks = [selected[n][1] for n in range(FIRST, LAST + 1)]
    original = "\n".join(chunks)
    if (baseline["status"] != "INCOMPLETE_INTERIOR_EXCERPT_NOT_CORPUS_OR_PARITY"
            or baseline["join"]["joined_projected_wikitext_sha256"] != sha256(original.encode("utf-8")).hexdigest()
            or baseline["normalized_sha256"] != sha256(normalize_text(original).encode("utf-8")).hexdigest()):
        raise ValueError("folio baseline identity mismatch")
    literal, omitted, edits = folio_join_variants(chunks)
    if len(original) - len(literal) != 1 + edits["left_edge_whitespace_removed"] + edits["right_edge_whitespace_removed"] or len(literal) - len(omitted) != 1:
        raise ValueError("folio character accounting mismatch")
    values = [analyze_deterministic_metrics(t) for t in (original, literal, omitted)]
    prior = {row["metric_id"]: row for row in baseline["metric_rows"]}
    if len(prior) != 29 or len(baseline["metric_rows"]) != 29:
        raise ValueError("invalid baseline metric surface")
    for result, txt in zip(values, (original, literal, omitted)):
        if (result["schema_version"] != SCHEMA_VERSION
                or result["metric_contract_id"] != METRIC_CONTRACT_ID
                or result["normalized_sha256"] != sha256(normalize_text(txt).encode("utf-8")).hexdigest()
                or set(result["metrics"]) != set(prior)
                or result["dependencies"].get("vocabulary_dictionary") is not None):
            raise ValueError("folio metric contract drift")
    rows = []
    for key in sorted(prior):
        metrics = [v["metrics"][key] for v in values]
        a, b, c = (m["value"] for m in metrics)
        if (type(a) is not type(prior[key]["actual"]) or a != prior[key]["actual"]
                or any(m["unit"] != prior[key]["unit"] for m in metrics)
                or any(v is not None and (type(v) not in (int, float) or not isfinite(v))
                       for v in (a, b, c))
                or key in _UNBOUND and any(v is not None for v in (a, b, c))):
            raise ValueError("folio metric baseline drift")
        rows.append({"metric_id": key, "unit": prior[key]["unit"],
                     "baseline_one_LF": a, "literal_direct": b, "carrier_omission_direct": c,
                     "delta_join_only": b - a if a is not None and b is not None else None,
                     "delta_hyphen_only": c - b if b is not None and c is not None else None,
                     "delta_total": c - a if a is not None and c is not None else None})
    return {"schema_version": "scriptorium-trusov-folio-join-metrics-v1",
            "scope": "INCOMPLETE_INTERIOR_SINGLE_SEAM_SENSITIVITY_ONLY",
            "source_page_graph_sha256": baseline["source_page_graph_sha256"],
            "baseline_normalized_sha256": baseline["normalized_sha256"],
            "proof_pages": expected, "edge": [106, 107], "edits": edits,
            "normalized_sha256": [v["normalized_sha256"] for v in values],
            "normalized_characters_including_spaces": [len(normalize_text(t)) for t in (original, literal, omitted)],
            "metric_rows": rows,
            "full_literary_body": "NOT_VERIFIED", "print_collation": "NOT_VERIFIED",
            "historical_page_join_verified": False, "corpus_admitted": False,
            "m2_parity_admissible": False, "source_text_committed": False}


def measure_interior(graph: Mapping[str, object], graph_sha256: str, *,
                     query: Callable[..., dict], delay: float = 0) -> dict[str, object]:
    """Source-verified one-pass standalone diagnostic, never a corpus admission."""
    collector = InteriorCollector()
    projection = capture_projection(graph, graph_sha256, query=query, delay=delay,
                                    page_observer=collector.observe)
    return collector.build(graph, graph_sha256, projection)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--delay", type=float, default=0.75)
    args = parser.parse_args(argv)
    if (args.output.resolve() in {args.graph.resolve(), args.receipt.resolve()}
            or args.output.exists()):
        parser.error("output must be new and must not overwrite frozen source identities")
    graph = verify_frozen_graph(args.graph, args.receipt)
    from .single_page_revision import _api_query
    result = measure_interior(graph, sha256(args.graph.read_bytes()).hexdigest(),
                              query=_api_query, delay=args.delay)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
    print(f"Trusov inferred interior sample Pages {FIRST}-{LAST}: "
          f"{result['join']['joined_projected_wikitext_characters_including_spaces']} "
          f"projected characters, {result['numeric_metric_count']}/29 numeric metrics; "
          "NOT a complete body, corpus entry, rendered edition or FantLab parity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
