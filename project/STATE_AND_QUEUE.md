# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 377
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-31
LAST_RESULT: #376 merged as e9ae1265e47a06ea62689887ce291620dc68f527. New Reader pair-coverage PR shows both observed and unavailable dialogue sentence-length metrics without altering any source measurements or parity gates.
LAST_VERIFIED_PROGRESS: Ten source-bound measured Russian works in master Reader; 269 metric rows (225 numeric, 44 unavailable). FantLab input identity remains UNKNOWN (M2 0/5; M3 open). Live browser/mobile verification is NOT_VERIFIED.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-PAIR-COVERAGE
ISSUE: #283 literary Reader and comparison accessibility.
STATUS: PR_READY_FOR_LATER_ACCEPTANCE
BRANCH: scrip-reader-pair-coverage
BASE: e9ae1265e47a06ea62689887ce291620dc68f527

ACCEPTANCE: In root Reader, each same-profile pair shows nine eligible normalized metrics including missing cells explicitly as «нет данных» and no fabricated delta; a missing metric's chart displays an unavailable message. The two additional sentence-length charts work for measured books. Existing JSON/CSV schemas export only jointly measured numbers, retaining edition and translator evidence. Preserve 10-book catalog, 269 measurements, no-JS initial table, M2 0/5; Node positive/negative, Python structure, exact-head CI and later independent acceptance required.

## Next user-visible milestone and compact queue

Milestone: Russian Reader with complete, honest side-by-side comparison of nine compatible measures and reproducible source-free provenance.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Later accept and merge pair-coverage PR | Exact-head CI, nine rows with two honest Beketova gaps, correct two new charts, unchanged numeric export schemas | Later wake and passing checks |
| P2 | Verify current Reader at live Pages | Latest master deployment and live HTML/CSV, desktop/mobile/keyboard | Existing HTTP/browser administrator restriction |
| P3 | #282 native N discriminator | Source-backed measured noun/cardinal distinction with negative controls | Public adapter loses source enum |
| P4 | #281 source-matched FantLab benchmark | Actual analyzer-input identity and per-field rounding evidence | Identity UNKNOWN |
| P5 | Distinct measured Russian translation edition | Rights, translator/edition IDs, normalized same-language comparison | Need independently frozen second edition |

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
