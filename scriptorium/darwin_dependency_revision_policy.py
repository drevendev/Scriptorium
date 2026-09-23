"""Validate the source-free Darwin/Rachinsky dependency revision-selection policy."""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence


POLICY_VERSION = "scriptorium-darwin-dependency-revision-selection-policy-v1"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
BOUND_CONTRACT_VERSION = "scriptorium-darwin-template-yo-replay-contract-v4"
BOUND_CONTRACT_SHA256 = "f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64"
POLICY_SHA256 = "4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855"
REQUIRED_BINDING_FIELDS = [
    "canonical_title",
    "revision_id",
    "revision_timestamp",
    "mediawiki_sha1",
    "observation_context",
]


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def policy_sha256(policy: Mapping[str, object]) -> str:
    payload = deepcopy(dict(policy))
    payload.pop("policy_sha256", None)
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Darwin dependency revision-selection policy must be a JSON object")
    return value


def validate_policy(policy: Mapping[str, object], predecessor: Mapping[str, object]) -> None:
    if policy.get("schema_version") != POLICY_VERSION:
        raise ValueError("Darwin dependency revision-selection policy schema drift")
    if policy.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin dependency revision-selection candidate drift")
    if policy.get("policy_sha256") != POLICY_SHA256 or policy_sha256(policy) != POLICY_SHA256:
        raise ValueError("Darwin dependency revision-selection policy digest drift")
    if policy.get("source_text_included") is not False:
        raise ValueError("Darwin dependency revision-selection policy must remain source-free")

    bound = policy.get("bound_replay_contract")
    if not isinstance(bound, dict):
        raise ValueError("Darwin dependency revision-selection predecessor binding missing")
    if bound != {
        "schema_version": BOUND_CONTRACT_VERSION,
        "contract_sha256": BOUND_CONTRACT_SHA256,
    }:
        raise ValueError("Darwin dependency revision-selection predecessor binding drift")
    if predecessor.get("schema_version") != BOUND_CONTRACT_VERSION:
        raise ValueError("Darwin dependency revision-selection predecessor schema drift")
    if predecessor.get("contract_sha256") != BOUND_CONTRACT_SHA256:
        raise ValueError("Darwin dependency revision-selection predecessor digest drift")
    replay = predecessor.get("replay_contract")
    if not isinstance(replay, dict) or replay.get("discovered_unbound_dependencies") != ["Модуль:String"]:
        raise ValueError("Darwin dependency revision-selection unbound dependency drift")
    if replay.get("dependency_closure_complete") is not False:
        raise ValueError("Darwin dependency revision-selection predecessor unexpectedly closed")

    decision = policy.get("decision")
    if not isinstance(decision, dict):
        raise ValueError("Darwin dependency revision-selection decision missing")
    for key in (
        "caller_revision_timestamp_selects_dependency_revision",
        "expandtemplates_revid_pins_transcluded_dependency_revisions",
        "historical_dependency_revision_inference_allowed",
    ):
        if decision.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if decision.get("required_binding_fields") != REQUIRED_BINDING_FIELDS:
        raise ValueError("Darwin dependency revision-selection binding fields drift")
    method = decision.get("required_binding_method")
    if not isinstance(method, str) or "controlled replay snapshot" not in method or "never backdate" not in method:
        raise ValueError("Darwin dependency revision-selection binding method drift")

    evidence = policy.get("evidence")
    if not isinstance(evidence, list) or len(evidence) != 3:
        raise ValueError("Darwin dependency revision-selection evidence set drift")
    urls = {row.get("url") for row in evidence if isinstance(row, dict)}
    if urls != {
        "https://www.mediawiki.org/wiki/Help:Templates",
        "https://www.mediawiki.org/wiki/API:Expandtemplates/en",
        "https://phabricator.wikimedia.org/T31051",
    }:
        raise ValueError("Darwin dependency revision-selection evidence URLs drift")

    gates = policy.get("gates")
    if not isinstance(gates, dict):
        raise ValueError("Darwin dependency revision-selection gates missing")
    for key in (
        "module_string_identity_bound",
        "dependency_closure_complete",
        "outputs_verified",
        "render_profile_rule_promoted",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "m2_parity_admissible",
    ):
        if gates.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if gates.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--predecessor-contract", type=Path, required=True)
    args = parser.parse_args(argv)
    policy = load_object(args.policy)
    predecessor = load_object(args.predecessor_contract)
    validate_policy(policy, predecessor)
    print(policy["policy_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
