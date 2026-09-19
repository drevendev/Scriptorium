# Run receipt — SCRIP-CORPUS-028

Date: 2026-09-19
Issue: #143
Pull request: #144 (`scrip-corpus-028-running-waves-body`)
Mode: recovery-first corpus/provenance implementation + later independent review

## Selected bounded unit

Freeze a deterministic, replayable, source-free literary-body identity for the already revision-frozen 36-page Detskaya literatura 1965 Russian Wikisource route of Alexander Grin's *Running on Waves*, without storing source prose and without promoting FantLab source identity.

## Recovery and evidence

The existing Draft PR's required `Running on Waves literary body` workflow initially failed closed because the generic Wikisource body extractor encountered source-observed templates. Recovery preserved the fail-closed boundary rather than weakening it. Temporary CI diagnostics emitted only source-free template names/arities and synthetic expansion probes. Across the exact pinned 36-page set the observed bounded surface was: `roman`, `^`, `poem1`, `razr`, `razr2`, `акут`, `Гравис`, `опечатка2`, and `Так в тексте`.

Official/source-behavior checks and synthetic MediaWiki expansion evidence established the visible-value decisions used by the candidate-specific renderer: formatting wrappers preserve their visible argument; zero-argument accent/grave templates emit combining marks; `Так в тексте` preserves the first visible argument; `опечатка2` exposes the corrected second argument; the observed `poem1` shape has empty title/footer slots and preserves only its middle literary body. Unknown names or unobserved argument shapes remain unresolved and therefore fail closed.

## Frozen identity

- Source-revision manifest SHA-256: `b50a26b17c72d4e8f3d402d00ff0f50d8df3074cfc1db812e675ec794658e331`
- Literary pages: 36 (`/1` through `/35`, then `/Эпилог`)
- Extraction profile: `scriptorium-running-waves-wikisource-body-v1`
- Composition profile: `scriptorium-wikisource-composite-v1`
- Separator: two newline characters
- Composite characters including spaces: **363,819**
- Composite UTF-8 bytes: **656,239**
- Raw SHA-256: `41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`
- `scriptorium-text-v1` normalized SHA-256: `41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`
- Source text committed: **false**
- >=300k general calibration/profile admission: **true**

The bootstrap live capture that produced the canonical source-free manifest was workflow run `35436513374`; its artifact `10582375841` has digest `sha256:2bc3f6d89035fdae447f45433d78d287cef3c2be000528eeb418ae890b760077`.

## FantLab / gate boundary

FantLab displays 360,987 characters for its 18 September 2022 analysis, which is 2,832 fewer than this frozen public composite. This is diagnostic-only evidence. FantLab does not disclose immutable analyzer-input bytes or a source-edition identity sufficient to equate the two streams.

- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**

The separate Wikisource `/Версия 2` route declaring `az.lib.ru` / Pravda 1980 is not composed into the retained 1965 route.

## Independent exact-head review and merge

A later run independently reviewed final authored head `01e8624da0ac7a23527932bdd3d93d46345ae2ce`. Current `master` was still the PR base, so the branch was **17 commits ahead / 0 behind**, mergeable, and had no inline review threads. All **15 exact-head pull-request workflows** completed successfully.

Candidate-specific run `35436771725`, job `105880664668`, checked out that exact SHA and successfully completed the standard-library suite, a fresh live source-free literary-body capture, byte-for-byte comparison against the committed manifest, exact pinned-revision replay, source-free/M2 guards, and artifact upload. Artifact `10582546118` is `sha256:34d2bde7347d7d29718f577c460a5d0bf60106bcf4893477efe4a712bf503133`.

The independent code/provenance review found no blocking defect: the extractor remains bounded to observed shapes, unsupported residual markup still fails closed, only the retained 36-page 1965-family route is composed, the distinct 1980 `az.lib.ru` route remains excluded, and public wording does not promote bibliography/count proximity into source identity or M2 evidence.

PR #144 was marked Ready and squash-merged as `953b3e0ec7ca657ec3371373fafcf3d472c88dd6`; Issue #143 closed completed. Post-merge durable bookkeeping advanced `STATE_AND_QUEUE` to revision 166. The literary-body freeze is now canonical in `master` while FantLab source match remains unknown and M2 remains 0/5.
