"""Inspect the native JSON layer before LemmaInfo discards fields; no values exported."""
import argparse
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path

from tools.pylem_n_attestation_probe import CONTROLS, PROFILE, SDIST_SHA256

SCHEMA = "scriptorium-aot-n-raw-json-surface-v1"
SOURCE_KEYS = frozenset(("ancode", "ancodeId", "sourceAncode", "sourcePos", "sourcePosSlot",
                         "aotPos", "aotPosSlot", "posIndex", "gramtabPos", "ancode_id",
                         "source_pos", "source_pos_slot", "aot_pos", "aot_pos_slot",
                         "pos_index", "gramtab_pos"))
KNOWN_KEYS = SOURCE_KEYS | {"morphInfo", "commonGrammems", "found", "srcNorm", "wordForm",
                            "wordWeight", "homonymWeight", "paradigm", "allForms"}


def digest(value):
    return sha256(value.encode("utf-8")).hexdigest()


def measure(holder):
    groups = {}
    manifest = []
    source_counts = dict.fromkeys(sorted(SOURCE_KEYS), 0)
    total = 0
    unknown = 0
    for role, words in CONTROLS:
        rows = []
        for word in words:
            raw = holder.lemmatize_json(word, False)
            if type(raw) is not list:
                raise ValueError("invalid native JSON collection")
            tags = []
            surfaces = []
            for item in raw:
                if type(item) is not dict or type(item.get("morphInfo")) is not str:
                    raise ValueError("invalid native JSON analysis")
                tag = item["morphInfo"].partition(" ")[0]
                if not tag or tag != tag.strip():
                    raise ValueError("invalid native JSON POS")
                tags.append(tag)
                if tag == "N":
                    names = sorted(KNOWN_KEYS.intersection(item))
                    extra = len(item.keys() - KNOWN_KEYS)
                    surfaces.append({"known_keys": names, "unrecognized_key_count": extra})
                    unknown += extra
                    total += 1
                    for name in SOURCE_KEYS.intersection(item):
                        source_counts[name] += 1
            wrapped = [a.part_of_speech for a in holder.lemmatize(word)]
            if tags != wrapped:
                raise ValueError("native JSON and Python POS sequence differ")
            token_hash = digest(word)
            manifest.append(role + ":" + token_hash)
            rows.append({"token_sha256": token_hash, "candidate_count": len(tags),
                         "n_candidate_count": len(surfaces), "n_surfaces": surfaces})
        groups[role] = rows
    negatives = groups["unrelated_preposition_controls"]
    decision = ("no_n_observed" if not total else
                "possible_source_key_needs_semantic_validation" if any(source_counts.values()) else
                "unrecognized_keys_need_source_review" if unknown else
                "no_explicit_source_key_in_examined_raw_n_rows")
    return {"schema_version": SCHEMA, "status": "diagnostic_only",
            "provider": {"distribution": "pylem", "version": "0.0.18",
                         "runtime_profile": PROFILE, "sdist_sha256": SDIST_SHA256},
            "fixture_manifest_sha256": digest("\n".join(manifest)), "groups": groups,
            "n_candidate_count": total, "explicit_source_key_counts": source_counts,
            "unrecognized_n_key_count": unknown,
            "clean_negative_control_count": sum(r["candidate_count"] > 0 and not r["n_candidate_count"] for r in negatives),
            "raw_and_wrapper_pos_sequences_match": True, "decision": decision,
            "observation_sha256": digest(json.dumps(groups, sort_keys=True, separators=(",", ":"))),
            "original_aot_enum_verified": False, "noun_cardinal_source_pos": "unresolved",
            "source_text_included": False, "production_pos_mapping_changed": False,
            "fantlab_homonym_selection": "unresolved", "m2_parity_admissible": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if version("pylem") != "0.0.18":
        raise RuntimeError("wrong native pylem version")
    from pylem import MorphLanguage, MorphanHolder
    doc = measure(MorphanHolder(MorphLanguage.Russian))
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x", encoding="utf-8") as stream:
        json.dump(doc, stream, indent=2, sort_keys=True)
        stream.write("\n")


if __name__ == "__main__":
    main()
