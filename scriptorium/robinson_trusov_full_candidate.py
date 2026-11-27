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
from .robinson_trusov_projection import VAR_REFUSAL_KEYS, ProjectedPageJoin, capture_projection
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
        blocker_details: list[dict] = []
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
                # The verified projection already partitions each historical
                # VAR invocation. Surface those source-free decisions at the
                # exact blocked Page, without treating any preview as rendering.
                reasons = actual["var_preview_refusal_reasons"]
                flat, multiline = (actual["flat_var_preview_count"],
                                   actual["multiline_var_preview_count"])
                if (not isinstance(reasons, dict)
                        or set(reasons) != set(VAR_REFUSAL_KEYS)
                        or any(type(v) is not int or v < 0 for v in reasons.values())
                        or type(flat) is not int or flat < 0
                        or type(multiline) is not int or multiline < 0):
                    raise ValueError(f"blocked Page {n} invalid VAR classification")
                preview_only = flat + multiline
                all_var = preview_only + sum(reasons.values())
                if all_var > b["unresolved_invocations"]:
                    raise ValueError(f"blocked Page {n} VAR classification drift")
                blocker_details.append({
                    **b,
                    "unresolved_non_var_invocations":
                        b["unresolved_invocations"] - all_var,
                    "var_preview_only_invocations": preview_only,
                    "var_preview_refusals": {
                        key: reasons[key] for key in VAR_REFUSAL_KEYS if reasons[key]
                    },
                })
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
            "blocked_pages": blocker_details,
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
        # The per-Page digests alone do not authenticate the aggregate receipt:
        # bind this reconstructed LF join to the independently validated
        # 150-Page projection, including seam counters and join policy.
        if any(projection.get(key) != value for key, value in join_info.items()):
            raise ValueError("150-Page projected join versus projection receipt drift")
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


BOUNDARY_PAGES = (2, 148, 149, 150, 151)


def assemble_boundary_metrics(collector, baseline, boundaries):
    """Separate historical-branch diagnostic; never replace the frozen interior.

    The caller supplies only boundary strings from the pinned scope replays.
    One synthetic LF per Page is retained, including the /106→107 hyphen.
    """
    if (set(boundaries) != set(BOUNDARY_PAGES)
            or set(collector.selected) != set(range(3, 148))
            or baseline.get("status") != "INCOMPLETE_INTERIOR_EXCERPT_NOT_CORPUS_OR_PARITY"):
        raise ValueError("incomplete boundary assembly")
    chunks = {n: value[1] for n, value in collector.selected.items()}
    if any(not isinstance(t, str) or not t.strip() or _UNRENDERED_MARKUP.search(t)
           or any(c in t for c in "{}<>[]") or "''" in t
           for t in boundaries.values()):
        raise ValueError("unresolved boundary assembly markup")
    interior = "\n".join(chunks[n] for n in range(3, 148))
    if (sha256(interior.encode("utf-8")).hexdigest()
            != baseline["join"]["joined_projected_wikitext_sha256"]
            or sha256(normalize_text(interior).encode("utf-8")).hexdigest()
            != baseline["normalized_sha256"]):
        raise ValueError("boundary assembly interior identity drift")
    chunks.update(boundaries)
    assembled = "\n".join(chunks[n] for n in PAGE_NUMBERS)
    if len(assembled) != len(interior) + sum(map(len, boundaries.values())) + 5:
        raise ValueError("boundary assembly character accounting drift")
    reference = {r["metric_id"]: r for r in baseline["metric_rows"]}
    if len(reference) != 29 or len(baseline["metric_rows"]) != 29:
        raise ValueError("invalid boundary metric reference")
    prior, current = (analyze_deterministic_metrics(t) for t in (interior, assembled))
    normalized = normalize_text(assembled)
    for result, txt in ((prior, interior), (current, assembled)):
        if (result["schema_version"] != SCHEMA_VERSION
                or result["metric_contract_id"] != METRIC_CONTRACT_ID
                or result["normalized_sha256"] != sha256(normalize_text(txt).encode("utf-8")).hexdigest()
                or result["dependencies"].get("vocabulary_dictionary") is not None
                or set(result["metrics"]) != set(reference)):
            raise ValueError("boundary metric contract drift")
    rows = []
    for key, ref in sorted(reference.items()):
        old, new = prior["metrics"][key], current["metrics"][key]
        a, v = old["value"], new["value"]
        if (type(a) is not type(ref["actual"]) or a != ref["actual"]
                or old["unit"] != ref["unit"] or new["unit"] != ref["unit"]
                or any(x is not None and (type(x) not in (int, float) or not isfinite(x))
                       for x in (a, v))
                or key in _UNBOUND and v is not None):
            raise ValueError("boundary metric reference drift")
        rows.append({"metric_id": key, "unit": ref["unit"],
                     "interior_value": a, "assembly_value": v,
                     "delta": v - a if v is not None and a is not None else None})
    return {
        "schema_version": "scriptorium-trusov-boundary-assembly-v1",
        "scope": "INFERRED_150_PAGE_HISTORICAL_BRANCH_ASSEMBLY_DIAGNOSTIC",
        "source_page_graph_sha256": baseline["source_page_graph_sha256"],
        "source_revision_list_sha256": baseline["source_revision_list_sha256"],
        "baseline_normalized_sha256": baseline["normalized_sha256"],
        "page_interval": {"from": 2, "to": 151, "count": 150},
        "boundary_pages": [{"page_sequence": n, "characters": len(boundaries[n]),
                            "sha256": sha256(boundaries[n].encode("utf-8")).hexdigest()}
                           for n in BOUNDARY_PAGES],
        "join_profile": "one_LF_between_projected_Page_inputs_diagnostic_only",
        "raw_joined_characters": len(assembled),
        "raw_joined_sha256": sha256(assembled.encode("utf-8")).hexdigest(),
        "normalized_characters_including_spaces": len(normalized),
        "normalized_sha256": current["normalized_sha256"],
        "metric_rows": rows,
        "numeric_metric_count": sum(r["assembly_value"] is not None for r in rows),
        "unavailable_metric_count": sum(r["assembly_value"] is None for r in rows),
        "full_literary_body": "NOT_VERIFIED", "print_collation": "NOT_VERIFIED",
        "historical_render_equivalence_proven": False,
        "historical_page_join_verified": False, "corpus_admitted": False,
        "m2_parity_admissible": False, "source_text_committed": False,
    }


def capture_boundary_assembly(collector, baseline, graph, preflight, *, query):
    """Use the exact-byte opening and closing replays; never store boundary prose."""
    from .robinson_trusov_opening_seam import capture as opening
    from .robinson_trusov_closing_seams import capture as closing
    if preflight["source_page_graph_sha256"] != baseline["source_page_graph_sha256"]:
        raise ValueError("boundary assembly graph drift")
    boundaries = {}
    def observe(n, text):
        if n in boundaries or n not in BOUNDARY_PAGES:
            raise ValueError("duplicate/unexpected boundary observation")
        boundaries[n] = text
    layout = {}
    opened = opening(graph, preflight, query=query, layout_output=layout,
                     body_observer=observe)
    closed = closing(graph, preflight, query=query, compare_current=True,
                     body_observer=observe)
    result = assemble_boundary_metrics(collector, baseline, boundaries)
    result["boundary_source_identities"] = [
        row for row in opened["pages"] + closed["pages"]
        if row["page_sequence"] in BOUNDARY_PAGES]
    result["opening_layout"] = layout["layout"]
    result["closing_scope"] = "SIX_LITERAL_SEAMS_AND_CURRENT_LAYOUT_VERIFIED"
    return result
