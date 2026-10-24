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
