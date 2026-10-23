# Scriptorium · Reader preview

**Understand the language of a text without uploading the manuscript.**
Scriptorium measures vocabulary, sentence length, dialogue and punctuation, then produces
readable offline reports and reproducible data. This **0.4.0a1 preview** adds private
comparison of two analyses to the canonical Reader and its real-work gallery.

## Try your own text

With Python 3.13 or later, from this checkout:

```bash
python -m pip install .
scriptorium analyze manuscript.txt --format html --output report.html
scriptorium analyze manuscript.txt --output analysis.json
scriptorium analyze manuscript.txt --format csv --output metrics.csv
```

Open `report.html` locally. All **29 metric rows** retain their units and algorithm
profiles; unavailable measurements stay unknown. The report has readable metric names,
a four-value overview, exact numeric values and keyboard-accessible tables. JSON and
CSV include source digests, not manuscript content. Choose a new output filename for
each run: existing files are never overwritten.

No runtime dependencies, account, server or telemetry are required. Installation may
fetch build tools; see [offline wheel installation](docs/READER_PREVIEW.md).
`python -m scriptorium` exposes the same commands from a checkout.

## Compare your own analyses

```bash
scriptorium analyze second-manuscript.txt --output second-analysis.json
scriptorium compare analysis.json second-analysis.json --output comparison.html
scriptorium compare analysis.json second-analysis.json --format json --output comparison.json
scriptorium compare analysis.json second-analysis.json --format csv --output comparison.csv
```

Open `comparison.html` for the same 29 measurements, explicit units, source identities
and **right minus left** differences. Percentage differences use percentage points.
Unknown measurements do not become zero; different methods or dictionaries are labelled
incomparable where applicable. JSON decimal observations and their differences retain
precision. Contradictory counts, means, punctuation rates and same-text results are rejected.
Imported JSON and hashes are declarations, not authenticated proof: rerun the analyzer
on the original bytes to verify them. [Comparison contract and examples](docs/PRIVATE_COMPARISON.md).

## Compare in your browser (private beta)

Build the canonical site with `scriptorium site --repo-root . --output build/site`
and open `build/site/compare/index.html`, or use the **Compare private reports**
action in the generated homepage. Select two local `scriptorium analyze` JSON
reports; no manuscripts or report bytes are uploaded. Inspect all 29 measurements,
incomparable/missing reasons, exact decimal right-minus-left differences, and
download source-free JSON/CSV. The browser validates the same versioned report
contract as the installed Python Reader and rejects duplicate keys, integer
lexeme spoofs, impossible counts, nonfinite values and changed units. Browser
support requires JavaScript; the offline `scriptorium compare` CLI always works.
[Browser validation and limitations](docs/PRIVATE_COMPARISON.md).

This is a **local build capability**, not a live GitHub Pages deployment. No private
manuscripts are included; imported report hashes are unauthenticated declarations.
Scientific/FantLab parity remains unverified (M2 0/5).

## Open a real literary result

The repository contains a source-free, historical full-work diagnostic for
**Anna Karenina**: **28 expected/actual/delta rows**, with 23 numeric results and five
unavailable values. No novel download is needed:

```bash
scriptorium diagnostic benchmarks/fantlab/work270306-wikisource-diagnostic.json \
  --title "Anna Karenina — full-work diagnostic" --output anna-report.html
scriptorium site --repo-root . --output build/site
```

Open `anna-report.html` or `build/site/index.html`. The canonical site retains the five
earlier evidence/report routes and the Reader 0.3 two-book comparison route.
**A successful local build is not a live GitHub Pages deployment.** The Pages activation
interlock is unchanged; this preview does not enable publishing by itself. Atomic site
replacement currently requires Linux `renameat2`; unsupported platforms fail without
deleting the previous build. Private text analysis and comparison are separate capabilities.

## Compare two already-analyzed books

No manuscript download or morphology setup is needed for the frozen **Running on Waves**
and **Children of Captain Grant — Beketova translation** comparison:

```bash
mkdir -p build
python -m scriptorium.full_work_gallery --repo-root . --format html > build/full-work-gallery.html
python -m scriptorium.full_work_gallery --repo-root . --format csv > build/full-work-evidence.csv
```

Open `build/full-work-gallery.html` for ten exact measurements and seven row-wise charts.
These are Scriptorium-side results, not FantLab parity or author-style scores. The pinned
canonical site route is `build/site/works/two-full-work-differences/index.html`, with
`measurements.json` and `measurements.csv` downloads. Navigation and export links have
44-pixel minimum touch targets; visible focus and reduced-motion styles are retained.
Newly approved replacement evidence must declare compatible source units before display;
legacy Grin diagnostics are not assigned invented source-unit fields.
Building this route does not prove GitHub Pages is deployed. Shell redirection replaces
its destination; use new filenames to keep older exports. [Method and limits](docs/FULL_WORK_GALLERY.md).

## Inspect FantLab reproduction readiness

Inspect **five frozen public literary sources** and the distance between their
character counts and the *displayed* FantLab counts, without downloading books:

~~~bash
python -m scriptorium.benchmark_readiness --root . --format markdown
python -m scriptorium.benchmark_readiness --root . --format json --output readiness.json
~~~

Each source-free report includes source rights/edition evidence, immutable body
hashes, dated FantLab references and explicit source-matching status. Differences
are **diagnostic only**: FantLab's analyzer-input identities remain unknown, other
metric comparisons are NOT_RUN and **M2 stays 0/5**.
[Readiness methodology, CSV and limitations](docs/BENCHMARK_READINESS.md).


To join a separately generated **source-free POS artifact from the same normalized
text** into a FantLab benchmark, add \`--pos-metrics pos.json\` to the
\`python -m scriptorium.benchmark --reference ... --text ... --scriptorium-revision ...\`
command. This adds **40 explicitly unresolved/diagnostic POS rows**, including
17 visible category counts and percentages, but never claims POS parity.
Unmatched text digests, profiles or inconsistent 17×17/20×17 structures are
rejected. The work488 FantLab category counts are not a simple partition of
defined words, and service-word actuals remain unknown.
[POS benchmark usage and evidence boundaries](docs/BENCHMARKING.md).

## What the results mean

FantLab-shaped metrics are **inferred compatibility candidates**, not demonstrated
parity. Scriptorium-only features are **extensions**. The historical Anna diagnostic
has no established identity match to FantLab's input text. **M2 remains 0/5**; none of
M1–M5 is declared complete by this preview. The AOT-lineage morphology target and
field-by-field parity criteria remain unchanged.

Texts shorter than 300,000 characters including spaces are valid inputs with explicit
representativeness limits. That length is a corpus-admission floor, not a guarantee of
quality; legal provenance and source identity require separate evidence. Source books,
private manuscripts and dictionary contents are not included in reports or uploaded.
Hashes can identify known works; share derived reports deliberately.

## Safety and reproducibility

The CLI bounds manuscripts to 32 MiB and dictionaries and comparison reports to 8 MiB
per file, rejects special files and symlinks, and uses a create-only atomic writer.
Operational errors do not echo private paths or source text. CSV neutralizes formula-like
**text** while preserving numeric cells; spreadsheet import/save behavior is not universally guaranteed.

```bash
python -m unittest discover -s tests -v
python -m pip wheel --no-deps . --wheel-dir dist
```

The Reader workflow runs the complete canonical suite, builds a full wheel and tests it
outside the checkout: actual manuscript analysis/comparison, HTML/JSON/CSV, historical
report, safe failures and deterministic source-free gallery/site. No analyzer stubs are
used in the private-comparison acceptance. Package, project and CLI versions must agree.
The full Python public API, morphology modules, benchmark data and corpus records remain
in place. No external package-registry release is performed by CI.

Site locks are persistent regular files whose kernel locks are released on process death.
Do not delete a lock file while a publisher could be using it. Legacy directory locks
from an interrupted older preview fail closed and are not automatically deleted.

## Documentation

[Reader installation and commands](docs/READER_PREVIEW.md) ·
[Local analysis and dictionaries](docs/LOCAL_ANALYSIS.md) ·
[Private comparison](docs/PRIVATE_COMPARISON.md) ·
[Frozen diagnostic methodology](docs/FROZEN_DIAGNOSTIC_REPORT.md) ·
[Five-work benchmark readiness](docs/BENCHMARK_READINESS.md) ·
[Canonical site and publication boundary](docs/FULL_WORK_SITE_REPORT.md) ·
[Roadmap and repository assessment](project/ROADMAP.md)

The detailed [Research and evidence index](RESEARCH_INDEX.md) retains project history,
corpus investigations and original reference links. EPUB/batch Workbench prototypes remain **unpublished** and require focused adoption.
The browser comparison is merged into master as a local-build capability;
public deployment remains unverified and separately gated. Code/data licensing and Pages activation retain separate gates (#284/#285).
