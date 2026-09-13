# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 25
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-13T00:46:47Z
LAST_RESULT: SCRIP-METRIC-002 repaired the PR #23 Unicode dictionary-canonicalization blocker; the unit remains in REVIEW for an independent exact-head verification.
LAST_VERIFIED_PROGRESS: The repair makes scriptorium-vocabulary-v1 lexical identity NFC + casefold on both text and explicit-dictionary paths, so canonically equivalent spellings share membership and dependency identity. Two regressions cover composed/decomposed dictionary-set+digest equality and decomposed-dictionary membership against equivalent text. A focused reconstruction bound to the repaired published vocabulary/text source passed 7/7 Unicode repair assertions. The full repository suite and v3 schema have not been rerun on the repaired final head in this authoring run; hosted CI remains not configured. M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-METRIC-002
ISSUE:          #22
STATUS:         REVIEW
BRANCH:         feature/22-vocabulary-metrics
PR:             #23
NEXT_ACTION:    Independently review the repaired PR #23 exact head, run the full
                repository suite and v3 schema validation, confirm the Unicode
                canonicalization regressions plus dictionary admission gates, and
                merge only if no blocker remains.
```

## Current milestone gate

M0 is closed. M1 closes when the benchmark harness can compare expected vs actual
FantLab-visible deterministic metrics field-by-field while preserving text and
configuration provenance.

## Queue

Ordered highest first among unblocked work after the current review closes.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
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
- Both noun `С` and cardinal numeral `ЧИСЛ` render as runtime `N`. The public pylem Python
  result does not expose the original AOT POS enum/ancode, so this distinction remains
  unresolved rather than guessed.
- `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT` and `INFINITIVE` are distinct pinned
  runtime POS values with no standalone bucket on the observed 2022 FantLab surface.
  Their folding behavior remains unresolved.
- `scriptorium-text-v1` is the first executable text profile. It normalizes line endings
  and Unicode NFC, emits deterministic word/sentence candidate spans with offsets into
  normalized text, and is explicitly classified as inferred rather than reproduced.
- Independent review of the final text-model implementation content passed 11/11
  standard-library golden tests under Python 3.13.5 before merge.
- The architecture names standard-library `unittest` as the initial unit, golden and
  benchmark contract runner. `pytest` is optional future infrastructure, not an implicit
  dependency or a contradictory bootstrap requirement.
- `scriptorium-metrics-v1` provides deterministic character/word/mean-length values plus
  the Scriptorium sentence-count diagnostic; FantLab-namespaced values remain explicitly
  `inferred`.
- `scriptorium-punctuation-v1` covers all 14 observed punctuation fields with a declared
  greedy non-overlap policy, explicit ellipsis/dash/quote mappings and opening-parenthesis
  candidate counting rather than hidden heuristics.
- The first public showcase is bound to Russian Wikisource `Анна Каренина`, Part I,
  Chapter I revision `oldid=4929732`. It stores only provenance, a precise four-paragraph
  selection rule, hashes and derived metrics. The 1,298-character excerpt is explicitly
  non-corpus and non-benchmark evidence.
- `scriptorium-benchmark-v1` executes the frozen comparison contract over implemented
  FantLab metrics, recording raw/normalized hashes, source-edition/legal provenance,
  expected/actual values and raw deltas.
- Integer character/word comparisons can only pass with exact-edition admissible
  provenance; otherwise numeric matches remain diagnostic `unresolved` results.
- Decimal mean/rate comparisons remain `unresolved_precision` with `numeric_match: null`.
  The harness preserves captured JSON numeric lexemes (including trailing zeroes) as
  display evidence without treating those lexical digits as a precision oracle.
- Independent review of the benchmark admission gate required non-empty `edition_label`
  and `source_reference` in addition to exact match, legal basis and raw digest. Regression
  tests prove either missing identity field keeps integer comparisons `unresolved`.
- A reconstructed final benchmark suite passed 26/26 tests under Python 3.13 before merge;
  hosted CI remained not configured rather than green.
- `scriptorium-dialogue-v1` classifies LF-delimited paragraphs as dialogue only for an
  explicit leading `—`, `–` or `-` followed by whitespace and preserves normalized-text
  offsets for dialogue/narration spans.
- Candidate author text inside dialogue is exposed as alternating spans after internal
  whitespace-dash-whitespace separators. This is inspectable inferred behavior, not a
  recovered FantLab parser.
- `scriptorium-metrics-v2` adds all four FantLab dialogue scalars with explicit
  non-whitespace-character denominators and keeps them `inferred`; the benchmark harness
  maps 22 implemented FantLab fields at that revision.
- The second public showcase binds two *Anna Karenina*, Part I, Chapter II dialogue
  paragraphs to Russian Wikisource `oldid=4929731`, the cited Nauka 1970 edition, and
  SHA-256 `2dcd42a6e638809ae17ecb2e250b092e65ac7919701ae0d25cc9cccb5790e7f9` without
  committing the source prose. Its 250 characters are explicitly non-corpus/non-parity.
- Independent review found the first dialogue implementation used Python `splitlines()`,
  which recognizes Unicode separators beyond the frozen LF-only paragraph contract.
  The repaired implementation scans literal normalized `\n` only and regression coverage
  proves U+2028, U+0085 and VT remain inside a single paragraph instead of creating false
  dialogue spans.
- Independent repaired-head review reconstructed exact PR #21 content and passed 34/34
  standard-library tests. A generated v2 artifact also validated against the exact Draft
  2020-12 schema; hosted statuses/workflows were absent, so CI remains not configured.
- FantLab's public vocabulary methodology defines unique words, active dictionary and
  non-dictionary vocabulary, and UASZ-N as unique dictionary words within N consecutive
  words after repeat removal and dictionary filtering; production lexical normalization,
  dictionary identity/version and scalar window/aggregation details are not published.
- `scriptorium-vocabulary-v1` uses Unicode NFC + case-folded tokens as an explicit
  inferred lexical identity on both the text and explicit-dictionary paths. It does not
  lemmatize or fold `ё` into `е`.
- `scriptorium-metrics-v3` adds six vocabulary rows. Unique words require no external
  dictionary; active dictionary/non-dictionary and UASZ values remain `null` until an
  explicit dictionary lexeme set plus profile ID is supplied.
- Explicit dictionary dependencies are bound by profile, canonical normalized-lexeme
  SHA-256 and lexeme count. This makes the supplied dependency reproducible without
  claiming it is FantLab's production dictionary.
- The inferred UASZ scalar uses every complete contiguous N-token window at one-token
  step and an arithmetic mean of rolling unique dictionary counts; incomplete tails do
  not contribute and the implementation is O(words) for each configured window size.
- The benchmark mapping now covers 28 FantLab IDs. Dictionary-dependent rows are barred
  from `pass`/`fail` while FantLab dictionary identity/version is unproven; missing active
  integer actuals are `not_run`, while missing UASZ values remain `unresolved` under the
  frozen `unresolved_precision` comparison-v1 rule.
- Independent review found dictionary entries skipped NFC before case-folding, so
  canonically equivalent spellings could diverge in membership and dependency digest.
  The repaired `normalize_lexeme()` applies NFC before case-folding for every caller; two
  regressions prove composed/decomposed dictionary identities share a digest and match
  canonically equivalent text tokens.

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
4. **General-metric denominator inference.** Character unit, token length and sentence
   length denominator details are not public enough to call current formulas reproduced.
5. **Punctuation inference.** FantLab does not publish overlap, Unicode dash/quote,
   ellipsis normalization or parenthesis-pair rules. `scriptorium-punctuation-v1` is a
   deterministic candidate whose choices require source-matched benchmark pressure.
6. **Dialogue inference.** FantLab does not publish paragraph markers, embedded
   author-remark grammar, quoted-speech handling or scalar dialogue denominators.
   `scriptorium-dialogue-v1` is intentionally narrow and must remain inferred until
   source-matched deltas discriminate its choices.
7. **Runtime POS collision.** Pinned pylem renders both noun and cardinal numeral as
   Latin `N`. `LemmaInfo.part_of_speech` cannot recover the distinction; an explicitly
   exposed source POS discriminator plus benchmark validation is required before these
   two FantLab buckets can be produced compatibly.
8. **Extra-category folding unresolved.** `POSL`, `COLLOC`, `ADJ_SHORT`,
   `PARTICIPLE_SHORT` and `INFINITIVE` exist separately in the pinned runtime, while the
   observed FantLab 2022 surface has no matching standalone buckets.
9. **Morphology drift.** The pinned pylem dictionary/source has not been shown identical
   to FantLab's 2022 production morphology. Source-matched benchmarks must measure drift.
10. **Morphology ambiguity.** Pylem can expose multiple analyses; FantLab's homonym and
    prediction-selection policy is not public. No first-result/weight heuristic is accepted.
11. **Native-build verification pending.** pylem 0.0.18 has not yet been built in a
    verified network-enabled runtime. This remains `not_run`, not a package failure.
12. **Copyright risk.** Author.Today/fanfiction availability is not a license. Treat
    platform texts as candidates until work-specific rights permit analysis/publication.
13. **Scheduler serialization unverified.** Re-read refs/state before write and avoid
    same-run author+merge of substantial PRs.
14. **External mode controller unverified.** The user-authorized deterministic selection
    ladder is operative, but no independent EndlessZen controller/selection receipt
    mechanism has been bound and proven yet.
15. **Display/cache surface drift.** Summary and detailed FantLab surfaces may expose
    differently rounded or cached values. Benchmark expectations must name the exact
    source surface and capture display text; cross-surface joining is not parity evidence.
16. **Display precision unresolved.** FantLab may trim trailing zeroes and does not publish
    a general formatting/tie rule. Unknown precision remains unresolved rather than
    inferred from rendered text.
17. **Parity-corpus edition gap.** None of the five retained candidates has evidence
    tying its source transcription to FantLab's exact analyzed edition/bytes. M2 remains
    blocked until that evidence is found or the user explicitly changes the gate.
18. **Vocabulary lexical/window inference.** FantLab does not publish exact lexical
    normalization, UASZ window step, edge policy or scalar aggregation. NFC + case-folded
    surface forms and step-1 complete-window means remain inferred candidates.
19. **Vocabulary dictionary identity gap.** FantLab's production dictionary/version is
    not established. An arbitrary explicit dictionary is reproducible input only and
    must not make dictionary-dependent rows parity-admissible.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect open PR checks/comments relevant to that unit;
3. otherwise choose the first unblocked queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file in the same semantic change.

Do not create parallel units merely because an hourly wake occurred.
