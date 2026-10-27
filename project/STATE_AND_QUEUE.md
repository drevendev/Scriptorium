# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 334
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-27
LAST_RESULT: PR #332 merged at 6098ce582ed7d06b9dbaec82a75957ac779a601e; branch Pages deploy succeeded. This PR proposes Russian-first ten-title catalogue, six measured works, translator/edition identities and two-work comparison. Proposed UI/data are not yet merged.
LAST_VERIFIED_PROGRESS: Root Pages currently shows four measured works (113 rows); new branch proposal expands to six measured Russian-language works (153 fields, 129 actuals, 24 unavailable) plus four explicitly pending catalogue records. Full Python-generated Reader remains narrower. FantLab source identity unknown; M2 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-SITE-RU-010-TRANSLATION-READER
ISSUES: #281, #283, #285 (partial)
STATUS: AUTHORED_PENDING_CI_AND_LATER_ACCEPTANCE
BRANCH: scrip-site-021-ru-first-translators-ten-books
BASE: 6098ce582ed7d06b9dbaec82a75957ac779a601e
ACCEPTANCE: Every one of the ten catalogue entries is a unique Russian-language edition/source identity; six have unchanged measured metrics and pinned witnesses, four remain preparation/NOT_RUN rather than being called analyzed. Preserve all 29 Hyperboloid CI rows with original artifact checksum, the verified 11 Beketova translation observations and explicit translator/original-language/edition relations. An active side-by-side normalized comparison works only for two measured works sharing a pinned profile. No fake English/French originals, no unsupported translation effects, no manuscript text, no M2 claim. Build root Pages, exact-head tests, desktop/mobile browser verification where available, and independent later-run acceptance before merge.

## Next user-visible milestone and compact queue

Milestone: Russian-first Reader with genuinely measured originals/translations, provenance-aware comparisons, and ten separate edition entries without pretending unfinished works are analyzed.

| Priority | Unit | Deliverable | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Current Russian Reader PR | Later accept source-verified six-book interactive Pages release, ten-title catalogue, translator identity and charts | Exact-head CI and review; branch Pages deploy after merge |
| P2 | #281 Hyperboloid retention in generated Reader | Reuse reviewed source-free 29 fields in the Python multi-route matrix/exports | Artifact is available; update existing manifest with separate semantic PR |
| P3 | Resurrection measured diagnostic | Replay the independently frozen 129-revision Tolstoy body for versioned candidate metrics | Source-provenance/rights gate; exact replay, no FantLab parity claim |
| P4 | Road to Nowhere alternate text | Validate alternate complete body and create measured source-free profile without collapsing with incomplete primary edition | Source integrity and rights; raw/normalized hashes |
| P5 | Translation/original module | Analyze a rights-clear French original of Verne and an English Darwin original in **separate language profiles**, then compare version-pairs only on meaningfully commensurable features | Original identity, legal provenance, separate tokenization/morphology and test corpus |

M2: 0/5 unchanged. A six-work measured Russian showcase is *not* FantLab parity completion or M5. Four pending titles remain catalogued but not analyzed. The existing hourly job remains unchanged.

## Retained evidence and scientific gates

Immutable detail remains in `corpus/candidates/`, `benchmarks/`, `showcase/`,
`project/run-receipts/`, `project/CHANGELOG.md` and `CHANGELOG.d/`. Reread the relevant
candidate records before acting; this delivery does not recalculate, admit or relabel works.

- Anna Karenina: 239 pinned revisions, 1,705,605 characters; source identity unknown.
- Resurrection: 129 revisions, 890,835 characters; source identity unknown.
- Brothers Karamazov: 98 admitted revisions, 1,810,351 characters; source identity unknown.
- Silver Dove: 563,125 characters; source identity unknown.
- Hyperboloid: frozen 499,066-character body and source-free measured CI receipt (24 actual / 5 NOT_RUN); future generated Reader retention still pending; print/FantLab identity unresolved.
- Running on Waves: frozen 363,819-character body and diagnostics; denominator resemblance is hypothesis only.
- Children of Captain Grant / Alexandra A. Beketova: frozen 1,095,467-character Russian translation and 11 measured derived fields; distinct from French original/other translations, no FantLab result/input identity.
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
- #285 Pages: GitHub has_pages=true; branch master/root deployment succeeded at 6098ce58. The separate artifact-deploy workflow interlock remains unchanged. A newly authored root UI is PR_CREATED, not LIVE_VERIFIED until merged and publicly checked.
- #284 licensing: do not infer a code/data license or publish externally before the rights gate is resolved.
- Local checkout: Git DNS failed; exact source blobs were recovered and verified for actual local tests. Hosted full-repository CI supplies complete integrated execution evidence, not the limited local closure.
- Browser HTTP navigation returned ERR_BLOCKED_BY_ADMINISTRATOR. Current visual changes are VISUAL_NOT_VERIFIED; structural tests are not live browser acceptance. Continue other executable work without bypassing the restriction.
