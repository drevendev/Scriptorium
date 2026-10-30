# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 369
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-30
LAST_RESULT: Ninth Russian Reader book *Oblomov* was merged in #368 at master e7dc72081bf94e1df610bd08ec510104a4af3911. Proposed tenth full-source diagnostic targets Dostoevsky's *Humiliated and Insulted*, immutable Wikisource oldid 5611473. Actual exact-revision measurement and admission remain NOT_RUN until hosted verification.
LAST_VERIFIED_PROGRESS: Nine Russian works measured and shown in the master Reader; 240 retained fields (201 numerical, 39 unavailable). Tenth candidate is NOT an additional counted work. M2 remains 0/5; M3 open.

## Current delivery and acceptance

UNIT_ID: SCRIP-CORPUS-090-HUMILIATED-MEASURED
ISSUE: #281 reproducible field evidence; #283 Reader delivery.
STATUS: PR_CANDIDATE_PENDING_REAL_REPLAY_AND_LATER_REVIEW
BRANCH: scrip-corpus-090-humiliated-measured
BASE: e7dc72081bf94e1df610bd08ec510104a4af3911

ACCEPTANCE: Pinned oldid 5611473 source must identify Russian public-domain Dostoevsky, all four parts (15+11+10+9 chapters) and epilogue; exclude editorial commentary and confirm start/end anchors and >=300,000 actual characters including spaces. Hosted replay must yield a source-free, versioned 29-field JSON artifact with hashes and 5 NOT_RUN dictionary fields, no original prose. Do not count a tenth measured work until exact-source CI and independent acceptance pass. Print collation and FantLab input UNKNOWN, M2 weight 0. Retain only derived evidence in repository via later PR; Reader admission requires separately verified integration and Pages gate.

## Next user-visible milestone and compact queue

Milestone: Publish a tenth *actually measured* Russian novel with source hashes and a source-free Reader card, while keeping full FantLab parity unresolved.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Source-free tenth work replay | Exact oldid, rights, 52 ordered headings, full body and 29-field artifact from hosted CI | Real wikitext/replay; NOT_RUN until observed |
| P2 | Retain and publish verified tenth results | Separate later-run acceptance, immutable digests/values, Reader charts/CSV and no-JS table | Actual successful P1 evidence |
| P3 | #281 strict FantLab benchmark | Source-unmatched field-level diagnostics, explicit edition and rounding evidence | FantLab analyzer input UNKNOWN |
| P4 | #285 Pages live UX | Independent HTTP, keyboard, desktop/mobile and CSV download acceptance | Browser navigation restricted; existing CI independently checks structure |
| P5 | #282 AOT N ambiguity | Native noun/cardinal conditional bounds under pinned pylem | Dictionary/runtime evidence |

## Retained evidence and scientific gates

Immutable detail remains in `corpus/candidates/`, `benchmarks/`, `showcase/`,
`project/run-receipts/`, `project/CHANGELOG.md` and `CHANGELOG.d/`. Reread the relevant
candidate records before acting; this delivery does not recalculate, admit or relabel works.

- Anna Karenina: 239 pinned revisions, 1,705,605 characters; source identity unknown.
- Resurrection: 129 revisions, 890,835 characters; source identity unknown.
- Brothers Karamazov: 98 admitted revisions, 1,810,351 characters; source identity unknown.
- Silver Dove: 563,125 characters; source identity unknown.
- Hyperboloid: frozen 499,066-character body and source-free measured CI receipt (24 actual / 5 NOT_RUN); root Reader retention verified in master; print/FantLab identity unresolved.
- Running on Waves: frozen 363,819-character body and diagnostics; denominator resemblance is hypothesis only.
- Children of Captain Grant / Alexandra A. Beketova: frozen 1,095,467-character Russian translation and 11 measured derived fields; distinct from French original/other translations, no FantLab result/input identity.
- Aelita and We: published FantLab inputs are below 300k; zero M2 weight. We's public body remains separately unfrozen.
- Petersburg: exact 632-page 1916 PDF and OCR/body contract; literary selection, body, size and identity gates remain open.
- Shining World is incomplete; Road to Nowhere has 442,656 frozen alternate characters and 24 measured plus 5 NOT_RUN rows (Reader merged, FantLab input identity UNKNOWN); White Guard mixes source families; Twelve Chairs retains unresolved template/body semantics; Klim Samgin retains unresolved historical-renderer/FantLab equivalence.
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
- #285 Pages: #360 is now merged into master. Live HTTP and desktop/mobile visual verification remain blocked/unverified despite earlier successful root deployments. Do not infer current LIVE_VERIFIED from CI.
- #284 licensing: do not infer a code/data license or publish externally before the rights gate is resolved.
- Local checkout: Git DNS failed; exact source blobs were recovered and verified for actual local tests. Hosted full-repository CI supplies complete integrated execution evidence, not the limited local closure.
- Browser HTTP navigation returned ERR_BLOCKED_BY_ADMINISTRATOR. Current visual changes are VISUAL_NOT_VERIFIED; structural tests are not live browser acceptance. Continue other executable work without bypassing the restriction.
