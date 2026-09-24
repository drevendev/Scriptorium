# Darwin/Rachinsky 1864 — rendering semantics backlog

This public source-free companion to `darwin-origin-species-rachinsky-1864-ru` exposes the reviewed rendering-semantic boundary without storing literary source text, Page wikitext, template argument values, rendered prose, OCR or scan bytes.

The original frozen render profile and semantic backlog remain immutable predecessor evidence. SCRIP-CORPUS-077 independently reviewed the zero-argument `{{ё}}` replay evidence; SCRIP-CORPUS-078 promoted that one template shape; SCRIP-CORPUS-079 independently proved candidate-local containment for self-closing `<references/>`; and SCRIP-CORPUS-080 records the separate promotion judgement as another compact successor layer rather than rewriting that history.

## Reviewed `{{ё}}` promotion

The reviewed v6 replay contract binds the selected live-snapshot dependency graph `Шаблон:Ё@5687302 → Шаблон:ЕЁ@3684646 → Модуль:String@3684569` inside an identity-stable provider window. For the observed zero-argument `{{ё}}` shape it verifies:

| Mode | Defined output | SHA-256 |
| --- | --- | --- |
| forced yoification | `ё` | `30fbc377ae9122edc2cdbed70b9261817d196eca8db96ac8bfa4cfaf412667ac` |
| non-forced yoification | `е` | `259f56cb715ba3a3f1ca41a4ff1972cca698cb49eef1ae018dff325507da8b26` |

The promotion contract applies that evidence to exactly one frozen render-profile shape: template `ё`, **0 positional / 0 named arguments**, observed **2,227 times**. Its source-free promotion SHA-256 is `153f6ceb89025da90971ddc265df680359ff498103bb47ecd68f86bb3205ed28`.

This is deliberately **not** historical transclusion provenance and is not a claim that Scriptorium has an offline/version-pinned MediaWiki runtime.

## Reviewed candidate-local `<references/>` promotion

SCRIP-CORPUS-079 replayed all **388 exact frozen literary Page revisions** and found **388 / 388** observed self-closing `<references/>` tokens inside the same `<noinclude>...</noinclude>` regions removed by the already-defined `strip_nontranscluded_region` stage, with **0 outside**. The independently reviewed containment probe SHA-256 is `3dde2e1ea259ccc4f855ad20dc8df588f9546a9ec181f84155175a86c3b139e3`.

SCRIP-CORPUS-080 consumes only that reviewed fact. The candidate-local successor rule changes the observed shape from `provider_reference_semantics_required` / unresolved to `drop_via_existing_strip_nontranscluded_region` / `defined_candidate_local`. It does **not** implement or replay MediaWiki Cite semantics, and it makes no claim about `<references/>` outside stripped regions, historical Wikisource transclusion, or a general MediaWiki renderer.

The source-free references promotion SHA-256 is `4052973abc6c413503f26c27419770a2214bf3253ecb31ec9d4cf3c1276dec39`.

## Effective unresolved surface

After removing only the reviewed zero-argument `{{ё}}` shape and the candidate-local self-closing `<references/>` shape, **41 unresolved shapes** remain:

| Research track | Shapes | Observed occurrences |
| --- | ---: | ---: |
| provider-template semantics | 36 | 2,352 |
| provider-reference semantics | 2 | 78 |
| provider-math semantics | 2 | 52 |
| inter-page semantics | 1 | 4 |

The effective unresolved totals are therefore **4 tag shapes / 130 tag tokens** and **37 template shapes / 2,356 invocations**. No other semantic behavior is inferred by these reductions.

The deterministic next research slice is template `ВАР`, **2 positional / 0 named arguments**, observed **388** times. This is the highest remaining unresolved occurrence count and preserves the original predecessor ordering.

## Source-free artifacts

- immutable render profile v1: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile.json), SHA-256 `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`
- immutable semantic backlog v1: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json), SHA-256 `4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2`
- independently reviewed replay v6: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v6.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v6.json), SHA-256 `c317eb5247701f0ad860811e9349f4e6f42274e72e8856eecb8a9aff610f988f`
- `{{ё}}` render-profile promotion: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile-yo-promotion-v1.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile-yo-promotion-v1.json), SHA-256 `153f6ceb89025da90971ddc265df680359ff498103bb47ecd68f86bb3205ed28`
- effective semantic backlog v2: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v2.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v2.json), SHA-256 `6d4ba2bb9ec78731d97d91c87d0628207ec880901e9d388fa7aa7c70fb20e3be`
- independently reviewed `<references/>` containment probe: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.references-containment-v1.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.references-containment-v1.json), SHA-256 `3dde2e1ea259ccc4f855ad20dc8df588f9546a9ec181f84155175a86c3b139e3`
- candidate-local `<references/>` promotion: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile-references-promotion-v1.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile-references-promotion-v1.json), SHA-256 `4052973abc6c413503f26c27419770a2214bf3253ecb31ec9d4cf3c1276dec39`
- effective semantic backlog v3: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v3.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v3.json), SHA-256 `4b68de749eec8bbacf0e07cb9f87e2c5c2db0c81d438a191fadd15f4dffbda18`
- deterministic builders/validators: [`../../scriptorium/darwin_yo_render_profile_promotion.py`](../../scriptorium/darwin_yo_render_profile_promotion.py), [`../../scriptorium/darwin_references_containment.py`](../../scriptorium/darwin_references_containment.py), [`../../scriptorium/darwin_references_profile_promotion.py`](../../scriptorium/darwin_references_profile_promotion.py)

## Gates unchanged

These promotions resolve two high-volume candidate-local shapes, but they do not implement a complete renderer. `renderer_semantics_complete`, `renderer_implementation_ready`, `inter_page_composition_frozen`, `literary_body_count_and_digests_frozen`, `minimum_300k_proved`, `admitted_for_calibration`, `diagnostic_ready` and `m2_parity_admissible` remain false; `fantlab_source_edition_match=unknown`. Provider Cite semantics remain unreplayed. M2 remains **0/5**.
