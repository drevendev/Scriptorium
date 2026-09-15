# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 65
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-15T00:04:00Z
LAST_RESULT: SCRIP-MORPH-005 authored as Issue #58 / PR #59. The new source-free POS diagnostic decomposes every conservative undefined pylem token into mutually exclusive evidence classes and adds fail-closed FantLab word/defined/undefined POS accounting without changing morphology resolution semantics. The substantive PR is intentionally unmerged pending a later independent exact-head review. Benchmark movement remains 0/5 source-matched works.
LAST_VERIFIED_PROGRESS: Hosted full-work evidence on authored head 4ceee1baa4b961960d32addf878fcef5a2ecf809 passed provider run 34911038536, ordinary frozen diagnostic run 34911038506 and Pages run 34911038635. Artifact 10374333136 was downloaded and inspected: exactly one source-free JSON, 269358 current words, 117554 defined and 151804 undefined. Undefined reasons were 2 no_analysis, 55081 runtime_n_only, 19670 runtime_n_mixed, 10677 extra_runtime_only, 7120 extra_runtime_mixed and 59254 direct_cross_bucket_ambiguity. Thus 151802 / 151804 undefined tokens (99.9987%) are held out by known conservative policy boundaries rather than provider no-analysis. Subsequent commits only enrich source-free bucket-presence diagnostics/tests; this state commit itself creates a newer final head, so fresh exact-final-head CI and artifact inspection are required before review/merge.

## Current unit

```text
UNIT_ID:        SCRIP-MORPH-005
ISSUE:          #58
STATUS:         REVIEW
PR:             #59
BASE_REVISION:  01fe7898ca2ee275818948076f1bbb5d2ee50122
NEXT_ACTION:    Independently review the exact final PR head, changed-file surface,
                comments/threads and hosted checks. Require the Python 3.13 contract,
                exact pylem 0.0.18 native smoke, full frozen Anna Karenina sidecar,
                ordinary frozen diagnostic and Pages builds to be green on that head.
                Download the v2 POS artifact and verify source-free reason accounting,
                partition sums and diagnostic-only/M2-fail-closed boundaries before merge.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral artifact and a reviewed exact-pylem frozen-work transport. SCRIP-MORPH-005 now proposes an inspectable explanation layer for why conservative POS aggregation leaves tokens undefined, but it does not recover any unresolved morphology. The M2 reproduction gate remains **0/5 source-matched works** because FantLab analyzer-input editions remain unknown.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. Recovery/review-ready work preempts new selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-MORPH-005 | review / reproduction | Independently review and, if exact-head evidence is green, merge PR #59 POS undefined/delta decomposition | Issue #58 / PR #59 open; authored substantive unit must not self-merge |
| P1 | SCRIP-MORPH continuation | analyzer core / reproduction | Use reviewed decomposition to investigate the largest still-unresolved morphology axis without guessing `N`, extra-category folding, homonym selection, dictionary identity or service-word aggregation | Depends on SCRIP-MORPH-005 merge |
| P2 | SCRIP-REPRO | benchmark / provenance | Strengthen source-edition matching for retained >=300k FantLab candidates | No current candidate is source-matched; M2 remains 0/5 |
| P3 | SCRIP-SITE | public representation | Publish additional derived analysis when it can be represented without source prose or parity overclaim | Existing static renderer/Pages build is ready; live activation is a separate owner/admin effect |

## Evidence already established

### FantLab / reproduction boundary

- `fantlab-2022-v1` is the frozen compatibility contract. FantLab publicly documents broad metric families while leaving some coefficients/parser details unpublished.
- Exact integer parity is admissible only with exact source-edition identity, legal basis and immutable text digest. Decimal/rate parity also requires independent display-rounding evidence.
- The retained parity seed remains **0/5 source-matched works**. Diagnostic resemblance never advances M2.

### Frozen Anna Karenina candidate

- FantLab work 270306 reports the 19 September 2022 analysis at 1,692,647 characters and 253,275 words but does not disclose analyzer-input edition/bytes.
- The frozen Russian Wikisource/FEB candidate contains 239 pinned chapter revisions and replays deterministically.
- Composite identity: 1,705,605 characters; 3,072,993 UTF-8 bytes; raw and `scriptorium-text-v1` normalized SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`.
- `fantlab_source_edition_match=unknown`; all full-work comparisons are diagnostic-only and M2-inadmissible.

### Frozen Resurrection candidate

- FantLab work 296603 reports 881,244 characters and 126,457 words; immutable analyzer-input identity is undisclosed.
- 129 Wikisource chapter revisions are pinned and replayed under explicit extraction/composition contracts.
- Composite identity: 890,835 characters; 1,610,692 UTF-8 bytes; raw/normalized SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`.
- Source match remains unknown; the 9,591-character display delta is not identity evidence.

### Deterministic metric findings

- The Anna Karenina diagnostic shows characters +12,958 and words +16,083 relative to FantLab; simple numeric-token and lexical-hyphen probes explain little of the gap.
- `scriptorium-punctuation-v2` avoids double-counting token-internal ASCII hyphen-minus, but the frozen dash rate remains about +14.913 per 1000 current words relative to FantLab.
- Dialogue denominator/author-remark semantics remain materially unresolved: production-v1 author text inside dialogue is 38.3920% versus FantLab 17.02%, while stricter opener and whole-text denominator probes move substantially but do not establish parity.
- FantLab dictionary identity is unknown, so dictionary-dependent vocabulary rows remain unresolved.

### Morphology compatibility

- `pylem==0.0.18` is pinned by exact sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` plus source/dictionary provenance.
- Fifteen runtime strings map directly as inferred candidates. Runtime `N` collapses noun/cardinal; `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT` and `INFINITIVE` remain unresolved extra categories.
- `scriptorium-pos-v1` resolves a token only when every supplied analysis maps to the same direct FantLab-shaped bucket. Empty analyses, `N`, extra categories, unknown codes and cross-bucket homonyms remain undefined.
- POS artifacts are bound to normalization profile, normalized-text SHA-256, runtime profile, mapping contract and canonical runtime-candidate digest.
- Provider executability is verified: exact pylem 0.0.18 builds/runs unchanged on isolated Ubuntu 22.04 / Python 3.9 while the modern contract suite remains on Ubuntu 24.04 / Python 3.13.
- `scriptorium-pylem-sidecar-request-v1` is ephemeral and source-bearing; the source-free response carries token hashes and ordered runtime candidates. The modern consumer validates canonical text/token identity and exact provider identity before aggregation.
- The reviewed pre-M005 frozen diagnostic contains 269358 Scriptorium word tokens, 117554 conservatively defined tokens and 151804 undefined tokens. Noun and cardinal remain zero by design because runtime `N` is unresolved, not because the work contains none.
- SCRIP-MORPH-005 diagnostics classify the 151804 undefined rows without changing resolution: 55081 N-only, 19670 N-mixed, 10677 extra-only, 7120 extra-mixed, 59254 direct cross-bucket ambiguity and only 2 no-analysis. `N` is present in 74751 undefined rows; extra-category presence includes ADJ_SHORT 10126, INFINITIVE 8230, PARTICIPLE_SHORT 1100, COLLOC 350 and POSL 0.
- FantLab partition deltas on the unmatched candidate are +16083 words, -70685 defined POS words and +86768 undefined POS words. These are diagnostic accounting only and cannot identify FantLab policy while source identity is unknown.

### Public repository representation

- The static site renderer/publication manifest remain fail-closed and source-free. Existing public material includes two short Anna Karenina derived showcases and a provenance-only Resurrection page.
- Pages builds are reproducible and green; live deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.
- SCRIP-MORPH-005 does not publish the full-work diagnostic as a permanent showcase; it remains hosted verification evidence until independent review determines the diagnostic contract is safe and useful for public representation.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 is 0/5.
2. FantLab corrective coefficients, parser details, exact word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym-selection/prediction behavior and service-word folding remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; five extra runtime categories still lack justified FantLab folding.
5. SCRIP-MORPH-005 shows provider no-analysis is negligible on the frozen candidate, but this does not reveal how FantLab resolves the 151802 policy-blocked tokens.
6. The exact pinned pylem source requires an isolated legacy toolchain; changing that lane requires new evidence rather than silently patching upstream bytes.
7. Pages live activation is a repository-admin effect and remains off.

## Run selection rule

On each wake:

1. resolve interrupted or review-ready work before new selection;
2. inspect exact PR head, checks, comments and artifacts for any recovery unit;
3. otherwise choose the first dependency-satisfied queue row;
4. create/search the corresponding issue before implementation;
5. do exactly one bounded unit and update this file plus the relevant changelog/benchmark/provenance record;
6. do not infer parity or unblock M2 from provider executability or diagnostic resemblance.
