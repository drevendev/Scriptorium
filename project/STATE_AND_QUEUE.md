# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 308
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-10-24
LAST_RESULT: #303 merged at d934473e417627a2e6b1e6fb36e033112f9764cc. EPUB follow-up to merged #296 now preflights known collisions across the report and separate provenance receipt before either create-only write; related tests and docs are on a focused PR branch.
LAST_VERIFIED_PROGRESS: Branch file writes/readback verified; exact-head CI and later-run acceptance pending for this EPUB change. Master Reader and site builds passed after #303; Pages deployment/live URL not verified.

## Current delivery and acceptance

```text
UNIT_ID:        SCRIP-INGEST-EPUB-DUAL-OUTPUT-PREFLIGHT
ISSUES:         #289 (closed; narrowly scoped post-merge regression)
STATUS:         AUTHORED_PENDING_LATER_ACCEPTANCE
BRANCH:         scrip-epub-dual-output-preflight
BASE:           d934473e417627a2e6b1e6fb36e033112f9764cc
ACCEPTANCE:     One EPUB invocation requesting report and provenance rejects
                identical/aliased paths, existing receipt and dangling symlink
                before either write. Fresh report + sidecar still work, and
                no existing output is overwritten. These two independent
                writes remain nontransactional under late I/O failures/races.
                Require exact-head CI and later-run review before merge.
```

## Next user-visible milestone and compact queue

Milestone: dependable private EPUB -> 29-metric Reader report + source-free
provenance, alongside the existing source-free real-book showcase; public Pages
activation is independent and currently requires repository administration.

| Priority | Unit | Deliverable and acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | #289 follow-up: EPUB dual-output safety | Accept current PR after exact-head tests/checks; existing sidecar or path aliases must not create partial new report | Later-run acceptance for current branch |
| P2 | #283 Reader visual usability | Real built-route desktop/mobile/keyboard and print verification and any measured fixes; preserve already merged #303 showcase | Browser navigation limitation; independent checks allowed |
| P3 | #285 publish Pages | Admin enables Pages GitHub Actions source and deployment variable; deploy reviewed master, verify public URL | Repository admin permission; not an analyzer blocker |
| P4 | #281 FantLab evidence | Obtain an independently lawful, exact-identity witness and one fresh metric run; keep four NOT_RUN works explicit until then | Source/input identity and executable witness |
| P5 | #282 AOT ambiguity | Measured noun/cardinal runtime N collision experiment with pinned provider; do not guess bucket assignment | Reproducible pinned provider evidence |

#284 code/data licensing remains an independent legal release gate. M2 stays
0/5; M3/M4/M5 and corpus/rights/privacy gates are unchanged. The #303 merge
does not prove a live Pages route; branch #303 is not a renewed open PR.

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
