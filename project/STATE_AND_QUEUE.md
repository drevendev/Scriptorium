# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 480
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-10
LAST_RESULT: #489 merged as 922c85ac1060ef582225b1bbb58bbec0a63b1dfd; PR #491 created for opt-in six-book, three-author holdout diagnostic (not merged).
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; FantLab analyzer-input identity UNKNOWN; M2 0/5; M3 open; no new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-VOICE-SIX-FOLD-v2
ISSUE: #490 — source-bound six-fold author-rhythm stress test
STATUS: PR_CREATED; LATER_RUN_ACCEPTANCE_REQUIRED
PR: #491
BRANCH: scrip-voice-six-fold-stress-20261110
BASE: 922c85ac1060ef582225b1bbb58bbec0a63b1dfd

ACCEPTANCE: Extend the #489 opt-in third author into six deterministic leave-one-out folds with three independently pinned author centroids, explicit per-author training keys, eight identical units/features and honest ties. Reject changing source hash/edition, absent/non-numeric evidence and author/feature drift. Preserve default four-fold v1 preview, ablation and published Reader. Report observed 2/6 successes as **within-sample negative evidence**, not classifier generalization or accepted M3.
Verification: source-snapshot arithmetic independently cross-checked as 2/6 with no ties; Python/CI, wheel and Pages exact-head checks pending; later independent PR review and qualifying merge only.

## Next user-visible milestone and compact queue

Milestone: credible, reproducible real-book descriptive/author comparisons, followed by independently measured rights-cleared editions; do not relax FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #491 six-fold three-author stress test | All six folds/negative controls and exact-head CI; later-run qualifying merge | Current source-free six-edition pinned snapshot |
| P2 | Additional >=300k independent edition(s) | Rights, source/translation/edition hash, reproducible full-text analysis, held-out source-free measurement | Legally reusable source/body; never publish unlicensed prose |
| P3 | #282 AOT N collision and field-by-field FantLab diagnostic | Native pinned evidence, explicit unresolved POS bounds and per-metric deltas | Unknown FantLab input edition; M2 gate unchanged |
| P4 | #285 live Reader / #283 mobile, keyboard, print acceptance | Deployed HTTP readback, desktop/mobile screenshots and verified controls | Browser/deploy access; independent code work permitted |
| P5 | #284 source-code licence and attribution | Actual rights inventory and owner-granted licence | No implied public licence or invented grant |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. The original four-book rhythm 1/4 holdout and ablation are still exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov source body / #436 historical EOF and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 was closed via #481, not recreated.
