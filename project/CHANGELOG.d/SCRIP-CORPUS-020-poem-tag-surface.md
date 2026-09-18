# SCRIP-CORPUS-020 — reached `#tag:poem` source surface

- Issue: #109
- PR: #119 — Draft, authored for later independent review
- Scope: freeze only the concrete top-level `#tag:poem` argument/attribute source surface reached by the six already-frozen `poemx1` frames.
- FantLab gate: unchanged at M2 0/5; source-edition identity remains unknown.

## Result

Exact-source replay of pinned `Шаблон:Poemx1` oldid `5142743` re-applies the committed partial-transclusion profile and finds exactly one live `#tag:poem` call. The call has **one top-level argument and zero attributes**. Its whole source expression is 22 ASCII bytes with SHA-256 `802765da0c42ff7a629167637cb97926023e0a60f11e58a2677849166c958233`.

The sole content expression is one empty-default reference to template parameter `2`, 8 ASCII bytes, SHA-256 `64e1af6f2e37ee4bcf0ab4f139c75b671321279929eade54fae4cf49be0346f9`. Its source surface contains no nested parser functions, ordinary templates, magic words, HTML-like tags, secondary extension calls or attributes. The six previously frozen parameter-2 value identities are bound to this same call without persisting literary prose.

This closes the concrete `#tag:poem` argument/attribute-surface prerequisite. There is no candidate-specific attribute value branch to evaluate. MediaWiki core recursive parsing, Poem output transformation, actual Russian Wikisource Poem deployment identity, resolved Part 2 bytes, four-part literary-body composition and FantLab source equivalence remain unresolved.

## Verification

Dedicated discovery run `35297169381` checked out authored head `a7e3fde2867cc30d09da9b17db2c96bc43300752`, ran **230** standard-library tests successfully, re-fetched exact template oldid `5142743`, verified its frozen source identity, regenerated the source-free tag surface, and emitted the exact artifact later committed on the branch. The workflow was then tightened from discovery mode to require the committed artifact and byte-for-byte replay equality on every relevant PR head.

PR #119 remains Draft by design. A later autonomous run must independently inspect the exact final head and required checks before any merge decision.
