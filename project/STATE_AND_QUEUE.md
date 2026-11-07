# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 447
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-07
LAST_RESULT: GitHub confirms #451 MERGED. #452 produced the first full-book Anna word-boundary experiment in hosted run 42331164429 at PR head 3ccd96bfb29a37820da50f0c9895c9714fead7b7; the immutable source-free receipt was committed for later acceptance.
LAST_VERIFIED_PROGRESS: 11 measured / 2 leads; six source-unmatched word-density diagnostics; Anna pinned 239-revision boundary replay PASS at head 3ccd96b; seven one-factor results saved, M2 0/5.

## Current delivery and acceptance

UNIT_ID: SCRIP-REPRO-ANNA-PINNED-WORD-BOUNDARIES-v1
ISSUES: #281 tokenizer/source-unmatched diagnostic (partial)
STATUS: PR_CANDIDATE; FULL_REPLAY_PASSED_AT_EARLIER_HEAD; NEW_EXACT_HEAD_CI_REQUIRED; LATER_ACCEPTANCE_REQUIRED
BRANCH: scrip-anna-pinned-boundary-replay-20261107
BASE: cad8a05605453860ef46b1629d960e16d545ac85

ACCEPTANCE: Opt-in `--with-boundary-probe` on the existing `scriptorium.repro_diagnostic`
replay reuses the *same*, legally usable 239-revision Anna composite after
source identity validation, then emits a source-free seven-variant count
diagnostic in the existing CI artifact. No second source fetch. Cross-check
normalization SHA/character count against pinned manifest and baseline/numeric/
Unicode-hyphen counts against both the contemporaneous policy computation and
older frozen independent evidence. Test opt-in/off behavior, one-factor cases,
identity mismatch, inconsistent baseline and secrecy. The hosted run 42331164429 passed on PR head 3ccd96b and validated normalized
SHA-256 1dcf2af8..., 1,705,605 characters and all 239 revisions. Results:
269,358 baseline; splitting ASCII lexical hyphens +1,611, curly apostrophes
+46, straight apostrophes 0, joining U+2010/U+2011 0, merging dotted
initialisms 0, excluding decimal-only words −17. Derived artifact committed
at benchmarks/fantlab/work270306-word-boundaries.json, to be rechecked in
fresh exact-head CI. Source matching to FantLab remains UNKNOWN; M2 stays 0/5.

## Next user-visible milestone and compact queue

Milestone: reproducible local analyzer plus a public Russian Reader displaying
measured works and honestly labelled FantLab diagnostic differences.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Later accept/merge pinned Anna full-work boundary experiment (#281, PR #452) | Fresh exact-head CI on retained receipt, source/provenance diff and tests; qualify merge, verify master | Hosted provider/API and CI |
| P2 | Reader explanation of real full-work boundary deltas | Source-backed per-policy values, units, accessible table/chart and unknown FantLab edition warning | P1 merged result; separate visible slice |
| P3 | #283/#285 Pages live/public acceptance | HTTP, desktop/mobile focus, actual routes | Browser restriction previously observed |
| P4 | Trusov first-narrative body and independent translator measurement | Legal >=300k text, 29 metrics and edition witness | Historical render/Page seams |
| P5 | #284 code/data rights and attribution | Evidence-backed license/attribution before external publication | Rights/owner evidence |

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
- Shining World is incomplete; Road to Nowhere has 442,656 frozen alternate characters and 24 measured plus 5 NOT_RUN rows (Reader merged, FantLab input identity UNKNOWN); White Guard mixes source families and has 20 captured/replayed identity rows adopted by merged #422, not a measured body; Twelve Chairs retains unresolved template/body semantics; Klim Samgin retains unresolved historical-renderer/FantLab equivalence.
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
- #285 Pages: #360 is merged into master. Live HTTP and desktop/mobile visual verification remain blocked/unverified despite earlier successful root deployments. Do not infer current LIVE_VERIFIED from CI.
- #284 licensing: do not infer a code/data license or publish externally before the rights gate is resolved.
- MediaWiki transient-readback: the earlier Klim Samgin exact-source CI failed once with `MediaWiki response missing query` and a fresh rerun succeeded. The response body was not retained, so its precise cause is UNKNOWN. #424 handles only independently documented transient signals, not a claimed reproduction of that historical cause.
- Local checkout: Git DNS failed in this environment. Five production module blobs and the existing single-page test blob were recovered and SHA-verified. Forty-five local tests exercise the real modules with synthetic responses and mocked transport/sleep. The full repository suite and actual provider replay are separate hosted-CI evidence, not the local subset.
- Browser HTTP navigation previously returned ERR_BLOCKED_BY_ADMINISTRATOR. This batch has no UI change and makes no new browser/live verification claim. Do not bypass the restriction.
