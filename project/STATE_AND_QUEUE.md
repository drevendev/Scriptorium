# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 146
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-18T13:55:00Z
LAST_RESULT: SCRIP-CORPUS-020 / Issue #109 independently captured the source-free Klim Samgin literary-body identity that PR #126 deliberately left uncommitted. The prior exact-head replay artifact from run `35340846781` / job `105586149163` was recovered and verified (artifact ZIP SHA-256 `717177464f00e51915cd65d661cb428d22210bb1f7b5055c4a813f0777ae6193`; contained manifest SHA-256 `8057605ce3d8f547c7091647f5315662b1d8d9c04b94b7b16f7fbacf80b7499f`). Draft PR #127 now commits that exact source-free manifest, a regression that prevents source/parity claim promotion, and a synchronized public candidate page. The frozen candidate-specific composite is 3,810,618 characters / 6,958,930 UTF-8 bytes with raw and `scriptorium-text-v1` SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`. Historical Russian Wikisource MediaWiki/Poem deployment equivalence and FantLab analyzer-input identity remain unresolved.
LAST_VERIFIED_PROGRESS: Draft PR #127 exact head before this state commit was `a58421d1f5040365ac9af525936ae7949353feb5` and mergeable-clean. Its dedicated exact-head workflow run `35352951917`, job `105625237664`, checked out that SHA, ran 255 tests successfully, re-fetched the exact five-revision source graph, regenerated the committed literary-body manifest byte-for-byte, and replay-validated it. Frozen diagnostic and Pages checks on the same head also passed. Subsequent public-provenance/state commits are documentation/control-plane changes and require final-head CI before independent review. M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-020
ISSUE:          #109
STATUS:         LITERARY_BODY_IDENTITY_CAPTURE_DRAFT_OPEN
PR:             #127 (Draft); #126 (merged); #125 (closed superseded duplicate)
MERGED_COMMIT:  211540828eae37d65e9f2ea994a592295d54b4b3
NEXT_ACTION:    Independently review Draft PR #127 on its final exact head. Require the dedicated Klim replay to re-fetch
                all five pinned revisions, regenerate the committed source-free manifest byte-for-byte, and replay it
                successfully together with all triggered required checks. If clean, merge #127 and reconcile the
                structured Klim provenance trace/state without promoting historical MediaWiki/Poem deployment or
                FantLab analyzer-input equivalence. M2 remains 0/5 until independent source-match evidence exists.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-CORPUS-020 continuation | corpus / provenance | Independently review Draft PR #127 and, only with exact-final-head replay/required checks green, merge the canonical source-free Klim literary-body identity; then reconcile the structured provenance trace and close or advance #109 without source prose | Candidate-specific fail-closed extractor is merged as PR #126; Draft #127 captures the independently reproduced identity and public page; historical Wikisource core/Poem deployment equivalence and FantLab source identity remain unproven |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation/edition identity and explicit legal provenance |

## Retained corpus / provenance status

Detailed evidence lives in `corpus/candidates/`, `benchmarks/`, `project/run-receipts/`, `project/CHANGELOG.md`, and `project/CHANGELOG.d/`; this state file keeps only the orientation-critical summary.

- **Anna Karenina** — frozen public-source candidate: 239 pinned chapter revisions; composite 1,705,605 characters; SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; FantLab source match unknown.
- **Resurrection** — frozen public-source candidate: 129 pinned chapter revisions; composite 890,835 characters; SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`; FantLab source match unknown.
- **Brothers Karamazov** — frozen public-source candidate: 98 admitted revisions; composite 1,810,351 characters; SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`; FantLab source match unknown.
- **Silver Dove** — frozen single-revision public-source candidate at `oldid=5588003`; composite 563,125 characters; SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`; FantLab source match unknown.
- **Petersburg** — first-1916-edition facsimile lead; Commons description revision is pinned but PDF bytes/OCR identity are not; no binary/source match claim.
- **Hyperboloid of Engineer Garin** — frozen single-revision public-source candidate at Russian Wikisource `oldid=5014458`; versioned `scriptorium-hyperboloid-wikisource-body-v1` extraction reproduces 499,066 characters / 930,560 bytes with raw and normalized SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`. Direct print-edition identity remains unresolved and FantLab source match is unknown.
- **Shining World** — 1965-source Wikisource family with 34 chapter subpages; chapter identities/composite remain unfrozen.
- **Road to Nowhere** — primary Pravda-1965 source family remains unfrozen. The distinct `az.lib.ru` single-page route at `oldid=5585836` has replay-frozen revision-wikitext and alternate literary-body identity: 442,656 characters / 825,899 bytes, SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`. Neither route is identified as FantLab input.
- **Running on Waves** — Detskaya literatura 1965 source-cited family with 35 chapters plus epilogue; literary subpage identities/composite remain unfrozen.
- **The White Guard** — Wikisource explicitly mixes two bibliographic source families across chapters 1–11 and 12–20; all 20 chapter identities/composite remain unfrozen.
- **The Twelve Chairs** — keep the 40-chapter later 1938/1961 editorial family distinct from the 41-chapter 1928 first standalone edition; neither literary body is frozen, and coauthorship prevents individual-author attribution without an explicit VOICE model.
- **The Life of Klim Samgin** — four exact Russian Wikisource parent revisions are replay-frozen at oldids `5733765`, `5198033`, `5138882`, `5724453`; ordered parent revision-wikitext identity SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`, totaling 3,228,790 parent wikitext characters / 5,902,920 UTF-8 bytes. Part 2's target dependency is replay-frozen at oldid `2366546`; merged PRs #111–#124 freeze the target-only `#lst`, inferred `poemx1`/Poem boundaries, parent structural surface and all thirteen plain literary values; merged PR #126 provides the candidate-specific fail-closed four-part extractor. Draft PR #127 now captures the independently replayed source-free literary-body identity: Part 1 964,215 chars / SHA `1a41cef4...`, Part 2 1,164,870 / `75896b6a...`, Part 3 680,940 / `7dc60303...`, Part 4 1,000,587 / `237b2119...`; ordered composite 3,810,618 chars / 6,958,930 bytes with raw and normalized SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`. The exact-head #127 replay already reproduced the committed manifest byte-for-byte before the final documentation/state commits. Evidence class remains candidate-specific inferred reconstruction; exact historical MediaWiki/Poem deployment and FantLab source identity remain unresolved.

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
- SCRIP-CORPUS-016 upgrades the public Hyperboloid entry to a frozen source-free literary-body identity with exact counts/digests and an explicit fail-closed extraction profile while preserving the unresolved print-edition and FantLab-input boundary.
- SCRIP-CORPUS-017/018 add and strengthen the standalone public Klim Samgin candidate page with exact per-part revision identities and an ordered revision-set digest while explicitly retaining the body-unfrozen and FantLab-unknown boundary.
- SCRIP-CORPUS-019 upgrades the Road to Nowhere public entry and provenance trace with a replay-frozen source-free alternate-body identity while explicitly leaving the retained primary Pravda-1965 family and FantLab-input identity unresolved.
- SCRIP-CORPUS-020 progressively exposed the Klim source graph and candidate-specific reconstruction layers through merged PR #126. Draft PR #127 now adds the verified source-free canonical literary-body manifest and updates the public candidate page with per-part/composite identities while explicitly labeling them `candidate_specific_inferred_reconstruction`; historical deployment and FantLab source equivalence remain unresolved.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories are diagnostic until their visible work-page relation is evidenced.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg lacks a Scriptorium-recorded PDF snapshot digest and deterministic OCR/page-extraction identity.
7. Hyperboloid has a frozen revision and deterministic frozen literary-body identity but no direct bibliographic print-edition identity and no FantLab analyzer-input match; Shining World, Running on Waves, White Guard and Twelve Chairs remain trace-only/unfrozen at the literary-body level.
8. Road to Nowhere has a frozen alternate revision/body identity, but the primary Pravda-1965 literary family remains unfrozen and no evidence ties either route to FantLab input.
9. Klim Samgin's candidate-specific extractor is merged and Draft PR #127 captures a source-free literary-body identity independently reproduced against the exact five-revision source graph. The exact historical Russian Wikisource MediaWiki-core and Poem deployment revisions remain unproven, and FantLab analyzer-input bytes/edition remain undisclosed; therefore neither historical render/parser-byte equivalence nor parity admissibility may be inferred from the successful replay.
10. Pages live activation remains a repository-admin effect and is off.
