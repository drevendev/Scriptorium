# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 474
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-10
LAST_RESULT: #482 merged at 4e93e69b2f0f4b559b822858f402243e5368cfd1. Current branch addresses an async clipboard status race affecting verified book-pair and chart links; CI acceptance pending.
LAST_VERIFIED_PROGRESS: 11 measured / 2 leads; FantLab input identity UNKNOWN; M2 0/5; M3 open. No new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-READER-ASYNC-CLIPBOARD-STATUS-v1
ISSUE: #283 (focused public-reader usability)
STATUS: PR_OPEN; LATER_ACCEPTANCE_REQUIRED
PR: #483
BRANCH: scrip-reader-clipboard-async-state-20261110
BASE: 4e93e69b2f0f4b559b822858f402243e5368cfd1

ACCEPTANCE: A delayed Clipboard API success or rejection must not display feedback for a different selected book pair/chart, nor overwrite a newer in-flight clipboard result for the same link. Keep same-origin/source allow-list validation, no-JS fallback, 44px controls, and pinned 11 measured editions. Add positive and deferred-promise regression cases to both shipped Node smoke tests. Later exact-head CI/PR review and real browser/mobile acceptance are separate. No FantLab parity promotion.

Verification: prior #482 merge confirmed, local full-suite and browser NOT_RUN; PR #483 created at d578d9e448f0e8c247248e6339c56d3550c2c351; initial checks pending.

## Next user-visible milestone and compact queue

Milestone: ship safely shareable real-book comparisons and expand independently measured editions without changing FantLab parity criteria.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 prevent stale clipboard acknowledgements for chart and paired links | Deferred-promise regressions, exact-head Pages checks, later-run acceptance | Focused async-state PR |
| P2 | New independent >=300k source-bound author editions | Rights, distinct author/translator/edition, reproducible measurements and held-out tests | Clear legal source and pin; do not tune the existing four-book pilot |
| P3 | #282 AOT N ambiguity and source-matched FantLab witness | Native pinned evidence, exact metric deltas, edition/input identity | Pinned morphology, FantLab input identity UNKNOWN; M2 0/5 |
| P4 | #285 live Reader / #283 mobile, keyboard, print | HTTP verification, desktop/mobile screenshots and tested controls | Browser availability; independent source work permitted |
| P5 | #284 explicit source-code licence and attribution | Rights inventory and owner-authorized grant | Cannot invent grant |

## Retained scientific and operational boundaries

11 measured editions and 2 research leads; four-edition rhythm stress tests are extensions, not a classifier or external validation. M0 closed; M1 open; M2 0/5; M3/M4/M5 open. >=300000 characters INCLUDING spaces and legal evidence required per profile/benchmark work. No published manuscripts. Translation identities are separate; AOT/pylem 0.0.18 N noun/cardinal ambiguity remains. Exact FantLab input identity is UNKNOWN and all source-unmatched comparisons are diagnostic; NOT_RUN is not PASS.

#284 attribution/rights grant and Trusov body / #436 historical EOF remain scoped unresolved work, not blockers for independent product PRs. #265 non-admin branch rules prohibit direct master commits; deletion/admin capability remains separate. Preserve the existing perpetual schedule.

Reviewed Drive leads were deduplicated: Compare003 mean-integrity guards are already in current compare.py (#279); POS distribution integration is tracked by closed #287; CORPUS-087 is already marked reconciled to #422. The distinct still-missing schema-publication lead is now #479. Do not recreate these issues or blindly replay old patches; private storage identifiers stay private.
