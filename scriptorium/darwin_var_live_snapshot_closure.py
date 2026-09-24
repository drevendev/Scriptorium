"""Freeze a source-free observed-live dependency closure for Darwin/Rachinsky ``{{ВАР}}``.

This contract follows the independently reviewed provider-drift guard. It binds the
exact revision IDs observed for the template root and the load-time Lua closure used by
the retained Darwin mainspace path, while failing closed because MediaWiki revision
SHA-1 identities could not be retrieved from the provider API in this execution
environment. It does not claim historical transclusion, a full Scribunto replay, or a
render-profile promotion.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence


EVIDENCE_VERSION = "scriptorium-darwin-var-live-snapshot-closure-v1"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
PRIOR_VERSION = "scriptorium-darwin-var-provider-drift-evidence-v1"
PRIOR_SHA256 = "6126adbc966c7120ca487fb940bd0e01aafa0d7350d332e6422edbf8b3846cb8"
RESEARCH_DATE = "2026-09-24"
CANDIDATE_TITLE = "О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)"

RESOURCES = (
    ("Шаблон:ВАР", 3684602, "2019-06-04", "template_root", ("Модуль:Дореформенная орфография",)),
    ("Модуль:Дореформенная орфография", 5721277, "2026-06-08", "implementation_module", ("Module:Header",)),
    ("Module:Header", 5746249, "2026-09-10", "title_classifier", ("Module:BEED", "Module:Util")),
    ("Module:BEED", 5746253, "2026-09-10", "header_load_dependency", ("Module:RomanNumber",)),
    ("Module:Util", 5750249, "2026-09-18", "header_load_dependency", ()),
    ("Module:RomanNumber", 3684553, "2019-06-04", "beed_load_dependency", ()),
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _validate_prior(prior: Mapping[str, object]) -> None:
    if prior.get("schema_version") != PRIOR_VERSION:
        raise ValueError("Darwin VAR provider-drift evidence schema drift")
    if prior.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin VAR provider-drift evidence candidate drift")
    if prior.get("evidence_sha256") != PRIOR_SHA256:
        raise ValueError("Darwin VAR provider-drift evidence digest drift")
    unsigned = dict(prior)
    stored = unsigned.pop("evidence_sha256", None)
    if _sha256_json(unsigned) != stored:
        raise ValueError("Darwin VAR provider-drift evidence self-digest drift")


def build_evidence(prior: Mapping[str, object]) -> dict[str, object]:
    """Build the deterministic source-free live-snapshot closure contract."""

    _validate_prior(prior)
    resources = [
        {
            "title": title,
            "revision_id": revision_id,
            "revision_date": revision_date,
            "role": role,
            "loads": list(loads),
            "mediawiki_sha1": None,
        }
        for title, revision_id, revision_date, role, loads in RESOURCES
    ]
    evidence: dict[str, object] = {
        "schema_version": EVIDENCE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "researched_on": RESEARCH_DATE,
        "prior_evidence": {
            "schema_version": PRIOR_VERSION,
            "evidence_sha256": PRIOR_SHA256,
        },
        "snapshot": {
            "provider": "Russian Wikisource",
            "kind": "observed_live_snapshot",
            "observed_on": RESEARCH_DATE,
            "historical_transclusion_proven": False,
            "resources": resources,
        },
        "execution_boundary": {
            "candidate_title": CANDIDATE_TITLE,
            "path": (
                "Шаблон:ВАР -> Модуль:Дореформенная орфография.variative -> "
                'Module:Header.parse_title(..., "isPRS")'
            ),
            "expected_classification_isPRS": False,
            "selected_argument_if_replayed": "second_parameter_modern",
            "load_time_closure_complete_by_source_inspection": True,
            "latent_not_reached": [
                "Module:Header/Data via mw.loadData inside Header.data()",
                "Module:BEED/scans via mw.loadData inside BEED scan helpers",
                "Module:BEED/lists via mw.loadData inside BEED list helpers",
                "Модуль:Math via require inside BEED.duplicate()",
                "Модуль:Отексте/ЭСБЕ via mw.loadData inside BEED.duplicate()",
            ],
        },
        "identity_gate": {
            "revision_ids_complete": True,
            "mediawiki_sha1_complete": False,
            "missing_mediawiki_sha1_titles": [item["title"] for item in resources],
            "provider_api_attempted": True,
            "provider_api_result": "unavailable_from_execution_environment",
            "replay_ready": False,
            "reason": (
                "revision IDs and observed load-time topology are bound, but MediaWiki "
                "SHA-1 identities were not retrievable; exact replay remains fail-closed"
            ),
        },
        "promotion_decision": {
            "full_var_candidate_branch_replayed": False,
            "render_profile_rule_promoted": False,
            "backlog_item_removed": False,
            "effective_backlog_changed": False,
            "var_invocations_unresolved": 388,
            "next_evidence_required": (
                "obtain MediaWiki SHA-1 for the exact six-revision snapshot, then perform "
                "a separately bounded full candidate invocation replay"
            ),
        },
        "renderer_semantics_complete": False,
        "renderer_implementation_ready": False,
        "offline_version_pinned_runtime_proven": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }
    evidence["evidence_sha256"] = _sha256_json(evidence)
    return evidence


def validate_evidence(evidence: Mapping[str, object], prior: Mapping[str, object]) -> None:
    expected = build_evidence(prior)
    if dict(evidence) != expected:
        raise ValueError("Darwin VAR live-snapshot closure evidence drift")
    gate = evidence.get("identity_gate")
    if not isinstance(gate, dict):
        raise ValueError("identity gate missing")
    if gate.get("revision_ids_complete") is not True:
        raise ValueError("revision IDs must be complete")
    if gate.get("mediawiki_sha1_complete") is not False or gate.get("replay_ready") is not False:
        raise ValueError("SHA-1/replay gates must remain closed")
    snapshot = evidence.get("snapshot")
    if not isinstance(snapshot, dict) or snapshot.get("historical_transclusion_proven") is not False:
        raise ValueError("historical transclusion must remain unproven")
    decision = evidence.get("promotion_decision")
    if not isinstance(decision, dict):
        raise ValueError("promotion decision missing")
    for key in ("full_var_candidate_branch_replayed", "render_profile_rule_promoted", "backlog_item_removed", "effective_backlog_changed"):
        if decision.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    for key in ("renderer_semantics_complete", "renderer_implementation_ready", "offline_version_pinned_runtime_proven", "literary_body_count_and_digests_frozen", "minimum_300k_proved", "m2_parity_admissible"):
        if evidence.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if evidence.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prior", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    prior = json.loads(args.prior.read_text(encoding="utf-8"))
    if not isinstance(prior, dict):
        raise ValueError("Darwin VAR provider-drift evidence must be a JSON object")
    evidence = build_evidence(prior)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(evidence["evidence_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
