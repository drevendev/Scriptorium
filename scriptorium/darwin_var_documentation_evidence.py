"""Freeze source-free documentation evidence for Darwin/Rachinsky ``{{ВАР}}``.

This unit records revision-pinned Russian Wikisource documentation and one pinned
implementation-module revision for the next unresolved Darwin renderer shape. It
intentionally does not bind the live template root, Module:Header, historical
transclusion, or a complete replay runtime, so profile/backlog promotion remains
closed.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence


EVIDENCE_VERSION = "scriptorium-darwin-var-documentation-evidence-v1"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
BACKLOG_VERSION = "scriptorium-darwin-render-semantic-backlog-v3"
DOCUMENTATION_TITLE = "Шаблон:ВАР/Документация"
DOCUMENTATION_REVISION_ID = 5711068
DOCUMENTATION_REVISION_DATE = "2026-05-11"
DOCUMENTATION_URL = (
    "https://ru.wikisource.org/w/index.php?title=Шаблон:ВАР/Документация"
    f"&oldid={DOCUMENTATION_REVISION_ID}"
)
MODULE_TITLE = "Модуль:Дореформенная орфография"
MODULE_REVISION_ID = 5721277
MODULE_REVISION_DATE = "2026-06-08"
MODULE_URL = (
    "https://ru.wikisource.org/w/index.php?title="
    "Модуль:Дореформенная_орфография"
    f"&oldid={MODULE_REVISION_ID}"
)
RESEARCH_DATE = "2026-09-24"


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _verified_backlog_sha(backlog: Mapping[str, object]) -> str:
    stored = backlog.get("backlog_sha256")
    if not isinstance(stored, str) or len(stored) != 64:
        raise ValueError("Darwin semantic backlog digest missing")
    unsigned = dict(backlog)
    unsigned.pop("backlog_sha256", None)
    actual = _sha256_json(unsigned)
    if actual != stored:
        raise ValueError("Darwin semantic backlog digest drift")
    return stored


def _target_from_backlog(backlog: Mapping[str, object]) -> dict[str, object]:
    if backlog.get("schema_version") != BACKLOG_VERSION:
        raise ValueError("Darwin semantic backlog schema drift")
    if backlog.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Darwin semantic backlog candidate drift")
    expected = {
        "source_kind": "template",
        "name": "ВАР",
        "positional": 2,
        "named": 0,
        "count": 388,
        "semantic_status": "unresolved",
    }
    next_slice = backlog.get("next_research_slice")
    if not isinstance(next_slice, dict):
        raise ValueError("Darwin semantic backlog next slice missing")
    for key, value in expected.items():
        if next_slice.get(key) != value:
            raise ValueError(f"Darwin {{ВАР}} research target drift: {key}")
    if next_slice.get("priority_rank") != 1:
        raise ValueError("Darwin {{ВАР}} priority rank drift")
    return {**expected, "backlog_priority_rank": 1}


def build_evidence(backlog: Mapping[str, object]) -> dict[str, object]:
    """Build deterministic source-free documentation evidence."""

    backlog_sha = _verified_backlog_sha(backlog)
    target = _target_from_backlog(backlog)

    manifest: dict[str, object] = {
        "schema_version": EVIDENCE_VERSION,
        "candidate_id": CANDIDATE_ID,
        "source_text_included": False,
        "source_backlog": {
            "schema_version": BACKLOG_VERSION,
            "backlog_sha256": backlog_sha,
        },
        "target": target,
        "official_documentation": {
            "provider": "Russian Wikisource",
            "title": DOCUMENTATION_TITLE,
            "revision_id": DOCUMENTATION_REVISION_ID,
            "revision_date": DOCUMENTATION_REVISION_DATE,
            "permanent_url": DOCUMENTATION_URL,
            "researched_on": RESEARCH_DATE,
            "evidence_scope": (
                "documented_parameter_roles_and_template_to_module_relationship"
            ),
        },
        "implementation_module": {
            "provider": "Russian Wikisource",
            "title": MODULE_TITLE,
            "revision_id": MODULE_REVISION_ID,
            "revision_date": MODULE_REVISION_DATE,
            "permanent_url": MODULE_URL,
            "researched_on": RESEARCH_DATE,
            "evidence_scope": (
                "documented_current_module_branch_behavior_not_historical_template_binding"
            ),
            "direct_dependency_titles": ["Module:Header"],
        },
        "documented_semantics": {
            "invocation_family": "{{ВАР|pre_reform|modern}}",
            "arity": {"positional": 2, "named": 0},
            "first_parameter_role": "pre_reform_text",
            "second_parameter_role": "modern_text",
            "page_namespace_behavior": (
                "emit_both_variants_with_generated_references_and_divider"
            ),
            "non_page_namespace_behavior": (
                "delegate_title_classification_to_Module_Header_parse_title_isPRS_"
                "then_select_one_variant"
            ),
            "isPRS_true_output": "first_parameter_pre_reform",
            "isPRS_false_output": "second_parameter_modern",
            "historical_equivalence_proven": False,
            "candidate_mainspace_branch_replayed": False,
        },
        "dependency_boundary": {
            "template_root_revision_frozen": False,
            "implementation_module_revision_documented": True,
            "module_header_revision_frozen": False,
            "nested_dependency_closure_frozen": False,
            "offline_version_pinned_runtime_proven": False,
            "reason": (
                "the pinned module source directly requires Module:Header, while this "
                "unit does not bind the live Шаблон:ВАР root or Module:Header/nested "
                "runtime identities"
            ),
        },
        "promotion_decision": {
            "render_profile_rule_promoted": False,
            "backlog_item_removed": False,
            "reason": (
                "documentation and one module revision explain branch semantics but do "
                "not replay the selected candidate context or freeze the complete "
                "replay-time dependency graph"
            ),
            "next_evidence_required": (
                "freeze exact Шаблон:ВАР, Модуль:Дореформенная орфография, "
                "Module:Header and nested dependency identities for one chosen replay "
                "snapshot, then replay the candidate mainspace title/context before "
                "any profile promotion"
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
    manifest["evidence_sha256"] = _sha256_json(manifest)
    return manifest


def validate_evidence(
    manifest: Mapping[str, object],
    backlog: Mapping[str, object],
) -> None:
    expected = build_evidence(backlog)
    if dict(manifest) != expected:
        raise ValueError("Darwin {{ВАР}} documentation evidence drift")
    if manifest.get("source_text_included") is not False:
        raise ValueError("Darwin {{ВАР}} evidence must remain source-free")
    semantics = manifest.get("documented_semantics")
    if not isinstance(semantics, dict):
        raise ValueError("Darwin {{ВАР}} documented semantics missing")
    if semantics.get("historical_equivalence_proven") is not False:
        raise ValueError("historical {{ВАР}} equivalence must remain unproven")
    if semantics.get("candidate_mainspace_branch_replayed") is not False:
        raise ValueError("candidate {{ВАР}} mainspace branch must remain unreplayed")
    boundary = manifest.get("dependency_boundary")
    if not isinstance(boundary, dict):
        raise ValueError("Darwin {{ВАР}} dependency boundary missing")
    for key in (
        "template_root_revision_frozen",
        "module_header_revision_frozen",
        "nested_dependency_closure_frozen",
        "offline_version_pinned_runtime_proven",
    ):
        if boundary.get(key) is not False:
            raise ValueError(f"{key} must remain false in Darwin {{ВАР}} evidence")
    if boundary.get("implementation_module_revision_documented") is not True:
        raise ValueError("pinned {{ВАР}} implementation-module evidence missing")
    decision = manifest.get("promotion_decision")
    if (
        not isinstance(decision, dict)
        or decision.get("render_profile_rule_promoted") is not False
        or decision.get("backlog_item_removed") is not False
    ):
        raise ValueError("Darwin {{ВАР}} promotion must remain closed")
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
        if manifest.get(key) is not False:
            raise ValueError(f"{key} must remain false in Darwin {{ВАР}} evidence")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")
    forbidden = {"wikitext", "content", "body", "text", "source_text", "rendered_prose"}
    if forbidden.intersection(manifest):
        raise ValueError("source prose leaked into Darwin {{ВАР}} evidence")


def build_evidence_from_path(backlog_path: Path) -> dict[str, object]:
    backlog = json.loads(backlog_path.read_text(encoding="utf-8"))
    if not isinstance(backlog, dict):
        raise ValueError("Darwin semantic backlog must be a JSON object")
    return build_evidence(backlog)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backlog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = build_evidence_from_path(args.backlog)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(manifest["evidence_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
