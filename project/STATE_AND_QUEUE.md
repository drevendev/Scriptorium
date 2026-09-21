# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 201
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-09-21T03:47:52Z
LAST_RESULT: SCRIP-CORPUS-046 / Issue #179 remains in recovery after independent review COMMENT `5262708679` found two acceptance/recoverability blockers in Draft PR #180: canonical `project/STATE_AND_QUEUE.md` had not recorded the open unit, and the canonical Darwin/Rachinsky candidate page still described merged PR #178 as Draft while omitting the new semantic-backlog artifact. This recovery unit repaired both surfaces on the PR branch: the candidate page now links/summarizes the source-free backlog and keeps every renderer/body/>=300k/FantLab/diagnostic/M2 gate closed, while canonical state now records SCRIP-CORPUS-046 / #179 / #180 as `REVIEW_PENDING`. The PR remains Draft; because the head changed, fresh exact-head checks must settle and a later independent review must re-read the repaired head before any Ready/merge decision.
LAST_VERIFIED_PROGRESS: The Draft PR contains a deterministic source-free unresolved-semantic backlog derived only after validating the reviewed Darwin/Rachinsky render-profile/source-surface boundary. It preserves all 43 unresolved shapes: 5 tag shapes / 518 tag tokens and 38 template shapes / 4,583 invocations, grouped into provider-template (37 shapes / 4,579 occurrences), provider-reference (3 / 466), provider-math (2 / 52), and inter-page (1 / 4) tracks. The mechanically selected next research target is template `ё`, arity 0/0, observed 2,227 times, but it remains explicitly unresolved. Canonical backlog SHA-256 is `4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2`. This is review-pending branch state, not merged capability. Renderer semantics/implementation/equivalence, inter-page composition, literary-body counts/digests, >=300k admission, FantLab source match, diagnostic readiness and M2 parity remain closed; M2 remains 0/5.

## Current unit

```text
UNIT_ID:        SCRIP-CORPUS-046
ISSUE:          #179 (open)
STATUS:         REVIEW_PENDING
PR:             #180 (Draft; recovery repair committed after review COMMENT 5262708679)
NEXT_ACTION:    Re-read the final repaired PR #180 head after all exact-head workflows settle. Independently verify the
                canonical candidate-page/state repairs plus the existing semantic-backlog implementation/artifact.
                If no blocker remains, mark Ready and merge in that later judgement run. Do not infer template `ё`,
                reference, math or inter-page semantics here; keep renderer/body/>=300k/FantLab/diagnostic/M2 gates closed.
```

## Current milestone gate

M0 is closed. M1 remains open. General, dialogue, vocabulary and punctuation metric families are executable inferred candidates. POS has two explicitly separated surfaces: the 17-bucket work-page-compatible `scriptorium-pos-v1` production candidate and a diagnostic-only broader methodology surface with five additional AOT-backed categories while runtime `N` noun/cardinal ambiguity remains unresolved.

No retained work has an independently established FantLab analyzer-input identity, so M2 remains open at **0/5 source-matched works**. Public-source freezing, bibliographic compatibility, count proximity and diagnostic resemblance do not advance M2.

## Queue

Evaluate rows in priority order. Recovery/review-ready work and failing required checks preempt normal selection.

| Priority | Unit | Mode | Deliverable | Gate / dependency |
| --- | --- | --- | --- | --- |
| P2 | SCRIP-CORPUS continuation | corpus / provenance | Add or strengthen legally usable >=300k candidates, prioritizing diversity beyond 19th-century Russian classics when licensing/source identity is strong enough; Petersburg's frozen scan and Darwin/Rachinsky's frozen source/surface/scan/profile identities make separate candidate-specific OCR/renderer units executable when selected | Preserve translation/edition identity and explicit legal provenance; renderer/OCR work must keep body/admission/FantLab/M2 gates closed until separately verified |

## Retained corpus / provenance status

Detailed evidence lives in `corpus/candidates/`, `benchmarks/`, `project/run-receipts/`, `project/CHANGELOG.md`, and `project/CHANGELOG.d/`; this state file keeps only the orientation-critical summary.

- **Anna Karenina** — frozen public-source candidate: 239 pinned chapter revisions; composite 1,705,605 characters; SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`; FantLab source match unknown.
- **Resurrection** — frozen public-source candidate: 129 pinned chapter revisions; composite 890,835 characters; SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`; FantLab source match unknown.
- **Brothers Karamazov** — frozen public-source candidate: 98 admitted revisions; composite 1,810,351 characters; SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`; FantLab source match unknown.
- **Silver Dove** — frozen single-revision public-source candidate at `oldid=5588003`; composite 563,125 characters; SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`; FantLab source match unknown.
- **Petersburg** — SCRIP-CORPUS-038 complete. Exact backing Commons PDF identity for the explicit 632-page 1916 first-book-edition facsimile is independently reviewed: 3,621,459 bytes, SHA-1 `682476934dd6ed49c6bbcdb0720127c1812ff477`, SHA-256 `b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`; the 1916 identity stays distinct from the 1922 revision. OCR/page selection, literary-body identity and >=300k admission remain unfrozen; FantLab source match unknown.
- **Hyperboloid of Engineer Garin** — frozen Russian Wikisource single-revision candidate at `oldid=5014458`; extraction profile `scriptorium-hyperboloid-wikisource-body-v1` reproduces 499,066 characters / 930,560 bytes with raw and normalized SHA-256 `a01c5eadef53b2437eff3abe6052bb7f7bf6f95737641558343363628da7f513`. Print-edition identity and FantLab source match remain unresolved.
- **Shining World** — the reviewed 1965-source Wikisource index advertises 34 chapter links but only 19 pages currently exist: Part I I-XVI and Part II I-III. Part II IV-XI and all Part III chapters are missing. Exact present-page revision identities are frozen; a complete literary body cannot be frozen from this route alone and FantLab source match is unknown.
- **Road to Nowhere** — the primary Pravda-1965/lib.web family remains body-unfrozen; permanent index `oldid=4715367` has 8 labels mapping to 6 targets, duplicate/misdirected Chapter IV labels, and current red links for all three distinct Part II targets. Distinct `az.lib.ru` route `oldid=5585836` remains separately frozen at 442,656 characters / 825,899 bytes, SHA-256 `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`. Neither route is identified as FantLab input.
- **Running on Waves** — SCRIP-CORPUS-028 complete. The Detskaya literatura 1965 family has exact source-free identities for all 36 literary pages and a fail-closed literary-body freeze: 363,819 characters / 656,239 UTF-8 bytes, raw and normalized SHA-256 `41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`. It clears the general >=300k rule. FantLab displays 360,987 characters, but source/analyzer-input match remains unknown and M2 weight is zero. Distinct `/Версия 2` at `oldid=5655654` declares `az.lib.ru` / Pravda 1980 and remains excluded.
- **The White Guard** — Wikisource mixes two bibliographic source families across chapters 1–11 and 12–20; all 20 chapter identities/composite remain unfrozen.
- **The Twelve Chairs** — SCRIP-CORPUS-044 complete. Master retains the independently reviewed parent route graph, all 410 exact Page dependency identities, exact backing Commons PDF identity (77,978,350 bytes; SHA-1 `4ab6aa42c3517169e99c1177b6fb6412cfe9187d`; SHA-256 `5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4`), four-gap audit/membership decision, exact-410 source-free markup inventory and fail-closed rendering profile. All 30 template shapes / 602 invocations and 410 `<references/>` remain semantically unresolved; inter-page composition, literary-body counts/digests, >=300k admission and FantLab source identity remain unresolved. The later 1938/1961 editorial family stays distinct; coauthorship prevents individual-author attribution without an explicit VOICE model.
- **The Life of Klim Samgin** — SCRIP-CORPUS-020 complete. Four exact parent revisions and Part 2 dependency are replay-frozen; merged PRs #111–#124 freeze target-only `#lst`, inferred `poemx1`/Poem boundaries, structural surface and thirteen plain literary values; #126 merged fail-closed extraction; #127 merged canonical source-free per-part/composite literary-body identities; #128 reconciled structured provenance. Exact historical MediaWiki/Poem deployment and FantLab analyzer-input/source-edition identity remain unresolved.
- **Children of Captain Grant — Beketova translation** — SCRIP-CORPUS-026 complete. `oldid=5304880` plus `scriptorium-beketova-captain-grant-wikisource-body-v1` freeze a 1,095,467-character / 2,040,240-byte literary body with raw and normalized SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`. Beketova / Detgiz 1955 / `az.lib.ru` bibliography and explicit source PD evidence are retained. It clears the >=300k general-corpus rule. No FantLab linguistic result/analyzer-input identity is established for this translation; M2 weight remains zero.
- **On the Origin of Species — Rachinsky translation** — SCRIP-CORPUS-045 is independently reviewed and complete on master. The current SCRIP-CORPUS-046 Draft PR adds a review-pending source-free semantic backlog over that frozen profile. Master retains 418 exact Page revision identities, reviewed 388-literary/30-apparatus composition contract, exact-388 source-free markup inventory, independently reviewed backing Commons DjVu identity (27,368,263 bytes; SHA-1 `75ef508588194ae74874272ce290f3ec1043ea9b`; SHA-256 `7f3ae1aadd4a844b193783a0c350e23815a76e7bb14a92bae7fa1c077354a2c8`) and the independently reviewed fail-closed render decision profile SHA-256 `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`. The review-pending backlog preserves all 43 unresolved shapes and mechanically selects template `ё` (2,227 invocations) as the next research target without resolving its semantics. Renderer implementation/equivalence, inter-page composition, literary-body count/digests and >=300k admission remain unfrozen; `admitted_for_calibration=false`. FantLab work 969964 currently exposes Timiryazev rather than Rachinsky; source match/M2 remain unknown/zero.

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
- Beketova exposes exact frozen literary-body identity and >=300k general-corpus admission while FantLab source match/M2 remain closed.
- Petersburg exposes its exact source-free 1916 PDF identity and 1916/1922 edition boundary while OCR/body/admission/FantLab gates remain open.
- Hyperboloid and Road to Nowhere expose frozen source-free alternate literary-body identities with explicit unresolved source-match boundaries; Road to Nowhere also exposes the primary-route defect instead of implying readiness.
- Shining World exposes the mismatch between 34 advertised links and 19 existing pages as an explicit blocker.
- Running on Waves exposes a frozen 363,819-character literary body while preserving the separate 1980 route and keeping FantLab source match/M2 closed.
- The Twelve Chairs exposes the independently reviewed fail-closed exact-surface rendering decision profile and unresolved template/reference counts without claiming renderer/body equivalence.
- The Darwin/Rachinsky canonical candidate page now exposes the review-pending source-free unresolved-semantic backlog, its four research tracks, canonical digest, and mechanically selected `ё` target while explicitly preserving every renderer/body/>=300k/FantLab/diagnostic/M2 gate as closed.
- Klim Samgin exposes the source graph, fail-closed extractor, canonical source-free per-part/composite literary-body identities and structured provenance; FantLab source match remains unknown.
- Live Pages deployment remains disabled behind `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true` plus repository Pages administration.

## Known risks / blockers

1. FantLab analyzer-input bytes/edition identity remain undisclosed for retained benchmark works; M2 remains 0/5.
2. FantLab corrective coefficients, parser details, word-boundary semantics, dash classifier and dialogue grammar/denominators remain partly unpublished.
3. FantLab dictionary/version, homonym selection/prediction and service-word aggregation remain unknown.
4. pylem runtime `N` loses noun/cardinal distinction; methodology-only categories are diagnostic until their visible work-page relation is evidenced.
5. Frozen public-source candidates remain unmatched to FantLab input and therefore cannot advance M2.
6. Petersburg has an exact 1916 Commons PDF byte identity, but deterministic literary-page/OCR extraction, literary-body count/digests and >=300k admission remain unfrozen; FantLab source identity is unknown.
7. Shining World's primary 1965-source family is incomplete: 15 of 34 advertised chapter targets are missing; a complete body needs a separately justified source-complete witness.
8. Running on Waves has a replay-frozen 363,819-character body, but FantLab analyzer-input/source-edition identity remains unknown; the separate 1980 route remains non-composable.
9. Road to Nowhere's primary Pravda-1965/lib.web index is not a complete route witness; a complete same-family route set must be established independently before primary page/body freezing and the alternate az.lib.ru body cannot fill those gaps.
10. Several other twentieth-century candidates remain trace-only/unfrozen or bibliographically unresolved at the literary-body level.
11. Klim Samgin is frozen at candidate-specific literary-body/provenance level, but exact historical MediaWiki-core/Poem deployment equivalence and FantLab analyzer-input bytes/edition remain unproven.
12. The Beketova *Children of Captain Grant* translation has a frozen >=300k literary body, but no FantLab linguistic result/analyzer-input identity for this translation; it cannot advance M2 yet.
13. The 1928 *Twelve Chairs* route has exact source-free dependencies/scan/gap/surface/profile evidence, but all 30 template shapes / 602 invocations and 410 `<references/>` tokens still require evidenced semantics; inter-page composition, body identity and FantLab source identity remain unresolved.
14. Darwin/Rachinsky 1864 has reviewed source-free 388/30 composition, exact-388 markup inventory, backing scan identity and fail-closed decision profile. Draft PR #180 now also carries a deterministic unresolved-semantic backlog, but all 43 shapes remain unresolved and the repaired head still requires fresh exact-head CI settlement plus independent review before merge; body count/digests and >=300k admission remain unresolved, and FantLab's current Russian translation surface is a different translation.
15. Pages live activation remains a repository-admin effect and is off.