# Darwin/Rachinsky 1864 — unresolved rendering semantics

This public source-free companion to `darwin-origin-species-rachinsky-1864-ru` exposes the remaining rendering-semantic work after the reviewed exact-388 Page surface and fail-closed render profile were frozen.

No literary source text, Page wikitext, template argument values, rendered prose, OCR or scan bytes are stored here. Counts come only from the already frozen render profile SHA-256 `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`.

## Remaining surface

The profile still has **43 unresolved shapes**:

| Research track | Shapes | Observed occurrences |
| --- | ---: | ---: |
| provider-template semantics | 37 | 4,579 |
| provider-reference semantics | 3 | 466 |
| provider-math semantics | 2 | 52 |
| inter-page semantics | 1 | 4 |

Those totals exactly preserve the reviewed boundary: **5 unresolved tag shapes / 518 tag tokens** and **38 unresolved template shapes / 4,583 invocations**.

## Mechanical next target

The deterministic backlog ranks unresolved items by descending observed occurrence count with stable tie-breaking. The first research target is template **`ё`**, arity **0 positional / 0 named**, observed **2,227 times** (2,227 / 4,583 unresolved template invocations).

This ranking is **not a semantics claim**. `ё` remains `semantic_status=unresolved`; a separate bounded unit must establish its provider behavior with independent evidence before the renderer profile may change.

The next two rows are self-closing `<references/>` (**388**) and template `ВАР` with arity 2/0 (**388**). Reference/math behavior and the inter-page-sensitive `nop` track remain independently reviewable rather than being folded into one guessed renderer policy.

## `{{ё}}` documentation and replay-dependency evidence

SCRIP-CORPUS-047 established the documented semantic class. Official Russian Wikisource documentation at permanent revision `oldid=5090323` identifies zero-argument `{{ё}}` as the lowercase shorthand of the conditional `ЕЁ` yoification family: the documented output is **`ё` in forced-yoification mode and `е` otherwise**. Proofread help is independently pinned at permanent revision `oldid=5731079` (2026-07-19), where `{{ё}}` / `{{ё!}}` are described as the mechanism used to support yoified and non-yoified finished-text variants.

SCRIP-CORPUS-048 corrects the dependency model used to interpret old Page revisions. Official MediaWiki `Help:History` at permanent revision `oldid=8524540` states that wikitext history and rendered-page history are different and that an old page revision still uses the **current versions of templates and images** unless old versions have been renamed. MediaWiki `Transclusion/en` at permanent revision `oldid=8551508` describes transclusion as a live link whose targets update when the template changes and references the lack of versioned transclusion support (`T31051`).

Therefore the retained Darwin Page `oldid`s freeze Page wikitext identity, **not** the `Шаблон:ё` / `Шаблон:ЕЁ` revisions that will be used by a later replay. Looking up those template revisions at the 2018/2022 Page-save timestamps would not bind deterministic rendering and is no longer the queued prerequisite.

The corrected prerequisite is to freeze the exact `Шаблон:ё` and `Шаблон:ЕЁ` revisions, plus any nested dependencies, used by the chosen replay/rendering environment at analysis time — or to use an explicitly version-pinned template-expansion mechanism — and then validate the conditional outputs before any render-profile promotion.

A retained 2018 Page witness remains useful as Page-wikitext provenance context (Page sequence 11, revision `3358032`, timestamp `2018-08-13T19:18:33Z`), but its save timestamp is explicitly **not** a template-revision binding.

Consequently `ё` deliberately remains in the unresolved backlog and the render profile is unchanged.

Source-free evidence artifact:

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-evidence.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-evidence.json)
- schema: `scriptorium-darwin-template-yo-documentation-evidence-v2`
- evidence SHA-256: `d92bdfcad71aaa8a50f9f35b5b1ada462ed41619400c40576d0603cf154877dc`
- Wikisource template-documentation permalink: `https://ru.wikisource.org/w/index.php?title=Шаблон:ЕЁ/Документация&oldid=5090323`
- Wikisource proofread-help permalink: `https://ru.wikisource.org/w/index.php?title=Справка:Вычитка&oldid=5731079`
- MediaWiki history-model permalink: `https://www.mediawiki.org/w/index.php?title=Help:History&oldid=8524540`
- MediaWiki transclusion-model permalink: `https://www.mediawiki.org/w/index.php?title=Transclusion/en&oldid=8551508`
- builder/validator: [`../../scriptorium/darwin_template_yo_evidence.py`](../../scriptorium/darwin_template_yo_evidence.py)

The evidence builder recomputes the full canonical semantic-backlog self-digest before deriving this record. A stale `backlog_sha256` with any non-target backlog mutation therefore fails closed instead of being copied into a new evidence artifact.

## Frozen backlog artifact

Canonical source-free backlog artifact:

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.semantic-backlog.json)
- schema: `scriptorium-darwin-render-semantic-backlog-v1`
- backlog SHA-256: `4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2`
- builder/validator: [`../../scriptorium/darwin_semantic_backlog.py`](../../scriptorium/darwin_semantic_backlog.py)

The backlog artifact is derived only after the existing render profile validates against its frozen source surface. Any profile/surface drift fails before backlog derivation.

## Gates unchanged

This slice does not implement rendering and does not advance corpus or FantLab parity gates. The following remain false/unknown: `renderer_semantics_complete`, `renderer_implementation_ready`, `inter_page_composition_frozen`, `literary_body_count_and_digests_frozen`, `minimum_300k_proved`, `admitted_for_calibration`, `diagnostic_ready`, `m2_parity_admissible`; `fantlab_source_edition_match=unknown`. M2 remains **0/5**.
