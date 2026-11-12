# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 498
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-12
LAST_RESULT: #509 native MERGED at d9a83671c57bdc3d71e8e04704b767036aba8bd6. Browser screenshot/print acceptance remains open; new independent PR adds executable Chromium checks.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; FantLab analyzer-input identity UNKNOWN; M2 0/5; M3 open; no new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-012-REAL-BROWSER-ACCEPTANCE-V1
ISSUES: #283 visual, mobile, print, keyboard acceptance and #285 publication distinction; neither is closed by branch-preview checks alone
STATUS: PR_CREATED; LATER_RUN_ACCEPTANCE_REQUIRED
BRANCH: scrip-reader-browser-acceptance-20261112
BASE: d9a83671c57bdc3d71e8e04704b767036aba8bd6

ACCEPTANCE: Existing Pages CI stages the actual branch-root Reader and runs pinned real Chromium browser acceptance at desktop 1440x900 and mobile 390x844. Check loaded/verified 11-work snapshot, 7/9 paired observations with missing sides, chart selection, keyboard skip, 29 glossary targets, author-preview page and CSV, mobile overflow, and generate actual A4 print PDF + screenshots. Upload seven-day source-free evidence artifact even on failed acceptance. Browser screenshots require human inspection; branch-preview test != live-route verification. No owner/admin/Page deployment interlocks changed, no manuscript text. Exact-head CI then later independent acceptance/merge.

## Next user-visible milestone and compact queue

Milestone: a working, accessible Reader showing real-book comparisons and trustworthy downloadable evidence, followed by independently measured rights-cleared editions; do not relax FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283/#285 real branch-root browser acceptance | Execute desktop/mobile Chromium, pair/keyboard/glossary controls, screenshot/PDF artifacts; later exact-head CI review. Live URL remains separate. | Browser download in CI; live website and human screenshot inspection not proven by a local branch preview |
| P2 | Additional >=300k independent edition(s) | Rights, source/translation/edition hash, reproducible full-text analysis, held-out source-free measurement | Legally reusable source/body; never publish unlicensed prose |
| P3 | #282 AOT N collision and field-by-field FantLab diagnostic | Native pinned evidence, explicit unresolved POS bounds and per-metric deltas | Unknown FantLab input edition; M2 gate unchanged |
| P4 | #285 live Reader / #283 mobile, keyboard, print acceptance | GitHub-managed master/root deployment readback, desktop/mobile screenshots and verified controls; offline root link closure shipped by #496 | Live browser access; static tests are not visual proof |
| P5 | #284 source-code licence and attribution | Actual rights inventory and owner-granted licence | No implied public licence or invented grant |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. The original four-book rhythm 1/4 holdout and ablation are still exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov source body / #436 historical EOF and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 was closed via #481, not recreated.
