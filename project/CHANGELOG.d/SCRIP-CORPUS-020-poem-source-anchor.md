# SCRIP-CORPUS-020 — historical Poem extension source anchor

- Issue: #109
- Branch: `scrip-corpus-020-poem-source-anchor`
- Status: `AUTHORED_REVIEW_PENDING`
- Scope: freeze one source-free inferred upstream source anchor for the sole live `#tag:poem` boundary; no render-equivalence or Part 2 identity claim.

## Bounded result

Research of upstream `wikimedia/mediawiki-extensions-Poem` history for `includes/Poem.php`, bounded by the pinned Klim Samgin Part 2 parent timestamp `2024-11-26T11:16:35Z`, identified commit `03b3694613e23efa1254d8bbbb98121efaef2cb0` (`2024-10-20T09:15:42Z`) as the latest observed path commit not later than that anchor. The exact file is frozen source-free by Git blob SHA-1 `a362a50d6e139b03a6afd5c24ce7a0923d68ee13`, SHA-256 `86e853c6c41e94356d57824492f32407b916b890ccdfe31c38a081070fb5313c`, and 2,702 UTF-8 bytes.

The pinned source explicitly provides the bounded behavior needed for the next layer: registration of the `poem` parser hook, the `compact` wrapper-newline switch, insertion of `<br />` strip items for interior line breaks, leading-colon indentation spans, leading-space conversion to `&#160;`, recursive tag parsing, sanitized `div` attributes, forced `poem` CSS class, and final `div` wrapping. These are source semantics only; the extension's interaction with MediaWiki core parsing has not yet been reproduced.

The committed manifest `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poem-extension-anchor.json` labels this evidence `inferred_reconstruction_anchor`. It deliberately records `historical_wikisource_deployment_equivalence_proven=false`: upstream history does not by itself prove which extension commit Russian Wikisource actually deployed when the parent page was saved.

## Verification contract

`scriptorium/mediawiki_poem_history.py` fails closed on byte count, SHA-256, Git blob identity, or loss of any bounded source semantic. `tests/test_mediawiki_poem_history.py` covers Git object identity, the bounded semantic inventory, source-free artifact behavior, explicit historical uncertainty, and source drift. `.github/workflows/klim-samgin-poem-history.yml` re-fetches the exact upstream source on the PR head, runs the full standard-library suite, regenerates the source-free manifest, uploads it, and byte-compares it to the committed artifact.

## Boundary / next trigger

Issue #109 remains open. Independent later-run review must judge the exact PR head before merge. If merged, the next bounded layer is to freeze the concrete reached `#tag:poem` argument/attribute surface and then determine which remaining MediaWiki-core recursive-parse behavior is material for the six exact plain parameter-2 values. Resolved Part 2 bytes, four-part literary-body identity, FantLab analyzer-input identity and M2 advancement remain unclaimed.
