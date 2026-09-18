# Run receipt — SCRIP-CORPUS-020 Part 2 resolution

Date: 2026-09-18
Issue: #109
Pull request: #122 (Draft; independent later-run review required)
Base revision: `957266307475fc4859167bf395739202a5d3df75`

## Bounded unit

Resolve the already-pinned target-only Part 2 source graph end-to-end through the six frozen `poemx1` invocations, while persisting only source-free identities and keeping historical deployment equivalence, literary extraction/composition, FantLab source identity and M2 admission explicitly unresolved.

## Authoring evidence

Initial dedicated replay run `35312964855` checked out exact authored head `570a160a6c4134474602ae177b020f086665be0a`, ran the complete standard-library suite (**239 tests, all passing**), re-fetched exact Part 2 parent oldid `5198033`, target oldid `2366546`, and inferred template anchor oldid `5142743`, then rebuilt the candidate-specific resolution artifact without storing literary prose.

The replay reproduced six full `poemx1` expansions. Each invocation reached exactly `#if` ×4, `#ifeq` ×3, `#tag` ×1, `#expr` ×0 and `#iferror` ×0, and each Poem fragment digest agreed with the already-frozen render-surface evidence.

Generated source-free identities:

- expanded target dependency: 585,113 characters / 1,059,957 UTF-8 bytes; SHA-256 `a027dfe0d867572f3802050fcfd72b07a43fa6efe539d58035b3af59f49a04d4`;
- resolved parent Part 2 wikitext after exact target-only substitution: 1,166,949 characters / 2,114,262 UTF-8 bytes; SHA-256 `ab45577f567ce504e24936f73fcdff261780168414e4bccc04bbf8927299d016`;
- remaining target expansion surface: zero `poemx1` invocations and zero `{{` / `}}` delimiters.

The generated artifact was committed as `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.part2-resolution.json`.

## Exact-head verification

After the complete semantic authoring slice was committed, exact head `cadbd2f812468c468f41a322965672b328cfbf65` completed **all 11 triggered workflows successfully**. Dedicated Part 2 run `35313433442` checked out that exact SHA, ran the complete **239-test** standard-library suite, re-fetched the three pinned source revisions, regenerated the source-free resolution artifact, and byte-compared it against the committed JSON with `cmp` successfully. The pinned-pylem provider workflow also completed all three jobs successfully, including the isolated provider smoke and frozen Anna replay.

This verification is evidence for the authored slice only; PR #122 remains Draft and still requires independent later-run code/claim review before Ready/merge.

## Claims boundary

This is `candidate_specific_inferred_reconstruction`. The inferred Poem source anchor does not prove which MediaWiki-core or Poem revision Russian Wikisource actually deployed for the historical render. The unit therefore does not claim historical render equivalence, a literary-body identity, four-part composition, FantLab input identity, or parity progress. M2 remains **0/5**.

## Next action

Keep PR #122 Draft. On a later wake, independently review its exact final head and checks; if clean, mark Ready and merge. Only after that merge should SCRIP-CORPUS-020 define fail-closed per-part literary extraction and deterministic `1 -> 2 -> 3 -> 4` composition before recording raw or `scriptorium-text-v1` composite body digests.
