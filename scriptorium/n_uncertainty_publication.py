"""Validate source-free, evidence-bound N-only reader summaries.

This deliberately does not turn native N into noun/cardinal labels and does not
assert correspondence to FantLab's unpublished morphology.
"""
from __future__ import annotations

import re
from collections.abc import Mapping

SCHEMA = "scriptorium-native-n-uncertainty-summary-v1"
_SHA = re.compile(r"[0-9a-f]{64}$")


def _int(value: object, name: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def validate_n_summary(doc: object) -> dict[str, float]:
    """Fail closed on identity, unsupported certainty, or inconsistent rates."""
    required = {"schema_version", "status", "source_text_included", "m2_parity_admissible",
                "work", "evidence", "counts", "bucket_bounds", "bigram_bounds",
                "sentence_position_bounds", "native_controls", "boundary"}
    if not isinstance(doc, dict) or set(doc) != required:
        raise ValueError("native N summary keys mismatch")
    if (doc["schema_version"] != SCHEMA or doc["status"] != "diagnostic_only"
            or doc["source_text_included"] is not False or doc["m2_parity_admissible"] is not False):
        raise ValueError("native N evidence boundary mismatch")
    work = doc["work"]
    if not isinstance(work, dict) or set(work) != {"candidate_id", "title", "language"} or work["language"] != "ru":
        raise ValueError("native N work identity mismatch")
    if not all(isinstance(work[k], str) and work[k].strip() for k in ("candidate_id", "title")):
        raise ValueError("native N work identity missing")
    evidence = doc["evidence"]
    ekeys = {"workflow_url", "artifact_id", "artifact_json_sha256",
             "native_control_artifact_sha256", "scriptorium_revision",
             "normalized_sha256", "runtime_analysis_sha256", "pylem_version",
             "runtime_profile", "pylem_sdist_sha256"}
    if not isinstance(evidence, dict) or set(evidence) != ekeys:
        raise ValueError("native N evidence identity mismatch")
    for key in ("artifact_json_sha256", "native_control_artifact_sha256",
                "scriptorium_revision", "normalized_sha256", "runtime_analysis_sha256",
                "pylem_sdist_sha256"):
        if not isinstance(evidence[key], str) or _SHA.fullmatch(evidence[key]) is None:
            raise ValueError(f"native N {key} is not an immutable SHA-256 / commit identity")
    if (_int(evidence["artifact_id"], "artifact_id") == 0
            or evidence["workflow_url"] != "https://github.com/drevendev/Scriptorium/actions/runs/40825478901"
            or evidence["pylem_version"] != "0.0.18"
            or evidence["runtime_profile"] != "pylem-0.0.18-python39-sidecar-v1"):
        raise ValueError("native N provider/run identity mismatch")
    counts = doc["counts"]
    keys = {"word_count", "sentence_count", "baseline_defined",
            "n_only", "n_mixed_excluded", "conditional_defined"}
    if not isinstance(counts, dict) or set(counts) != keys:
        raise ValueError("native N count keys mismatch")
    n = {key: _int(counts[key], key) for key in keys}
    if (n["word_count"] == 0 or n["sentence_count"] == 0 or
            n["baseline_defined"] + n["n_only"] != n["conditional_defined"] or
            n["conditional_defined"] + n["n_mixed_excluded"] > n["word_count"]):
        raise ValueError("native N token partition inconsistent")
    if doc["bucket_bounds"] != {"noun": [0, n["n_only"]], "cardinal": [0, n["n_only"]]}:
        raise ValueError("native N noun/cardinal bounds must remain conditional")
    pairs = doc["bigram_bounds"]
    expected_pairs = {(a, b) for a in ("noun", "cardinal") for b in ("noun", "cardinal")}
    if not isinstance(pairs, list) or len(pairs) != 4:
        raise ValueError("native N bigram subset mismatch")
    seen = set()
    for row in pairs:
        if not isinstance(row, dict) or set(row) != {"first", "second", "min", "max", "independent_edge_upper"}:
            raise ValueError("native N bigram row malformed")
        pair = (row["first"], row["second"])
        if pair in seen or pair not in expected_pairs:
            raise ValueError("native N duplicate or unknown bigram")
        seen.add(pair)
        low, high, loose = (_int(row[key], key) for key in ("min", "max", "independent_edge_upper"))
        if not (low <= high <= loose <= n["word_count"]):
            raise ValueError("native N bigram bounds inconsistent")
    positions = doc["sentence_position_bounds"]
    if not isinstance(positions, list) or len(positions) != 5:
        raise ValueError("native N position subset mismatch")
    for index, row in enumerate(positions, start=1):
        if not isinstance(row, dict) or set(row) != {"position", "min", "max"}:
            raise ValueError("native N position row malformed")
        if (_int(row["position"], "position") != index or
                _int(row["min"], "min") > _int(row["max"], "max") or
                row["max"] > n["sentence_count"]):
            raise ValueError("native N position bounds inconsistent")
    controls = doc["native_controls"]
    if not isinstance(controls, dict) or set(controls) != {"noun_examples", "cardinal_examples", "other_pos_controls"}:
        raise ValueError("native N lexical control groups mismatch")
    for key, group in controls.items():
        if not isinstance(group, dict) or set(group) != {"token_count", "n_only"}:
            raise ValueError("native N lexical control malformed")
        if not (0 <= _int(group["n_only"], key) <= _int(group["token_count"], key)):
            raise ValueError("native N lexical control count mismatch")
    boundary = doc["boundary"]
    if not isinstance(boundary, dict) or set(boundary) != {
            "only_n_only_reassigned", "n_mixed_excluded", "cell_bounds_jointly_attainable",
            "native_roles_are_fixture_annotations", "fantlab_dictionary_equivalence",
            "fantlab_homonym_selection", "production_pos_mapping_changed"}:
        raise ValueError("native N interpretation missing")
    if (boundary["only_n_only_reassigned"] is not True or boundary["n_mixed_excluded"] is not True
            or boundary["cell_bounds_jointly_attainable"] is not False
            or boundary["native_roles_are_fixture_annotations"] is not True
            or boundary["fantlab_dictionary_equivalence"] != "unknown"
            or boundary["fantlab_homonym_selection"] != "unresolved"
            or boundary["production_pos_mapping_changed"] is not False):
        raise ValueError("native N scientific interpretation weakened")
    return {"n_only_percent_of_words": n["n_only"] * 100 / n["word_count"],
            "conditional_noun_or_cardinal_percent_of_defined": n["n_only"] * 100 / n["conditional_defined"]}
