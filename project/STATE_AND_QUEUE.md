# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 338
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-27
LAST_RESULT: PR #336 verified merged at 6ba4b1bcdac31af6d04d11d19ef5adf3e4f8504c. Proposed history-aware, shareable two-edition comparison URLs for root Pages.
LAST_VERIFIED_PROGRESS: Root Pages source has 10 Russian-language titles, six measured works (129 numeric / 24 unavailable values). Per-book links #336 are merged, master Pages build #40572592825 succeeded. This work proposes safe two-book pair URLs; public HTTP remains unverified. Generated Reader retains Hyperboloid and Beketova reports. M2 remains 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-ROOT-PAIR-PERMALINK-013
ISSUES: #283 (navigation/accessibility), #285 (publication verification)
STATUS: AUTHORED_PENDING_EXACT_HEAD_CI_AND_LATER_ACCEPTANCE
BRANCH: scrip-site-025-pair-permalinks
BASE: 6ba4b1bcdac31af6d04d11d19ef5adf3e4f8504c
ACCEPTANCE: Valid `?left=<measured-key>&right=<distinct-measured-key>#pairs` URLs select exactly two pinned Russian measured editions, preserve selector history/reload/back-forward and display an accessible share link. Invalid/pending/partial/duplicate URL pairs safely fall back to two distinct measured defaults. Duplicate UI selectors display an error and hide a stale link; no untrusted URL becomes a fetch path. Static no-JS table and methodology remain. Verify Node positive/negative execution, Python structural tests and later exact-head CI before merge. No measurement, M2, publishing rule or master changes.

## Next user-visible milestone and compact queue

Milestone: make six-book Russian branch Pages comparisons shareable and genuinely navigable, then independently verify public HTTP without implying FantLab parity.

| Priority | Unit | Deliverable | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 shareable two-book comparison | Later CI/review/merge of pair URLs with history and robust fallback | Authored change requires later acceptance |
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
- #285 Pages: branch master/root deploy succeeded on 6ba4b1bc (pages build and deployment #40572592825); proposed comparison URLs are not deployed/LIVE_VERIFIED without later merge, deployment and HTTP readback.
- #284 licensing: do not infer a code/data license or publish externally before the rights gate is resolved.
- Local checkout: Git DNS failed; exact source blobs were recovered and verified for actual local tests. Hosted full-repository CI supplies complete integrated execution evidence, not the limited local closure.
- Browser HTTP navigation returned ERR_BLOCKED_BY_ADMINISTRATOR. Current visual changes are VISUAL_NOT_VERIFIED; structural tests are not live browser acceptance. Continue other executable work without bypassing the restriction.
