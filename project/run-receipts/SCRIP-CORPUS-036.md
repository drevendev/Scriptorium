# SCRIP-CORPUS-036 run receipt

- **Unit:** Darwin/Rachinsky source-free rendering-surface inventory
- **Issue:** #159
- **PR:** #160 (Draft; authored this run, not self-approved or merged)
- **Base:** `f5687b95d20e2714cebfcef8370883377c25f0bb`
- **Repository:** `drevendev/Scriptorium`
- **Connected identity:** `andy-zen-dev`

## Produced

1. Added `scriptorium.darwin_render_surface`, which replays only the 388 already-frozen literary Page revision IDs and verifies title/revision/timestamp/MediaWiki SHA-1 before transient wikitext inspection.
2. Added a source-free construct audit for template name/arity shapes, tag name/kind shapes and aggregate structural counts. Template arguments, lexical snippets, wikitext, rendered prose, OCR and scan bytes are never serialized.
3. Added `scriptorium.darwin_render_surface_freeze`, which reduces the hosted per-Page audit to a deterministic compact durable manifest and validates that all downstream gates remain closed.
4. Added dedicated hosted CI and regression tests for nested templates, triple-brace parameter syntax, noinclude/comments, literal blocks, source-payload leakage and deterministic freeze materialization.
5. Added a public candidate-page surface plus a source-free provenance graph connecting the 418-Page identity freeze, 388/30 composition contract, hosted exact-revision audit and compact inventory.

## Hosted evidence

The first hosted run failed after unit tests because the initial curly-brace scanner treated `}}}` inside nested template closing runs as proof of triple-brace parameter syntax. That was a real implementation defect, not waived evidence; the parser was replaced with a stack-based scanner and regressions were added.

The repaired exact-head hosted audit on `708e780417efa43c80332a782181348aea3e79fb` succeeded:

- workflow run `35487766954`;
- job `106017178554`;
- artifact `10598162631`, 43,615 bytes, digest `sha256:49fdcce34d1e30a10b335024a90c27feb8042d4f48a819e6ff3bb21cc3a8ca1c`;
- full source-free audit SHA-256 `cd6b748090298a5a1a4fe0b1bc63feb7e1ba9c49332bb6217e744b3fd7197b49`;
- 388/388 exact literary Page identities replayed with `identity_replay_match=true`.

Observed source-free surface: 38 template shapes, 18 tag shapes, 1,069 comments, 776 noinclude blocks, 8 wikilinks, and zero external links, headings, table openings/closings or triple-brace parameter constructs. The durable compact freeze hashes the full 388-entry source-free Page receipt list as `7c170f513bf21f2c9e0d7736bc9fc20b4c9a40fdfe942a7b1dd1b0ac048ba09b`; compact manifest digest is `e5ae625fef6afb2e890de990e1ef3b9e108a409a2e0ea2136947c2c3e1cea44d`.

## Verification boundary

This unit freezes **only the observed markup surface**, not MediaWiki rendering semantics. `rendering_profile_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false` remain mandatory.

The PR is left Draft for an independent later exact-head review. Final exact-head CI must be re-read after the bookkeeping/freeze commits before any Ready/merge decision.
