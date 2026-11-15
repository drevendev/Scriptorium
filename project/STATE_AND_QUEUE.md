# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 529
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-15
LAST_RESULT: #543 merged at 9ceda8f5ef40d25e37f2963a8e8f5ff0a139b101; independent Reader snapshot retry candidate under #283.
LAST_VERIFIED_PROGRESS: 11 complete measured editions / 2 research leads plus separate 145-Page Trusov **incomplete** projected excerpt; M2 0/5, FantLab analyzer-input identity UNKNOWN; M3 open.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-014-VERIFIED-SNAPSHOT-RETRY
ISSUE: #283 Reader interactive-data failure recovery
STATUS: PR_CANDIDATE; exact-head Chromium/Pages and later-run acceptance required
BRANCH: scrip-reader-snapshot-retry-20261115
BASE: 9ceda8f5ef40d25e37f2963a8e8f5ff0a139b101

ACCEPTANCE: On first HTTP failure and invalid JSON, interactive controls stay disabled and the 11-row static source-backed chart table persists. Visible retry re-fetches the identical pinned JSON, validates before a one-time interactive bootstrap, and works without reloading the page. No-JavaScript sees no inert retry button. Verify desktop Chromium, source-free data invariants and PR CI before a later merge.

## Next user-visible milestone and compact queue

Milestone: recover Reader interactive controls after transient data failure without losing static evidence, then complete an independently measured second Robinson translation only after full historical body/rights gates pass.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 verified snapshot retry | 503 and invalid JSON fail closed; same-page retry recovers validated 11-edition UI | Fresh head Chromium/Pages, later-run acceptance |
| P2 | #511 complete Trusov body and paired comparison | Resolve Pages 2/148–151, verify rights, whole-body hashes, metric profiles and threshold | Historical rendering/edition evidence |
| P3 | #283 remaining mobile/keyboard acceptance | Actual built Reader keyboard/touch/focus/print checks | Browser evidence; no fake live verification |
| P4 | #282 AOT noun/cardinal discriminator experiment | Measured lexical/POS choices under pinned AOT without silent compatibility change | Pinned native runtime and legal samples |
| P5 | Rights-cleared new >=300k edition and #284 attribution | Independent reproducible derived measurements and explicit rights evidence | Rights and edition identity |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. Original four-book rhythm 1/4 holdout and ablation remain exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov historical EOF #436 and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 closed via #481, not recreated.
