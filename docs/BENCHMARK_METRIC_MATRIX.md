# Retained FantLab field-by-field diagnostics (#281)

The five-work readiness matrix validates legally usable frozen body witnesses and
source/reference identity metadata. This companion command **inspects retained,
source-free metric evidence** without downloading manuscripts or inventing benchmark runs:

~~~sh
python -m scriptorium.benchmark_metric_matrix --root . --format markdown
python -m scriptorium.benchmark_metric_matrix --root . --format json --output /tmp/retained-metrics.json
python -m scriptorium.benchmark_metric_matrix --root . --format csv --output /tmp/retained-metrics.csv
~~~

The command creates output files only; it never overwrites an existing report.
JSON, CSV and Markdown are deterministic from the checked-in records and include
no source prose. CSV emits one row per retained metric, plus a clearly labelled
**NOT_RUN** coverage row for each candidate without an existing metric artifact.

## Evidence actually available

- **Five** frozen public candidates have independently recorded
  character-count witnesses and dated FantLab reference URLs.
- **Anna Karenina** has an older, source-unmatched diagnostic with **28** metric
  rows: **23** raw expected/actual/delta observations and **five** without a
  numeric actual (dictionary-dependent vocabulary fields).
- **Running on Waves** already has a source-frozen, Git-blob-pinned report with
  **27 retained metrics**, **23 measured** and **four dictionary-dependent NOT_RUN**
  rows. Its full source has 363,819 characters, vs 360,987 displayed by FantLab
  (+2,832); the source edition is NOT proven to be FantLab's input. This is
  recovered prior work, not a new analysis or evidence of exact parity.
- **The Silver Dove** now has a permanently retained byte-for-byte copy of
  the exact 2026-10-26 successful CI receipt: **29 Scriptorium fields**,
  **24 numeric**, **five NOT_RUN**; its only retained FantLab displayed
  reference counts are characters and words. The other **27 expected values
  are UNKNOWN**, not zero. The sentence count is a Scriptorium extension.
- **The Brothers Karamazov and The Hyperboloid of Engineer Garin** still have
  no retained field-by-field artifact: their metric status remains **NOT_RUN**.
- All five FantLab analyzer-input identities are **UNKNOWN**. M2 remains **0/5**.
  Even a numerically equal row is **UNRESOLVED_SOURCE**, not a PASS.

The reader joins the original `scriptorium-fantlab-readiness-v1` source witnesses,
the independent `work270306.json` reference, and the frozen
`work270306-wikisource-diagnostic.json` artifact. It rejects mismatched
candidate/reference URLs, dates, source raw/normalized hashes, re-run integrity,
declared source-match upgrades, missing/extra metric IDs, forged expected values,
nonfinite actual values and inconsistent integer/decimal raw deltas. The existing
benchmark field registry supplies the metric ID/path mapping rather than a
competing new definition.

**Limits:** a retained diagnostic is not a fresh re-execution, authentication of
the stored evidence, proof of the FantLab original input, or proof of FantLab
decimal display/tie-breaking rules. Floating raw deltas are checked against
the stored numerical values for internal arithmetic consistency; the original
recorded delta is returned unchanged. This does not relax the per-metric parity
contract or replace `scriptorium.benchmark`. To create *new* field-by-field
comparison evidence, run that existing harness on legally usable local bytes
with the correct provenance fields.

The remaining scientific work for #281 requires two more properly bound
field-level runs, independent reference-rounding evidence, and—before any M2
progress—actual confirmed FantLab analyzer-input identity for five qualifying
works. No artifact in this preview meets that gate.


## Reusing the frozen Running on Waves evidence (#281)

The 27-field, source-free artifact
`corpus/candidates/diagnostics/grin-running-on-waves-ru.json` was already present
but excluded from the consolidated matrix. The report now binds its original
Git-blob SHA-1 to the reviewed full-work gallery record, checks exact source-body
SHA-256 and character count against the separate five-work readiness witness,
and validates the dated FantLab reference, metric profile and all 27 displayed
reference lexemes against the original versioned diagnostic definitions.

The 23 measured raw deltas must reproduce the source artifact's exact
integer/Decimal arithmetic; four unbound dictionary actuals stay NOT_RUN.
No original diagnostic is rewritten and no FantLab floating rounding tolerance
is inferred. Anna and Running on Waves still contribute exactly 55 recorded
fields, 46 numeric observations and nine missing actuals; the new Silver Dove
receipt adds 29 rows (24 numeric and five missing). The consolidated matrix
now has **84 rows** across three works; the two works without retained diagnostics
remain **NOT_RUN**. The readiness files continue to
document **character-count/source readiness** separately.

The Reader keeps its accessible, progressive **28-row Anna explorer** and
adds an **independent 27-row Running on Waves explorer**. Both tables support
local-only search by label/ID, metric family and measurement availability,
with keyboard controls, counts, reset and a no-JavaScript/print fallback.
Their unit labels, scientific statuses and JSON/CSV exports are unchanged.
Site build is not Pages deployment or visual verification. M2 remains 0/5.



## Retaining the exact Silver Dove CI measurements (#281)

The checked-in `corpus/candidates/diagnostics/bely-silver-dove-ru.json` has
**identical original Git blob bytes** to the source-free JSON emitted by the
successful 2026-10-26 `Silver Dove measured field diagnostic` workflow,
PR #325 HEAD `5f107a3d79a9a2270f0e672b777093cf893b006b`,
run `40266373995`. The reviewed blob SHA-1 is
`88bfe95435be1b72703de65d314c6926b5f83a60`; JSON SHA-256 is
`e78b973199dec86a3b41ab30311dd9e9a4e1abe57e4916190bc62eb553353f53`.
A failed source-provenance match, blob change, profile drift, unbound vocabulary
value, fabricated expected value or integer-delta discrepancy stops the matrix
and site build before publication. Original literary bytes are not retained.

The 29-row report has 24 measured Scriptorium candidate values, five
dictionary-dependent `NOT_RUN` values, and **only two** dated FantLab public
reference counts: 549,050 characters vs 563,125 frozen (+14,075) and 83,369
words vs 88,236 frozen (+4,867). Other FantLab expected values and
deltas are `UNKNOWN` in the page, `null`/empty in source-free exports.
The sentence count is separately labelled an **extension**; no new parity,
author-voice or FantLab definition claims are made. M2 remains **0/5**.
Build is distinct from deployment and real browser visual verification.

## Two-work normalized-rate view (Reader)

The built FantLab evidence page includes a **20-row side-by-side** table drawn
exclusively from the same frozen 28-row Anna and 27-row Running on Waves reports.
Rows must have an actual value in **both** reports, the same registry metric ID
and a candidate unit of characters per word/sentence, occurrences per 1,000
word tokens, or percent. Raw character, word and unique-vocabulary totals are
excluded because corpus lengths differ; dictionary-dependent missing values
stay absent rather than becoming zero. No additional text is downloaded or
reanalyzed.

The signed difference is **Running on Waves minus Anna Karenina**. Differences
in percentage-valued fields use **percentage points**, not percent change.
Numeric arithmetic uses decimal representations of retained raw observations,
without rounding them to FantLab's display precision. The individual metric
rows and JSON/CSV downloads remain unchanged and preserve every missing state.

The view is **descriptive only**: both source editions are unverified against
FantLab's analyzer inputs, and nominally matching units do not prove that
FantLab used the same tokenization, dialogue denominators or normalization.
Two different works do not establish a causal author/genre effect or an author
profile. The new table does not count toward M2, which remains **0/5**.

## Source-free local evidence page

Build the canonical site with `scriptorium site --repo-root . --output build/site`,
then open `build/site/evidence/fantlab/index.html` (or follow **FantLab evidence**
from the built homepage). The route renders the existing validated five-work report:
the Anna Karenina diagnostic with 28 rows (23 numeric actuals and five
unavailable) and a searchable Running on Waves table with 27 rows (23 numeric
actuals and four NOT_RUN), plus a static accessible Silver Dove table of 29
fields (24 numeric and five NOT_RUN). The remaining two works remain `NOT_RUN`.
The same validated machine-readable `metrics.json` and `metrics.csv` exports
include all 84 rows, explicitly retaining unknown FantLab references.

The route is explicitly registered in the publication allow-list and refuses
contradictory source/reference hashes, invented metric values, forged parity status,
and unrecognized registration. It carries no source prose, cannot enable deployment,
and does not prove FantLab input identity or rounding. **M2 stays 0/5.**
The built artifact is not a live Pages publication; desktop/mobile screenshots
remain `VISUAL_NOT_VERIFIED` until browser access is permitted.

## Evidence page label contract

The built HTML gives each of the 28 retained metric rows its human-readable Russian
label from the existing versioned benchmark comparison registry, its family and
unchanged technical ID. Evidence statuses have explanatory English descriptions
and retain their underlying machine values. JSON/CSV remain byte-identical to the
validated source-free matrix; this is a reader-facing display improvement, not
new metric execution, source matching, decimal rounding proof or FantLab parity.

## Quick navigation by metric family

The static five-work evidence page has keyboard-accessible links to its
Dialogue (4), General (4), Punctuation (14) and Vocabulary (6) rows. Each link
jumps to the first row of its family in the unchanged 28-row semantic table.
The links need no JavaScript; the full table is visible in print and offline,
and source-free JSON/CSV downloads are unaffected. This is presentation
only, not a new analysis run or parity evidence. Browser visuals remain
`VISUAL_NOT_VERIFIED` until an allowed desktop/mobile test succeeds.

## Frozen-source character evidence in the Reader (#281)

The existing five-work evidence page now exposes the **separately validated**
readiness records next to metric coverage: public-domain source and edition links,
frozen public-body characters (spaces included), FantLab displayed character
counts and **actual minus displayed** diagnostic deltas. A visitor can check
both the metric run state and the source evidence without downloading a book.

The renderer independently binds each readiness row to its metric-matrix
candidate ID, frozen raw digest, dated FantLab reference and explicit UNKNOWN
input identity. Contradictory lengths, delta arithmetic, rights evidence or
unsafe source URLs reject the built page before atomic publication.

This changes only the human-readable built HTML. The verified metrics.json
and metrics.csv exports remain byte-identical, and the separate
`python -m scriptorium.benchmark_readiness --format json|csv` CLI remains
the source-free way to inspect all normalized/raw hashes and rights evidence.
No new FantLab benchmark was run; M2 remains 0/5. A successful local Pages
build is not live deployment or visual acceptance.

## Measurement availability by family

The canonical Reader evidence route derives a source-free coverage table from the
same validated 28-row Anna Karenina metric matrix as the detailed rows. It
separates **measured actual** from **NOT_RUN** and **UNRESOLVED_NO_ACTUAL**:

| Metric family | Measured | NOT_RUN | Unavailable actual | Total |
| --- | ---: | ---: | ---: | ---: |
| General | 4 | 0 | 0 | 4 |
| Dialogue | 4 | 0 | 0 | 4 |
| Punctuation | 14 | 0 | 0 | 14 |
| Vocabulary | 1 | 2 | 3 | 6 |

Each family links to its full per-metric table. Coverage is an availability
inventory, not a parity score; all 23 measured values remain **UNRESOLVED_SOURCE**,
the two works without retained diagnostics remain **NOT_RUN**, and M2 remains 0/5.
The export field names, reference editions and parity gates are unchanged;
the new Silver Dove measurements are versioned, not source-matched.
Malformed coverage totals fail closed rather than silently displaying a false
measurement count. Browser visual acceptance remains unverified.

## Downloadable source provenance from the Reader

The canonical `evidence/fantlab/` route now packages `readiness.json` and
`readiness.csv` alongside the unchanged `metrics.json` / `metrics.csv`.
Both new files come from the same validated five-work readiness object already
joined to the metric matrix. JSON retains the raw and normalized SHA-256
witnesses, public-domain evidence, source/edition metadata and dated FantLab
references; CSV exposes its established flat source summary. No full text,
new benchmark execution, inferred source match or public-upload feature is added.

The page has direct download links. The deterministic site `build.json` records
SHA-256 identities for both added exports, and the repository tests verify that
the packaged files equal the existing source-free readiness CLI renderers.
Corrupt or contradictory canonical evidence stops the build before the last
valid site is replaced. M2 remains 0/5; built is not deployed or visually verified.

## Progressive local metric explorer (#283)

The FantLab evidence page now has **two independent** local-only, keyboard-labelled
filters: Anna Karenina (28 rows) and Running on Waves (27 rows). Each searches
human labels or stable field IDs, filters by Dialogue/General/Punctuation/Vocabulary
and measured/NOT_RUN/actual-unavailable state, and has its own live count and
reset action. Metric-family jumps reveal hidden targets. Without JavaScript both
full filtered tables remain visible; printing restores their 55 rows after
filtering, while the new Silver Dove table always shows all 29 fields.
No search text is sent off-device, stored or submitted.

Filtering changes **only on-screen visibility**. There are **all 84 rows in exports**:
55 in the two independently filtered work tables and 29 in the static Silver
Dove table. The five-work source witness inventory and readiness files are
unchanged; the metrics JSON/CSV gain the reviewed new measurements.
A measured row is NOT a parity pass: FantLab input identity and decimal rounding
remain unknown. M2 is 0/5. Browser screenshots require later visual verification.

## Inspect units in the evidence table (#283)

The Reader's 28-row Anna Karenina diagnostic table explicitly labels the Scriptorium
candidate unit for **every** retained metric. Character, token, sentence, vocabulary
window and occurrences-per-1,000-token quantities must not appear as anonymous
numbers. The displayed **actual − expected** difference uses the same unit as the
value, except for percentage-valued metrics, where the difference is in **percentage
points** (not a relative percent change). Vocabulary UASZ values are means of
unique word forms in complete sliding windows of the stated token length.

The mapping covers exactly the retained benchmark field registry; new metric IDs
require an explicit, reviewed unit decision. These units describe Scriptorium's
current candidate definitions, **not proof** that FantLab uses identical
segmentation, denominator or rounding rules. Metric JSON/CSV and source readiness
exports are unchanged, M2 remains 0/5, and browser visuals remain unverified until
real desktop/mobile checks can run.


## Download the observed two-work rate differences

The FantLab evidence route now offers \`shared-rates.json\` and
\`shared-rates.csv\`, a portable export of the same **20 measured rates**
shown in the existing side-by-side table. Each row includes stable metric
identity, candidate unit, both unrounded retained observations and the exact
signed *Running on Waves minus Anna Karenina* decimal difference. Percent
differences use **percentage points**, not relative percentages.

The exports bind both works to frozen raw SHA-256 source witnesses and dated
FantLab references. They explicitly mark their scientific status
\`diagnostic_source_unmatched\` / input identity \`UNKNOWN\`, with M2
weight zero. Raw size/vocabulary totals, missing observations and any parity
promotion are excluded. Original 55-row \`metrics.json/csv\` and source
\`readiness.json/csv\` retain their previous content.

The canonical site builder computes these files from validated retained
records, writes them atomically with the site, and records their SHA-256
digests in \`build.json\`. Build and packaging tests assert deterministic
output and correct scientific boundaries. This is no new full-text run
and is not a deployed or visually verified Pages release.
