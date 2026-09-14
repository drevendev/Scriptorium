# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 61
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-14T20:15:00Z
LAST_RESULT: SCRIP-MORPH-004 authored as Issue #56 / PR #57. The branch now defines a fail-closed JSON transport from the modern Scriptorium runtime to the isolated exact pylem 0.0.18 Python 3.9 sidecar and back, then uses it for a full frozen Anna Karenina POS diagnostic. Source-bearing request material is ephemeral CI-local state; uploaded output is derived/source-free and diagnostic-only. The substantive PR is intentionally unmerged pending a later independent exact-head review.
LAST_VERIFIED_PROGRESS: On authored head 7011ed51a00a66f5e5ad186e019bde0ed045abaa the complete Python 3.13 standard-library contract job passed, Pages run 34891499205 passed, and the ordinary frozen diagnostic run 34891499241 passed. The new full-work pylem job was still executing when this durable-state commit was prepared, so those intermediate checks must not be treated as final-head evidence. Updating this file creates a newer head and therefore requires fresh exact-final-head CI before review/merge. Benchmark movement remains 0/5 source-matched works.

## Current unit

```text
UNIT_ID:        SCRIP-MORPH-004
ISSUE:          #56
STATUS:         REVIEW
PR:             #57
BASE_REVISION:  df37e6021b26512d1766dc4c44b4fd1b65d6e425
NEXT_ACTION:    Independently review the exact final PR head, changed-file surface,
                comments/threads and hosted checks. Require all three provider jobs,
                especially the frozen Anna Karenina sidecar diagnostic, to be green on
                that exact head. Inspect the uploaded diagnostic and verify that it is
                source-free, diagnostic_only, source-match unknown and M2-inadmissible.
                Merge only if those boundaries hold; otherwise repair the exact defect.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation families are executable inferred candidates. POS aggregation has a versioned provider-neutral artifact and exact pylem 0.0.18 executability is verified in an isolated Ubuntu 22.04 / Python 3.9 lane. SCRIP-MORPH-004 now proposes the missing frozen-work transport: the modern runtime freezes token identity, the legacy sidecar returns all pylem runtime candidates, and the modern runtime validates hashes/profile/candidates before applying unchanged `scriptorium-pos-v1` aggregation. The M2 reproduction gate remains **0/5 source-matched works** because FantLab analyzer-input editions are still unknown.

## Queue

Evaluate rows in priority order and skip dependencies that are not executable. Recovery/review-ready work preempts new selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-MORPH-004 | review / reproduction | Independently review and, if exact-head evidence is green, merge PR #57 frozen-work pylem transport/diagnostic | Issue #56 / PR #57 open; authored substantive unit must not self-merge |
| P1 | SCRIP-MORPH-005 | analyzer core / reproduction | Use the first verified full-work POS diagnostic to investigate the largest POS deltas without guessing unresolved `N`, extra-category folding or FantLab homonym behavior | Depends on SCRIP-MORPH-004 merge and source-free diagnostic evidence |
| P2 | SCRIP-REPRO | benchmark / provenance | Strengthen source-edition matching for retained >=300k FantLab candidates | No current candidate is source-matched; M2 remains 0/5 |
| P3 | SCRIP-SITE | public representation | Publish additional derived analysis only when it can be represented without source prose or parity overclaim | Existing static renderer/Pages build is ready; live activation is a separate owner/admin effect |

## Evidence already established

### FantLab / reproduction boundary

- `fantlab-2022-v1` is the frozen compatibility contract and FantLab publicly documents broad metric families while leaving some coefficients/parser details unpublished.
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

- The Anna Karenina diagnostic previously showed characters +12,958 and words +16,083 relative to FantLab; simple numeric-token and lexical-hyphen probes explain little of the gap.
- `scriptorium-punctuation-v2` avoids double-counting token-internal ASCII hyphen-minus, but the frozen dash rate remains about +14.913 per 1000 current words relative to FantLab.
- Dialogue denominator/author-remark semantics remain materially unresolved: production-v1 author text inside dialogue is 38.3920% versus FantLab 17.02%, while stricter opener and whole-text denominator probes move substantially but do not establish parity.
- FantLab dictionary identity is unknown, so dictionary-dependent vocabulary rows remain unresolved.

### Morphology compatibility

- `pylem==0.0.18` is pinned by exact sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` plus source/dictionary provenance.
- Fifteen runtime strings map directly as inferred candidates. Runtime `N` collapses noun/cardinal; `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT` and `INFINITIVE` remain unresolved extra categories.
- `scriptorium-pos-v1` resolves a token only when every supplied analysis maps to the same direct FantLab-shaped bucket. Empty analyses, `N`, extra categories, unknown codes and cross-bucket homonyms remain undefined.
- POS artifacts are bound to normalization profile, normalized-text SHA-256, runtime profile, mapping contract and canonical runtime-candidate digest.
- Provider executability is verified: exact pylem 0.0.18 builds/runs unchanged on isolated Ubuntu 22.04 / Python 3.9 while the modern contract suite remains on Ubuntu 24.04 / Python 3.13. Ubuntu 24.04 / GCC 13 does not compile the pinned legacy vendored source unchanged; this is a toolchain constraint, not evidence about morphology parity.
- SCRIP-MORPH-004 adds `scriptorium-pylem-sidecar-request-v1` / `scriptorium-pylem-sidecar-response-v1`. The request is ephemeral and source-bearing; the response carries token hashes and ordered runtime candidates. The modern consumer revalidates normalized text, every token ordinal/hash, runtime profile and runtime vocabulary before aggregation.
- The proposed `scriptorium-frozen-pos-diagnostic-v1` uploads only aggregate POS/provenance. It explicitly keeps FantLab source edition, dictionary equivalence, homonym selection, noun/cardinal recovery, extra-category folding and M2 parity unresolved.

### Public repository representation

- The static site renderer/publication manifest remain fail-closed and source-free. Existing public material includes two short Anna Karenina derived showcases and a provenance-only Resurrection page.
- Pages builds are reproducible and green; live deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration. Activation is still a separate owner/admin effect rather than a code blocker.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 is 0/5.
2. FantLab corrective coefficients, parser details, exact word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym-selection/prediction behavior and service-word folding remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; five extra runtime categories still lack justified FantLab folding.
5. The exact pinned pylem source requires an isolated legacy toolchain; changing that lane requires new evidence rather than silently patching upstream bytes.
6. PR #57 full frozen-work sidecar execution must pass on its **final exact head** and its uploaded artifact must be independently inspected before merge.
7. Pages live activation is a repository-admin effect and remains off.

## Run selection rule

On each wake:

1. resolve `CURRENT_UNIT` review/recovery before new work;
2. inspect exact PR head, changed files, checks, comments and review threads;
3. for PR #57, verify the frozen-work artifact itself, not merely workflow conclusion;
4. if merged, update canonical changelog/state on master and only then select the next dependency-satisfied queue row;
5. do not infer parity or unblock M2 from provider executability or diagnostic resemblance.
