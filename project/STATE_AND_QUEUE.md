# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 539
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-16
LAST_RESULT: #553 natively merged at 8fcc3a8c54afb4cdfc3c9b3486e0607b20d7faf8; #283 evidence-type separation selected to distinguish measured books from comparisons without changing scientific status.
LAST_VERIFIED_PROGRESS: 11 complete measured editions / 2 research leads and a separate incomplete 145-Page Trusov projected excerpt; M2 0/5, FantLab analyzer-input identity UNKNOWN.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-GALLERY-EVIDENCE-TYPE-FACETS
ISSUE: #283 — distinguish measured full-work reports from comparisons in evidence browsing
STATUS: PR_CANDIDATE; later exact-head CI/Chromium and independent acceptance required
BRANCH: scrip-gallery-evidence-type-separation-20261116
BASE: 8fcc3a8c54afb4cdfc3c9b3486e0607b20d7faf8

ACCEPTANCE: Separate genuine full-work measurements from pairwise comparison cards in the gallery evidence-type filter; retain current excerpts and provenance-only categories, source-backed cards, Cyrillic/romanized title-author search, keyboard and no-JS fallback. Positive and negative Python/Chromium regression tests must exercise the built gallery. Classification only, no changes to scientific metrics, source rights, corpus or FantLab parity.

## Next user-visible milestone and compact queue

Milestone: enable accurate, discoverable measured-book reading and a legally supportable Trusov/Shishmareva comparison when historical source coverage can be proven.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 distinguish measured-book and comparison facets | Built gallery shows mutually exclusive full-work vs comparison cards, with real Chromium checks; retain Romanized search and no-JS fallback | Existing #551 browser acceptance gate |
| P2 | #511 recover actual Page 2/148–151 rendering | Verified whole translation body/rights/coverage, not another seam hypothesis | Exact 2023 template/transclusion semantics and frozen oldids still unresolved |
| P3 | #282 AOT noun/cardinal experiment | Native versioned ambiguity evidence, no guessed POS mapping | Pinned AOT runtime |
| P4 | #284 independent rights-cleared >=300k new edition | Concrete explicit reuse permission and independently measured source | Legal/edition proof |
| P5 | #283 Reader print/keyboard/accessibility follow-up | Real built desktop/mobile and no-JS evidence | Deduplicate against merged checks before selecting |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. Original four-book rhythm 1/4 holdout and ablation remain exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov historical EOF #436 and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 closed via #481, not recreated.
