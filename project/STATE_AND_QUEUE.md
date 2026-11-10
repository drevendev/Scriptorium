# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 481
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-11
LAST_RESULT: #491 merged as 259f4e1707fb35d4eb5281d790bea95b96d17928 (issue #490 closed); #492 source-bound aggregate-consistency defect claimed in PR #493 (not merged).
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; FantLab analyzer-input identity UNKNOWN; M2 0/5; M3 open; no new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-VOICE-HOLDOUT-AGGREGATE-INTEGRITY
ISSUE: #492 — reject inconsistent imported four-/six-book author-preview aggregates
STATUS: PR_CREATED; LATER_RUN_ACCEPTANCE_REQUIRED; hosted CI pending
PR: #493
BRANCH: scrip-voice-holdout-aggregate-guard-20261111
BASE: 259f4e1707fb35d4eb5281d790bea95b96d17928

ACCEPTANCE: Verify exact v1/v2 word-weight totals, eight weighted means/population SDs rounded to 6 decimals and declared metric profiles before computing holdout. Missing, Boolean, nonfinite, negative or drifted aggregate values must fail closed. Retain source SHA, feature units, the original four-fold 1/4 and six-fold 2/6 outcomes, and M2 0/5 / M3 open. This is internal consistency, not source authentication.
Verification: positive v1/v2 and 18 adversarial tests authored; exact-head CI NOT_RUN at queue write. Later fresh review/merge only.

## Next user-visible milestone and compact queue

Milestone: credible, reproducible real-book descriptive/author comparisons, followed by independently measured rights-cleared editions; do not relax FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #493 reject drifted holdout aggregates | V1/v2 consistency rejection, complete exact-head CI and later-run acceptance | Frozen six-edition source-free snapshot; no source download |
| P2 | Additional >=300k independent edition(s) | Rights, source/translation/edition hash, reproducible full-text analysis, held-out source-free measurement | Legally reusable source/body; never publish unlicensed prose |
| P3 | #282 AOT N collision and field-by-field FantLab diagnostic | Native pinned evidence, explicit unresolved POS bounds and per-metric deltas | Unknown FantLab input edition; M2 gate unchanged |
| P4 | #285 live Reader / #283 mobile, keyboard, print acceptance | Deployed HTTP readback, desktop/mobile screenshots and verified controls | Browser/deploy access; independent code work permitted |
| P5 | #284 source-code licence and attribution | Actual rights inventory and owner-granted licence | No implied public licence or invented grant |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. The original four-book rhythm 1/4 holdout and ablation are still exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov source body / #436 historical EOF and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 was closed via #481, not recreated.
