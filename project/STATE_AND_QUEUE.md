# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 148
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-18T15:58:00Z
LAST_RESULT: SCRIP-CORPUS-020 / Issue #109 authored Draft PR #128 from master `155a98cadf1595e9bbadd0a2cd63f61a164f8e55` to reconcile the structured Klim provenance trace with the merged literary-body identity. The trace now references canonical `gorky-klim-samgin-ru.literary-body.json`, records the candidate-specific four-part composite identity, removes stale body-unfrozen claims, and sets `diagnostic_ready=true` while preserving `fantlab_source_edition_match=unknown`, `gate_ready=false`, and `m2_parity_admissible=false`. The change deliberately does not promote exact historical Russian Wikisource MediaWiki-core/Poem deployment equivalence or FantLab analyzer-input identity. PR #128 remains Draft for independent later-run review.
LAST_VERIFIED_PROGRESS: The canonical source-free Klim literary-body identity remains 3,810,618 characters / 6,958,930 UTF-8 bytes with raw and `scriptorium-text-v1` SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`; PR #128 synchronizes the structured trace to that already-merged evidence without changing its `candidate_specific_inferred_reconstruction` class. M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-020
ISSUE:          #109
STATUS:         TRACE_RECONCILIATION_AUTHORED_REVIEW_PENDING
PR:             #128 (Draft); #127 (merged); #126 (merged); #125 (closed superseded duplicate)
MERGED_COMMIT:  7bf0dd79bde5e9df76a4b96ebe56f4792c49e23e
NEXT_ACTION:    Independently review Draft PR #128 on its exact final head. Verify the structured trace remains
                consistent with canonical `gorky-klim-samgin-ru.literary-body.json`, that the JSON is valid,
                and that all relevant exact-head checks are green. If no blocking defect exists, merge it and
                close #109 only if every issue acceptance criterion is then satisfied. Preserve
                `fantlab_source_edition_match=unknown`, `gate_ready=false`, `m2_parity_admissible=false`;
                do not infer historical MediaWiki/Poem deployment or FantLab analyzer-input identity.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-CORPUS-020 review | recovery / corpus provenance | Independently review Draft PR #128, verify exact-head checks and evidence boundaries, merge only if safe, then decide whether #109 is complete | Structured trace reconciliation authored; substantial authoring must not be self-approved in the same run |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation/edition identity and explicit legal provenance |

## Retained corpus / provenance status

Detailed evidence lives in `corpus/candidates/`, `benchmarks/`, `project/run-receipts/`, `project/CHANGELOG.md`, and `project/CHANGELOG.d/`; this state file keeps only the orientation-critical summary.

- **Anna Karenina** — frozen public-source candidate: 239 pinned chapter revisions; composite 1,705,605 characters; SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; FantLab source match unknown.
- **Resurrection** — frozen public-source candidate: 129 pinned chapter revisions; composite 890,835 characters; SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`; FantLab source match unknown.
- **Brothers Karamazov** — frozen public-source candidate: 98 admitted revisions; composite 1,810,351 characters; SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`; FantLab source match unknown.
- **Silver Dove** — frozen single-revision public-source candidate at `oldid=5588003`; composite 563,125 characters; SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`; FantLab source match unknown.
- **Petersburg** — first-1916-edition facsimile lead; Commons description revision is pinned but PDF bytes/OCR identity are not; no binary/source match claim.
- **Hyperboloid of Engineer Garin** — frozen Russian Wikisource single-revision candidate at `oldid=5014458`; extraction profile `scriptorium-hyperboloid-wikisource-body-v1` reproduces 499,066 characters / 930,560 bytes with raw and normalized SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`. Print-edition identity and FantLab source match remain unresolved.
- **Shining World** — 1965-source Wikisource family with 34 chapter subpages; chapter identities/composite remain unfrozen.
- **Road to Nowhere** — primary Pravda-1965 family remains unfrozen; distinct `az.lib.ru` route at `oldid=5585836` has alternate literary-body identity 442,656 characters / 825,899 bytes, SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`. Neither route is identified as FantLab input.
- **Running on Waves** — Detskaya literatura 1965 source-cited family with 35 chapters plus epilogue; literary subpage identities/composite remain unfrozen.
- **The White Guard** — Wikisource mixes two bibliographic source families across chapters 1–11 and 12–20; all 20 chapter identities/composite remain unfrozen.
- **The Twelve Chairs** — keep the 40-chapter later 1938/1961 editorial family distinct from the 41-chapter 1928 first standalone edition; neither literary body is frozen, and coauthorship prevents individual-author attribution without an explicit VOICE model.
- **The Life of Klim Samgin** — four exact parent revisions and the Part 2 dependency are replay-frozen; merged PRs #111–#124 freeze the target-only `#lst`, inferred `poemx1`/Poem boundaries, structural surface and all thirteen plain literary values; #126 merged the candidate-specific fail-closed extractor; #127 merged the canonical source-free per-part and composite literary-body identities. Draft PR #128 now reconciles the structured provenance trace to that identity, marks it diagnostic-ready only, and retains exact historical MediaWiki/Poem deployment plus FantLab analyzer-input/source-edition identity as unresolved.

## Deterministic / morphology findings

- Frozen Anna diagnostics still show large character/word differences from FantLab; numeric-token and lexical-hyphen probes do not explain the word gap.
- `scriptorium-punctuation-v2` removes internal ASCII-hyphen double counting, but dash-rate parity remains unresolved.
- Dialogue author-remark / denominator semantics remain unresolved.
- FantLab dictionary/version, homonym selection, word-boundary semantics and service-word aggregation remain unknown.
- `pylem==0.0.18` is pinned by exact sdist SHA-256 `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515` plus source/dictionary provenance.
- Runtime `N` loses noun/cardinal distinction. Five additional methodology-only AOT categories remain diagnostic and are not silently folded into the work-page-compatible production view.

## Public repository representation

- Static publication remains source-free and deterministic; publication tests reject forbidden source-prose keys.
- Public corpus navigation exposes retained candidates with provenance boundaries rather than parity claims.
- Hyperboloid and Road to Nowhere expose frozen source-free literary-body identities with explicit unresolved source-match boundaries.
- Klim Samgin exposes the source graph, fail-closed extractor, canonical source-free per-part/composite literary-body identities and public candidate page. PR #128 is a machine-readable provenance consistency fix only; it does not add a new Pages slice or change the public evidence class.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories are diagnostic until their visible work-page relation is evidenced.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg lacks a Scriptorium-recorded PDF snapshot digest and deterministic OCR/page-extraction identity.
7. Several twentieth-century candidates remain trace-only/unfrozen or bibliographically unresolved at the literary-body level.
8. Klim Samgin has a replay-verified candidate-specific literary-body identity, but exact historical Russian Wikisource MediaWiki-core/Poem deployment equivalence and FantLab analyzer-input bytes/edition remain unproven. PR #128 reconciles the structured trace but must receive independent review before #109 is closed.
9. Pages live activation remains a repository-admin effect and is off.
