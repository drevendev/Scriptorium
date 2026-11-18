"""Accessible, strictly source-free offline HTML view of private tag curation.

The input is a versioned *derived* report, not book text. This renderer never
publishes anything and never upgrades curator claims into verified rights.
"""
from __future__ import annotations

from html import escape
from math import isfinite
import re

from .tag_profile import FEATURES, VERSION

_SHA = re.compile(r"[0-9a-f]{64}\Z")
_BOUNDARY = {
    "class": "private_curator_declared_descriptive_extension",
    "public_release_ready": False,
    "rights_independently_verified": False,
    "fantlab_parity": False,
    "m2_source_matched": 0,
    "no_source_text": True,
}
_LABELS = {
    "fantlab.general.mean_word_length_chars": "Mean word length",
    "fantlab.general.mean_sentence_length_chars": "Mean sentence length",
    "fantlab.dialogue.share_percent": "Dialogue share",
    "fantlab.punctuation.comma.per_1000_words": "Comma frequency",
    "fantlab.punctuation.dash.per_1000_words": "Dash frequency",
}


def _esc(value: object) -> str:
    return escape("NOT_RUN" if value is None else str(value), quote=True)


def _number(value: object, *, minimum: float = 0, maximum: float | None = None) -> bool:
    return (type(value) in (int, float) and isfinite(value) and value >= minimum
            and (maximum is None or value <= maximum))


def _validated(report: dict) -> list[dict]:
    if type(report) is not dict or report.get("schema_version") != VERSION:
        raise ValueError("unsupported tag profile schema")
    boundary = report.get("scientific_boundary")
    if (type(boundary) is not dict or set(boundary) != set(_BOUNDARY)
            or any(type(boundary[k]) is not type(v) or boundary[k] != v
                   for k, v in _BOUNDARY.items())):
        raise ValueError("private scientific/publication boundary must be preserved")
    if type(report.get("source_snapshot_sha256")) is not str or not _SHA.fullmatch(report["source_snapshot_sha256"]):
        raise ValueError("invalid source snapshot identity")
    if type(report.get("taxonomy_version")) is not str or not report["taxonomy_version"]:
        raise ValueError("missing taxonomy identity")
    tags = report.get("tags")
    if type(tags) is not list or not tags:
        raise ValueError("missing curated tag summaries")
    seen_tags = set()
    for tag in tags:
        if type(tag) is not dict or type(tag.get("tag_id")) is not str or tag["tag_id"] in seen_tags:
            raise ValueError("invalid/duplicate tag")
        seen_tags.add(tag["tag_id"])
        if type(tag.get("label")) is not str or not tag["label"].strip():
            raise ValueError("invalid tag label")
        works = tag.get("works")
        count = tag.get("confirmed_work_count")
        if type(works) is not list or type(count) is not int or len(works) != count:
            raise ValueError("invalid confirmed-work count")
        warning = "NO_CONFIRMED_WORKS" if count == 0 else "SINGLE_WORK" if count == 1 else "DESCRIPTIVE_ONLY"
        if tag.get("sample_warning") != warning:
            raise ValueError("inconsistent sample warning")
        for work in works:
            if type(work) is not dict or any(type(work.get(k)) is not str for k in
                    ("key", "edition_id", "candidate_id", "source_sha256", "rights_basis",
                     "rights_evidence_url", "tag_authority", "tag_evidence_url")):
                raise ValueError("invalid edition provenance")
            if _SHA.fullmatch(work["source_sha256"]) is None:
                raise ValueError("invalid edition hash")
        metrics = tag.get("metrics")
        if type(metrics) is not list or len(metrics) != len(FEATURES):
            raise ValueError("invalid metric coverage")
        seen_metrics = set()
        for row in metrics:
            if type(row) is not dict or row.get("id") not in FEATURES or row["id"] in seen_metrics:
                raise ValueError("unknown/duplicate tag metric")
            key = row["id"]
            seen_metrics.add(key)
            if row.get("unit") != FEATURES[key]:
                raise ValueError("mismatched metric unit")
            observed, missing = row.get("observed_count"), row.get("missing_count")
            if type(observed) is not int or type(missing) is not int or observed < 0 or missing < 0 or observed + missing != count:
                raise ValueError("inconsistent missingness")
            maximum = 100 if FEATURES[key] == "%" else None
            vals = [row.get("mean_per_work"), row.get("minimum"), row.get("maximum")]
            std = row.get("population_stddev_between_works")
            if observed == 0:
                if any(v is not None for v in vals) or std is not None:
                    raise ValueError("unobserved metric cannot have numeric values")
            else:
                if not all(_number(v, maximum=maximum) for v in vals) or not vals[1] <= vals[0] <= vals[2]:
                    raise ValueError("invalid observed metric range")
                if observed == 1 and std is not None:
                    raise ValueError("single-work dispersion must be NOT_RUN")
                if observed > 1 and not _number(std):
                    raise ValueError("invalid observed dispersion")
        if seen_metrics != set(FEATURES):
            raise ValueError("missing tag metrics")
    return tags


def render_tag_profiles_html(report: dict) -> str:
    """Make a self-contained print-friendly research report with no manuscript prose."""
    tags = _validated(report)
    content = []
    for tag in tags:
        count = tag["confirmed_work_count"]
        content.append('<section class="tag" aria-label="Tag profile">')
        content.append(f'<h2>{_esc(tag["label"])} <small>({_esc(tag["tag_id"])})</small></h2>')
        content.append(f'<p class="size">Confirmed curated editions: <strong>{count}</strong>. '
                       f'Sample: <strong>{_esc(tag["sample_warning"])}</strong>.</p>')
        if count == 0:
            content.append('<p class="caution">No confirmed editions. All measurements are NOT_RUN, not zero.</p>')
        elif count == 1:
            content.append('<p class="caution">One edition: between-work dispersion is NOT_RUN.</p>')
        content.append('<div class="scroll" tabindex="0" role="region" aria-label="Tag numeric metrics; scroll horizontally if needed">'
                       '<table><caption>Five descriptive measurements; unweighted across observed editions</caption>'
                       '<thead><tr><th scope="col">Metric</th><th scope="col">Mean</th>'
                       '<th scope="col">Between-work SD</th><th scope="col">Range</th>'
                       '<th scope="col">Observed / missing</th><th scope="col">Unit</th></tr></thead><tbody>')
        by_id = {row["id"]: row for row in tag["metrics"]}
        for metric in FEATURES:
            row = by_id[metric]
            low, high = row["minimum"], row["maximum"]
            span = "NOT_RUN" if low is None else f"{low}–{high}"
            content.append('<tr>'
                           f'<th scope="row">{_esc(_LABELS[metric])}</th>'
                           f'<td>{_esc(row["mean_per_work"])}</td>'
                           f'<td>{_esc(row["population_stddev_between_works"])}</td>'
                           f'<td>{_esc(span)}</td>'
                           f'<td>{row["observed_count"]} / {row["missing_count"]}</td>'
                           f'<td>{_esc(FEATURES[metric])}</td></tr>')
        content.append('</tbody></table></div>')
        if count:
            content.append('<h3>Curator-declared evidence (not independently verified)</h3><ul class="evidence">')
            for work in tag["works"]:
                content.append('<li>'
                               f'Edition <code>{_esc(work["edition_id"])}</code>; '
                               f'work <code>{_esc(work["candidate_id"])}</code>; '
                               f'SHA-256 <code>{_esc(work["source_sha256"])}</code>. '
                               f'Rights claim: {_esc(work["rights_basis"])} '
                               f'({_esc(work["rights_evidence_url"])}). '
                               f'Tag: {_esc(work["tag_authority"])} '
                               f'({_esc(work["tag_evidence_url"])}).</li>')
            content.append('</ul>')
        content.append('</section>')
    return '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Scriptorium · Private tag profiles</title>
<style>
:root{color-scheme:light;background:#faf7f0;color:#202c29;font-family:Georgia,'Times New Roman',serif}
*{box-sizing:border-box}body{margin:0}main{max-width:66rem;margin:auto;padding:clamp(1rem,4vw,3rem)}
h1,h2{line-height:1.15}h1{font-size:clamp(1.85rem,5vw,3rem)}h2{font-size:1.45rem}small{font-size:.75em;font-weight:normal}
.intro,.size{line-height:1.65}.caution{padding:.7rem 1rem;border-left:4px solid #9d662a;background:#f4e8d2}
.tag{margin:2rem 0;padding:1.25rem;background:white;border:1px solid #aebcb6;border-radius:.6rem}
.scroll{max-width:100%;overflow-x:auto} .scroll:focus-visible{outline:3px solid #156f61;outline-offset:2px}
table{border-collapse:collapse;width:100%;min-width:42rem;font-size:.96rem}caption{text-align:left;padding:.8rem 0}
th,td{text-align:left;padding:.6rem .55rem;border-bottom:1px solid #a5b5b0;vertical-align:top}
thead{background:#e2ede8}tbody tr:nth-child(even){background:#f0f5f2}
.evidence{padding-left:1.2rem;line-height:1.6}.evidence li{margin:.8rem 0;overflow-wrap:anywhere}
code{font-size:.87em}footer{margin-top:2rem;border-top:1px solid #aebcb6;padding-top:1rem}
@media(max-width:40rem){.tag{padding:.8rem}table{font-size:.86rem}}
@media print{*{background:white!important;color:black!important}main{padding:0}.tag{break-inside:avoid;border:1px solid #777}.scroll{overflow:visible}table{min-width:0;font-size:9pt}.caution{border:1px solid #777}}
</style></head><body><main>
<h1>Private curated tag profiles</h1>
<p class="intro"><strong>Descriptive extension only.</strong> This is an offline, source-free report for curator review, not a public Reader release, a verified rights clearance, an author fingerprint or FantLab parity. Edition and tag evidence is curator-declared. M2: 0/5.</p>
<p class="intro">Taxonomy: <code>''' + _esc(report["taxonomy_version"]) + '''</code>. Derived snapshot SHA-256: <code>''' + _esc(report["source_snapshot_sha256"]) + '''</code>. Values are unweighted means across measured editions; absent evidence is <strong>NOT_RUN</strong>, never zero.</p>
''' + "\n".join(content) + '''
<footer>Local report only · no scripts, network assets, manuscript text or automatic publication.</footer>
</main></body></html>
'''
