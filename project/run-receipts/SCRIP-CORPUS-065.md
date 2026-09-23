# Run receipt — SCRIP-CORPUS-065

- **Unit:** SCRIP-CORPUS-065 — freeze direct-dependency discovery for Darwin `{{ё}}` replay roots
- **Issue:** #217 (open)
- **Pull request:** #218 (draft; independent judgement pending)
- **Base:** `master@82a7a7baa02b7ae26b25c63b8ed8d51888367308`
- **Branch:** `scrip-corpus-065-darwin-yo-dependencies`
- **Scope:** `drevendev/Scriptorium` only

## Produced

The bounded unit advances only direct-dependency discovery for the two exact canonical replay roots already bound by reviewed v3. Exact Russian Wikisource revision content is fetched transiently, checked against the frozen MediaWiki SHA-1, reduced under transclusion controls, and discarded. Committed artifacts remain source-free.

An initial `action=parse&oldid&prop=templates` experiment was explicitly rejected as canonical evidence because the page-view parse surface included documentation/noinclude templates. The accepted scanner instead works on exact-revision source after identity verification and fails closed on dynamic or unsupported invocation names.

Frozen source-free observations:

- `Шаблон:Ё@5687302`: 271 UTF-8 bytes, source SHA-1 `963c1796d693d5451cf0c0897c35bd7e5b327ae1`, transclusion SHA-256 `bd7465151d984f06c75eae0c1246c26a0643826a26a170a3e9a9d43c9e5a03b7`, no direct template/module dependency;
- `Шаблон:ЕЁ@3684646`: 688 UTF-8 bytes, source SHA-1 `435bb2a412d8fb5962ccd5adc0ac2e03412fe109`, transclusion SHA-256 `3975fa227e23e8cc1487a49a3eab86b28e0ddb6a753c347c3191ee800ae56026`, direct dependency `Модуль:String`.

The new `scriptorium-darwin-template-yo-replay-contract-v4` is derived from reviewed v3 SHA-256 `8caa144d9f4c0b9a8149c1822bd79d168d212dea14d72079c3259d55e5e03c8c` and has contract SHA-256 `2e314e81fb3dbbedf05b3b83399d33e233abf0cd858ff70f5728de5c2e613c57`. It records complete root-level discovery proof but intentionally leaves the newly discovered `Модуль:String` target unbound.

## Verification / handoff

Bootstrap run `35800089647` checked out authoring head `d782474459270cee58935524f6d391379aed3715`, passed 12 scanner+v3 regressions after the fail-closed dynamic-name repair, deterministically built v4, and freshly reproduced both exact-root source-free observations. The dedicated final workflow now also runs the v4 regressions, byte-compares the committed v4 JSON, re-fetches the exact roots, and compares the transient scan results with the canonical source-free artifact.

Independent review and merge are deliberately deferred to the next wake. Before judgement, re-read the exact final PR head, confirm the base has not moved unexpectedly, inspect all changed files/review threads, and require all PR-triggered checks to settle successfully.

## Gates / handoff

- `root_identities_bound=true`
- `root_direct_dependency_discovery_complete=true`
- discovered child: `Шаблон:ЕЁ -> Модуль:String`, with `target_identity_bound=false`
- `dependency_closure_complete=false`
- deterministic forced/non-forced outputs remain unverified
- renderer rule promotion remains false; `ё` remains unresolved in the semantic backlog
- literary-body / >=300k admission remains false
- `fantlab_source_edition_match=unknown`
- `m2_parity_admissible=false`
- M2 remains **0/5**

Next evidence-bearing Darwin step after independent review is to bind a deliberate exact replay identity for `Модуль:String`, freeze that module's direct dependencies, and continue recursively before any output/renderer/body promotion.
