# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 164
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-19T08:55:00Z
LAST_RESULT: SCRIP-CORPUS-027 / Issue #141 completed after independent review and repair of PR #142. Review of authored head `7a4afc6d0bc1b9f48b852637517c1923e1f610b4` found an acceptance-coverage gap: missing-page and redirect capture guards existed in implementation but were not directly exercised by tests despite Issue #141 requiring missing/redirect/drift coverage. Review repair added deterministic missing-page, redirect and unexpected-title capture tests without changing the frozen source manifest or provenance semantics. Final exact head `ba4d22a12bb3be2df72637e39a99215fa3c4a842` passed all 14 PR workflows; candidate-specific run `35433175579`, job `105871255330`, ran 279 tests, matched the live source-free 36-page inventory to the committed manifest, replayed every pinned revision and uploaded source-free artifact `10582210362` (`sha256:41df3264f4934dbe44780c1f27e4ad0c2fdff9a238c940cb4cf41bd215765bdb`). Pages run `35433175583` also passed canonical build and deterministic rebuild. PR #142 was marked Ready and squash-merged as `45ae261c03a18471d7798b1c083ab69fee8c4866`; Issue #141 closed completed.
LAST_VERIFIED_PROGRESS: `grin-running-on-waves-ru` now canonically has a source-free manifest for all 36 retained 1965-source literary page revisions. Route inventory and page-revision identity are frozen and replayable; literary-body extraction, composite counts/digests and FantLab analyzer-input/source-edition identity remain deliberately unfrozen/unknown. The distinct 1980/az.lib.ru `/Версия 2` route remains non-composable. M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-027
ISSUE:          #141 (closed completed)
STATUS:         COMPLETE
PR:             #142 (squash-merged)
MERGED_COMMIT:  45ae261c03a18471d7798b1c083ab69fee8c4866
NEXT_ACTION:    Resume normal-flow P2 corpus/provenance work. Add or strengthen a legally usable >=300k candidate,
                biasing toward diversity beyond 19th-century Russian classics where source identity and rights evidence are
                strong. Preserve translation/edition identity and do not promote FantLab/M2 status without exact source match.
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
- **Road to Nowhere** — the primary Pravda-1965/lib.web family is still body-unfrozen, but merged SCRIP-CORPUS-023 audits permanent index `oldid=4715367` as an incomplete/misdirected navigation surface: 8 labels map to 6 distinct targets, both Chapter IV labels duplicate Chapter III targets, and the three distinct Part II index targets currently resolve as red links. The distinct `az.lib.ru` route at `oldid=5585836` remains separately frozen at 442,656 characters / 825,899 bytes, SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`. Neither route is identified as FantLab input.
- **Running on Waves** — SCRIP-CORPUS-027 is complete. The retained Detskaya literatura 1965 Wikisource family has route topology frozen by category `oldid=4715419` and a source-free exact identity for all 36 expected literary pages (`/1`–`/35` plus `/Эпилог`) with page IDs, revision IDs, UTC timestamps and MediaWiki SHA-1 values plus deterministic pinned-revision replay. Literary-body extraction/composite identity remain unfrozen. Distinct `/Версия 2` at `oldid=5655654` declares `az.lib.ru` / Pravda 1980 and remains excluded. FantLab source match remains unknown.
- **The White Guard** — Wikisource mixes two bibliographic source families across chapters 1–11 and 12–20; all 20 chapter identities/composite remain unfrozen.
- **The Twelve Chairs** — keep the 40-chapter later 1938/1961 editorial family distinct from the 41-chapter 1928 first standalone edition; neither literary body is frozen, and coauthorship prevents individual-author attribution without an explicit VOICE model.
- **The Life of Klim Samgin** — SCRIP-CORPUS-020 is complete. Four exact parent revisions and the Part 2 dependency are replay-frozen; merged PRs #111–#124 freeze the target-only `#lst`, inferred `poemx1`/Poem boundaries, structural surface and all thirteen plain literary values; #126 merged the candidate-specific fail-closed extractor; #127 merged the canonical source-free per-part and composite literary-body identities; #128 reconciled the structured provenance trace. Exact historical MediaWiki/Poem deployment and FantLab analyzer-input/source-edition identity remain unresolved.
- **Children of Captain Grant — Beketova translation** — SCRIP-CORPUS-026 is complete. Merged PR #140 keeps exact Russian Wikisource revision `oldid=5304880` replay-frozen and adds candidate-specific `scriptorium-beketova-captain-grant-wikisource-body-v1`, freezing a 1,095,467-character / 2,040,240-byte literary body with raw and normalized SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`. Beketova / Detgiz 1955 / `az.lib.ru` bibliography and explicit source PD evidence covering the translation remain retained. The frozen body clears the >=300k rule for general calibration/profile use. No FantLab linguistic result or analyzer-input identity is established for this translation; M2 weight remains zero.

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
- Running on Waves now exposes in master a committed source-free 36-page exact revision manifest and dedicated candidate-page wording that distinguishes frozen route/page identities from still-unfrozen literary-body/composite identity and from the separate 1980/az.lib.ru route.
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
8. Running on Waves now has its 1965-route topology and all 36 literary page revisions frozen in master, but no deterministic literary-body extraction/composite identity yet; the separate 1980/az.lib.ru route remains non-composable.
9. Road to Nowhere's primary Pravda-1965/lib.web index is not a complete route witness: it contains duplicate/misdirected Chapter IV labels and current red links for all three distinct Part II targets exposed there. A complete same-family route set must be established independently before primary page/body freezing; the alternate az.lib.ru body cannot fill those gaps.
10. Several other twentieth-century candidates remain trace-only/unfrozen or bibliographically unresolved at the literary-body level.
11. Klim Samgin is fully frozen at the candidate-specific literary-body/provenance level, but exact historical Russian Wikisource MediaWiki-core/Poem deployment equivalence and FantLab analyzer-input bytes/edition remain unproven; these are evidence boundaries, not open acceptance criteria for closed Issue #109.
12. The Beketova *Children of Captain Grant* translation now has a frozen literary body large enough for general corpus admission, but no FantLab linguistic result/analyzer-input identity has been established for this translation; it cannot advance M2 until that evidence exists.
13. Pages live activation remains a repository-admin effect and is off.
