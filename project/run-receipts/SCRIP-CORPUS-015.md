# SCRIP-CORPUS-015 run receipt

- Date: 2026-09-16
- Issue: #99
- PR: #100
- Base revision: `b58598f7e54d8849369077ad07ad0628ad5e38d9`
- Reviewed head: `239c9bf358f376a49598f2808f6a32b7c07bb15a`
- Merged commit: `9e27cedca58a884af283ad56d76056c59725e64b`
- Selection reason: no recovery/review-ready PR or failing required check existed when the unit was authored; the only executable queue row was `SCRIP-CORPUS continuation`. The retained Hyperboloid trace explicitly named exact MediaWiki revision freezing as its next evidence step. A later run recovered the now-review-ready PR first, per the selection ladder.
- Status: DONE / MERGED_AFTER_INDEPENDENT_REVIEW

## Produced

- Reused the merged generic `scriptorium.single_page_revision` implementation; no candidate-specific capture code was added.
- Added `.github/workflows/hyperboloid-source-revision.yml` to regenerate and replay the exact pinned revision on pull requests.
- Added `corpus/candidates/source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.revision.json` containing source-free revision-wikitext identity only.
- Updated the canonical Hyperboloid source-edition trace so revision-wikitext freezing cannot be confused with literary-body identity, bibliographic print-edition identity or FantLab source matching.
- Synchronized `corpus/candidates/README.md` with the new Hyperboloid boundary and repaired its previously stale Road to Nowhere alternate-revision description.
- Added and then finalized `project/CHANGELOG.d/SCRIP-CORPUS-015.md`.

## Captured source-free identity

- page ID: `1022517`
- revision ID: `5014458`
- revision timestamp: `2023-08-30T20:13:01Z`
- MediaWiki SHA-1: `605afeabc38e4f5948371afdf976f586edbf1955`
- wikitext characters: `502280`
- wikitext UTF-8 bytes: `934455`
- wikitext SHA-256: `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`
- source prose committed: `false`

The exact API timestamp is one second later than the display-level timestamp previously retained in the trace; the canonical trace now uses the exact revision timestamp.

## Verification

Bootstrap workflow run `35143256162` completed successfully and produced artifact `hyperboloid-source-revision` from revision `5014458` before the manifest was committed.

The later independent review verified exact head `239c9bf358f376a49598f2808f6a32b7c07bb15a`: current `master` still matched authored base `b58598f7e54d8849369077ad07ad0628ad5e38d9`, the branch was 6 commits ahead / 0 behind, the PR changed exactly six expected provenance/replay files, and there were no inline review threads. Hyperboloid source-revision run `35143599234` completed successfully with the full standard-library suite, fresh pinned capture, byte-for-byte committed-manifest comparison, replay and source-free artifact upload. Pages run `35143599189` completed successfully with the full suite, canonical Pages build, deterministic rebuild and artifact upload. The review found no blocking defect, recorded the judgement on PR #100, and merged with the exact expected head SHA.

## Gates

The MediaWiki revision wikitext is frozen, but no deterministic literary-body extraction or raw/normalized literary-text digest exists. The `az.lib.ru` transcription still has no direct print-edition identity, and the Moscow 1958 / 1939-derived family remains a lead only. FantLab work `44824` does not disclose analyzer-input edition or bytes. Therefore `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, `fantlab_source_edition_match=unknown`, and M2 remains `0/5`.

## Next wake

Select the next dependency-satisfied `SCRIP-CORPUS continuation` unit. Prefer a legally usable >=300k diversity candidate or stronger independent source-identity evidence for an existing candidate. A frozen revision/container is never enough by itself to claim frozen literary-body identity or FantLab source matching.
