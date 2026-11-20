# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 582
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-20
LAST_RESULT: #598 merged at 5dd162dfe01e122040a842ccba52a82161c74124; follow-up fixes the remaining English screen-reader landmark on the Russian comparison route.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; M2 0/5, FantLab analyzer-input identity UNKNOWN.

## Current delivery and acceptance

UNIT_ID: SCRIP-READER-RUSSIAN-LANDMARK-017
ISSUE: #283 post-merge reader accessibility follow-on (already closed)
STATUS: PR_CANDIDATE; exact-head CI and later independent acceptance pending
BRANCH: scrip-reader-russian-landmark-20261120
BASE: 5dd162dfe01e122040a842ccba52a82161c74124

ACCEPTANCE: On the already localized pinned comparison HTML route, change the remaining `aria-label='Reader navigation'` to a Russian accessible landmark. Assert exactly one accessible navigation landmark and no remaining English label; reject language-template drift. Preserve all visible copy, the ten metrics, seven signed differences, machine JSON/CSV bytes, gallery CLI, immutable source hashes, no network/manuscripts and M2 0/5. Require exact-head regression/build CI and later independent review; visual/live verification remains separate.

## Next user-visible milestone and compact queue

Milestone: Screen-reader users get the same Russian navigation affordance as sighted readers on the already localized, evidence-backed frozen two-book comparison page.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 reader landmark locale regression | Russian navigation aria-label, exactly one landmark, unchanged source-free exports | Later PR CI/review; visual/live check separate |
| P2 | #562 legally publishable lexical comparison | Only edition-verified rights-cleared, source-free aggregate distributions and explicit replay identity | Rights and edition identities |
| P3 | #511 Trusov translation pair | Independently complete historical literary body | Historical Page completeness |
| P4 | #282 pinned native AOT collision | Reproducible measured noun/cardinal bounds | Python 3.9/pylem native sidecar and source |
| P5 | #284 license/attribution release gate | Explicit software license and source/data rights publication checks | Rights holder evidence |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. Holdout/ablation and within-sample tests are exploratory, NOT external validation. Admission/author/parity requires >=300,000 characters INCLUDING spaces and reuse rights. No manuscripts in public artifacts; translation identities separate. AOT/pylem==0.0.18 noun/cardinal N collision unresolved. Source-unmatched resemblance is DIAGNOSTIC only; UNKNOWN is not zero, NOT_RUN is not PASS. Trusov EOF #436 and #265 controls remain scoped. Do not mutate hourly scheduler.
