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

Part 2 contains one `#lst` call to `Жизнь Клима Самгина (Горький)/Часть 2/part2`. Scriptorium independently pins that dependency at **`oldid=2366546`** (page ID `580081`, timestamp `2016-11-29T05:49:23Z`) with **583,889 wikitext characters / 1,058,733 UTF-8 bytes** and wikitext SHA-256 **`173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`**.

A later source-free replay established that this is **not a labeled-section selection**. The exact parent invocation has only one argument—the target page—with parent offsets `581758..581810` and invocation SHA-256 `89969a0424eb9fa332d132216bbeb96647239ab613cf6dadf6c5e2087ff0f15e`. Current upstream Wikimedia `LabeledSectionTransclusion` source shows that after resolving the target, a target-only `#lst` call returns `newFrame->expand(root)`: the whole target template DOM is delegated to normal MediaWiki frame expansion, with no label filter. The source-free contract is `source-edition-traces/gorky-klim-samgin-ru.part2-lst.json`.

The pinned dependency contains **six `poemx1` template invocations**. Scriptorium freezes a deterministic historical-reconstruction anchor for `Шаблон:Poemx1`: select the latest template revision not later than the pinned Part 2 save timestamp (`2024-11-26T11:16:35Z`). That policy resolves to **`oldid=5142743`** (page ID `54236`, timestamp `2024-06-02T02:25:12Z`), with **2,412 wikitext characters / 2,918 UTF-8 bytes** and SHA-256 **`fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`**. CI re-resolves the as-of selection and separately re-fetches the exact pinned revision. This anchor remains **inferred reconstruction evidence**, not proof of the actual parser-cache or render-time template state used by MediaWiki in November 2024.

The next provenance layer is now explicit and replayable. MediaWiki's documented partial-transclusion rules say that `noinclude` content is excluded, `includeonly` content participates in transclusion, and the presence of `onlyinclude` restricts transclusion to material inside `onlyinclude`. Scriptorium applies only that control-tag layer to pinned `poemx1` oldid `5142743`, failing closed on malformed control markup or `nowiki` cases that need separate MediaWiki handling.

For this exact revision the frozen source-free control inventory is **two `noinclude` pairs, one `includeonly` pair, and zero `onlyinclude` pairs**. Applying those rules removes the raw `doc` invocation, its `templatedata` documentation surface, **and the raw `PAGENAME` magic-word occurrence** from the effective transclusion graph. The remaining unresolved constructs are:

- parser functions: `#expr` ×2, `#if` ×5, `#ifeq` ×5, `#iferror` ×1, `#tag` ×1;
- `#tag` target: `poem` ×1;
- magic words: **none**;
- ordinary template transclusions: **none**;
- remaining ordinary HTML-like tags in the post-selection input: `div` ×6.

The immutable source-free artifact is `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.transclusion.json`; the raw pre-selection diagnostic remains `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.shape.json`. This is a meaningful narrowing: no additional mutable ordinary-template revision or magic-word dependency is exposed by `poemx1` after documented inclusion selection. It is **not** equivalent to reproducing MediaWiki expansion.

Scriptorium now also freezes the **literal triple-brace parameter-reference/default surface** of that post-selection template input. The source-free manifest is `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.parameters.json`, bound to post-selection input SHA-256 `86ad628a9d8fc3d904fd513a1b4335f4e9f816ceedfa2af736e8e3a94e32ffbf`. It contains **21 parameter references** across literal names `1`, `2`, `3`, `fixed`, `poem`, `small`, and `width`; the observed reference counts are `1`×2, `2`×1, `3`×2, `fixed`×6, `poem`×1, `small`×6, `width`×3. All except one bare `fixed` reference have defaults; empty defaults are observed for `1`×2, `2`×1, `3`×2, `fixed`×1, `poem`×1, and `width`×1. The bounded implementation preserves MediaWiki's missing-versus-defined-empty distinction and default behavior for **literal** parameter names, but deliberately rejects dynamic/unsupported names rather than guessing them.

This does **not** mean the six real `poemx1` calls have been expanded. Invocation argument binding, recursive expansion of inserted argument wikitext, `#expr` / `#if` / `#ifeq` / `#iferror`, and `#tag:poem` still have to be reproduced or otherwise source-bound before resolved Part 2 bytes can be claimed. Historical render equivalence remains unproven.

Therefore there is still **no resolved Part 2 wikitext identity**, no candidate-specific four-part literary-body extraction/composition contract, and no raw/`scriptorium-text-v1` composite digest. The extractor is not tuned toward FantLab's displayed count.

Accordingly the retained status is:

- `source_identity_status = revision_wikitext_source_graph_target_only_lst_poemx1_revision_inclusion_and_literal_parameter_surface_frozen_body_unfrozen`
- `fantlab_source_edition_match = unknown`
- `diagnostic_ready = false`
- `gate_ready = false`
- `m2_parity_admissible = false`
- main parity-catalog admission remains deferred until a deterministic literary body is replay-frozen.

The provenance record is `source-edition-traces/gorky-klim-samgin-ru.json`; the source-graph summary is `source-edition-traces/gorky-klim-samgin-ru.revisions.json`; the dependency revision is `source-edition-traces/gorky-klim-samgin-ru.part2-part2.revision.json`; the target-only transclusion contract is `source-edition-traces/gorky-klim-samgin-ru.part2-lst.json`; the historical `poemx1` anchor/raw-shape evidence is `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.revision.json` plus `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.shape.json`; the post-inclusion effective graph is `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.transclusion.json`; and the literal parameter surface is `source-edition-traces/gorky-klim-samgin-ru.poemx1-template.parameters.json`. No source prose is committed. M2 remains **0/5 source-matched works**.
