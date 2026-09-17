# SCRIP-CORPUS-020 — parameter-2 expansion surface

- Issue: #109
- PR: #117 — Draft; authored for independent later-run review
- Scope: one bounded source-free prerequisite for the Klim Samgin literary-body source graph
- Benchmark movement: none; M2 remains 0/5

## Result

The six already-frozen `poemx1` parameter-2 values from dependency oldid `2366546` are now independently revalidated against their committed binding identities and represented by `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-content.json`. No literary prose is committed.

Across the six exact values the source-free evidence records 324 characters / 589 UTF-8 bytes, 15 value-local lines and 9 newline characters. The observed expansion/render surface contains zero double-brace template/parser constructs, zero triple-brace parameter constructs, zero XML-like tags, zero wikilinks, zero external links and zero apostrophe-markup runs. No value has a leading-colon line, leading-space line or blank line.

Under MediaWiki's documented template-expansion model, this proves only that nested template/parser/tplarg expansion is identity for these exact six inserted values. It does **not** reproduce the Poem extension or historical rendered output. The remaining live template-expansion boundary is therefore narrowed to the already-reachable `#tag:poem` / historical Poem-extension behavior.

## Verification protocol

Discovery workflow `35279662523` on head `76ce460d9a9c7f9ee097266fd23e56d288124205` passed the standard-library suite, exact dependency re-fetch, source-free manifest generation and artifact upload. It failed only at the intentionally absent expected-manifest comparison. The generated source-free artifact was inspected and committed as the expected manifest; fresh exact-head replay is required before independent review.

## Boundary

PR #117 must not be self-merged by the authoring run. Issue #109 stays open. Historical `#tag:poem` / Poem rendering, resolved Part 2 bytes, four-part fail-closed extraction/composition, raw and `scriptorium-text-v1` composite digests, FantLab analyzer-input identity and M2 advancement all remain unresolved.
