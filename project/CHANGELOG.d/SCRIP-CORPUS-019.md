# SCRIP-CORPUS-019 — Road to Nowhere alternate literary-body freeze

- Issue: #107
- PR: #108
- Status: `DONE`
- Independently reviewed exact head: `ade0921c385ddb7ff8265c672e88197813123c31`
- Squash merge: `9a73f7cb43f5770e4134c1b3655174b6718756cc`
- Scope: corpus / provenance strengthening plus public representation; no FantLab source-match or M2 promotion.

## Change

The distinct `az.lib.ru`-derived Russian Wikisource route for Alexander Grin's *Road to Nowhere* now has a replay-frozen, source-free literary-body identity bound to the already frozen permanent revision `oldid=5585836`.

A reusable `scriptorium.single_page_body` layer verifies exact revision identity before extraction and persists only body counts/digests. Candidate-specific `scriptorium.road_nowhere_freeze` then applies the versioned `scriptorium-road-nowhere-alt-wikisource-body-v1` fail-closed contract to the observed direct-page source shape: one leading `Отексте` scaffold, exactly 27 level-three literary headings, five trailing category links, and no unsupported post-scaffold templates, HTML tags, external links, tables, comments or bold/italic markers. Source prose is never committed.

The frozen alternate body contains **442,656 characters including spaces / 825,899 UTF-8 bytes**. Raw and `scriptorium-text-v1` normalized SHA-256 are both `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`. Its source revision remains page ID `1003775`, revision `5585836`, timestamp `2025-07-30T20:33:01Z`, MediaWiki SHA-1 `135933c3b9155bddb0356d0eb9644d11f55ba870`, wikitext SHA-256 `f47b9b05d06dc2f5c6e2642d0822e6db68128386e4f1374b9188206a69fef11b`.

Public corpus navigation and the provenance trace expose the stronger alternate-route identity while continuing to distinguish it from the retained primary Pravda-1965 transcription family.

## Independent review and verification

Later-run review of exact head `ade0921c385ddb7ff8265c672e88197813123c31` found no blocking defect. The PR was mergeable, 16 commits ahead / 0 behind its base, contained the expected 11 files, and had no inline review threads.

All exact-head workflows completed successfully:

- Road to Nowhere alternate source revision run `35192693840` — full standard-library suite plus exact source-revision recapture/byte comparison, committed body-manifest recapture/byte comparison, source-specific replay and source-free assertions;
- Scriptorium Pages run `35192693818` — success;
- Scriptorium frozen diagnostic run `35192693735` — success;
- Scriptorium pinned pylem provider run `35192693699` — success.

PR #108 was marked Ready and squash-merged as `9a73f7cb43f5770e4134c1b3655174b6718756cc`; Issue #107 closed completed.

## Boundary

FantLab displays 438,439 characters for its 18 September 2022 analysis, **4,217 fewer** than the frozen alternate body. This delta is diagnostic evidence of non-identity or extraction/counting-policy difference only. The primary Pravda-1965 Wikisource family remains literary-body-unfrozen, and neither public route is identified as FantLab's analyzer input. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains **0/5 source-matched works**.
