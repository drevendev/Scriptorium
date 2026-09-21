# SCRIP-CORPUS-045 — Darwin/Rachinsky fail-closed render profile

- Issue: #177
- Draft PR: #178
- Stream: corpus / provenance; renderer prerequisite for a translated nonfiction candidate
- Base: `master@87929007415ede118cc5700a1e34f2cb3cfc576f`

## Change

Freeze `scriptorium-darwin-page-render-profile-v1` over the already reviewed exact-388 source-free markup-surface inventory for the 1864 Rachinsky translation of Darwin's *On the Origin of Species*.

The profile validates the frozen surface's canonical self-digest before classification, covers all 18 tag shapes / 5,164 tag tokens and all 38 template shapes / 4,583 invocations, and fails closed on changed counts or new/missing shapes. Conservative local wrapper/noinclude/ProofreadPage metadata handling is defined; `<math>`, `<ref>`, `<references/>`, every template shape, and `nop` inter-page behavior remain explicitly unresolved rather than inferred.

Canonical profile SHA-256: `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`.

Structured provenance and the public candidate page are synchronized with `rendering_profile_frozen=true` while `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `rendering_equivalence_claimed=false`, `inter_page_composition_frozen=false`, body/admission gates false, FantLab source match unknown, diagnostics false and M2 weight zero.

No Page wikitext, template argument values, OCR, rendered prose, DjVu/PDF bytes or literary text are retained.

## Handoff

This authored unit intentionally leaves PR #178 Draft. A later run must independently review the exact final head and settled checks before Ready/merge. Provider/template/reference/math semantics and inter-page composition remain subsequent evidence units; this change does not implement a renderer or prove >=300k/FantLab parity.
