# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 426
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-05
LAST_RESULT: PR #429 merged at b53cce9a123051a7f10f281823a7bf02a9872014 with safe structural diagnostics and privacy regression fixes; this candidate makes pinned Paris <pages /> ranges explicitly inspectable without claiming Page content or modifying extraction.
LAST_VERIFIED_PROGRESS: Master b53cce9a123051a7f10f281823a7bf02a9872014 includes merged #429. Previous pinned historical replay: Paris 1927 11 UNSUPPORTED_INLINE_MARKUP, Moscow 1989 4 UNSUPPORTED_TEMPLATE + 5 tentative; complete mixed-source size null. The current Paris chapter 1 edit view shows a ProofreadPage <pages /> transclusion (not historical-oldid proof); hosted exact-head v3 plan replay NOT_RUN. Reader: 11 measured Russian editions, 13 catalogue cards, 298 fields (249 numeric, 49 unavailable). Live browser/mobile NOT_VERIFIED; M2 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-CORPUS-WHITE-GUARD-PROOFREADPAGE-RANGE-PLAN
ISSUES: follow-up to merged #429; Paris 1927 currently transcludes unpinned Page-namespace source rather than embedding literal prose
STATUS: PR_CANDIDATE; PINNED_20_REPLAY_INITIAL_HEAD_SUCCESS; PARIS_11_ROUTE_PLANS_VERIFIED_185_PAGES; FULL_FINAL_HEAD_CI_PENDING; LATER_ACCEPTANCE_REQUIRED
BRANCH: scrip-white-guard-proofreadpage-range-plan-20261105
BASE: b53cce9a123051a7f10f281823a7bf02a9872014

ACCEPTANCE: Preserve conservative v1 extraction semantics and no-source-prose receipts. Expose only narrow source-family-matched <pages /> index/from/to spans as UNFROZEN dependencies in v3, reject unapproved/complex routes, keep mixed-edition/composite/admission gates closed. Hosted replay must validate exact 20 revisions and prove actual non-prose route coverage before any Page dependency freeze is claimed. See [preflight contract](../docs/WHITE_GUARD_BODY_PREFLIGHT.md).

## Next user-visible milestone and compact queue

Milestone: first honest comparison of two independently measured Russian translations of the same work; advance White Guard body readiness without treating an unmatched edition as FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | White Guard ProofreadPage route-plan preview (this PR) | Exact-head hosted 20-revision v3 receipt, no raw prose, unpinned Page spans only when exact-safe; targeted negative tests | Historic source must actually match route whitelist; current edit view is not oldid evidence |
| P2 | Resolve Paris 1927 Page dependency set | Bind Page: oldids/SHA-1 for accepted routes, then test separate renderer on frozen content | No live transclusion shortcut; preserve 1927/1989 partitions and body/parity unknowns |
| P3 | Second independently measured Russian Robinson Crusoe translation | Freeze distinct literary body, run 29 metrics, truthful same-work comparison | Trusov historical renderer unresolved; select independent work if unchanged blocked |
| P4 | #282/#281 AOT/FantLab compatibility or source-bound metric readiness | Native N disambiguation or exact-source field evidence without parity overclaim | Native runtime/reference identity unresolved |
| P5 | #283/#285 Reader live Pages, desktop/mobile verification | HTTP, keyboard/focus and mobile screenshots | Browser navigation previously restricted; preserve last publication |

## Retained evidence and scientific gates

Immutable detail remains in `corpus/candidates/`, `benchmarks/`, `showcase/`,
`project/run-receipts/`, `project/CHANGELOG.md` and `CHANGELOG.d/`. Reread the relevant
candidate records before acting; this delivery does not recalculate, admit or relabel works.

- Anna Karenina: 239 pinned revisions, 1,705,605 characters; source identity unknown.
- Resurrection: 129 revisions, 890,835 characters; source identity unknown.
- Brothers Karamazov: 98 admitted revisions, 1,810,351 characters; source identity unknown.
- Silver Dove: 563,125 characters; source identity unknown.
- Hyperboloid: frozen 499,066-character body and source-free measured CI receipt (24 actual / 5 NOT_RUN); root Reader retention verified in master; print/FantLab identity unresolved.
- Running on Waves: frozen 363,819-character body and diagnostics; denominator resemblance is hypothesis only.
- Children of Captain Grant / Alexandra A. Beketova: frozen 1,095,467-character Russian translation and 11 measured derived fields; distinct from French original/other translations, no FantLab result/input identity.
- Aelita and We: published FantLab inputs are below 300k; zero M2 weight. We's public body remains separately unfrozen.
- Petersburg: exact 632-page 1916 PDF and OCR/body contract; literary selection, body, size and identity gates remain open.
- Shining World is incomplete; Road to Nowhere has 442,656 frozen alternate characters and 24 measured plus 5 NOT_RUN rows (Reader merged, FantLab input identity UNKNOWN); White Guard mixes source families and has 20 captured/replayed identity rows adopted by merged #422, not a measured body; Twelve Chairs retains unresolved template/body semantics; Klim Samgin retains unresolved historical-renderer/FantLab equivalence.
- Darwin/Rachinsky: SCRIP-CORPUS-078 through 084 retain zero-argument yo, references containment, VAR documentation/provider drift and six-revision identity evidence, not full historical replay/body/parity. Effective unresolved surface remains 4 tag shapes/130 tokens and 37 template shapes/2,356 invocations.
- Perelman 1913: SCRIP-CORPUS-085 exact-PDF anchors include carrier 60 without a directly visible folio. Sampled +9 compatibility cannot establish total/global mapping, PDF/DjVu equivalence, OCR/body/size or FantLab identity. Do not interpolate missing folios arithmetically.

M0 is closed; M1 remains open. General/dialogue/vocabulary/punctuation metric families are
executable inferred candidates. POS has separate work-page-compatible and diagnostic-only
surfaces. `pylem==0.0.18` remains pinned; runtime N noun/cardinal ambiguity is unresolved.
FantLab dictionary/version, homonym selection, word boundaries, service-word aggregation,
corrective coefficients and some dialogue/denominator semantics remain unknown. The Anna
word gap and dash-rate parity are unresolved; punctuation-v2's internal-hyphen correction
is not new evidence of parity.

M2 stays **0/5**: five independent legally usable works >=300,000 characters including
spaces, established source edition/analyzer-input identity, required published compatible
metrics after displayed rounding, and explicit unchanged equality/tolerance rules. Unmatched
comparisons remain diagnostic. Unknown is not zero, NOT_RUN is not PASS. M3/M4/M5 retain their
own manifest gates. Short excerpts/fixtures do not count as corpus admission.

## Scoped operational blockers

- #265: default-branch rules prevent deletion/non-fast-forward and require PRs, with zero required approvals in the read ruleset. Connector identity has push/triage, not admin. No unsupported deletion/settings mutation or ref bypass.
- #285 Pages: #360 is merged into master. Live HTTP and desktop/mobile visual verification remain blocked/unverified despite earlier successful root deployments. Do not infer current LIVE_VERIFIED from CI.
- #284 licensing: do not infer a code/data license or publish externally before the rights gate is resolved.
- MediaWiki transient-readback: the earlier Klim Samgin exact-source CI failed once with `MediaWiki response missing query` and a fresh rerun succeeded. The response body was not retained, so its precise cause is UNKNOWN. #424 handles only independently documented transient signals, not a claimed reproduction of that historical cause.
- Local checkout: Git DNS failed in this environment. Five production module blobs and the existing single-page test blob were recovered and SHA-verified. Forty-five local tests exercise the real modules with synthetic responses and mocked transport/sleep. The full repository suite and actual provider replay are separate hosted-CI evidence, not the local subset.
- Browser HTTP navigation previously returned ERR_BLOCKED_BY_ADMINISTRATOR. This batch has no UI change and makes no new browser/live verification claim. Do not bypass the restriction.
