# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 430
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-05
LAST_RESULT: #433 is MERGED at 9c647ada25ad1390774deb3ba722633a0a4e38c1. Reader catalogue sorting by Russian title or source-backed dialogue share is authored in a focused branch; same-run merge forbidden, exact-head hosted CI and desktop/mobile browser verification NOT_RUN.
LAST_VERIFIED_PROGRESS: The branch-root Reader has 11 independently measured Russian-language editions and two correctly marked research leads. The catalogue feature operates only on validated source-free derived results, preserves no-JavaScript ordering and keeps unavailable values after measured values. FantLab input identity remains UNKNOWN; M2 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-CATALOG-MEASURED-SORT
ISSUES: #283 — literary Reader discoverability/accessibility
STATUS: PR_CANDIDATE; V8_SORT_LOGIC_CHECK_PASS; HOSTED_CI_NOT_RUN; VISUAL_NOT_VERIFIED; LATER_ACCEPTANCE_REQUIRED
BRANCH: scrip-site-reader-catalog-metric-sort-20261105
BASE: 9c647ada25ad1390774deb3ba722633a0a4e38c1

ACCEPTANCE: Exact-head full Python/Node CI, real eleven-work sorting behavior by title and measured dialogue rate, missing-last and numeric-zero preservation, original no-JS static fallback, matched visual and keyboard DOM order, robust failure without fabricated measurements. No new source text or scientific metric values. Later independent review/merge, and separate branch Pages LIVE_VERIFIED/desktop-mobile checks.

## Next user-visible milestone and compact queue

Milestone: first honest comparison of two independently measured Russian translations of the same work, while making available edition measurements discoverable and useful on the public Reader.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Accept/revise measured catalogue sort in existing branch/PR | Real 13-card source-backed title/dialogue ordering, CI, keyboard/order verification | Later fresh acceptance; optional visual verification |
| P2 | Independently measure the Trusov *Robinson Crusoe* first-book body | Frozen exact body, ≥300k/edition rights verification, 29 fields and honest Shishmareva pair | Historical ProofreadPage/rendering and coverage |
| P3 | #282/#281 AOT/FantLab metric readiness | Measured runtime N disambiguation or explicit field-level evidence; no parity overclaim | Exact provider/reference input identity |
| P4 | #283/#285 Reader live Pages and desktop/mobile verification | Root branch Reader HTTP, keyboard/focus and mobile screenshot readback | Browser navigation restrictions; preserve last valid publication |
| P5 | Paris ProofreadPage renderer after merged #433 | Source-free real markup classification, reproducible candidate chapter boundaries | 183 unsupported Page markup; historic transclusion separate |

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
