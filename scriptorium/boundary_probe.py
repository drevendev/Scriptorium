"""Private, same-input word-boundary sensitivity; no FantLab rule inference.

Variants are independent counterfactuals against one normalized input, not
simultaneous edits or a fit to an unknown FantLab edition.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re

from .policy_diagnostic import analyze_word_dash_policy
from .text import NORMALIZATION_PROFILE, normalize_text, word_tokens

SCHEMA_VERSION = "scriptorium-word-boundary-probe-v1"
_DOTTED_INITIALISM_RE = re.compile(r"(?<!\w)(?:[^\W_\d]\.){2,}(?!\w)", re.UNICODE)
_VARIANT_LABELS = (
    ("current_scriptorium_text_v1", "Current Scriptorium word tokens"),
    ("split_ascii_hyphen", "Split each internal ASCII hyphen"),
    ("split_straight_apostrophe", "Split each internal straight apostrophe"),
    ("split_curly_apostrophe", "Split each internal curly apostrophe"),
    ("join_unicode_hyphens", "Join U+2010/U+2011 lexical connectors"),
    ("merge_dotted_initialisms", "Merge standalone dotted initialisms"),
    ("exclude_numeric_only", "Exclude decimal-only word tokens"),
)


def analyze_boundary_probe(text: str) -> dict[str, object]:
    """Measure one-factor token-count counterfactuals on exactly the same text.

    No source prose, matched FantLab claim, corpus admission or concatenation of
    independently estimated deltas is included in the artifact.
    """
    normalized = normalize_text(text)
    tokens = word_tokens(normalized)
    baseline = len(tokens)
    policy = analyze_word_dash_policy(normalized)["word_policy"]["variants"]
    if policy["current_scriptorium_text_v1"]["count"] != baseline:
        raise AssertionError("text-profile baseline drift")

    internals = {
        "ascii_hyphen": sum(t.text.count("-") for t in tokens),
        "straight_apostrophe": sum(t.text.count("'") for t in tokens),
        "curly_apostrophe": sum(t.text.count("’") for t in tokens),
    }
    initialisms = tuple(_DOTTED_INITIALISM_RE.finditer(normalized))
    initialism_reductions = sum(len(word_tokens(m.group(0))) - 1 for m in initialisms)
    counts = {
        "current_scriptorium_text_v1": baseline,
        "split_ascii_hyphen": baseline + internals["ascii_hyphen"],
        "split_straight_apostrophe": baseline + internals["straight_apostrophe"],
        "split_curly_apostrophe": baseline + internals["curly_apostrophe"],
        "join_unicode_hyphens": policy["join_unicode_hyphen_connectors"]["count"],
        "merge_dotted_initialisms": baseline - initialism_reductions,
        "exclude_numeric_only": policy["exclude_numeric_only_tokens"]["count"],
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "DIAGNOSTIC_ONLY",
        "normalization_profile": NORMALIZATION_PROFILE,
        "normalized_sha256": sha256(normalized.encode("utf-8")).hexdigest(),
        "normalized_characters_including_spaces": len(normalized),
        "source_text_embedded": False,
        "source_identity_to_fantlab": "UNKNOWN",
        "m2_parity_admissible": False,
        "note": (
            "Independent, one-factor changes to token counts on one exact input; "
            "not FantLab tokenization, not additive, not a matched-edition benchmark."
        ),
        "observed_boundaries": {
            "internal_ascii_hyphens": internals["ascii_hyphen"],
            "internal_straight_apostrophes": internals["straight_apostrophe"],
            "internal_curly_apostrophes": internals["curly_apostrophe"],
            "standalone_dotted_initialisms": len(initialisms),
            "initialism_token_reduction_if_merged": initialism_reductions,
        },
        "variants": [
            {
                "id": name,
                "description": label,
                "word_count": counts[name],
                "delta_from_current_words": counts[name] - baseline,
                "delta_per_1000_current_words": (
                    None if not baseline else
                    round((counts[name] - baseline) * 1000 / baseline, 6)
                ),
            }
            for name, label in _VARIANT_LABELS
        ],
    }


def render_boundary_probe(artifact: dict[str, object], kind: str) -> str:
    if artifact.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported boundary probe")
    if kind == "json":
        return json.dumps(artifact, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if kind != "markdown":
        raise ValueError("unsupported output format")
    lines = [
        "# Scriptorium · private word-boundary probe", "",
        "**DIAGNOSTIC_ONLY · FantLab input UNKNOWN · M2: 0/5.**", "",
        str(artifact["note"]), "",
        f"Normalization: `{artifact['normalization_profile']}`; normalized SHA-256: `{artifact['normalized_sha256']}`.",
        "",
        "| One-factor policy | Words | Difference vs current | Difference per 1,000 current words |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in artifact["variants"]:
        rate = row["delta_per_1000_current_words"]
        lines.append(
            f"| {row['description']} | {row['word_count']} | {row['delta_from_current_words']:+d} | "
            f"{rate if rate is not None else 'NOT_RUN'} |"
        )
    lines.extend(["", "Zero input words means an undefined rate, not a zero rate. No source text is included.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    from .analyze import MAX_ANALYSIS_BYTES, LocalInputError, _read_bounded_regular_file

    parser = argparse.ArgumentParser(
        description="Compare explicit word-boundary counterfactuals on one private UTF-8 file"
    )
    parser.add_argument("text", type=Path, help="local UTF-8 text; never uploaded")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path, help="create-only output; never overwrite")
    args = parser.parse_args(argv)
    try:
        raw = _read_bounded_regular_file(args.text, MAX_ANALYSIS_BYTES, "text")
        rendered = render_boundary_probe(analyze_boundary_probe(raw.decode("utf-8")), args.format)
        if args.output is None:
            print(rendered, end="")
        else:
            with args.output.open("x", encoding="utf-8", newline="") as output:
                output.write(rendered)
    except FileExistsError:
        parser.error("output already exists; choose another filename")
    except (LocalInputError, UnicodeError, OSError, ValueError):
        parser.error("local text invalid or destination unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
