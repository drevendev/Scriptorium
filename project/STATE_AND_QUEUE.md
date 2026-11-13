# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 512
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-13
LAST_RESULT: #525 merged at b96a0a714e3657c57d0b37add17341248535873b; #526 source-span provenance implemented on focused branch, later-run CI and acceptance pending.
LAST_VERIFIED_PROGRESS: 11 complete measured editions / 2 research leads plus a separate 145-Page Trusov **incomplete** projected excerpt; M2 0/5, FantLab analyzer-input identity UNKNOWN; M3 open.

## Current delivery and acceptance

UNIT_ID: SCRIP-TEXT-SOURCE-SPANS-V1
ISSUE: #526 optional normalized-to-original code-point span mapping
STATUS: BRANCH_COMMITTED; exact-head CI and independent later-run acceptance required
BRANCH: scrip-source-spans-20261113
BASE: b96a0a714e3657c57d0b37add17341248535873b

ACCEPTANCE: Opt-in local Python API maps normalized token/sentence ranges back to original coordinates; CRLF/NFC/Hangul and reordering cases are tested, ambiguous inverse mappings are explicitly marked, and default text-v1 metrics, Reader, corpus and reports are unchanged.

## Next user-visible milestone and compact queue

Milestone: reliable offline analysis and 11-book Reader with source-bound, human-readable exports; independently establish a complete Trusov literary body before any paired translation claim.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #526 optional original-coordinate span API | Local consumer and regression suite for Unicode provenance; independent CI/merge | Focused branch and later-run acceptance |
| P2 | #511 full Trusov body and two-translation comparison | Inspect opening/tail, resolve Page2 parser and Pages148–151 VAR, historically defensible page joins, verify rights/coverage/hashes before 29-metric comparison | Exact Page rendering/edition identity |
| P3 | #282 pinned AOT noun/cardinal N diagnostic | Measured native noun/cardinal samples and POS/bigram deltas; separately label uncertainty | Native pinned pylem dictionary; FantLab input still unknown |
| P4 | #283 Reader accessibility / visual issues | Real browser-observed defect, desktop/mobile/keyboard regression and reader-first results | Site build and visual execution |
| P5 | Separate rights-cleared >=300k edition, then #284 attribution guidance | Source-bound metrics and distinct rights/provenance; no unlicensed publication | Independently established whole-work rights and identity |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. Original four-book rhythm 1/4 holdout and ablation remain exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov historical EOF #436 and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 closed via #481, not recreated.
