"""Verify the selected Darwin/Rachinsky {{ё}} replay modes without widening provenance claims."""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unicodedata
from typing import Mapping, Sequence

CONTRACT_VERSION = "scriptorium-darwin-template-yo-replay-contract-v6"
PREDECESSOR_VERSION = "scriptorium-darwin-template-yo-replay-contract-v5"
PREDECESSOR_SHA256 = "4ded05d3ea45e9cfa9aa657e6b4e1c26c48cf2f1be60643d0194993e995b4c0c"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
PROVIDER_API = "https://ru.wikisource.org/w/api.php"
INVOCATION = "{{ё}}"
NORMALIZATION = "unicode-nfc-then-python-str-strip"
REPETITIONS_PER_MODE = 2

BOUND_IDENTITIES = (
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
    {
        "title": "Модуль:String",
        "revision_id": 3684569,
        "revision_timestamp": "2019-06-04T20:18:11Z",
        "mediawiki_sha1": "a34727a1e4ec3c4b4c7ec556c94991f75442d99c",
    },
)

MODES = {
    "forced_yoification": {
        "context_title": "О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)",
        "documented_expected_output": "ё",
    },
    "non_forced_yoification": {
        "context_title": "О происхождении видов (Дарвин; Рачинский)/1864",
        "documented_expected_output": "е",
    },
}


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _sha256_json(value: object) -> str:
    return _sha256_text(_canonical_json(value))


def _self_digest(value: Mapping[str, object], field: str) -> str:
    unsigned = deepcopy(dict(value))
    unsigned.pop(field, None)
    return _sha256_json(unsigned)


def _load_object(path: Path, *, label: str) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Darwin {{ё}} {label} must be a JSON object")
    return value


def normalize_semantic_output(value: str) -> str:
    return unicodedata.normalize("NFC", value).strip()


def _verify_predecessor(predecessor: Mapping[str, object]) -> None:
    if predecessor.get("schema_version") != PREDECESSOR_VERSION:
        raise ValueError("Darwin {{ё}} replay v6 predecessor schema drift")
    if predecessor.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin {{ё}} replay v6 predecessor candidate drift")
    if predecessor.get("contract_sha256") != PREDECESSOR_SHA256:
        raise ValueError("Darwin {{ё}} replay v6 predecessor digest identity drift")
    if _self_digest(predecessor, "contract_sha256") != PREDECESSOR_SHA256:
        raise ValueError("Darwin {{ё}} replay v6 predecessor self-digest drift")

    replay = predecessor.get("replay_contract")
    if not isinstance(replay, dict):
        raise ValueError("Darwin {{ё}} replay v5 body missing")
    rows = replay.get("dependencies")
    if not isinstance(rows, list) or len(rows) != 3:
        raise ValueError("Darwin {{ё}} replay v5 dependency set drift")
    actual = [
        {
            "title": row.get("title"),
            "revision_id": row.get("revision_id"),
            "revision_timestamp": row.get("revision_timestamp"),
            "mediawiki_sha1": row.get("mediawiki_sha1"),
        }
        for row in rows
        if isinstance(row, dict)
    ]
    if actual != list(BOUND_IDENTITIES):
        raise ValueError("Darwin {{ё}} replay v5 bound identities drift")
    if replay.get("dependency_closure_complete") is not True:
        raise ValueError("Darwin {{ё}} replay v5 dependency closure drift")
    if replay.get("discovered_unbound_dependencies") != []:
        raise ValueError("Darwin {{ё}} replay v5 regained unbound dependencies")
    if replay.get("live_or_unbound_dependency_allowed") is not False:
        raise ValueError("Darwin {{ё}} replay v5 live dependency boundary drift")
    mode = predecessor.get("mode_verification")
    if not isinstance(mode, dict) or mode.get("outputs_verified") is not False:
        raise ValueError("Darwin {{ё}} replay v5 output gate unexpectedly advanced")


def build_contract(predecessor: Mapping[str, object]) -> dict[str, object]:
    """Build the source-free v6 semantic-output contract from reviewed v5."""
    _verify_predecessor(predecessor)
    modes: dict[str, object] = {}
    for name, spec in MODES.items():
        output = spec["documented_expected_output"]
        context = spec["context_title"]
        modes[name] = {
            "context_title": context,
            "context_title_sha256": _sha256_text(context),
            "documented_expected_output": output,
            "verified_semantic_output": output,
            "verified_semantic_output_sha256": _sha256_text(output),
            "repetitions_required": REPETITIONS_PER_MODE,
        }
    modes["outputs_verified"] = True

    contract: dict[str, object] = {
        "schema_version": CONTRACT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "predecessor_contract": {
            "schema_version": PREDECESSOR_VERSION,
            "contract_sha256": PREDECESSOR_SHA256,
        },
        "replay_environment": {
            "provider_api": PROVIDER_API,
            "api_action": "expandtemplates",
            "api_property": "wikitext",
            "invocation": INVOCATION,
            "invocation_sha256": _sha256_text(INVOCATION),
            "semantic_output_normalization": NORMALIZATION,
            "repetitions_per_mode": REPETITIONS_PER_MODE,
            "identity_stable_window_required": True,
            "current_revision_identities_required_before_and_after": [dict(row) for row in BOUND_IDENTITIES],
            "revid_used_as_recursive_dependency_selector": False,
            "offline_version_pinned_mediawiki_environment_claimed": False,
            "historical_transclusion_provenance_proved": False,
            "scope": (
                "provider replay is admissible only while all recursively discovered current dependency "
                "identities exactly equal the reviewed v5 snapshot before and after both mode replays"
            ),
        },
        "mode_verification": {
            **modes,
        },
        "promotion_decision": {
            "render_profile_rule_promoted": False,
            "backlog_item_removed": False,
            "reason": (
                "zero-argument {{ё}} forced/non-forced semantic outputs are verified for the selected "
                "identity-stable replay snapshot, but render-profile promotion is a separate bounded judgement"
            ),
            "next_evidence_required": (
                "independently review this output evidence, then update the frozen render profile/backlog in "
                "a separate unit before implementing the complete literary renderer"
            ),
        },
        "gates": {
            "semantic_dependency_closure_proved": True,
            "zero_argument_template_yo_outputs_verified": True,
            "outputs_verified": True,
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


def _identity_rows_from_query(payload: Mapping[str, object]) -> list[dict[str, object]]:
    query = payload.get("query")
    pages = query.get("pages") if isinstance(query, dict) else None
    if not isinstance(pages, list):
        raise ValueError("Darwin {{ё}} replay identity query is missing pages")
    by_title: dict[str, dict[str, object]] = {}
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("Darwin {{ё}} replay identity page row is malformed")
        revisions = page.get("revisions")
        if not isinstance(revisions, list) or len(revisions) != 1 or not isinstance(revisions[0], dict):
            raise ValueError("Darwin {{ё}} replay identity revision row is malformed")
        revision = revisions[0]
        title = page.get("title")
        if not isinstance(title, str):
            raise ValueError("Darwin {{ё}} replay identity title is malformed")
        by_title[title] = {
            "title": title,
            "revision_id": revision.get("revid"),
            "revision_timestamp": revision.get("timestamp"),
            "mediawiki_sha1": revision.get("sha1"),
        }
    try:
        return [by_title[row["title"]] for row in BOUND_IDENTITIES]
    except KeyError as exc:
        raise ValueError("Darwin {{ё}} replay identity query is incomplete") from exc


def verify_identity_window(before: Mapping[str, object], after: Mapping[str, object]) -> None:
    expected = list(BOUND_IDENTITIES)
    if _identity_rows_from_query(before) != expected:
        raise ValueError("Darwin {{ё}} replay pre-window dependency identity drift")
    if _identity_rows_from_query(after) != expected:
        raise ValueError("Darwin {{ё}} replay post-window dependency identity drift")


def _expand_wikitext(payload: Mapping[str, object]) -> str:
    expanded = payload.get("expandtemplates")
    value = expanded.get("wikitext") if isinstance(expanded, dict) else None
    if not isinstance(value, str):
        raise ValueError("Darwin {{ё}} replay response is missing expanded wikitext")
    return value


def verify_mode_replays(
    contract: Mapping[str, object],
    replay_payloads: Mapping[str, Sequence[Mapping[str, object]]],
) -> dict[str, str]:
    if contract.get("contract_sha256") != _self_digest(contract, "contract_sha256"):
        raise ValueError("Darwin {{ё}} replay v6 contract self-digest drift")
    mode_contract = contract.get("mode_verification")
    if not isinstance(mode_contract, dict) or mode_contract.get("outputs_verified") is not True:
        raise ValueError("Darwin {{ё}} replay v6 output gate is not verified")

    verified: dict[str, str] = {}
    for mode_name, spec in MODES.items():
        payloads = replay_payloads.get(mode_name)
        if not isinstance(payloads, Sequence) or isinstance(payloads, (str, bytes)):
            raise ValueError(f"Darwin {{ё}} {mode_name} replay payloads missing")
        if len(payloads) != REPETITIONS_PER_MODE:
            raise ValueError(f"Darwin {{ё}} {mode_name} replay count drift")
        outputs = [normalize_semantic_output(_expand_wikitext(payload)) for payload in payloads]
        if len(set(outputs)) != 1:
            raise ValueError(f"Darwin {{ё}} {mode_name} replay is nondeterministic")
        expected = spec["documented_expected_output"]
        if outputs[0] != expected:
            raise ValueError(f"Darwin {{ё}} {mode_name} semantic output mismatch")
        frozen = mode_contract.get(mode_name)
        if not isinstance(frozen, dict):
            raise ValueError(f"Darwin {{ё}} {mode_name} frozen contract missing")
        if frozen.get("context_title") != spec["context_title"]:
            raise ValueError(f"Darwin {{ё}} {mode_name} context drift")
        if frozen.get("verified_semantic_output") != outputs[0]:
            raise ValueError(f"Darwin {{ё}} {mode_name} frozen output drift")
        digest = _sha256_text(outputs[0])
        if frozen.get("verified_semantic_output_sha256") != digest:
            raise ValueError(f"Darwin {{ё}} {mode_name} semantic digest drift")
        verified[mode_name] = digest
    return verified


def validate_contract(contract: Mapping[str, object], predecessor: Mapping[str, object]) -> None:
    expected = build_contract(predecessor)
    if dict(contract) != expected:
        raise ValueError("Darwin {{ё}} replay v6 contract drift")
    if _self_digest(contract, "contract_sha256") != contract.get("contract_sha256"):
        raise ValueError("Darwin {{ё}} replay v6 self-digest drift")
    environment = contract.get("replay_environment")
    if not isinstance(environment, dict):
        raise ValueError("Darwin {{ё}} replay v6 environment missing")
    if environment.get("identity_stable_window_required") is not True:
        raise ValueError("Darwin {{ё}} replay v6 identity-stable window must be required")
    for key in (
        "revid_used_as_recursive_dependency_selector",
        "offline_version_pinned_mediawiki_environment_claimed",
        "historical_transclusion_provenance_proved",
    ):
        if environment.get(key) is not False:
            raise ValueError(f"{key} must remain false in Darwin {{ё}} replay v6")

    decision = contract.get("promotion_decision")
    if not isinstance(decision, dict) or decision.get("render_profile_rule_promoted") is not False:
        raise ValueError("Darwin {{ё}} replay v6 render-profile promotion must remain closed")
    if decision.get("backlog_item_removed") is not False:
        raise ValueError("Darwin {{ё}} replay v6 backlog removal must remain closed")

    gates = contract.get("gates")
    if not isinstance(gates, dict):
        raise ValueError("Darwin {{ё}} replay v6 gates missing")
    if gates.get("semantic_dependency_closure_proved") is not True:
        raise ValueError("Darwin {{ё}} replay v6 dependency closure gate drift")
    if gates.get("zero_argument_template_yo_outputs_verified") is not True or gates.get("outputs_verified") is not True:
        raise ValueError("Darwin {{ё}} replay v6 output verification gate drift")
    for key in (
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
            raise ValueError(f"{key} must remain false in Darwin {{ё}} replay v6")
    if gates.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")
    if contract.get("source_text_included") is not False:
        raise ValueError("Darwin {{ё}} replay v6 must remain source-free")


def build_contract_from_path(predecessor_path: Path) -> dict[str, object]:
    return build_contract(_load_object(predecessor_path, label="v5 predecessor contract"))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predecessor-contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    contract = build_contract_from_path(args.predecessor_contract)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(contract["contract_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
