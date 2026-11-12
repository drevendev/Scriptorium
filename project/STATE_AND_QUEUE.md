# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 499
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-12
LAST_RESULT: #510 native MERGED at e14e622efe4f54f7e6c6c48d14652a1b52d84ac2. Inspected 16-page Chromium A4 evidence: page 1 had only hero copy, while the tall evidence panel was forced to page 2; scoped print-flow fix authored for later acceptance.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; FantLab analyzer-input identity UNKNOWN; M2 0/5; M3 open; no new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-012-A4-PRINT-FLOW-V1
ISSUE: #283 Reader print usability; #285 live publication verification remains separate
STATUS: PR_CREATED; LATER_RUN_ACCEPTANCE_REQUIRED
BRANCH: scrip-reader-a4-print-flow-20261112
BASE: e14e622efe4f54f7e6c6c48d14652a1b52d84ac2

ACCEPTANCE: Real Chromium A4 PDF from merged #510 exposes a near-empty first sheet because `.hero-visual` is forced `break-inside:avoid` although it exceeds a page. Let the evidence panel fragment, keep individual chart observations intact, preserve the exact numeric table, and assert print computed styles in existing Chromium acceptance. Require fresh exact-head CI, visual inspection of the new PDF and later-run merge; browser-preview proof is not live Pages verification.

## Next user-visible milestone and compact queue

Milestone: a working, accessible Reader showing real-book comparisons and trustworthy downloadable evidence, followed by independently measured rights-cleared editions; do not relax FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 A4 Reader print-flow regression | Remove page-spanning `break-inside:avoid` from evidence panel, print complete chart rows and exact table; exercise real Chromium PDF/print styles and inspect new artifact | Later exact-head CI and next-run independent acceptance |
| P2 | Additional >=300k independent edition(s) | Rights, source/translation/edition hash, reproducible full-text analysis, held-out source-free measurement | Legally reusable source/body; never publish unlicensed prose |
| P3 | #282 AOT N collision and field-by-field FantLab diagnostic | Native pinned evidence, explicit unresolved POS bounds and per-metric deltas | Unknown FantLab input edition; M2 gate unchanged |
| P4 | #285 live Reader / #283 mobile, keyboard, print acceptance | GitHub-managed master/root deployment readback, desktop/mobile screenshots and verified controls; offline root link closure shipped by #496 | Live browser access; static tests are not visual proof |
| P5 | #284 source-code licence and attribution | Actual rights inventory and owner-granted licence | No implied public licence or invented grant |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. The original four-book rhythm 1/4 holdout and ablation are still exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov source body / #436 historical EOF and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 was closed via #481, not recreated.
