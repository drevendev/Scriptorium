# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 571
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-19
LAST_RESULT: #587 confirmed merged at bd9d1124f8205b7ac53ac2eaadcb3309dbe3a605; contextual Reader chart highlights prepared for independent acceptance.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; M2 0/5, FantLab analyzer-input identity UNKNOWN.

## Current delivery and acceptance

UNIT_ID: SCRIP-READER-CHART-SUBSET-HIGHLIGHT-006
ISSUE: Reader chart subset visibility; follows merged #587 catalogue-to-chart navigation
STATUS: PR_CANDIDATE; exact-head CI and later independent review/browser/Pages acceptance pending
BRANCH: scrip-reader-chart-subset-highlight-20261119
BASE: bd9d1124f8205b7ac53ac2eaadcb3309dbe3a605

ACCEPTANCE: The catalogue-to-chart permalink visibly identifies measured editions in the validated *current* catalogue subset in both chart bars and the exact-value table, including on mobile and in print. The chart still displays every measured edition, retains 11-edition baseline/CSV, and explicitly distinguishes the all-edition data from the highlighted subset. Empty, mismatched, forged duplicate query parameters and reset never imply a subset. No changed source data, metric definitions, corpus admission, manuscript text or parity claims. Require positive/negative Node and desktop/mobile Chromium tests, fresh exact-head CI, and later independent acceptance.

## Next user-visible milestone and compact queue

Milestone: A reader can follow a filtered measured-book catalogue to a real chart, immediately distinguish selected books from the full evidence-backed distribution, and inspect their exact source-bound values.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Contextual chart selection highlighting | Fresh CI + later independent browser review/merge | PR head/checks |
| P2 | Verify live Reader release | Exact Pages deployment + actual public route and interactions | DNS/network availability |
| P3 | #562 source-bound lexical comparison | Rights-reviewed, pinned derived evidence | Edition-specific publication rights |
| P4 | #511 Trusov translation pair | Independent complete body and evidence | Historical Page completeness |
| P5 | #282 native AOT ambiguity | Measured discrimination on frozen inputs | Pinned backend/source |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. Holdout/ablation and within-sample tests are exploratory, NOT external validation. Admission/author/parity requires >=300,000 characters INCLUDING spaces and reuse rights. No manuscripts in public artifacts; translation identities separate. AOT/pylem==0.0.18 noun/cardinal N collision unresolved. Source-unmatched resemblance is DIAGNOSTIC only; UNKNOWN is not zero, NOT_RUN is not PASS. #284 rights, Trusov EOF #436 and #265 controls remain scoped. Do not mutate hourly scheduler.
