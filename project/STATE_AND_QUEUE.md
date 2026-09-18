# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 151
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-18T19:52:41Z
LAST_RESULT: SCRIP-CORPUS-021 / Issue #129 independently reviewed PR #130 on exact head `e28c33e1eca894d0e065355a337905712f0dd414`. The branch was 14 commits ahead / 0 behind master, mergeable, with no prior submitted reviews or inline review threads. All 14 pull-request workflows on the final exact head were green. Dedicated `Shining World source inventory` run `35383710767`, job `105725607198`, checked out that exact head and completed the full standard-library suite, live source-free 34-title audit, semantic comparison against the committed inventory, exact replay of all 19 present revisions, source-free artifact guard, and artifact upload successfully. Independent review found no blocking defect; the prior public README inconsistency was already reconciled on the final head. PR #130 was marked Ready and squash-merged as `55ed6ed314d995d695c27d33cb73a8146e63035b`.
LAST_VERIFIED_PROGRESS: `grin-shining-world-ru` now has a merged fail-closed source-inventory contract rather than the prior false shorthand "34 chapter subpages". Exact revision ID / UTC timestamp / MediaWiki SHA-1 identities are recorded for 19 present pages; 15 missing advertised titles carry no invented identity. Public corpus navigation and the structured provenance trace both distinguish 34 advertised links from 19 existing pages and explicitly forbid silent cross-provider completion. The 1965 Pravda bibliographic family remains useful provenance, but this Wikisource route is not a source-complete novel witness and no complete literary body/composite is claimed. FantLab source identity remains unknown and M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-021
ISSUE:          #129 (closed completed)
STATUS:         COMPLETE
PR:             #130 (merged)
MERGED_COMMIT:  55ed6ed314d995d695c27d33cb73a8146e63035b
NEXT_ACTION:    On the next wake, re-apply the selection ladder. There are no open Scriptorium PRs and no known
                failing required checks after this review. Select the highest-priority unblocked corpus/provenance
                continuation, prioritizing a legally usable >=300k twentieth/twenty-first-century, translated or
                nonfiction candidate when evidence quality is sufficient. Preserve translation/edition identity and
                do not move M2 without an independently established FantLab analyzer-input/source-edition match.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation/edition identity and explicit legal provenance |

## Retained corpus / provenance status

Detailed evidence lives in `corpus/candidates/`, `benchmarks/`, `project/run-receipts/`, `project/CHANGELOG.md`, and `project/CHANGELOG.d/`; this state file keeps only the orientation-critical summary.

- **Anna Karenina** — frozen public-source candidate: 239 pinned chapter revisions; composite 1,705,605 characters; SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; FantLab source match unknown.
- **Resurrection** — frozen public-source candidate: 129 pinned chapter revisions; composite 890,835 characters; SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`; FantLab source match unknown.
- **Brothers Karamazov** — frozen public-source candidate: 98 admitted revisions; composite 1,810,351 characters; SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`; FantLab source match unknown.
- **Silver Dove** — frozen single-revision public-source candidate at `oldid=5588003`; composite 563,125 characters; SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`; FantLab source match unknown.
- **Petersburg** — first-1916-edition facsimile lead; Commons description revision is pinned but PDF bytes/OCR identity are not; no binary/source match claim.
- **Hyperboloid of Engineer Garin** — frozen Russian Wikisource single-revision candidate at `oldid=5014458`; extraction profile `scriptorium-hyperboloid-wikisource-body-v1` reproduces 499,066 characters / 930,560 bytes with raw and normalized SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`. Print-edition identity and FantLab source match remain unresolved.
- **Shining World** — reviewed 1965-source Wikisource index advertises 34 chapter links, but the merged SCRIP-CORPUS-021 source-free audit found only 19 existing pages: Part I I-XVI and Part II I-III. Part II IV-XI and all Part III chapters are missing. Exact present-page revision identities are frozen in master; complete literary-body/composite identity remains impossible from this route alone, and FantLab source match is unknown.
- **Road to Nowhere** — primary Pravda-1965 family remains unfrozen; distinct `az.lib.ru` route at `oldid=5585836` has alternate literary-body identity 442,656 characters / 825,899 bytes, SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`. Neither route is identified as FantLab input.
- **Running on Waves** — Detskaya literatura 1965 source-cited family with 35 chapters plus epilogue; literary subpage identities/composite remain unfrozen.
- **The White Guard** — Wikisource mixes two bibliographic source families across chapters 1–11 and 12–20; all 20 chapter identities/composite remain unfrozen.
- **The Twelve Chairs** — keep the 40-chapter later 1938/1961 editorial family distinct from the 41-chapter 1928 first standalone edition; neither literary body is frozen, and coauthorship prevents individual-author attribution without an explicit VOICE model.
- **The Life of Klim Samgin** — SCRIP-CORPUS-020 is complete. Four exact parent revisions and the Part 2 dependency are replay-frozen; merged PRs #111–#124 freeze the target-only `#lst`, inferred `poemx1`/Poem boundaries, structural surface and all thirteen plain literary values; #126 merged the candidate-specific fail-closed extractor; #127 merged the canonical source-free per-part and composite literary-body identities; #128 reconciled the structured provenance trace. Exact historical MediaWiki/Poem deployment and FantLab analyzer-input/source-edition identity remain unresolved.

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
- Shining World now exposes a merged inspectable source-free inventory artifact and corrected public/structured provenance that distinguish the 34 links advertised by the reviewed index from the 19 pages that actually exist; missing targets are visible blockers, not silently filled text.
- Klim Samgin exposes the source graph, fail-closed extractor, canonical source-free per-part/composite literary-body identities, public candidate page, and a structured provenance trace consistent with those identities. Evidence remains explicitly diagnostic-only and source-match unknown.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories are diagnostic until their visible work-page relation is evidenced.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg lacks a Scriptorium-recorded PDF snapshot digest and deterministic OCR/page-extraction identity.
7. Shining World's primary 1965-source Wikisource family is incomplete: 15 of 34 advertised chapter targets are missing, so a complete literary body cannot be frozen from that route alone without a separately justified source-complete witness.
8. Several other twentieth-century candidates remain trace-only/unfrozen or bibliographically unresolved at the literary-body level.
9. Klim Samgin is fully frozen at the candidate-specific literary-body/provenance level, but exact historical Russian Wikisource MediaWiki-core/Poem deployment equivalence and FantLab analyzer-input bytes/edition remain unproven; these are evidence boundaries, not open acceptance criteria for closed Issue #109.
10. Pages live activation remains a repository-admin effect and is off.
