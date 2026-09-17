# Maxim Gorky — *The Life of Klim Samgin* (`gorky-klim-samgin-ru`)

This page is a **source-free provenance snapshot**, not a FantLab parity claim and not a copy of the novel.

FantLab's linguistic-analysis surface for work `427585` reports **3,789,857 characters** and **531,192 words**, analyzed on **19 September 2022**. That easily clears Scriptorium's >=300,000-character calibration threshold. FantLab does not disclose which edition or immutable byte stream was uploaded, so the analyzer-input identity remains unknown.

Russian Wikisource exposes a legally usable original-Russian transcription family for *Жизнь Клима Самгина (Сорок лет)*. Its work index identifies **Library Moshkov** as the electronic source, links four literary parts, and explicitly marks the original work public domain. The retained work-index locator is `oldid=5628161`.

Scriptorium now replay-freezes the exact **revision-wikitext identity** of all four retained literary part revisions. The manifests store only source-free metadata and digests:

| Part | oldid | Revision timestamp | Wikitext characters | Wikitext SHA-256 | Wikisource bibliographic source |
| --- | ---: | --- | ---: | --- | --- |
| 1 | `5733765` | `2026-07-28T12:17:48Z` | 964,649 | `556dab4e3c66c8d597dd19f5db6ddae8c1eb52649a97025ff61d4ce388fad575` | Gorky, Collected Works, GIKhL, Moscow, 1952, vol. 19 |
| 2 | `5198033` | `2024-11-26T11:16:35Z` | 581,888 | `34dc8bf7d1dc77f9aa1686ef0ac348101beac19ccd97d467ee3857e014ad8853` | Gorky, Collected Works, GIKhL, Moscow, 1952, vol. 20 |
| 3 | `5138882` | `2024-05-24T20:48:07Z` | 681,084 | `95d782223c9c6893131fbb2ed7a4a6c4b2c14aea074083721d9425b1d30c8182` | Gorky, Collected Works, GIKhL, Moscow, 1952, vol. 21 |
| 4 | `5724453` | `2026-06-21T18:58:09Z` | 1,001,169 | `ce353961f4d76a7f6775456ce1df53d23f33c3073f2126c716fa69561d119bbb` | Gorky, Collected Works, GIKhL, Moscow, 1953, vol. 22 |

The ordered four-part revision set totals **3,228,790 revision-wikitext characters / 5,902,920 UTF-8 bytes** and has ordered source-identity SHA-256 `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`. This digest identifies the ordered source-free revision metadata projection; it is **not** a digest of a composed literary body.

The revision freeze still does **not** establish a Scriptorium literary-body identity. No candidate-specific fail-closed extraction profile, literary composition contract, or raw/`scriptorium-text-v1` normalized composite digest is frozen in this unit. It also does not establish that FantLab analyzed these revisions or this transcription family.

Accordingly the retained status is:

- `source_identity_status = revision_wikitext_frozen_body_unfrozen`
- `fantlab_source_edition_match = unknown`
- `diagnostic_ready = false`
- `gate_ready = false`
- `m2_parity_admissible = false`
- main parity-catalog admission remains deferred until a deterministic four-part literary body is replay-frozen.

The provenance record is `source-edition-traces/gorky-klim-samgin-ru.json`; the ordered revision-set manifest is `source-edition-traces/gorky-klim-samgin-ru.revisions.json`, which links the four exact per-part revision manifests. No source prose is committed. M2 remains **0/5 source-matched works**.
