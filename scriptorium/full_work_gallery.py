"""Source-free, offline comparison of two pinned full-work evidence records."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import math
import os
from pathlib import Path
import stat
import sys

PROFILE = "scriptorium-full-work-gallery-v1"
SOURCES = (
    ("grin-running-on-waves-ru", "811d408e576c2f59809f5ba13ae638fed7950428", "Running on Waves", "Alexander Grin", "unmatched FantLab diagnostic"),
    ("verne-children-captain-grant-beketova-ru", "140823b70e9ac28a5fc24b402e75f3e83bf5bb8f", "The Children of Captain Grant", "Jules Verne · Alexandra Beketova translation", "Scriptorium-only derived metrics"),
)
METRICS = (
    ("fantlab.general.characters", "Characters including spaces", "characters", False),
    ("fantlab.general.words", "Word tokens", "words", False),
    ("fantlab.general.mean_word_length_chars", "Mean word length", "characters/word", True),
    ("fantlab.general.mean_sentence_length_chars", "Mean sentence length", "characters/sentence", True),
    ("fantlab.dialogue.share_percent", "Dialogue share", "%", True),
    ("fantlab.dialogue.author_text_inside_dialogue_percent", "Author text in dialogue", "%", True),
    ("fantlab.vocabulary.unique_words", "Unique word forms", "types", False),
    ("fantlab.punctuation.comma.per_1000_words", "Commas", "per 1,000 words", True),
    ("fantlab.punctuation.dash.per_1000_words", "Dashes", "per 1,000 words", True),
    ("fantlab.punctuation.question.per_1000_words", "Question marks", "per 1,000 words", True),
)

class GalleryError(ValueError):
    """Unverified or unsafe source-free evidence."""


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise GalleryError("duplicate JSON key")
        result[key] = value
    return result


def _load(root: Path, index: int):
    candidate, expected_blob, title, author, evidence = SOURCES[index]
    relative = Path("corpus/candidates/diagnostics") / (candidate + ".json")
    root = root.resolve()
    path = root / relative
    if path.is_symlink() or path.absolute() != path.resolve(strict=False):
        raise GalleryError("unsafe source path")
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        details = os.fstat(fd)
        if not stat.S_ISREG(details.st_mode) or not 0 < details.st_size < 2_000_000:
            raise GalleryError("source must be a bounded regular file")
        data = os.read(fd, 2_000_001)
    finally:
        os.close(fd)
    if hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() != expected_blob:
        raise GalleryError("frozen evidence checksum mismatch")
    doc = json.loads(data.decode("utf-8"), object_pairs_hook=_unique_pairs,
                     parse_constant=lambda _: (_ for _ in ()).throw(GalleryError("nonfinite JSON")))
    if not isinstance(doc, dict) or doc.get("candidate_id") != candidate or doc.get("source_text_committed") is not False:
        raise GalleryError("unreviewed source identity")
    body = doc.get("body_identity", {})
    size = body.get("character_count_including_spaces")
    if type(size) is not int or size < 300_000 or len(str(body.get("raw_sha256", ""))) != 64:
        raise GalleryError("full-work body identity missing")
    gates = doc.get("gates", {})
    if (gates.get("fantlab_source_edition_match") != "unknown" or
            gates.get("m2_parity_admissible") is not False or gates.get("m2_weight") != 0 or
            gates.get("gate_ready") is not False):
        raise GalleryError("unverified scientific gate")
    if index == 0:
        if (doc.get("comparison_policy", {}).get("class") != "diagnostic_unmatched_source" or
                doc.get("fantlab", {}).get("source_edition_disclosed") is not False or
                doc.get("fantlab", {}).get("source_bytes_disclosed") is not False):
            raise GalleryError("diagnostic status drift")
    elif (doc.get("translation_identity") != "Alexandra A. Beketova Russian translation" or
          doc.get("interpretation", {}).get("fantlab_comparison_performed") is not False):
        raise GalleryError("translation or parity status drift")
    metric_rows = doc.get("metrics")
    if not isinstance(metric_rows, list) or len(metric_rows) > 500:
        raise GalleryError("invalid metric collection")
    values = {}
    for row in metric_rows:
        if not isinstance(row, dict) or not isinstance(row.get("metric_id"), str):
            raise GalleryError("invalid metric row")
        mid = row["metric_id"]
        if mid in values:
            raise GalleryError("duplicate metric")
        status = row.get("status" if index == 0 else "compatibility_status")
        allowed = {"diagnostic_only_source_unmatched", "not_run_dependency_unbound"} if index == 0 else {"inferred", "extension"}
        if status not in allowed:
            raise GalleryError("invalid scientific status")
        number = row.get("scriptorium_raw_value" if index == 0 else "value")
        if number is not None and (type(number) not in (int, float) or not math.isfinite(number)):
            raise GalleryError("non-finite metric")
        if status == "not_run_dependency_unbound" and number is not None:
            raise GalleryError("not-run cannot have a value")
        values[mid] = number
    for key, _, unit, normalized in METRICS:
        value = values.get(key)
        if value is None or value < 0 or (unit == "%" and value > 100):
            raise GalleryError("missing or invalid shared measurement")
    # Cardinal observations are countable events; JSON 10.0 is not an integer.
    for metric_id in ("fantlab.general.characters", "fantlab.general.words",
                      "fantlab.vocabulary.unique_words"):
        if type(values[metric_id]) is not int:
            raise GalleryError("cardinal measurement must be an integer")
    if (values["fantlab.general.characters"] != size or
            values["fantlab.general.words"] > size or
            values["fantlab.vocabulary.unique_words"] > values["fantlab.general.words"]):
        raise GalleryError("inconsistent body statistics")
    profiles = doc.get("scriptorium", {}).get("profiles", {})
    return {"id": candidate, "title": title, "author": author, "evidence": evidence,
            "body": size, "body_hash": body["raw_sha256"], "json_hash": hashlib.sha256(data).hexdigest(),
            # Each of these algorithms can change at least one displayed metric.
            "profiles": tuple(profiles.get(k) for k in (
                "metrics", "normalization", "dialogue", "vocabulary", "punctuation"
            )),
            "values": values}


def load_gallery(root: Path):
    records = tuple(_load(root, index) for index in range(2))
    if (any(type(p) is not str or not p for p in records[0]["profiles"]) or
            records[0]["profiles"] != records[1]["profiles"]):
        raise GalleryError("incompatible measurement profiles")
    return records


def render_csv(records):
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(("candidate_id", "work", "metric_id", "label", "unit", "value", "evidence", "body_sha256", "source_json_sha256"))
    for record in records:
        for mid, label, unit, _ in METRICS:
            writer.writerow((record["id"], record["title"], mid, label, unit, str(record["values"][mid]),
                             record["evidence"], record["body_hash"], record["json_hash"]))
    return out.getvalue()


def render_html(records):
    esc = lambda text: html.escape(str(text), quote=True)
    cards = []
    for record in records:
        cards.append("<article class='card'><p class='eyebrow'>" + esc(record["evidence"]) +
                     "</p><h2>" + esc(record["title"]) + "</h2><p>" + esc(record["author"]) +
                     "</p><strong class='big'>" + format(record["body"], ",") +
                     "</strong><p>Characters including spaces</p><details><summary>Inspect source identity</summary>" +
                     "<p>Literary body SHA-256: <code>" + record["body_hash"] +
                     "</code></p><p>Frozen JSON SHA-256: <code>" + record["json_hash"] + "</code></p></details></article>")
    rows, charts = [], []
    for mid, label, unit, normalized in METRICS:
        a, b = (record["values"][mid] for record in records)
        rows.append("<tr><th scope='row'>" + esc(label) + " <small>" + esc(unit) + "</small></th><td>" +
                    esc(a) + "</td><td>" + esc(b) + "</td></tr>")
        if normalized:
            upper = max(a, b)
            bars = []
            for name, value, cssclass in (("Grin", a, "teal"), ("Verne", b, "ochre")):
                width = format(value / upper * 100 if upper else 0, ".5f")
                bars.append("<div class='bar'><span>" + name + "</span><div class='track'><div class='fill " +
                            cssclass + "' style='width:" + width + "%'></div></div><strong>" +
                            format(value, ".2f") + "</strong></div>")
            charts.append("<li><h3>" + esc(label) + " <small>" + esc(unit) + "</small></h3>" + "".join(bars) + "</li>")
    css = """*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f6f1e5;color:#20312b;font:16px/1.55 system-ui,sans-serif}.wrap{max-width:1120px;margin:auto;padding:clamp(1rem,4vw,3rem)}h1,h2,h3{font-family:Georgia,serif;font-weight:400;line-height:1.15}h1{font-size:clamp(2.8rem,6vw,5.5rem)}.lede{font-size:1.15rem;max-width:65ch}.eyebrow{font-size:.8rem;color:#20665f;text-transform:uppercase;letter-spacing:.09em;font-weight:700}.skip{position:absolute;top:-5rem;left:1rem;background:white;padding:1rem}.skip:focus{top:1rem}a{color:#14615a}a:focus-visible,summary:focus-visible,.scroll:focus-visible{outline:3px solid #a24f07;outline-offset:4px}.notice{padding:1rem 1.4rem;background:#e1ece6;border-left:5px solid #266b64}.cards,.charts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.card,.charts li{min-width:0;background:#fffdf8;border:1px solid #d7cebd;border-radius:.7rem;padding:1.4rem}.big{display:block;font:3rem Georgia,serif;margin:1rem 0}.card code{overflow-wrap:anywhere}.charts{padding:0;list-style:none}.charts h3{font-size:1.2rem}.charts small,th small{font:.8rem system-ui,sans-serif;color:#52635b}.bar{display:grid;grid-template-columns:3rem minmax(0,1fr) 4rem;gap:.6rem;align-items:center;font-size:.85rem;margin:.7rem 0}.bar strong{text-align:right}.track{background:#e2e0d5;height:.9rem;border-radius:3px;overflow:hidden}.fill{height:100%;border-radius:3px}.teal{background:#277069}.ochre{background:#ae7134}section{padding-top:2.5rem}.scroll{overflow:auto;background:#fffdf8;border:1px solid #d7cebd;border-radius:.5rem}table{border-collapse:collapse;width:100%;min-width:570px}caption{text-align:left;padding:1rem}th,td{text-align:left;padding:.8rem 1rem;border-bottom:1px solid #ded4c5;font-variant-numeric:tabular-nums}summary{cursor:pointer;min-height:44px;padding:.8rem 0;font-weight:700}footer{margin-top:3rem;border-top:1px solid #d7cebd;padding:1.5rem 0}@media(max-width:700px){.cards,.charts{grid-template-columns:1fr}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}"""
    return ("<!doctype html>\n<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>" +
            "<title>Scriptorium — Two analyzed works</title><style>" + css + "</style></head><body>" +
            "<a class='skip' href='#main'>Skip to content</a><main id='main' class='wrap'><header><p class='eyebrow'>Scriptorium / Literary measurement</p>" +
            "<h1>Two books. Different rhythms.</h1><p class='lede'>Real source-free measurements from two frozen full works. " +
            "These are Scriptorium-side observations, not proven FantLab parity.</p><nav><a href='#comparison'>See the comparison ↓</a></nav></header>" +
            "<aside class='notice' role='note'><strong>Scientific boundary: M2 0/5.</strong> Both works exceed 300,000 characters, " +
            "but FantLab analyzer-input identity is unknown. The Verne entry is the distinct Beketova translation. " +
            "No manuscript text is present.</aside><section aria-labelledby='works'><h2 id='works'>The works</h2>" +
            "<div class='cards'>" + "".join(cards) + "</div></section><section aria-labelledby='comparison'><h2 id='comparison'>Compare the language</h2>" +
            "<p>Seven normalized measures, scaled separately within each row. Bar lengths cannot be compared across measures.</p>" +
            "<ul class='charts'>" + "".join(charts) + "</ul></section><section aria-labelledby='values'><h2 id='values'>Exact numbers</h2>" +
            "<p>Absolute counts are not style scores. Values retain their inferred or diagnostic scientific status.</p>" +
            "<div class='scroll' tabindex='0' role='region' aria-label='Exact metrics comparison'><table>" +
            "<caption>Ten shared metrics and their units</caption><thead><tr><th scope='col'>Metric</th><th scope='col'>Running on Waves</th>" +
            "<th scope='col'>Children of Captain Grant · Beketova</th></tr></thead><tbody>" + "".join(rows) +
            "</tbody></table></div></section><footer>" + esc(PROFILE) + " · offline · no tracking · M2 0/5</footer></main></body></html>\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--format", choices=("html", "csv"), default="html")
    args = parser.parse_args(argv)
    try:
        records = load_gallery(args.repo_root)
        result = render_html(records) if args.format == "html" else render_csv(records)
    except (GalleryError, OSError, TypeError, ValueError, KeyError):
        print("Cannot build gallery: frozen source-free evidence is unavailable or incompatible.", file=sys.stderr)
        return 2
    sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
