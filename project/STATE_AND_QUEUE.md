# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 123
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-17T14:55:00Z
LAST_RESULT: SCRIP-CORPUS-020 / Issue #109 / draft PR #113 authored a bounded MediaWiki partial-transclusion prerequisite for pinned `Шаблон:Poemx1` oldid `5142743`. The new source-free profile applies documented `noinclude` / `includeonly` / `onlyinclude` selection semantics. Exact replay showed that this removes both the raw `doc` invocation and the raw `PAGENAME` occurrence from the effective transclusion graph. The remaining unresolved classes are parser functions `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, and `#tag` x1 targeting `poem`; there are no ordinary template transclusions or remaining magic words. Historical render equivalence, parameter/frame expansion, parser-function expansion, extension-tag rendering, resolved Part 2 bytes and literary-body digests remain explicitly unproven/unfrozen.
LAST_VERIFIED_PROGRESS: The bounded implementation passed 198 standard-library tests on exact PR head `087771d0449698a22a422255d75c409c061fd553`. Dedicated workflow `35237044297` also re-resolved oldid `5142743`, regenerated the raw shape and applied the inclusion profile successfully. Its final byte comparison then correctly failed because the first hand-authored post-inclusion artifact had incorrectly retained raw `PAGENAME`; the live generated artifact proved that occurrence is inside excluded content. The committed artifact and public/durable wording were repaired from that exact replay evidence. A fresh exact-head rerun is required before independent review/merge. No FantLab source identity was promoted and M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-020
ISSUE:          #109
STATUS:         POEMX1_INCLUSION_AUTHORED_REVIEW_PENDING
PR:             #113 (draft)
NEXT_ACTION:    Independently review the final exact head of PR #113 and its GitHub checks. If clean,
                merge this bounded inclusion-semantics prerequisite without closing Issue #109.
                Then continue with only the evidenced unresolved MediaWiki layer: template parameter/frame
                behavior, #expr/#if/#ifeq/#iferror, and #tag:poem. Do not infer historical render
                equivalence or resolved Part 2 bytes until that expansion replays deterministically.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | Review PR #113 | recovery / review | Independently inspect exact-head diff and checks; merge only if the frozen inclusion-semantics artifact is reproduced byte-for-byte and the uncertainty boundary is intact | Do not self-approve the authored substantive change |
| P0 | SCRIP-CORPUS-020 continuation | corpus / provenance | After PR #113 resolution, reproduce only evidenced template parameter/frame, `#expr` / `#if` / `#ifeq` / `#iferror`, and `#tag:poem` behavior needed by pinned `poemx1`, then continue toward resolved Part 2 and fail-closed four-part extraction/composition | Historical template revision remains an inferred as-of anchor; no render equivalence may be assumed |
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
- **The Life of Klim Samgin** — four exact Russian Wikisource parent revisions are replay-frozen at oldids `5733765`, `5198033`, `5138882`, `5724453`; ordered parent revision-wikitext identity SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`, totaling 3,228,790 parent wikitext characters / 5,902,920 UTF-8 bytes. Part 2's target dependency is independently replay-frozen at oldid `2366546`, wikitext SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`; merged PR #111 freezes the exact target-only `#lst` invocation/placement and upstream full-target-template-DOM semantic branch. Merged PR #112 freezes the deterministic as-of reconstruction identity for `Шаблон:Poemx1` at oldid `5142743`, wikitext SHA-256 `fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`, explicitly without claiming historical render equivalence. Draft PR #113 now applies the documented partial-transclusion control layer: oldid `5142743` has two `noinclude` pairs, one `includeonly` pair and no `onlyinclude`; after that selection the raw `doc` template dependency and raw `PAGENAME` occurrence both disappear. The frozen remaining graph is parser functions `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, `#tag` x1 targeting `poem`, with no ordinary template transclusion and no remaining magic word. Parameter/frame/parser/extension expansion, resolved Part 2 identity, literary extraction/composition and composite digests remain unfrozen. FantLab source identity remains unknown and main parity-catalog admission remains deferred.

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
- SCRIP-CORPUS-020 first pinned the Klim Part 2 dependency, PR #111 corrected the public explanation to target-only `#lst`, PR #112 exposed the exact source-free `poemx1` as-of anchor, and draft PR #113 now exposes the post-inclusion effective dependency boundary while keeping parser expansion and historical render equivalence explicitly unresolved.
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
9. Klim Samgin's parent/dependency revisions, target-only `#lst` semantics and inferred historical `poemx1` revision are frozen. Draft PR #113 narrows the next layer further by freezing partial-transclusion controls and showing no remaining ordinary-template or magic-word dependency after excluded content is removed. The unresolved historical layer is now template parameter/frame behavior plus `#expr`, `#if`, `#ifeq`, `#iferror`, and `#tag:poem` semantics. Resolved Part 2 bytes, candidate-specific extraction/composition and composite raw/normalized body digests remain unfrozen; no historical render or FantLab-input identity may be inferred yet.
10. Pages live activation remains a repository-admin effect and is off.
