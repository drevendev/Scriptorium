"""Fail-closed 150-Page Trusov measurement candidate, not a historical book.

Keep fetched Page text transient. A single unresolved opening/ending Page
prevents ALL full-candidate metrics; the accepted 145-Page interior diagnostic
is a separate artifact. Even an all-safe projection is inferred synthetic
wikitext, not a verified ProofreadPage render, 1775 printed edition or corpus.
"""
from __future__ import annotations

from hashlib import sha256
import json
from math import isfinite
from typing import Callable, Mapping

from .metrics import METRIC_CONTRACT_ID, SCHEMA_VERSION, analyze_deterministic_metrics
from .robinson_trusov_interior import _UNBOUND, _UNRENDERED_MARKUP
from .robinson_trusov_pages import WORK_ID
from .robinson_trusov_projection import ProjectedPageJoin, capture_projection
from .text import normalize_text

SCHEMA = "scriptorium-trusov-150-page-projected-candidate-v1"
PROFILE = "inferred_150_Page_synthetic_join_candidate_v1"
BLOCKED = "BLOCKED_UNRESOLVED_150_PAGE_PROJECTION"
READY = "MEASURED_150_PAGE_PROJECTION_NOT_HISTORICAL_BODY"
PAGE_NUMBERS = tuple(range(2, 152))


class FullCandidateCollector:
    """Transient projection collector that refuses incomplete candidate metrics."""

    def __init__(self) -> None:
        self.safe: dict[int, tuple[dict, str]] = {}
        self.blocked: dict[int, dict] = {}

    def observe(self, identity: dict, projected: str,
                unresolved: int, residual: int) -> None:
        n = identity["page_sequence"]
        if (n not in PAGE_NUMBERS or n in self.safe or n in self.blocked
                or type(unresolved) is not int or unresolved < 0
                or type(residual) is not int or residual < 0):
            raise ValueError("duplicate/invalid pinned Page observation")
        markup = bool(_UNRENDERED_MARKUP.search(projected))
        blank = not projected.strip()
        if unresolved or residual or markup or blank:
            # No candidate text is retained for blocked pages or emitted.
            self.blocked[n] = {
                "page_sequence": n,
                "revision_id": identity["revision_id"],
                "unresolved_invocations": unresolved,
                "unclassified_openers": residual,
                "unrendered_markup": markup,
                "empty_projected_page": blank,
            }
        else:
            self.safe[n] = (identity, projected)

    def build(self, graph: Mapping[str, object], graph_sha256: str,
              projection: Mapping[str, object]) -> dict[str, object]:
        selection = graph.get("selection", {})
        if (graph.get("candidate_id") != WORK_ID
                or selection.get("from") != 2 or selection.get("to") != 151
                or projection.get("page_count") != 150
                or projection.get("source_page_graph_sha256") != graph_sha256
                or set(self.safe) | set(self.blocked) != set(PAGE_NUMBERS)
                or set(self.safe) & set(self.blocked)):
            raise ValueError("incomplete/mismatched 150-Page projection")
        expected = {row["page_sequence"]: row for row in graph["pages"]}
        observed = {row["page_sequence"]: row for row in projection["pages"]}
        if set(expected) != set(PAGE_NUMBERS) or set(observed) != set(PAGE_NUMBERS):
            raise ValueError("incomplete/duplicate frozen Page identities")
        identities: list[list[object]] = []
        for n in PAGE_NUMBERS:
            frozen, actual = expected[n], observed[n]
            if (frozen["revision_id"] != actual["revision_id"]
                    or frozen["mediawiki_sha1"] != actual["source_mediawiki_sha1"]):
                raise ValueError(f"pinned Page {n} identity drift")
            identities.append([n, frozen["revision_id"], frozen["mediawiki_sha1"]])
            if n in self.blocked:
                b = self.blocked[n]
                if (b["revision_id"] != actual["revision_id"]
                        or b["unresolved_invocations"] != actual["unresolved_invocations"]
                        or b["unclassified_openers"] != actual["unclassified_openers"]):
                    raise ValueError(f"blocked Page {n} count drift")
            else:
                identity, text = self.safe[n]
                if (identity["revision_id"] != actual["revision_id"]
                        or identity["mediawiki_sha1"] != actual["source_mediawiki_sha1"]
                        or sha256(text.encode("utf-8")).hexdigest()
                           != actual["projected_wikitext_sha256"]
                        or len(text) != actual["projected_wikitext_characters_including_spaces"]
                        or actual["unresolved_invocations"] != 0
                        or actual["unclassified_openers"] != 0):
                    raise ValueError(f"safe Page {n} projection drift")
        result: dict[str, object] = {
            "schema_version": SCHEMA,
            "version": PROFILE,
            "candidate_id": WORK_ID,
            "carrier_revision_id": graph["carrier"]["revision_id"],
            "source_page_graph_sha256": graph_sha256,
            "source_revision_list_sha256": sha256(
                json.dumps(identities, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            ).hexdigest(),
            "page_interval": {"from": 2, "to": 151, "count": 150},
            "status": BLOCKED if self.blocked else READY,
            "blocked_pages": [self.blocked[n] for n in sorted(self.blocked)],
            "projected_join": None,
            "normalized_sha256": None,
            "normalized_characters_including_spaces": None,
            "scriptorium": None,
            "metric_rows": None,
            "numeric_metric_count": None,
            "unavailable_metric_count": None,
            "gates": {
                "historical_ProofreadPage_rendering": "NOT_VERIFIED",
                "historical_page_join_identity": "UNKNOWN",
                "1775_print_edition_collation": "NOT_RUN",
                "full_literary_body": "NOT_VERIFIED",
                "translation_coverage_alignment": "NOT_RUN",
                "permission_for_full_text_reuse": "NOT_VERIFIED",
                "fantlab_analyzer_input_identity": "UNKNOWN",
                "corpus_admitted_for_calibration": False,
                "author_profile_admissible": False,
                "m2_parity_admissible": False,
                "source_text_committed": False,
            },
        }
        if self.blocked:
            return result

        # Only all 150 safe, source-bound Pages can produce candidate metrics.
        chunks = [self.safe[n][1] for n in PAGE_NUMBERS]
        joined_text = "\n".join(chunks)
        joined = ProjectedPageJoin()
        for chunk in chunks:
            joined.add(chunk)
        join_info = joined.source_free_identity()
        if (len(joined_text) < 1_000
                or len(joined_text) != join_info["joined_projected_wikitext_characters_including_spaces"]
                or sha256(joined_text.encode("utf-8")).hexdigest()
                   != join_info["joined_projected_wikitext_sha256"]):
            raise ValueError("150-Page projected join identity drift")
        normalized = normalize_text(joined_text)
        analyzed = analyze_deterministic_metrics(joined_text)
        fields = analyzed.get("metrics")
        if (analyzed.get("schema_version") != SCHEMA_VERSION
                or analyzed.get("metric_contract_id") != METRIC_CONTRACT_ID
                or analyzed.get("normalized_sha256")
                   != sha256(normalized.encode("utf-8")).hexdigest()
                or analyzed.get("dependencies", {}).get("vocabulary_dictionary") is not None
                or not isinstance(fields, dict) or len(fields) != 29
                or fields.get("fantlab.general.characters", {}).get("value") != len(normalized)):
            raise ValueError("150-Page candidate metrics contract drift")
        rows = []
        for key, field in sorted(fields.items()):
            value = field["value"]
            if (value is not None and (type(value) not in (int, float) or not isfinite(value))
                    or key in _UNBOUND and value is not None):
                raise ValueError("invalid/unbound full-candidate metric")
            rows.append({
                "metric_id": key, "actual": value,
                "unit": field["unit"],
                "compatibility_status": field["compatibility_status"],
                "result": ("NOT_RUN_DICTIONARY_UNBOUND" if key in _UNBOUND
                           else "UNAVAILABLE_NO_OBSERVATIONS" if value is None
                           else "MEASURED_SYNTHETIC_150_PAGE_PROJECTION_ONLY"),
                "fantlab_display": None,
            })
        result.update({
            "projected_join": join_info,
            "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
            "normalized_characters_including_spaces": len(normalized),
            "scriptorium": {
                "schema_version": SCHEMA_VERSION,
                "metric_contract_id": METRIC_CONTRACT_ID,
                "profiles": analyzed["profiles"],
                "vocabulary_dictionary_dependency": None,
            },
            "metric_rows": rows,
            "numeric_metric_count": sum(r["actual"] is not None for r in rows),
            "unavailable_metric_count": sum(r["actual"] is None for r in rows),
        })
        return result


def measure_full_candidate(graph: Mapping[str, object], graph_sha256: str, *,
                           query: Callable[..., dict], delay: float = 0) -> dict[str, object]:
    """One pinned source replay: results are source-free, never corpus admission."""
    collector = FullCandidateCollector()
    projection = capture_projection(graph, graph_sha256, query=query, delay=delay,
                                    page_observer=collector.observe)
    return collector.build(graph, graph_sha256, projection)
