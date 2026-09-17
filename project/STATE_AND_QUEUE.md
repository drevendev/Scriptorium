# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 117
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-17T09:03:00Z
LAST_RESULT: SCRIP-CORPUS-020 / Issue #109 / draft PR #110 attempted to strengthen Klim Samgin from four pinned parent revisions toward a deterministic literary-body identity, but a source-free structural probe found that Part 2 oldid `5198033` contains an unversioned `#lst` dependency on `Жизнь Клима Самгина (Горький)/Часть 2/part2`. The run therefore stopped fail-closed at the correct prerequisite boundary, pinned that hidden dependency at exact oldid `2366546`, extended replay/tests/provenance, and explicitly did not claim a literary-body freeze. Issue #109 remains open for the later labeled-section/extraction/composition continuation; PR #110 is a prerequisite and remains Draft for independent review.
LAST_VERIFIED_PROGRESS: Substantive exact head `d4c055856f00bd06840b46fd5f9efcec91db32ed` passed Klim source-graph replay run `35202668027`, Scriptorium Pages run `35202668056`, and frozen diagnostic run `35202667999`. The Klim run passed 183 standard-library tests, re-captured/byte-compared/replayed all four parent revisions plus dependency oldid `2366546`, and source-free probing explicitly reported the Part 2 transclusion target. The dependency is page ID `580081`, timestamp `2016-11-29T05:49:23Z`, MediaWiki SHA-1 `899c3d348b8550486c2c6774b84bc3ff55495f43`, 583,889 wikitext characters / 1,058,733 UTF-8 bytes, SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`. No literary-body digest was created; FantLab source identity remains unknown and M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-020
ISSUE:          #109
STATUS:         REVIEW_PENDING_PREREQUISITE
PR:             #110 (Draft)
MERGED_COMMIT:  none
NEXT_ACTION:    Independently review the final head of draft PR #110.
                If clean, merge the source-graph prerequisite without closing Issue #109.
                Only after that may a later unit continue #109 by freezing exact #lst
                labeled-section selection/placement semantics, fail-closed per-part
                extraction and deterministic Part 1 -> 2 -> 3 -> 4 composition before
                recording raw or scriptorium-text-v1 composite body digests.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | Review PR #110 | independent review / recovery | Review final exact head of the Klim hidden-transclusion prerequisite; merge only if scope, fail-closed source-graph evidence and checks are clean | Do not self-approve authored substantive work; Issue #109 must remain open after prerequisite merge |
| P1 | SCRIP-CORPUS-020 continuation | corpus / provenance | After prerequisite merge, continue Issue #109 by freezing exact Part 2 `#lst` labeled-section semantics plus fail-closed four-part extraction/composition and source-free composite digests | Requires #110 merged; no body identity until complete source graph replays deterministically |
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
- **The Life of Klim Samgin** — four exact Russian Wikisource parent revisions are replay-frozen at oldids `5733765`, `5198033`, `5138882`, `5724453`; ordered parent revision-wikitext identity SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`, totaling 3,228,790 parent wikitext characters / 5,902,920 UTF-8 bytes. Source-free probing found Part 2's hidden `#lst` dependency and now pins its subpage at oldid `2366546`, wikitext SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`. Exact labeled-section semantics, literary-body extraction/composition and composite digests remain unfrozen; FantLab source identity remains unknown and main parity-catalog admission remains deferred.

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
- SCRIP-CORPUS-020 updates the standalone Klim page and machine-readable trace to expose the hidden Part 2 transclusion dependency and the stronger replay-frozen source-graph identity while explicitly refusing a premature literary-body or parity claim.
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
9. Klim Samgin's four parent revisions plus the discovered Part 2 transclusion dependency are replay-frozen, but exact `#lst` labeled-section selection/placement semantics, candidate-specific extraction/composition and composite raw/normalized body digests remain unfrozen; no body or FantLab-input identity may be inferred from the parent/dependency oldids alone.
10. Pages live activation remains a repository-admin effect and is off.
