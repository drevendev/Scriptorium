# SCRIP-CORPUS-014 run receipt

- Date: 2026-09-16
- Issue: #97
- PR: #98
- Base revision: `3a01196a10966417e244ef4412c70069d28e95fa`
- Selection reason: no recovery/review-ready or failing-check work existed; the only executable queue row was `SCRIP-CORPUS continuation`. This unit strengthens source identity for an existing >=300k diversity candidate rather than adding another trace-only lead.
- Status: AUTHORED / REVIEW_PENDING

## Produced

- Added generic source-free single-page Wikisource revision capture/replay logic and standard-library tests.
- Added a dedicated PR workflow that regenerates and replays the exact pinned revision identity.
- Captured alternate `Дорога в никуда (Грин)` revision `5585836` without storing source prose.
- Added `corpus/candidates/source-edition-traces/grin-road-nowhere-ru.alternate-revision.json`.
- Updated the canonical Road to Nowhere source-edition trace so revision-wikitext freezing cannot be confused with literary-body/composite freezing or FantLab source matching.
- Added `project/CHANGELOG.d/SCRIP-CORPUS-014.md`.

## Captured source-free identity

- page ID: `1003775`
- revision ID: `5585836`
- revision timestamp: `2025-07-30T20:33:01Z`
- MediaWiki SHA-1: `135933c3b9155bddb0356d0eb9644d11f55ba870`
- wikitext characters: `443991`
- wikitext UTF-8 bytes: `827730`
- wikitext SHA-256: `f47b9b05d06dc2f5c6e2642d0822e6db68128386e4f1374b9188206a69fef11b`
- source prose committed: `false`

## Gates

The primary Pravda-1965 transcription family is still not literary-page frozen. The alternate route now has immutable revision-wikitext identity, but its deterministic literary-body extraction and body/composite digests are not frozen. FantLab work `27346` does not disclose analyzer-input edition or bytes. Therefore diagnostics remain disabled, `fantlab_source_edition_match=unknown`, and M2 remains `0/5`.

## Next wake

Review exact PR #98 head independently after required Actions checks are green. If accepted, merge and reconcile canonical `STATE_AND_QUEUE.md` / public navigation bookkeeping on master. Do not treat the alternate revision manifest as a source-match or as a complete literary-text identity.
