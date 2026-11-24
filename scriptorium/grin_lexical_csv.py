"""Replay the reviewed Grin Reader CSV offline, without fetching either book."""
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
from typing import Sequence

from .analyze import _read_bounded_regular_file, _write_new

PROJECTION_SHA256 = "d4b158f4249d10a961e0122df05ddeb368f5774e7fa92ce73121e0647255bcb6"
MAX_BYTES = 64 * 1024
SCHEMA = "scriptorium-grin-lexical-reader-csv-v1"
SECTIONS = {"provenance", "works", "aggregate", "methodology"}


def _unit(key: str) -> str:
    if key.endswith("_percent"):
        return "percent"
    if key.endswith("_bits"):
        return "bits"
    if key.endswith("_form_count") or key == "distinct_forms":
        return "forms"
    return {"characters_including_spaces": "characters", "word_tokens": "tokens",
            "literary_page_revisions": "pages"}.get(key, "")


def render_reviewed_csv(payload: bytes) -> str:
    """Accept only the exact separately reviewed, source-free projection bytes."""
    if len(payload) > MAX_BYTES or sha256(payload).hexdigest() != PROJECTION_SHA256:
        raise ValueError("reviewed Grin projection identity mismatch")
    doc = json.loads(payload)
    rows = [["section", "field", "value", "unit"], ["export", "schema_version", SCHEMA, ""]]
    sections = [("report", {k: v for k, v in doc.items() if k not in SECTIONS}),
                ("provenance", doc["provenance"]), ("left", doc["works"][0]),
                ("right", doc["works"][1]), ("aggregate", doc["aggregate"]),
                ("methodology", doc["methodology"])]
    for section, values in sections:
        for key, value in values.items():
            rendered = str(value).lower() if type(value) is bool else str(value)
            row = [section, key, rendered, _unit(key) if section != "report" else ""]
            if any(cell.startswith(("=", "+", "-", "@", "\t", "\r", "\n")) for cell in row):
                raise ValueError("unsafe reviewed CSV cell")
            rows.append(row)
    out = io.StringIO(newline="")
    csv.writer(out, quoting=csv.QUOTE_ALL, lineterminator="\n").writerows(rows)
    return out.getvalue()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("projection", type=Path, help="exact reviewed public JSON projection")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--output", type=Path, help="create a new CSV, never overwrite")
    mode.add_argument("--check", type=Path, help="verify existing CSV bytes without writing")
    args = parser.parse_args(argv)
    try:
        rendered = render_reviewed_csv(_read_bounded_regular_file(args.projection, MAX_BYTES, "projection"))
        if args.check is not None:
            if _read_bounded_regular_file(args.check, MAX_BYTES, "CSV") != rendered.encode("utf-8"):
                parser.error("reviewed CSV bytes differ")
        elif args.output is not None:
            _write_new(args.output, rendered)
        else:
            print(rendered, end="")
    except FileExistsError:
        parser.error("report output already exists; choose another destination")
    except (OSError, ValueError):
        parser.error("unable to replay the exact reviewed Grin projection")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
