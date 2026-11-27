"""Compare source-free Robinson diagnostics, not aligned translations or parity.

The assembly input must come from the fresh pinned boundary replay. Frozen
reference receipts are Git-blob bound; the comparison does not read prose.
"""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
from html import escape
import json
from math import isfinite
from pathlib import Path
import re

from .trusov_excerpt_export import load_frozen_report, render_csv, SOURCE_RELATIVE

SHISH_RELATIVE = (
    "corpus/candidates/diagnostics/"
    "defoe-robinson-crusoe-shishmareva-1935-ru.measured.json"
)
SHISH_BLOB = "0afd42fe5825b7eb6b07ca209aef963e006f333b"
SCOPE = "INFERRED_150_PAGE_HISTORICAL_BRANCH_ASSEMBLY_DIAGNOSTIC"
LIMITS = (
    "Trusov: 1775 volume 1, translated via French; inferred historical spelling "
    "Page 2–151 assembly with synthetic LF joins, not a verified complete body.",
    "Shishmareva: ACADEMIA 1935 volume 1, first narrative, Russian translation; "
    "electronic body replayed but printed edition not collated.",
    "Coverage and abridgement are not aligned. Orthography, chronology, "
    "intermediary language, editorial choices and length confound differences.",
    "No translator-effect or author-attribution inference, corpus admission "
    "or FantLab parity. Missing observations are not zero.",
)


def load_shish(path: Path) -> dict:
    raw = path.read_bytes()
    if sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest() != SHISH_BLOB:
        raise ValueError("Shishmareva receipt blob mismatch")
    return json.loads(raw)


def build(assembly: dict, interior: dict, shish: dict) -> dict:
    render_csv(interior)  # preserve the existing frozen-scope validation
    if (assembly.get("schema_version") != "scriptorium-trusov-boundary-assembly-v1"
            or assembly.get("scope") != SCOPE
            or assembly.get("page_interval") != {"from": 2, "to": 151, "count": 150}
            or assembly.get("source_page_graph_sha256") != interior["source_page_graph_sha256"]
            or assembly.get("baseline_normalized_sha256") != interior["normalized_sha256"]
            or assembly.get("interior_source_revision_list_sha256") != interior["source_revision_list_sha256"]
            or assembly.get("join_profile") != interior["join"]["projected_page_join_profile"]
            or assembly.get("closing_scope") != "SIX_LITERAL_SEAMS_AND_CURRENT_LAYOUT_VERIFIED"
            or assembly.get("full_literary_body") != "NOT_VERIFIED"
            or assembly.get("print_collation") != "NOT_VERIFIED"
            or any(assembly.get(k) is not False for k in (
                "historical_render_equivalence_proven", "historical_page_join_verified",
                "corpus_admitted", "m2_parity_admissible", "source_text_committed"))
            or [r["page_sequence"] for r in assembly["boundary_pages"]] != [2,148,149,150,151]
            or [r["revision_id"] for r in assembly["boundary_source_identities"]]
                != [4958669,4958660,4958661,4958663,4958664]
            or assembly.get("raw_joined_characters") != interior["join"]["joined_projected_wikitext_characters_including_spaces"]
                + sum(r["characters"] for r in assembly["boundary_pages"]) + 5
            or shish.get("candidate_id") != "defoe-robinson-shishmareva-1935-vol1-ru"
            or shish["source"]["revision_id"] != 5634933
            or shish["scriptorium"] != interior["scriptorium"]
            or shish["gates"]["fantlab_input_identity"] != "UNKNOWN"
            or shish["gates"]["m2_parity_admissible"] is not False):
        raise ValueError("comparison source/scope drift")
    for digest in (assembly["normalized_sha256"], assembly["raw_joined_sha256"]):
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("invalid assembly digest")
    rows = []
    for a, i, s in zip(assembly["metric_rows"], interior["metric_rows"], shish["metric_rows"], strict=True):
        key, unit = i["metric_id"], i["unit"]
        if ((a["metric_id"], a["unit"], a["interior_value"]) != (key, unit, i["actual"])
                or (s["metric_id"], s["unit"], s["compatibility_status"]) != (key, unit, i["compatibility_status"])
                or s["fantlab_display"] is not None):
            raise ValueError("comparison metric identity drift")
        t, m = a["assembly_value"], s["actual"]
        if any(v is not None and (type(v) not in (int, float) or not isfinite(v)) for v in (t,m)):
            raise ValueError("invalid metric value")
        if i["result"] == "NOT_RUN_DICTIONARY_UNBOUND" and (t is not None or m is not None):
            raise ValueError("unbound dictionary value")
        expected_delta = t-i["actual"] if t is not None and i["actual"] is not None else None
        if a["delta"] != expected_delta:
            raise ValueError("assembly delta drift")
        rows.append({"metric_id": key, "unit": unit, "compatibility_status": i["compatibility_status"],
                     "trusov": t, "shishmareva": m,
                     "delta_trusov_minus_shishmareva": t-m if t is not None and m is not None else None})
    if len(rows) != 29 or sum(r["trusov"] is not None for r in rows) != assembly["numeric_metric_count"] or sum(r["shishmareva"] is not None for r in rows) != shish["numeric_metric_count"]:
        raise ValueError("comparison counts drift")
    chars = next(r for r in rows if r["metric_id"] == "fantlab.general.characters")
    if (chars["trusov"] != assembly["normalized_characters_including_spaces"]
            or chars["shishmareva"] != shish["body"]["normalized_characters_including_spaces"]
            or min(chars["trusov"], chars["shishmareva"]) < 300000):
        raise ValueError("comparison character accounting drift")
    return {
        "schema_version": "scriptorium-robinson-translation-diagnostic-v1",
        "scope": "UNALIGNED_EDITION_DIAGNOSTIC_ONLY",
        "trusov": {"carrier_revision_id": 5041937, "source_page_graph_sha256": interior["source_page_graph_sha256"],
                    "normalized_sha256": assembly["normalized_sha256"], "assembly_receipt_sha256": sha256(json.dumps(assembly, sort_keys=True, ensure_ascii=True).encode()).hexdigest()},
        "shishmareva": {"revision_id": 5634933, "normalized_sha256": shish["body"]["normalized_sha256"], "receipt_git_blob": SHISH_BLOB},
        "scriptorium": interior["scriptorium"], "limitations": list(LIMITS),
        "metric_rows": rows, "joint_numeric_count": sum(r["delta_trusov_minus_shishmareva"] is not None for r in rows),
        "fantlab_input_identity": "UNKNOWN", "m2_parity_admissible": False, "corpus_admitted": False,
        "translation_coverage_alignment": "NOT_RUN",
    }


def render(report: dict) -> str:
    def cell(v):
        return "Unavailable" if v is None else escape(str(v) if isinstance(v, int) else format(v, ".8g"))
    rows = "".join("<tr><th scope='row'>" + escape(r["metric_id"]) + "</th><td>" +
                   escape(r["unit"]) + "</td>" + "".join("<td>" + cell(r[k]) + "</td>" for k in
                   ("trusov", "shishmareva", "delta_trusov_minus_shishmareva")) + "</tr>" for r in report["metric_rows"])
    limits = "".join("<li>" + escape(x) + "</li>" for x in LIMITS)
    return """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Robinson Crusoe | Scriptorium diagnostic</title><style>
body{margin:0 auto;padding:1.2rem;max-width:72rem;font:1rem/1.55 system-ui;color:#28221e;background:#faf7ef}
h1,h2{font-family:Georgia,serif} a{color:#174e67} table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
td,th{padding:.55rem;text-align:left;border-bottom:1px solid #b8b0a3} .scroll{overflow-x:auto} :focus-visible{outline:3px solid #174e67}
</style><main><h1>Robinson Crusoe: two Russian editions</h1><p>Diagnostic only — not aligned translations or verified complete historical print.</p>
<ul>""" + limits + """</ul><p><a href="https://ru.wikisource.org/w/index.php?oldid=5041937">Trusov source</a> · <a href="https://ru.wikisource.org/w/index.php?oldid=5634933">Shishmareva source</a> · <a href="robinson-pair.json">Exact JSON</a></p>
<h2>29 measured or unavailable fields</h2><p>Signed difference = Trusov minus Shishmareva. Display rounded to eight significant digits; exact values in JSON.</p>
<div class="scroll" tabindex="0" role="region" aria-label="Metric comparison table"><table><caption>Source-free edition measurements</caption><thead><tr><th scope="col">Metric</th><th scope="col">Unit</th><th scope="col">Trusov 1775</th><th scope="col">Shishmareva 1935</th><th scope="col">Difference</th></tr></thead><tbody>""" + rows + """</tbody></table></div></main></html>\n"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assembly", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = build(json.loads(args.assembly.read_bytes()), load_frozen_report(Path(SOURCE_RELATIVE)), load_shish(Path(SHISH_RELATIVE)))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "robinson-pair.json").write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "robinson-pair.html").write_text(render(report), encoding="utf-8")
    print("Robinson diagnostic joint numeric fields:", report["joint_numeric_count"], "/29")


if __name__ == "__main__":
    main()
