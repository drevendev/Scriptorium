# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 367
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-30
LAST_RESULT: PR #366 merged at master 601e1ee298b6cabd6bbab08752994604e88d568f. Hosted exact-revision Oblomov measurement replay passed; derived 29-field snapshot (24 numeric, 5 NOT_RUN) retained in this PR; independent later-wake acceptance and Reader integration outstanding; M2 0/5.
LAST_VERIFIED_PROGRESS: 8/10 full Russian works measured; 211 fields (177 numeric, 34 unavailable), M2 0/5; M3 open.

## Current delivery and acceptance

UNIT_ID: SCRIP-CORPUS-088-OBLOMOV-MEASURED
ISSUE: #281 evidence boundary; #283 reader catalogue.
STATUS: CI_MEASURED_SNAPSHOT_RETAINED_IN_PR_PENDING_LATER_ACCEPTANCE
BRANCH: scrip-corpus-088-oblomov-measured
BASE: 601e1ee298b6cabd6bbab08752994604e88d568f

ACCEPTANCE: For the public-domain Russian original Goncharov's Oblomov, replay Wikisource az.lib.ru exact revision oldid 5724579 transiently, reject changes in rights, source digest, four-part 46-chapter inventory and literary-body boundaries. Verify >=300,000 characters including spaces and produce real deterministic 29-field JSON with source/body hashes, profiles, five NOT_RUN dictionary fields and no source text. Hosted oldid 5724579 run #41077141367 confirmed 930248 characters, 147447 words and 24/29 numeric fields; source SHA-256 fb3e3817792ed1769aa5cd9cc5b33a8326c56ff76007ca92331ac9fad516b394; retained derived snapshot must match every fresh replay. Reader still has only eight measured works until the snapshot is later accepted and integrated. No established FantLab input/edition match, hence DIAGNOSTIC_ONLY and M2 0/5.

## Next user-visible milestone and compact queue

Milestone: Publish a verified ninth fully measured Russian book from a rights-cleared full-text witness, with distinct edition identity and inspectable reader results, while maintaining source-matched FantLab research independently.

| Priority | Executable unit | User-visible acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #281 / #283 Oblomov exact-source measurement | Source/body hashes, 29 honest fields, positive/negative regressions, source-free CI artifact | Current PR measured/replayed; later-run independent acceptance plus historical-data CI equality |
| P2 | #283 ninth Reader book | After acceptance, add 930248-character Oblomov retained results to Reader with detail/charts and provenance | Requires P1 source/body evidence and rights/completeness verification |
| P3 | #281 strict FantLab benchmark | Field-by-field provenance and unmatched-source diagnostics with unchanged rounding rules | FantLab analyzer input unknown |
| P4 | #282 AOT N ambiguity | Native noun/cardinal uncertainty diagnostics under pinned pylem | Dictionary/runtime evidence |
| P5 | #285 Pages live UX | Actual desktop/mobile HTTP, keyboard and route validation | Browser tool may block; structural CI remains executable |

Previous #366 range plots are merged in master; do not re-review unchanged heads. Master currently has 8 measured books / 211 fields; public Pages direct live/browser verification remains incomplete.

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
