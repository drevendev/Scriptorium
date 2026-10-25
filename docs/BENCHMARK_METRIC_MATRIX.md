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
- **The Brothers Karamazov, The Silver Dove, The Hyperboloid of Engineer Garin,
  and Running on Waves** have no corresponding retained field-by-field
  benchmark artifacts in this report: their metric status is **NOT_RUN**,
  not a zero difference or a parity failure.
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

The remaining scientific work for #281 requires four more properly bound
field-level runs, independent reference-rounding evidence, and—before any M2
progress—actual confirmed FantLab analyzer-input identity for five qualifying
works. No artifact in this preview meets that gate.

## Source-free local evidence page

Build the canonical site with `scriptorium site --repo-root . --output build/site`,
then open `build/site/evidence/fantlab/index.html` (or follow **FantLab evidence**
from the built homepage). The route renders the existing validated five-work report:
one retained Anna Karenina diagnostic with 28 rows (23 numeric actuals and five
unavailable); the other four works remain `NOT_RUN`. It also provides the same
validated machine-readable `metrics.json` and `metrics.csv` exports.

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
all four other works remain **NOT_RUN**, and M2 remains 0/5. The export schemas,
retained measurements, reference editions and parity gates are unchanged.
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

The existing FantLab evidence page adds a local-only, keyboard-labelled filter over the
28 retained Anna Karenina diagnostic rows: search human labels or stable field IDs,
choose Dialogue/General/Punctuation/Vocabulary, and select measured/NOT_RUN/actual
unavailable. A live count and reset action make the current view explicit.
Choosing a metric-family jump first reveals the family target. With JavaScript
disabled the full 28-row table remains visible; printing restores all rows
even after an interactive filter was applied. No search text is sent off-device,
stored or submitted.

Filtering changes **only on-screen visibility**. The 28 scientific rows, five-work
source witness inventory and all metrics/readiness JSON and CSV files are unchanged.
A measured row is NOT a parity pass: FantLab input identity and decimal rounding
remain unknown. M2 is 0/5. Browser screenshots require later visual verification.
