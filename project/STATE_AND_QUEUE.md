# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 472
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-10
LAST_RESULT: #478 merged at 92f58f2bd31b5c02f35bb98157d7e531b9b1eb4d; #481 proposes strict current v3/v4 publication support for #479. No new master or live Pages change from #481.
LAST_VERIFIED_PROGRESS: 11 measured / 2 leads; FantLab input identity UNKNOWN; M2 0/5; M3 open. No new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-CURRENT-METRIC-PUBLICATION-v1
ISSUE: #479
STATUS: PR_OPEN; LATER_ACCEPTANCE_REQUIRED
PR: #481
BRANCH: scrip-site-current-metric-publication
BASE: 92f58f2bd31b5c02f35bb98157d7e531b9b1eb4d

ACCEPTANCE: An explicit synthetic publication-manifest entry renders a real current v4 engine result, while a separately labelled structural v3 fixture and historical v1/v2 remain supported. Strict 29-row IDs, per-metric evidence/unit/status, versioned profiles, dictionary dependency, hashes, no-source-text gates, manifest-only paths and fail-closed staged publication. Full exact-head native CI, deterministic site rebuild and installed CLI verification are required before later-run acceptance; no same-run merge. No FantLab parity promotion.

Verification: Initial focused positive/negative tests are proposed in #481 and not yet independently verified. Local Python/full checkout, installed wheel and live browser tests: NOT_RUN. PR CI needs exact final-head verification. #478 is already merged; its closed issues #476/#477/#480 must not be reopened or reworked.

## Next user-visible milestone and compact queue

Milestone: publish safe current-engine metric profiles through reviewed manifests, then expose new independently measured real-book comparisons without weakening scientific source-match gates.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #481 / #479 v3/v4 renderer acceptance | Exact head CI, full suite, reproducible build, verified 29-row current artifact, staged privacy contract; later-run merge | Current PR head and review/check gates |
| P2 | Independently measured editions for author-profile replication | >=300k legally usable works, separate author/translator/edition identities, held-out tests on new books | Rights/source identity; avoid tuning on the four existing books |
| P3 | #282 measured AOT N ambiguity and a source-matched FantLab witness | Pinned runtime evidence, unchanged per-metric rounding, source-identity matched reference | Native ambiguity, analyzer-input identity UNKNOWN; M2 0/5 |
| P4 | #285 live Reader routes / #283 mobile, keyboard and print acceptance | Actual HTTP, mobile/desktop screenshots and interactions | Browser navigation restrictions; source improvements independent |
| P5 | #284 explicit source-code licence and attribution | Contributor/third-party inventory and owner-authorized licence decision | No invented grant; separate from product PR |

## Retained scientific and operational boundaries

11 measured editions and 2 research leads; four-edition rhythm stress tests are extensions, not a classifier or external validation. M0 closed; M1 open; M2 0/5; M3/M4/M5 open. >=300000 characters INCLUDING spaces and legal evidence required per profile/benchmark work. No published manuscripts. Translation identities are separate; AOT/pylem 0.0.18 N noun/cardinal ambiguity remains. Exact FantLab input identity is UNKNOWN and all source-unmatched comparisons are diagnostic; NOT_RUN is not PASS.

#284 attribution/rights grant and Trusov body / #436 historical EOF remain scoped unresolved work, not blockers for independent product PRs. #265 non-admin branch rules prohibit direct master commits; deletion/admin capability remains separate. Preserve the existing perpetual schedule.

Reviewed Drive leads were deduplicated: Compare003 mean-integrity guards are already in current compare.py (#279); POS distribution integration is tracked by closed #287; CORPUS-087 is already marked reconciled to #422. The distinct still-missing schema-publication lead is now #479. Do not recreate these issues or blindly replay old patches; private storage identifiers stay private.
