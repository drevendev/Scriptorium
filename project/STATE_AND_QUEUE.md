# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 307
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-24
LAST_RESULT: #303 expanded in existing branch to a product-first Pages homepage with a verified frozen-book comparison; intended Pages URL linked prominently in README.
LAST_VERIFIED_PROGRESS: Reader package and Pages CI successful for this branch revision; full exact-head acceptance still required. Deployment / public browser availability NOT_VERIFIED.

## Current delivery and acceptance

```text
UNIT_ID:        SCRIP-SITE-015-PUBLIC-READER-SHOWCASE
ISSUES:         #283 (reader presentation) and #285 (deployment, scoped)
STATUS:         AUTHORED_PENDING_LATER_ACCEPTANCE
BRANCH:         scrip-site-015-metric-family-jumps
BASE:           86efa80dd3ef529ed81803bbe036c53301674698
ACCEPTANCE:     Main screen uses the actually frozen Grin/Verne derived
                comparison for three labelled quantitative charts and an exact
                accessible table. Clickable real-work, private comparison and
                FantLab evidence routes, 28-row family navigation and mobile /
                keyboard / print checks all retained. README links intended URL
                and states that Pages is NOT LIVE_VERIFIED. Same-run merge not
                authorized; read exact-head CI before later acceptance.
```

## Next user-visible milestone and compact queue

Milestone: a coherent real-work Reader homepage on an actually public GitHub Pages
URL, without claiming FantLab source identity or scientific parity.

| Priority | Unit | Deliverable and acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #283 real-work Pages UX | Exact-head CI, canonical artifact link/desktop/mobile acceptance and later qualifying #303 merge | Authored PR, later-run merge |
| P2 | #285 publish Pages | Admin enables Pages GitHub Actions source and existing deployment variable; deploy reviewed master via existing workflow and verify public URL | Repository admin permission, not a code blocker |
| P3 | #281 scientific evidence | Four currently NOT_RUN measured works with unchanged source/rights/rounding gates | Source identity and legally usable witness |
| P4 | #282 AOT ambiguity | Measured noun/cardinal N regression; no guessed semantic mapping | Pinned provider evidence |

#284 source-code/data licensing remains an independent legal gate. The user requested
a working public Pages experience; a working GitHub Actions build is NOT deployment.
M2 0/5, M3/M4/M5 and the corpus/legal/privacy constraints are unchanged.

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
