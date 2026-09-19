# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 177
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-19T22:03:00Z
LAST_RESULT: SCRIP-CORPUS-034 / Issue #155 advanced in Draft PR #156. The already-frozen Darwin/Rachinsky 1864 topology was materialized into an exact source-free identity freeze for all 418 included Russian Wikisource Page dependencies. The first hosted capture attempt exposed HTTP 414 from 40-title Cyrillic GET batches; batching was reduced to 8 and repaired run `35471807464`, job `105973987426`, checked out exact head `db4d5657af3e13548324eb1a101bc6c13a7aa382`, ran 291 tests successfully and captured exactly 418 identities with MediaWiki `ids|timestamp|sha1` only. Artifact `10592834383` has ZIP SHA-256 `1fe9319448ea932a57c48378381e111cbcd6c7e8ca902d162aea1b93f675a014`; extracted verbose capture JSON SHA-256 is `8979500217049380826c2d8c304dd94dc214087e3c356c16f5779e559115b375`. The same identity tuples are committed source-free as four SHA-256-pinned shards plus an authoritative index, with deterministic exact-revision replay tooling/tests. PR #156 remains Draft for an independent exact-head review; this authored production wake did not self-approve or merge it.
LAST_VERIFIED_PROGRESS: `darwin-origin-species-rachinsky-1864-ru` now has authored provenance status `rendered_route_graph_proofreadpage_topology_and_418_page_revision_identities_frozen_literary_body_unfrozen` in Draft PR #156. Exact revision ID, timestamp and MediaWiki SHA-1 are frozen for all 418 included Page sequences; source-declared no-text sequences 114 and 411 remain excluded. No wikitext/OCR/rendered prose/scan bytes are committed. Independent scan bytes/SHA-256, candidate-specific fail-closed literary-body extraction/composition, body count/digests and >=300k admission remain unfrozen/false. FantLab still exposes Timiryazev rather than Rachinsky and M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-034
ISSUE:          #155 (open)
STATUS:         REVIEW_PENDING
PR:             #156 (Draft)
NEXT_ACTION:    Independently review PR #156 at its then-current exact head after required checks complete. Verify the
                committed four-shard 418-Page identity inventory, hosted exact-revision replay, source-free boundary and
                fail-closed downstream gates. Only then mark Ready/merge if safe; do not restart production on this unit.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility, count proximity and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P0 | SCRIP-CORPUS-034 / PR #156 | independent review / recovery | Resolve exact current head; inspect changed paths, hosted 418-Page replay and required checks; Ready/merge only if evidence supports it | Production and judgment separation; no self-approval from authored wake |
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
- **Road to Nowhere** — the primary Pravda-1965/lib.web family is still body-unfrozen, but merged SCRIP-CORPUS-023 audits permanent index `oldid=4715367` as an incomplete/misdirected navigation surface: 8 labels map to 6 distinct targets, both Chapter IV labels duplicate Chapter III targets, and the three distinct Part II index targets currently resolve as red links. The distinct `az.lib.ru` route at `oldid=5585836` remains separately frozen at 442,656 characters / 825,899 bytes, SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`. Neither route is identified as FantLab input.
- **Running on Waves** — SCRIP-CORPUS-028 is complete. The retained Detskaya literatura 1965 Wikisource family has route topology frozen by category `oldid=4715419`, exact source-free identities for all 36 literary pages, and a merged candidate-specific fail-closed literary-body freeze: 363,819 characters / 656,239 UTF-8 bytes, raw and normalized SHA-256 `41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`. It clears the general >=300k corpus rule. FantLab displays 360,987 characters, but source/analyzer-input match remains unknown and M2 weight remains zero. Distinct `/Версия 2` at `oldid=5655654` declares `az.lib.ru` / Pravda 1980 and remains excluded.
- **The White Guard** — Wikisource mixes two bibliographic source families across chapters 1–11 and 12–20; all 20 chapter identities/composite remain unfrozen.
- **The Twelve Chairs** — SCRIP-CORPUS-029 is complete. The distinct 41-chapter 1928 first-standalone family now has a merged source-free parent route graph: work index `oldid=5706135`, ProofreadPage index `oldid=5702510`, part parents `5702507` / `5704332` / `5702508`, and exact transclusion ranges 8–149, 152–313, and 316–421 totaling 410 Page dependencies. The 410 Page revision identities, PDF bytes and literary body remain unfrozen. The 40-chapter later 1938/1961 editorial family stays distinct; coauthorship prevents individual-author attribution without an explicit VOICE model.
- **The Life of Klim Samgin** — SCRIP-CORPUS-020 is complete. Four exact parent revisions and the Part 2 dependency are replay-frozen; merged PRs #111–#124 freeze the target-only `#lst`, inferred `poemx1`/Poem boundaries, structural surface and all thirteen plain literary values; #126 merged the candidate-specific fail-closed extractor; #127 merged the canonical source-free per-part and composite literary-body identities; #128 reconciled the structured provenance trace. Exact historical MediaWiki/Poem deployment and FantLab analyzer-input/source-edition identity remain unresolved.
- **Children of Captain Grant — Beketova translation** — SCRIP-CORPUS-026 is complete. Merged PR #140 keeps exact Russian Wikisource revision `oldid=5304880` replay-frozen and adds candidate-specific `scriptorium-beketova-captain-grant-wikisource-body-v1`, freezing a 1,095,467-character / 2,040,240-byte literary body with raw and normalized SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`. Beketova / Detgiz 1955 / `az.lib.ru` bibliography and explicit source PD evidence covering the translation remain retained. The frozen body clears the >=300k rule for general calibration/profile use. No FantLab linguistic result or analyzer-input identity is established for this translation; M2 weight remains zero.
- **On the Origin of Species — Rachinsky translation** — SCRIP-CORPUS-034 is review-pending in Draft PR #156. The merged SCRIP-CORPUS-033 topology still provides parent `oldid=5628021`, ProofreadPage index `oldid=4494408`, 15 rendered routes, shared route-template `oldid=3775868`, parent topology witness `oldid=5712882`, 399 route plus 19 parent dependencies and exact no-text exclusions 114/411. The Draft PR now freezes exact revision ID/timestamp/MediaWiki SHA-1 for all 418 included Page dependencies in four digest-pinned source-free shards with hosted replay. Literary-body extraction/composition, body count/digests, independent scan bytes/SHA-256 and >=300k admission remain unfrozen, so `admitted_for_calibration=false`. FantLab work 969964 currently exposes Timiryazev rather than Rachinsky; source match/M2 remain unknown/zero.

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
- `corpus/README.md` and the dedicated Beketova candidate page expose the translated candidate's exact frozen literary-body identity and >=300k general-corpus admission while explicitly keeping FantLab source match and M2 parity closed.
- Hyperboloid and Road to Nowhere expose frozen source-free alternate literary-body identities with explicit unresolved source-match boundaries; merged SCRIP-CORPUS-023 additionally makes the primary Road to Nowhere index-routing defect inspectable as source-free provenance rather than implying that the primary route is ready to freeze.
- Shining World exposes a merged inspectable source-free inventory artifact and corrected public/structured provenance that distinguish the 34 links advertised by the reviewed index from the 19 pages that actually exist; missing targets are visible blockers, not silently filled text.
- Running on Waves now exposes in master a source-free frozen literary-body identity and >=300k general-corpus admission while preserving the separate 1980/az.lib.ru route and keeping FantLab source match/M2 closed.
- Merged SCRIP-CORPUS-029 makes the 1928 *Twelve Chairs* parent route graph inspectable on the dedicated candidate page and in a machine-readable source-free manifest while explicitly keeping the 410 Page revisions and literary body unfrozen.
- Draft SCRIP-CORPUS-034 makes Darwin/Rachinsky's complete source-free 418-Page revision identity inventory inspectable as four SHA-256-pinned shards plus an authoritative index and public candidate explanation. No Page prose/scan bytes are published; literary-body >=300k and FantLab/M2 gates remain visibly closed pending independent review/merge.
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
8. Running on Waves now has a replay-frozen 363,819-character public literary body, but FantLab analyzer-input/source-edition identity remains unknown; the separate 1980/az.lib.ru route remains non-composable.
9. Road to Nowhere's primary Pravda-1965/lib.web index is not a complete route witness: it contains duplicate/misdirected Chapter IV labels and current red links for all three distinct Part II targets exposed there. A complete same-family route set must be established independently before primary page/body freezing; the alternate az.lib.ru body cannot fill those gaps.
10. Several other twentieth-century candidates remain trace-only/unfrozen or bibliographically unresolved at the literary-body level.
11. Klim Samgin is fully frozen at the candidate-specific literary-body/provenance level, but exact historical Russian Wikisource MediaWiki-core/Poem deployment equivalence and FantLab analyzer-input bytes/edition remain unproven; these are evidence boundaries, not open acceptance criteria for closed Issue #109.
12. The Beketova *Children of Captain Grant* translation now has a frozen literary body large enough for general corpus admission, but no FantLab linguistic result/analyzer-input identity has been established for this translation; it cannot advance M2 until that evidence exists.
13. The merged 1928 *Twelve Chairs* parent route graph leaves all 410 underlying Page-namespace revisions, the PDF byte stream, literary extraction/composition and body digests unfrozen; FantLab source identity remains unknown.
14. Darwin/Rachinsky 1864 now has an authored exact 418-Page revision-identity freeze in Draft PR #156, but the literary-body extraction/composition, body count/digests, independent scan-byte/SHA-256 identity and >=300k admission remain unresolved; FantLab's current Russian translation surface is a different translation. The PR must pass independent exact-head review before this authored identity freeze becomes canonical in master.
15. Pages live activation remains a repository-admin effect and is off.
