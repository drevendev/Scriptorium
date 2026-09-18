# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 142
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-18T07:53:00Z
LAST_RESULT: SCRIP-CORPUS-020 / Issue #109 / PR #123 received an independent later-run review of exact head `fb5e787027e9b156594bb217845652452d945017` with no blocking defect, was marked Ready, and was squash-merged as `c5b527f3390ae6aec5cfc3716d67da6af8311aa4`. The merged source-free prerequisite freezes the four-parent pre-extraction structural surface: direct parent `poemx1` inventory is 5 / 2 / 0 / 0, including two Part 2 calls at offsets `25519..25540` and `25568..26321` outside the frozen target-only `#lst` span `581758..581810`, so both survive target substitution. Literary-body extraction/composition, historical Russian Wikisource MediaWiki/Poem deployment equivalence and FantLab source identity remain unresolved.
LAST_VERIFIED_PROGRESS: Immediately before merge, PR #123 was mergeable, 9 commits ahead / 0 behind current master `78f168b86c6b7563a5f37f164b29234ddc4fc5f1`, with 8 changed files and no blocking review threads or prior submitted reviews. All 12 pull-request workflows on exact head `fb5e787027e9b156594bb217845652452d945017` completed successfully. Dedicated run `35317967589`, job `105513730940`, checked out the exact head and completed the standard-library suite, re-fetched all four pinned parent revisions, regenerated the source-free structural artifact and byte-compared it against the committed JSON successfully. The merged artifact stores structural names, counts, offsets and cryptographic identities only; no literary prose is committed. M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-020
ISSUE:          #109
STATUS:         BODY_EXTRACTION_SURFACE_MERGED_CONTINUATION_OPEN
PR:             #123 (merged)
MERGED_COMMIT:  c5b527f3390ae6aec5cfc3716d67da6af8311aa4
NEXT_ACTION:    Implement fail-closed literary extraction for Parts 1–4 against the frozen structural surface,
                explicitly handling all seven direct parent poemx1 calls and the inferred Part 2 target-substitution
                graph. Then define deterministic Part 1 -> 2 -> 3 -> 4 composition before recording source-free
                raw and `scriptorium-text-v1` composite-body digests.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-CORPUS-020 continuation | corpus / provenance | Define deterministic fail-closed literary extraction for Parts 1–4 against the merged structural surface and ordered 1 -> 2 -> 3 -> 4 composition, then freeze source-free raw and `scriptorium-text-v1` composite body identities | Part 2 target substitution and four-parent residual structural surface are merged as candidate-specific inferred prerequisites; historical Wikisource core/Poem deployment equivalence and FantLab source identity remain unproven |
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
- **The Life of Klim Samgin** — four exact Russian Wikisource parent revisions are replay-frozen at oldids `5733765`, `5198033`, `5138882`, `5724453`; ordered parent revision-wikitext identity SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`, totaling 3,228,790 parent wikitext characters / 5,902,920 UTF-8 bytes. Part 2's target dependency is replay-frozen at oldid `2366546`, and merged PRs #111–#122 freeze the target-only `#lst` semantics, inferred historical `poemx1` revision, inclusion controls, literal parameter surface, six dependency invocation bindings, reachable `#if`/`#ifeq` graph, exact dependency parameter-2 values, inferred Poem implementation anchor, reached one-content/zero-attribute `#tag:poem`, candidate-specific plain-value MediaWiki/Poem render surface, and the candidate-specific inferred target-only Part 2 source-graph resolution. Merged PR #123 additionally freezes the four-parent pre-extraction structural surface: direct parent `poemx1` counts 5 / 2 / 0 / 0, including two direct Part 2 calls outside the `#lst` substitution span. The expanded dependency remains 585,113 characters / 1,059,957 bytes with SHA-256 `a027dfe0d867572f3802050fcfd72b07a43fa6efe539d58035b3af59f49a04d4`; exact target-only substitution yields a resolved parent Part 2 reconstruction of 1,166,949 characters / 2,114,262 bytes with SHA-256 `ab45577f567ce504e24936f73fcdff261780168414e4bccc04bbf8927299d016`. Exact historical MediaWiki/Poem deployment, literary extraction/composition and FantLab source identity remain unresolved.

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
- SCRIP-CORPUS-020 progressively exposed the Klim Part 2 dependency, exact target-only `#lst`, inferred `poemx1` anchor, post-inclusion dependency and parameter surfaces, concrete dependency invocation bindings, control reachability, exact parameter-2 surface, inferred Poem implementation anchor, reached extension-call shape, bounded render surface, merged candidate-specific target-only Part 2 source-graph identities, and now merged PR #123's four-parent extraction-prerequisite surface. The public page explicitly warns that two direct Part 2 parent `poemx1` calls survive target substitution. Literary-body extraction/composition and historical deployment equivalence remain explicit unresolved boundaries.
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
9. Klim Samgin's target-only Part 2 source-graph expansion is merged source-free in PR #122, and merged PR #123 now freezes the residual four-parent structural surface, including seven direct parent-level `poemx1` calls and the two Part 2 calls that sit outside and survive the `#lst` substitution span. The exact historical Russian Wikisource MediaWiki-core and Poem deployment revisions remain unproven, so historical render or parser-byte equivalence must not be inferred. The resolved Part 2 identity remains inferred target-substitution/source-graph evidence, not a literary-body identity; per-part fail-closed extraction must explicitly handle the frozen structural surface before deterministic four-part composition and composite raw/normalized body digests can be claimed.
10. Pages live activation remains a repository-admin effect and is off.
