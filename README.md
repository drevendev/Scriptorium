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
