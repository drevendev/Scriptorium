# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 496
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-12
LAST_RESULT: #507 confirmed merged at 5f98dc76ac1db0db09bceb0cbe0b207d7acd0c72. Prepare per-edition missing observation counts for the paired Reader; later acceptance required.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; FantLab analyzer-input identity UNKNOWN; M2 0/5; M3 open; no new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-012-PAIR-SIDE-COVERAGE-V1
ISSUE: #283 — per-edition missing counts in interactive pair-table status (do not close)
STATUS: PR_CREATED; LATER_RUN_ACCEPTANCE_REQUIRED
BRANCH: scrip-reader-pair-side-coverage-20261112
BASE: 5f98dc76ac1db0db09bceb0cbe0b207d7acd0c72

ACCEPTANCE: On verified JSON, paired status counts unavailable observations independently for each edition (including overlap for a field absent on both sides), never treating true measured zero as missing. Existing nine-field no-JS fallback, shared-only toggle, chart, provenance and JSON/CSV/Markdown exports remain unchanged. Shipped-JS positive/negative tests, exact-head CI and later independent review required. Browser desktop/mobile VISUAL_NOT_VERIFIED. M2 0/5, M3 open.

## Next user-visible milestone and compact queue

Milestone: a working, accessible Reader showing real-book comparisons and trustworthy downloadable evidence, followed by independently measured rights-cleared editions; do not relax FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 per-edition missingness for Reader pair metrics | Verified pair status shows separate left/right missing counts, including overlap, never counts true zero as absent; no export/fallback drift; later CI acceptance | Existing nine-field pair coverage and measured snapshot; #507 merged |
| P2 | Additional >=300k independent edition(s) | Rights, source/translation/edition hash, reproducible full-text analysis, held-out source-free measurement | Legally reusable source/body; never publish unlicensed prose |
| P3 | #282 AOT N collision and field-by-field FantLab diagnostic | Native pinned evidence, explicit unresolved POS bounds and per-metric deltas | Unknown FantLab input edition; M2 gate unchanged |
| P4 | #285 live Reader / #283 mobile, keyboard, print acceptance | GitHub-managed master/root deployment readback, desktop/mobile screenshots and verified controls; offline root link closure shipped by #496 | Live browser access; separate generated Actions build is not the published root |
| P5 | #284 source-code licence and attribution | Actual rights inventory and owner-granted licence | No implied public licence or invented grant |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. The original four-book rhythm 1/4 holdout and ablation are still exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov source body / #436 historical EOF and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 was closed via #481, not recreated.
