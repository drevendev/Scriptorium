# Run receipt — SCRIP-CORPUS-020 PR #119 review and merge

- Date: 2026-09-18
- Issue: #109
- Pull request: #119
- Exact reviewed head: `82da5624c15a026b227f5ea910e9d7af71f0e0f5`
- Base at review: `44aa4ad1e35852debd4b23ac4b14a777b80a46fa`
- Merge result: squash commit `cd38920d78cb767cdaee4756e2d14875c3c06479`
- Unit type: recovery / independent later-run review

## Review evidence

The PR was re-oriented from repository state rather than chat state. Immediately before judgement it was open, Draft, mergeable, 9 commits ahead / 0 behind current master, with eight changed files, no inline review threads and no submitted reviews.

The substantive extractor and tests were inspected at the exact head. The bounded parser records only source identities and dependency inventories and refuses unsupported source shapes instead of widening behavior: it requires exactly one reached `#tag:poem`, requires a content argument, rejects positional and duplicate attributes, verifies the pinned template revision and digest, verifies post-transclusion digest, cross-checks the six control/content invocation identities, and never persists the six literary parameter-2 strings.

The committed source-free manifest records the reached call as one content argument and zero attributes. Whole-call identity is 22 ASCII bytes / SHA-256 `802765da0c42ff7a629167637cb97926023e0a60f11e58a2677849166c958233`; the sole content expression is 8 ASCII bytes / SHA-256 `64e1af6f2e37ee4bcf0ab4f139c75b671321279929eade54fae4cf49be0346f9` and is one empty-default reference to parameter `2`.

All nine workflows associated with the exact head completed successfully: Pages `35297392503`, reached-poem-tag replay `35297391387`, invocation bindings `35297391395`, historical template dependency `35297391534`, poemx1 control flow `35297391385`, Poem source anchor `35297391443`, parameter-2 surface `35297391544`, frozen diagnostic `35297391378`, and pinned pylem provider `35297391531`.

Dedicated run `35297391387` explicitly checked out the exact head, ran the standard-library suite, re-fetched pinned `Шаблон:Poemx1` oldid `5142743`, regenerated the source-free manifest and completed the byte-for-byte committed-artifact comparison step successfully.

## Judgement

No blocking defect was found. The PR's claims remain narrower than its evidence: it freezes only the reached source surface and does not claim MediaWiki recursive-parse equivalence, Poem output/deployment equivalence, resolved Part 2 bytes, literary-body identity or FantLab source identity. The PR was therefore marked Ready and squash-merged.

Issue #109 stays open. The next technical unit is to reproduce only the MediaWiki-core recursive parsing and bounded Poem transformation materially reached by the six exact plain values, then use that evidence to resolve Part 2 before attempting the four-part literary-body composite.

M2 remains 0/5 source-matched works.
