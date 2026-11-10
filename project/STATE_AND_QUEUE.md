# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 478
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-10
LAST_RESULT: #487 confirmed merged at b6e97964f462322608f59319ef029125acc4df68. Prepared streaming UASZ mean for book-length dictionary analysis with frozen numeric semantics; no new books or FantLab parity claims.
LAST_VERIFIED_PROGRESS: 11 measured / 2 leads; FantLab input identity UNKNOWN; M2 0/5; M3 open. No new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-VOCAB-STREAMING-UASZ-v1
ISSUE: Existing inferred vocabulary profile; focused performance/reproducibility regression
STATUS: PR_AUTHORED_IN_THIS_RUN; LATER_ACCEPTANCE_REQUIRED
BRANCH: scrip-vocabulary-streaming-uasz-20261110
BASE: b6e97964f462322608f59319ef029125acc4df68

ACCEPTANCE: Dictionary-dependent UASZ scalar window means stream over book-length token series without retaining all window values. Existing public rolling-series API and exact v1 numeric results, null/zero semantics, fixed profile version and all artifacts remain unchanged. Positive/negative regression tests, exact-head CI and later-run acceptance required.

Verification: deterministic standalone 3-case prototype PASS (randomized window/length/dictionary oracle, long input, invalid size); exact repository CI NOT_RUN before PR checks.

## Next user-visible milestone and compact queue

Milestone: ship safely shareable real-book comparisons and expand independently measured editions without changing FantLab parity criteria.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Streaming UASZ means for book-length analysis (current PR) | Exact scalar equivalence, no materialized full-window tuple, edge/invalid-window tests; later-run merge | Existing inferred vocabulary profile, no source/body changes |
| P2 | New independent >=300k source-bound author editions | Rights, distinct author/translator/edition, reproducible measurements and held-out tests | Clear legal source and pin; do not tune the existing four-book pilot |
| P3 | #282 AOT N ambiguity and source-matched FantLab witness | Native pinned evidence, exact metric deltas, edition/input identity | Pinned morphology, FantLab input identity UNKNOWN; M2 0/5 |
| P4 | #285 live Reader / #283 mobile, keyboard, print | HTTP verification, desktop/mobile screenshots and tested controls | Browser availability; independent source work permitted |
| P5 | #284 explicit source-code licence and attribution | Rights inventory and owner-authorized grant | Cannot invent grant |

## Retained scientific and operational boundaries

11 measured editions and 2 research leads; four-edition rhythm stress tests are extensions, not a classifier or external validation. M0 closed; M1 open; M2 0/5; M3/M4/M5 open. >=300000 characters INCLUDING spaces and legal evidence required per profile/benchmark work. No published manuscripts. Translation identities are separate; AOT/pylem 0.0.18 N noun/cardinal ambiguity remains. Exact FantLab input identity is UNKNOWN and all source-unmatched comparisons are diagnostic; NOT_RUN is not PASS.

#284 attribution/rights grant and Trusov body / #436 historical EOF remain scoped unresolved work, not blockers for independent product PRs. #265 non-admin branch rules prohibit direct master commits; deletion/admin capability remains separate. Preserve the existing perpetual schedule.

Reviewed Drive leads were deduplicated: Compare003 mean-integrity guards are already in current compare.py (#279); POS distribution integration is tracked by closed #287; CORPUS-087 is already marked reconciled to #422. The distinct still-missing schema-publication lead is now #479. Do not recreate these issues or blindly replay old patches; private storage identifiers stay private.
