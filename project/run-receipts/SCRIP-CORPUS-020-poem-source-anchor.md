# Run receipt — SCRIP-CORPUS-020 Poem extension source anchor

- Issue: #109
- Pull request: #118
- Branch: `scrip-corpus-020-poem-source-anchor`
- Base master at claim: `b4db400fd93ce3950d7503c7c923a5733799b8e3`
- Status: `AUTHORED_REVIEW_PENDING`
- Run date: 2026-09-18

## Selected bounded unit

Freeze one source-free inferred historical source anchor for the sole live `#tag:poem` / Poem-extension boundary left by the merged parameter-2 surface work. This unit intentionally stops before rendering: it identifies and verifies the exact upstream implementation candidate whose source semantics the next layer may reproduce.

## Produced

- `scriptorium/mediawiki_poem_history.py` — fail-closed verifier and source-free anchor builder.
- `tests/test_mediawiki_poem_history.py` — Git-object, semantic-inventory, source-free-boundary and drift coverage.
- `.github/workflows/klim-samgin-poem-history.yml` — exact-source refetch, full standard-library suite, source-free regeneration/upload/byte-compare replay.
- `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poem-extension-anchor.json` — committed source-free inferred anchor.
- dedicated changelog fragment plus synchronized durable state.

## Evidence

The latest observed upstream `wikimedia/mediawiki-extensions-Poem/includes/Poem.php` path commit not later than pinned parent timestamp `2024-11-26T11:16:35Z` is `03b3694613e23efa1254d8bbbb98121efaef2cb0`, timestamped `2024-10-20T09:15:42Z`. Exact source identity is Git blob SHA-1 `a362a50d6e139b03a6afd5c24ce7a0923d68ee13`, SHA-256 `86e853c6c41e94356d57824492f32407b916b890ccdfe31c38a081070fb5313c`, 2,702 UTF-8 bytes.

The pinned implementation source explicitly contains the relevant bounded transformations: `poem` hook registration, `compact` wrapper-newline selection, interior-newline break insertion, leading-colon indentation spans, leading-space NBSP conversion, recursive tag parsing, sanitized div attributes, forced `poem` CSS class and final div wrapping.

This is only an `inferred_reconstruction_anchor`. Repository history does not prove which extension commit Russian Wikisource deployed at the November 2024 page save. `historical_wikisource_deployment_equivalence_proven=false` remains explicit.

## Verification

Local isolated unit reconstruction passed 4/4 new tests before repository mutation. PR #118 hosted exact-head verification is the authoritative full-suite/replay check; the PR remains Draft for independent later-run judgement.

## Remaining boundary

Issue #109 remains open. After an independent exact-head review/merge of #118, freeze the concrete reached `#tag:poem` argument/attribute surface and determine the minimal MediaWiki-core recursive-parse behavior material to the six exact plain parameter-2 values. Resolved Part 2 bytes, four-part literary extraction/composition, FantLab analyzer-input identity and M2 advancement remain unclaimed.
