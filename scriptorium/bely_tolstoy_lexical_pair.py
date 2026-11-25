"""Replay a frozen cross-author lexical pair, retaining no literary prose."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from . import silver_dove_diagnostic as dove
from . import hyperboloid_diagnostic as garin
from .analyze import _write_new
from .lexical_contrast import build_lexical_contrast, render_lexical_contrast
from .wikisource_replay import fetch_pinned_chapter_revisions

SCHEMA = "scriptorium-bely-tolstoy-frozen-lexical-pair-v1"
LEFT_EDITION = "bely-silver-dove-1990-oldid-5588003"
RIGHT_EDITION = "tolstoy-hyperboloid-azlib-oldid-5014458"


def _check_body(text, identity):
    raw = text.encode("utf-8")
    if (len(text) != identity["character_count_including_spaces"]
            or len(raw) != identity["utf8_byte_count"]
            or sha256(raw).hexdigest() != identity["raw_sha256"]):
        raise ValueError("frozen lexical body identity drift")


def _assemble(left, right, left_identity, right_identity):
    _check_body(left, left_identity)
    _check_body(right, right_identity)
    report = build_lexical_contrast(
        left, right, left_edition_id=LEFT_EDITION,
        right_edition_id=RIGHT_EDITION,
        left_original_work_id="bely-silver-dove",
        right_original_work_id="tolstoy-hyperboloid-garin",
    )
    if (report["status"] != "COMPARABLE" or report["aggregate"] is None
            or report["left"]["normalized_sha256"] != left_identity["normalized_sha256"]
            or report["right"]["normalized_sha256"] != right_identity["normalized_sha256"]):
        raise ValueError("frozen cross-author lexical pair not comparable")
    render_lexical_contrast(report, "json")
    return {
        "schema_version": SCHEMA,
        "status": "FROZEN_PUBLIC_DOMAIN_PAIR_DIAGNOSTIC",
        "source_text_included": False,
        "fantlab_analyzer_input_match": "UNKNOWN",
        "m2_parity_admissible": False,
        "public_reader_release": "REQUIRES_SEPARATE_REVIEW",
        "source_evidence": {
            "left": {"revision_id": 5588003, "edition_id": LEFT_EDITION,
                     "normalized_sha256": left_identity["normalized_sha256"],
                     "characters_including_spaces": left_identity["character_count_including_spaces"]},
            "right": {"revision_id": 5014458, "edition_id": RIGHT_EDITION,
                      "normalized_sha256": right_identity["normalized_sha256"],
                      "characters_including_spaces": right_identity["character_count_including_spaces"]},
            "legal_basis": "public-domain original Russian works; frozen candidate manifests",
            "edition_relationship_to_fantlab": "UNKNOWN",
        },
        "lexical_contrast": report,
    }


def build_pinned_pair(dove_manifest, garin_revision, garin_body, *,
                      dove_fetcher=fetch_pinned_chapter_revisions,
                      garin_fetcher=garin.freeze.fetch_pinned_wikitext):
    # Validate both independent canonical pins and rights before either fetch.
    left_identity = dove._pinned_manifest(dove_manifest)
    right_identity = garin._validate_pins(garin_revision, garin_body)
    if (dove_manifest.get("legal_basis") != "public_domain"
            or garin_revision.get("legal_basis") != "public_domain"
            or any(i["character_count_including_spaces"] < 300_000
                   for i in (left_identity, right_identity))):
        raise ValueError("cross-author lexical rights or size gate not established")

    captured_left = {}
    def capture_left(identities):
        observed = dove_fetcher(identities)
        if (captured_left or type(observed) is not dict
                or set(observed) != {dove.freeze.WORK_TITLE}
                or type(observed[dove.freeze.WORK_TITLE]) is not str):
            raise ValueError("unexpected Silver Dove source inventory")
        captured_left.update(observed)
        return observed

    receipt = dove.freeze.replay_manifest(dove_manifest, fetcher=capture_left)
    if (receipt.get("source_text_included") is not False
            or receipt.get("composite_identity") != left_identity
            or receipt.get("m2_parity_admissible") is not False
            or not captured_left):
        raise ValueError("Silver Dove replay evidence drift")
    left = dove.freeze.extract_silver_dove_body(captured_left[dove.freeze.WORK_TITLE])

    captured_right = {}
    def capture_right(*, title, revision_id):
        observed = garin_fetcher(title=title, revision_id=revision_id)
        if (captured_right or type(observed) is not dict
                or type(observed.get("wikitext")) is not str):
            raise ValueError("unexpected Hyperboloid source inventory")
        captured_right.update(observed)
        return observed

    receipt = garin.freeze.replay_body_manifest(garin_revision, garin_body, fetcher=capture_right)
    if (receipt.get("verified") is not True
            or receipt.get("source_text_included") is not False
            or receipt.get("m2_parity_admissible") is not False
            or receipt.get("raw_sha256") != garin.FROZEN_BODY_SHA256
            or not captured_right):
        raise ValueError("Hyperboloid replay evidence drift")
    right = garin.freeze.extract_literary_body(captured_right["wikitext"])
    return _assemble(left, right, left_identity, right_identity)


def _load(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise ValueError("source manifest must be a JSON object")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dove-manifest", type=Path, required=True)
    parser.add_argument("--garin-revision", type=Path, required=True)
    parser.add_argument("--garin-body", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--html-output", type=Path)
    args = parser.parse_args(argv)
    artifact = build_pinned_pair(_load(args.dove_manifest),
                                 _load(args.garin_revision), _load(args.garin_body))
    serialized = json.dumps(artifact, ensure_ascii=False, sort_keys=True,
                            indent=2, allow_nan=False) + "\n"
    html = render_lexical_contrast(artifact["lexical_contrast"], "html")
    _write_new(args.output, serialized)
    if args.html_output:
        _write_new(args.html_output, html)
    print("BELY_TOLSTOY_LEXICAL_SOURCE_FREE=PASS; M2=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
