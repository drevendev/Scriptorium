"""Bind the reviewed exact Module:String revision into Darwin/Rachinsky {{ё}} replay closure."""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence

from .darwin_module_string_dependency_probe import probe_sha256
from .darwin_template_yo_replay_contract import (
    DISCOVERY_EVIDENCE_VERSION,
    dependency_discovery_evidence_sha256,
    validate_dependency_closure,
)

CONTRACT_VERSION = "scriptorium-darwin-template-yo-replay-contract-v5"
PREDECESSOR_VERSION = "scriptorium-darwin-template-yo-replay-contract-v4"
PREDECESSOR_SHA256 = "f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64"
PROBE_VERSION = "scriptorium-darwin-module-string-dependency-probe-v1"
PROBE_SHA256 = "e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
MODULE_TITLE = "Модуль:String"
MODULE_IDENTITY = {
    "canonical_title": MODULE_TITLE,
    "revision_id": 3684569,
    "revision_timestamp": "2019-06-04T20:18:11Z",
    "mediawiki_sha1": "a34727a1e4ec3c4b4c7ec556c94991f75442d99c",
}
MODULE_SOURCE_SHA256 = "258cec6ab8b4c1e3eb0e812d72d39f4302f321a4d1fdd7aa3883187db0eecb03"
MODULE_SOURCE_UTF8_BYTES = 18468
MODULE_SCAN_METHOD = "scriptorium-darwin-lua-loader-scan-v1"
BOUND_MODULE_EDGE = {"from": "Шаблон:ЕЁ", "to": MODULE_TITLE}


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _self_digest(value: Mapping[str, object], field: str) -> str:
    unsigned = deepcopy(dict(value))
    unsigned.pop(field, None)
    return _sha256_json(unsigned)


def _load_object(path: Path, *, label: str) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Darwin {{ё}} {label} must be a JSON object")
    return value


def _verify_predecessor(predecessor: Mapping[str, object]) -> list[dict[str, object]]:
    if predecessor.get("schema_version") != PREDECESSOR_VERSION:
        raise ValueError("Darwin {{ё}} replay v5 predecessor schema drift")
    if predecessor.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin {{ё}} replay v5 predecessor candidate drift")
    if predecessor.get("contract_sha256") != PREDECESSOR_SHA256:
        raise ValueError("Darwin {{ё}} replay v5 predecessor digest identity drift")
    if _self_digest(predecessor, "contract_sha256") != PREDECESSOR_SHA256:
        raise ValueError("Darwin {{ё}} replay v5 predecessor self-digest drift")

    replay = predecessor.get("replay_contract")
    if not isinstance(replay, dict):
        raise ValueError("Darwin {{ё}} replay v4 body missing")
    dependencies = replay.get("dependencies")
    if not isinstance(dependencies, list) or len(dependencies) != 2:
        raise ValueError("Darwin {{ё}} replay v4 dependency set drift")
    if replay.get("dependency_closure_complete") is not False:
        raise ValueError("Darwin {{ё}} replay v4 unexpectedly claims complete closure")
    if replay.get("discovered_unbound_dependencies") != [MODULE_TITLE]:
        raise ValueError("Darwin {{ё}} replay v4 unbound dependency set drift")
    return deepcopy(dependencies)


def _verify_probe(probe: Mapping[str, object]) -> dict[str, object]:
    if probe.get("schema_version") != PROBE_VERSION:
        raise ValueError("Darwin {{ё}} Module:String probe schema drift")
    if probe.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin {{ё}} Module:String probe candidate drift")
    if probe.get("probe_sha256") != PROBE_SHA256:
        raise ValueError("Darwin {{ё}} Module:String probe digest identity drift")
    if probe_sha256(probe) != PROBE_SHA256:
        raise ValueError("Darwin {{ё}} Module:String probe self-digest drift")
    if probe.get("source_text_included") is not False:
        raise ValueError("Darwin {{ё}} Module:String probe must remain source-free")

    identity = probe.get("identity")
    if not isinstance(identity, dict) or identity != MODULE_IDENTITY:
        raise ValueError("Darwin {{ё}} Module:String exact identity drift")
    surface = probe.get("dependency_surface")
    if not isinstance(surface, dict):
        raise ValueError("Darwin {{ё}} Module:String dependency surface missing")
    if surface.get("scan_complete") is not True:
        raise ValueError("Darwin {{ё}} Module:String dependency scan is not complete")
    if surface.get("scan_method") != MODULE_SCAN_METHOD:
        raise ValueError("Darwin {{ё}} Module:String scan method drift")
    if surface.get("dynamic_or_unsupported_loader_calls") != []:
        raise ValueError("Darwin {{ё}} Module:String has unsupported loader calls")
    if surface.get("static_wiki_module_dependencies") != []:
        raise ValueError("Darwin {{ё}} Module:String gained static wiki-module dependencies")
    if surface.get("source_sha1") != MODULE_IDENTITY["mediawiki_sha1"]:
        raise ValueError("Darwin {{ё}} Module:String source SHA-1 drift")
    if surface.get("source_sha256") != MODULE_SOURCE_SHA256:
        raise ValueError("Darwin {{ё}} Module:String source SHA-256 drift")
    if surface.get("source_utf8_bytes") != MODULE_SOURCE_UTF8_BYTES:
        raise ValueError("Darwin {{ё}} Module:String source byte count drift")
    return dict(surface)


def _module_dependency_row() -> dict[str, object]:
    row: dict[str, object] = {
        "title": MODULE_TITLE,
        "revision_id": MODULE_IDENTITY["revision_id"],
        "revision_timestamp": MODULE_IDENTITY["revision_timestamp"],
        "mediawiki_sha1": MODULE_IDENTITY["mediawiki_sha1"],
        "discovery": {
            "status": "complete",
            "method": MODULE_SCAN_METHOD,
            "direct_dependencies": [],
            "evidence_sha256": "0" * 64,
        },
    }
    row["discovery"]["evidence_sha256"] = dependency_discovery_evidence_sha256(row)
    return row


def build_contract(
    predecessor: Mapping[str, object],
    probe: Mapping[str, object],
) -> dict[str, object]:
    """Bind the reviewed module identity and close only the dependency graph."""
    dependencies = _verify_predecessor(predecessor)
    _verify_probe(probe)
    module_row = _module_dependency_row()
    dependencies.append(module_row)

    predecessor_replay = predecessor["replay_contract"]
    prior_edges = predecessor_replay.get("edges")
    if prior_edges != [{"from": "Шаблон:Ё", "to": "Шаблон:ЕЁ"}]:
        raise ValueError("Darwin {{ё}} replay v4 bound edge drift")
    edges = [deepcopy(prior_edges[0]), dict(BOUND_MODULE_EDGE)]
    validate_dependency_closure(dependencies, edges, require_complete=True)

    contract: dict[str, object] = {
        "schema_version": CONTRACT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "predecessor_contract": {
            "schema_version": PREDECESSOR_VERSION,
            "contract_sha256": PREDECESSOR_SHA256,
        },
        "binding_evidence": {
            "module_string_probe": {
                "schema_version": PROBE_VERSION,
                "probe_sha256": PROBE_SHA256,
            },
            "selected_dependency": {
                **MODULE_IDENTITY,
                "source_sha256": MODULE_SOURCE_SHA256,
                "source_utf8_bytes": MODULE_SOURCE_UTF8_BYTES,
                "selection": (
                    "deliberately selected exact revision from the reviewed point-in-time "
                    "observation and exact-revision dependency probe"
                ),
                "historical_transclusion_provenance_proved": False,
            },
            "source_content_retained": False,
        },
        "replay_contract": {
            "dependencies": dependencies,
            "edges": edges,
            "discovered_unbound_dependencies": [],
            "dependency_closure_complete": True,
            "dependency_discovery_evidence_schema_version": DISCOVERY_EVIDENCE_VERSION,
            "dependency_graph_must_be_transitively_closed": True,
            "live_or_unbound_dependency_allowed": False,
        },
        "mode_verification": {
            "forced_yoification": {
                "documented_expected_output": "ё",
                "verified_output_sha256": None,
            },
            "non_forced_yoification": {
                "documented_expected_output": "е",
                "verified_output_sha256": None,
            },
            "outputs_verified": False,
        },
        "promotion_decision": {
            "render_profile_rule_promoted": False,
            "backlog_item_removed": False,
            "reason": (
                "the replay dependency graph is now source-free, exact-revision-bound and "
                "transitively closed, but forced and non-forced outputs have not yet been "
                "deterministically verified in an environment that consumes only those bound identities"
            ),
            "next_evidence_required": (
                "replay the bound three-node graph in a controlled version-pinned environment and "
                "verify deterministic forced/non-forced outputs before promoting the {{ё}} renderer rule"
            ),
        },
        "gates": {
            "semantic_dependency_closure_proved": True,
            "outputs_verified": False,
            "renderer_semantics_complete": False,
            "renderer_implementation_ready": False,
            "render_profile_rule_promoted": False,
            "inter_page_composition_frozen": False,
            "literary_body_count_and_digests_frozen": False,
            "minimum_300k_proved": False,
            "admitted_for_calibration": False,
            "diagnostic_ready": False,
            "fantlab_source_edition_match": "unknown",
            "m2_parity_admissible": False,
        },
    }
    contract["contract_sha256"] = _sha256_json(contract)
    return contract


def validate_contract(
    contract: Mapping[str, object],
    predecessor: Mapping[str, object],
    probe: Mapping[str, object],
) -> None:
    expected = build_contract(predecessor, probe)
    if dict(contract) != expected:
        raise ValueError("Darwin {{ё}} replay v5 contract drift")
    if contract.get("source_text_included") is not False:
        raise ValueError("Darwin {{ё}} replay v5 must remain source-free")
    if _self_digest(contract, "contract_sha256") != contract.get("contract_sha256"):
        raise ValueError("Darwin {{ё}} replay v5 self-digest drift")

    replay = contract.get("replay_contract")
    if not isinstance(replay, dict):
        raise ValueError("Darwin {{ё}} replay v5 body missing")
    dependencies = replay.get("dependencies")
    edges = replay.get("edges")
    if not isinstance(dependencies, list) or not isinstance(edges, list):
        raise ValueError("Darwin {{ё}} replay v5 graph missing")
    validate_dependency_closure(dependencies, edges, require_complete=True)
    if replay.get("dependency_closure_complete") is not True:
        raise ValueError("Darwin {{ё}} replay v5 dependency closure must be complete")
    if replay.get("discovered_unbound_dependencies") != []:
        raise ValueError("Darwin {{ё}} replay v5 must not retain unbound dependencies")

    evidence = contract.get("binding_evidence")
    selected = evidence.get("selected_dependency") if isinstance(evidence, dict) else None
    if not isinstance(selected, dict) or selected.get("historical_transclusion_provenance_proved") is not False:
        raise ValueError("Darwin {{ё}} replay v5 must not claim historical transclusion provenance")

    mode = contract.get("mode_verification")
    if not isinstance(mode, dict) or mode.get("outputs_verified") is not False:
        raise ValueError("Darwin {{ё}} replay v5 output verification must remain open")
    decision = contract.get("promotion_decision")
    if (
        not isinstance(decision, dict)
        or decision.get("render_profile_rule_promoted") is not False
        or decision.get("backlog_item_removed") is not False
    ):
        raise ValueError("Darwin {{ё}} replay v5 renderer promotion must remain closed")

    gates = contract.get("gates")
    if not isinstance(gates, dict) or gates.get("semantic_dependency_closure_proved") is not True:
        raise ValueError("Darwin {{ё}} replay v5 semantic dependency closure gate drift")
    for key in (
        "outputs_verified",
        "renderer_semantics_complete",
        "renderer_implementation_ready",
        "render_profile_rule_promoted",
        "inter_page_composition_frozen",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "admitted_for_calibration",
        "diagnostic_ready",
        "m2_parity_admissible",
    ):
        if gates.get(key) is not False:
            raise ValueError(f"{key} must remain false in Darwin {{ё}} replay v5 contract")
    if gates.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")


def build_contract_from_paths(
    predecessor_path: Path,
    probe_path: Path,
) -> dict[str, object]:
    return build_contract(
        _load_object(predecessor_path, label="v4 predecessor contract"),
        _load_object(probe_path, label="Module:String probe"),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predecessor-contract", type=Path, required=True)
    parser.add_argument("--module-probe", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    contract = build_contract_from_paths(args.predecessor_contract, args.module_probe)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(contract["contract_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
