# SCRIP-CORPUS-020 — four-parent body extraction surface

- Issue: #109
- Draft PR: #123
- Base master: `78f168b86c6b7563a5f37f164b29234ddc4fc5f1`
- Scope: one bounded correctness/provenance prerequisite before literary-body extraction; no body digest, FantLab source match or M2 promotion.

The target-only Part 2 resolution merged in PR #122 expands the transcluded dependency and substitutes it into the pinned parent, but that operation does not prove the parent is template-free. This run added a fail-closed source-free replay over all four pinned parent revisions before implementing body extraction.

Live replay established the exact parent structural surface: aggregate templates are `Жизнь Клима Самгина` ×4, direct `poemx1` ×7, `примечания` ×2, `Ко` ×1, plus the single Part 2 target-only `#lst`; aggregate HTML-tag occurrences are `center` ×6, `ref` ×10 and `nowiki` ×50. Part 1 has five level-three headings. Every parent has one category link and no table starts/ends.

The seven direct parent `poemx1` calls are source-freezeable as **5 in Part 1 and 2 in Part 2**. All seven have exactly two anonymous arguments, zero named arguments, explicitly empty parameter `1`, and defined non-empty parameter `2`; only offsets/counts/SHA-256 identities are persisted.

The important correction is Part 2 placement. Its direct parent calls are at offsets `25519..25540` and `25568..26321`; the frozen target-only `#lst` call is at `581758..581810`. Both direct calls are outside the substitution span, so target substitution necessarily preserves them. The merged `ab45577f...` resolved Part 2 identity is therefore a target-substitution reconstruction, not evidence of a template-free parent.

Dedicated generation run `35317530945` on authored head `c6fe334c496bc67c71641ec09732fc1c006047c2` passed the full standard-library suite, re-fetched all four pinned parent revisions, generated the source-free surface and uploaded artifact `10534919689`. The generated canonical artifact was then committed as `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.body-surface.json` and covered by focused regressions plus byte-for-byte replay CI.

The public candidate page now exposes this prerequisite explicitly. `literary_body_extraction_frozen=false`, `literary_composition_frozen=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.

Next trigger after independent review/merge: implement the fail-closed extractor against this frozen surface, including the seven direct parent `poemx1` calls, leading work scaffold, `Ко`, `примечания`/`ref`, `center`, `nowiki`, Part 1 headings and trailing categories; then compose Parts `1 -> 2 -> 3 -> 4` before recording raw or `scriptorium-text-v1` composite identities.
