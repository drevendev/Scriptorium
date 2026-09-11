# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 4
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-11T19:54:00Z
LAST_RESULT: SCRIP-REPRO-001 defined the FantLab metric surface and versioned field-by-field benchmark comparison contract; PR #6 is ready for independent review.
LAST_VERIFIED_PROGRESS: Issue #5 owns the contract; the JSON Schema parses and validates a representative not-run work488 comparison artifact under Draft 2020-12.

## Current unit

```text
UNIT_ID:        SCRIP-REPRO-001
ISSUE:          #5
STATUS:         REVIEW
BRANCH:         spec/5-fantlab-metric-contract
PR:             #6
NEXT_ACTION:    Independently review the metric contract and schema against issue #5,
                public FantLab evidence and the existing work488 fixture; merge only if
                identifiers, unresolved edges and parity-gate semantics remain honest.
```

## Current milestone gate

M0 is closed. M1 closes when the benchmark harness can compare expected vs actual
FantLab-visible deterministic metrics field-by-field while preserving text and
configuration provenance.

## Queue

Ordered highest first among unblocked work after the current review closes.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-CORPUS-001 | research | Candidate list of legally usable >=300k works that also have FantLab analysis, with source-edition confidence | M0 |
| P0 | SCRIP-MORPH-001 | research/spike | Reproducible AOT/pylem environment and mapping from AOT tags to FantLab POS buckets | M0 |
| P1 | SCRIP-TEXT-001 | implementation | Deterministic normalization/tokenization/sentence model with golden tests | SCRIP-REPRO-001 |
| P1 | SCRIP-METRIC-001 | implementation | Character/word/sentence/punctuation metrics and JSON schema | SCRIP-TEXT-001 |
| P1 | SCRIP-REPRO-002 | implementation | CLI benchmark harness reporting expected/actual/delta and provenance | SCRIP-METRIC-001 |
| P1 | SCRIP-TEXT-002 | implementation | Dialogue segmentation and author-text-in-dialogue metrics | SCRIP-TEXT-001 |
| P1 | SCRIP-METRIC-002 | implementation | Vocabulary/rolling-window metrics | SCRIP-TEXT-001 |
| P1 | SCRIP-MORPH-002 | implementation | POS distributions, bigrams and sentence-position metrics | SCRIP-MORPH-001, SCRIP-TEXT-001 |
| P2 | SCRIP-SITE-001 | architecture | Static artifact/site contract for GitHub Pages | M1 underway |

## Evidence already established

- FantLab article `https://fantlab.ru/article374` states the analyzer was developed in
  2007-2008 and produces more than 1,000 statistical characteristics.
- Publicly described families include sentence/dialogue measures, unique/dictionary
  vocabulary and 3k/10k/100k windows, POS frequencies/bigrams/positions, punctuation,
  character bigrams, inter-word character features and later distinguishing-word
  frequencies.
- A concrete 18 September 2022 work page (`work12625/lp`) exposes the first-wave scalar
  labels, 17 displayed POS buckets, POS bigrams, POS-by-sentence-position and 14
  punctuation patterns used by `fantlab-2022-v1`.
- The methodology article names additional POS labels not observed as separate buckets
  on that 2022 page; their mapping is explicitly deferred to SCRIP-MORPH-001.
- FantLab says corrective coefficients and some implementation details remain
  unpublished. Exact parity must therefore be demonstrated, not inferred.
- FantLab's 2022 `Шутиха` page is captured as the first numeric reference in
  `benchmarks/fantlab/work488.json`.
- The public `Шутиха` summary currently displays an approximate page count that differs
  from the captured detailed-analysis reference, reinforcing the requirement to bind
  every expected value to its exact FantLab source surface.
- The maintained AOT repository is LGPL and `pylem` is an MIT-licensed Python wrapper
  around the historical AOT C++ morphology lineage. This makes `pylem` the first
  compatibility candidate, not an already-proven match.

## Known risks / blockers

1. **Exact source edition risk.** FantLab publishes analysis values but not necessarily
   the exact full text bytes used. Parity requires finding works where the source
   edition can be matched or strongly established.
2. **Hidden-algorithm risk.** FantLab publicly acknowledges unpublished corrective
   coefficients/know-how. Keep reverse-engineering evidence-based; do not lower the M2
   gate without an explicit manifest amendment.
3. **Morphology drift.** Current AOT dictionaries/wrappers may not be byte-for-byte the
   same dictionary/version used by FantLab in 2022. Pin versions and measure drift.
4. **Copyright risk.** Author.Today/fanfiction availability is not a license. Treat
   platform texts as candidates until work-specific rights permit analysis/publication.
5. **Scheduler serialization unverified.** Re-read refs/state before write and avoid
   same-run author+merge of substantial PRs.
6. **External mode controller unverified.** The user-authorized deterministic selection
   ladder is operative, but no independent EndlessZen controller/selection receipt
   mechanism has been bound and proven yet.
7. **Display/cache surface drift.** Summary and detailed FantLab surfaces may expose
   differently rounded or cached values. Benchmark expectations must name the exact
   source surface and capture display text; cross-surface joining is not parity evidence.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect open PR checks/comments relevant to that unit;
3. otherwise choose the first unblocked queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file in the same semantic change.

Do not create parallel units merely because an hourly wake occurred.
