# Run receipt — SCRIP-CORPUS-041

Date: 2026-09-20  
Issue: #169 (closed completed)  
Pull request: #170 (independently reviewed and squash-merged as `aa5a2a1d809b71283acbf02eaaf3a01131e14c25`)  
Base at selection: `363004d58abe7908ee82a8c1ae9a29498e2a54e7`

## Unit

Inspect the four explicit scan-index gaps outside the frozen 410-Page dependency set for the retained 1928 *Zemlya i Fabrika* first-standalone edition of Ilf and Petrov's *The Twelve Chairs*. Freeze only exact Page identities plus source-free structural/body-presence evidence; do not compose the gap pages into a literary body.

## Evidence captured

Hosted capture workflow run `35515025304`, job `106089401762`, checked out authored PR head `b5ed51c576e1bb022579020d7d5db8a29d6da93d`, passed the standard-library suite and source-free boundary assertions, and read exact Page revisions 150, 151, 314 and 315 transiently. Artifact `10606587097` is a 1,576-byte source-free ZIP with GitHub/recomputed SHA-256 `8171ce8c0dcd6d9f20a117e22cc35d0cee4a04d30b4a24c3d8d9befeaf55daa6`; its single 4,670-byte JSON capture has SHA-256 `f1ca4fb4b0ac475be548c0b51efc08b7c1acbbdca3484101de128501862386ad`.

The frozen Page evidence is:

- page 150: revision `5702065`, MediaWiki SHA-1 `ec8cf1e4be633102be57d24e7f92ce5b8f5b2a09`, `nonempty_body_unclassified`;
- page 151: revision `5702062`, MediaWiki SHA-1 `a5e9448c366881761d9792d458c8e33ec4653999`, `no_transcluded_body`;
- page 314: revision `5702066`, MediaWiki SHA-1 `db7f57fc08df092cbed2ce31da776404ba5ed329`, `nonempty_body_unclassified`;
- page 315: revision `5701572`, MediaWiki SHA-1 `667deafe474f3fac76671c04a2ba3d2be40a2bb5`, `no_transcluded_body`.

For the two empty-body pages, the transcluded-body SHA-256 is the standard empty digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Page 150's source-free transcluded-body counts are 22 codepoints / 40 UTF-8 bytes / 18 letters; page 314's are 40 codepoints / 74 UTF-8 bytes / 34 letters. These counts are evidence of nonempty bodies only, not semantic or literary classification.

## Exact-head repair

After the public/structured provenance reconciliation, exact-head CI on `0963b0d8d9c2dc215c90b351180ed7ea891c64e1` ran 348 standard-library tests and exposed exactly two stale assertions in `test_twelve_chairs_provenance_trace`: one still required the pre-audit gap class `unclassified_non_transcluded_gap`, and one still required the pre-audit immutable-status string. The new gap-audit unit itself passed all five dedicated tests. The stale provenance tests were repaired to bind the committed gap-audit manifest and its exact page classes while still asserting the unchanged 410 dependency count and fail-closed downstream gates. This was treated as a correctness repair inside the same bounded unit, not as a reason to weaken or bypass CI.

## Independent exact-head review and merge

A later review wake re-read exact PR head `2798e84a61fd6d312796377fa3ad474785d68e98` against unchanged base `363004d58abe7908ee82a8c1ae9a29498e2a54e7`. The PR was mergeable with 13 commits and 11 changed files, with no inline review threads. All 16 PR-triggered workflows on that exact head were settled `success`.

Dedicated replay run `35515470627`, job `106090556415`, checked out exact head `2798e84a61fd6d312796377fa3ad474785d68e98`; checkout, Python 3.13 setup, standard-library suite, pinned-revision replay, source-free/gate assertions and artifact upload all completed `success`. Replay artifact `10607280063` was independently downloaded and recomputed as a 627-byte ZIP with SHA-256 `b9277875bbe3d0ec537ae8cb5e53e7617af41af37d0b67b97cf3ce68198ec31b`. It contains exactly one 759-byte JSON receipt, SHA-256 `f470fbbe7f406cd215c6b90359794b64812bec28226e817683b9fe03ab389b0f`, with `identity_and_source_free_summary_replay_match=true`, manifest SHA-256 `f1ca4fb4b0ac475be548c0b51efc08b7c1acbbdca3484101de128501862386ad`, unchanged 410 dependency inventory, the four expected body-presence classes, `source_text_included=false`, and all downstream gates still closed.

Review was recorded as COMMENT rather than self-approval because the connected account authored the change. With no blocker remaining, PR #170 was marked Ready and squash-merged with expected-head protection as `aa5a2a1d809b71283acbf02eaaf3a01131e14c25`; Issue #169 closed `completed`.

## Boundary and durable artifacts

The committed `ilf-petrov-twelve-chairs-zif-1928.gap-audit.json` contains no Page wikitext or prose. The 410 frozen dependency identities remain unchanged. The source graph and public candidate page distinguish exact gap inspection from literary-body composition: pages 150/314 are nonempty but unclassified, pages 151/315 have no transcluded body, and all four remain outside the 410 dependency set for this unit.

No Page wikitext, OCR, rendered prose, PDF/image bytes, scan payload, or literary source text is committed.

## Gates

`literary_membership_frozen=false`, `literary_body_frozen=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `m2_parity_admissible=false`. Benchmark movement: none; M2 remains 0/5.

## Handoff

SCRIP-CORPUS-041 is complete. Resume normal-flow selection from the queue. A later bounded unit may define a candidate-specific fail-closed literary-body extraction/composition contract over the 410 pinned dependency pages and explicitly decide whether nonempty gap pages 150/314 belong to the literary body. Pages 151/315 are frozen with no transcluded body. Do not advance >=300k admission, FantLab source-match, diagnostic or M2 parity gates until the resulting literary body and source identity are separately verified.
