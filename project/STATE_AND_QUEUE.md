# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 578
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-20
LAST_RESULT: #594 merged at f87d8507d808737f0096c8e8905d5b5d2a9e20b4; same-edition lexical provenance consistency fix proposed from exact master.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; M2 0/5, FantLab analyzer-input identity UNKNOWN.

## Current delivery and acceptance

UNIT_ID: SCRIP-LEXICAL-EDITION-INTEGRITY-013
ISSUE: #562 private lexical comparison follow-on
STATUS: PR_CANDIDATE; exact-head CI and later independent acceptance pending
BRANCH: scrip-lexical-edition-identity-20261120
BASE: f87d8507d808737f0096c8e8905d5b5d2a9e20b4

ACCEPTANCE: Reused edition IDs reject contradictory declared language, original-work ID or translator even when normalized bytes match; translation-pair mode requires two distinct edition IDs. Valid same-edition self-comparisons and separately identified translations still work. Tests cover each conflict, positive controls and source-free outputs. No historical metric, text or licensing change.

## Next user-visible milestone and compact queue

Milestone: Private lexical comparisons must preserve edition/translator identity, not merely matching source hashes.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #562 edition-ID provenance guard | Reject contradictory identities; positive/negative regressions; later merge | Exact-head PR CI and later acceptance |
| P2 | #592 Reader live release verification | Public route and deployed Reader bytes match validated source | External network/DNS availability |
| P3 | #562 legally published lexical comparison | Edition-specific source-free distributions and explicit rights/replay evidence | Rights and edition identities |
| P4 | #511 Trusov translation pair | Independently complete historical literary body | Historical Page completeness |
| P5 | #282 pinned native AOT collision | Reproducible measured noun/cardinal bounds | Python 3.9/pylem native sidecar and source |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. Holdout/ablation and within-sample tests are exploratory, NOT external validation. Admission/author/parity requires >=300,000 characters INCLUDING spaces and reuse rights. No manuscripts in public artifacts; translation identities separate. AOT/pylem==0.0.18 noun/cardinal N collision unresolved. Source-unmatched resemblance is DIAGNOSTIC only; UNKNOWN is not zero, NOT_RUN is not PASS. #284 rights, Trusov EOF #436 and #265 controls remain scoped. Do not mutate hourly scheduler.
