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
