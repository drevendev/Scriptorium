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

A fail-closed source-shape probe found an important dependency that the four parent oldids do not express by themselves: Part 2 contains a `#lst` labeled-section transclusion from `Жизнь Клима Самгина (Горький)/Часть 2/part2`. Scriptorium now independently pins that dependency at **`oldid=2366546`** (page ID `580081`, timestamp `2016-11-29T05:49:23Z`) with **583,889 wikitext characters / 1,058,733 UTF-8 bytes** and wikitext SHA-256 **`173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`**. Exact-revision CI replay verifies it without committing source prose.

That discovery deliberately prevents a premature literary-body claim. Scriptorium has **not yet frozen the exact labeled-section selection/placement semantics of the Part 2 transclusion**, a candidate-specific fail-closed extraction profile for all four parts, the final four-part composition contract, or raw/`scriptorium-text-v1` composite digests. A parent-page oldid alone is therefore not treated as a complete body identity, and the extractor is not tuned toward FantLab's displayed count.

Accordingly the retained status is:

- `source_identity_status = revision_wikitext_source_graph_frozen_body_unfrozen`
- `fantlab_source_edition_match = unknown`
- `diagnostic_ready = false`
- `gate_ready = false`
- `m2_parity_admissible = false`
- main parity-catalog admission remains deferred until a deterministic literary body is replay-frozen.

The provenance record is `source-edition-traces/gorky-klim-samgin-ru.json`; the source-graph summary is `source-edition-traces/gorky-klim-samgin-ru.revisions.json`; the newly pinned dependency is `source-edition-traces/gorky-klim-samgin-ru.part2-part2.revision.json`. No source prose is committed. M2 remains **0/5 source-matched works**.
