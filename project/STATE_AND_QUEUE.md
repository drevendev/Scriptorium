# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 10
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-12T09:12:00Z
LAST_RESULT: Independent review of SCRIP-MORPH-001 found that PR #10 maps documentation-facing Cyrillic AOT POS labels rather than the Latin runtime constants exposed by pinned pylem 0.0.18; the current head must not merge.
LAST_VERIFIED_PROGRESS: Review of exact head dcf3dcfdf1deaf4be201c1e1b127ff7c7e34f423 verified SetUseNationalConstants(false) in pinned pylem and the pinned morph_dict 22-POS runtime inventory, including the lossy runtime `N` collision between noun and cardinal numeral. Review finding is recorded on PR #10.

## Current unit

```text
UNIT_ID:        SCRIP-MORPH-001
ISSUE:          #9
STATUS:         REPAIR_REQUIRED
BRANCH:         research/9-aot-pylem-contract
PR:             #10
REVIEWED_HEAD:  dcf3dcfdf1deaf4be201c1e1b127ff7c7e34f423
NEXT_ACTION:    Repair the contract around the actual pylem 0.0.18 runtime POS representation:
                enumerate all 22 Latin runtime POS values, classify the extra categories,
                and resolve or explicitly preserve the N noun/cardinal collision before
                requesting a fresh independent review.
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
- Rendered decimal text is not treated as proof of decimal precision. A known
  `display_places` value requires independent field/surface evidence; otherwise the
  metric remains `unresolved_precision`.
- The first parity-corpus seed has five candidate-eligible full novels: `Анна Каренина`,
  `Воскресение`, `Идиот`, `Братья Карамазовы` and `Бесы`. Candidate availability has not
  advanced M2 because every FantLab source-edition match remains unknown.
- PyPI still exposes pylem 0.0.18 as the selected compatibility candidate; the repository
  revision pins `morph_dict@4c5e9b6d048d1ba74e02988593b23fb0cbc87772`.
- Pinned pylem calls `SetUseNationalConstants(false)` after morphology load, therefore
  runtime POS/grammeme strings exposed through that holder use Latin constants rather
  than the Cyrillic documentation-facing constants.
- Pinned morph_dict defines 22 Russian POS runtime entries. The Latin runtime inventory
  includes `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT`, and `INFINITIVE` as distinct
  values in addition to the categories represented on the observed FantLab surface.
- The pinned runtime maps both Cyrillic noun `С` and cardinal numeral `ЧИСЛ` to Latin
  `N`. `LemmaInfo.part_of_speech` alone therefore cannot justify a direct noun/cardinal
  distinction; another proven discriminator is required or the distinction remains
  unresolved.

## Known risks / blockers

1. **Exact source edition risk.** FantLab publishes analysis values but not necessarily
   the exact full text bytes used. Parity requires finding works where the source
   edition can be matched or strongly established.
2. **Hidden-algorithm risk.** FantLab publicly acknowledges unpublished corrective
   coefficients/know-how. Keep reverse-engineering evidence-based; do not lower the M2
   gate without an explicit manifest amendment.
3. **Morphology runtime-contract mismatch.** PR #10 currently maps Cyrillic AOT labels,
   while pinned pylem exposes Latin runtime constants after `SetUseNationalConstants(false)`.
   The contract must be repaired before merge.
4. **Runtime POS collision.** Pinned morph_dict maps both noun and cardinal numeral to
   Latin `N`; `part_of_speech` alone loses this distinction. Do not invent a recovery
   heuristic without evidence from ancodes/grammemes or source-matched benchmarks.
5. **Morphology drift.** The pinned pylem dictionary/source has not been shown identical
   to FantLab's 2022 production morphology. Source-matched benchmarks must measure drift.
6. **Morphology ambiguity.** Pylem can expose multiple analyses; FantLab's homonym and
   prediction-selection policy is not public. No first-result/weight heuristic is accepted.
7. **Native-build verification pending.** pylem 0.0.18 has not yet been built in a
   verified network-enabled runtime. This remains `not_run`, not a package failure.
8. **Copyright risk.** Author.Today/fanfiction availability is not a license. Treat
   platform texts as candidates until work-specific rights permit analysis/publication.
9. **Scheduler serialization unverified.** Re-read refs/state before write and avoid
   same-run author+merge of substantial PRs.
10. **External mode controller unverified.** The user-authorized deterministic selection
    ladder is operative, but no independent EndlessZen controller/selection receipt
    mechanism has been bound and proven yet.
11. **Display/cache surface drift.** Summary and detailed FantLab surfaces may expose
    differently rounded or cached values. Benchmark expectations must name the exact
    source surface and capture display text; cross-surface joining is not parity evidence.
12. **Display precision unresolved.** FantLab may trim trailing zeroes and does not publish
    a general formatting/tie rule. Unknown precision remains unresolved rather than
    inferred from rendered text.
13. **Parity-corpus edition gap.** None of the five retained candidates has evidence
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
