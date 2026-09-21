"""Freeze source-free evidence for Darwin/Rachinsky {{ё}} semantics and replay dependencies.

This unit records what official Russian Wikisource documentation says about the
zero-argument ``{{ё}}`` shorthand and what official MediaWiki documentation says
about rendering an old page revision: page ``oldid`` freezes the page wikitext,
while transcluded templates remain live/current unless separately version-pinned.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping, Sequence


EVIDENCE_VERSION = "scriptorium-darwin-template-yo-documentation-evidence-v2"
CANDIDATE_ID = "darwin-origin-species-rachinsky-1864-ru"
BACKLOG_VERSION = "scriptorium-darwin-render-semantic-backlog-v1"
DOCUMENTATION_REVISION_ID = 5090323
DOCUMENTATION_REVISION_DATE = "2024-01-11"
DOCUMENTATION_TITLE = "Шаблон:ЕЁ/Документация"
DOCUMENTATION_URL = (
    "https://ru.wikisource.org/w/index.php?title=Шаблон:ЕЁ/Документация"
    f"&oldid={DOCUMENTATION_REVISION_ID}"
)
HELP_REVISION_ID = 5731079
HELP_REVISION_DATE = "2026-07-19"
HELP_TITLE = "Справка:Вычитка"
HELP_URL = (
    "https://ru.wikisource.org/w/index.php?title=Справка:Вычитка"
    f"&oldid={HELP_REVISION_ID}"
)
MEDIAWIKI_HISTORY_REVISION_ID = 8524540
MEDIAWIKI_HISTORY_REVISION_DATE = "2026-07-25"
MEDIAWIKI_HISTORY_TITLE = "Help:History"
MEDIAWIKI_HISTORY_URL = (
    "https://www.mediawiki.org/w/index.php?title=Help:History"
    f"&oldid={MEDIAWIKI_HISTORY_REVISION_ID}"
)
MEDIAWIKI_TRANSCLUSION_REVISION_ID = 8551508
MEDIAWIKI_TRANSCLUSION_REVISION_DATE = "2026-08-09"
MEDIAWIKI_TRANSCLUSION_TITLE = "Transclusion/en"
MEDIAWIKI_TRANSCLUSION_URL = (
    "https://www.mediawiki.org/w/index.php?title=Transclusion/en"
    f"&oldid={MEDIAWIKI_TRANSCLUSION_REVISION_ID}"
)
RESEARCH_DATE = "2026-09-21"


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _verified_backlog_sha(backlog: Mapping[str, object]) -> str:
    """Verify the semantic backlog self-digest before deriving evidence from it."""

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
    next_slice = backlog.get("next_research_slice")
    if not isinstance(next_slice, dict):
        raise ValueError("Darwin semantic backlog next slice missing")
    expected = {
        "source_kind": "template",
        "name": "ё",
        "positional": 0,
        "named": 0,
        "count": 2227,
        "semantic_status": "unresolved",
    }
    for key, value in expected.items():
        if next_slice.get(key) != value:
            raise ValueError(f"Darwin {{ё}} research target drift: {key}")
    items = backlog.get("prioritized_items")
    if not isinstance(items, list) or not items or not isinstance(items[0], dict):
        raise ValueError("Darwin semantic backlog priority rows missing")
    first = items[0]
    for key, value in expected.items():
        if first.get(key) != value:
            raise ValueError(f"Darwin {{ё}} priority row drift: {key}")
    if first.get("priority_rank") != 1:
        raise ValueError("Darwin {{ё}} priority rank drift")
    return {**expected, "backlog_priority_rank": 1}


def _page_revision_context(shard: Mapping[str, object]) -> dict[str, object]:
    """Retain one exact old Page revision as context, not as a template binding."""

    rows = shard.get("page_identities")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Darwin page-revision shard missing identities")
    valid: list[tuple[int, int, str, str]] = []
    for raw in rows:
        if (
            isinstance(raw, list)
            and len(raw) == 4
            and isinstance(raw[0], int)
            and isinstance(raw[1], int)
            and isinstance(raw[2], str)
            and isinstance(raw[3], str)
        ):
            valid.append((raw[0], raw[1], raw[2], raw[3]))
    if len(valid) != len(rows):
        raise ValueError("Darwin page-revision shard row drift")
    before_docs = [row for row in valid if row[2][:10] < DOCUMENTATION_REVISION_DATE]
    if not before_docs:
        raise ValueError("no retained Darwin Page revision predates documentation evidence")
    page_sequence, revision_id, timestamp, mediawiki_sha1 = min(
        before_docs, key=lambda row: (row[2], row[0], row[1])
    )
    return {
        "page_sequence": page_sequence,
        "revision_id": revision_id,
        "revision_timestamp": timestamp,
        "mediawiki_sha1": mediawiki_sha1,
        "documentation_revision_postdates_page_revision": True,
        "page_oldid_binds_transcluded_template_revision": False,
    }


def build_evidence(
    backlog: Mapping[str, object],
    page_revision_shard: Mapping[str, object],
) -> dict[str, object]:
    """Build deterministic source-free documentation/replay evidence."""

    backlog_sha = _verified_backlog_sha(backlog)
    target = _target_from_backlog(backlog)
    page_context = _page_revision_context(page_revision_shard)

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
            "evidence_scope": "documented_semantics_at_revision_not_replay_dependency_identity",
        },
        "proofread_help": {
            "provider": "Russian Wikisource",
            "title": HELP_TITLE,
            "revision_id": HELP_REVISION_ID,
            "revision_date": HELP_REVISION_DATE,
            "permanent_url": HELP_URL,
            "researched_on": RESEARCH_DATE,
            "evidence_scope": "current_workflow_documentation",
        },
        "mediawiki_rendering_model": {
            "provider": "MediaWiki.org",
            "researched_on": RESEARCH_DATE,
            "old_revision_rendering": {
                "title": MEDIAWIKI_HISTORY_TITLE,
                "revision_id": MEDIAWIKI_HISTORY_REVISION_ID,
                "revision_date": MEDIAWIKI_HISTORY_REVISION_DATE,
                "permanent_url": MEDIAWIKI_HISTORY_URL,
                "evidence_scope": (
                    "old_page_revision_rendering_uses_current_template_and_image_versions"
                ),
                "current_template_versions_used": True,
            },
            "transclusion_model": {
                "title": MEDIAWIKI_TRANSCLUSION_TITLE,
                "revision_id": MEDIAWIKI_TRANSCLUSION_REVISION_ID,
                "revision_date": MEDIAWIKI_TRANSCLUSION_REVISION_DATE,
                "permanent_url": MEDIAWIKI_TRANSCLUSION_URL,
                "evidence_scope": "live_transclusion_and_no_versioned_transclusion_support",
                "live_link_updates_targets_when_template_changes": True,
                "versioned_transclusion_supported": False,
                "phabricator_reference": "T31051",
            },
        },
        "documented_semantics": {
            "template_family": "ЕЁ conditional yoification family",
            "invocation": "{{ё}}",
            "arity": {"positional": 0, "named": 0},
            "output_kind": "conditional_single_character",
            "forced_yoification_output": "ё",
            "non_forced_yoification_output": "е",
            "proofread_help_role": (
                "marks yoification so finished text can support yoified and non-yoified variants"
            ),
            "historical_equivalence_proven": False,
        },
        "page_revision_context": page_context,
        "promotion_decision": {
            "render_profile_rule_promoted": False,
            "backlog_item_removed": False,
            "page_save_time_template_lookup_required": False,
            "reason": (
                "official MediaWiki history semantics show that an old page revision renders "
                "with current template/image versions, so Page-save-time template revisions "
                "do not bind deterministic replay; documented {{ё}} semantics still need an "
                "exact replay-time dependency freeze before promotion"
            ),
            "next_evidence_required": (
                "freeze exact Шаблон:ё and Шаблон:ЕЁ revisions plus nested dependencies used "
                "by the chosen replay/rendering environment at analysis time, or use an "
                "explicitly version-pinned template expansion mechanism, then validate the "
                "conditional outputs before renderer-profile promotion"
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
    page_revision_shard: Mapping[str, object],
) -> None:
    expected = build_evidence(backlog, page_revision_shard)
    if dict(manifest) != expected:
        raise ValueError("Darwin {{ё}} documentation evidence drift")
    if manifest.get("source_text_included") is not False:
        raise ValueError("Darwin {{ё}} evidence must remain source-free")
    target = manifest.get("target")
    if not isinstance(target, dict) or target.get("semantic_status") != "unresolved":
        raise ValueError("Darwin {{ё}} backlog target must remain unresolved")
    semantics = manifest.get("documented_semantics")
    if not isinstance(semantics, dict) or semantics.get("historical_equivalence_proven") is not False:
        raise ValueError("historical {{ё}} equivalence must remain unproven")
    rendering = manifest.get("mediawiki_rendering_model")
    if not isinstance(rendering, dict):
        raise ValueError("MediaWiki rendering evidence missing")
    old_revision = rendering.get("old_revision_rendering")
    transclusion = rendering.get("transclusion_model")
    if not isinstance(old_revision, dict) or old_revision.get("current_template_versions_used") is not True:
        raise ValueError("oldid current-template rendering evidence drift")
    if not isinstance(transclusion, dict) or transclusion.get("versioned_transclusion_supported") is not False:
        raise ValueError("versioned-transclusion evidence drift")
    page_context = manifest.get("page_revision_context")
    if not isinstance(page_context, dict) or page_context.get("page_oldid_binds_transcluded_template_revision") is not False:
        raise ValueError("Page oldid must not be treated as a template revision binding")
    decision = manifest.get("promotion_decision")
    if (
        not isinstance(decision, dict)
        or decision.get("render_profile_rule_promoted") is not False
        or decision.get("backlog_item_removed") is not False
        or decision.get("page_save_time_template_lookup_required") is not False
    ):
        raise ValueError("Darwin {{ё}} profile/backlog promotion must remain closed")
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
            raise ValueError(f"{key} must remain false in Darwin {{ё}} evidence")
    if manifest.get("fantlab_source_edition_match") != "unknown":
        raise ValueError("FantLab source match must remain unknown")
    forbidden = {"wikitext", "content", "body", "text", "source_text", "rendered_prose"}
    if forbidden.intersection(manifest):
        raise ValueError("source prose leaked into Darwin {{ё}} evidence")


def build_evidence_from_paths(backlog_path: Path, shard_path: Path) -> dict[str, object]:
    backlog = json.loads(backlog_path.read_text(encoding="utf-8"))
    shard = json.loads(shard_path.read_text(encoding="utf-8"))
    if not isinstance(backlog, dict) or not isinstance(shard, dict):
        raise ValueError("Darwin {{ё}} evidence inputs must be JSON objects")
    return build_evidence(backlog, shard)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backlog", type=Path, required=True)
    parser.add_argument("--page-revision-shard", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = build_evidence_from_paths(args.backlog, args.page_revision_shard)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(manifest["evidence_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
