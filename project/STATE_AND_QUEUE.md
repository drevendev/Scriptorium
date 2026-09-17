# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 119
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-17T11:08:00Z
LAST_RESULT: SCRIP-CORPUS-020 / Issue #109 advanced through draft PR #111. Exact-source replay corrected the earlier model of Part 2: the retained oldid `5198033` contains one target-only `#lst` call, not a labeled-section selection. A source-free contract now freezes its exact invocation/placement against dependency oldid `2366546` and binds the semantic branch to upstream `wikimedia/mediawiki-extensions-LabeledSectionTransclusion` evidence commit `3e9a44dec6858aeaf3ca547a32ab3162d6887ed6`, where zero remaining arguments return `newFrame->expand(root)`. The dependency contains six `poemx1` template invocations, so resolved Part 2 bytes/body remain deliberately unfrozen.
LAST_VERIFIED_PROGRESS: The source-free contract records one target argument, no section/range, parent offsets `581758..581810`, invocation SHA-256 `89969a0424eb9fa332d132216bbeb96647239ab613cf6dadf6c5e2087ff0f15e`, dependency oldid `2366546`, zero `<section>` tags, zero nested `#lst` calls, and six `poemx1` template invocations. Bootstrap exact-head Klim run `35213791952` passed the full standard-library suite, exact recapture/replay of all five pinned revisions, contract capture, source-graph verification, and source-free artifact upload. The finalized PR remains Draft pending independent exact-head review; FantLab source identity remains unknown and M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-020
ISSUE:          #109
STATUS:         TARGET_ONLY_LST_SEMANTICS_AUTHORED_REVIEW_PENDING
PR:             #111 (draft)
BASE_AT_SELECT: 0de8766941bff76e7b20fbd923cd2df95ffbb20b
NEXT_ACTION:    Independently review the current exact head of PR #111 and its fresh
                checks. If clean, merge the bounded target-only #lst semantic contract
                without closing Issue #109. After merge, continue #109 by freezing or
                deterministically reproducing the MediaWiki template-DOM expansion layer,
                starting with the six observed poemx1 invocations, before any resolved
                Part 2, literary-body, composite digest, or FantLab parity claim.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | Review PR #111 | recovery / review | Independently review current exact head of target-only Klim `#lst` contract; merge only if current checks/evidence are clean | Authored this run; no self-approval or merge |
| P1 | SCRIP-CORPUS-020 continuation | corpus / provenance | After #111 merge, freeze/reproduce the target-only MediaWiki template-DOM expansion layer (starting with six `poemx1` invocations), then fail-closed four-part extraction/composition and source-free composite digests | No resolved Part 2/body identity until parser/template dependencies replay deterministically |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough | Preserve translation/edition identity and explicit legal provenance |

## Retained corpus / provenance status

Detailed evidence lives in `corpus/candidates/`, `benchmarks/`, `project/run-receipts/`, `project/CHANGELOG.md`, and `project/CHANGELOG.d/`; this state file keeps only the orientation-critical summary.

- **Anna Karenina** — frozen public-source candidate: 239 pinned chapter revisions; composite 1,705,605 characters; SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; FantLab source match unknown.
- **Resurrection** — frozen public-source candidate: 129 pinned chapter revisions; composite 890,835 characters; SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`; FantLab source match unknown.
- **Brothers Karamazov** — frozen public-source candidate: 98 admitted revisions; composite 1,810,351 characters; SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`; FantLab source match unknown.
- **Silver Dove** — frozen single-revision public-source candidate at `oldid=5588003`; composite 563,125 characters; SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`; FantLab source match unknown.
- **Petersburg** — first-1916-edition facsimile lead; Commons description revision is pinned but PDF bytes/OCR identity are not; no binary/source match claim.
- **Hyperboloid of Engineer Garin** — frozen single-revision public-source candidate at Russian Wikisource `oldid=5014458`: page ID `1022517`, wikitext SHA-256 `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`; versioned `scriptorium-hyperboloid-wikisource-body-v1` extraction reproduces 499066 characters / 930560 bytes with raw and normalized SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`. Direct print-edition identity remains unresolved and FantLab source match is unknown.
- **Shining World** — 1965-source Wikisource family with 34 chapter subpages; chapter identities/composite remain unfrozen.
- **Road to Nowhere** — primary Pravda-1965 source family remains unfrozen. The distinct `az.lib.ru` single-page route at `oldid=5585836` now has replay-frozen revision-wikitext and literary-body identities under `scriptorium-road-nowhere-alt-wikisource-body-v1`: 442,656 characters / 825,899 bytes, raw and normalized SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`. FantLab displays 438,439 characters; the +4,217 delta is diagnostic-only. Neither route is identified as FantLab input.
- **Running on Waves** — Detskaya literatura 1965 source-cited family with 35 chapters plus epilogue; literary subpage identities/composite remain unfrozen.
- **The White Guard** — Wikisource explicitly mixes two bibliographic source families across chapters 1–11 and 12–20; all 20 chapter identities/composite remain unfrozen.
- **The Twelve Chairs** — keep 40-chapter later 1938/1961 editorial family distinct from 41-chapter 1928 first standalone edition; neither literary body is frozen, and coauthorship prevents individual-author attribution without an explicit VOICE model.
- **The Life of Klim Samgin** — four exact Russian Wikisource parent revisions are replay-frozen at oldids `5733765`, `5198033`, `5138882`, `5724453`; ordered parent revision-wikitext identity SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`, totaling 3,228,790 parent wikitext characters / 5,902,920 UTF-8 bytes. Part 2's target dependency is independently replay-frozen at oldid `2366546`, wikitext SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`. PR #111 freezes the exact target-only `#lst` invocation/placement and the upstream semantic branch that expands the whole target template DOM; the dependency contains six `poemx1` template invocations, so MediaWiki expansion, resolved Part 2 identity, literary extraction/composition and composite digests remain unfrozen. FantLab source identity remains unknown and main parity-catalog admission remains deferred.

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
- The repaired machine-readable candidate catalog agrees with the Hyperboloid trace/body manifests and no longer advertises the candidate as `traced_not_frozen`.
- SCRIP-CORPUS-017 adds the standalone public Klim Samgin candidate page and provenance trace.
- SCRIP-CORPUS-018 strengthens that page/trace with exact per-part revision identities and an ordered revision-set digest while explicitly retaining the body-unfrozen and FantLab-unknown boundary. It intentionally does not change the main parity catalog.
- SCRIP-CORPUS-019 upgrades the Road to Nowhere public entry and provenance trace with a replay-frozen source-free alternate-body identity while explicitly leaving the retained primary Pravda-1965 family and FantLab-input identity unresolved.
- SCRIP-CORPUS-020 first pinned the Klim Part 2 dependency, then PR #111 corrected the public explanation from "labeled-section selection" to the evidenced target-only `#lst` behavior and exposes the six-`poemx1` MediaWiki-expansion boundary without claiming resolved body bytes.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories are diagnostic until their visible work-page relation is evidenced.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg lacks a Scriptorium-recorded PDF snapshot digest and deterministic OCR/page-extraction identity.
7. Hyperboloid has a frozen revision and deterministic frozen literary-body identity but no direct bibliographic print-edition identity and no FantLab analyzer-input match; Shining World, Running on Waves, White Guard and Twelve Chairs remain trace-only/unfrozen at the literary-body level.
8. Road to Nowhere now has a frozen alternate revision and deterministic frozen alternate literary-body identity, but the primary Pravda-1965 literary family remains unfrozen and no evidence ties either route to FantLab input.
9. Klim Samgin's parent/dependency revisions and target-only `#lst` invocation semantics are now source-free frozen in PR #111, but MediaWiki template-DOM expansion is not reproduced; the dependency contains six `poemx1` invocations. Resolved Part 2 bytes, candidate-specific extraction/composition and composite raw/normalized body digests remain unfrozen; no body or FantLab-input identity may be inferred yet.
10. Pages live activation remains a repository-admin effect and is off.
