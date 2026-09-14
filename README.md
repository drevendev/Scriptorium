# Scriptorium

Scriptorium is an open-source toolkit for quantitative analysis of literary text.

The first milestone is a reproducible implementation of the public parts of the
FantLab linguistic analyzer, benchmarked field-by-field against published FantLab
results. Later milestones add author-voice profiles, profile comparison, richer
literary metrics, book/tag profiles, corpus exploration, and a GitHub Pages browser.

The project treats source provenance as part of the result. Calibration texts must be
legally usable and at least 300,000 characters including spaces; copyrighted text is
not committed merely because it is accessible online. Shorter texts and excerpts are
still valid analyzer inputs, but their results carry representativeness warnings.

## What works today

Scriptorium now has a standard-library-only deterministic analysis core:

- versioned CRLF/CR → LF and Unicode NFC normalization;
- deterministic word candidates and sentence spans with normalized-text offsets;
- explicit dash-led dialogue paragraphs and candidate author-remark spans;
- first-wave character, word, mean word/sentence length, dialogue and punctuation metrics;
- a versioned punctuation-v2 policy that does not double-count ASCII hyphens retained
  inside current word tokens as dash punctuation, while keeping the rule explicitly
  inferred rather than claiming FantLab parity;
- dictionary-free unique-vocabulary counting plus explicit external-dictionary active
  vocabulary and UASZ-3000/10000/100000 candidates;
- immutable dictionary dependency identity using profile + normalized lexeme-set SHA-256;
- a provider-neutral `scriptorium-pos-v1` aggregation layer for defined/undefined POS,
  the 17 displayed FantLab buckets, a complete 17×17 POS-bigram matrix, and positions
  1..20 while preserving unresolved pylem categories and homonyms;
- versioned JSON artifacts/schemas with explicit `inferred` vs `extension` status;
- a local-text FantLab benchmark CLI that emits expected/actual/delta plus source hashes
  and refuses to turn incomplete source provenance, an unproven dictionary, or unknown
  decimal precision into parity;
- source-free exact-revision replay for the frozen 239-chapter Russian Wikisource
  *Anna Karenina* candidate, with title/timestamp/MediaWiki-SHA-1 and composite-digest
  verification before a full-work diagnostic can run;
- source-free exact-revision replay for the frozen 129-chapter Russian Wikisource
  *Resurrection* candidate, with a versioned source-specific extraction contract for its
  heterogeneous Wikisource page shapes and the same fail-closed source-match boundary;
- a versioned static-publication allow-list plus a deterministic, fail-closed static
  renderer for derived/public work-showcase and provenance-only pages;
- golden tests for text boundaries, dialogue spans, metric formulas, vocabulary windows,
  punctuation overlap, POS aggregation rules, source replay, publication safety and
  benchmark gate behavior.

The FantLab-shaped values are **inferred candidates**, not claimed reproduction.
See [`docs/TEXT_MODEL.md`](docs/TEXT_MODEL.md),
[`docs/DIALOGUE_MODEL.md`](docs/DIALOGUE_MODEL.md),
[`docs/VOCABULARY_MODEL.md`](docs/VOCABULARY_MODEL.md),
[`docs/POS_MODEL.md`](docs/POS_MODEL.md),
[`docs/METRIC_PROFILE.md`](docs/METRIC_PROFILE.md),
[`docs/BENCHMARKING.md`](docs/BENCHMARKING.md),
[`docs/SITE_CONTRACT.md`](docs/SITE_CONTRACT.md), and
[`docs/SITE_RENDERER.md`](docs/SITE_RENDERER.md).

The POS artifact deliberately accepts an externally produced pylem-style runtime
candidate matrix rather than pretending native pylem execution is already verified.
Runtime `N` remains unresolved because pinned pylem collapses noun and cardinal to the
same public POS string; cross-bucket homonyms and extra AOT categories are not guessed
into a bucket. See [`docs/AOT_PYLEM_COMPATIBILITY.md`](docs/AOT_PYLEM_COMPATIBILITY.md)
and [`docs/POS_MODEL.md`](docs/POS_MODEL.md).

### Benchmark a local text

```bash
python -m scriptorium.benchmark \
  --reference benchmarks/fantlab/work488.json \
  --text /path/to/local-text.txt \
  --scriptorium-revision <git-sha> \
  --edition-match unknown \
  --output comparison.json
```

An optional external dictionary can enable the dictionary-dependent vocabulary actuals:

```bash
  --dictionary /path/to/dictionary.txt \
  --dictionary-profile my-dictionary-v1
```

Supplying a dictionary makes that analysis reproducible, not FantLab-compatible. Until
FantLab's production dictionary identity/version is established, dictionary-dependent
benchmark rows remain diagnostic `unresolved` results even when their numbers happen to
match.

The harness never fetches or commits the local text. `Шутиха` currently has no
source-matched legally usable full text in the project, so this reference remains a
diagnostic target rather than parity evidence. The harness currently maps 28 implemented
FantLab fields: four general, four dialogue, six vocabulary and fourteen punctuation
fields. POS aggregation now has its own versioned artifact, but it is not yet wired into
the benchmark CLI because native/provider execution provenance is not established.
Decimal fields remain unresolved until FantLab display precision is independently
established. See [`docs/BENCHMARKING.md`](docs/BENCHMARKING.md).

The repository also contains a full-work **diagnostic-only** comparison for *Anna
Karenina*. [`benchmarks/fantlab/work270306.json`](benchmarks/fantlab/work270306.json)
records FantLab's public 19 September 2022 values, while
[`benchmarks/fantlab/work270306-wikisource-diagnostic.json`](benchmarks/fantlab/work270306-wikisource-diagnostic.json)
records expected/actual/delta evidence from a replay of the 239 frozen public-domain
Wikisource revisions. The replayed source is bound to SHA-256
`1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; novel prose is
not committed or uploaded. FantLab does not disclose the analyzer-input edition or
bytes, so every result remains source-unmatched diagnostic evidence and M2 parity stays
0/5.

A second frozen public-domain candidate is now available for *Resurrection*.
[`corpus/candidates/source-edition-traces/tolstoy-resurrection-ru.json`](corpus/candidates/source-edition-traces/tolstoy-resurrection-ru.json)
records its provenance and fail-closed admissibility boundary, while the compact
[`tolstoy-resurrection-ru.revisions.json`](corpus/candidates/source-edition-traces/tolstoy-resurrection-ru.revisions.json)
pins all **129** chapter revision IDs, timestamps and MediaWiki SHA-1 identities without
storing source prose. Exact replay reconstructs a **890,835-character** composite bound
to raw and `scriptorium-text-v1` normalized SHA-256
`2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`.
FantLab displays 881,244 characters for its 2022 analysis, but does not disclose the
analyzer-input bytes or edition; this candidate is therefore eligible only for
**diagnostic-only** comparison and does not move the 0/5 source-matched reproduction gate.

A source-free [word/dash policy sensitivity artifact](benchmarks/fantlab/work270306-policy-sensitivity.json)
records the investigation that led to the punctuation boundary without turning the
unmatched work into a tuning target. It showed that excluding numeric-only tokens removes
only 17 of the +16,083 word difference, and that 1,611 ASCII hyphens occur inside current
word tokens. Historical punctuation-v1 counted those glyphs as dash events too. The
current `scriptorium-punctuation-v2` candidate removes that double role: ASCII hyphens
retained inside `scriptorium-text-v1` word tokens are lexical connectors for punctuation
purposes and are not also dash events. The historical artifact remains v1 evidence rather
than being silently rewritten.

This still does **not** establish FantLab's hyphen rule. The public methodology only says
punctuation frequencies are measured and the work surface labels its `-` row as `тире`;
FantLab does not publish the classifier. Even the historical sensitivity result after
excluding all token-internal ASCII hyphens remained about +14.913 dash events per 1000
words above the source-unmatched FantLab result. Punctuation-v2 is therefore an internal
consistency improvement under a new profile, not a parity promotion.

### Public showcase

The repository includes source-free public slices for real public-domain literary
sources:

- [`showcase/anna-karenina-part1-ch1-opening.json`](showcase/anna-karenina-part1-ch1-opening.json)
  shows the first general/punctuation metrics on the opening four prose paragraphs of
  *Anna Karenina*, Part I, Chapter I.
- [`showcase/anna-karenina-part1-ch2-dialogue.json`](showcase/anna-karenina-part1-ch2-dialogue.json)
  shows the inferred dialogue profile on two dash-led dialogue paragraphs from Chapter II.
- [`public-artifacts/tolstoy-resurrection-ru-provenance.json`](public-artifacts/tolstoy-resurrection-ru-provenance.json)
  exposes the full frozen *Resurrection* source identity: 129 pinned revisions,
  extraction/composition profiles, immutable counts and SHA-256 identities, legal/source
  provenance, and the explicit `unknown` FantLab source-edition boundary. It contains no
  novel prose and makes no parity claim.

The Anna Karenina metric artifacts are bound to exact Russian Wikisource revisions and
store provenance, hashes and derived metrics only. They are intentionally marked
**illustrative excerpts**, not corpus entries and not FantLab parity evidence. Existing
artifacts preserve the metric profile under which they were generated; a future
vocabulary/POS showcase must be regenerated from a provenance-bound source selection
rather than inventing new values from hashes alone. The full-work Anna Karenina diagnostic
is likewise source-free and inspectable, but it is not published as a Pages work view
because its benchmark rendering contract has not yet been defined. The *Resurrection*
Pages slice is deliberately provenance-first: it demonstrates a reproducibly frozen
>=300k public-domain candidate while keeping source-match and M2 parity fail-closed.

The publication boundary is explicit rather than directory-based.
[`site/publication-manifest.json`](site/publication-manifest.json) allow-lists public
artifacts and freezes stable slugs plus source-text/admissibility safety metadata under
[`scriptorium-publication-manifest-v1`](schemas/scriptorium-publication-manifest-v1.schema.json).
The static renderer consumes only that manifest and re-validates canonical evidence
before writing pages:

```bash
python -m scriptorium.site_renderer --output build/site
```

Generated pages include a root index, stable `/works/<slug>/` views, derived metric or
frozen-provenance evidence labels and selected provenance metadata. Artifact-controlled
text is HTML-escaped, provenance links must be HTTP(S), and source selection prose is not
copied into the output. The renderer validates the whole build before replacing the
disposable output tree and emits `build.json` with exact input digests for reproducibility.
See [`docs/SITE_RENDERER.md`](docs/SITE_RENDERER.md).

The reviewed GitHub Actions Pages pipeline now runs tests, builds the canonical static
site twice, requires a byte-identical rebuild and uploads only the disposable generated
site tree on relevant pull requests and `master` changes. Publication-source provenance
changes also trigger the build, preventing a source trace from drifting away from a
published derived artifact without CI noticing. **Live GitHub Pages deployment is still
disabled**: deployment requires the explicit repository variable
`SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true`, and repository Pages activation/settings remain
a separate owner/admin effect. See [`docs/SITE_CONTRACT.md`](docs/SITE_CONTRACT.md).

## Project state

This is an hourly autonomous project operated with an EndlessZen-derived work cycle.
The durable project contract lives in:

- [`project/PROJECT_MANIFEST.md`](project/PROJECT_MANIFEST.md)
- [`project/STATE_AND_QUEUE.md`](project/STATE_AND_QUEUE.md)
- [`project/CHANGELOG.md`](project/CHANGELOG.md)
- [`AGENTS.md`](AGENTS.md)

The first public numeric reference is FantLab's analysis of Henry Lion Oldie's
`Шутиха`; its published values are recorded in
[`benchmarks/fantlab/work488.json`](benchmarks/fantlab/work488.json). No novel text is
stored with that reference. The frozen *Anna Karenina* diagnostic adds the first
full-work expected/actual comparison without promoting a source-unmatched candidate to
parity; frozen *Resurrection* adds a second reproducible full-work source identity ready
for the same diagnostic-only discipline.

## Methodology status

FantLab publicly describes sentence/dialogue metrics, vocabulary windows, POS
statistics and bigrams, punctuation/character features, and the weighted construction
of author profiles. It also says some corrective coefficients and implementation
know-how are unpublished. Scriptorium therefore distinguishes benchmarked
**reproduced** behavior from evidence-based **inferred** behavior and Scriptorium-only
**extensions**.

See [`docs/RESEARCH_EVIDENCE.md`](docs/RESEARCH_EVIDENCE.md) and
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
