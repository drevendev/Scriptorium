# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 482
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-11
LAST_RESULT: #493 merged as 8e1f05a4f33f134767808c4a236e0ef223507a96 (issue #492 closed); #494 adds a source-bound six-fold, three-author public negative-result section (PR_CREATED, not merged).
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; FantLab analyzer-input identity UNKNOWN; M2 0/5; M3 open; no new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-READER-THREE-AUTHOR-HOLDOUT
ISSUE: #283 — incremental Reader scientific interpretability (do not close)
STATUS: PR_CREATED; LATER_RUN_ACCEPTANCE_REQUIRED; exact-head CI pending
PR: #494
BRANCH: scrip-voice-three-author-reader-20261111
BASE: 8e1f05a4f33f134767808c4a236e0ef223507a96

ACCEPTANCE: Public static voice Reader shows six exact v2 held-out book rows, three relative distances with units and known/nearest author, 2/6 correct/4/6 other, explicit source links and a pinned source snapshot Git blob. Keep the original four-book 1/4 and ablation unchanged. Strong M2 0/5, M3 open and no classifier/parity claim. New positive/negative tests reconstruct v2 directly from frozen evidence; later fresh CI/merge and browser/mobile validation remain separate.
Verification: source-free JS recomputation yielded six distinct fold rows and 2/6; Python exact-head GitHub CI NOT_RUN at queue commit. No live site change yet.

## Next user-visible milestone and compact queue

Milestone: credible, reproducible real-book descriptive/author comparisons, followed by independently measured rights-cleared editions; do not relax FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #494 six-book public author-stress-test evidence | Pinned six-fold table, source identity, accessible no-JS route, exact-head CI and later acceptance | Existing v2 CLI + 11-work source-free snapshot; browser visual check separately |
| P2 | Additional >=300k independent edition(s) | Rights, source/translation/edition hash, reproducible full-text analysis, held-out source-free measurement | Legally reusable source/body; never publish unlicensed prose |
| P3 | #282 AOT N collision and field-by-field FantLab diagnostic | Native pinned evidence, explicit unresolved POS bounds and per-metric deltas | Unknown FantLab input edition; M2 gate unchanged |
| P4 | #285 live Reader / #283 mobile, keyboard, print acceptance | Deployed HTTP readback, desktop/mobile screenshots and verified controls | Browser/deploy access; independent code work permitted |
| P5 | #284 source-code licence and attribution | Actual rights inventory and owner-granted licence | No implied public licence or invented grant |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. The original four-book rhythm 1/4 holdout and ablation are still exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov source body / #436 historical EOF and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 was closed via #481, not recreated.
