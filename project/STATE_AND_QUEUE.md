# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 484
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-11
LAST_RESULT: #495 merged in master as 5659544c917fa12ed573f60bee7075e4aa2d635d. Root branch Pages Reader/voice and CSV require an executable link-closure gate; focused CI and regression PR candidate.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; FantLab analyzer-input identity UNKNOWN; M2 0/5; M3 open; no new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-BRANCH-PAGES-ROOT-LINKS
ISSUE: #285 — branch Pages publication acceptance (do not close)
STATUS: PR_CREATED; LATER_RUN_ACCEPTANCE_REQUIRED
BRANCH: scrip-pages-root-link-audit-20261111
BASE: 5659544c917fa12ed573f60bee7075e4aa2d635d

ACCEPTANCE: Python offline QA checks all five actual branch-published Reader HTML routes, local links, same-site fragments, pinned downloadable CSV/JSON/CSS/JS, nested voice paths and unsafe/traversal paths. Positive and negative regressions run in canonical tests and exact-branch Pages CI. Branch master/(root) publisher stays unchanged; generated build/site is a separate Actions artifact, not proof of live root. Live HTTP and visual acceptance remain UNVERIFIED.
Verification: source-level root link inspection and new negative fixtures; full exact-head CI pending, local Python execution NOT_RUN. Scientific M2/M3 gates unchanged.

## Next user-visible milestone and compact queue

Milestone: credible, reproducible real-book descriptive/author comparisons, followed by independently measured rights-cleared editions; do not relax FantLab parity.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #285 branch Pages Reader route/download closure | All actual root Reader links, deep links, CSV/JSON and fragments checked by CI; no mistaken Actions-artifact deployment claim | PR acceptance and branch Pages live HTTP still separate |
| P2 | Additional >=300k independent edition(s) | Rights, source/translation/edition hash, reproducible full-text analysis, held-out source-free measurement | Legally reusable source/body; never publish unlicensed prose |
| P3 | #282 AOT N collision and field-by-field FantLab diagnostic | Native pinned evidence, explicit unresolved POS bounds and per-metric deltas | Unknown FantLab input edition; M2 gate unchanged |
| P4 | #285 live Reader / #283 mobile, keyboard, print acceptance | GitHub-managed master/root deployment readback, desktop/mobile screenshots and verified controls | Live browser access; separate generated Actions build is not the published root |
| P5 | #284 source-code licence and attribution | Actual rights inventory and owner-granted licence | No implied public licence or invented grant |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. The original four-book rhythm 1/4 holdout and ablation are still exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov source body / #436 historical EOF and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 was closed via #481, not recreated.
