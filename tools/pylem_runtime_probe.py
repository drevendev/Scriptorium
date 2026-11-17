#!/usr/bin/env python3
"""Execute a tiny source-free native pylem smoke under the legacy provider runtime."""
import argparse
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform

PYLEM_VERSION = "0.0.18"
SCHEMA_VERSION = "scriptorium-pylem-runtime-receipt-v1"
TOKENS = ("Красный", "быстро", "бежит")


def _sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


# Deliberately small, source-free semantic controls. These lexical roles are
# fixture annotations, NOT a native AOT homonym decision.
N_CONTRAST_GROUPS = (
    ("noun_examples", ("дом", "книга", "город")),
    ("cardinal_examples", ("два", "три", "пять")),
    ("other_pos_controls", ("красный", "быстро", "бежит")),
)



# Additional independently measured candidates, NOT a replacement for the strict
# v2 three-token unrelated controls. Native tags and token hashes only leave CI.
N_NEGATIVE_CONTROL_SURVEY = (
    ("adjectives", "A", ("красивый", "прекрасный", "огромный")),
    ("adverbs", "ADV", ("вчера", "внезапно", "совсем")),
    ("verbs", "V", ("говорит", "читает", "пишет")),
)

def _runtime_candidates(holder, token):
    candidates = []
    for analysis in holder.lemmatize(token):
        value = getattr(analysis, "part_of_speech", None)
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError("pylem returned blank/non-string part_of_speech")
        candidates.append(value.strip())
    return candidates


def build_n_contrast(holder):
    """Record observed native labels by lexical fixture role, never infer true POS."""
    groups = {}
    manifest = []
    for role, tokens in N_CONTRAST_GROUPS:
        rows = []
        for token in tokens:
            labels = _runtime_candidates(holder, token)
            token_hash = _sha256_text(token)
            rows.append({
                "token_sha256": token_hash,
                "candidate_count": len(labels),
                "runtime_pos": labels,
                "n_only": bool(labels) and set(labels) == {"N"},
                "n_present": "N" in labels,
            })
            manifest.append(role + ":" + token_hash)
        groups[role] = {
            "token_count": len(rows),
            "n_only_count": sum(row["n_only"] for row in rows),
            "n_present_count": sum(row["n_present"] for row in rows),
            "tokens": rows,
        }
    # An all-N backend would otherwise look like a cross-role collision.
    # Empty analyses are not successful negative controls.
    negative_controls_non_n_observed = all(
        row["candidate_count"] > 0 and not row["n_present"]
        for row in groups["other_pos_controls"]["tokens"]
    )
    cross_role_n_only = (
        groups["noun_examples"]["n_only_count"] > 0
        and groups["cardinal_examples"]["n_only_count"] > 0
    )
    return {
        "schema_version": "scriptorium-aot-n-contrast-v2",
        "source_text_included": False,
        "token_manifest_sha256": _sha256_text("\n".join(manifest)),
        "groups": groups,
        "observed_n_only_across_noun_and_cardinal_examples": cross_role_n_only,
        "negative_controls_non_n_observed": negative_controls_non_n_observed,
        "controlled_cross_role_n_collision_observed": (
            cross_role_n_only and negative_controls_non_n_observed
        ),
        "interpretation": "Fixture lexical roles are annotations, not recovered AOT POS enums.",
        "fantlab_dictionary_equivalence": "unknown",
        "fantlab_homonym_selection": "unresolved",
        "production_pos_mapping_changed": False,
        "m2_parity_admissible": False,
    }



def build_n_control_survey(holder):
    """Measure independent negative-control candidates without relaxing v2."""
    groups = {}
    manifest = []
    for role, expected_tag, tokens in N_NEGATIVE_CONTROL_SURVEY:
        rows = []
        for token in tokens:
            labels = _runtime_candidates(holder, token)
            if not labels:
                status = "no_analysis"
            elif "N" in labels:
                status = "n_present"
            elif expected_tag not in labels:
                status = "expected_tag_absent"
            else:
                status = "usable"
            digest = _sha256_text(token)
            rows.append({
                "token_sha256": digest,
                "candidate_count": len(labels),
                "runtime_pos": labels,
                "status": status,
            })
            manifest.append(role + ":" + expected_tag + ":" + digest)
        groups[role] = {
            "expected_runtime_pos": expected_tag,
            "token_count": len(rows),
            "usable_count": sum(row["status"] == "usable" for row in rows),
            "tokens": rows,
        }
    return {
        "schema_version": "scriptorium-aot-n-control-survey-v1",
        "source_text_included": False,
        "token_manifest_sha256": _sha256_text("\n".join(manifest)),
        "groups": groups,
        "all_roles_have_usable_control": all(
            group["usable_count"] > 0 for group in groups.values()
        ),
        "qualifies_v2_n_collision": False,
        "interpretation": (
            "Curated negative-control survey only; does not change the strict v2 "
            "N-collision verdict or resolve FantLab POS."
        ),
    }



def build_n_contrast_v3(contrast, survey):
    """Independently qualify curated N-only observations; never alter v2."""
    if (contrast.get("schema_version") != "scriptorium-aot-n-contrast-v2"
            or survey.get("schema_version") != "scriptorium-aot-n-control-survey-v1"):
        raise ValueError("unknown native N contrast/survey schema")
    positive = contrast.get("observed_n_only_across_noun_and_cardinal_examples")
    strict_v2 = contrast.get("controlled_cross_role_n_collision_observed")
    if type(positive) is not bool or type(strict_v2) is not bool:
        raise ValueError("invalid native N contrast verdict")
    groups = survey.get("groups")
    if not isinstance(groups, dict) or set(groups) != {"adjectives", "adverbs", "verbs"}:
        raise ValueError("missing/extra native negative-control groups")
    coverage = {}
    for role, expected in (("adjectives", "A"), ("adverbs", "ADV"), ("verbs", "V")):
        group = groups[role]
        if not isinstance(group, dict) or group.get("expected_runtime_pos") != expected:
            raise ValueError("native control role/tag mismatch")
        rows = group.get("tokens")
        if not isinstance(rows, list) or len(rows) != 3 or group.get("token_count") != 3:
            raise ValueError("native control slate is incomplete")
        usable = 0
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError("invalid native control row")
            labels = row.get("runtime_pos")
            if (not isinstance(labels, list)
                    or not all(isinstance(tag, str) and tag.strip() for tag in labels)
                    or row.get("candidate_count") != len(labels)):
                raise ValueError("invalid native control analysis")
            status = ("no_analysis" if not labels else
                      "n_present" if "N" in labels else
                      "expected_tag_absent" if expected not in labels else "usable")
            if row.get("status") != status:
                raise ValueError("native control status does not match actual tags")
            usable += status == "usable"
        if group.get("usable_count") != usable:
            raise ValueError("native control usable count mismatch")
        coverage[role] = {
            "usable_controls": usable,
            "required_controls": 2,
            "qualified": usable >= 2,
        }
    controls_qualified = all(group["qualified"] for group in coverage.values())
    return {
        "schema_version": "scriptorium-aot-n-independent-controls-v3",
        "source_text_included": False,
        "positive_n_only_fixture_observed": positive,
        "independent_negative_controls_qualified": controls_qualified,
        "negative_control_coverage": coverage,
        "independently_controlled_n_only_observed": positive and controls_qualified,
        "historical_v2_controlled_verdict_unchanged": strict_v2,
        "noun_cardinal_source_pos": "unresolved",
        "fantlab_dictionary_equivalence": "unknown",
        "fantlab_homonym_selection": "unresolved",
        "production_pos_mapping_changed": False,
        "m2_parity_admissible": False,
        "interpretation": (
            "Curated lexical N-only observation, not recovered source POS identity "
            "or FantLab homonym selection. Requires two clean controls per unrelated role."
        ),
    }


def build_receipt():
    try:
        installed = version("pylem")
    except PackageNotFoundError as exc:
        raise RuntimeError("pylem==0.0.18 is not installed") from exc
    if installed != PYLEM_VERSION:
        raise RuntimeError("expected pylem==0.0.18, found pylem==%s" % installed)

    from pylem import MorphanHolder, MorphLanguage

    holder = MorphanHolder(MorphLanguage.Russian)
    rows = []
    observed = set()
    for ordinal, token in enumerate(TOKENS):
        runtime_pos = _runtime_candidates(holder, token)
        observed.update(runtime_pos)
        rows.append(
            {
                "ordinal": ordinal,
                "token_sha256": _sha256_text(token),
                "candidate_count": len(runtime_pos),
                "runtime_pos": runtime_pos,
            }
        )

    fixture_identity = "\n".join(
        "%d:%s" % (ordinal, _sha256_text(token)) for ordinal, token in enumerate(TOKENS)
    )
    contrast = build_n_contrast(holder)
    survey = build_n_control_survey(holder)
    return {
        "schema_version": SCHEMA_VERSION,
        "provider": {
            "distribution": "pylem",
            "version": installed,
            "runtime_profile": "pylem-0.0.18-python39-sidecar-v1",
        },
        "runtime": {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "fixture": {
            "token_count": len(TOKENS),
            "token_manifest_sha256": _sha256_text(fixture_identity),
            "tokens": rows,
            "observed_runtime_pos": sorted(observed),
            "source_text_included": False,
        },
        "n_contrast": contrast,
        "n_control_survey": survey,
        "n_contrast_v3": build_n_contrast_v3(contrast, survey),
        "epistemic_boundary": {
            "fantlab_dictionary_equivalence": "unknown",
            "homonym_selection_policy": "unresolved",
            "noun_cardinal_runtime_collision": "unresolved",
            "m2_parity_admissible": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt = build_receipt()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
