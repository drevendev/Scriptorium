# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 362
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-30
LAST_RESULT: #361 merged as e2653667de1a7224e2d1d198dd4923e22aeb8bb8; branch Pages run 40999630626 succeeded on that exact head. Static source-bound CSV fallback authored for later acceptance.
LAST_VERIFIED_PROGRESS: 8/10 measured in master; 211 fields (177 numeric, 34 NOT_RUN/unavailable), M2 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-042-STATIC-MEASUREMENT-CSV
ISSUE: #283 accessible Reader.
STATUS: AUTHORED_PENDING_LATER_ACCEPTANCE
BRANCH: scrip-site-042-static-source-bound-csv
BASE: e2653667de1a7224e2d1d198dd4923e22aeb8bb8
ACCEPTANCE: Public root Reader provides a complete, source-free UTF-8 BOM CSV to users without JavaScript (and as a fallback if interactive validation cannot start). The committed 211-row artifact must be byte-for-byte identical to the validated 8-edition browser export (177 numeric, 34 status-only rows), preserve translator/edition/source digests and DIAGNOSTIC_ONLY/M2 0/5, be spreadsheet-formula safe, and never include pending candidates or source prose. Existing smoke must fail on static/serializer drift and missing fallback link. Later fresh exact-head CI, acceptance and qualifying merge required.

## Next user-visible milestone and compact queue

Milestone: Make all eight measured books and their 211 fields genuinely accessible even without JavaScript, then expand independent licensed literary bodies.

| Priority | Unit | Deliverable | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 Reader static CSV | Review/test and merge no-JavaScript CSV fallback, byte-identical to live serializer | Fresh exact-head CI |
| P2 | #285 Pages | Confirm publication of static fallback; HTTP/mobile/keyboard acceptance only if permitted | Browser/HTTP restriction |
| P3 | #283 ninth/tenth works | Prepare independently licensed source bodies and run reproducible analyzer (Petersburg/Darwin) | Body/rights gates still open |
| P4 | #281 FantLab parity | Identify exact analyzer-input edition and displayed rounding without weakening acceptance | FantLab input undisclosed |
| P5 | #282 morphology | Quantify unresolved noun/cardinal N with preserved ambiguity bounds | Original AOT enum unavailable |

PR #361 and its exact-head Pages workflow are successful, but direct live HTTP/visual evidence is still unavailable; this static CSV is a proposed new feature until merged and published. Road measurements are DIAGNOSTIC for an alternate source family. The perpetual hourly task remains unchanged.

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
