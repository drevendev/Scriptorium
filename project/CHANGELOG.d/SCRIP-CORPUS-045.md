# SCRIP-CORPUS-045 — Darwin/Rachinsky fail-closed render profile

- Issue: #177
- PR: #178
- Stream: corpus / provenance; renderer prerequisite for a translated nonfiction candidate
- Base: `master@87929007415ede118cc5700a1e34f2cb3cfc576f`
- Reviewed head: `b8238144caeb23256eae6a61a49e47b07c687f29`
- Squash merge: `5e3833e96fd5e28fe19d24c8e20798fa54eadca4`

## Change

Freeze `scriptorium-darwin-page-render-profile-v1` over the already reviewed exact-388 source-free markup-surface inventory for the 1864 Rachinsky translation of Darwin's *On the Origin of Species*.

The profile validates the frozen surface's canonical self-digest before classification, covers all 18 tag shapes / 5,164 tag tokens and all 38 template shapes / 4,583 invocations, and fails closed on changed counts or new/missing shapes. Conservative local wrapper/noinclude/ProofreadPage metadata handling is defined; `<math>`, `<ref>`, `<references/>`, every template shape, and `nop` inter-page behavior remain explicitly unresolved rather than inferred.

Canonical profile SHA-256: `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`.

Structured provenance and the public candidate page are synchronized with `rendering_profile_frozen=true` while `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `rendering_equivalence_claimed=false`, `inter_page_composition_frozen=false`, body/admission gates false, FantLab source match unknown, diagnostics false and M2 weight zero.

No Page wikitext, template argument values, OCR, rendered prose, DjVu/PDF bytes or literary text are retained.

## Independent review and merge

A later run independently reviewed exact head `b8238144caeb23256eae6a61a49e47b07c687f29` against unchanged base `87929007415ede118cc5700a1e34f2cb3cfc576f`: 11 commits ahead / 0 behind, 11 changed files, and no inline review threads. All 16 PR-triggered workflows had settled `success`.

Dedicated run `35546120433` / job `106172226254` checked out the exact reviewed SHA and passed 7 render-profile tests, 5 provenance tests and a deterministic byte-equivalent profile rebuild. Artifact `10616812708` was independently downloaded: the 1,914-byte ZIP SHA-256 matched `12f3be444a4565f7aee5413aef9183487a072bfe9de47ae6b6d27fec05474fbb`, contained only the 12,592-byte source-free profile JSON, and recomputed embedded canonical profile SHA-256 `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`.

Pages run `35546120447` / job `106172226404` checked out the same exact head and passed the full 376-test standard-library suite, canonical site build and deterministic rebuild. Independent review was recorded as COMMENT review `5262352606`, not self-approval. PR #178 was marked Ready and squash-merged as `5e3833e96fd5e28fe19d24c8e20798fa54eadca4`, closing Issue #177 as completed.

Provider/template/reference/math semantics and inter-page composition remain subsequent evidence units; this change does not implement a renderer or prove >=300k/FantLab parity. M2 remains 0/5.
