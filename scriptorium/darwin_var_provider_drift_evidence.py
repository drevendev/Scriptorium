"""Freeze a source-free provider-drift guard for Darwin/Rachinsky ``{{ВАР}}``.

The preceding VAR documentation unit pinned the documentation and implementation
module but intentionally left ``Module:Header`` and the live template root
unbound. Fresh provider evidence shows that Header changed after the pinned VAR
module and that Wikisource editors raised a possible VAR breakage in September
2026. This module records that drift boundary and replays only the deterministic
``parse_title(..., "isPRS")`` classification needed by the retained Darwin
mainspace title. It does not promote VAR or claim a complete MediaWiki runtime.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence


EVIDENCE_VERSION = "scriptorium-darwin-var-provider-drift-evidence-v1"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
PRIOR_EVIDENCE_VERSION = "scriptorium-darwin-var-documentation-evidence-v1"
PRIOR_EVIDENCE_SHA256 = "321ced32bb7ffc75829b6fbb5255bce3243641a80c21ad4e2b7bb7a25138502d"
CANDIDATE_MAINSPACE_TITLE = "О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)"
DOCUMENTATION_REVISION_ID = 5711068
VAR_MODULE_REVISION_ID = 5721277
OBSERVED_HEADER_REVISION_ID = 5746249
OBSERVED_HEADER_EDIT_DATE = "2026-09-10"
RESEARCH_DATE = "2026-09-24"
WIKISOURCE_FORUM_URL = "https://ru.wikisource.org/wiki/Викитека:Форум"


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def parse_title_is_prs(title: str) -> bool:
    """Replay the Header@5746249 isPRS rule for ordinary edition-style titles.

    The retained Darwin title follows Header's ordinary slash-separated path, so
    this helper intentionally implements only the branch exercised by that
    candidate and fails closed for malformed input.
    """

    if not isinstance(title, str) or not title or "/" not in title:
        raise ValueError("candidate title must be a slash-separated mainspace title")
    _root, name = title.split("/", 1)
    if not name:
        raise ValueError("candidate edition segment missing")
    if "/" in name:
        edition, _subpages = name.split("/", 1)
        subpages1 = name
    else:
        edition = name
        subpages1 = name
    return (
        edition == "ДО"
        or edition.endswith(" (ДО)")
        or subpages1.endswith("/ДО")
    )


def _validate_prior(prior: Mapping[str, object]) -> None:
    if prior.get("schema_version") != PRIOR_EVIDENCE_VERSION:
        raise ValueError("Darwin VAR prior evidence schema drift")
    if prior.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin VAR prior evidence candidate drift")
    if prior.get("evidence_sha256") != PRIOR_EVIDENCE_SHA256:
        raise ValueError("Darwin VAR prior evidence digest drift")
    unsigned = dict(prior)
    stored = unsigned.pop("evidence_sha256", None)
    if _sha256_json(unsigned) != stored:
        raise ValueError("Darwin VAR prior evidence self-digest drift")


def build_evidence(prior: Mapping[str, object]) -> dict[str, object]:
    """Build deterministic source-free provider-drift evidence."""

    _validate_prior(prior)
    is_prs = parse_title_is_prs(CANDIDATE_MAINSPACE_TITLE)

    evidence: dict[str, object] = {
        "schema_version": EVIDENCE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "researched_on": RESEARCH_DATE,
        "prior_evidence": {
            "schema_version": PRIOR_EVIDENCE_VERSION,
            "evidence_sha256": PRIOR_EVIDENCE_SHA256,
            "documentation_revision_id": DOCUMENTATION_REVISION_ID,
            "implementation_module_revision_id": VAR_MODULE_REVISION_ID,
        },
        "provider_drift_observation": {
            "provider": "Russian Wikisource",
            "observed_header": {
                "title": "Модуль:Header",
                "revision_id": OBSERVED_HEADER_REVISION_ID,
                "revision_date": OBSERVED_HEADER_EDIT_DATE,
                "permanent_url": (
                    "https://ru.wikisource.org/w/index.php?"
                    f"title=Модуль:Header&oldid={OBSERVED_HEADER_REVISION_ID}"
                ),
                "relationship_to_pinned_var_module": "later_revision",
            },
            "community_warning": {
                "forum_url": WIKISOURCE_FORUM_URL,
                "discussion_date": "2026-09-08",
                "observation": (
                    "Wikisource editors explicitly raised whether template VAR had "
                    "broken after Header-related changes and noted that the small "
                    "pre-reform module delegates page-title parsing to Header."
                ),
                "claim_scope": "provider_drift_risk_not_a_proven_runtime_failure",
            },
            "decision_effect": (
                "do_not_silently_bind_a_future_live_Header_as_replay_equivalence; "
                "select_and_record_an_explicit_coherent_snapshot_before_full_VAR_replay"
            ),
        },
        "observed_header_rule_replay": {
            "header_revision_id": OBSERVED_HEADER_REVISION_ID,
            "function": 'parse_title(..., "isPRS")',
            "candidate_title": CANDIDATE_MAINSPACE_TITLE,
            "candidate_namespace": "mainspace",
            "edition_segment": "1864 (ВТ:Ё)",
            "isPRS": is_prs,
            "selected_variant_if_module_branch_is_reached": (
                "second_parameter_modern" if not is_prs else "first_parameter_pre_reform"
            ),
            "scope": (
                "deterministic_replay_of_the_observed_Header_title_classification_rule_only"
            ),
        },
        "dependency_boundary": {
            "template_root_revision_frozen": False,
            "implementation_module_revision_frozen_for_this_chain": True,
            "module_header_revision_observed": True,
            "module_header_mediawiki_sha1_frozen": False,
            "nested_dependency_closure_frozen": False,
            "offline_version_pinned_runtime_proven": False,
            "historical_transclusion_proven": False,
            "full_var_candidate_branch_replayed": False,
            "reason": (
                "the Header revision and title-classification rule are observed, but "
                "the live template root, Header SHA-1 and complete replay-time closure "
                "are not yet bound into one executable snapshot"
            ),
        },
        "promotion_decision": {
            "render_profile_rule_promoted": False,
            "backlog_item_removed": False,
            "effective_backlog_changed": False,
            "reason": (
                "provider drift evidence narrows snapshot selection but does not prove "
                "a complete deterministic VAR invocation replay"
            ),
            "next_evidence_required": (
                "choose one explicit coherent replay snapshot, freeze exact Шаблон:ВАР "
                "plus Модуль:Дореформенная орфография plus Module:Header identities "
                "including MediaWiki SHA-1 and the execution-relevant nested closure, "
                "then replay the candidate mainspace invocation without substituting "
                "later live descendants"
            ),
        },
        "renderer_semantics_complete": False,
        "renderer_implementation_ready": False,
        "inter_page_composition_frozen": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "admitted_for_calibration": False,
        "fantlab_source_edition_match": "unknown",
        "diagnostic_ready": False,
        "m2_parity_admissible": False,
    }
    evidence["evidence_sha256"] = _sha256_json(evidence)
    return evidence


def validate_evidence(
    evidence: Mapping[str, object],
    prior: Mapping[str, object],
) -> None:
    expected = build_evidence(prior)
    if dict(evidence) != expected:
        raise ValueError("Darwin VAR provider-drift evidence drift")
    replay = evidence.get("observed_header_rule_replay")
    if not isinstance(replay, dict) or replay.get("isPRS") is not False:
        raise ValueError("Darwin mainspace title must classify as isPRS=false")
    if replay.get("selected_variant_if_module_branch_is_reached") != "second_parameter_modern":
        raise ValueError("Darwin observed Header branch must select modern VAR argument")
    boundary = evidence.get("dependency_boundary")
    if not isinstance(boundary, dict):
        raise ValueError("Darwin VAR dependency boundary missing")
    for key in (
        "template_root_revision_frozen",
        "module_header_mediawiki_sha1_frozen",
        "nested_dependency_closure_frozen",
        "offline_version_pinned_runtime_proven",
        "historical_transclusion_proven",
        "full_var_candidate_branch_replayed",
    ):
        if boundary.get(key) is not False:
            raise ValueError(f"{key} must remain false in provider-drift evidence")
    decision = evidence.get("promotion_decision")
    if (
        not isinstance(decision, dict)
        or decision.get("render_profile_rule_promoted") is not False
        or decision.get("backlog_item_removed") is not False
        or decision.get("effective_backlog_changed") is not False
    ):
        raise ValueError("Darwin VAR promotion must remain closed")
    for key in (
        "renderer_semantics_complete",
        "renderer_implementation_ready",
        "inter_page_composition_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    ):
        if evidence.get(key) is not False:
            raise ValueError(f"{key} must remain false in provider-drift evidence")
    if evidence.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")
    forbidden = {"wikitext", "content", "body", "text", "source_text", "rendered_prose"}
    if forbidden.intersection(evidence):
        raise ValueError("source prose leaked into Darwin VAR provider-drift evidence")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prior", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    prior = json.loads(args.prior.read_text(encoding="utf-8"))
    if not isinstance(prior, dict):
        raise ValueError("Darwin VAR prior evidence must be a JSON object")
    evidence = build_evidence(prior)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(evidence["evidence_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
