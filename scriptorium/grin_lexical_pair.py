"""Source-verified two-book Grin lexical contrast; no literary text is retained.

Replays the frozen public-domain Wikisource witnesses, then passes transient
text to the versioned private lexical extension. No FantLab parity or
automatic Pages publication is claimed.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

from .analyze import _write_new
from .lexical_contrast import build_lexical_contrast, render_lexical_contrast
from . import road_nowhere_freeze as road
from . import road_nowhere_diagnostic as road_diagnostic
from . import running_waves_body as waves
from .wikisource_replay import fetch_pinned_chapter_revisions

SCHEMA = "scriptorium-grin-frozen-lexical-pair-v1"
ROAD_EDITION = "grin-road-nowhere-azlib-oldid-5585836"
WAVES_EDITION = "grin-running-waves-detlit-1965-revision-composite"


def _check_body(text: str, identity: Mapping[str, object]) -> None:
    raw = text.encode("utf-8")
    if (
        len(text) != identity.get("character_count_including_spaces")
        or len(raw) != identity.get("utf8_byte_count")
        or sha256(raw).hexdigest() != identity.get("raw_sha256")
    ):
        raise ValueError("frozen Grin literary body identity drift")


def _assemble(road_text: str, waves_text: str, road_identity: Mapping[str, object],
              waves_identity: Mapping[str, object]) -> dict[str, object]:
    """Pure source-free projection; independently testable with fake texts."""
    _check_body(road_text, road_identity)
    _check_body(waves_text, waves_identity)
    report = build_lexical_contrast(
        road_text, waves_text,
        left_edition_id=ROAD_EDITION,
        right_edition_id=WAVES_EDITION,
        left_original_work_id="grin-road-nowhere",
        right_original_work_id="grin-running-waves",
    )
    if (report["status"] != "COMPARABLE" or report["aggregate"] is None or
            report["left"]["normalized_sha256"] != road_identity["normalized_sha256"] or
            report["right"]["normalized_sha256"] != waves_identity["normalized_sha256"]):
        raise ValueError("frozen Grin lexical contrast was not comparable")
    # Reuse fail-closed stored-export validation; no per-form strings or hashes.
    render_lexical_contrast(report, "json")
    return {
        "schema_version": SCHEMA,
        "status": "FROZEN_PUBLIC_DOMAIN_PAIR_DIAGNOSTIC",
        "source_text_included": False,
        "fantlab_analyzer_input_match": "UNKNOWN",
        "m2_parity_admissible": False,
        "public_reader_release": "REQUIRES_SEPARATE_REVIEW",
        "source_evidence": {
            "left": {"source": "Russian Wikisource oldid 5585836 / az.lib family",
                     "revision_id": 5585836,
                     "normalized_sha256": road_identity["normalized_sha256"],
                     "characters_including_spaces": road_identity["character_count_including_spaces"]},
            "right": {"source": "Russian Wikisource / 36 pinned 1965-family pages",
                      "literary_page_count": 36,
                      "normalized_sha256": waves_identity["normalized_sha256"],
                      "characters_including_spaces": waves_identity["character_count_including_spaces"]},
            "legal_basis": "public-domain original Russian works; see frozen candidate manifests",
            "edition_relationship_to_fantlab": "UNKNOWN",
        },
        "lexical_contrast": report,
    }


def build_pinned_pair(
    road_revision: Mapping[str, object], road_body: Mapping[str, object],
    waves_source: Mapping[str, object], waves_body: Mapping[str, object], *,
    road_fetcher: Callable[..., dict[str, object]] = road.fetch_pinned_wikitext,
    waves_fetcher: Callable[[Iterable[Mapping[str, object]]], dict[str, str]] = fetch_pinned_chapter_revisions,
) -> dict[str, object]:
    """Recheck exact revision/body witnesses and public-domain basis before output."""
    road_diagnostic._validate_pins(road_revision, road_body)
    waves.validate_manifest(waves_body, waves_source)
    if (road_revision.get("legal_basis") != "public_domain" or
            waves_source.get("legal_basis") !=
            "public_domain_original_russian_work_with_wikisource_reuse_terms" or
            waves_body.get("corpus_admission", {}).get("general_calibration_profile_admissible") is not True):
        raise ValueError("Grin source rights or calibration gate not established")

    captured_road: dict[str, object] = {}
    def capture_road(*, title: str, revision_id: int) -> dict[str, object]:
        if captured_road:
            raise ValueError("duplicate Road to Nowhere fetch")
        observed = road_fetcher(title=title, revision_id=revision_id)
        if type(observed) is not dict or type(observed.get("wikitext")) is not str:
            raise ValueError("invalid Road to Nowhere source response")
        captured_road.update(observed)
        return observed

    receipt = road.replay_body_manifest(road_revision, road_body, fetcher=capture_road)
    if receipt.get("verified") is not True or not captured_road:
        raise ValueError("Road to Nowhere source replay unverified")
    road_text = road.extract_literary_body(captured_road["wikitext"])

    captured_waves: dict[str, str] | None = None
    def capture_waves(identities: Iterable[Mapping[str, object]]) -> dict[str, str]:
        nonlocal captured_waves
        if captured_waves is not None:
            raise ValueError("duplicate Running on Waves fetch")
        observed = waves_fetcher(identities)
        if (type(observed) is not dict or any(
            type(key) is not str or type(value) is not str
            for key, value in observed.items()
        )):
            raise ValueError("invalid Running on Waves source response")
        captured_waves = observed
        return observed

    receipt = waves.replay_manifest(waves_body, waves_source, fetcher=capture_waves)
    if receipt.get("verified") is not True or captured_waves is None:
        raise ValueError("Running on Waves source replay unverified")
    _, bodies = waves._extract_bodies(waves_source, fetcher=lambda _ids: captured_waves)
    waves_text = waves.CHAPTER_SEPARATOR.join(bodies)
    left_identity = road_body["literary_body_identity"]
    right_identity = waves_body["composite_identity"]
    if (left_identity.get("character_count_including_spaces", 0) < 300_000 or
            right_identity.get("character_count_including_spaces", 0) < 300_000):
        raise ValueError("Grin source falls below corpus calibration floor")
    return _assemble(road_text, waves_text, left_identity, right_identity)


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise ValueError("Grin source manifest must be a JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--road-revision", type=Path, required=True)
    parser.add_argument("--road-body", type=Path, required=True)
    parser.add_argument("--waves-source", type=Path, required=True)
    parser.add_argument("--waves-body", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--html-output", type=Path)
    args = parser.parse_args(argv)
    artifact = build_pinned_pair(_load(args.road_revision), _load(args.road_body),
                                 _load(args.waves_source), _load(args.waves_body))
    serialized = json.dumps(artifact, ensure_ascii=False, sort_keys=True,
                            indent=2, allow_nan=False) + "\n"
    html = render_lexical_contrast(artifact["lexical_contrast"], "html")
    _write_new(args.output, serialized)
    if args.html_output:
        _write_new(args.html_output, html)
    print("GRIN_LEXICAL_PAIR_SOURCE_FREE=PASS; M2=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
