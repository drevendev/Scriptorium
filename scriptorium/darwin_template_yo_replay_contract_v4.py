"""Freeze source-free direct-dependency discovery for Darwin/Rachinsky ``{{ё}}`` roots.

Version 4 is a narrow successor to the independently reviewed v3 root-identity
contract. It binds complete direct-dependency discovery evidence for the two exact root
revisions, while deliberately keeping recursive closure and every downstream renderer,
body, FantLab and parity gate open.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from .darwin_template_dependency_scan import (
    DOCUMENTED_BARE_MAGIC_WORDS,
    MAGIC_WORD_EVIDENCE_REVISION_DATE,
    MAGIC_WORD_EVIDENCE_REVISION_ID,
    MAGIC_WORD_EVIDENCE_TITLE,
    MAGIC_WORD_EVIDENCE_URL,
    SCAN_METHOD,
)
from .darwin_template_yo_replay_contract import (
    dependency_discovery_evidence_sha256,
    validate_dependency_closure,
)
from .darwin_template_yo_replay_contract_v3 import validate_contract as validate_v3_contract


CONTRACT_VERSION = "scriptorium-darwin-template-yo-replay-contract-v4"
PREDECESSOR_VERSION = "scriptorium-darwin-template-yo-replay-contract-v3"
PREDECESSOR_SHA256 = "8caa144d9f4c0b9a8149c1822bd79d168d212dea14d72079c3259d55e5e03c8c"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
RESEARCH_DATE = "2026-09-23"
ROOT_SCAN_OBSERVATIONS: tuple[dict[str, object], ...] = (
    {
        "title": "Шаблон:Ё",
        "revision_id": 5687302,
        "revision_timestamp": "2026-01-21T12:32:10Z",
        "mediawiki_sha1": "963c1796d693d5451cf0c0897c35bd7e5b327ae1",
        "source_utf8_bytes": 271,
        "transclusion_sha256": "bd7465151d984f06c75eae0c1246c26a0643826a26a170a3e9a9d43c9e5a03b7",
        "redirect_target": None,
        "direct_dependencies": ["Шаблон:ЕЁ"],
    },
    {
        "title": "Шаблон:ЕЁ",
        "revision_id": 3684646,
        "revision_timestamp": "2019-06-04T20:49:40Z",
        "mediawiki_sha1": "435bb2a412d8fb5962ccd5adc0ac2e03412fe109",
        "source_utf8_bytes": 688,
        "transclusion_sha256": "3975fa227e23e8cc1487a49a3eab86b28e0ddb6a753c347c3191ee800ae56026",
        "redirect_target": None,
        "direct_dependencies": ["Модуль:String"],
    },
)
BOUND_ROOT_EDGE = {"from": "Шаблон:Ё", "to": "Шаблон:ЕЁ"}


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _load_object(path: Path, *, label: str) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Darwin {{ё}} {label} must be a JSON object")
    return value


def _identity(row: Mapping[str, object]) -> dict[str, object]:
    return {
        key: row[key]
        for key in ("title", "revision_id", "revision_timestamp", "mediawiki_sha1")
    }


def _discovery_row(observation: Mapping[str, object]) -> dict[str, object]:
    row = _identity(observation)
    row["discovery"] = {
        "status": "complete",
        "method": SCAN_METHOD,
        "direct_dependencies": list(observation["direct_dependencies"]),
        "evidence_sha256": "0" * 64,
    }
    row["discovery"]["evidence_sha256"] = dependency_discovery_evidence_sha256(row)
    return row


def build_contract(
    evidence: Mapping[str, object],
    v2_predecessor: Mapping[str, object],
    predecessor: Mapping[str, object],
) -> dict[str, object]:
    """Promote only complete direct-dependency discovery for the already-bound roots."""

    validate_v3_contract(predecessor, evidence, v2_predecessor)
    if predecessor.get("schema_version") != PREDECESSOR_VERSION:
        raise ValueError("Darwin {{ё}} replay v4 predecessor schema drift")
    if predecessor.get("contract_sha256") != PREDECESSOR_SHA256:
        raise ValueError("Darwin {{ё}} replay v4 predecessor digest drift")
    if predecessor.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin {{ё}} replay v4 predecessor candidate drift")

    replay = predecessor.get("replay_contract")
    if not isinstance(replay, dict):
        raise ValueError("Darwin {{ё}} replay v3 body missing")
    prior_dependencies = replay.get("dependencies")
    if not isinstance(prior_dependencies, list):
        raise ValueError("Darwin {{ё}} replay v3 dependencies missing")
    if [_identity(row) for row in ROOT_SCAN_OBSERVATIONS] != prior_dependencies:
        raise ValueError("Darwin {{ё}} exact root identities drift before discovery promotion")

    contract = deepcopy(dict(predecessor))
    contract.pop("contract_sha256", None)
    contract["schema_version"] = CONTRACT_VERSION
    contract["predecessor_contract"] = {
        "schema_version": PREDECESSOR_VERSION,
        "contract_sha256": PREDECESSOR_SHA256,
    }

    api = contract.get("official_api_evidence")
    if not isinstance(api, dict):
        raise ValueError("Darwin {{ё}} official API evidence missing")
    api["direct_dependency_scan"] = {
        "provider": "Russian Wikisource Action API",
        "endpoint": "https://ru.wikisource.org/w/api.php",
        "query_mode": "revids",
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
        "source_content_used_transiently": True,
        "source_content_retained": False,
        "scan_method": SCAN_METHOD,
        "researched_on": RESEARCH_DATE,
    }
    api["magic_word_classification"] = {
        "provider": "MediaWiki.org",
        "title": MAGIC_WORD_EVIDENCE_TITLE,
        "revision_id": MAGIC_WORD_EVIDENCE_REVISION_ID,
        "revision_date": MAGIC_WORD_EVIDENCE_REVISION_DATE,
        "permanent_url": MAGIC_WORD_EVIDENCE_URL,
        "researched_on": RESEARCH_DATE,
        "documented_bare_variables": list(DOCUMENTED_BARE_MAGIC_WORDS),
        "template_name_conflict_variable_wins_by_default": True,
        "parameters_can_force_template_transclusion": True,
        "scanner_policy": (
            "ignore only listed bare variables without parameters; fail closed on parameterized "
            "or unclassified uppercase invocations"
        ),
    }

    dependencies = [_discovery_row(row) for row in ROOT_SCAN_OBSERVATIONS]
    bound_edges = [dict(BOUND_ROOT_EDGE)]
    validate_dependency_closure(dependencies, bound_edges, require_complete=False)
    current_replay = contract.get("replay_contract")
    if not isinstance(current_replay, dict):
        raise ValueError("Darwin {{ё}} replay v4 body missing")
    current_replay["dependencies"] = dependencies
    current_replay["edges"] = bound_edges
    current_replay["root_direct_dependency_discovery_complete"] = True
    current_replay["discovered_unbound_dependencies"] = ["Модуль:String"]
    current_replay["dependency_closure_complete"] = False

    contract["direct_dependency_discovery"] = {
        "scan_method": SCAN_METHOD,
        "source_text_retained": False,
        "root_observations": [
            {
                "title": row["title"],
                "revision_id": row["revision_id"],
                "source_utf8_bytes": row["source_utf8_bytes"],
                "source_sha1": row["mediawiki_sha1"],
                "transclusion_sha256": row["transclusion_sha256"],
                "redirect_target": row["redirect_target"],
                "direct_dependencies": list(row["direct_dependencies"]),
            }
            for row in ROOT_SCAN_OBSERVATIONS
        ],
        "discovered_edges": [
            {
                "from": "Шаблон:Ё",
                "to": "Шаблон:ЕЁ",
                "target_identity_bound": True,
            },
            {
                "from": "Шаблон:ЕЁ",
                "to": "Модуль:String",
                "target_identity_bound": False,
            },
        ],
    }

    contract["promotion_decision"] = {
        "render_profile_rule_promoted": False,
        "backlog_item_removed": False,
        "reason": (
            "complete source-free direct-dependency discovery is frozen for both exact roots and "
            "the bound Шаблон:Ё -> Шаблон:ЕЁ edge is explicit, but Шаблон:ЕЁ discovers "
            "Модуль:String whose exact revision identity and own direct dependencies are not yet "
            "bound, so recursive replay closure remains open"
        ),
        "next_evidence_required": (
            "bind an exact replay revision identity for Модуль:String, freeze complete direct-dependency "
            "discovery for that exact module revision and every further descendant, close the bound graph, "
            "then verify deterministic forced and non-forced outputs before promotion"
        ),
    }

    contract["contract_sha256"] = _sha256_json(contract)
    return contract


def validate_contract(
    contract: Mapping[str, object],
    evidence: Mapping[str, object],
    v2_predecessor: Mapping[str, object],
    predecessor: Mapping[str, object],
) -> None:
    expected = build_contract(evidence, v2_predecessor, predecessor)
    if dict(contract) != expected:
        raise ValueError("Darwin {{ё}} replay v4 contract drift")
    if contract.get("source_text_included") is not False:
        raise ValueError("Darwin {{ё}} replay v4 contract must remain source-free")

    discovery = contract.get("direct_dependency_discovery")
    if not isinstance(discovery, dict) or discovery.get("source_text_retained") is not False:
        raise ValueError("Darwin {{ё}} direct-dependency evidence must remain source-free")
    observations = discovery.get("root_observations")
    if not isinstance(observations, list) or len(observations) != len(ROOT_SCAN_OBSERVATIONS):
        raise ValueError("Darwin {{ё}} root scan observations missing")
    for actual, frozen in zip(observations, ROOT_SCAN_OBSERVATIONS, strict=True):
        if actual.get("title") != frozen["title"] or actual.get("revision_id") != frozen["revision_id"]:
            raise ValueError("Darwin {{ё}} root scan identity drift")
        if actual.get("source_sha1") != frozen["mediawiki_sha1"]:
            raise ValueError("Darwin {{ё}} root scan source SHA-1 drift")
        if actual.get("direct_dependencies") != frozen["direct_dependencies"]:
            raise ValueError("Darwin {{ё}} root direct-dependency drift")
        if {"content", "text", "wikitext", "body", "source_text"}.intersection(actual):
            raise ValueError("source/template prose leaked into Darwin {{ё}} root scan evidence")

    expected_discovered_edges = [
        {"from": "Шаблон:Ё", "to": "Шаблон:ЕЁ", "target_identity_bound": True},
        {"from": "Шаблон:ЕЁ", "to": "Модуль:String", "target_identity_bound": False},
    ]
    if discovery.get("discovered_edges") != expected_discovered_edges:
        raise ValueError("Darwin {{ё}} direct-dependency edge evidence drift")

    replay = contract.get("replay_contract")
    if not isinstance(replay, dict):
        raise ValueError("Darwin {{ё}} replay v4 body missing")
    dependencies = replay.get("dependencies")
    edges = replay.get("edges")
    if not isinstance(dependencies, list) or edges != [BOUND_ROOT_EDGE]:
        raise ValueError("Darwin {{ё}} partial replay graph drift")
    validate_dependency_closure(dependencies, edges, require_complete=False)
    if replay.get("root_direct_dependency_discovery_complete") is not True:
        raise ValueError("Darwin {{ё}} root direct-dependency discovery gate drift")
    if replay.get("discovered_unbound_dependencies") != ["Модуль:String"]:
        raise ValueError("Darwin {{ё}} unbound dependency set drift")
    if replay.get("dependency_closure_complete") is not False:
        raise ValueError("Darwin {{ё}} recursive dependency closure must remain open")
    try:
        validate_dependency_closure(dependencies, edges, require_complete=True)
    except ValueError as exc:
        if "discovered dependency remains unbound" not in str(exc):
            raise
    else:
        raise ValueError("Darwin {{ё}} recursive closure unexpectedly passed")

    mode = contract.get("mode_verification")
    if not isinstance(mode, dict) or mode.get("outputs_verified") is not False:
        raise ValueError("Darwin {{ё}} output verification must remain open")
    decision = contract.get("promotion_decision")
    if (
        not isinstance(decision, dict)
        or decision.get("render_profile_rule_promoted") is not False
        or decision.get("backlog_item_removed") is not False
    ):
        raise ValueError("Darwin {{ё}} replay promotion must remain closed")
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
        if contract.get(key) is not False:
            raise ValueError(f"{key} must remain false in Darwin {{ё}} replay v4 contract")
    if contract.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")


def build_contract_from_paths(
    evidence_path: Path,
    v2_predecessor_path: Path,
    predecessor_path: Path,
) -> dict[str, object]:
    evidence = _load_object(evidence_path, label="evidence input")
    v2_predecessor = _load_object(v2_predecessor_path, label="v2 predecessor contract")
    predecessor = _load_object(predecessor_path, label="v3 predecessor contract")
    return build_contract(evidence, v2_predecessor, predecessor)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--v2-predecessor-contract", type=Path, required=True)
    parser.add_argument("--predecessor-contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    contract = build_contract_from_paths(
        args.evidence,
        args.v2_predecessor_contract,
        args.predecessor_contract,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(contract["contract_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
