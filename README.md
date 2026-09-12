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
- first-wave character, word, mean word/sentence length and punctuation metrics;
- a versioned JSON artifact/schema with explicit `inferred` vs `extension` status;
- a local-text FantLab benchmark CLI that emits expected/actual/delta plus source hashes
  and refuses to turn incomplete provenance or unknown decimal precision into parity;
- golden tests for text boundaries, metric formulas, punctuation overlap and benchmark
  gate behavior.

The FantLab-shaped values are **inferred candidates**, not claimed reproduction.
See [`docs/TEXT_MODEL.md`](docs/TEXT_MODEL.md),
[`docs/METRIC_PROFILE.md`](docs/METRIC_PROFILE.md), and
[`docs/BENCHMARKING.md`](docs/BENCHMARKING.md).

### Benchmark a local text

```bash
python -m scriptorium.benchmark \
  --reference benchmarks/fantlab/work488.json \
  --text /path/to/local-text.txt \
  --scriptorium-revision <git-sha> \
  --edition-match unknown \
  --output comparison.json
```

The harness never fetches or commits the local text. `Шутиха` currently has no
source-matched legally usable full text in the project, so this reference remains a
diagnostic target rather than parity evidence. See
[`docs/BENCHMARKING.md`](docs/BENCHMARKING.md) for the provenance and comparison rules.

### First public showcase

The repository includes a derived metric slice for a real public-domain literary
source: the opening four prose paragraphs of Tolstoy's *Anna Karenina*, Part I,
Chapter I, bound to an exact Russian Wikisource revision.

[`showcase/anna-karenina-part1-ch1-opening.json`](showcase/anna-karenina-part1-ch1-opening.json)
contains source provenance, hashes and the derived metric artifact, but no source prose.
It is intentionally marked as a **short illustrative excerpt**, not a corpus entry and
not FantLab parity evidence. Full-work showcase artifacts will follow as ingestion and
source freezing mature.

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
