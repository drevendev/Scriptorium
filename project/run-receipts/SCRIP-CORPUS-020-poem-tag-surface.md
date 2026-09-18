# Run receipt — SCRIP-CORPUS-020 reached `#tag:poem` surface

- Date: 2026-09-18
- Issue: #109
- Pull request: #119
- Base master at selection: `44aa4ad1e35852debd4b23ac4b14a777b80a46fa`
- Authored branch: `scrip-corpus-020-poem-tag-surface`
- Unit class: corpus / provenance / historical expansion prerequisite

## Orientation and selection

`AGENTS.md`, `project/PROJECT_MANIFEST.md`, `project/STATE_AND_QUEUE.md`, `project/CHANGELOG.md`, Issue #109 and the current open-PR set were re-read before selection. There were no open recovery/review-ready PRs. The state P0 therefore selected the next SCRIP-CORPUS-020 continuation: freeze the concrete reached `#tag:poem` argument/attribute surface before implementing any broader MediaWiki parsing behavior.

## Produced

Added a bounded source-free parser at `scriptorium/mediawiki_poem_tag_surface.py`, unit tests, a dedicated exact-source replay workflow, machine-readable evidence at `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poem-tag-surface.json`, and a public candidate-page explanation.

The exact historical template source surface is materially simpler than the queue could establish beforehand:

- one reached `#tag:poem` call;
- one top-level argument total;
- that argument is the content argument;
- zero tag attributes;
- content expression: one empty-default reference to parameter `2`;
- whole call identity: 22 ASCII bytes, SHA-256 `802765da0c42ff7a629167637cb97926023e0a60f11e58a2677849166c958233`;
- content-expression identity: 8 ASCII bytes, SHA-256 `64e1af6f2e37ee4bcf0ab4f139c75b671321279929eade54fae4cf49be0346f9`.

All six already-frozen parameter-2 content identities are bound to this call. No literary prose is committed.

## Verification

Discovery workflow run `35297169381` on head `a7e3fde2867cc30d09da9b17db2c96bc43300752` completed successfully. It ran 230 standard-library tests, re-fetched pinned `Шаблон:Poemx1` oldid `5142743`, required the previously frozen source SHA-256 `fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`, reapplied partial-transclusion preprocessing, and generated the source-free result used for the committed artifact. The branch then changed the workflow to fail closed unless a fresh replay is byte-identical to the committed artifact.

## Boundary and next trigger

This slice does not evaluate MediaWiki core recursive parsing, reproduce Poem output, prove the Poem version actually deployed on Russian Wikisource, freeze resolved Part 2 bytes, compose the four-part literary body, or advance FantLab parity. M2 remains 0/5.

PR #119 remains Draft for independent later-run review. If its final exact head is green, the next technical continuation after merge is to reproduce only the MediaWiki-core recursive-parse behavior material to the six plain parameter-2 values and the bounded Poem transform, without inventing generic parser support that the frozen source does not reach.
