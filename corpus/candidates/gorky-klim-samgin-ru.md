# Maxim Gorky — *The Life of Klim Samgin* (`gorky-klim-samgin-ru`)

This page is a **source-free provenance snapshot**, not a FantLab parity claim and not a copy of the novel.

FantLab's linguistic-analysis surface for work `427585` reports **3,789,857 characters** and **531,192 words**, analyzed on **19 September 2022**. That easily clears Scriptorium's >=300,000-character calibration threshold. FantLab does not disclose which edition or immutable byte stream was uploaded, so the analyzer-input identity remains unknown.

Russian Wikisource exposes a legally usable original-Russian transcription family for *Жизнь Клима Самгина (Сорок лет)*. Its work index identifies **Library Moshkov** as the electronic source, links four literary parts, and explicitly marks the original work public domain. The retained work-index locator is `oldid=5628161`.

Scriptorium replay-freezes the exact **revision-wikitext identity** of all four retained literary part revisions. The manifests store only source-free metadata and digests:

| Part | oldid | Revision timestamp | Wikitext characters | Wikitext SHA-256 | Wikisource bibliographic source |
| --- | ---: | --- | ---: | --- | --- |
| 1 | `5733765` | `2026-07-28T12:17:48Z` | 964,649 | `556dab4e3c66c8d597dd19f5db6ddae8c1eb52649a97025ff61d4ce388fad575` | Gorky, Collected Works, GIKhL, Moscow, 1952, vol. 19 |
| 2 | `5198033` | `2024-11-26T11:16:35Z` | 581,888 | `34dc8bf7d1dc77f9aa1686ef0ac348101beac19ccd97d467ee3857e014ad8853` | Gorky, Collected Works, GIKhL, Moscow, 1952, vol. 20 |
| 3 | `5138882` | `2024-05-24T20:48:07Z` | 681,084 | `95d782223c9c6893131fbb2ed7a4a6c4b2c14aea074083721d9425b1d30c8182` | Gorky, Collected Works, GIKhL, Moscow, 1952, vol. 21 |
| 4 | `5724453` | `2026-06-21T18:58:09Z` | 1,001,169 | `ce353961f4d76a7f6775456ce1df53d23f33c3073f2126c716fa69561d119bbb` | Gorky, Collected Works, GIKhL, Moscow, 1953, vol. 22 |

The ordered four-parent revision set totals **3,228,790 revision-wikitext characters / 5,902,920 UTF-8 bytes** and has ordered source-identity SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`. This digest identifies the ordered source-free parent-revision metadata projection; it is **not** a digest of a composed literary body.

## Part 2 source graph

Part 2 contains one `#lst` call to `Жизнь Клима Самгина (Горький)/Часть 2/part2`. Scriptorium independently pins that dependency at **`oldid=2366546`** (page ID `580081`, timestamp `2016-11-29T05:49:23Z`) with **583,889 wikitext characters / 1,058,733 UTF-8 bytes** and wikitext SHA-256 **`173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`**.

A source-free replay established that this is **not a labeled-section selection**. The exact parent invocation has one argument—the target page—with parent offsets `581758..581810` and invocation SHA-256 `89969a0424eb9fa332d132216bbeb96647239ab613cf6dadf6c5e2087ff0f15e`. Upstream Wikimedia `LabeledSectionTransclusion` evidence shows that after target resolution, this target-only shape delegates the whole target template DOM to MediaWiki frame expansion with no label filter. The source-free contract is `source-edition-traces/gorky-klim-samgin-ru.part2-lst.json`.

The pinned dependency contains **six `poemx1` template invocations**. Scriptorium freezes a deterministic historical-reconstruction anchor for `Шаблон:Poemx1`: select the latest template revision not later than the pinned Part 2 save timestamp (`2024-11-26T11:16:35Z`). That policy resolves to **`oldid=5142743`** (page ID `54236`, timestamp `2024-06-02T02:25:12Z`), with **2,412 wikitext characters / 2,918 UTF-8 bytes** and SHA-256 **`fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`**. This remains **inferred reconstruction evidence**, not proof of the actual parser-cache or render-time template state used by MediaWiki in November 2024.

Scriptorium applies only documented `noinclude` / `includeonly` / `onlyinclude` selection semantics to that pinned template. For this revision the frozen source-free control inventory is **two `noinclude` pairs, one `includeonly` pair, and zero `onlyinclude` pairs**. After selection, the raw `doc` invocation and raw `PAGENAME` occurrence disappear. The unresolved post-selection construct graph is `#expr` ×2, `#if` ×5, `#ifeq` ×5, `#iferror` ×1 and `#tag` ×1 targeting `poem`; there are no ordinary template dependencies or magic words.

The literal triple-brace surface of the post-selection input is also frozen at SHA-256 `86ad628a9d8fc3d904fd513a1b4335f4e9f816ceedfa2af736e8e3a94e32ffbf`. It contains **21 parameter references** across names `1`, `2`, `3`, `fixed`, `poem`, `small`, and `width`. Scriptorium reproduces missing-versus-defined-empty/default behavior for those literal parameter names while rejecting unsupported dynamic names.

## Concrete `poemx1` frame bindings

The six real invocations are replay-frozen source-free in `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.bindings.json`. Each exact call has **two anonymous arguments and zero named arguments**. In all six calls, anonymous parameter `1` is explicitly defined as the empty string, while anonymous parameter `2` is defined and non-empty. The remaining frozen template-surface names—`3`, `fixed`, `poem`, `small`, and `width`—are omitted in all six calls. There are no duplicate assignments and no effective binding names outside the frozen parameter surface.

The invocation identities are source-free: the artifact stores parent offsets, character/byte counts and SHA-256 digests rather than argument prose. Across the six calls there are 12 assignments total. This binding evidence matters because it narrows the next historical-expansion layer to the template behavior under `1=""`, `2=<defined raw argument>`, with defaults/undefined behavior applying to the other observed surface names.

## Frozen parser-control reachability

The candidate-specific source-free control artifact `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.control.json` now resolves only the documented `#if` / `#ifeq` branch choices that are forced by that exact shared frame. From the pinned static graph, **4 of 5 `#if` calls and 3 of 5 `#ifeq` calls are reachable**, together with the single `#tag:poem`. The two `#expr` calls and the single `#iferror` call are on branches that are never reached by any of the six frozen invocations.

Concretely, the empty title omits the title block; omitted `fixed` selects automatic centering/fit-content and then the conditional-width path; omitted `width` makes that width branch empty before either arithmetic call can execute; omitted `poem` selects the default-font path; omitted `small` does not enable the small-font path; and omitted parameter `3` omits the signature block. The reducer is fail-closed against changes in the template revision/digests, static construct inventory, literal parameter surface, invocation count or frame shape.

This deliberately **does not** implement generic `#expr` or `#iferror` semantics merely to satisfy a static inventory: the exact frozen frames cannot reach them. The one live operation is `#tag:poem` with parameter `2` as its content.

## Frozen parameter-2 expansion surface

The exact six parameter-2 values are revalidated source-free in `source-edition-traces/gorky-klim-samgin-ru.poemx1-content.json`. Across the six values the artifact records **324 characters / 589 UTF-8 bytes**, **15 value-local lines**, and **9 newline characters**, while persisting only counts and SHA-256 identities rather than literary prose.

For all six exact values the observed recursive template-expansion surface is empty: **0 double-brace template/parser constructs, 0 triple-brace parameter constructs, 0 XML-like tags, 0 wikilinks, 0 external links, and 0 apostrophe-markup runs**. No value has a leading-colon line, leading-space line, or blank line. Therefore the template-expansion prerequisite for these exact inserted values is identity and **no additional template dependency resolution is required** before the live `#tag:poem` call.

## Reached `#tag:poem` source surface

A dedicated replay now re-fetches exact template revision `5142743`, reapplies the frozen partial-transclusion layer, and source-freezes the one reached extension call as `source-edition-traces/gorky-klim-samgin-ru.poem-tag-surface.json`. The historical source call has **exactly one top-level argument: content, with zero tag attributes**. Its whole source expression is 22 ASCII bytes with SHA-256 `802765da0c42ff7a629167637cb97926023e0a60f11e58a2677849166c958233`.

The content expression is exactly one empty-default reference to template parameter `2`: its source expression is 8 ASCII bytes with SHA-256 `64e1af6f2e37ee4bcf0ab4f139c75b671321279929eade54fae4cf49be0346f9`. There are no nested parser functions, templates, magic words, HTML tags or secondary extension calls in that content expression, and there are **no attribute value expressions to evaluate at all**. The artifact binds all six already-frozen parameter-2 identities to this same reached call without storing their prose.

This closes the previously open `#tag:poem` argument/attribute-surface prerequisite more strongly than expected: no candidate-specific attribute branch remains. It still does **not** reproduce MediaWiki core recursive parsing or the Poem extension's output transformation, and it does not establish which Poem commit Russian Wikisource actually deployed. Those rendering layers remain required before resolved Part 2 bytes can be claimed.

Therefore there is still **no resolved Part 2 wikitext identity**, no candidate-specific four-part literary-body extraction/composition contract, and no raw/`scriptorium-text-v1` composite digest. The extractor is not tuned toward FantLab's displayed count.

Accordingly the retained status is:

- `source_identity_status = revision_wikitext_source_graph_target_only_lst_poemx1_revision_inclusion_parameter_surface_invocation_bindings_control_flow_parameter2_and_tag_surface_frozen_body_unfrozen`
- `fantlab_source_edition_match = unknown`
- `diagnostic_ready = false`
- `gate_ready = false`
- `m2_parity_admissible = false`
- main parity-catalog admission remains deferred until a deterministic literary body is replay-frozen.

The provenance record is `source-edition-traces/gorky-klim-samgin-ru.json`; the source-graph summary is `source-edition-traces/gorky-klim-samgin-ru.revisions.json`; the dependency revision is `source-edition-traces/gorky-klim-samgin-ru.part2-part2.revision.json`; the target-only transclusion contract is `source-edition-traces/gorky-klim-samgin-ru.part2-lst.json`; the historical `poemx1` anchor/raw-shape evidence is `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.revision.json` plus `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.shape.json`; the post-inclusion graph is `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.transclusion.json`; the literal parameter surface is `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.parameters.json`; concrete invocation/frame bindings are `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.bindings.json`; frozen parser-control reachability is `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.control.json`; the source-free parameter-2 surface is `source-edition-traces/gorky-klim-samgin-ru.poemx1-content.json`; and the reached extension-call surface is `source-edition-traces/gorky-klim-samgin-ru.poem-tag-surface.json`. No source prose is committed. M2 remains **0/5 source-matched works**.
