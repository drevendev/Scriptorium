"""Validate the source-free Wikisource route inventory for Grin's *Running on Waves*.

This module freezes only route topology and source-family boundaries.  It does not
fetch or serialize literary prose, pin literary-page revisions, define extraction,
or claim that FantLab analyzed either public Wikisource route.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Sequence


CANDIDATE_ID = "grin-running-on-waves-ru"
MANIFEST_VERSION = "scriptorium-running-waves-route-inventory-v1"
WORK_TITLE = "Бегущая по волнам (Грин)"
WORK_URL = "https://ru.wikisource.org/wiki/Бегущая_по_волнам_(Грин)"
WORK_INDEX_REVISION_ID = 2_595_407
CATEGORY_TITLE = "Категория:Бегущая по волнам (Грин)"
CATEGORY_URL = "https://ru.wikisource.org/wiki/Категория:Бегущая_по_волнам_(Грин)"
CATEGORY_REVISION_ID = 4_715_419
CATEGORY_PAGE_COUNT = 37
PRIMARY_BIBLIOGRAPHIC_SOURCE = (
    "А. Грин. Алые паруса. Бегущая по волнам. Золотая цепь. — "
    "М.: Дет. лит., 1965. — (Библиотека приключений)."
)
EXCLUDED_ROUTE_TITLE = f"{WORK_TITLE}/Версия 2"
EXCLUDED_ROUTE_REVISION_ID = 5_655_654
EXCLUDED_ROUTE_SOURCE = "az.lib.ru"
EXCLUDED_ROUTE_BIBLIOGRAPHIC_SOURCE = (
    "А.С. Грин. Собрание сочинений: Правда; Москва; 1980"
)


def expected_literary_titles() -> tuple[str, ...]:
    """Return the exact 35 numbered chapters plus epilogue for the 1965 route."""

    return tuple(f"{WORK_TITLE}/{number}" for number in range(1, 36)) + (
        f"{WORK_TITLE}/Эпилог",
    )


def build_manifest() -> dict[str, object]:
    """Build the deterministic source-free route-inventory witness."""

    titles = expected_literary_titles()
    return {
        "manifest_version": MANIFEST_VERSION,
        "candidate_id": CANDIDATE_ID,
        "provider": "Russian Wikisource",
        "primary_route": {
            "work_title": WORK_TITLE,
            "work_url": WORK_URL,
            "work_index_revision_id": WORK_INDEX_REVISION_ID,
            "bibliographic_source": PRIMARY_BIBLIOGRAPHIC_SOURCE,
        },
        "route_inventory_witness": {
            "category_title": CATEGORY_TITLE,
            "category_url": CATEGORY_URL,
            "category_revision_id": CATEGORY_REVISION_ID,
            "listed_page_count": CATEGORY_PAGE_COUNT,
            "main_page_title": WORK_TITLE,
            "literary_subpage_count": len(titles),
            "literary_titles": list(titles),
            "witness_scope": (
                "The permanent category revision witnesses the listed route topology "
                "only; it does not freeze the literary subpages' revision/content identities."
            ),
        },
        "excluded_distinct_routes": [
            {
                "title": EXCLUDED_ROUTE_TITLE,
                "revision_id": EXCLUDED_ROUTE_REVISION_ID,
                "source": EXCLUDED_ROUTE_SOURCE,
                "bibliographic_source": EXCLUDED_ROUTE_BIBLIOGRAPHIC_SOURCE,
                "relationship": "distinct_transcription_route_not_composed_into_primary",
            }
        ],
        "capture_scope": {
            "route_inventory_frozen": True,
            "literary_page_revisions_frozen": False,
            "literary_body_extraction_frozen": False,
            "composite_identity_frozen": False,
            "source_text_committed": False,
            "fantlab_source_edition_match": "unknown",
        },
    }


def validate_manifest(manifest: Mapping[str, object]) -> tuple[str, ...]:
    """Fail closed on route drift and return the admitted literary titles."""

    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("unsupported Running on Waves route-inventory version")
    if manifest.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("unexpected Running on Waves candidate id")
    if manifest.get("provider") != "Russian Wikisource":
        raise ValueError("unexpected provider")

    primary = manifest.get("primary_route")
    if not isinstance(primary, dict):
        raise ValueError("route inventory missing primary_route")
    expected_primary = {
        "work_title": WORK_TITLE,
        "work_url": WORK_URL,
        "work_index_revision_id": WORK_INDEX_REVISION_ID,
        "bibliographic_source": PRIMARY_BIBLIOGRAPHIC_SOURCE,
    }
    if primary != expected_primary:
        raise ValueError("primary route identity drift")

    witness = manifest.get("route_inventory_witness")
    if not isinstance(witness, dict):
        raise ValueError("route inventory missing witness")
    titles = witness.get("literary_titles")
    expected_titles = expected_literary_titles()
    if not isinstance(titles, list) or tuple(titles) != expected_titles:
        raise ValueError("literary route title inventory drift")
    if len(set(titles)) != len(expected_titles):
        raise ValueError("duplicate literary route title")
    expected_witness = {
        "category_title": CATEGORY_TITLE,
        "category_url": CATEGORY_URL,
        "category_revision_id": CATEGORY_REVISION_ID,
        "listed_page_count": CATEGORY_PAGE_COUNT,
        "main_page_title": WORK_TITLE,
        "literary_subpage_count": len(expected_titles),
        "literary_titles": list(expected_titles),
        "witness_scope": (
            "The permanent category revision witnesses the listed route topology "
            "only; it does not freeze the literary subpages' revision/content identities."
        ),
    }
    if witness != expected_witness:
        raise ValueError("route inventory witness drift")

    excluded = manifest.get("excluded_distinct_routes")
    expected_excluded = [
        {
            "title": EXCLUDED_ROUTE_TITLE,
            "revision_id": EXCLUDED_ROUTE_REVISION_ID,
            "source": EXCLUDED_ROUTE_SOURCE,
            "bibliographic_source": EXCLUDED_ROUTE_BIBLIOGRAPHIC_SOURCE,
            "relationship": "distinct_transcription_route_not_composed_into_primary",
        }
    ]
    if excluded != expected_excluded:
        raise ValueError("excluded route boundary drift")

    expected_scope = {
        "route_inventory_frozen": True,
        "literary_page_revisions_frozen": False,
        "literary_body_extraction_frozen": False,
        "composite_identity_frozen": False,
        "source_text_committed": False,
        "fantlab_source_edition_match": "unknown",
    }
    if manifest.get("capture_scope") != expected_scope:
        raise ValueError("route inventory capture scope drift")
    return expected_titles


def canonical_json_text(value: Mapping[str, object]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate or emit the Running on Waves source-free route inventory."
    )
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if (args.manifest is None) == (args.output is None):
        parser.error("provide exactly one of --manifest or --output")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(canonical_json_text(build_manifest()), encoding="utf-8")
        return 0

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("route inventory manifest must be a JSON object")
    validate_manifest(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
