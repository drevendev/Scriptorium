# SCRIP-CORPUS-036 run receipt

- **Unit:** Darwin/Rachinsky source-free rendering-surface inventory
- **Issue:** #159 (closed completed)
- **PR:** #160 (independently reviewed; Ready; squash-merged)
- **Production base:** `f5687b95d20e2714cebfcef8370883377c25f0bb`
- **Reviewed exact head:** `ee97e29af7225131002b6e0922c731536d903d13`
- **Merge commit:** `1d9a7795724a68747ea1bb6e1fe1e7ea8b590519`
- **Repository:** `drevendev/Scriptorium`
- **Connected identity:** `andy-zen-dev`

## Produced

1. Added `scriptorium.darwin_render_surface`, which replays only the 388 already-frozen literary Page revision IDs and verifies title/revision/timestamp/MediaWiki SHA-1 before transient wikitext inspection.
2. Added a source-free construct audit for template name/arity shapes, tag name/kind shapes and aggregate structural counts. Template arguments, lexical snippets, wikitext, rendered prose, OCR and scan bytes are never serialized.
3. Added `scriptorium.darwin_render_surface_freeze`, which reduces the hosted per-Page audit to a deterministic compact durable manifest and validates that all downstream gates remain closed.
4. Added dedicated hosted CI and regression tests for nested templates, triple-brace parameter syntax, noinclude/comments, literal blocks, source-payload leakage and deterministic freeze materialization.
5. Added a public candidate-page surface plus a source-free provenance graph connecting the 418-Page identity freeze, 388/30 composition contract, hosted exact-revision audit and compact inventory.

## Production evidence

The first hosted run failed after unit tests because the initial curly-brace scanner treated `}}}` inside nested template closing runs as proof of triple-brace parameter syntax. That was a real implementation defect, not waived evidence; the parser was replaced with a stack-based scanner and regressions were added.

The repaired capture run on `708e780417efa43c80332a782181348aea3e79fb` succeeded:

- workflow run `35487766954`;
- job `106017178554`;
- artifact `10598162631`, 43,615 bytes, digest `sha256:49fdcce34d1e30a10b335024a90c27feb8042d4f48a819e6ff3bb21cc3a8ca1c`;
- full source-free audit SHA-256 `cd6b748090298a5a1a4fe0b1bc63feb7e1ba9c49332bb6217e744b3fd7197b49`;
- 388/388 exact literary Page identities replayed with `identity_replay_match=true`.

Observed source-free surface: 38 template shapes, 18 tag shapes, 1,069 comments, 776 noinclude blocks, 8 wikilinks, and zero external links, headings, table openings/closings or triple-brace parameter constructs. The durable compact freeze hashes the full 388-entry source-free Page receipt list as `7c170f513bf21f2c9e0d7736bc9fc20b4c9a40fdfe942a7b1dd1b0ac048ba09b`; compact manifest digest is `e5ae625fef6afb2e890de990e1ef3b9e108a409a2e0ea2136947c2c3e1cea44d`.

## Independent exact-head review

A later review pass re-oriented from the repository and independently reviewed exact head `ee97e29af7225131002b6e0922c731536d903d13` rather than relying on the production handoff.

- The base remained `f5687b95d20e2714cebfcef8370883377c25f0bb`; the branch was 14 commits ahead / 0 behind and mergeable, with no inline review threads.
- All 15 pull-request-triggered workflows on the exact head were completed `success`.
- Dedicated exact-head workflow `Darwin Rachinsky rendering surface` run `35488061151`, job `106017954957`, checked out `ee97e29af7225131002b6e0922c731536d903d13`, ran the source-free audit tests, replayed the 388 exact revisions, rebuilt and compared the durable freeze, verified the source/gate boundary and uploaded the audit evidence.
- Artifact `10598173002` is 45,088 bytes with GitHub digest `sha256:e11f34e0c84fcdc922efa99e019eeaa6a7e499212d2b0d0f6a8c46fb54f6f750`.
- Independent download of that exact artifact reproduced the same ZIP SHA-256 and contained only the full source-free audit plus compact freeze. Recomputed canonical values matched the committed evidence: audit `cd6b748090298a5a1a4fe0b1bc63feb7e1ba9c49332bb6217e744b3fd7197b49`, per-Page receipt set `7c170f513bf21f2c9e0d7736bc9fc20b4c9a40fdfe942a7b1dd1b0ac048ba09b`, compact freeze `e5ae625fef6afb2e890de990e1ef3b9e108a409a2e0ea2136947c2c3e1cea44d`.
- Receipt sequences were exactly 388 unique literary sequences; revision IDs were unique; full and compact template/tag inventories and aggregate totals agreed; source payload fields were absent.
- Because the connected identity authored the production PR, the review was recorded as a review comment rather than self-approval.

No blocking defect was found. PR #160 was marked Ready and squash-merged as `1d9a7795724a68747ea1bb6e1fe1e7ea8b590519`; Issue #159 closed with reason `completed`.

## Verification boundary

This unit freezes **only the observed markup surface**, not MediaWiki rendering semantics. `rendering_profile_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false` remain mandatory. No benchmark gate moved; M2 remains 0/5 source-matched works.
