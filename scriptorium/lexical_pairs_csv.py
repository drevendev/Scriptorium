"""Replay two independently reviewed, source-free public lexical receipts as one CSV."""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, ROUND_HALF_EVEN
from hashlib import sha256
import io
import json
from pathlib import Path

from .analyze import _read_bounded_regular_file, _write_new
from .grin_lexical_csv import PROJECTION_SHA256 as GRIN_SHA256, _unit

CROSS_SHA256 = "c79fc139f702cb7ec30ccadb6ea14d4b0272cfa28e884c151a78339a11d9d648"
MAX_BYTES = 64 * 1024
SCHEMA = "scriptorium-reviewed-lexical-pairs-csv-v1"
AGGREGATES = (
    "shared_form_count",
    "left_only_form_count",
    "right_only_form_count",
    "eligible_form_count",
    "excluded_rare_form_count",
    "balanced_form_count",
    "left_dominant_form_count",
    "right_dominant_form_count",
    "type_jaccard_percent",
    "token_distribution_overlap_percent",
    "jensen_shannon_divergence_bits",
    "left_dominant_token_share_percent",
    "right_dominant_token_share_percent"
,
)
DIFFERENCES = {
    "type_jaccard_percent": (6, "percentage_points"),
    "token_distribution_overlap_percent": (6, "percentage_points"),
    "jensen_shannon_divergence_bits": (4, "bits"),
}


def _load(payload: bytes, expected: str) -> dict:
    if len(payload) > MAX_BYTES or sha256(payload).hexdigest() != expected:
        raise ValueError("reviewed projection identity mismatch")
    return json.loads(payload, parse_float=Decimal)


def _scalar(value):
    return str(value).lower() if type(value) is bool else str(value)


def render_reviewed_pairs_csv(grin: bytes, cross: bytes) -> str:
    """No new source access or corpus/admission claim; only exact reviewed bytes."""
    left = _load(grin, GRIN_SHA256)
    right = _load(cross, CROSS_SHA256)
    rows = [["pair", "section", "field", "value", "unit", "status"],
            ["all", "export", "schema_version", SCHEMA, "", "metadata"]]
    for pair, doc, digest in (("grin", left, GRIN_SHA256), ("cross", right, CROSS_SHA256)):
        rows.append([pair, "report", "projection_sha256", digest, "", "metadata"])
        for section, values in (
            ("report", {k: v for k, v in doc.items() if k not in ("provenance", "works", "aggregate", "methodology")}),
            ("provenance", doc["provenance"]), ("left", doc["works"][0]),
            ("right", doc["works"][1]), ("methodology", doc["methodology"]),
        ):
            for key, value in values.items():
                rows.append([pair, section, key, _scalar(value), _unit(key), "metadata"])
        for key in AGGREGATES:
            present = key in doc["aggregate"]
            rows.append([pair, "aggregate", key, _scalar(doc["aggregate"][key]) if present else "NOT_RETAINED",
                         _unit(key), "measured" if present else "not_retained"])
    for key, (places, unit) in DIFFERENCES.items():
        delta = right["aggregate"][key] - left["aggregate"][key]
        delta = delta.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN)
        rows.append(["cross_minus_grin", "difference", key, str(delta), unit, "derived_descriptive"])
    # All fields are frozen, except the computed numeric differences. Signed
    # decimals in the latter are numeric cells, not arbitrary spreadsheet formulas.
    for row in rows:
        for index, cell in enumerate(row):
            if index == 3 and row[1] == "difference":
                Decimal(cell)
            elif cell.startswith(("=", "+", "-", "@", "\t", "\r", "\n")):
                raise ValueError("unsafe reviewed CSV cell")
    out = io.StringIO(newline="")
    csv.writer(out, quoting=csv.QUOTE_ALL, lineterminator="\n").writerows(rows)
    return out.getvalue()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("grin", type=Path)
    parser.add_argument("cross", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--output", type=Path)
    mode.add_argument("--check", type=Path)
    args = parser.parse_args(argv)
    try:
        result = render_reviewed_pairs_csv(
            _read_bounded_regular_file(args.grin, MAX_BYTES, "Grin projection"),
            _read_bounded_regular_file(args.cross, MAX_BYTES, "cross-author projection"))
        if args.check is not None:
            if _read_bounded_regular_file(args.check, MAX_BYTES, "CSV") != result.encode("utf-8"):
                parser.error("reviewed pairs CSV bytes differ")
        elif args.output is not None:
            _write_new(args.output, result)
        else:
            print(result, end="")
    except FileExistsError:
        parser.error("report output already exists; choose another destination")
    except (OSError, ValueError):
        parser.error("unable to replay exact reviewed lexical projections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
