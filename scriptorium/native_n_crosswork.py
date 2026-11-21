"""Source-free comparison of independently pinned AOT/pylem N-only observations.

The two records are *different works*, not a controlled difference in POS choice.
This deliberately reports only the observed runtime N share and never estimates
noun/cardinal frequencies or FantLab source-matched parity.
"""
from __future__ import annotations

from collections.abc import Mapping

from .n_uncertainty_publication import validate_n_summary

SCHEMA = "scriptorium-native-n-resurrection-summary-v1"
_RESURRECTION_PIN = {
    "candidate_id": "tolstoy-resurrection-ru",
    "normalized_sha256": "2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0",
    "runtime_analysis_sha256": "13c318f2af1da439f8e204a26da39ee57cbf6c06f7a9fc17d99fc9a4ac7112c2",
    "artifact_json_sha256": "8feb3f7d2d53a5fdafb2d7bce1b52bfce2a96503ca6dbedbdaca3afb121946f6",
    "head_sha": "73310bd251094395c21e7075b3f4f1df4edd0737",
    "run_id": 44309635723,
    "artifact_id": 14429917083,
}
_COUNTS = {
    "word_count": 136129,
    "sentence_count": 9600,
    "baseline_defined": 57868,
    "n_only": 31708,
    "n_mixed_excluded": 9555,
    "conditional_defined": 89576,
}


def compare_pinned_native_n(anna: Mapping[str, object], resurrection: Mapping[str, object]) -> dict[str, object]:
    """Verify both source-free witnesses before computing descriptive percentage points."""
    if not isinstance(anna, dict) or not isinstance(resurrection, dict):
        raise ValueError("native N comparison requires two JSON objects")
    validate_n_summary(anna)
    if (anna["work"]["candidate_id"] != "tolstoy-anna-karenina-ru"
            or anna["evidence"]["artifact_json_sha256"] !=
            "6da40b4723cafc0288fea530a35f8d910b76e7ccffd60f754e6aa899412e5554"):
        raise ValueError("Anna frozen source identity mismatch")
    ac = anna["counts"]
    if ac != {"word_count": 269358, "sentence_count": 21228,
              "baseline_defined": 117554, "n_only": 55081,
              "n_mixed_excluded": 19670, "conditional_defined": 172635}:
        raise ValueError("Anna native count receipt drift")
    if (set(resurrection) != {"schema_version", "status", "source_text_included",
                                "m2_parity_admissible", "provider", "evidence", "counts"}
            or resurrection["schema_version"] != SCHEMA
            or resurrection["status"] != "diagnostic_only"
            or resurrection["source_text_included"] is not False
            or resurrection["m2_parity_admissible"] is not False):
        raise ValueError("Resurrection evidence boundary mismatch")
    # JSON booleans and floats can compare equal to Python integers. Counts
    # and run IDs must keep their actual type, not only their numeric value.
    evidence = resurrection["evidence"]
    counts = resurrection["counts"]
    if (not isinstance(evidence, dict)
            or any(type(evidence.get(key)) is not int for key in ("run_id", "artifact_id"))
            or evidence != _RESURRECTION_PIN):
        raise ValueError("Resurrection native artifact identity mismatch")
    if (not isinstance(counts, dict)
            or set(counts) != set(_COUNTS)
            or any(type(counts[key]) is not int for key in _COUNTS)):
        raise ValueError("Resurrection native counts must be JSON integers")
    if counts != _COUNTS:
        raise ValueError("Resurrection native counts mismatch")
    if resurrection["provider"] != {
        "distribution": "pylem", "version": "0.0.18",
        "runtime_profile": "pylem-0.0.18-python39-sidecar-v1",
        "sdist_sha256": "66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515",
    }:
        raise ValueError("Resurrection native provider mismatch")
    anna_n = ac["n_only"] * 100 / ac["word_count"]
    resurrection_n = _COUNTS["n_only"] * 100 / _COUNTS["word_count"]
    return {
        "status": "diagnostic_only",
        "unit": "percentage_points_of_word_tokens",
        "anna_n_only_percent": anna_n,
        "resurrection_n_only_percent": resurrection_n,
        "resurrection_minus_anna_pp": resurrection_n - anna_n,
        "inference": "descriptive_cross_work_difference_not_noun_cardinal_disambiguation",
        "m2_parity_admissible": False,
    }
