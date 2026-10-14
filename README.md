# Scriptorium · Reader preview

**Understand the language of a text without uploading the manuscript.**
Scriptorium measures vocabulary, sentence length, dialogue and punctuation, then produces
readable offline reports and reproducible data. This integrated **0.2.0a1 preview** brings
the reader site and the local analyzer into the canonical repository.

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

## Open a real literary result

The repository already contains a source-free, historical full-work diagnostic for
**Anna Karenina**. It has **28 expected/actual/delta rows: 23 numeric results and five
unavailable values**. No novel download is needed:

```bash
scriptorium diagnostic benchmarks/fantlab/work270306-wikisource-diagnostic.json \
  --title "Anna Karenina — full-work diagnostic" --output anna-report.html
scriptorium site --repo-root . --output build/site
```

Open `anna-report.html` or `build/site/index.html`. The canonical site retains its four
earlier evidence pages and adds the full-work report with a working homepage action.
**A successful local build is not a live GitHub Pages deployment.** The existing Pages
activation interlock is unchanged; this preview does not enable publishing by itself.

## What the results mean

FantLab-shaped metrics are **inferred compatibility candidates**, not demonstrated
parity. Scriptorium-only features are **extensions**. The historical Anna diagnostic
has no established identity match to FantLab's input text. **M2 remains 0/5**; none of
M1–M5 is declared complete by this release. The AOT-lineage morphology target and
field-by-field parity criteria remain unchanged.

Texts shorter than 300,000 characters including spaces are valid inputs with explicit
representativeness limits. That length is a corpus-admission floor, not a guarantee of
quality; legal provenance and source identity require separate evidence. Source books,
private manuscripts and dictionary contents are not included in reports or uploaded.
Hashes can identify known works; share derived reports deliberately.

## Safety and reproducibility

The reader CLI bounds manuscripts to 32 MiB and dictionaries to 8 MiB, rejects special
files and symlinks, and uses a create-only atomic writer. Operational errors do not echo
private paths or source text. CSV neutralizes formula-like **text** while preserving
numeric cells; spreadsheet import/save behavior is not universally guaranteed.

```bash
python -m unittest discover -s tests -v
python -m pip wheel --no-deps . --wheel-dir dist
```

The Reader package workflow tests the installed wheel outside the checkout; the existing
Pages workflow runs the complete canonical suite and a byte-identical site rebuild.
The full Python public API, morphology modules, benchmark data and corpus records remain
in place. No external package-registry release is performed by CI.

## Documentation

[Reader installation and commands](docs/READER_PREVIEW.md) ·
[Local analysis and dictionaries](docs/LOCAL_ANALYSIS.md) ·
[Frozen diagnostic methodology](docs/FROZEN_DIAGNOSTIC_REPORT.md) ·
[Canonical site and publication boundary](docs/FULL_WORK_SITE_REPORT.md)

The previous detailed README is preserved as [Research and evidence index](RESEARCH_INDEX.md).
It retains the project history, corpus investigations and original reference links.
The remaining unpublished EPUB/batch Workbench prototypes are **not** advertised as
features of this integrated preview; they need focused adoption and repository tests.
