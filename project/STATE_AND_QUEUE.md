# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 501
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-12
LAST_RESULT: #513 native MERGED at 359b2381def5777d050d0539c5311d7c7802787b; #285 closed after GitHub-hosted exact-byte/Chromium LIVE_VERIFIED at this master (runs 43274480335 and 43274481129). The independent public-browser environment could not resolve the host.
LAST_VERIFIED_PROGRESS: 11 measured editions / 2 research leads; FantLab analyzer-input identity UNKNOWN; M2 0/5; M3 open; no new corpus measurements.

## Current delivery and acceptance

UNIT_ID: SCRIP-CORPUS-TRUSOV-VAR-CR-BREAK-BOUND-V4
ISSUE: #511 measured Trusov translation; narrow historical-Page projection correctness slice, NOT the literary body
STATUS: PR_CREATED; LATER_RUN_ACCEPTANCE_REQUIRED
BRANCH: scrip-trusov-var-line-break-bounds-20261112
BASE: 359b2381def5777d050d0539c5311d7c7802787b

ACCEPTANCE: Reject a VAR candidate exceeding twelve logical line breaks regardless of LF, CRLF, or bare CR. CRLF counts as one break; a call with twelve breaks remains a source-free *inferred* preview. Positive/negative regression tests, unchanged pinned-150-page source identities, exact-head CI and a later-run review are required before merge. This closes a bounded historical newline semantics bug, NOT #511's body-only extraction/measurement, Page joining or FantLab parity.

## Next user-visible milestone and compact queue

Milestone: measure the rights-cleared 1775 Trusov literary body to expose an honestly qualified historical-vs-modern Russian translation comparison; preserve the already live, functional Reader.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Accept/fix historical VAR logical-line-break bound in #511 slice | Exact-head tests, pinned Page-source workflow and later-run qualifying merge | Provider access for actual 150-Page capture; no dependence for local unit regressions |
| P2 | #511 body-only historical Trusov extraction and 29-field analysis | Independent section/volume boundary evidence; rights + hashes; >=300k character body; derived no-prose metrics; comparison caveats | Historical template/VAR/transclusion and Page joins; never infer body from Page graph |
| P3 | #282 pinned AOT N collision diagnostic | Native noun/cardinal evidence, exact toolchain and bounded POS deltas | Native pylem dictionary; FantLab exact input still unknown |
| P4 | #283 Reader accessibility / presentation issues | Actual browser-visible defect + regression; maintain live acceptance | Existing real Chromium screenshots and root Reader |
| P5 | A different legally licensed >=300k edition, then #284 release attribution | Source hash, measured metrics and legal/edition facts; #284 still needs owner license grant | Independent full-text body and rights; no code-license presumption |

## Retained scientific and operational boundaries

M0 closed; M1 open; M2 0/5; M3/M4/M5 open. Eleven measured editions; two research leads. Original four-book rhythm 1/4 holdout and ablation remain exploratory source-bound extensions; new six-book 2/6 is also within-sample, NOT external validation. Calibration/author/parity works require >=300,000 characters INCLUDING spaces and explicit reuse rights. No published manuscripts. Translation identities remain separate. AOT/pylem==0.0.18 noun/cardinal runtime N collision remains unresolved. Source-unmatched numeric similarity is DIAGNOSTIC, not parity; UNKNOWN is not zero, NOT_RUN is not PASS.

#284 rights grant, Trusov historical EOF #436 and #265 branch protection/cleanup remain scoped, not global prerequisites. Do not mutate perpetual hourly scheduler. Earlier Drive leads deduplicated: Compare003 already in compare.py (#279), POS distributions tracked through #287, CORPUS-087 reconciled to #422; distinct schema-publication lead #479 closed via #481, not recreated.
