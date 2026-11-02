# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 396
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-02
LAST_RESULT: PR #396 merged at 35f72c82df302fe1bf5c18b79fb3945ef97f43d2; this PR adds a pinned-source, source-free 150-Page content/transclusion-input preflight with positive/negative tests and CI. Live Page content capture and literary render/size remain unverified until exact-head run.
LAST_VERIFIED_PROGRESS: Master retains 11 measured Russian works, 298 fields (249 numeric, 49 unavailable), and the 150-Page Trusov historical graph frozen in Git (SHA-256 d2104ad33fc15ddb8479c13b9fdbe0abf94f8418e76c02261a803b79130ebaa4). This preflight checks each pinned Page revision/content and emits only source-free candidate hashes/markup counts; candidate is NOT a literary body. M2 0/5, M3 open; Pages live/browser/mobile NOT_VERIFIED.

## Current delivery and acceptance

UNIT_ID: SCRIP-TRUSOV-PINNED-CONTENT-PREFLIGHT
ISSUE: inspect 150 frozen historical Page contents, retain only derived hashes and markup diagnostics
STATUS: PR_CANDIDATE; FIXTURE_TESTS_IN_CI_PENDING; LIVE_CONTENT_NOT_RUN
BRANCH: scrip-trusov-pinned-page-content-preflight
BASE: 35f72c82df302fe1bf5c18b79fb3945ef97f43d2

ACCEPTANCE: verify full frozen graph and each pinned Page's oldid/page ID/title/timestamp/provider SHA-1 before inspecting its wikitext; reject missing, changed, duplicate or non-wikitext responses and unknown inclusion tags; source-free 150-page candidate hashes/markup inventory, no source prose or fabricated literary size/parity; positive and negative CI plus real-provider output before later merge. The diagnostic transclusion input retains unexpanded markup and explicit synthetic page joins: NOT literary body.

## Next user-visible milestone and compact queue

Milestone: add a second independently measured Russian Robinson Crusoe translation for an honest, source-bound paired Reader comparison.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Capture source-free pinned Trusov Page content preflight | Verify 150/150 oldid/page/title/SHA-1 and derived per-page candidate hashes/markup inventory, no prose; CI PASS | Requires frozen graph #396 (MERGED); MediaWiki content rate limit is scoped to live fetch |
| P2 | Resolve actual Trusov 1775 transclusion and freeze first narrative | Verified complete, normalized literary SHA-256, page-join/template semantics and >=300k gate | Depends on source-free pinned Page content preflight and print/body verification |
| P3 | Run Trusov 29 metrics and show honest translation pair in Reader | Distinct translation sources/profiles, diagnostic deltas and historical/French intermediary caveats | Requires accepted first-narrative body, not FantLab input identity |
| P4 | Reconcile stale Reader README and verify root Pages desktop/mobile | No stale PR-candidate/counter language; actual deployed browser flow and fallback evidence if allowed | HTTP browser historically ADMIN_BLOCKED; docs/structural tests independent |
| P5 | #282/#281 native AOT/FantLab compatibility | New measured POS-N discrimination or source-matched benchmark evidence | Primary dependency evidence still unresolved |


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
