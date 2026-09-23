# Run receipt — SCRIP-CORPUS-065

- **Unit:** SCRIP-CORPUS-065 — freeze direct-dependency discovery for Darwin `{{ё}}` replay roots
- **Issue:** #217 (closed completed)
- **Pull request:** #218 (independently reviewed; squash-merged as `d2d1da61c92f058213c008b4e8c0bdd0a7f7f40c`)
- **Base:** `master@82a7a7baa02b7ae26b25c63b8ed8d51888367308`
- **Final reviewed head:** `0de7f525d06e0e209ae6cf6591c1e2c1561ca56b`
- **Branch:** `scrip-corpus-065-darwin-yo-dependencies`
- **Scope:** `drevendev/Scriptorium` only

## Produced

The bounded unit advances only direct-dependency discovery for the two exact canonical replay roots already bound by reviewed v3. Exact Russian Wikisource revision content is fetched transiently, checked against the frozen MediaWiki SHA-1, reduced under transclusion controls, and discarded. Committed artifacts remain source-free.

An initial `action=parse&oldid&prop=templates` experiment was explicitly rejected as canonical evidence because the page-view parse surface included documentation/noinclude templates. The accepted scanner instead works on exact-revision source after identity verification and fails closed on dynamic or unsupported invocation names.

Independent review `5285711348` then found a merge-blocking false negative: the first scanner version treated every uppercase bare invocation as a magic word, so the exact transclusion-visible `{{ЕЁ|ё|е}}` invocation was silently dropped and `Шаблон:Ё` was incorrectly frozen with no direct dependency. The repair removed that heuristic, pinned the official MediaWiki `Help:Magic words@8589537` evidence surface, explicitly bound exact uppercase `ЕЁ` as a template from the root evidence, and made unknown uppercase or parameterized magic-word-like invocations fail closed.

The first repaired exact-head replay correctly reached the stricter fail-closed boundary and exposed one further documented variable used by the historical roots: bare `{{NAMESPACE}}`. Official MediaWiki magic-word documentation explicitly identifies `NAMESPACE` as a variable, so it was added to the same pinned allowlist and a regression covers `{{PAGENAME}}{{NAMESPACE}}` as non-template syntax. Unknown uppercase names remain fail-closed.

Corrected frozen source-free observations:

- `Шаблон:Ё@5687302`: 271 UTF-8 bytes, source SHA-1 `963c1796d693d5451cf0c0897c35bd7e5b327ae1`, transclusion SHA-256 `bd7465151d984f06c75eae0c1246c26a0643826a26a170a3e9a9d43c9e5a03b7`, direct dependency `Шаблон:ЕЁ`;
- `Шаблон:ЕЁ@3684646`: 688 UTF-8 bytes, source SHA-1 `435bb2a412d8fb5962ccd5adc0ac2e03412fe109`, transclusion SHA-256 `3975fa227e23e8cc1487a49a3eab86b28e0ddb6a753c347c3191ee800ae56026`, direct dependency `Модуль:String`.

The corrected `scriptorium-darwin-template-yo-replay-contract-v4` is derived from reviewed v3 SHA-256 `8caa144d9f4c0b9a8149c1822bd79d168d212dea14d72079c3259d55e5e03c8c` and has contract SHA-256 `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64`. Its bound replay graph contains `Шаблон:Ё -> Шаблон:ЕЁ`; the separately recorded `Шаблон:ЕЁ -> Модуль:String` target remains identity-unbound.

## Verification / independent judgement

The repair adds regressions proving `{{ЕЁ|ё|е}} -> Шаблон:ЕЁ`, confirming pinned documented bare `PAGENAME` and `NAMESPACE` variables are not treated as templates, and rejecting unknown uppercase / parameterized magic-word-like invocations. V4 tests require the explicit bound root edge and pinned magic-word evidence. The dedicated read-only workflow deterministically rebuilds/byte-compares canonical v4 and freshly re-fetches both exact historical roots before comparing their source-free observations.

During repair, exact-head run `35808760352` passed all 23 scanner/v3/v4 regressions and deterministic v4 rebuild, then failed closed on previously unclassified bare `NAMESPACE`; this was evidence-bearing and led to the pinned `NAMESPACE` classification rather than reopening the broad uppercase heuristic. On repaired head `c62a000dec51fc10fe76660e91c9223c72b921f5`, all 22 PR-triggered workflows settled `success`, including dedicated direct-dependency run `35809264224`.

A subsequent independent read of `c62a000dec51fc10fe76660e91c9223c72b921f5` found no new scanner/contract semantic blocker but did find a public-representation contradiction: the v3 root-identity companion still said `Шаблон:Ё` had no direct template/module dependency. Commit `0de7f525d06e0e209ae6cf6591c1e2c1561ca56b` corrected that public companion plus the durable changelog/receipt without changing analyzer or v4 contract semantics.

Final independent exact-head review `5286379571` re-read `0de7f525d06e0e209ae6cf6591c1e2c1561ca56b` against unchanged `master@82a7a7baa02b7ae26b25c63b8ed8d51888367308`, reviewed all 11 changed files, confirmed the corrected graph/public companion and unchanged v4 digest, and found no remaining merge blocker or open review thread. All 22 PR-triggered workflows on that exact head settled `success`. Dedicated run `35809729651` checked out the exact reviewed SHA, passed the scanner/v3/v4 regression set, deterministically rebuilt/byte-compared v4, and freshly re-queried both historical roots. General pinned-pylem run `35809729692` also settled `success`, including the complete standard-library suite, native pinned provider smoke and frozen Anna sidecar replay.

PR #218 was then marked Ready and squash-merged with expected-head protection as `d2d1da61c92f058213c008b4e8c0bdd0a7f7f40c`, closing Issue #217 completed.

## Gates / handoff

- `root_identities_bound=true`
- `root_direct_dependency_discovery_complete=true` only for the two exact roots
- bound edge: `Шаблон:Ё -> Шаблон:ЕЁ`
- discovered unbound child: `Шаблон:ЕЁ -> Модуль:String`
- `dependency_closure_complete=false`
- deterministic forced/non-forced outputs remain unverified
- renderer rule promotion remains false; `ё` remains unresolved in the semantic backlog
- literary-body / >=300k admission remains false
- `fantlab_source_edition_match=unknown`
- `m2_parity_admissible=false`
- M2 remains **0/5**

Next evidence-bearing Darwin step is to bind a deliberate exact replay identity for `Модуль:String`, freeze that module's direct dependencies, and continue recursively before any output/renderer/body promotion. Normal-flow selection resumes from the canonical queue; this sentence is not a priority override.
