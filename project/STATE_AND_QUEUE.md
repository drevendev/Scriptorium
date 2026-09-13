# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 26
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-13T01:59:30Z
LAST_RESULT: SCRIP-METRIC-002 passed independent repaired-head review and PR #23 was squash-merged; issue #22 is complete.
LAST_VERIFIED_PROGRESS: Exact PR #23 head 4468f9e64da7fcdfc2ef8ad2a6d50bb803cbc111 was reconstructed from published GitHub blobs and reviewed independently. The full standard-library suite passed 46/46 tests under Python 3.13.5. Draft 2020-12 validation accepted the v3 schema and generated artifacts both without a vocabulary dictionary and with an explicit profile/SHA-256/lexeme-count dependency. The Unicode NFC + casefold repair, rolling-window behavior, source-provenance gate and dictionary parity-admission barrier were rechecked. Hosted statuses/workflows remain absent, so CI is not configured rather than green. PR #23 merged as ab8cd21c505bf3c229648be491f31d0a8a5f30fd. M2 remains 0/5 source-matched works.

## Current unit

```text
UNIT_ID:        SCRIP-METRIC-002
ISSUE:          #22
STATUS:         DONE
PR:             #23
MERGED_COMMIT:  ab8cd21c505bf3c229648be491f31d0a8a5f30fd
NEXT_ACTION:    Select the highest-priority unblocked queue unit after confirming its
                dependency state; SCRIP-MORPH-002 is the first listed candidate.
```

## Current milestone gate

M0 is closed. M1 closes when the benchmark harness can compare expected vs actual
FantLab-visible deterministic metrics field-by-field while preserving text and
configuration provenance. General, dialogue, vocabulary and punctuation families are
now executable inferred candidates; the remaining queued deterministic family is POS.

## Queue

Ordered highest first among unblocked work.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-002 | implementation | POS distributions, bigrams and sentence-position metrics | SCRIP-MORPH-001, SCRIP-TEXT-001 |
| P2 | SCRIP-SITE-001 | architecture | Static artifact/site contract for GitHub Pages | M1 underway |

## Evidence already established

### FantLab / benchmark surface

- FantLab's public methodology describes sentence/dialogue measures, unique/dictionary
  vocabulary and 3k/10k/100k windows, POS frequencies/bigrams/positions, punctuation,
  character bigrams, inter-word character features and later distinguishing-word
  frequencies. Corrective coefficients and some implementation details are unpublished;
  resemblance is never treated as parity.
- `fantlab-2022-v1` is the frozen compatibility contract. The first captured numeric
  reference is the 19 September 2022 `Шутиха` analysis in
  `benchmarks/fantlab/work488.json`.
- `scriptorium-benchmark-v1` records raw/normalized hashes, edition/source/legal
  provenance, analyzer configuration, expected/actual values and raw deltas.
- Exact integer comparisons can become `pass`/`fail` only with `edition_match=exact`,
  non-empty edition identity, source reference, legal basis and harness-computed raw
  SHA-256. Otherwise numeric resemblance remains `unresolved`.
- Decimal/rate comparisons remain `unresolved_precision` until FantLab display precision
  and tie-breaking are independently established. Captured JSON numeric lexemes are
  retained as display evidence without inferring precision from visible digits.
- The first parity-corpus seed contains five candidate-eligible full novels, but none has
  evidence tying the public transcription to FantLab's exact analyzed source edition.
  M2 therefore remains 0/5 source-matched works.

### Deterministic text / dialogue / metric surface

- `scriptorium-text-v1` normalizes CRLF/CR to LF and Unicode to NFC, then emits
  deterministic word/sentence candidate spans with offsets into normalized text. It is
  explicitly `inferred`, not reproduced.
- `scriptorium-dialogue-v1` uses literal normalized LF paragraph boundaries and an
  explicit leading dash+whitespace rule. Unicode U+2028, U+0085 and VT do not create
  false paragraph boundaries. Candidate author remarks use an inspectable alternating
  internal dash-separator rule.
- `scriptorium-punctuation-v1` covers all 14 observed FantLab punctuation fields with a
  declared greedy non-overlap policy and explicit dash/quote/ellipsis handling.
- `scriptorium-metrics-v3` / `scriptorium-deterministic-metrics-v3` currently contains
  29 rows: 28 FantLab-shaped fields plus the Scriptorium sentence-count extension.
- The benchmark harness currently maps 28 FantLab IDs: four general, four dialogue, six
  vocabulary and fourteen punctuation fields.

### Vocabulary profile

- `scriptorium-vocabulary-v1` uses Unicode NFC followed by `casefold()` as its explicit
  inferred lexical identity. It does not lemmatize and does not fold `ё` into `е`.
- `fantlab.vocabulary.unique_words` is available without an external dictionary.
  Active dictionary/non-dictionary counts and UASZ-3000/10000/100000 remain `null`
  unless an explicit dictionary lexeme collection and non-empty profile ID are supplied.
- Explicit dictionaries are normalized/deduplicated and bound to profile ID, canonical
  normalized-set SHA-256 and lexeme count. This establishes reproducible dependency
  identity but does not claim equivalence to FantLab's production dictionary.
- UASZ v1 is an inferred candidate using every complete contiguous N-token window with
  step 1, dictionary filtering, rolling unique-count maintenance and arithmetic mean;
  incomplete tails do not contribute.
- Dictionary-dependent benchmark rows cannot become `pass`/`fail` while FantLab's
  production dictionary identity/version is unproven. Missing integer dictionary actuals
  are `not_run`; missing UASZ values remain `unresolved` under the frozen
  `unresolved_precision` rule.
- Independent review found and repaired a Unicode canonicalization defect in the initial
  dictionary path. The final implementation NFC-normalizes inside `normalize_lexeme()`;
  regressions prove composed/decomposed spellings share membership and dependency digest.
- Independent repaired-head review of PR #23 passed 46/46 standard-library tests under
  Python 3.13.5 and validated generated v3 artifacts against Draft 2020-12 schema rules.

### Morphology compatibility research

- `pylem==0.0.18` is the selected AOT-lineage compatibility candidate; the repository
  records the package/sdist identity and pinned `morph_dict` revision.
- Pinned pylem calls `SetUseNationalConstants(false)`, so runtime POS strings use Latin
  constants. Fifteen runtime strings map unambiguously to observed FantLab buckets.
- Noun `С` and cardinal numeral `ЧИСЛ` both render as runtime `N`; the public Python result
  does not expose a source discriminator, so the collision remains unresolved.
- `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT` and `INFINITIVE` remain distinct
  runtime categories with no proven standalone FantLab bucket/folding rule.
- FantLab homonym/prediction selection and production dictionary equivalence are not
  public. No first-result or guessed folding heuristic is accepted as compatibility.
- Native pylem build/runtime verification is still `not_run`, not a package failure.

### Public repository representation

- README/docs expose the deterministic text, dialogue, punctuation, vocabulary and local
  benchmark capabilities while labeling FantLab-shaped behavior as inferred.
- Two derived *Anna Karenina* excerpt showcases are published with exact Wikisource
  revision provenance, hashes and metrics only; source prose is not committed. Both are
  explicitly illustrative, below 300,000 characters and inadmissible for corpus/parity.
- Existing showcase artifacts preserve the metric profile under which they were
  generated. Vocabulary values were not fabricated from historical hashes; a future
  vocabulary showcase must re-read a provenance-bound source selection.

## Known risks / blockers

1. **Exact source edition risk.** FantLab does not necessarily identify the exact bytes or
   edition behind a published analysis. Parity requires a traceable source match.
2. **Hidden-algorithm risk.** FantLab acknowledges unpublished corrective coefficients
   and know-how; source-matched deltas must drive revisions rather than speculation.
3. **Text-boundary inference.** Exact FantLab normalization, tokenization, abbreviation and
   sentence-boundary behavior remain unknown.
4. **General-metric denominator inference.** Character/token/sentence denominator details
   are not proven equivalent to FantLab.
5. **Punctuation inference.** Overlap, Unicode glyph normalization and parenthesis rules
   remain inferred candidates.
6. **Dialogue inference.** Paragraph markers, embedded author-remark grammar, quoted speech
   and scalar denominators remain unproven.
7. **Vocabulary lexical/window inference.** Exact lexical normalization, UASZ step/edge
   policy and scalar aggregation are not public.
8. **Vocabulary dictionary identity gap.** FantLab's production dictionary/version is
   unknown; arbitrary explicit dictionaries are reproducible input only.
9. **Runtime POS collision.** Pinned pylem collapses noun/cardinal to runtime `N` on the
   public adapter surface.
10. **Extra POS folding unresolved.** Several AOT runtime categories have no proven
    observed FantLab bucket mapping.
11. **Morphology drift.** Pinned pylem/AOT dictionary/source equivalence to FantLab 2022
    has not been established.
12. **Morphology ambiguity.** FantLab homonym/prediction-selection policy is not public.
13. **Native-build verification pending.** pylem 0.0.18 has not yet been built in a
    verified network-enabled runtime.
14. **Copyright risk.** Web accessibility, including Author.Today/fanfiction, is not a
    license; work-specific rights evidence remains mandatory.
15. **Scheduler serialization unverified.** Re-read refs/state before every write and do
    not overwrite a newer state revision.
16. **External mode controller unverified.** The authorized deterministic selection ladder
    is operative, but no independent selection-receipt mechanism has been proven.
17. **Display/cache surface drift.** FantLab summary/detail surfaces may round or cache
    differently; exact source surface must be captured with benchmark expectations.
18. **Display precision unresolved.** Visible decimal digits do not establish formatting
    precision or tie behavior.
19. **Parity-corpus edition gap.** All five retained candidates remain below the M2
    source-edition-admissibility gate.
20. **Hosted CI absent.** Legacy statuses and PR workflow runs were both absent for the
    reviewed PR #23 head. Local independent review evidence is recorded, but CI remains
    not configured.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect open PR checks/comments relevant to that unit;
3. otherwise choose the first unblocked queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file in the same semantic change.

Do not create parallel units merely because an hourly wake occurred.
