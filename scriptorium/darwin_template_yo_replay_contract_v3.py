"""Bind exact source-free root identities for Darwin/Rachinsky ``{{ё}}`` replay.

Version 3 is deliberately a narrow successor to the independently reviewed v2 replay
contract. It binds the two canonical Russian Wikisource root revisions by exact
revision timestamp and MediaWiki SHA-1, but it does not claim recursive dependency
closure, deterministic template expansion, renderer equivalence, literary-body
identity, corpus admission, or FantLab parity.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from .darwin_template_yo_replay_contract import (
    validate_contract as validate_v2_contract,
    validate_dependency_closure,
)


CONTRACT_VERSION = "scriptorium-darwin-template-yo-replay-contract-v3"
PREDECESSOR_VERSION = "scriptorium-darwin-template-yo-replay-contract-v2"
PREDECESSOR_SHA256 = "9b2e8914a5b4c3518ef331c27dc09a6a30d4d6433e90169c677348048f3dcd52"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
RESEARCH_DATE = "2026-09-22"
ROOT_IDENTITIES: tuple[dict[str, object], ...] = (
    {
        "title": "Шаблон:Ё",
        "revision_id": 5687302,
        "revision_timestamp": "2026-01-21T12:32:10Z",
        "mediawiki_sha1": "963c1796d693d5451cf0c0897c35bd7e5b327ae1",
    },
    {
        "title": "Шаблон:ЕЁ",
        "revision_id": 3684646,
        "revision_timestamp": "2019-06-04T20:49:40Z",
        "mediawiki_sha1": "435bb2a412d8fb5962ccd5adc0ac2e03412fe109",
    },
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _load_object(path: Path, *, label: str) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Darwin {{ё}} {label} must be a JSON object")
    return value


def build_contract(
    evidence: Mapping[str, object],
    predecessor: Mapping[str, object],
) -> dict[str, object]:
    """Promote only exact root revision identity while preserving all open gates."""

    validate_v2_contract(predecessor, evidence)
    if predecessor.get("schema_version") != PREDECESSOR_VERSION:
        raise ValueError("Darwin {{ё}} replay predecessor schema drift")
    if predecessor.get("contract_sha256") != PREDECESSOR_SHA256:
        raise ValueError("Darwin {{ё}} replay predecessor digest drift")
    if predecessor.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin {{ё}} replay predecessor candidate drift")

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
    api["revision_identity_query"] = {
        "provider": "Russian Wikisource Action API",
        "endpoint": "https://ru.wikisource.org/w/api.php",
        "query_mode": "revids",
        "rvprop": "ids|timestamp|sha1",
        "source_content_requested": False,
        "sha1_encoding": "base16",
        "researched_on": RESEARCH_DATE,
    }

    predecessor_observations = contract.get("root_title_observations")
    if not isinstance(predecessor_observations, list) or len(predecessor_observations) != 2:
        raise ValueError("Darwin {{ё}} predecessor root observations missing")
    by_title = {
        str(row.get("canonical_title")): row
        for row in predecessor_observations
        if isinstance(row, dict)
    }
    promoted_observations: list[dict[str, object]] = []
    for identity in ROOT_IDENTITIES:
        title = str(identity["title"])
        prior = by_title.get(title)
        if not isinstance(prior, dict):
            raise ValueError("Darwin {{ё}} canonical predecessor root observation missing")
        if prior.get("revision_id") != identity["revision_id"]:
            raise ValueError("Darwin {{ё}} root revision identity drift")
        promoted = deepcopy(prior)
        promoted["revision_timestamp"] = identity["revision_timestamp"]
        promoted["mediawiki_sha1"] = identity["mediawiki_sha1"]
        promoted["mediawiki_sha1_bound"] = True
        promoted_observations.append(promoted)
    contract["root_title_observations"] = promoted_observations

    dependencies = [dict(row) for row in ROOT_IDENTITIES]
    validate_dependency_closure(dependencies, [], require_complete=False)
    replay = contract.get("replay_contract")
    if not isinstance(replay, dict):
        raise ValueError("Darwin {{ё}} replay contract body missing")
    replay["root_identities_bound"] = True
    replay["dependencies"] = dependencies
    replay["edges"] = []
    replay["dependency_closure_complete"] = False

    contract["promotion_decision"] = {
        "render_profile_rule_promoted": False,
        "backlog_item_removed": False,
        "reason": (
            "the two canonical root revisions now have exact source-free MediaWiki content identities, "
            "but their direct dependencies have not yet been enumerated with complete per-node discovery "
            "proof and the recursive dependency graph remains open, so deterministic replay equivalence "
            "is not yet demonstrated"
        ),
        "next_evidence_required": (
            "discover and bind the exact direct dependencies of Шаблон:Ё and Шаблон:ЕЁ, recursively bind "
            "every nested template/module revision with MediaWiki content SHA-1 plus complete source-free "
            "discovery evidence, close the graph edges exactly, and then verify deterministic forced and "
            "non-forced outputs before promotion"
        ),
    }

    contract["contract_sha256"] = _sha256_json(contract)
    return contract


def validate_contract(
    contract: Mapping[str, object],
    evidence: Mapping[str, object],
    predecessor: Mapping[str, object],
) -> None:
    expected = build_contract(evidence, predecessor)
    if dict(contract) != expected:
        raise ValueError("Darwin {{ё}} replay v3 contract drift")
    if contract.get("source_text_included") is not False:
        raise ValueError("Darwin {{ё}} replay v3 contract must remain source-free")

    observations = contract.get("root_title_observations")
    if not isinstance(observations, list) or len(observations) != len(ROOT_IDENTITIES):
        raise ValueError("Darwin {{ё}} exact root observations missing")
    for observation, identity in zip(observations, ROOT_IDENTITIES, strict=True):
        if observation.get("canonical_title") != identity["title"]:
            raise ValueError("Darwin {{ё}} canonical root title drift")
        if observation.get("revision_id") != identity["revision_id"]:
            raise ValueError("Darwin {{ё}} root revision id drift")
        if observation.get("revision_timestamp") != identity["revision_timestamp"]:
            raise ValueError("Darwin {{ё}} root revision timestamp drift")
        if observation.get("mediawiki_sha1") != identity["mediawiki_sha1"]:
            raise ValueError("Darwin {{ё}} root MediaWiki SHA-1 drift")
        if observation.get("mediawiki_sha1_bound") is not True:
            raise ValueError("Darwin {{ё}} root MediaWiki SHA-1 must be bound")

    replay = contract.get("replay_contract")
    if not isinstance(replay, dict):
        raise ValueError("Darwin {{ё}} replay v3 body missing")
    dependencies = replay.get("dependencies")
    edges = replay.get("edges")
    if dependencies != [dict(row) for row in ROOT_IDENTITIES] or edges != []:
        raise ValueError("Darwin {{ё}} exact root dependency surface drift")
    validate_dependency_closure(dependencies, edges, require_complete=False)
    if replay.get("root_identities_bound") is not True:
        raise ValueError("Darwin {{ё}} root identity binding gate drift")
    if replay.get("dependency_closure_complete") is not False:
        raise ValueError("Darwin {{ё}} recursive dependency closure must remain open")

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
            raise ValueError(f"{key} must remain false in Darwin {{ё}} replay v3 contract")
    if contract.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")


def build_contract_from_paths(evidence_path: Path, predecessor_path: Path) -> dict[str, object]:
    evidence = _load_object(evidence_path, label="evidence input")
    predecessor = _load_object(predecessor_path, label="predecessor contract")
    return build_contract(evidence, predecessor)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--predecessor-contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    contract = build_contract_from_paths(args.evidence, args.predecessor_contract)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(contract["contract_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
