# On the Origin of Species — Rachinsky 1864 Russian translation

This candidate records **Sergey A. Rachinsky's 1864 Russian translation** of Charles Darwin's *On the Origin of Species* as its own translation/source identity. It must not be collapsed with Darwin's English original, K. A. Timiryazev's Russian translation, other Russian translations, or rendered orthography transformations without an explicit transform/identity contract.

## Public-source witness

Russian Wikisource identifies the edition as **Ч. Дарвин. О происхождении видов**, translated by **Сергей Александрович Рачинский**, Saint Petersburg: **Издание книгопродавца А. И. Глазунова**, **1864**, **399 pages**.

Two earlier source-free anchors remain retained:

- rendered edition-family page `О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)`, permanent revision **`oldid=5628021`**;
- ProofreadPage index `Индекс:Дарвин - О происхождении видов, 1864.djvu`, permanent revision **`oldid=4494408`**.

The ProofreadPage index reports **`Закончено — Все страницы вычитаны и проверены`**. This is useful provenance/quality evidence for the transcription family, but it does not by itself freeze the underlying Page-namespace revisions, scan binary, OCR, or literary body.

### Rendered route graph

The source-free graph pins the exact rendered-route revisions underneath the edition parent: numbered routes `/1` through `/14` plus `/Указатель`. Their permanent revision IDs are recorded in [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json).

The route metadata reports displayed bibliographic print-page spans **1–387** for the introduction/chapter sequence and **389–399** for the alphabetical index. These displayed print-page spans are bibliographic route metadata, not a complete Page-namespace or scan-page identity.

### ProofreadPage transclusion topology

The exact source-free transclusion topology is now frozen one layer below the rendered routes without copying Page prose. The shared Wikisource route template is pinned at permanent revision **`oldid=3775868`**. It defines the following Page-sequence dependencies:

- `/1`: 22–56
- `/2`: 57–69
- `/3`: 70–85
- `/4`: 86–131, explicitly excluding **114**
- `/5`: 132–161
- `/6`: 162–190
- `/7`: 191–219
- `/8`: 220–245
- `/9`: 246–269
- `/10`: 270–297
- `/11`: 298–326
- `/12`: 327–348
- `/13`: 349–384
- `/14`: 385–410
- `/Указатель`: 412–422

Those rendered routes reference **399 Page-sequence dependencies** after the explicit route-4 exclusion. A later exact parent topology witness, permanent revision **`oldid=5712882`**, separately transcludes Page sequences **8–21** and **423–427**, adding **19** non-overlapping dependencies. Therefore the exact parent-plus-route topology references **418 distinct Page-sequence numbers**.

That count freezes topology only. Scriptorium has **not** yet pinned the exact revision ID/timestamp/MediaWiki SHA-1 for each of those 418 referenced Page pages, so it does not claim that their contents are revision-frozen.

Two omitted sequence positions now have exact source-free classification evidence:

- Page sequence **114**, permanent revision **`oldid=3364724`**, is explicitly excluded by route `/4`; its Wikisource Page surface says `Эта страница не требует вычитки` and places it in hidden category **`Без текста`**.
- Page sequence **411**, permanent revision **`oldid=3364733`**, is the single omitted sequence position between `/14` ending at 410 and `/Указатель` starting at 412; its Page surface carries the same no-proofreading / **`Без текста`** classification.

The page-388 gap is therefore no longer left unclassified. Route `/14` has equal-cardinality displayed/source spans 362–387 ↔ 385–410, while `/Указатель` has 389–399 ↔ 412–422. The sole one-page gap on both surfaces uniquely aligns displayed print page **388** with Page sequence **411**. Because exact Page revision `oldid=3364733` is source-declared `Без текста`, Scriptorium records page 388 as a **source-declared no-text non-literary gap**. This classification does not use OCR or visual interpretation of the scan.

No literary prose, Page-namespace payload, DjVu/PDF bytes, OCR, or screenshots are committed by this unit.

### Provider-reported scan-file metadata

The DjVu file behind the retained ProofreadPage family has a source-free provider-metadata identity recorded from the Wikimedia Commons file description as transcluded on Russian Wikisource. The retained source surface reports:

- **27,368,263 bytes**;
- MIME type **`image/vnd.djvu`**;
- dimensions **3744 × 5616**;
- **432 pages**;
- SHA-1 **`75ef508588194ae74874272ce290f3ec1043ea9b`**;
- current file-history display **`11:45, 8 March 2016`**, uploader **`Nonexyst`**;
- source locator `https://archive.org/details/oproiskhozhdenii00darw`.

The same source surface describes the file as a mechanical scan/public-domain source and shows Public Domain Mark 1.0. Scriptorium records those statements as source provenance.

This is deliberately **not a local binary freeze**. Scriptorium has not retrieved one exact DjVu byte stream in this unit, has not independently recomputed the provider SHA-1, and has not computed a SHA-256 over the binary. Provider-reported size/checksum metadata therefore strengthens source identity without substituting for independent byte-level verification.

## Rights evidence

The retained Wikisource work surface explicitly states that the work is in the public domain in Russia and jurisdictions with a life-plus-70-or-shorter term; its translation-specific notice says the exclusive rights have expired for all authors of the original and translation. Scriptorium records that source declaration as provenance evidence, not as independent legal advice.

The source page also exposes site text under CC BY-SA subject to Wikisource terms. Source-site licensing of page content is kept separate from the public-domain status asserted for the literary work/translation.

## Corpus boundary

This candidate is deliberately **not yet admitted** to the >=300,000-character calibration/profile corpus. The 399-page bibliographic length, rendered route graph, and now-frozen **418-dependency ProofreadPage topology** make the source identity materially stronger, but none is a substitute for the required literary-body character count including spaces.

Still required before corpus admission:

- exact source-free revision identities for the 418 included Page-namespace dependencies actually referenced by the frozen topology;
- an evidence-based literary-body composition decision for the parent/front matter, numbered routes, alphabetical index, and any other apparatus, while preserving the now-resolved no-text exclusions at Page sequences 114 and 411;
- a deterministic fail-closed extraction/composition contract;
- literary-body character count including spaces and raw/normalized digests;
- verification that the frozen body, not merely the print edition's nominal page count or transclusion topology, clears 300,000 characters.

Accordingly `source_identity_status=rendered_route_graph_proofreadpage_transclusion_topology_and_remote_scan_metadata_frozen_page_revision_set_unfrozen` and `admitted_for_calibration=false`. Transclusion topology and provider-reported scan metadata do not satisfy the literary-body threshold or complete Page-revision identity requirements.

## FantLab boundary

FantLab work **`work969964`** identifies Darwin's 1859 English monograph *On the Origin of Species*. The currently exposed Russian translation in that record is **K. Timiryazev**, not Rachinsky's 1864 translation. The work-level relation therefore does not establish that FantLab has a linguistic result for this Rachinsky text, nor that any analyzer input matches the Wikisource family.

No `/lp` result attributable to this exact translation/source edition has been established. Keep `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.

## Canonical evidence

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json) — translation identity, parent/index locators, exact transclusion-topology boundary, provider-reported scan metadata, bibliography, rights evidence, corpus boundary, and FantLab boundary.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json) — exact rendered route revisions, exact shared-template/parent Page-sequence topology, explicit no-text Page 114 / Page 411 evidence, resolved displayed page 388, provider scan metadata, and the still-unfrozen complete Page-revision/body boundary.

## Next evidence

A later bounded unit should pin the exact revision ID/timestamp/MediaWiki SHA-1 for each of the **418 Page-sequence dependencies** referenced by the now-frozen topology. Only after those included Page revisions are frozen should Scriptorium define a candidate-specific fail-closed literary-body extraction/composition contract and compute source-free counts/digests. If a scan-byte identity becomes necessary, retrieve one exact DjVu byte stream and independently record its byte count plus SHA-256 rather than promoting provider metadata. Only after the exact literary body proves >=300,000 characters may this translation be admitted to the general calibration/profile corpus. FantLab parity remains a separate, stricter source-matching problem.
