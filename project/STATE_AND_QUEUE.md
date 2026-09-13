# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 36
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-13T13:59:00Z
LAST_RESULT: SCRIP-SITE-003 authored on PR #31; a gated GitHub Pages build/upload/deploy workflow is ready for independent exact-head review and must not be merged in the authoring run.
LAST_VERIFIED_PROGRESS: Re-checked SCRIP-MORPH-003 first; native pylem/provider provenance remains non-executable because pylem is not installed and the execution container still cannot resolve GitHub/PyPI package hosts. SCRIP-SITE-003 therefore became the first dependency-satisfied queue unit. PR #31 adds a Python 3.13 standard-library verification and deterministic static-site build, uploads only disposable build/site output, pins current GitHub-owned Pages actions to reviewed full release-tag SHAs, keeps build permissions read-only with checkout credentials not persisted, and isolates pages:write/id-token:write to a master-only deployment job behind the explicit SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true repository-variable interlock. The workflow does not enable Pages or use secrets/PATs. Focused workflow contract checks pass 5/5 in the authoring environment. Independent hosted execution and review remain required before merge. GitHub Pages repository settings remain disabled/unconfigured by this unit. M2 remains 0/5 source-matched works.

## Current unit

```text
UNIT_ID:        SCRIP-SITE-003
ISSUE:          #30
STATUS:         REVIEW
PR:             #31
MERGED_COMMIT:  —
NEXT_ACTION:    Independently review the exact PR #31 head. Inspect the hosted pull-request
                workflow run and jobs, require the complete standard-library suite and
                deterministic build/upload job to pass, confirm deploy is skipped on PR,
                verify full-SHA action pins/permissions/activation boundary, and only then
                decide whether to merge. Do not enable Pages or set the deployment
                interlock in the review unless separately justified as an administrator
                effect after the code is merged.
```

## Current milestone gate

M0 is closed. M1 closes when the benchmark harness can compare expected vs actual
FantLab-visible deterministic metrics field-by-field while preserving text and
configuration provenance. General, dialogue, vocabulary and punctuation families are
executable inferred candidates. POS aggregation now has a versioned provider-neutral
candidate artifact, but native/provider execution identity and benchmark-harness wiring
remain separate work; the M1 gate is therefore still open.

## Queue

Evaluate rows in priority order after checking their dependencies; skip a row while its
dependency is not executable.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P1 | SCRIP-MORPH-003 | implementation | Bind pinned pylem/provider execution and wire POS artifacts into diagnostic benchmark comparison | SCRIP-MORPH-002; verified provider/runtime provenance; currently blocked by unavailable native/provider execution environment |
| P2 | SCRIP-SITE-003 | implementation | Add a reviewed GitHub Pages build/upload/deploy workflow over `scriptorium-static-site-v1`; keep generated output disposable and preserve fail-closed evidence/legal gates | SCRIP-SITE-002; authored on PR #31 and awaiting independent hosted review |

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
- `scriptorium-metrics-v3` / `scriptorium-deterministic-metrics-v3` contains 29 rows:
  28 FantLab-shaped general/dialogue/vocabulary/punctuation fields plus the Scriptorium
  sentence-count extension.
- The main benchmark harness currently maps those 28 FantLab IDs. POS is deliberately
  not injected into that artifact until a provider execution/configuration identity is
  pinned rather than supplied as an unverified detached candidate matrix.

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
- Noun `С` and cardinal numeral `ЧИСЛ` both render as runtime `N`; the public Python
  result does not expose a source discriminator, so the collision remains unresolved.
- `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT` and `INFINITIVE` remain distinct
  runtime categories with no proven standalone FantLab bucket/folding rule.
- FantLab homonym/prediction selection and production dictionary equivalence are not
  public. No first-result or guessed folding heuristic is accepted as compatibility.
- Native pylem build/runtime verification is still `not_run`, not a package failure.
- The 2026-09-13 SCRIP-SITE-003 selection re-check again found no installed pylem and DNS
  unavailable for GitHub/PyPI package hosts in the execution container. Connector access
  to GitHub remains healthy; this does not constitute provider-runtime verification.

### Provider-neutral POS metric surface

- `scriptorium-pos-v1` accepts exactly one runtime-analysis sequence per deterministic
  Scriptorium word token and binds the artifact to `scriptorium-text-v1`, SHA-256 of the
  normalized UTF-8 text, a caller-supplied runtime profile, the canonical candidate-matrix
  SHA-256 and the pinned AOT/pylem mapping contract.
- Independent review proved the runtime-candidate digest alone was insufficient: two
  texts with identical word/sentence counts and the same candidate matrix can have
  different sentence boundaries and therefore different bigram/position metrics. The
  repaired schema freezes both text profile and normalized-text identity.
- A token is defined only when every candidate uses one of the 15 direct runtime strings
  and all candidates map to the same displayed FantLab bucket. Empty analyses, runtime
  `N`, unresolved extra categories, unknown codes and cross-bucket homonyms are undefined.
- Distribution output includes defined/undefined word counts/rates and every one of the
  17 displayed FantLab bucket counts and percentages of defined words. Service-word
  aggregation stays explicit `unresolved` null data rather than a guessed POS fold.
- The POS-bigram candidate emits all 17x17 ordered cells, counts only resolved adjacent
  tokens inside the same Scriptorium sentence candidate and reports raw count plus
  occurrences per 1000 total Scriptorium word tokens. Undefined tokens break pairs.
- Sentence-position output emits positions 1..20. Based on FantLab's public “randomly
  selected sentence” wording, every cell uses all Scriptorium sentence candidates as
  denominator; short sentences and undefined tokens contribute zero to the numerator.
- Bigram sentence-bounding and position denominator choices are explicitly inferred;
  they require source-matched benchmark discrimination before any reproduced claim.
- `scriptorium-pos-metrics-v1` freezes a 17-bucket distribution, complete 17x17 bigram
  matrix and 20x17 position surface. Independent repaired-head review of PR #25 passed
  the full 56/56 standard-library suite and Draft 2020-12 validation of generated POS
  artifacts, including the text-segmentation identity regression.

### Public repository representation

- README/docs expose deterministic text, dialogue, punctuation, vocabulary and POS
  aggregation capabilities while labeling FantLab-shaped behavior as inferred.
- `docs/POS_MODEL.md` explains the conservative pylem runtime boundary, unresolved
  noun/cardinal collision, text/runtime identity, bigram candidate and sentence-position
  denominator.
- Two derived *Anna Karenina* excerpt showcases are published with exact Wikisource
  revision provenance, hashes and metrics only; source prose is not committed. Both are
  explicitly illustrative, below 300,000 characters and inadmissible for corpus/parity.
- Existing showcase artifacts preserve the metric profile under which they were
  generated. Vocabulary/POS values were not fabricated from historical hashes; a future
  richer showcase must re-read a provenance-bound source selection and record provider
  execution identity where morphology is involved.
- `scriptorium-publication-manifest-v1` is merged as an explicit Pages allow-list rather
  than directory discovery. The seed manifest indexes exactly the two existing showcase
  artifacts, freezes stable slugs and marks source text absent plus both benchmark/corpus
  admissibility as false.
- Manifest-level compatibility claims are checked against canonical per-metric
  `compatibility_status` values by executable fail-closed derivation. The two historical
  showcase artifacts derive to `mixed`; a manifest-only upgrade to `reproduced` is a
  validation error rather than publishable presentation metadata.
- `scriptorium-static-site-v1` is merged. It consumes only the explicit manifest,
  implements stable work-showcase routes, revalidates canonical evidence/admissibility/
  source-text labels, renders selected derived and provenance fields with HTML escaping,
  emits exact input digests, and does not fetch remote source material. Reserved future
  artifact kinds fail closed.
- The renderer enforces the exact v1 manifest top-level/entry key sets and allows only
  the two current showcase artifact contracts (`scriptorium-deterministic-metrics-v1`
  and `scriptorium-deterministic-metrics-v2`). Unknown future schema strings fail closed
  even when the manifest and artifact agree, so publication semantics cannot expand by
  accident.
- The renderer validates/renders the full requested site before replacing output; a
  failed entry leaves the previous tree untouched, while a successful rebuild removes
  stale files. Generated `/build/` output is ignored and remains non-canonical.
- Independent repaired-head review of PR #29 passed the reconstructed full 74/74
  standard-library inventory and two deterministic real seed builds. The generated HTML
  contained no source-selection prose from either canonical showcase and preserved the
  public `mixed` / `not_admissible` evidence labels.
- PR #31 now proposes the first executable Pages workflow: PR/relevant master builds run
  Python 3.13 tests, build and byte-compare the deterministic site, and upload only
  `build/site`. All five GitHub-owned actions are full-SHA pinned to reviewed current
  release tags; current configure/deploy action generations use Node 24.
- The proposed deploy job is master-only, requires the explicit
  `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` repository variable, targets the `github-pages`
  environment, and alone receives `pages: write` and `id-token: write`. The workflow does
  not use configure-pages privileged enablement, secrets or a PAT. Pages repository
  configuration therefore remains a separate administrator effect after independent
  review rather than being inferred from workflow presence.

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
    verified network-enabled runtime; the current execution environment still lacks DNS
    for required package/source hosts.
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
20. **Hosted CI absent historically.** Reviewed PR #29 had no hosted statuses/workflow
    runs. PR #31 introduces the first hosted verification path and must be judged from its
    actual exact-head run rather than assumed green from workflow syntax.
21. **POS adjacency/position inference.** Sentence-bounded bigrams and all-sentence
    position denominators are evidence-based candidates, not established FantLab internals.
22. **Detached provider provenance.** The POS aggregator binds text and supplied runtime
    candidates, but it still does not prove which binary/dictionary/config produced those
    candidates; provider execution must be pinned before benchmark integration.
23. **Pages deployment activation pending.** PR #31 contains a gated workflow candidate,
    but repository Pages source/settings are not enabled by code and the explicit deploy
    interlock must remain unset until independent workflow review succeeds.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect open PR checks/comments relevant to that unit;
3. otherwise choose the first dependency-satisfied queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file in the same semantic change.

Do not create parallel units merely because an hourly wake occurred.
