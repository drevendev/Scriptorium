# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 337
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-27
LAST_RESULT: PR #335 confirmed merged at 851269fe03e9ce6d39207713629f629f695d7c04. Proposed shareable per-edition links for the six measured root Pages books, preserving source fallbacks and navigation history.
LAST_VERIFIED_PROGRESS: Root Pages source has ten Russian-language titles with six measured works (129 numeric / 24 unavailable values). Generated Reader has merged Hyperboloid 29-row and Beketova 11-row routes. Root Pages now proposes direct edition-specific metric URLs with history/focus and safe invalid-ID fallback; live HTTP remains unverified. Five-source FantLab matrix retains four measured works and one pending source. M2 remains 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-ROOT-WORK-PERMALINK-012
ISSUES: #283 (reader navigation/accessibility), #285 (publication verification)
STATUS: AUTHORED_PENDING_EXACT_HEAD_CI_AND_LATER_ACCEPTANCE
BRANCH: scrip-site-024-book-deep-links
BASE: 851269fe03e9ce6d39207713629f629f695d7c04
ACCEPTANCE: Shareable same-origin `?book=<measured-key>#measurements` root Pages URLs resolve exactly one pinned measured edition; selection survives reload and browser history. Six book cards retain direct original source-JSON fallback for no-JS/modified clicks. Invalid/pending keys never request remote paths, create fabricated records or modify M2. Heading receives programmatic focus from in-page book navigation; permalink is keyboard accessible. Verify node-backed positive/negative routing tests, exact-head CI and independent later acceptance. No change to measured JSON, manifest M2, publishing interlocks or protected master.

## Next user-visible milestone and compact queue

Milestone: make the six-book Russian root Reading Room genuinely navigable and publicly verifiable, without conflating descriptive diagnostics with FantLab input-matched parity.

| Priority | Unit | Deliverable | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 root per-book permalinks | Exact-head CI, review findings and later qualifying merge of shareable edition routes | Authored semantic change requires later acceptance |
| P2 | #285 live Pages verification | Confirm branch-root Pages URL and assets, keyboard/responsive behavior when allowed | Browser/HTTP restrictions do not block independent code |
| P3 | Resurrection pinned-body replay | Remeasure 129 frozen revisions with versioned profile, retain source-free derived values | Legal and immutable source SHA checks; no parity |
| P4 | Road to Nowhere alternate candidate | Verify alternate complete body and retain separate measurements | Do not conflate with incomplete primary edition |
| P5 | #281 strict benchmark coverage/deltas | Expand inspectable source-matched eligibility report WITHOUT lowering M2 | Exact source-edition identity required for parity |

M2 remains **0/5**. New navigation does not establish an analyzer-input match or corpus admission. The existing hourly task is unchanged.

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
- #285 Pages: GitHub has_pages=true; branch master/root deployment succeeded at 6098ce58. The separate artifact-deploy workflow interlock remains unchanged. A newly authored root UI is PR_CREATED, not LIVE_VERIFIED until merged and publicly checked.
- #284 licensing: do not infer a code/data license or publish externally before the rights gate is resolved.
- Local checkout: Git DNS failed; exact source blobs were recovered and verified for actual local tests. Hosted full-repository CI supplies complete integrated execution evidence, not the limited local closure.
- Browser HTTP navigation returned ERR_BLOCKED_BY_ADMINISTRATOR. Current visual changes are VISUAL_NOT_VERIFIED; structural tests are not live browser acceptance. Continue other executable work without bypassing the restriction.
