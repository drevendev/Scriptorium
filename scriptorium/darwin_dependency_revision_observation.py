"""Build and validate a source-free controlled revision observation for Darwin/Rachinsky replay."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Mapping, Sequence

SCHEMA_VERSION = "scriptorium-darwin-dependency-revision-observation-v1"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
DEPENDENCY_TITLE = "Модуль:String"
BOUND_CONTRACT_VERSION = "scriptorium-darwin-template-yo-replay-contract-v4"
BOUND_CONTRACT_SHA256 = "f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64"
BOUND_POLICY_VERSION = "scriptorium-darwin-dependency-revision-selection-policy-v1"
BOUND_POLICY_SHA256 = "4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855"
ENDPOINT = "https://ru.wikisource.org/w/api.php"
FORBIDDEN_SOURCE_KEYS = {"content", "text", "wikitext", "body", "source_text"}
_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def observation_sha256(observation: Mapping[str, object]) -> str:
    payload = deepcopy(dict(observation))
    payload.pop("observation_sha256", None)
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Darwin dependency revision observation input must be a JSON object")
    return value


def _parse_timestamp(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{label} must be an RFC3339 UTC timestamp")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{label} must be an RFC3339 UTC timestamp") from exc
    return value


def _assert_source_free(value: object, *, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_SOURCE_KEYS:
                raise ValueError(f"source content key {key!r} forbidden at {path}")
            _assert_source_free(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_source_free(child, path=f"{path}[{index}]")


def build_observation(api_response: Mapping[str, object]) -> dict[str, object]:
    observed_at = _parse_timestamp(api_response.get("curtimestamp"), label="curtimestamp")
    query = api_response.get("query")
    if not isinstance(query, dict):
        raise ValueError("MediaWiki query payload missing")
    pages = query.get("pages")
    if not isinstance(pages, list) or len(pages) != 1 or not isinstance(pages[0], dict):
        raise ValueError("expected exactly one MediaWiki page")
    page = pages[0]
    if page.get("title") != DEPENDENCY_TITLE:
        raise ValueError("canonical dependency title drift")
    revisions = page.get("revisions")
    if not isinstance(revisions, list) or len(revisions) != 1 or not isinstance(revisions[0], dict):
        raise ValueError("expected exactly one current dependency revision")
    revision = revisions[0]
    revision_id = revision.get("revid")
    if not isinstance(revision_id, int) or revision_id <= 0:
        raise ValueError("dependency revision ID missing")
    revision_timestamp = _parse_timestamp(revision.get("timestamp"), label="revision timestamp")
    mediawiki_sha1 = revision.get("sha1")
    if not isinstance(mediawiki_sha1, str) or not _SHA1_RE.fullmatch(mediawiki_sha1):
        raise ValueError("dependency MediaWiki SHA-1 missing or malformed")
    if any(key in revision for key in FORBIDDEN_SOURCE_KEYS) or "slots" in revision:
        raise ValueError("metadata-only dependency observation unexpectedly contains source content")

    observation: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": CANDIDATE_ID,
        "dependency_title": DEPENDENCY_TITLE,
        "bound_replay_contract": {
            "schema_version": BOUND_CONTRACT_VERSION,
            "contract_sha256": BOUND_CONTRACT_SHA256,
        },
        "bound_revision_selection_policy": {
            "schema_version": BOUND_POLICY_VERSION,
            "policy_sha256": BOUND_POLICY_SHA256,
        },
        "identity": {
            "canonical_title": DEPENDENCY_TITLE,
            "revision_id": revision_id,
            "revision_timestamp": revision_timestamp,
            "mediawiki_sha1": mediawiki_sha1,
        },
        "observation_context": {
            "provider": "Russian Wikisource Action API",
            "endpoint": ENDPOINT,
            "observed_at": observed_at,
            "selection": "current_revision_at_observation_time",
            "query": {
                "action": "query",
                "format": "json",
                "formatversion": 2,
                "curtimestamp": True,
                "prop": "revisions",
                "titles": DEPENDENCY_TITLE,
                "rvprop": "ids|timestamp|sha1",
                "rvlimit": 1,
                "source_content_requested": False,
            },
        },
        "gates": {
            "module_string_identity_observed": True,
            "module_string_identity_bound": False,
            "dependency_closure_complete": False,
            "outputs_verified": False,
            "render_profile_rule_promoted": False,
            "literary_body_count_and_digests_frozen": False,
            "minimum_300k_proved": False,
            "fantlab_source_edition_match": "unknown",
            "m2_parity_admissible": False,
        },
        "source_text_included": False,
    }
    observation["observation_sha256"] = observation_sha256(observation)
    return observation


def validate_observation(
    observation: Mapping[str, object],
    predecessor: Mapping[str, object],
    policy: Mapping[str, object],
) -> None:
    _assert_source_free(observation)
    if observation.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Darwin dependency revision observation schema drift")
    if observation.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin dependency revision observation candidate drift")
    if observation.get("dependency_title") != DEPENDENCY_TITLE:
        raise ValueError("Darwin dependency revision observation title drift")
    if observation.get("source_text_included") is not False:
        raise ValueError("Darwin dependency revision observation must remain source-free")
    digest = observation.get("observation_sha256")
    if not isinstance(digest, str) or len(digest) != 64 or observation_sha256(observation) != digest:
        raise ValueError("Darwin dependency revision observation digest drift")

    if predecessor.get("schema_version") != BOUND_CONTRACT_VERSION or predecessor.get("contract_sha256") != BOUND_CONTRACT_SHA256:
        raise ValueError("Darwin dependency revision observation predecessor drift")
    replay = predecessor.get("replay_contract")
    if not isinstance(replay, dict) or replay.get("discovered_unbound_dependencies") != [DEPENDENCY_TITLE]:
        raise ValueError("Darwin dependency revision observation predecessor unbound dependency drift")
    if replay.get("dependency_closure_complete") is not False:
        raise ValueError("Darwin dependency revision observation predecessor unexpectedly closed")

    if policy.get("schema_version") != BOUND_POLICY_VERSION or policy.get("policy_sha256") != BOUND_POLICY_SHA256:
        raise ValueError("Darwin dependency revision observation policy drift")
    decision = policy.get("decision")
    if not isinstance(decision, dict) or decision.get("historical_dependency_revision_inference_allowed") is not False:
        raise ValueError("Darwin dependency revision observation policy no longer fail-closed")
    if observation.get("bound_replay_contract") != {
        "schema_version": BOUND_CONTRACT_VERSION,
        "contract_sha256": BOUND_CONTRACT_SHA256,
    }:
        raise ValueError("Darwin dependency revision observation contract binding drift")
    if observation.get("bound_revision_selection_policy") != {
        "schema_version": BOUND_POLICY_VERSION,
        "policy_sha256": BOUND_POLICY_SHA256,
    }:
        raise ValueError("Darwin dependency revision observation policy binding drift")

    identity = observation.get("identity")
    if not isinstance(identity, dict) or set(identity) != {
        "canonical_title", "revision_id", "revision_timestamp", "mediawiki_sha1"
    }:
        raise ValueError("Darwin dependency revision observation identity fields drift")
    if identity.get("canonical_title") != DEPENDENCY_TITLE:
        raise ValueError("Darwin dependency revision observation canonical title drift")
    if not isinstance(identity.get("revision_id"), int) or identity["revision_id"] <= 0:
        raise ValueError("Darwin dependency revision observation revision ID drift")
    _parse_timestamp(identity.get("revision_timestamp"), label="revision timestamp")
    if not isinstance(identity.get("mediawiki_sha1"), str) or not _SHA1_RE.fullmatch(identity["mediawiki_sha1"]):
        raise ValueError("Darwin dependency revision observation SHA-1 drift")

    context = observation.get("observation_context")
    if not isinstance(context, dict):
        raise ValueError("Darwin dependency revision observation context missing")
    if context.get("provider") != "Russian Wikisource Action API" or context.get("endpoint") != ENDPOINT:
        raise ValueError("Darwin dependency revision observation provider drift")
    _parse_timestamp(context.get("observed_at"), label="observation timestamp")
    if context.get("selection") != "current_revision_at_observation_time":
        raise ValueError("Darwin dependency revision observation selection semantics drift")
    q = context.get("query")
    if not isinstance(q, dict) or q.get("titles") != DEPENDENCY_TITLE or q.get("rvprop") != "ids|timestamp|sha1":
        raise ValueError("Darwin dependency revision observation query drift")
    if q.get("curtimestamp") is not True or q.get("source_content_requested") is not False:
        raise ValueError("Darwin dependency revision observation query boundary drift")

    gates = observation.get("gates")
    if not isinstance(gates, dict) or gates.get("module_string_identity_observed") is not True:
        raise ValueError("Darwin dependency revision observation gate missing")
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
    parser.add_argument("--api-response", type=Path, required=True)
    parser.add_argument("--predecessor-contract", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    predecessor = load_object(args.predecessor_contract)
    policy = load_object(args.policy)
    observation = build_observation(load_object(args.api_response))
    validate_observation(observation, predecessor, policy)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(observation, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    identity = observation["identity"]
    print(
        "SCRIPTORIUM_DARWIN_MODULE_STRING_OBSERVATION="
        f"{identity['canonical_title']}@{identity['revision_id']} "
        f"{identity['revision_timestamp']} sha1={identity['mediawiki_sha1']} "
        f"observation_sha256={observation['observation_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
