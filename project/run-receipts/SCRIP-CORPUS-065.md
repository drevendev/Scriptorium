# Run receipt — SCRIP-CORPUS-065

- **Unit:** SCRIP-CORPUS-065 — freeze direct-dependency discovery for Darwin `{{ё}}` replay roots
- **Issue:** #217 (open)
- **Pull request:** #218 (draft; repaired after independent review, new independent judgement pending)
- **Base:** `master@82a7a7baa02b7ae26b25c63b8ed8d51888367308`
- **Branch:** `scrip-corpus-065-darwin-yo-dependencies`
- **Scope:** `drevendev/Scriptorium` only

## Produced

The bounded unit advances only direct-dependency discovery for the two exact canonical replay roots already bound by reviewed v3. Exact Russian Wikisource revision content is fetched transiently, checked against the frozen MediaWiki SHA-1, reduced under transclusion controls, and discarded. Committed artifacts remain source-free.

An initial `action=parse&oldid&prop=templates` experiment was explicitly rejected as canonical evidence because the page-view parse surface included documentation/noinclude templates. The accepted scanner instead works on exact-revision source after identity verification and fails closed on dynamic or unsupported invocation names.

Independent review `5285711348` then found a merge-blocking false negative: the first scanner version treated every uppercase bare invocation as a magic word, so the exact transclusion-visible `{{ЕЁ|ё|е}}` invocation was silently dropped and `Шаблон:Ё` was incorrectly frozen with no direct dependency. This repair wake removed that heuristic, pinned the official MediaWiki `Help:Magic words@8589537` evidence surface, explicitly bound exact uppercase `ЕЁ` as a template from the root evidence, and made unknown uppercase or parameterized magic-word-like invocations fail closed.

The first repaired exact-head replay correctly reached the stricter fail-closed boundary and exposed one further documented variable used by the historical roots: bare `{{NAMESPACE}}`. Official MediaWiki magic-word documentation explicitly identifies `NAMESPACE` as a variable, so it was added to the same pinned allowlist and a regression now covers `{{PAGENAME}}{{NAMESPACE}}` as non-template syntax. Unknown uppercase names remain fail-closed.

Corrected frozen source-free observations:

- `Шаблон:Ё@5687302`: 271 UTF-8 bytes, source SHA-1 `963c1796d693d5451cf0c0897c35bd7e5b327ae1`, transclusion SHA-256 `bd7465151d984f06c75eae0c1246c26a0643826a26a170a3e9a9d43c9e5a03b7`, direct dependency `Шаблон:ЕЁ`;
- `Шаблон:ЕЁ@3684646`: 688 UTF-8 bytes, source SHA-1 `435bb2a412d8fb5962ccd5adc0ac2e03412fe109`, transclusion SHA-256 `3975fa227e23e8cc1487a49a3eab86b28e0ddb6a753c347c3191ee800ae56026`, direct dependency `Модуль:String`.

The corrected `scriptorium-darwin-template-yo-replay-contract-v4` is derived from reviewed v3 SHA-256 `8caa144d9f4c0b9a8149c1822bd79d168d212dea14d72079c3259d55e5e03c8c` and has contract SHA-256 `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64`. Its bound replay graph now contains `Шаблон:Ё -> Шаблон:ЕЁ`; the separately recorded `Шаблон:ЕЁ -> Модуль:String` target remains identity-unbound.

## Verification / handoff

The repair adds regressions proving `{{ЕЁ|ё|е}} -> Шаблон:ЕЁ`, confirming pinned documented bare `PAGENAME` and `NAMESPACE` variables are not treated as templates, and rejecting unknown uppercase / parameterized magic-word-like invocations. V4 tests require the explicit bound root edge and pinned magic-word evidence. The dedicated read-only workflow deterministically rebuilds/byte-compares canonical v4 and freshly re-fetches both exact historical roots before comparing their source-free observations.

During repair, exact-head run `35808760352` passed all 23 scanner/v3/v4 regressions and deterministic v4 rebuild, then failed closed on previously unclassified bare `NAMESPACE`; this was evidence-bearing and led to the pinned `NAMESPACE` classification rather than reopening the broad uppercase heuristic. The next exact-head run is required to prove the final refreshed contract and historical-root observations together.

This repair wake deliberately does **not** self-approve or merge the substantive changes. Re-read the exact final PR head after all PR-triggered checks settle; confirm the review blocker is actually removed, the deterministic rebuild matches the committed SHA-256 above, the exact-root replay reproduces `Шаблон:Ё -> Шаблон:ЕЁ -> Модуль:String`, and only then perform a separate judgement/merge wake if clean.

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

Next evidence-bearing Darwin step after independent repaired-head review is to bind a deliberate exact replay identity for `Модуль:String`, freeze that module's direct dependencies, and continue recursively before any output/renderer/body promotion.
