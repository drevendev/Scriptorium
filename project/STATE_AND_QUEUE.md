# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 9
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-11T23:59:30Z
LAST_RESULT: SCRIP-MORPH-001 pinned the first AOT/pylem compatibility candidate and defined the machine-readable AOT POS to FantLab bucket mapping; PR #10 is ready for independent review.
LAST_VERIFIED_PROGRESS: pylem 0.0.18 package/source/submodule identifiers and AOT POS documentation were source-verified; the mapping JSON parses with 17 direct buckets while ambiguity, infinitives and short-form handling remain explicit unresolved work. Native build was not run because the execution container could not resolve external package hosts.

## Current unit

```text
UNIT_ID:        SCRIP-MORPH-001
ISSUE:          #9
STATUS:         REVIEW
BRANCH:         research/9-aot-pylem-contract
PR:             #10
NEXT_ACTION:    Independently review the pinned pylem/AOT source identities, the 17 direct
                POS mappings, unresolved overrides and build-verification limitation;
                merge only if no inferred behavior is mislabeled as reproduced.
```

## Current milestone gate

M0 is closed. M1 closes when the benchmark harness can compare expected vs actual
FantLab-visible deterministic metrics field-by-field while preserving text and
configuration provenance.

## Queue

Ordered highest first among unblocked work after the current review closes.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
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
  on that 2022 page; their mapping is not guessed.
- FantLab says corrective coefficients and some implementation details remain
  unpublished. Exact parity must therefore be demonstrated, not inferred.
- FantLab's 2022 `Шутиха` page is captured as the first numeric reference in
  `benchmarks/fantlab/work488.json`.
- The public `Шутиха` summary currently displays an approximate page count that differs
  from the captured detailed-analysis reference, reinforcing the requirement to bind
  every expected value to its exact FantLab source surface.
- Rendered decimal text is not treated as proof of decimal precision. A known
  `display_places` value requires independent field/surface evidence; otherwise the
  metric remains `unresolved_precision`.
- The first parity-corpus seed has five candidate-eligible full novels: `Анна Каренина`,
  `Воскресение`, `Идиот`, `Братья Карамазовы` and `Бесы`. Their FantLab analyses report
  881,244–1,807,107 characters and their retained source pages carry explicit
  public-domain notices.
- Candidate availability has not advanced the M2 gate: all five FantLab source-edition
  matches remain unknown, so source-matched parity progress is still 0/5.
- PyPI still exposes pylem 0.0.18 (2022-01-16) as the latest release, with sdist SHA-256
  `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515`.
- `sokirko74/pylem@68d62ce5452b6b80f2c2ef3345b4160c09e24bdf` declares 0.0.18 and pins
  `morph_dict@4c5e9b6d048d1ba74e02988593b23fb0cbc87772` plus
  `pybind11@cd176ceeff94ec184abde945ef0867ebe9fb3664`; PyPI itself does not encode a Git
  commit, so this is a repository-version match rather than cryptographic sdist-to-Git proof.
- Pylem's release source requires CMake 3.16 and C++17 and exposes AOT POS through
  `LemmaInfo.part_of_speech`; `MorphanHolder.lemmatize()` may yield multiple analyses.
- AOT's pinned documentation exposes 18 Russian POS labels. Seventeen map directly by
  public label semantics to the observed FantLab buckets. `ИНФИНИТИВ`, `П + кр`,
  `ПРИЧАСТИЕ + кр`, postpositions and phrasal verbs remain unresolved.

## Known risks / blockers

1. **Exact source edition risk.** FantLab publishes analysis values but not necessarily
   the exact full text bytes used. Parity requires finding works where the source
   edition can be matched or strongly established.
2. **Hidden-algorithm risk.** FantLab publicly acknowledges unpublished corrective
   coefficients/know-how. Keep reverse-engineering evidence-based; do not lower the M2
   gate without an explicit manifest amendment.
3. **Morphology drift.** The pinned pylem dictionary/source has not been shown identical
   to FantLab's 2022 production morphology. Source-matched benchmarks must measure drift.
4. **Morphology ambiguity.** Pylem can expose multiple analyses; FantLab's homonym and
   prediction-selection policy is not public. No first-result/weight heuristic is accepted.
5. **Native-build verification pending.** The current execution container cannot resolve
   external package hosts, so pylem 0.0.18 was not built locally in SCRIP-MORPH-001.
   Re-run the pinned build in a network-enabled CI/runtime before production adapter work.
6. **Copyright risk.** Author.Today/fanfiction availability is not a license. Treat
   platform texts as candidates until work-specific rights permit analysis/publication.
7. **Scheduler serialization unverified.** Re-read refs/state before write and avoid
   same-run author+merge of substantial PRs.
8. **External mode controller unverified.** The user-authorized deterministic selection
   ladder is operative, but no independent EndlessZen controller/selection receipt
   mechanism has been bound and proven yet.
9. **Display/cache surface drift.** Summary and detailed FantLab surfaces may expose
   differently rounded or cached values. Benchmark expectations must name the exact
   source surface and capture display text; cross-surface joining is not parity evidence.
10. **Display precision unresolved.** FantLab may trim trailing zeroes and does not publish
    a general formatting/tie rule. Unknown precision remains unresolved rather than
    inferred from rendered text.
11. **Parity-corpus edition gap.** The seed catalog proves that long, legally usable works
    with FantLab analyses exist, but none of the five retained candidates has evidence
    tying its source transcription to FantLab's exact analyzed edition/bytes. M2 remains
    blocked until that evidence is found or the user explicitly changes the gate.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect open PR checks/comments relevant to that unit;
3. otherwise choose the first unblocked queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file in the same semantic change.

Do not create parallel units merely because an hourly wake occurred.
