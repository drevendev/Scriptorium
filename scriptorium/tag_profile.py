"""Fail-closed, source-free tag aggregation over measured edition snapshots.

A curation assertion is not independent legal verification: generated profiles are
private research previews and are NEVER automatically eligible for publication.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import fsum, isfinite, sqrt
from pathlib import Path
import re
from urllib.parse import urlsplit

VERSION = "scriptorium-tag-profile-preview-v1"
CURATION_SCHEMA = "scriptorium-tag-curation-v1"
MIN_CHARS = 300_000
FEATURES = {
    "fantlab.general.mean_word_length_chars": "characters/word",
    "fantlab.general.mean_sentence_length_chars": "characters/sentence",
    "fantlab.dialogue.share_percent": "%",
    "fantlab.punctuation.comma.per_1000_words": "per 1000 words",
    "fantlab.punctuation.dash.per_1000_words": "per 1000 words",
}
_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,79}\Z")
_HASH = re.compile(r"[0-9a-f]{64}\Z")


def _exact(value, fields, description):
    if type(value) is not dict or set(value) != set(fields):
        raise ValueError("malformed " + description)
    return value


def _safe_text(value):
    if type(value) is not str or not value.strip() or len(value) > 160 or any(ord(c) < 32 for c in value):
        raise ValueError("invalid label")
    return value


def _url(value):
    if type(value) is not str or len(value) > 2048 or any(ord(c) < 33 for c in value):
        raise ValueError("invalid evidence URL")
    p = urlsplit(value)
    if p.scheme != "https" or not p.hostname or p.username or p.password:
        raise ValueError("evidence URL must be credential-free HTTPS")
    return value


def _edition(snapshot, claimed):
    _exact(claimed, ("key", "candidate_id", "edition_id", "source_sha256", "language",
                     "translator", "rights", "annotations"), "edition claim")
    for field in ("key", "candidate_id", "edition_id", "source_sha256", "language", "translator"):
        if claimed[field] != snapshot.get(field):
            raise ValueError("edition/source/translator mismatch: " + field)
    if type(claimed["source_sha256"]) is not str or not _HASH.fullmatch(claimed["source_sha256"]):
        raise ValueError("invalid source hash")
    if snapshot.get("text_status") != "measured" or snapshot.get("language") != "ru":
        raise ValueError("not a measured Russian edition")
    rights = _exact(claimed["rights"], ("basis", "evidence_url", "reviewed"), "rights assertion")
    if rights["basis"] not in ("public_domain", "open_license", "explicit_permission") or rights["reviewed"] is not True:
        raise ValueError("rights not curator-reviewed")
    _url(rights["evidence_url"])
    raw_metrics = snapshot.get("metrics")
    if type(raw_metrics) is not list:
        raise ValueError("missing measurement rows")
    metric_map = {}
    for row in raw_metrics:
        if type(row) is not dict or type(row.get("id")) is not str or row["id"] in metric_map:
            raise ValueError("duplicate or malformed metrics")
        metric_map[row["id"]] = row
    char_row = metric_map.get("fantlab.general.characters")
    if (not isinstance(char_row, dict) or char_row.get("status") != "measured"
            or char_row.get("kind") != "candidate" or type(char_row.get("actual")) is not int
            or char_row["actual"] < MIN_CHARS):
        raise ValueError("unverified full-length text")
    profiles = snapshot.get("profiles")
    if type(profiles) is not dict or not profiles or any(type(x) is not str for x in profiles.values()):
        raise ValueError("missing measurement profiles")
    observations = {}
    for metric, unit in FEATURES.items():
        row = metric_map.get(metric)
        if row is None:
            observations[metric] = None
            continue
        if row.get("status") == "unavailable" and row.get("actual") is None:
            observations[metric] = None
            continue
        if row.get("status") != "measured" or row.get("kind") != "candidate":
            raise ValueError("invalid observed metric status")
        val = row.get("actual")
        if type(val) not in (int, float) or not isfinite(val) or val < 0 or (unit == "%" and val > 100):
            raise ValueError("invalid observed metric")
        observations[metric] = float(val)
    return observations, profiles


def build_tag_profiles(snapshot: dict, curation: dict, *, snapshot_sha256: str) -> dict:
    """Aggregate explicitly curated confirmed tags; unknown/inferred tags are not guessed."""
    if type(snapshot_sha256) is not str or not _HASH.fullmatch(snapshot_sha256):
        raise ValueError("unbound source snapshot")
    if (type(snapshot) is not dict or snapshot.get("schema") != "scriptorium-ru-reader-v2"
            or snapshot.get("scientific_claim") != "DIAGNOSTIC_ONLY"
            or snapshot.get("fantlab_input_identity") != "UNKNOWN"
            or type(snapshot.get("counts")) is not dict
            or snapshot["counts"].get("m2_source_matched") != 0
            or type(snapshot.get("comparability")) is not dict
            or snapshot["comparability"].get("m2_parity_admissible") is not False):
        raise ValueError("unverified scientific boundary")
    _exact(curation, ("schema", "taxonomy_version", "tags", "editions"), "curation catalog")
    if curation["schema"] != CURATION_SCHEMA or not isinstance(curation["taxonomy_version"], str) or not _ID.fullmatch(curation["taxonomy_version"]):
        raise ValueError("unsupported curation schema/taxonomy")
    tags = curation["tags"]
    if type(tags) is not list or not tags:
        raise ValueError("missing curated taxonomy")
    taxonomy = {}
    for tag in tags:
        _exact(tag, ("id", "label"), "tag")
        tag_id = tag["id"]
        if type(tag_id) is not str or not _ID.fullmatch(tag_id) or tag_id in taxonomy:
            raise ValueError("invalid or duplicate tag")
        taxonomy[tag_id] = _safe_text(tag["label"])
    books = snapshot.get("books")
    if type(books) is not list:
        raise ValueError("missing source editions")
    indexed = {}
    for book in books:
        if type(book) is not dict or type(book.get("key")) is not str or book["key"] in indexed:
            raise ValueError("duplicate source edition key")
        indexed[book["key"]] = book
    claims = curation["editions"]
    if type(claims) is not list:
        raise ValueError("invalid edition claims")
    matched = {key: [] for key in taxonomy}
    seen_keys, seen_sources, seen_candidates = set(), set(), set()
    baseline_profiles = None
    for claim in claims:
        if type(claim) is not dict or type(claim.get("key")) is not str or claim["key"] not in indexed:
            raise ValueError("unknown edition in curation")
        key = claim["key"]
        if key in seen_keys:
            raise ValueError("duplicate edition claim")
        seen_keys.add(key)
        book = indexed[key]
        measurements, profiles = _edition(book, claim)
        if baseline_profiles is None:
            baseline_profiles = profiles
        elif baseline_profiles != profiles:
            raise ValueError("incompatible analysis profiles")
        if book.get("source_sha256") in seen_sources or book.get("candidate_id") in seen_candidates:
            raise ValueError("duplicate work body or work identity")
        seen_sources.add(book["source_sha256"])
        seen_candidates.add(book["candidate_id"])
        annotations = claim["annotations"]
        if type(annotations) is not list:
            raise ValueError("invalid tag annotations")
        seen_tags = set()
        for annotation in annotations:
            _exact(annotation, ("tag_id", "authority", "certainty", "evidence_url"), "annotation")
            tag_id = annotation["tag_id"]
            if type(tag_id) is not str or tag_id not in taxonomy or tag_id in seen_tags:
                raise ValueError("unknown or duplicate tag annotation")
            seen_tags.add(tag_id)
            if annotation["authority"] not in ("human_curator", "documented_source") or annotation["certainty"] not in ("confirmed", "uncertain", "inferred"):
                raise ValueError("invalid tag evidence status")
            _url(annotation["evidence_url"])
            if annotation["certainty"] != "confirmed":
                continue
            matched[tag_id].append({"key": key, "candidate_id": book["candidate_id"],
                                    "edition_id": book["edition_id"], "source_sha256": book["source_sha256"],
                                    "rights_basis": claim["rights"]["basis"],
                                    "rights_evidence_url": claim["rights"]["evidence_url"],
                                    "tag_authority": annotation["authority"],
                                    "tag_evidence_url": annotation["evidence_url"],
                                    "measurements": measurements})
    output = []
    for tag_id, label in sorted(taxonomy.items()):
        group = sorted(matched[tag_id], key=lambda row: row["key"])
        values = []
        for metric, unit in FEATURES.items():
            observed = [row["measurements"][metric] for row in group if row["measurements"][metric] is not None]
            average = fsum(observed) / len(observed) if observed else None
            values.append({"id": metric, "unit": unit, "observed_count": len(observed),
                           "missing_count": len(group) - len(observed),
                           "mean_per_work": round(average, 6) if average is not None else None,
                           "population_stddev_between_works": (round(sqrt(fsum((v-average)**2 for v in observed) / len(observed)), 6)
                                                               if len(observed) >= 2 else None),
                           "minimum": min(observed) if observed else None,
                           "maximum": max(observed) if observed else None})
        output.append({"tag_id": tag_id, "label": label, "confirmed_work_count": len(group),
                       "sample_warning": "NO_CONFIRMED_WORKS" if not group else ("SINGLE_WORK" if len(group) == 1 else "DESCRIPTIVE_ONLY"),
                       "works": [{k: v for k, v in row.items() if k != "measurements"} for row in group],
                       "metrics": values})
    return {"schema_version": VERSION, "taxonomy_version": curation["taxonomy_version"],
            "source_snapshot_sha256": snapshot_sha256, "source_metric_profiles": baseline_profiles,
            "aggregation": "unweighted per independently observed edition; population dispersion across works only",
            "scientific_boundary": {"class": "private_curator_declared_descriptive_extension",
                                    "public_release_ready": False, "rights_independently_verified": False,
                                    "fantlab_parity": False, "m2_source_matched": 0,
                                    "no_source_text": True}, "tags": output}


def _unique_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON key")
        out[key] = value
    return out


def main(argv=None):
    from .analyze import MAX_ANALYSIS_BYTES, _read_bounded_regular_file
    parser = argparse.ArgumentParser(description="Source-free private curated tag profiles (M2 0/5; not public-ready)")
    parser.add_argument("--snapshot", required=True, type=Path, help="source-free measured-edition snapshot JSON")
    parser.add_argument("--curation", required=True, type=Path, help="explicit rights and tag evidence catalog JSON")
    parser.add_argument("--format", choices=("json", "html", "csv"), default="json",
                         help="private derived report format; JSON remains the default")
    parser.add_argument("--output", type=Path, help="create a new local report; never overwrite")
    args = parser.parse_args(argv)
    try:
        raw = _read_bounded_regular_file(args.snapshot, MAX_ANALYSIS_BYTES, "snapshot")
        curated = _read_bounded_regular_file(args.curation, MAX_ANALYSIS_BYTES, "curation")
        snapshot = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_keys)
        curation = json.loads(curated.decode("utf-8"), object_pairs_hook=_unique_keys)
        result = build_tag_profiles(snapshot, curation, snapshot_sha256=sha256(raw).hexdigest())
        if args.format == "html":
            from .tag_profile_html import render_tag_profiles_html
            rendered = render_tag_profiles_html(result)
        elif args.format == "csv":
            from .tag_profile_csv import render_tag_profiles_csv
            rendered = render_tag_profiles_csv(result)
        else:
            rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
        if args.output is None:
            print(rendered, end="")
        else:
            with args.output.open("x", encoding="utf-8") as output:
                output.write(rendered)
    except FileExistsError:
        parser.error("output already exists; never overwrite a previous profile")
    except (OSError, UnicodeError, ValueError, TypeError, OverflowError, RecursionError):
        parser.error("invalid source-free evidence input or destination; no book text processed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
