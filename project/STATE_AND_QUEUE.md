# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 347
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-28
LAST_RESULT: PR #346 merged (5891163130bb2f1afea82bd9a045e0e12548c99b); chart print exact-value lifecycle authored for later acceptance.
LAST_VERIFIED_PROGRESS: Seven measured Russian editions in master (7/10; 182 fields, 153 numeric and 29 unavailable). Retained FantLab matrix: 142 rows, including 29 supplemental source-unmatched Resurrection rows. Branch Pages build AND deploy completed successfully on master 0ca6c30d (GitHub Actions #40719281314); public HTTP/browser still LIVE_NOT_VERIFIED / VISUAL_NOT_VERIFIED. M2 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-012-PRINT-CHART-022
ISSUES: #283 (accessible/print charts), #285 (Pages)
STATUS: AUTHORED_PENDING_LATER_ACCEPTANCE
BRANCH: scrip-site-012-print-chart-exact-table
BASE: 5891163130bb2f1afea82bd9a045e0e12548c99b
ACCEPTANCE: Printing the currently selected one of eight Russian chart metrics
temporarily opens its exact-value table, preserves full numeric precision and
missing-vs-zero status in monochrome, and restores the previous disclosure state.
Works on the static source-backed default chart if the JSON fetch fails, with
independent positive/negative print-event regression. No book text or parity changes.
VISUAL_NOT_VERIFIED until desktop/mobile browser print preview can be inspected.

## Next user-visible milestone and compact queue

Milestone: review/merge print-readable exact chart values, then verify real
branch Pages HTML/JSON and browser keyboard/mobile/print flows.

| Priority | Unit | Deliverable | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 chart print lifecycle | Later exact-head CI, independent acceptance and qualifying merge | Same-wake authorship excludes merge |
| P2 | #285 live Pages verification | Check merged page, JSON/CSV, keyboard/mobile/print behavior | HTTP/browser execution unavailable in prior wakes |
| P3 | #281 FantLab matrix | New field-level source/rounding diagnostic on already frozen books | Exact FantLab edition remains UNKNOWN |
| P4 | #282 pinned AOT/pylem | Quantify N noun/cardinal impact without unsupported mapping | Native category ambiguity unresolved |
| P5 | Road to Nowhere alternate | Analyze independently frozen Russian edition without overstating parity | Primary source transcription incomplete |

M2 stays **0/5**. Source text is not published. Existing hourly schedule unchanged.

## Retained evidence and scientific gates

Immutable detail remains in `corpus/candidates/`, `benchmarks/`, `showcase/`,
`project/run-receipts/`, `project/CHANGELOG.md` and `CHANGELOG.d/`. Reread the relevant
candidate records before acting; this delivery does not recalculate, admit or relabel works.

- Anna Karenina: 239 pinned revisions, 1,705,605 characters; source identity unknown.
- Resurrection: 129 revisions, 890,835 characters; source identity unknown.
- Brothers Karamazov: 98 admitted revisions, 1,810,351 characters; source identity unknown.
- Silver Dove: 563,125 characters; source identity unknown.
- Hyperboloid: frozen 499,066-character body and source-free measured CI receipt (24 actual / 5 NOT_RUN); future generated Reader retention still pending; print/FantLab identity unresolved.
- Running on Waves: frozen 363,819-character body and diagnostics; denominator resemblance is hypothesis only.
- Children of Captain Grant / Alexandra A. Beketova: frozen 1,095,467-character Russian translation and 11 measured derived fields; distinct from French original/other translations, no FantLab result/input identity.
- Aelita and We: published FantLab inputs are below 300k; zero M2 weight. We's public body remains separately unfrozen.
- Petersburg: exact 632-page 1916 PDF and OCR/body contract; literary selection, body, size and identity gates remain open.
- Shining World is incomplete; Road to Nowhere has a >=300k alternate frozen route but no FantLab identity; White Guard mixes source families; Twelve Chairs retains unresolved template/body semantics; Klim Samgin retains unresolved historical-renderer/FantLab equivalence.
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
- #285 Pages: branch master/root deploy succeeded on 6ba4b1bc (pages build and deployment #40572592825); proposed comparison URLs are not deployed/LIVE_VERIFIED without later merge, deployment and HTTP readback.
- #284 licensing: do not infer a code/data license or publish externally before the rights gate is resolved.
- Local checkout: Git DNS failed; exact source blobs were recovered and verified for actual local tests. Hosted full-repository CI supplies complete integrated execution evidence, not the limited local closure.
- Browser HTTP navigation returned ERR_BLOCKED_BY_ADMINISTRATOR. Current visual changes are VISUAL_NOT_VERIFIED; structural tests are not live browser acceptance. Continue other executable work without bypassing the restriction.
