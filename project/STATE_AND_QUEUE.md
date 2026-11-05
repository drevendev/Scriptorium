# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 429
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-05
LAST_RESULT: #432 is confirmed MERGED at adb47e0f0a4d414e38a821a659aa3da484291876. Bounded read-only preflight for all 185 retained Paris Page oldids in a new PR; synthetic 5/5 PASS with mocked repository imports; hosted replay and full CI NOT_RUN at authorship.
LAST_VERIFIED_PROGRESS: Master holds 185 reviewed Page identities in SHA-pinned CSV. New Page-body preflight never commits prose, distinguishes accepted candidate pages and unsupported markup, and suppresses incomplete chapter digests. Neither historical render nor 300k admission/FantLab parity is established; M2 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-CORPUS-WHITE-GUARD-PARIS-PAGE-BODY-PREFLIGHT
ISSUES: follow-up to merged #432; source-free extraction experiment for retained 185 exact Page oldids
STATUS: PR_CANDIDATE; LOCAL_ISOLATED_SYNTHETIC_TESTS_5_PASS; FULL_LOCAL_TESTS_NOT_RUN; REAL_PROVIDER_REPLAY_NOT_RUN; EXACT_HEAD_CI_PENDING; LATER_ACCEPTANCE_REQUIRED
BRANCH: scrip-white-guard-paris-body-preflight-20261105
BASE: adb47e0f0a4d414e38a821a659aa3da484291876

ACCEPTANCE: Run exact-head read-only hosted workflow against 185 pinned Page identities with no raw wikitext in logs/artifacts. Inspect statuses and validate conservative per-page and all-or-nothing per-chapter candidate SHA-256/length. Check exceptions, noinclude/template/HTML exclusion, privacy and deterministic replay. This cannot establish historic ProofreadPage transclusion or corpus admission. See [Page body preflight](../docs/WHITE_GUARD_PARIS_BODY_PREFLIGHT.md).

## Next user-visible milestone and compact queue

Milestone: first honest comparison of two independently measured Russian translations of the same work; advance White Guard body readiness without treating an unmatched edition as FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Independently accept/revise Paris Page-body preflight PR | Exact head, full CI, 185 real oldids, only safe schema and meaningful candidate coverage; eligible later merge | New hosted replay may reveal unhandled Page markup |
| P2 | Refine versioned ProofreadPage renderer using actual preflight gaps | Evidence-backed boundary/page-join handling and a reproducible candidate 1927 literary body | Requires real Page observations and historical transclusion distinction |
| P3 | Second independently measured Russian Robinson Crusoe translation | Frozen distinct body, 29 measured fields, honest same-work comparison | Trusov historical renderer unresolved; independent user-facing slice preferred if unchanged blocked |
| P4 | #282/#281 AOT/FantLab metric readiness | Runtime N disambiguation or exact-source field evidence without parity overclaim | Native runtime/reference identity unresolved |
| P5 | #283/#285 Reader live Pages and desktop/mobile verification | HTTP, keyboard/focus and mobile screenshot readback | Browser navigation restrictions; preserve last valid publication |

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
