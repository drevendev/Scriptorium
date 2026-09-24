"""Bind source-free provider identities for the frozen Darwin/Rachinsky ``{{ВАР}}`` closure.

This evidence follows SCRIP-CORPUS-083's independently reviewed observed-live
six-revision topology. It freezes exact Russian Wikisource revision identities
without persisting source prose. Completing the MediaWiki SHA-1 identity gate
does not establish a full Scribunto replay, historical transclusion, renderer
promotion, literary-body identity, or FantLab parity.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Mapping, Sequence


EVIDENCE_VERSION = "scriptorium-darwin-var-provider-revision-identities-v1"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
PRIOR_CLOSURE_VERSION = "scriptorium-darwin-var-live-snapshot-closure-v1"
PRIOR_CLOSURE_SHA256 = "245f77bf3d99d6610ca5fbbe4fcdcdb4ef68bebca612c5bb81db6c2d77f26509"
RESEARCH_DATE = "2026-09-24"
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")

# closure_title preserves the alias used by the reviewed dependency graph.
# provider_title records the canonical title returned by Russian Wikisource.
RESOURCES = (
    (
        "Шаблон:ВАР",
        "Шаблон:ВАР",
        122258,
        3684602,
        "2019-06-04T20:36:46Z",
        "fdb6fa7c0d4b08157bc30d44f5f77c5b9313167c",
        206,
        269,
        "583f46a8f7fa2444456abede564817e134d313fb20d5cabfa2f2c48591c54707",
    ),
    (
        "Модуль:Дореформенная орфография",
        "Модуль:Дореформенная орфография",
        378940,
        5721277,
        "2026-06-08T13:06:13Z",
        "64d28378f4f620c67e1823a0d4292445d9ab293d",
        1553,
        1588,
        "d0199f6df8f5f789e6a5aec0e450dae6d35c3448adca411481244e40aec3004d",
    ),
    (
        "Module:Header",
        "Модуль:Header",
        361783,
        5746249,
        "2026-09-10T02:29:30Z",
        "2ab2bfdd7e49c73c4ec9ef24e4625c1d228cfba0",
        54598,
        67792,
        "b3950aa5a04e8a8f3bec71c6c82843643dfdc1a1a82f3788f48830f21e434ecb",
    ),
    (
        "Module:BEED",
        "Модуль:BEED",
        362284,
        5746253,
        "2026-09-10T03:41:25Z",
        "9e9531e9178e0333bd3a939ace91e6a71e114cc5",
        10647,
        11979,
        "108fee006a43f146302aafda316f05f15198932c3389487ed7c760c83a7c4875",
    ),
    (
        "Module:Util",
        "Модуль:Util",
        980298,
        5750249,
        "2026-09-18T07:31:28Z",
        "945f8e6bf173bb5712385995255a8b6eccef38ed",
        1328,
        1585,
        "a69fdcf9cf4dbbfe34d3e41585f2bcd418eee4efbe6e5c42d82e450cc4045a90",
    ),
    (
        "Module:RomanNumber",
        "Модуль:RomanNumber",
        378544,
        3684553,
        "2019-06-04T20:13:27Z",
        "51a3956469ee3fbd4ed56ce3a1f72f76f231e1d3",
        1152,
        1212,
        "90edb9a1d3bf5d283112fd58e28ee60f2569ae0fe7850e936a17f4e23869cf45",
    ),
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def build_evidence() -> dict[str, object]:
    resources = [
        {
            "closure_title": closure_title,
            "title": provider_title,
            "page_id": page_id,
            "revision_id": revision_id,
            "revision_timestamp": revision_timestamp,
            "mediawiki_sha1": mediawiki_sha1,
            "wikitext_character_count": character_count,
            "wikitext_utf8_byte_count": byte_count,
            "wikitext_sha256": wikitext_sha256,
        }
        for (
            closure_title,
            provider_title,
            page_id,
            revision_id,
            revision_timestamp,
            mediawiki_sha1,
            character_count,
            byte_count,
            wikitext_sha256,
        ) in RESOURCES
    ]
    evidence: dict[str, object] = {
        "schema_version": EVIDENCE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "researched_on": RESEARCH_DATE,
        "prior_closure": {
            "schema_version": PRIOR_CLOSURE_VERSION,
            "evidence_sha256": PRIOR_CLOSURE_SHA256,
        },
        "capture_provenance": {
            "provider": "Russian Wikisource",
            "api_surface": (
                "MediaWiki revisions API: rvprop=ids|timestamp|sha1|content, rvslots=main"
            ),
            "source_text_persisted": False,
        },
        "resources": resources,
        "identity_gate": {
            "revision_ids_complete": True,
            "mediawiki_sha1_complete": True,
            "provider_title_aliases_explicit": True,
            "missing_mediawiki_sha1_titles": [],
            "replay_ready": False,
            "reason": (
                "all six exact observed-live revisions are bound to provider-returned "
                "identities, but a full candidate invocation replay and an explicit "
                "version-pinned Scribunto/runtime boundary are still missing"
            ),
        },
        "promotion_decision": {
            "full_var_candidate_branch_replayed": False,
            "render_profile_rule_promoted": False,
            "backlog_item_removed": False,
            "effective_backlog_changed": False,
            "var_invocations_unresolved": 388,
            "next_evidence_required": (
                "perform a separately bounded full candidate invocation replay against "
                "these six exact identities with an explicit version-pinned "
                "Scribunto/runtime boundary"
            ),
        },
        "historical_transclusion_proven": False,
        "offline_version_pinned_runtime_proven": False,
        "renderer_semantics_complete": False,
        "renderer_implementation_ready": False,
        "literary_body_count_and_digests_frozen": False,
        "minimum_300k_proved": False,
        "fantlab_source_edition_match": "unknown",
        "m2_parity_admissible": False,
    }
    evidence["evidence_sha256"] = _sha256_json(evidence)
    return evidence


def validate_evidence(evidence: Mapping[str, object]) -> None:
    expected = build_evidence()
    if dict(evidence) != expected:
        raise ValueError("Darwin VAR provider revision identity evidence drift")

    unsigned = dict(evidence)
    stored = unsigned.pop("evidence_sha256", None)
    if not isinstance(stored, str) or not _HEX64_RE.fullmatch(stored):
        raise ValueError("evidence SHA-256 missing or invalid")
    if _sha256_json(unsigned) != stored:
        raise ValueError("evidence self-digest drift")

    resources = evidence.get("resources")
    if not isinstance(resources, list) or len(resources) != 6:
        raise ValueError("exact six-revision identity set required")
    for item in resources:
        if not isinstance(item, dict):
            raise ValueError("revision identity row must be an object")
        mediawiki_sha1 = item.get("mediawiki_sha1")
        if not isinstance(mediawiki_sha1, str) or not _HEX40_RE.fullmatch(mediawiki_sha1):
            raise ValueError("provider MediaWiki SHA-1 missing or invalid")
        wikitext_sha256 = item.get("wikitext_sha256")
        if not isinstance(wikitext_sha256, str) or not _HEX64_RE.fullmatch(wikitext_sha256):
            raise ValueError("wikitext SHA-256 missing or invalid")
        if not isinstance(item.get("page_id"), int) or int(item["page_id"]) <= 0:
            raise ValueError("provider page id missing or invalid")
        timestamp = item.get("revision_timestamp")
        if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
            raise ValueError("revision timestamp missing or invalid")

    gate = evidence.get("identity_gate")
    if not isinstance(gate, dict):
        raise ValueError("identity gate missing")
    if gate.get("revision_ids_complete") is not True:
        raise ValueError("revision IDs must be complete")
    if gate.get("mediawiki_sha1_complete") is not True:
        raise ValueError("MediaWiki SHA-1 identities must be complete")
    if gate.get("provider_title_aliases_explicit") is not True:
        raise ValueError("provider title aliases must be explicit")
    if gate.get("missing_mediawiki_sha1_titles") != []:
        raise ValueError("no MediaWiki SHA-1 identity may remain missing")
    if gate.get("replay_ready") is not False:
        raise ValueError("full replay gate must remain closed")

    for key in (
        "historical_transclusion_proven",
        "offline_version_pinned_runtime_proven",
        "renderer_semantics_complete",
        "renderer_implementation_ready",
        "literary_body_count_and_digests_frozen",
        "minimum_300k_proved",
        "m2_parity_admissible",
    ):
        if evidence.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if evidence.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")

    decision = evidence.get("promotion_decision")
    if not isinstance(decision, dict):
        raise ValueError("promotion decision missing")
    for key in (
        "full_var_candidate_branch_replayed",
        "render_profile_rule_promoted",
        "backlog_item_removed",
        "effective_backlog_changed",
    ):
        if decision.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if decision.get("var_invocations_unresolved") != 388:
        raise ValueError("VAR unresolved invocation count drift")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    evidence = build_evidence()
    validate_evidence(evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(evidence["evidence_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
