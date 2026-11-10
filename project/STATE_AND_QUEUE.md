# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 476
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-10
LAST_RESULT: #485 merged into master at 668787d89007c7b8718bc1042ad7524b89c962f7. #486 proposes a ninth measured Reader chart (questions per 1,000 words); no analyzer formula, source text, corpus admission or FantLab parity change.
LAST_VERIFIED_PROGRESS: 11 measured / 2 leads; FantLab input identity UNKNOWN; M2 0/5; M3 open. No new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-READER-QUESTION-CHART-v1
ISSUE: #283 (focused chart slice)
STATUS: PR_OPEN #486; LATER_ACCEPTANCE_REQUIRED
BRANCH: scrip-reader-question-chart-20261110
BASE: 668787d89007c7b8718bc1042ad7524b89c962f7

ACCEPTANCE: Nine allow-listed Russian Reader charts include source-bound question-mark frequency per 1,000 words across all 11 measured editions. Chart selection, ranking, exact table, accessible control, link/clipboard, CSV and missing-data behavior remain consistent and deterministic; existing no-JavaScript chart stays available. Scientific status remains diagnostic only. Require exact-head CI, later-run acceptance and separate live Pages verification.

Verification: feature-branch structural source/HTML/metric-registry and 11-observation checks PASS. Python/Node suite, Pages build and visual browser checks NOT_RUN before exact-head CI.

## Next user-visible milestone and compact queue

Milestone: ship safely shareable real-book comparisons and expand independently measured editions without changing FantLab parity criteria.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #486 ninth measured Reader chart (questions) | Exact pinned data, full regression CI, later-run acceptance/merge and separate live check | Focused #283 presentation PR |
| P2 | New independent >=300k source-bound author editions | Rights, distinct author/translator/edition, reproducible measurements and held-out tests | Clear legal source and pin; do not tune the existing four-book pilot |
| P3 | #282 AOT N ambiguity and source-matched FantLab witness | Native pinned evidence, exact metric deltas, edition/input identity | Pinned morphology, FantLab input identity UNKNOWN; M2 0/5 |
| P4 | #285 live Reader / #283 mobile, keyboard, print | HTTP verification, desktop/mobile screenshots and tested controls | Browser availability; independent source work permitted |
| P5 | #284 explicit source-code licence and attribution | Rights inventory and owner-authorized grant | Cannot invent grant |

## Retained scientific and operational boundaries

11 measured editions and 2 research leads; four-edition rhythm stress tests are extensions, not a classifier or external validation. M0 closed; M1 open; M2 0/5; M3/M4/M5 open. >=300000 characters INCLUDING spaces and legal evidence required per profile/benchmark work. No published manuscripts. Translation identities are separate; AOT/pylem 0.0.18 N noun/cardinal ambiguity remains. Exact FantLab input identity is UNKNOWN and all source-unmatched comparisons are diagnostic; NOT_RUN is not PASS.

#284 attribution/rights grant and Trusov body / #436 historical EOF remain scoped unresolved work, not blockers for independent product PRs. #265 non-admin branch rules prohibit direct master commits; deletion/admin capability remains separate. Preserve the existing perpetual schedule.

Reviewed Drive leads were deduplicated: Compare003 mean-integrity guards are already in current compare.py (#279); POS distribution integration is tracked by closed #287; CORPUS-087 is already marked reconciled to #422. The distinct still-missing schema-publication lead is now #479. Do not recreate these issues or blindly replay old patches; private storage identifiers stay private.
