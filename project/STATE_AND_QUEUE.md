# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 583
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-20
LAST_RESULT: #599 confirmed merged at ee66ed024a4c92a7a0d0ff8f6e9b229b993adb27; private lexical HTML/Markdown report validation proposed as a scoped #562 follow-on.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; M2 0/5, FantLab analyzer-input identity UNKNOWN.

## Current delivery and acceptance

UNIT_ID: SCRIP-LEXICAL-HUMAN-REPORT-GUARD-018
ISSUE: #562 versioned source-free private lexical comparison
STATUS: PR_CANDIDATE; exact-head CI and later independent acceptance pending
BRANCH: scrip-lexical-human-report-guard-20261120
BASE: ee66ed024a4c92a7a0d0ff8f6e9b229b993adb27

ACCEPTANCE: Re-rendered source-free lexical HTML/Markdown must reject forged text in numeric fields, nonfinite/overrange measurements, inconsistent type overlap, bad method profile IDs, incomplete witness fields and contradictory token warnings before emitting a readable report. Direct HTML entry also validates. Preserve valid old v1 reports, the original CSV byte output, empty/NOT_RUN cases, all compatibility metrics, rights, corpus and M2 0/5. Require hosted exact-head tests and later independent acceptance. Local/browser/live verification remains separate.

## Next user-visible milestone and compact queue

Milestone: Private offline lexical comparison produces readable, source-free outputs from validated measurements, not merely HTML-escaped arbitrary data.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #562 lexical HTML/Markdown fail-closed validation | Typed human-readable aggregate rows and metadata, legacy compatibility, positive/negative regressions | CI and later independent PR acceptance |
| P2 | #562 rights-verified public lexical comparison | Only edition-verified rights-cleared aggregate evidence; no word forms | Rights and edition identities |
| P3 | #511 Trusov second translation body | Independently complete historical literary body | Historical Page completeness |
| P4 | #282 pinned native AOT collision | Reproducible measured noun/cardinal bounds | Python 3.9/pylem native sidecar and source |
| P5 | #284 license/attribution release gate | Explicit software license and source/data rights publication checks | Rights holder evidence |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. Holdout/ablation and within-sample tests are exploratory, NOT external validation. Admission/author/parity requires >=300,000 characters INCLUDING spaces and reuse rights. No manuscripts in public artifacts; translation identities separate. AOT/pylem==0.0.18 noun/cardinal N collision unresolved. Source-unmatched resemblance is DIAGNOSTIC only; UNKNOWN is not zero, NOT_RUN is not PASS. Trusov EOF #436 and #265 controls remain scoped. Do not mutate hourly scheduler.
