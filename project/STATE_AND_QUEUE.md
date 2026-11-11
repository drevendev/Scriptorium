# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 490
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-11
LAST_RESULT: #501 confirmed merged at 695e9d71ad87cc46a2a70b7ff329d948f7dd98e6. Proposed Russian CLI metric descriptions aligned with the already reviewed public glossary; later independent acceptance required.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; FantLab analyzer-input identity UNKNOWN; M2 0/5; M3 open; no new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-CLI-METRIC-CATALOG-RU-V1
ISSUE: #283 — offline Russian comprehension of registered metric definitions (do not close)
STATUS: PR_CREATED; LATER_RUN_ACCEPTANCE_REQUIRED
BRANCH: scrip-cli-russian-metric-catalog-20261111
BASE: 695e9d71ad87cc46a2a70b7ff329d948f7dd98e6

ACCEPTANCE: `scriptorium metrics --lang ru` prints Russian human labels for all 29 definitions, matching the reviewed public `metrics.html` glossary. Metric IDs/units, evidence/status, dictionary gates and default English text/JSON remain unchanged; opted-in Russian JSON has `label_language=ru`. Positive/negative regressions, exact-head CI, installed-wheel smoke and later independent review are required. No metric calculations or book-text changes; M2 0/5, M3 open.

## Next user-visible milestone and compact queue

Milestone: a working, accessible Reader showing real-book comparisons and trustworthy downloadable evidence, followed by independently measured rights-cleared editions; do not relax FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 Russian offline metric guide | Match 29 CLI labels to the reviewed Russian glossary while preserving machine contract; later PR acceptance | Merged #501 catalog and #468 glossary |
| P2 | Additional >=300k independent edition(s) | Rights, source/translation/edition hash, reproducible full-text analysis, held-out source-free measurement | Legally reusable source/body; never publish unlicensed prose |
| P3 | #282 AOT N collision and field-by-field FantLab diagnostic | Native pinned evidence, explicit unresolved POS bounds and per-metric deltas | Unknown FantLab input edition; M2 gate unchanged |
| P4 | #285 live Reader / #283 mobile, keyboard, print acceptance | GitHub-managed master/root deployment readback, desktop/mobile screenshots and verified controls; offline root link closure shipped by #496 | Live browser access; separate generated Actions build is not the published root |
| P5 | #284 source-code licence and attribution | Actual rights inventory and owner-granted licence | No implied public licence or invented grant |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. The original four-book rhythm 1/4 holdout and ablation are still exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov source body / #436 historical EOF and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 was closed via #481, not recreated.
