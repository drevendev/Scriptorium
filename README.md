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
- a versioned static-publication allow-list for future GitHub Pages rendering, with
  explicit source-text and admissibility safety flags;
- golden tests for text boundaries, dialogue spans, metric formulas, vocabulary windows,
  punctuation overlap, POS aggregation rules, publication safety and benchmark gate behavior.

The FantLab-shaped values are **inferred candidates**, not claimed reproduction.
See [`docs/TEXT_MODEL.md`](docs/TEXT_MODEL.md),
[`docs/DIALOGUE_MODEL.md`](docs/DIALOGUE_MODEL.md),
[`docs/VOCABULARY_MODEL.md`](docs/VOCABULARY_MODEL.md),
[`docs/POS_MODEL.md`](docs/POS_MODEL.md),
[`docs/METRIC_PROFILE.md`](docs/METRIC_PROFILE.md),
[`docs/BENCHMARKING.md`](docs/BENCHMARKING.md), and
[`docs/SITE_CONTRACT.md`](docs/SITE_CONTRACT.md).

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

### Public showcase

The repository includes derived metric slices for real public-domain literary sources
without storing the analyzed prose:

- [`showcase/anna-karenina-part1-ch1-opening.json`](showcase/anna-karenina-part1-ch1-opening.json)
  shows the first general/punctuation metrics on the opening four prose paragraphs of
  *Anna Karenina*, Part I, Chapter I.
- [`showcase/anna-karenina-part1-ch2-dialogue.json`](showcase/anna-karenina-part1-ch2-dialogue.json)
  shows the inferred dialogue profile on two dash-led dialogue paragraphs from Chapter II.

Both artifacts are bound to exact Russian Wikisource revisions and store provenance,
hashes and derived metrics only. They are intentionally marked **illustrative excerpts**,
not corpus entries and not FantLab parity evidence. Existing artifacts preserve the
metric profile under which they were generated; a future vocabulary/POS showcase must be
regenerated from a provenance-bound source selection rather than inventing new values
from hashes alone. Full-work showcase artifacts will follow as ingestion and source
freezing mature.

The future Pages UI has an explicit publication boundary rather than globbing every JSON
file in the repository. [`site/publication-manifest.json`](site/publication-manifest.json)
allow-lists public artifacts and freezes stable slugs plus source-text/admissibility
safety metadata under
[`scriptorium-publication-manifest-v1`](schemas/scriptorium-publication-manifest-v1.schema.json).
Pages is **not deployed yet**; generated HTML will be a disposable GitHub Actions artifact,
not a second committed source of truth. See [`docs/SITE_CONTRACT.md`](docs/SITE_CONTRACT.md).

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
stored with that reference.

## Methodology status

FantLab publicly describes sentence/dialogue metrics, vocabulary windows, POS
statistics and bigrams, punctuation/character features, and the weighted construction
of author profiles. It also says some corrective coefficients and implementation
know-how are unpublished. Scriptorium therefore distinguishes benchmarked
**reproduced** behavior from evidence-based **inferred** behavior and Scriptorium-only
**extensions**.

See [`docs/RESEARCH_EVIDENCE.md`](docs/RESEARCH_EVIDENCE.md) and
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
