# STATE_AND_QUEUE — Scriptorium

STATE_REVISION: 436
PHASE: M1 — Deterministic FantLab surface
LAST_COMMITTED_RUN_AT: 2026-11-06
LAST_RESULT: #440 confirmed MERGED in master at 9e27ce8a0d1b40a09af047edc5d130bb7e8019af; extending accepted private replay to original EPUB containers for later acceptance.
LAST_VERIFIED_PROGRESS: Reader retains 11 measured editions and 2 research leads. M2 0/5; Trusov historical render/page-join gates remain unresolved.

## Current delivery and acceptance

UNIT_ID: SCRIP-CLI-EPUB-REPLAY-v1
ISSUES: #281 reproducibility-adjacent independent user delivery; no existing EPUB report verification PR
STATUS: PR_CANDIDATE; EXACT_HEAD_CI_PENDING; LATER_ACCEPTANCE_REQUIRED
BRANCH: scrip-cli-epub-verify-v1-20261106
BASE: 9e27ce8a0d1b40a09af047edc5d130bb7e8019af

ACCEPTANCE: `scriptorium verify --epub novel.epub analysis.json` replays the
same bounded in-memory UTF-8 spine projection and all 29 metrics as the existing
`scriptorium epub` command, without intermediate prose or external requests.
Optional `--provenance` additionally verifies exact original archive SHA-256,
extraction profile, chapter counts and source digests; equal prose in a different
ZIP must fail only when archive evidence is supplied. Malformed sidecars,
changed books, symlinks and invalid options fail closed with path-free errors.
Neither mode claims historical edition identity or FantLab parity.
Positive/negative integration tests, exact-head CI and later acceptance are
required before merge.

## Next user-visible milestone and compact queue

Milestone: reproducible private analysis and measured Russian Reader; the
first fully qualified paired translation comparison remains open.

| Priority | Executable unit | Acceptance | Scoped dependency |
| --- | --- | --- | --- |
| P1 | Independently accept EPUB report replay PR | Exact-head EPUB/CLI tests, full Python suite and installed-wheel smoke; later qualifying merge | Fresh CI and review |
| P2 | Verify full Trusov *Robinson Crusoe* first-book literary body | Frozen actual ≥300k prose, rights/identity and 29 measured metrics; honest Shishmareva comparison | Historic rendering/coverage, unresolved VAR and printed edition evidence |
| P3 | #281/#282 AOT/FantLab diagnostic maturity | Measured native N evidence, rigorous source-matched deltas; preserve M2 0/5 | Reference-input identity |
| P4 | #283/#285 public Reader acceptance | Real live HTTP and mobile/desktop keyboard/focus verification | Browser restriction and deployment interlock |
| P5 | Paris ProofreadPage historical renderer | Reproducible source-free markup classification and chapter boundaries | Unsupported source Page markup and transclusion |

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
