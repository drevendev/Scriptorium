# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 1
PHASE: M0 — Recoverable project
LAST_COMMITTED_RUN_AT: 2026-09-11T18:49:00Z
LAST_RESULT: Bootstrap branch prepared for review; project setup is not yet merged.
LAST_VERIFIED_PROGRESS: Issue #1 defines the setup unit and FantLab/AOT evidence was
reviewed before the branch was prepared.

## Current unit

```text
UNIT_ID:        SCRIP-SETUP-001
ISSUE:          #1
STATUS:         REVIEW
BRANCH:         setup/1-bootstrap
NEXT_ACTION:    Review the bootstrap PR from repository state, fix any contradictions,
                then merge if it satisfies issue #1.
```

## Current milestone gate

M0 closes when the bootstrap project contract is merged and a fresh worker can select
work from this file without relying on chat history.

## Queue

Ordered highest first among unblocked work after M0.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-REPRO-001 | research/spec | Metric contract for FantLab-visible raw statistics and benchmark comparison schema | M0 |
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
- The article says author means and standard deviations are weighted by work word
  counts and describes feature weight as between-author spread relative to average
  within-author spread; features above 0.7 were reported as useful for recognition.
- The same article explicitly says corrective coefficients and some implementation
  details remain unpublished. Exact parity must therefore be demonstrated, not
  inferred.
- FantLab's 2022 `Шутиха` page is captured as the first numeric reference in
  `benchmarks/fantlab/work488.json`.
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

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect open PR checks/comments relevant to that unit;
3. otherwise choose the first unblocked queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file in the same semantic change.

Do not create parallel units merely because an hourly wake occurred.
