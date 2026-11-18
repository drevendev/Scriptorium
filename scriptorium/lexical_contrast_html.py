"""Offline, source-free and script-free presentation of a lexical contrast report."""
from __future__ import annotations

from html import escape

_SCHEMA = "scriptorium-private-lexical-contrast-v1"
_ROWS = (
    ("Eligible pooled forms", "eligible_form_count", "forms"),
    ("Excluded rare forms", "excluded_rare_form_count", "forms"),
    ("Left-dominant forms", "left_dominant_form_count", "forms"),
    ("Right-dominant forms", "right_dominant_form_count", "forms"),
    ("Balanced forms", "balanced_form_count", "forms"),
    ("Left-dominant token share", "left_dominant_token_share_percent", "% of left tokens"),
    ("Right-dominant token share", "right_dominant_token_share_percent", "% of right tokens"),
    ("Jensen–Shannon divergence", "jensen_shannon_divergence_bits", "bits (0–1)"),
)


def _cell(value: object) -> str:
    return escape("UNKNOWN" if value is None else str(value), quote=True)


def render_lexical_contrast_html(report: dict[str, object]) -> str:
    """Render only aggregate numbers and declared provenance; never manuscript words.

    The underlying lexical contrast builder supplies the reviewed source-free
    schema. All user-provided edition and translator labels are HTML escaped.
    No scripts, remote assets, tracking or outgoing links are included.
    """
    if report.get("schema_version") != _SCHEMA:
        raise ValueError("unsupported lexical contrast schema")
    left, right = report.get("left"), report.get("right")
    aggregate = report.get("aggregate")
    if not isinstance(left, dict) or not isinstance(right, dict) or (
        aggregate is not None and not isinstance(aggregate, dict)
    ):
        raise ValueError("invalid lexical contrast report")

    rows = []
    if aggregate is None:
        rows.append('<tr><th scope="row">Lexical comparison</th>'
                    '<td>NOT_RUN / INCOMPARABLE</td><td>—</td></tr>')
    else:
        for label, key, unit in _ROWS:
            if key not in aggregate:
                raise ValueError("incomplete lexical aggregate")
            rows.append(f'<tr><th scope="row">{_cell(label)}</th>'
                        f'<td>{_cell(aggregate[key])}</td><td>{_cell(unit)}</td></tr>')

    witness_rows = []
    for label, key in (
        ("Edition ID", "edition_id"),
        ("Original-work ID (declared)", "original_work_id"),
        ("Translator (declared)", "translator"),
        ("Language", "language"),
        ("Normalized characters incl. spaces", "characters_including_spaces"),
        ("Word tokens", "word_tokens"),
        ("Distinct surface forms", "distinct_forms"),
        ("Meets 300,000-character size floor", "meets_300000_character_floor"),
        ("Normalized SHA-256", "normalized_sha256"),
    ):
        witness_rows.append(f'<tr><th scope="row">{_cell(label)}</th>'
                            f'<td>{_cell(left.get(key))}</td>'
                            f'<td>{_cell(right.get(key))}</td></tr>')
    imbalance = (
        '<p class="caution">The normalized input lengths differ by at least 2×. '
        'Lexical contrast is descriptive and strongly length-sensitive.</p>'
        if report.get("length_imbalance_warning") is True else ""
    )
    short = (
        '<p class="caution">At least one input is below 300,000 characters '
        'including spaces: this is a nonrepresentative private preview.</p>'
        if not left.get("meets_300000_character_floor") or
           not right.get("meets_300000_character_floor") else ""
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; form-action 'none'; base-uri 'none'">
<title>Scriptorium · Private lexical contrast</title>
<style>
:root{{color-scheme:light; font-family:Georgia,serif; background:#f7f3ea; color:#23352c}}
*{{box-sizing:border-box}}body{{margin:0}}main{{max-width:68rem;margin:auto;padding:clamp(1rem,4vw,3rem)}}
h1{{font-size:clamp(1.8rem,4vw,2.8rem);line-height:1.15;margin:.5rem 0 1rem}}
h2{{font-size:1.4rem;margin:2rem 0 .7rem}}p{{line-height:1.7;max-width:78ch}}
.eyebrow{{font:700 .78rem/1.5 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.12em;color:#33614d}}
.notice,.caution{{border-left:4px solid #30664c;padding:.8rem 1rem;background:#e7eee4}}
.caution{{border-color:#9b6027;background:#fcf0db}}.table-scroll{{overflow-x:auto;border:1px solid #b9c9bd;border-radius:7px}}
table{{width:100%;border-collapse:collapse;min-width:34rem;background:#fff}}caption{{text-align:left;font-weight:bold;padding:.8rem;background:#e7eee4}}
th,td{{padding:.7rem .8rem;text-align:left;border-bottom:1px solid #d5ded6;overflow-wrap:anywhere}}
th{{font-weight:700}}thead{{background:#e7eee4}}tbody tr:nth-child(even){{background:#f3f7f1}}
:focus-visible{{outline:3px solid #195d44;outline-offset:3px}}code{{overflow-wrap:anywhere}}
@media print{{:root{{background:#fff}}main{{padding:0}}.table-scroll{{overflow:visible}}table{{min-width:0;page-break-inside:auto}}tr{{break-inside:avoid}}}}
</style></head><body><main>
<p class="eyebrow">Local report · extension preview</p>
<h1>Lexical contrast</h1>
<p class="notice"><strong>Not FantLab parity, copyright clearance or an author fingerprint.</strong>
Only aggregate counts and user-declared metadata are shown. No source text, distinctive words or rare-word hashes are embedded.</p>
<p><strong>Status:</strong> {_cell(report.get("status"))}. <strong>Profile:</strong> <code>{_cell(report.get("profile"))}</code>.</p>
{imbalance}{short}
<section aria-labelledby="metrics-title"><h2 id="metrics-title">Aggregate measurements</h2><div class="table-scroll"><table>
<caption>Source-free lexical differences; unavailable is never zero</caption>
<thead><tr><th scope="col">Observation</th><th scope="col">Value</th><th scope="col">Unit</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></section>
<section aria-labelledby="evidence-title"><h2 id="evidence-title">Declared inputs and replay identity</h2><div class="table-scroll"><table>
<caption>Local inputs are not verified corpus admissions</caption>
<thead><tr><th scope="col">Field</th><th scope="col">Left</th><th scope="col">Right</th></tr></thead>
<tbody>{''.join(witness_rows)}</tbody></table></div></section>
<section aria-labelledby="method-title"><h2 id="method-title">Method and scientific limits</h2>
<p>Surface word forms: NFC + casefold, no lemmatization or ё/е fold. Types occurring at least five times across both inputs
are considered for 2× dominance using a Jeffreys +0.5 prior. Jensen–Shannon divergence uses unsmoothed token frequencies,
base-2 logarithms, and is reported in bits from 0 to 1.</p>
<p>{_cell(report.get("scientific_boundary"))}</p>
<p><strong>Corpus admission:</strong> {_cell(report.get("corpus_admission"))}.
<strong>Public release ready:</strong> {_cell(report.get("public_release_ready"))}.
No data are transmitted by this static report.</p></section>
</main></body></html>
'''
