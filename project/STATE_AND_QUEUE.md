# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 428
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-05
LAST_RESULT: PR #431 merged at 2240b3aea8d1cc34d8d715c83a562dea86dd7c88; the 185/185 exact-current-Page capture from Actions #41959859796 was independently downloaded, hash-checked and prepared as a durable reviewed CSV plus offline/online replay verifier.
LAST_VERIFIED_PROGRESS: Master 2240b3aea8d1cc34d8d715c83a562dea86dd7c88 includes merged #431. Hosted capture replayed all 185 current Paris Page oldids; metadata receipt SHA-256 baf64a30cad23740dd0a6a1d51599f6bb7343f99922cf87efcd658f08042dc0f. This PR proposes 185 retained metadata rows, not a historical transclusion or literary body. Reader 11 measured Russian editions / 13 cards; live visual NOT_VERIFIED; M2 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-CORPUS-WHITE-GUARD-PARIS-PAGE-MANIFEST-ADOPTION
ISSUES: follow-up to merged #431; independently retain reviewed 185 Page revision IDs/SHA-1 and test offline + provider replay
STATUS: PR_CANDIDATE; LOCAL_STUBBED_IMPORT_TESTS_5_PASS; HOSTED_FULL_TESTS_NOT_RUN; FRESH_PROVIDER_REPLAY_NOT_RUN; LATER_ACCEPTANCE_REQUIRED
BRANCH: scrip-white-guard-paris-page-manifest-adoption-20261105
BASE: 2240b3aea8d1cc34d8d715c83a562dea86dd7c88

ACCEPTANCE: Independently inspect 185 metadata-only rows from successful workflow #41959859796 against checked-in CSV SHA-256 f2f2ea90a65ffb99b5cd12e64f20c15f16f6a2d7ca600cd7084488f311f81c02. Offline strict shape/topology/hash validation, exact-oldid metadata replay command, privacy/negative regressions and exact-head CI; do not claim an atomic historical transclusion. See [retained Page manifest](../docs/WHITE_GUARD_PARIS_FROZEN_PAGES.md).

## Next user-visible milestone and compact queue

Milestone: first honest comparison of two independently measured Russian translations of the same work; advance White Guard body readiness without treating an unmatched edition as FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Adopt reviewed Paris Page revision inventory (this PR) | 185 exact-current Page oldids/SHA-1 retained, hash-guarded, source-free offline and fresh-replay checks | Independent exact-head CI and later merge; neither historical transclusion nor book body is established |
| P2 | Implement bounded, versioned ProofreadPage body renderer | Replay retained 185 oldids; conservative page header/footer handling, real safe extraction experiment with no prose in artifacts | Requires accepted Page manifest and explicit rights/edition semantics; retain 1927/1989 split |
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
