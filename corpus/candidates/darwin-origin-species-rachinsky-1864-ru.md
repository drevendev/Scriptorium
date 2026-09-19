# On the Origin of Species — Rachinsky 1864 Russian translation

This candidate records **Sergey A. Rachinsky's 1864 Russian translation** of Charles Darwin's *On the Origin of Species* as its own translation/source identity. It must not be collapsed with Darwin's English original, K. A. Timiryazev's Russian translation, other Russian translations, or rendered orthography transformations without an explicit transform/identity contract.

## Public-source witness

Russian Wikisource identifies the edition as **Ч. Дарвин. О происхождении видов**, translated by **Сергей Александрович Рачинский**, Saint Petersburg: **Издание книгопродавца А. И. Глазунова**, **1864**, **399 pages**.

Retained source-free anchors are:

- rendered edition-family page `О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)`, permanent revision **`oldid=5628021`**;
- ProofreadPage index `Индекс:Дарвин - О происхождении видов, 1864.djvu`, permanent revision **`oldid=4494408`**;
- shared route template, permanent revision **`oldid=3775868`**;
- parent topology witness, permanent revision **`oldid=5712882`** with `include="8-21,423-427"`.

The ProofreadPage index reports **`Закончено — Все страницы вычитаны и проверены`**. This is provenance/quality evidence for the transcription family; it is not by itself a literary-body or scan-binary freeze.

## Rendered route and ProofreadPage topology

The source-free route graph pins `/1` through `/14` plus `/Указатель`. Numbered routes cover displayed bibliographic pages **1–387** and the alphabetical index covers **389–399**. These displayed print-page spans are bibliographic route metadata rather than scan-page identity.

The exact shared-template topology references:

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

Those routes contribute **399 distinct Page-sequence dependencies**. The parent witness adds sequences **8–21** and **423–427**, another **19** non-overlapping dependencies, for **418 included Page-sequence dependencies** total.

Two omitted positions have exact source-free classification evidence: Page **114**, `oldid=3364724`, is explicitly excluded by route `/4`; Page **411**, `oldid=3364733`, is the sole omission between `/14` and `/Указатель`. Both Wikisource Page surfaces are source-declared `Без текста`. Equal-cardinality adjacent ranges uniquely align displayed print page **388** with Page sequence **411**, so page 388 is recorded as a source-declared no-text non-literary gap without OCR or visual scan interpretation.

## Exact 418-Page revision identity freeze

**SCRIP-CORPUS-034** now freezes the revision identity of every one of those 418 included Page dependencies without committing Page prose. Hosted capture requested only MediaWiki `ids|timestamp|sha1`; it returned exactly 418 distinct included sequences, excluded 114 and 411, and contained no wikitext/OCR/source-text field.

The capture is committed as four digest-pinned source-free shards plus one index:

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json) — topology contract, capture provenance, shard digests and gate boundary;
- `.page-revisions.01.json` through `.page-revisions.04.json` — compact tuples of **Page sequence, exact revision ID, revision timestamp and MediaWiki SHA-1** only.

The first included dependency is Page sequence **8**, exact revision **`oldid=4493767`**, timestamp `2022-05-19T10:40:06Z`; the last is sequence **427**, exact revision **`oldid=4494407`**, timestamp `2022-05-22T07:58:34Z`. The inventory also records newer revisions where present—for example sequence 426 is pinned at its captured exact revision rather than assuming all pages share a 2018/2022 edit epoch.

The initial hosted capture artifact was produced by workflow run `35471807464`, artifact `10592834383`. Its ZIP SHA-256 is `1fe9319448ea932a57c48378381e111cbcd6c7e8ca902d162aea1b93f675a014`; the extracted verbose capture JSON SHA-256 is `8979500217049380826c2d8c304dd94dc214087e3c356c16f5779e559115b375`. The committed compact shards preserve the same 418 identity tuples and are independently SHA-256 pinned by the index. Hosted replay re-queries the exact revision IDs and fails closed if title, timestamp or MediaWiki SHA-1 differs.

No literary prose, Page-namespace payload, DjVu/PDF bytes, OCR or screenshots are committed. Freezing revision identity does **not** mean the literary body has been selected or extracted.

## Provider-reported scan-file metadata

The retained source surface reports **27,368,263 bytes**, MIME `image/vnd.djvu`, dimensions **3744 × 5616**, **432 pages**, SHA-1 `75ef508588194ae74874272ce290f3ec1043ea9b`, current file-history display `11:45, 8 March 2016` by `Nonexyst`, and Archive.org locator `https://archive.org/details/oproiskhozhdenii00darw`.

That is deliberately only **provider-reported remote metadata**. Scriptorium has not independently frozen the DjVu byte stream or computed a local SHA-256 over it.

## Rights evidence

The retained Wikisource work surface explicitly states that the work is in the public domain in Russia and jurisdictions with a life-plus-70-or-shorter term; its translation-specific notice says exclusive rights have expired for all authors of the original and translation. This page records that source declaration as provenance evidence, not independent legal advice. Wikisource site text licensing remains separate from the public-domain status asserted for the work/translation.

## Corpus boundary

This candidate is still **not admitted** to the >=300,000-character calibration/profile corpus. The source family, rendered route graph, exact 418-dependency topology and now the exact revision identities of all 418 included Page pages are frozen source-free, but the literary body has not yet been deterministically composed or counted.

Still required before corpus admission:

- define an evidence-based literary-body composition rule for parent/front matter, numbered routes, alphabetical index and other apparatus while preserving no-text exclusions 114 and 411;
- implement deterministic fail-closed extraction/composition from the now-pinned Page revisions;
- compute literary-body character count including spaces plus raw/normalized digests;
- verify that the frozen body itself, not nominal page count or topology, clears **300,000 characters**.

Accordingly `source_identity_status=rendered_route_graph_proofreadpage_topology_and_418_page_revision_identities_frozen_literary_body_unfrozen` and `admitted_for_calibration=false`.

## FantLab boundary

FantLab work **`work969964`** identifies Darwin's 1859 English monograph. The currently exposed Russian translation there is **K. Timiryazev**, not Rachinsky's 1864 translation. No `/lp` result attributable to this exact Rachinsky source edition has been established. Keep `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.

## Canonical evidence

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json) — current translation/source identity and gate boundary.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json) — route/topology evidence captured before the Page-identity freeze; its historical `page_revision_set_unfrozen` boundary is superseded for Page identity by the index below, not for literary-body selection.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json) — authoritative source-free index for the 418 exact Page revision identities and four committed shards.

## Next evidence

A later bounded unit should use the pinned 418 Page identities to define a candidate-specific fail-closed literary-body extraction/composition contract, then compute source-free counts/digests and independently prove the >=300,000-character threshold. If byte-level scan identity becomes necessary, retrieve one exact DjVu byte stream and record independent byte count plus SHA-256 rather than promoting provider metadata. FantLab parity remains a separate, stricter source-matching problem.
