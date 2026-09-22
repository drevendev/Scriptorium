"""Define a fail-closed version-pinned replay contract for Darwin/Rachinsky ``{{ё}}``.

The contract intentionally does not fetch or retain template source bodies. It records
what must be frozen before a replay can be called deterministic, prevents MediaWiki
``expandtemplates.revid`` from being mistaken for a historical template-version pin,
and records canonical template-title identity before dependency binding.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence


CONTRACT_VERSION = "scriptorium-darwin-template-yo-replay-contract-v2"
DISCOVERY_EVIDENCE_VERSION = "scriptorium-template-dependency-discovery-evidence-v1"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
UPSTREAM_EVIDENCE_VERSION = "scriptorium-darwin-template-yo-documentation-evidence-v2"
UPSTREAM_EVIDENCE_SHA256 = "d92bdfcad71aaa8a50f9f35b5b1ada462ed41619400c40576d0603cf154877dc"
BACKLOG_SHA256 = "4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2"
API_DOC_TITLE = "API:Expandtemplates/ru"
API_DOC_REVISION_ID = 6729113
API_DOC_REVISION_DATE = "2024-08-29"
API_DOC_URL = (
    "https://www.mediawiki.org/w/index.php?title=API:Expandtemplates/ru"
    f"&oldid={API_DOC_REVISION_ID}"
)
HELP_EXPAND_TITLE = "Help:ExpandTemplates"
HELP_EXPAND_REVISION_ID = 8168760
HELP_EXPAND_REVISION_DATE = "2026-01-23"
HELP_EXPAND_URL = (
    "https://www.mediawiki.org/w/index.php?title=Help:ExpandTemplates"
    f"&oldid={HELP_EXPAND_REVISION_ID}"
)
PAGE_NAMING_TITLE = "Manual:Page naming/en"
PAGE_NAMING_REVISION_ID = 8270202
PAGE_NAMING_REVISION_DATE = "2026-03-07"
PAGE_NAMING_URL = (
    "https://www.mediawiki.org/w/index.php?title=Manual:Page_naming/en"
    f"&oldid={PAGE_NAMING_REVISION_ID}"
)
WIKISOURCE_YO_TITLE = "Шаблон:Ё"
WIKISOURCE_YO_REVISION_ID = 5687302
WIKISOURCE_YO_REVISION_DATE = "2026-01-21"
WIKISOURCE_YO_URL = (
    "https://ru.wikisource.org/w/index.php?title=Шаблон:Ё"
    f"&oldid={WIKISOURCE_YO_REVISION_ID}"
)
WIKISOURCE_EYO_TITLE = "Шаблон:ЕЁ"
WIKISOURCE_EYO_REVISION_ID = 3684646
WIKISOURCE_EYO_REVISION_DATE = "2019-06-04"
WIKISOURCE_EYO_URL = (
    "https://ru.wikisource.org/w/index.php?title=Шаблон:ЕЁ"
    f"&oldid={WIKISOURCE_EYO_REVISION_ID}"
)
RESEARCH_DATE = "2026-09-22"
REQUIRED_ROOT_TITLES = (WIKISOURCE_YO_TITLE, WIKISOURCE_EYO_TITLE)
REQUIRED_DEPENDENCY_FIELDS = (
    "title",
    "revision_id",
    "revision_timestamp",
    "mediawiki_sha1",
)
REQUIRED_DISCOVERY_FIELDS = (
    "status",
    "method",
    "direct_dependencies",
    "evidence_sha256",
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _verified_upstream_sha(evidence: Mapping[str, object]) -> str:
    stored = evidence.get("evidence_sha256")
    if stored != UPSTREAM_EVIDENCE_SHA256:
        raise ValueError("Darwin {{ё}} upstream evidence digest identity drift")
    unsigned = dict(evidence)
    unsigned.pop("evidence_sha256", None)
    actual = _sha256_json(unsigned)
    if actual != stored:
        raise ValueError("Darwin {{ё}} upstream evidence self-digest drift")
    if evidence.get("schema_version") != UPSTREAM_EVIDENCE_VERSION:
        raise ValueError("Darwin {{ё}} upstream evidence schema drift")
    if evidence.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin {{ё}} upstream evidence candidate drift")
    source_backlog = evidence.get("source_backlog")
    if not isinstance(source_backlog, dict) or source_backlog.get("backlog_sha256") != BACKLOG_SHA256:
        raise ValueError("Darwin {{ё}} upstream backlog identity drift")
    target = evidence.get("target")
    if (
        not isinstance(target, dict)
        or target.get("name") != "ё"
        or target.get("count") != 2227
        or target.get("semantic_status") != "unresolved"
    ):
        raise ValueError("Darwin {{ё}} unresolved target drift")
    return stored


def _validate_sha256(value: object, *, field: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise ValueError(f"Darwin {{ё}} {field} invalid")


def dependency_discovery_evidence_sha256(row: Mapping[str, object]) -> str:
    """Return the canonical source-free discovery digest bound to one exact dependency."""

    proof = row.get("discovery")
    if not isinstance(proof, dict):
        raise ValueError("Darwin {{ё}} dependency discovery proof missing or malformed")
    payload = {
        "schema_version": DISCOVERY_EVIDENCE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "dependency_identity": {
            field: row.get(field)
            for field in REQUIRED_DEPENDENCY_FIELDS
        },
        "discovery": {
            "status": proof.get("status"),
            "method": proof.get("method"),
            "direct_dependencies": proof.get("direct_dependencies"),
        },
    }
    return _sha256_json(payload)


def _validate_discovery_proof(row: Mapping[str, object]) -> tuple[str, ...]:
    proof = row.get("discovery")
    if not isinstance(proof, dict) or set(proof) != set(REQUIRED_DISCOVERY_FIELDS):
        raise ValueError("Darwin {{ё}} dependency discovery proof missing or malformed")
    if proof.get("status") != "complete":
        raise ValueError("Darwin {{ё}} dependency discovery proof not complete")
    method = proof.get("method")
    if not isinstance(method, str) or not method:
        raise ValueError("Darwin {{ё}} dependency discovery method invalid")
    _validate_sha256(proof.get("evidence_sha256"), field="dependency discovery evidence_sha256")
    children = proof.get("direct_dependencies")
    if not isinstance(children, list):
        raise ValueError("Darwin {{ё}} direct dependency discovery list invalid")
    seen: set[str] = set()
    normalized: list[str] = []
    for child in children:
        if not isinstance(child, str) or not child:
            raise ValueError("Darwin {{ё}} discovered dependency title invalid")
        if not (child.startswith("Шаблон:") or child.startswith("Модуль:")):
            raise ValueError("Darwin {{ё}} discovered dependency is not a template/module title")
        if child in seen:
            raise ValueError("Darwin {{ё}} discovered dependency duplicated")
        seen.add(child)
        normalized.append(child)
    expected_digest = dependency_discovery_evidence_sha256(row)
    if proof["evidence_sha256"] != expected_digest:
        raise ValueError("Darwin {{ё}} dependency discovery evidence digest drift")
    return tuple(normalized)


def validate_dependency_closure(
    dependencies: Sequence[Mapping[str, object]],
    edges: Sequence[Mapping[str, object]],
    *,
    require_complete: bool,
) -> None:
    """Validate source-free dependency identities and explicit discovery closure."""

    by_title: dict[str, Mapping[str, object]] = {}
    for row in dependencies:
        for field in REQUIRED_DEPENDENCY_FIELDS:
            if field not in row:
                raise ValueError(f"Darwin {{ё}} dependency missing field: {field}")
        title = row["title"]
        revision_id = row["revision_id"]
        timestamp = row["revision_timestamp"]
        mediawiki_sha1 = row["mediawiki_sha1"]
        if not isinstance(title, str) or not title:
            raise ValueError("Darwin {{ё}} dependency title invalid")
        if title in by_title:
            raise ValueError("Darwin {{ё}} dependency title duplicated")
        if not isinstance(revision_id, int) or revision_id <= 0:
            raise ValueError("Darwin {{ё}} dependency revision_id invalid")
        if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
            raise ValueError("Darwin {{ё}} dependency timestamp invalid")
        if (
            not isinstance(mediawiki_sha1, str)
            or len(mediawiki_sha1) != 40
            or any(ch not in "0123456789abcdef" for ch in mediawiki_sha1)
        ):
            raise ValueError("Darwin {{ё}} dependency mediawiki_sha1 invalid")
        forbidden = {"content", "text", "wikitext", "body", "source_text", "rendered_prose"}
        if forbidden.intersection(row):
            raise ValueError("source/template prose leaked into Darwin {{ё}} dependency identity")
        if "discovery" in row:
            _validate_discovery_proof(row)
        by_title[title] = row

    actual_edges: set[tuple[str, str]] = set()
    for edge in edges:
        if set(edge) != {"from", "to"}:
            raise ValueError("Darwin {{ё}} dependency edge schema drift")
        source = edge["from"]
        target = edge["to"]
        if not isinstance(source, str) or not isinstance(target, str):
            raise ValueError("Darwin {{ё}} dependency edge title invalid")
        if source not in by_title or target not in by_title:
            raise ValueError("Darwin {{ё}} dependency edge references unbound title")
        pair = (source, target)
        if pair in actual_edges:
            raise ValueError("Darwin {{ё}} dependency edge duplicated")
        actual_edges.add(pair)

    if require_complete:
        missing_roots = [title for title in REQUIRED_ROOT_TITLES if title not in by_title]
        if missing_roots:
            raise ValueError("Darwin {{ё}} required root dependency missing")
        if not dependencies:
            raise ValueError("Darwin {{ё}} dependency closure empty")

        expected_edges: set[tuple[str, str]] = set()
        for title, row in by_title.items():
            if "discovery" not in row:
                raise ValueError("Darwin {{ё}} complete closure lacks dependency discovery proof")
            children = _validate_discovery_proof(row)
            for child in children:
                if child not in by_title:
                    raise ValueError("Darwin {{ё}} discovered dependency remains unbound")
                expected_edges.add((title, child))

        if actual_edges != expected_edges:
            raise ValueError("Darwin {{ё}} dependency edges do not match discovery proof")


def build_contract(evidence: Mapping[str, object]) -> dict[str, object]:
    """Build the committed source-free replay contract in its intentionally open state."""

    evidence_sha = _verified_upstream_sha(evidence)
    contract: dict[str, object] = {
        "schema_version": CONTRACT_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "source_evidence": {
            "schema_version": UPSTREAM_EVIDENCE_VERSION,
            "evidence_sha256": evidence_sha,
            "backlog_sha256": BACKLOG_SHA256,
        },
        "official_api_evidence": {
            "provider": "MediaWiki.org",
            "title": API_DOC_TITLE,
            "revision_id": API_DOC_REVISION_ID,
            "revision_date": API_DOC_REVISION_DATE,
            "permanent_url": API_DOC_URL,
            "researched_on": RESEARCH_DATE,
            "expandtemplates_revid": {
                "documented_scope": "revision_context_for_REVISIONID_and_similar_variables",
                "pins_transcluded_template_revisions": False,
            },
            "templatesandbox": {
                "direct_title_text_override_supported": True,
                "single_override_proves_recursive_dependency_closure": False,
            },
            "recursive_expansion": {
                "title": HELP_EXPAND_TITLE,
                "revision_id": HELP_EXPAND_REVISION_ID,
                "revision_date": HELP_EXPAND_REVISION_DATE,
                "permanent_url": HELP_EXPAND_URL,
                "templates_parser_functions_and_variables_expand_recursively": True,
            },
            "title_canonicalization": {
                "title": PAGE_NAMING_TITLE,
                "revision_id": PAGE_NAMING_REVISION_ID,
                "revision_date": PAGE_NAMING_REVISION_DATE,
                "permanent_url": PAGE_NAMING_URL,
                "first_page_name_character_auto_capitalized_by_default": True,
                "canonical_form_capitalizes_first_page_name_character": True,
            },
        },
        "root_title_observations": [
            {
                "provider": "Russian Wikisource",
                "invocation_spelling": "Шаблон:ё",
                "canonical_title": WIKISOURCE_YO_TITLE,
                "revision_id": WIKISOURCE_YO_REVISION_ID,
                "revision_date": WIKISOURCE_YO_REVISION_DATE,
                "permanent_url": WIKISOURCE_YO_URL,
                "mediawiki_sha1_bound": False,
            },
            {
                "provider": "Russian Wikisource",
                "invocation_spelling": WIKISOURCE_EYO_TITLE,
                "canonical_title": WIKISOURCE_EYO_TITLE,
                "revision_id": WIKISOURCE_EYO_REVISION_ID,
                "revision_date": WIKISOURCE_EYO_REVISION_DATE,
                "permanent_url": WIKISOURCE_EYO_URL,
                "mediawiki_sha1_bound": False,
            },
        ],
        "replay_contract": {
            "required_root_titles": list(REQUIRED_ROOT_TITLES),
            "required_dependency_fields": list(REQUIRED_DEPENDENCY_FIELDS),
            "required_discovery_proof_fields": list(REQUIRED_DISCOVERY_FIELDS),
            "dependency_identity_scope": (
                "canonical exact page title plus revision id, revision timestamp and MediaWiki content SHA-1"
            ),
            "dependency_discovery_proof_required": True,
            "dependency_discovery_evidence_schema_version": DISCOVERY_EVIDENCE_VERSION,
            "dependency_discovery_evidence_sha256_scope": (
                "canonical source-free JSON over candidate id, exact dependency identity, "
                "discovery status/method and exact direct-dependency title list"
            ),
            "dependency_graph_must_be_transitively_closed": True,
            "live_or_unbound_dependency_allowed": False,
            "native_expandtemplates_revid_is_version_pin": False,
            "single_templatesandbox_override_is_closed_graph": False,
            "strategy": (
                "bind every template/module revision in the transitive replay graph by canonical title; "
                "for every bound node retain source-free complete direct-dependency discovery evidence "
                "whose SHA-256 is recomputed from that exact node identity and dependency set, and "
                "require graph edges to exactly match that evidence; evaluate only in a controlled "
                "environment that consumes those bound identities"
            ),
            "dependencies": [],
            "edges": [],
            "dependency_closure_complete": False,
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
                "canonical root-title identity is now explicit, but MediaWiki expandtemplates revid "
                "supplies revision context rather than a historical transclusion-version pin; recursive "
                "template dependencies remain unbound and no complete per-node discovery proof exists, "
                "so deterministic replay equivalence is not yet demonstrated"
            ),
            "next_evidence_required": (
                "freeze exact source-free identities for canonical Шаблон:Ё, Шаблон:ЕЁ and every nested "
                "template/module dependency in one replay environment, including MediaWiki content SHA-1 "
                "and complete source-free direct-dependency discovery evidence for each exact revision; "
                "then verify deterministic forced and non-forced outputs before promotion"
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
    validate_dependency_closure([], [], require_complete=False)
    contract["contract_sha256"] = _sha256_json(contract)
    return contract


def validate_contract(contract: Mapping[str, object], evidence: Mapping[str, object]) -> None:
    expected = build_contract(evidence)
    if dict(contract) != expected:
        raise ValueError("Darwin {{ё}} replay contract drift")
    if contract.get("source_text_included") is not False:
        raise ValueError("Darwin {{ё}} replay contract must remain source-free")
    observations = contract.get("root_title_observations")
    if not isinstance(observations, list) or len(observations) != 2:
        raise ValueError("Darwin {{ё}} canonical root observations missing")
    if observations[0].get("canonical_title") != WIKISOURCE_YO_TITLE:
        raise ValueError("Darwin {{ё}} shorthand canonical title drift")
    if any(row.get("mediawiki_sha1_bound") is not False for row in observations):
        raise ValueError("Darwin {{ё}} root observations must not imply complete dependency identity")
    replay = contract.get("replay_contract")
    if not isinstance(replay, dict):
        raise ValueError("Darwin {{ё}} replay contract body missing")
    dependencies = replay.get("dependencies")
    edges = replay.get("edges")
    if not isinstance(dependencies, list) or not isinstance(edges, list):
        raise ValueError("Darwin {{ё}} replay dependency graph missing")
    validate_dependency_closure(dependencies, edges, require_complete=False)
    if replay.get("required_root_titles") != list(REQUIRED_ROOT_TITLES):
        raise ValueError("Darwin {{ё}} canonical root-title contract drift")
    if replay.get("dependency_closure_complete") is not False:
        raise ValueError("Darwin {{ё}} dependency closure must remain open")
    if replay.get("dependency_discovery_proof_required") is not True:
        raise ValueError("Darwin {{ё}} dependency discovery proof must be required")
    if replay.get("dependency_discovery_evidence_schema_version") != DISCOVERY_EVIDENCE_VERSION:
        raise ValueError("Darwin {{ё}} dependency discovery evidence schema drift")
    if replay.get("native_expandtemplates_revid_is_version_pin") is not False:
        raise ValueError("expandtemplates revid must not be treated as a version pin")
    if replay.get("single_templatesandbox_override_is_closed_graph") is not False:
        raise ValueError("single TemplateSandbox override must not imply closed graph")
    mode = contract.get("mode_verification")
    if (
        not isinstance(mode, dict)
        or mode.get("outputs_verified") is not False
        or not isinstance(mode.get("forced_yoification"), dict)
        or not isinstance(mode.get("non_forced_yoification"), dict)
        or mode["forced_yoification"].get("verified_output_sha256") is not None
        or mode["non_forced_yoification"].get("verified_output_sha256") is not None
    ):
        raise ValueError("Darwin {{ё}} replay output verification must remain open")
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
            raise ValueError(f"{key} must remain false in Darwin {{ё}} replay contract")
    if contract.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")


def build_contract_from_path(evidence_path: Path) -> dict[str, object]:
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    if not isinstance(evidence, dict):
        raise ValueError("Darwin {{ё}} evidence input must be a JSON object")
    return build_contract(evidence)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    contract = build_contract_from_path(args.evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(contract["contract_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
