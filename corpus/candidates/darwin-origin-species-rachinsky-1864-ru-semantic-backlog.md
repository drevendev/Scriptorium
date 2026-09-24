# Darwin/Rachinsky 1864 — rendering semantics backlog

This public source-free companion to `darwin-origin-species-rachinsky-1864-ru` exposes the reviewed rendering-semantic boundary without storing literary source text, Page wikitext, template argument values, rendered prose, OCR or scan bytes.

The original frozen render profile and semantic backlog remain immutable predecessor evidence. SCRIP-CORPUS-077 independently reviewed the zero-argument `{{ё}}` replay evidence, and SCRIP-CORPUS-078 records the separate promotion judgement as a compact successor layer rather than rewriting that history.

## Reviewed `{{ё}}` promotion

The reviewed v6 replay contract binds the selected live-snapshot dependency graph `Шаблон:Ё@5687302 → Шаблон:ЕЁ@3684646 → Модуль:String@3684569` inside an identity-stable provider window. For the observed zero-argument `{{ё}}` shape it verifies:

| Mode | Defined output | SHA-256 |
| --- | --- | --- |
| forced yoification | `ё` | `30fbc377ae9122edc2cdbed70b9261817d196eca8db96ac8bfa4cfaf412667ac` |
| non-forced yoification | `е` | `259f56cb715ba3a3f1ca41a4ff1972cca698cb49eef1ae018dff325507da8b26` |

The promotion contract applies that evidence to exactly one frozen render-profile shape: template `ё`, **0 positional / 0 named arguments**, observed **2,227 times**. Its source-free promotion SHA-256 is `153f6ceb89025da90971ddc265df680359ff498103bb47ecd68f86bb3205ed28`.

This is deliberately **not** historical transclusion provenance and is not a claim that Scriptorium has an offline/version-pinned MediaWiki runtime. The replay contract still records `historical_transclusion_provenance_proved=false` and `offline_version_pinned_mediawiki_environment_claimed=false`.

## Effective unresolved surface

Removing only the reviewed zero-argument `{{ё}}` shape leaves **42 unresolved shapes**:

| Research track | Shapes | Observed occurrences |
| --- | ---: | ---: |
| provider-template semantics | 36 | 2,352 |
| provider-reference semantics | 3 | 466 |
| provider-math semantics | 2 | 52 |
| inter-page semantics | 1 | 4 |

The effective unresolved totals are therefore **5 tag shapes / 518 tag tokens** and **37 template shapes / 2,356 invocations**. No other semantic behavior is inferred by this reduction.

The deterministic next research slice is now self-closing `<references/>`, observed **388** times. Template `ВАР` is also observed 388 times, but the predecessor backlog's stable ordering puts `<references/>` first; the successor keeps that ordering rather than introducing a new judgement.


## Candidate-local `<references/>` containment evidence

SCRIP-CORPUS-079 replays all **388 exact frozen literary Page revisions** and checks the raw self-closing `<references/>` spans against the same `<noinclude>...</noinclude>` regions used by the frozen render pipeline. The source-free probe finds **388 / 388 `<references/>` tokens inside `<noinclude>` and 0 outside**. Its contract SHA-256 is `3dde2e1ea259ccc4f855ad20dc8df588f9546a9ec181f84155175a86c3b139e3`.

That result changes the research decision, not the profile yet: for this frozen candidate, the observed `<references/>` shape is removed by the already-defined `strip_nontranscluded_region` step before provider reference semantics would be needed. The probe therefore records `candidate_local_drop_supported_by_containment=true`, but deliberately keeps `profile_rule_promoted=false` until an independent review and a separate promotion judgement.

Current MediaWiki documentation describes `<references />` as the placeholder that inserts the reference list produced by preceding `<ref>` tags (`https://www.mediawiki.org/wiki/Help:Cite`). Scriptorium does **not** rely on or reproduce that Cite behavior in this probe; the candidate-local conclusion comes only from exact frozen-source containment under the already-defined noinclude rule. No claim is made about `<references/>` outside stripped regions, historical Wikisource transclusion, or a general MediaWiki renderer.

## Source-free artifacts

- immutable render profile v1: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile.json), SHA-256 `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`
- immutable semantic backlog v1: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json), SHA-256 `4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2`
- independently reviewed replay v6: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v6.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v6.json), SHA-256 `c317eb5247701f0ad860811e9349f4e6f42274e72e8856eecb8a9aff610f988f`
- render-profile promotion layer: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile-yo-promotion-v1.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile-yo-promotion-v1.json), SHA-256 `153f6ceb89025da90971ddc265df680359ff498103bb47ecd68f86bb3205ed28`
- effective semantic backlog v2: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v2.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog-v2.json), SHA-256 `6d4ba2bb9ec78731d97d91c87d0628207ec880901e9d388fa7aa7c70fb20e3be`
- `<references/>` containment probe: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.references-containment-v1.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.references-containment-v1.json), SHA-256 `3dde2e1ea259ccc4f855ad20dc8df588f9546a9ec181f84155175a86c3b139e3`
- deterministic builders/validators: [`../../scriptorium/darwin_yo_render_profile_promotion.py`](../../scriptorium/darwin_yo_render_profile_promotion.py), [`../../scriptorium/darwin_references_containment.py`](../../scriptorium/darwin_references_containment.py)

## Gates unchanged

This promotion resolves one high-volume template shape, but it does not implement a complete renderer. `renderer_semantics_complete`, `renderer_implementation_ready`, `inter_page_composition_frozen`, `literary_body_count_and_digests_frozen`, `minimum_300k_proved`, `admitted_for_calibration`, `diagnostic_ready` and `m2_parity_admissible` remain false; `fantlab_source_edition_match=unknown`. M2 remains **0/5**.
