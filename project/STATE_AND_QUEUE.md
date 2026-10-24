# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 313
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-24
LAST_RESULT: #308 merged at 74c202f121db44bb504cd2a9d6cabcd7e3c4cc06. Authored a scoped #281 Reader source-provenance and count view.
LAST_VERIFIED_PROGRESS: Existing five-work readiness already preserves source hashes, edition/rights records and diagnostic count deltas, but the canonical Reader evidence page only showed metric run states. Proposed source-bound Reader annotations expose those diagnostics without modifying metrics; exact-head CI and later acceptance pending.

## Current delivery and acceptance

UNIT_ID: SCRIP-REPRO-010-SOURCE-COUNT-READER
ISSUES: #281 (open; partial)
STATUS: AUTHORED_PENDING_LATER_ACCEPTANCE
BRANCH: scrip-repro-010-source-count-reader
BASE: 74c202f121db44bb504cd2a9d6cabcd7e3c4cc06
ACCEPTANCE: Display five independently validated source/edition/rights witnesses and frozen-vs-FantLab displayed character deltas in the canonical Reader, alongside existing metric evidence. Fail closed on inconsistent digest, dates, count arithmetic or unsafe source URLs. Keep scientific input match UNKNOWN, old machine exports unchanged and M2 0/5; require exact-head CI and later-run independent acceptance before merge.

## Next user-visible milestone and compact queue

Milestone: Reader users can inspect five-work source provenance and quantitative diagnostics next to the 28 retained FantLab metric rows without mistaking counts for parity.

| Priority | Unit | Deliverable | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #281 Five-work provenance Reader | Verify real canonical site build/links, later accept the Reader source/count slice | Exact-head hosted CI; no FantLab input match assumed |
| P2 | #281 Strict source-bound benchmark | Additional legally usable source-and-reference-bound field-level runs; absent metrics remain NOT_RUN | Established actual input editions and rounding evidence |
| P3 | #283 Reader visual acceptance | Real desktop/mobile/print browser checks when supported | Browser access; structural checks otherwise |
| P4 | #285 Pages publication | Authorized Pages activation and live verification | Repository admin and #284 rights |
| P5 | #284 licensing | Explicit source-code license and attribution approval | Owner/rights-holder decision |

M2 remains 0/5. Corpus, privacy, scientific and provenance gates unchanged.

## Retained evidence and scientific gates

Immutable detail remains in `corpus/candidates/`, `benchmarks/`, `showcase/`,
`project/run-receipts/`, `project/CHANGELOG.md` and `CHANGELOG.d/`. Reread the relevant
candidate records before acting; this delivery does not recalculate, admit or relabel works.

- Anna Karenina: 239 pinned revisions, 1,705,605 characters; source identity unknown.
- Resurrection: 129 revisions, 890,835 characters; source identity unknown.
- Brothers Karamazov: 98 admitted revisions, 1,810,351 characters; source identity unknown.
- Silver Dove: 563,125 characters; source identity unknown.
- Hyperboloid: frozen 499,066-character body; print/FantLab identity unresolved.
- Running on Waves: frozen 363,819-character body and diagnostics; denominator resemblance is hypothesis only.
- Children of Captain Grant / Beketova: frozen 1,095,467-character body and derived metrics; no FantLab result/input identity for this translation.
- Aelita and We: published FantLab inputs are below 300k; zero M2 weight. We's public body remains separately unfrozen.
- Petersburg: exact 632-page 1916 PDF and OCR/body contract; literary selection, body, size and identity gates remain open.
- Shining World is incomplete; Road to Nowhere has a >=300k alternate frozen route but no FantLab identity; White Guard mixes source families; Twelve Chairs retains unresolved template/body semantics; Klim Samgin retains unresolved historical-renderer/FantLab equivalence.
- Darwin/Rachinsky: SCRIP-CORPUS-078 through 084 retain zero-argument yo, references containment, VAR documentation/provider drift and six-revision identity evidence, not full historical replay/body/parity. Effective unresolved surface remains 4 tag shapes/130 tokens and 37 template shapes/2,356 invocations.
- Perelman 1913: SCRIP-CORPUS-085 exact-PDF anchors include carrier 60 without a directly visible folio. Sampled +9 compatibility cannot establish total/global mapping, PDF/DjVu equivalence, OCR/body/size or FantLab identity. Do not interpolate missing folios arithmetically.

M0 is closed; M1 remains open. General/dialogue/vocabulary/punctuation metric families are
executable inferred candidates. POS has separate work-page-compatible and diagnostic-only
surfaces. `pylem==0.0.18` remains pinned; runtime N noun/cardinal ambiguity is unresolved.
FantLab dictionary/version, homonym selection, word boundaries, service-word aggregation,
corrective coefficients and some dialogue/denominator semantics remain unknown. The Anna
word gap and dash-rate parity are unresolved; punctuation-v2's internal-hyphen correction
is not new evidence of parity.

M2 stays **0/5**: five independent legally usable works >=300,000 characters including
spaces, established source edition/analyzer-input identity, required published compatible
metrics after displayed rounding, and explicit unchanged equality/tolerance rules. Unmatched
comparisons remain diagnostic. Unknown is not zero, NOT_RUN is not PASS. M3/M4/M5 retain their
own manifest gates. Short excerpts/fixtures do not count as corpus admission.

## Scoped operational blockers

- #265: default-branch rules prevent deletion/non-fast-forward and require PRs, with zero required approvals in the read ruleset. Connector identity has push/triage, not admin. No unsupported deletion/settings mutation or ref bypass.
- #285 Pages: repository reports has_pages=false. Deployment configuration interlock remains untouched. BUILT is not DEPLOYED or LIVE_VERIFIED; missing administration blocks activation only.
- #284 licensing: do not infer a code/data license or publish externally before the rights gate is resolved.
- Local checkout: Git DNS failed; exact source blobs were recovered and verified for actual local tests. Hosted full-repository CI supplies complete integrated execution evidence, not the limited local closure.
- Browser HTTP navigation returned ERR_BLOCKED_BY_ADMINISTRATOR. Current visual changes are VISUAL_NOT_VERIFIED; structural tests are not live browser acceptance. Continue other executable work without bypassing the restriction.
