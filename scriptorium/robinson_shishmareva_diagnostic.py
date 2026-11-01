"""Reproducible, source-free 29-field measurement of Shishmareva's Robinson Crusoe.

This is a derived Russian-translation diagnostic, NOT a verified FantLab source
match, reconstructed English original, or cross-translation parity claim.
All source prose lives only in transient memory during the exact-oldid replay.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import isfinite
from pathlib import Path
from typing import Callable, Mapping, Sequence

from . import robinson_shishmareva_body as pinned
from .metrics import METRIC_CONTRACT_ID, SCHEMA_VERSION, analyze_deterministic_metrics
from .text import normalize_text

PROFILE = "scriptorium-robinson-shishmareva-measured-v1"
SCHEMA = "scriptorium-robinson-shishmareva-diagnostic-v1"
_UNBOUND = frozenset({
    "fantlab.vocabulary.active_dictionary",
    "fantlab.vocabulary.active_nondictionary",
    "fantlab.vocabulary.uasz_3000",
    "fantlab.vocabulary.uasz_10000",
    "fantlab.vocabulary.uasz_100000",
})


def build_diagnostic(
    inventory: Mapping[str, object],
    frozen_body: Mapping[str, object],
    *,
    fetcher: Callable[..., dict[str, object]] = pinned.fetch_pinned_wikitext,
) -> dict[str, object]:
    """Replay exact source+body, then analyze transient bytes without saving prose."""
    transient: dict[str, str] = {}

    def capture(**kwargs: object) -> dict[str, object]:
        response = fetcher(**kwargs)
        if not isinstance(response, dict) or not isinstance(response.get("wikitext"), str):
            raise ValueError("pinned revision did not return transient wikitext")
        transient["wikitext"] = response["wikitext"]
        return dict(response)

    # The existing extractor validates oldid, page ID, source digest, body shape
    # and size before this measurement is permitted.
    verified = pinned.build_manifest(inventory, fetcher=capture)
    if verified != frozen_body:
        raise ValueError("saved Shishmareva body manifest differs from exact replay")
    if (
        verified.get("schema_version") != pinned.SCHEMA
        or verified.get("candidate_id") != pinned.CANDIDATE_ID
        or verified.get("m2_contribution") != 0
        or verified.get("m2_parity_admissible") is not False
        or verified.get("admitted_for_calibration") is not False
        or verified.get("fantlab_analyzer_input_identity") != "UNKNOWN"
        or verified.get("print_edition_collation") != "NOT_RUN"
        or verified.get("corpus_threshold_verified") is not True
    ):
        raise ValueError("frozen scientific gates must not be silently upgraded")

    # Re-extract instead of using an unchecked caller-supplied text string.
    raw_body = pinned.extract_literary_body(transient["wikitext"])
    normalized = normalize_text(raw_body)
    body_id = verified["literary_body_identity"]
    if not isinstance(body_id, dict) or (
        len(raw_body) != body_id.get("character_count_including_spaces")
        or len(raw_body.encode("utf-8")) != body_id.get("utf8_byte_count")
        or sha256(raw_body.encode("utf-8")).hexdigest() != body_id.get("raw_sha256")
        or len(normalized) != body_id.get("normalized_character_count_including_spaces")
        or sha256(normalized.encode("utf-8")).hexdigest() != body_id.get("normalized_sha256")
        or len(raw_body) < 300_000
    ):
        raise ValueError("measured literary body no longer matches frozen identities")
    result = analyze_deterministic_metrics(raw_body)
    metrics = result.get("metrics")
    if (
        result.get("schema_version") != SCHEMA_VERSION
        or result.get("metric_contract_id") != METRIC_CONTRACT_ID
        or result.get("normalized_sha256") != body_id["normalized_sha256"]
        or result.get("dependencies", {}).get("vocabulary_dictionary") is not None
        or not isinstance(metrics, dict)
        or len(metrics) != 29
        or metrics.get("fantlab.general.characters", {}).get("value") != len(normalized)
    ):
        raise ValueError("unexpected deterministic metric contract, normalization or dependencies")

    rows = []
    for metric_id, metric in sorted(metrics.items()):
        if not isinstance(metric, dict):
            raise ValueError("invalid measured metric")
        value = metric.get("value")
        if value is not None and (type(value) not in (int, float) or not isfinite(value)):
            raise ValueError("nonfinite or nonnumeric measurement")
        if metric_id in _UNBOUND and value is not None:
            raise ValueError("dictionary-dependent metric measured with no dictionary")
        if value is None and metric_id not in _UNBOUND and not metric_id.startswith("fantlab.dialogue."):
            raise ValueError("unexpected missing metric value")
        rows.append({
            "metric_id": metric_id,
            "actual": value,
            "unit": metric.get("unit"),
            "compatibility_status": metric.get("compatibility_status"),
            "fantlab_display": None,
            "result": (
                "NOT_RUN_DICTIONARY_UNBOUND" if metric_id in _UNBOUND
                else "UNAVAILABLE_NO_OBSERVATIONS" if value is None
                else "MEASURED_REFERENCE_UNAVAILABLE"
            ),
        })

    source = verified["source_revision"]
    if not isinstance(source, dict):
        raise ValueError("missing frozen source identity")
    return {
        "schema_version": SCHEMA,
        "version": PROFILE,
        "candidate_id": pinned.CANDIDATE_ID,
        "display_author": "Даниэль Дефо",
        "display_title": "Робинзон Крузо (первое повествование, том 1)",
        "original_language": "en",
        "analysis_language": "ru",
        "translator": "Мария Андреевна Шишмарёва",
        "source": {
            "url": "https://ru.wikisource.org/w/index.php?oldid=5634933",
            "revision_id": source["revision_id"],
            "page_id": source["page_id"],
            "revision_timestamp": source["timestamp_utc"],
            "mediawiki_sha1": source["mediawiki_sha1"],
            "wikitext_sha256": source["wikitext_sha256"],
            "rights_evidence": "Wikisource PD-old-70 notice; contributions have separate CC BY-SA terms",
            "edition": "ACADEMIA 1935, volume 1; first narrative; editor A. Frankovsky",
            "edition_identity_independently_matched": False,
        },
        "body": {
            "characters_including_spaces": body_id["character_count_including_spaces"],
            "utf8_byte_count": body_id["utf8_byte_count"],
            "raw_sha256": body_id["raw_sha256"],
            "normalized_characters_including_spaces": body_id["normalized_character_count_including_spaces"],
            "normalized_sha256": body_id["normalized_sha256"],
            "extraction_profile": verified["extraction"]["profile"],
        },
        "scriptorium": {
            "schema_version": result["schema_version"],
            "metric_contract_id": result["metric_contract_id"],
            "profiles": result["profiles"],
            "vocabulary_dictionary_dependency": None,
        },
        "metric_rows": rows,
        "numeric_metric_count": sum(row["actual"] is not None for row in rows),
        "unavailable_metric_count": sum(row["actual"] is None for row in rows),
        "gates": {
            "literary_body_source_replay": True,
            "minimum_300000_characters": True,
            "source_text_committed": False,
            "print_edition_collation": "NOT_RUN",
            "fantlab_input_identity": "UNKNOWN",
            "comparison_with_trusov": "NOT_RUN",
            "comparison_class": "DIAGNOSTIC_ONLY",
            "m2_parity_admissible": False,
            "m2_weight": 0,
            "corpus_admitted_for_calibration": False,
        },
    }


def render_json(result: Mapping[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("capture", "replay"))
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--body-manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Source-free JSON, create-only or exact replay")
    args = parser.parse_args(argv)
    if args.mode == "capture" and args.output.resolve() in {
        args.inventory.resolve(), args.body_manifest.resolve()
    }:
        parser.error("output must not overwrite pinned evidence")
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    frozen_body = json.loads(args.body_manifest.read_text(encoding="utf-8"))
    artifact = render_json(build_diagnostic(inventory, frozen_body))
    if args.mode == "capture":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(artifact)
    else:
        if args.output.read_bytes() != artifact.encode("utf-8"):
            raise ValueError("source-free measurement differs from exact pinned replay")
    print("SHISHMAREVA_MEASURED=PASS; fields=29; M2=0/5; source_text_committed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
