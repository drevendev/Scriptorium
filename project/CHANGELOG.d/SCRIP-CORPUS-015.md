# SCRIP-CORPUS-015 — Hyperboloid exact revision-wikitext identity

Date: 2026-09-16
Issue: #99
PR: #100
Base: `b58598f7e54d8849369077ad07ad0628ad5e38d9`
Status: merged after independent exact-head review
Merged commit: `9e27cedca58a884af283ad56d76056c59725e64b`

## Unit

Strengthened the existing `tolstoy-hyperboloid-garin-wikisource-ru` candidate instead of adding another trace-only work. The Russian Wikisource route is a stable reviewed public-domain single-page transcription at permanent revision `oldid=5014458`, with `az.lib.ru` cited as its source and the exact print-edition identity still unresolved.

A source-free capture now records exact revision-wikitext identity without committing literary prose: page ID `1022517`, revision timestamp `2023-08-30T20:13:01Z`, MediaWiki SHA-1 `605afeabc38e4f5948371afdf976f586edbf1955`, 502,280 wikitext characters / 934,455 UTF-8 bytes, and SHA-256 `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`.

This corrects the earlier trace's display-level timestamp (`20:13:00Z`) to the exact MediaWiki API revision timestamp (`20:13:01Z`). The capture boundary remains narrower than a frozen literary-text candidate: no deterministic literary-body extraction contract or raw/normalized literary digest exists, the Moscow 1958 / 1939-derived textual-family evidence remains a non-identifying bibliographic lead, and FantLab does not disclose its analyzer input.

## Verification design

The unit reuses `scriptorium.single_page_revision`; no parallel capture implementation was added. The dedicated pull-request workflow regenerates revision `5014458` through the MediaWiki API, runs the complete standard-library suite, compares the generated source-free manifest byte-for-byte with the committed identity, replays the pinned revision, and uploads only source-free evidence.

Bootstrap Actions run `35143256162` completed successfully before the manifest was committed and produced the source-free capture artifact used for the exact identity above.

## Independent review and merge

A later run independently reviewed exact PR head `239c9bf358f376a49598f2808f6a32b7c07bb15a`. Immediately before merge, `master` was still the authored base, the branch was 6 commits ahead / 0 behind, the PR changed exactly six expected provenance/replay files, and no inline review threads existed.

Exact-head workflow run `35143599234` completed successfully: the full standard-library suite passed, a fresh pinned revision capture matched the committed manifest byte-for-byte, replay passed, and only source-free evidence was uploaded. Pages run `35143599189` also completed successfully with the full test suite, canonical static build, deterministic rebuild and artifact upload. No blocking review defect was found.

PR #100 was squash-merged as `9e27cedca58a884af283ad56d76056c59725e64b`; Issue #99 closed completed.

The public corpus README is synchronized with the stronger Hyperboloid identity boundary and also repairs the previously stale Road to Nowhere navigation: its alternate route has frozen revision-wikitext identity while its literary body and primary 1965 family remain unfrozen.

Benchmark movement: none. `fantlab_source_edition_match=unknown`, diagnostics remain disabled, and M2 remains **0/5 source-matched works**.
