# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 458
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-08
LAST_RESULT: #462 MERGED at bf5c8ac4a5dc5f4350c40b3d5a207ca74d7b76da; verified original-language facet shipped. Card-to-pair navigation proposed; live browser acceptance remains UNVERIFIED.
LAST_VERIFIED_PROGRESS: 11 measured / 2 leads; pinned Anna 239-revision replay retains seven source-bound independent word-boundary results; M2 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-014-CARD-TO-PAIR-v1
ISSUES: #283 (Reader usability; full visual acceptance remains open)
STATUS: PR_CANDIDATE; LATER_ACCEPTANCE_REQUIRED; CI_NOT_RUN
BRANCH: scrip-site-014-card-to-pair-20261108
BASE: bf5c8ac4a5dc5f4350c40b3d5a207ca74d7b76da

ACCEPTANCE: After pinned JSON verification, each of eleven measured cards offers a
44px+ keyboard-accessible comparison action that selects the clicked edition and
a distinct existing partner, with an available shared chart metric, canonical
pair permalink and focus/scroll to the results. The two unmeasured leads have
no comparison action. With disabled JavaScript or rejected JSON, static links
and tables remain intact. A real Node regression exercises the actual Reader
functions and pinned eleven-book evidence; hosted exact-head CI and independent
mobile/browser visual acceptance are separate.

## Next user-visible milestone and compact queue

Milestone: publicly readable Russian Reader with verified full-book diagnostics, accessible print/export and useful local analyzer.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 measured book card → live pair comparison | Verified-data-only 11-card navigation, nonduplicate partner, source-backed shared metric, permalink, accessible focus and no-JS fallback | Existing Reader & source-free snapshot; later exact-head CI/review |
| P2 | #285 live Reader route and responsive/print acceptance | HTTP route/asset checks, desktop/mobile/keyboard/print screenshots on actual deployed site | Browser network access currently blocked; not a prerequisite |
| P3 | #281 independent source/profile and displayed-rounding witness | Observe truly source-matched metric and published display policy; do not infer | FantLab analyzer-input identity currently unknown |
| P4 | Trusov translator body / #436 exact EOF fidelity | Legal >=300k measurement and source witness; separate bounded EOF correctness fix | Historical-render evidence |
| P5 | #284 code/data licensing and attribution | Evidence-backed code/data reuse terms only after owner approval | Rights-holder authorization |

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
