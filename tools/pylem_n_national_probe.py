"""Isolated national-label experiment; never changes the production provider."""
import argparse
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import tarfile

from tools.pylem_n_attestation_probe import CONTROLS, SDIST_SHA256

OLD = b"GetHolder(langua).m_pGramTab->SetUseNationalConstants(false);"
NEW = OLD.replace(b"false", b"true")
CONTRACT = Path("compatibility/aot-pylem-0.0.18-to-fantlab-2022-v1.json")


def digest(data):
    return sha256(data).hexdigest()


def patch_binding(data):
    if data.count(OLD) != 1 or NEW in data:
        raise ValueError("unexpected native binding flag")
    return data.replace(OLD, NEW, 1)


def prepare(archive, target):
    if digest(archive.read_bytes()) != SDIST_SHA256:
        raise ValueError("sdist digest mismatch")
    with tarfile.open(archive, "r:gz") as source:
        members = source.getmembers()
        names = set()
        for member in members:
            path = PurePosixPath(member.name)
            if (not path.parts or path.is_absolute() or ".." in path.parts
                    or path.parts[0] != "pylem-0.0.18" or path in names
                    or not (member.isfile() or member.isdir())):
                raise ValueError("unexpected sdist member")
            names.add(path)
        binding = "pylem-0.0.18/pylem/binding/main.cpp"
        stream = source.extractfile(binding)
        if stream is None:
            raise ValueError("missing binding")
        original = stream.read()
        patched = patch_binding(original)
        target.mkdir(parents=True, exist_ok=False)
        for member in members:
            path = target.joinpath(*PurePosixPath(member.name).parts)
            if member.isdir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("xb") as out, source.extractfile(member) as inp:
                    while True:
                        chunk = inp.read(1024 * 1024)
                        if not chunk:
                            break
                        out.write(chunk)
                path.chmod(member.mode & 0o777)
        (target / binding).write_bytes(patched)
    return {"sdist_sha256": SDIST_SHA256, "binding_before_sha256": digest(original),
            "binding_after_sha256": digest(patched), "only_flag_changed": True}


def capture(holder, allowed):
    rows = []
    for role, words in CONTROLS:
        for word in words:
            tags = [a.part_of_speech for a in holder.lemmatize(word)]
            if any(type(tag) is not str or tag not in allowed for tag in tags):
                raise ValueError("unexpected native POS label")
            rows.append({"role": role, "token_sha256": digest(word.encode("utf-8")),
                         "tags": tags})
    return rows


def compare(latin, national, mapping):
    expected = [(role, digest(word.encode("utf-8"))) for role, words in CONTROLS for word in words]
    if len(latin) != len(expected) or len(national) != len(expected):
        raise ValueError("fixture coverage mismatch")
    rows = []
    for before, after, key in zip(latin, national, expected):
        if any((r["role"], r["token_sha256"]) != key for r in (before, after)):
            raise ValueError("fixture identity mismatch")
        b, a = before["tags"], after["tags"]
        if any(tag not in mapping.values() for tag in b) or any(tag not in mapping for tag in a):
            raise ValueError("unknown POS label")
        folded = [mapping[tag] for tag in a]
        if sorted(b) != sorted(folded):
            raise ValueError("candidate POS multiplicity changed")
        rows.append({"role": key[0], "token_sha256": key[1], "latin_tags": b,
                     "national_tags": a, "folded_sequence_matches": b == folded})
    noun, cardinal, negative = (role for role, _ in CONTROLS)
    noun_count = sum(r["national_tags"].count("С") for r in rows if r["role"] == noun)
    cardinal_count = sum(r["national_tags"].count("ЧИСЛ") for r in rows if r["role"] == cardinal)
    clean = sum(bool(r["latin_tags"]) and "N" not in r["latin_tags"]
                for r in rows if r["role"] == negative)
    return {"schema_version": "scriptorium-aot-n-national-labels-v1", "rows": rows,
            "noun_role_national_noun_count": noun_count,
            "cardinal_role_national_cardinal_count": cardinal_count,
            "clean_negative_controls": clean,
            "distinct_labels_observed": noun_count > 0 and cardinal_count > 0 and clean == 3,
            "source_enum_verified": False, "candidate_identity_verified": False,
            "production_pos_mapping_changed": False, "m2_parity_admissible": False,
            "source_text_included": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("archive", type=Path)
    prep.add_argument("target", type=Path)
    cap = sub.add_parser("capture")
    cap.add_argument("mode", choices=("latin", "national"))
    comp = sub.add_parser("compare")
    comp.add_argument("latin", type=Path)
    comp.add_argument("national", type=Path)
    comp.add_argument("patch_receipt", type=Path)
    for command in (prep, cap, comp):
        command.add_argument("receipt", type=Path)
    args = parser.parse_args()
    if args.action == "prepare":
        doc = prepare(args.archive, args.target)
    else:
        contract_bytes = CONTRACT.read_bytes()
        inventory = json.loads(contract_bytes)["runtime_pos_inventory"]
        mapping = {r["cyrillic"]: r["runtime_pos"] for r in inventory}
        if args.action == "capture":
            from importlib.metadata import version
            from pylem import MorphLanguage, MorphanHolder
            if version("pylem") != "0.0.18":
                raise ValueError("unexpected provider version")
            allowed = mapping if args.mode == "national" else set(mapping.values())
            doc = capture(MorphanHolder(MorphLanguage.Russian), allowed)
        else:
            doc = compare(json.loads(args.latin.read_text()), json.loads(args.national.read_text()), mapping)
            doc["patch"] = json.loads(args.patch_receipt.read_text())
            doc["contract_sha256"] = digest(contract_bytes)
    with args.receipt.open("x", encoding="utf-8") as out:
        json.dump(doc, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
