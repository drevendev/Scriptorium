# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 469
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-09
LAST_RESULT: PR #473 confirmed merged as 4e95f729521a48be5e640704ced182a87cbaac3e. The four-work holdout remains 1/4; author-voice reliability is limited. Proposed next independent sensitivity slice tests the result under all eight single-feature omissions (1/4 for seven omissions, 2/4 without question-mark rate).
LAST_VERIFIED_PROGRESS: 11 measured / 2 leads; FantLab input identity UNKNOWN; M2 0/5; M3 open.

## Current delivery and acceptance

UNIT_ID: SCRIP-VOICE-008-ABLATION-CLI-v1
ISSUES: #283 (partial Reader comprehension); M3 exploratory diagnostics, NOT a gate completion
STATUS: PR_CANDIDATE; LATER_ACCEPTANCE_REQUIRED; CI_NOT_RUN
BRANCH: scrip-voice-feature-ablation
BASE: 4e95f729521a48be5e640704ced182a87cbaac3e

ACCEPTANCE: Installed-wheel `scriptorium voice --ablate` produces deterministic source-bound JSON/Markdown with eight seven-feature recomputations of all four folds, explicit metrics/units, preserved training exclusion, and no source prose. Positive and negative regressions verify 1/4 baseline, seven unchanged 1/4 outcomes, one 2/4 outcome (question-mark-rate omission), strict pinned SHA validation and CLI option rejection. README describes this as sensitivity, not selection, independent validation, or FantLab parity. Require later exact-head CI acceptance and merge; no website deployment claim from an offline CLI PR.

## Next user-visible milestone and compact queue

Milestone: make the failure modes of real Russian-book author comparisons inspectable and reproducible, then extend evidence beyond four selected books.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Four-work voice feature-removal sensitivity CLI | Eight distinct ablations, pinned 1/4 and 2/4, honest JSON/Markdown, tests, later CI/merge | Current PR |
| P2 | #285 live Reader route and #283 mobile/print/focus verification | Actual HTTP and real desktop/mobile screenshots | Browser HTTP restriction; independent code work allowed |
| P3 | New independently measured works for author-profile replication | >=300k licensed works; explicit authors/editions, profile holdout on new books | Candidate rights and corpus identities; must avoid tuning on same four |
| P4 | Source-matched FantLab parity witness | >=300k legal input identity and required published metric deltas, unchanged rounding rules | Analyzer-input identity UNKNOWN; #281 closed without M2 |
| P5 | Trusov translation body / #436 exact EOF; #284 legal attribution | Rights-verified body and formal attributions where available | Historical render EOF/rights-holder grants needed |

## Retained scientific and operational boundaries

11 measured editions and 2 research leads; four edition rhythm stress test is an extension, not a classifier or external validation. M0 closed; M1 open; M2 0/5; M3/M4/M5 open. >=300000 characters INCLUDING spaces and legal evidence required per profile/benchmark work. No published manuscripts. Translation identities are separate; AOT/pylem 0.0.18 N noun/cardinal ambiguity remains. Exact FantLab input identity is UNKNOWN and all source-unmatched comparisons are diagnostic; NOT_RUN is not PASS.

#285 HTTP/mobile visual acceptance remains blocked by browser restriction (VISUAL_NOT_VERIFIED); #284 rights gate unresolved; #265 non-admin branch rule prohibits direct master commits. None blocks independent Reader PRs. Do not change the existing perpetual schedule.
