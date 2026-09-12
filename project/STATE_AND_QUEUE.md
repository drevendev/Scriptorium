# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 14
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-12T12:50:00Z
LAST_RESULT: SCRIP-TEXT-001 repaired the testing-policy drift found in independent review; PR #15 remains in REVIEW for fresh exact-head judgement.
LAST_VERIFIED_PROGRESS: Independent review of pre-repair head 45060bccdf9280a07661625346ef2d134493b3a3 confirmed 11/11 golden tests and coherent inferred text behavior. The repair changes only architecture/control documentation: standard-library unittest is now the initial unit/golden/benchmark runner, with pytest deferred until a concrete need justifies it.

## Current unit

```text
UNIT_ID:        SCRIP-TEXT-001
ISSUE:          #11
STATUS:         REVIEW
BRANCH:         feature/11-text-model
PR:             #15
NEXT_ACTION:    Independently review the repaired exact PR #15 head, confirm the code/test
                blobs are unchanged from the passing review evidence, inspect the testing
                policy repair, and merge only if no new blocker remains.
```

## Current milestone gate

M0 is closed. M1 closes when the benchmark harness can compare expected vs actual
FantLab-visible deterministic metrics field-by-field while preserving text and
configuration provenance.

## Queue

Ordered highest first among unblocked work after the current review closes.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
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
- `pylem/__init__.py` parses the leading `morphInfo` token into
  `LemmaInfo.part_of_speech`; this is the runtime adapter surface described by the
  compatibility contract.
- Pinned morph_dict defines 22 Russian source POS slots but only 21 unique Latin runtime
  strings. Fifteen runtime strings map unambiguously to one observed FantLab bucket.
- Both noun `С` and cardinal numeral `ЧИСЛ` render as runtime `N`; the public pylem Python
  result does not expose the original source POS enum/ancode, so this distinction remains
  unresolved rather than guessed.
- `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT` and `INFINITIVE` are distinct pinned
  runtime POS values with no standalone bucket on the observed 2022 FantLab surface.
  Their folding behavior remains unresolved.
- `scriptorium-text-v1` is the first executable text profile. It normalizes line endings
  and Unicode NFC, emits deterministic word/sentence candidate spans with offsets into
  normalized text, and is explicitly classified as inferred rather than reproduced.
- Independent review of the implementation content passed 11/11 standard-library golden
  tests under Python 3.13.5. The subsequent repair changed only architecture/control
  documentation, not the tested text-model or test blobs.
- The architecture now names standard-library `unittest` as the initial unit, golden and
  benchmark contract runner. `pytest` is optional future infrastructure, not an implicit
  dependency or a contradictory bootstrap requirement.

## Known risks / blockers

1. **Exact source edition risk.** FantLab publishes analysis values but not necessarily
   the exact full text bytes used. Parity requires finding works where the source
   edition can be matched or strongly established.
2. **Hidden-algorithm risk.** FantLab publicly acknowledges unpublished corrective
   coefficients/know-how. Keep reverse-engineering evidence-based; do not lower the M2
   gate without an explicit manifest amendment.
3. **Text-boundary inference.** FantLab's exact normalization, tokenization, abbreviation
   and sentence-boundary rules are not public. `scriptorium-text-v1` is a deterministic
   candidate only; benchmark deltas must drive any compatibility revisions.
4. **Runtime POS collision.** Pinned pylem renders both noun and cardinal numeral as
   Latin `N`. `LemmaInfo.part_of_speech` cannot recover the distinction; an explicitly
   exposed source POS discriminator plus benchmark validation is required before these
   two FantLab buckets can be produced compatibly.
5. **Extra-category folding unresolved.** `POSL`, `COLLOC`, `ADJ_SHORT`,
   `PARTICIPLE_SHORT` and `INFINITIVE` exist separately in the pinned runtime, while the
   observed FantLab 2022 surface has no matching standalone buckets.
6. **Morphology drift.** The pinned pylem dictionary/source has not been shown identical
   to FantLab's 2022 production morphology. Source-matched benchmarks must measure drift.
7. **Morphology ambiguity.** Pylem can expose multiple analyses; FantLab's homonym and
   prediction-selection policy is not public. No first-result/weight heuristic is accepted.
8. **Native-build verification pending.** pylem 0.0.18 has not yet been built in a
   verified network-enabled runtime. This remains `not_run`, not a package failure.
9. **Copyright risk.** Author.Today/fanfiction availability is not a license. Treat
   platform texts as candidates until work-specific rights permit analysis/publication.
10. **Scheduler serialization unverified.** Re-read refs/state before write and avoid
    same-run author+merge of substantial PRs.
11. **External mode controller unverified.** The user-authorized deterministic selection
    ladder is operative, but no independent EndlessZen controller/selection receipt
    mechanism has been bound and proven yet.
12. **Display/cache surface drift.** Summary and detailed FantLab surfaces may expose
    differently rounded or cached values. Benchmark expectations must name the exact
    source surface and capture display text; cross-surface joining is not parity evidence.
13. **Display precision unresolved.** FantLab may trim trailing zeroes and does not publish
    a general formatting/tie rule. Unknown precision remains unresolved rather than
    inferred from rendered text.
14. **Parity-corpus edition gap.** None of the five retained candidates has evidence
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
