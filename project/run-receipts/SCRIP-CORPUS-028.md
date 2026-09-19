# Run receipt — SCRIP-CORPUS-028

Date: 2026-09-19
Issue: #143
Pull request: #144 (`scrip-corpus-028-running-waves-body`)
Mode: recovery-first corpus/provenance implementation

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

The bootstrap live capture that produced the canonical source-free manifest was workflow run `35436513374`; its artifact `10582375841` has digest `sha256:2bc3f6d89035fdae447f45433d78d287cef3c2be000528eeb418ae890b760077`. Final-head replay evidence is recorded separately once the branch containing the committed manifest finishes CI.

## FantLab / gate boundary

FantLab displays 360,987 characters for its 18 September 2022 analysis, which is 2,832 fewer than this frozen public composite. This is diagnostic-only evidence. FantLab does not disclose immutable analyzer-input bytes or a source-edition identity sufficient to equate the two streams.

- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**

The separate Wikisource `/Версия 2` route declaring `az.lib.ru` / Pravda 1980 is not composed into the retained 1965 route.

## Review boundary

This run authored a substantial recovery and literary-body freeze. PR #144 therefore remains Draft and must receive independent exact-head review after its final checks complete. The next run must verify the canonical manifest against a fresh live source-free capture and exact-revision replay before considering Ready/merge.
