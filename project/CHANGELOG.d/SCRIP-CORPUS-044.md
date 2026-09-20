## SCRIP-CORPUS-044 — Twelve Chairs fail-closed render profile

- Selected the queued corpus/provenance continuation after re-orienting from `AGENTS.md`, `PROJECT_MANIFEST.md`, `STATE_AND_QUEUE.md` and current repository state; opened Issue #175 and Draft PR #176 from `master@af2f2e8c857ebb024ccac591ad50e61f0c60f3d6`.
- Added `scriptorium.twelve_chairs_render_profile`, a deterministic source-free profile builder bound to the independently reviewed exact-410 render-surface freeze. It fails closed when any observed tag/template shape is added, removed or changed.
- Frozen profile SHA-256: `88e410311435ab6bcfbd70ab0a2cea73ffe304e3ce2876d241d25ea38cc5d5cd`.
- The profile classifies all 12 observed tag shapes / 3,488 tag tokens and all 30 observed template shapes / 602 invocations. Structural Page-tag decisions are explicit; all 30 template shapes remain unresolved rather than guessed, as do the 410 `<references/>` tokens. The 246 `nop` invocations are explicitly marked inter-page-sensitive.
- Added five standard-library regression tests plus a dedicated PR workflow that deterministically rebuilds the committed profile and verifies the gate boundary.
- Updated the public Twelve Chairs candidate page to distinguish a frozen fail-closed decision boundary from renderer completeness/equivalence.
- No Page wikitext, template argument values, rendered prose, OCR, PDF/image bytes or literary text are committed. `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `rendering_equivalence_claimed=false`, `inter_page_composition_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`.
- Benchmark movement: none; M2 remains 0/5 source-matched works. PR #176 remains Draft for independent exact-head review in a later wake.
