# Corpus candidates

This directory stores **metadata and derived identity only**, not book text. Candidate admission follows the repository corpus rule: a calibration/benchmark work must have at least 300,000 characters including spaces and a documented legal basis. A legally usable public transcription is not automatically the text FantLab analyzed; source identity and parity remain separate claims.

## Anna Karenina diagnostic candidate

`tolstoy-anna-karenina-ru` now has a reproducibly frozen Russian Wikisource/FEB candidate. The committed revision manifest records all 239 chapter revision IDs, revision timestamps, MediaWiki SHA-1 identities, the deterministic `scriptorium-wikisource-body-v1` extraction contract, the `scriptorium-wikisource-composite-v1` composition order, and composite hashes. No source prose is committed.

The frozen composite contains **1,705,605 characters including spaces** and has raw and `scriptorium-text-v1` normalized SHA-256 `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`. FantLab displays **1,692,647 characters** for its 2022 analysis, a difference of **12,958 characters**. That difference is diagnostic evidence only: FantLab does not disclose the edition or bytes of its uploaded analyzer input, and its display/counting normalization may also differ.

Therefore the candidate is ready for a **diagnostic field-by-field comparison**, but `fantlab_source_edition_match` remains `unknown`, it is not M2 parity evidence, and the reproduction gate remains **0/5 source-matched works** until independent evidence ties FantLab's analyzer input to the same frozen source.

Canonical evidence:

- `source-edition-traces/tolstoy-anna-karenina-ru.json` — provenance, legal/source boundary, admissibility and next evidence.
- `source-edition-traces/tolstoy-anna-karenina-ru.revisions.json` — packed source-free 239-revision identity and composite hashes.
- `../../scriptorium/wikisource_freeze.py` — deterministic fetch/extraction/composition implementation.

## Resurrection diagnostic candidate

`tolstoy-resurrection-ru` is now a second reproducibly frozen public-domain candidate. Russian Wikisource identifies Alexey Komarov's library as its transcription source; Komarov's source page completes the citation as **L. N. Tolstoy, Collected Works in eight volumes, volume 6, Moscow: Lexika, 1996**. The work has **59 + 42 + 28 = 129 chapters**, and the committed source-free manifest pins every chapter revision ID, revision timestamp and MediaWiki SHA-1 identity in deterministic part/chapter order.

The frozen extraction uses the explicit `scriptorium-wikisource-resurrection-body-v1` contract because the source set contains two observed page shapes: some chapters wrap prose in one or more `text`/`indent` divs, while others place prose directly after the `Отексте` header. Exact-revision replay reconstructs a **890,835-character** composite with raw and `scriptorium-text-v1` normalized SHA-256 `2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`. No source prose is committed.

FantLab's 19 September 2022 analysis displays **881,244 characters** and **126,457 words**, a character-count difference of **9,591** from this frozen public candidate. That difference is diagnostic-only: FantLab still discloses neither the analyzer-input edition nor immutable bytes, and its TXT excerpt link is not source-match evidence. `fantlab_source_edition_match` therefore remains `unknown`; the candidate may now support source-frozen diagnostic comparisons but not M2 parity evidence, so the reproduction gate remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/tolstoy-resurrection-ru.json` — provenance, legal/source boundary, frozen identity and admissibility.
- `source-edition-traces/tolstoy-resurrection-ru.revisions.json` — compact source-free 129-revision identity and composite hashes.
- `../../scriptorium/resurrection_freeze.py` — versioned source-specific extraction and exact-revision replay implementation.

## Brothers Karamazov frozen candidate

`dostoevsky-brothers-karamazov-ru` now has a reproducibly frozen Russian Wikisource/RVB public-domain candidate. The committed source-free manifest pins **98 admitted source segments**: the work-index authorial dedication/epigraph, the separate author preface, 93 numbered chapters across twelve books, and three epilogue chapters. Navigation-only book and epilogue wrapper pages are excluded. Every admitted segment has an exact revision ID, timestamp and MediaWiki SHA-1 identity; the extraction contract is versioned as `scriptorium-wikisource-karamazov-body-v7` and replay is pinned to those exact revisions.

The frozen composite contains **1,810,351 characters including spaces** (3,261,432 UTF-8 bytes) and has raw and `scriptorium-text-v1` normalized SHA-256 `26b9991c95b30d262c24ae38fb2332333a58df588a62a4310f9e5c4b507dbce6`. The extractor handles only source-observed, explicitly bounded Wikisource markup: editor notes are excluded, level-5/6 literary subheadings preserve visible text, numeric line-start `Indent` inside the observed `Poem1` shape is treated as layout, unambiguous long-form `Опечатка` emits its corrected text, and zero-argument `NB` preserves the visible nota-bene marker. Unsupported shapes still fail closed. No source prose is committed.

FantLab's 18 September 2022 analysis displays **1,807,107 characters** and **281,507 words**, so its displayed character count is **3,244 lower** than the frozen public candidate. That difference is evidence against treating the two byte streams as established identity; it does not prove which edition or normalization FantLab used. FantLab does not disclose the immutable analyzer input, and its current TXT excerpt route redirects to a LitRes trial endpoint. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_comparison_admissible=false`, `m2_parity_admissible=false`, and the M2 reproduction gate remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/dostoevsky-brothers-karamazov-ru.json` — bibliographic provenance, frozen public identity, legal/source boundary and admissibility.
- `source-edition-traces/dostoevsky-brothers-karamazov-ru.revisions.json` — compact source-free 98-revision identity and composite hashes.
- `../../scriptorium/karamazov_freeze.py` — versioned source-specific extraction and exact-revision replay implementation.

## Silver Dove frozen modernist candidate

`bely-silver-dove-ru` is the first retained candidate deliberately added to move the corpus beyond its nineteenth-century Russian-classic concentration. FantLab's 19 September 2022 linguistic analysis reports **549,050 characters** and **83,369 words**, so the work clears the >=300,000-character calibration threshold.

Russian Wikisource publishes the complete work on one page, explicitly marks the literary work public domain in Russia, and cites **Andrei Bely, Works in two volumes, Moscow: Khudozhestvennaya literatura, 1990, volume 1, pp. 377–642**, with the electronic version credited to V. Esaulov on 19 August 2006. The source-free manifest now pins permanent revision `oldid=5588003` at `2025-07-30T21:54:23Z`, its MediaWiki SHA-1 and wikitext SHA-256, plus the versioned `scriptorium-wikisource-silver-dove-body-v1` extraction contract. The extractor retains the authorial preface and literary headings while excluding page/bibliographic scaffolding, empty level-three layout markup, the trailing Wikisource editorial publication note and category links; unsupported remaining markup fails closed. No source prose is committed.

The frozen public candidate contains **563,125 characters including spaces** (1,039,363 UTF-8 bytes) and has raw and `scriptorium-text-v1` normalized SHA-256 `496dad8aadaca13f3ce6ef8560b53bcd32c75b5b03f28f13f7735303bb4f7183`. FantLab's displayed count is **14,075 characters lower**. That delta is evidence of non-identity or differing extraction/counting policy, not permission to tune normalization and not proof of a source match.

The public metadata also preserves an unresolved bibliographic discrepancy: FantLab labels the work 1910 while Wikisource metadata says 1909. Scriptorium does not assume whether this reflects serialization versus book publication or another cataloging convention. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and M2 remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/bely-silver-dove-ru.json` — FantLab counts, public-domain/source-edition evidence, frozen public identity, diversity rationale, unresolved publication metadata and admissibility.
- `source-edition-traces/bely-silver-dove-ru.revisions.json` — source-free exact revision identity and composite hashes.
- `../../scriptorium/silver_dove_freeze.py` — versioned source-specific extraction and exact-revision replay implementation.

## Petersburg traced modernist candidate

`bely-petersburg-1916-ru` adds a second long Andrei Bely work while preserving a concrete edition identity. FantLab's 19 September 2022 linguistic analysis reports **944,182 characters** and **130,217 words**, so the work clears the >=300,000-character calibration threshold.

The retained source candidate is not the generic Russian Wikisource landing page. That landing page explicitly sits in the `Тексты без ссылок на источники` category and exposes edition navigation rather than a source-identified complete transcription, so it is useful only as a public-domain/bibliographic cross-check. Instead, Scriptorium records the Wikimedia Commons **632-page facsimile of the first 1916 book publication**, described there as a mechanical reproduction of the three *Sirin* installments from 1913–1914. Commons explicitly marks the work public domain. No scan pages, OCR, or source prose are committed.

The permanent Commons file-description revision **`oldid=1046280975` freezes descriptive page wikitext, not the PDF binary**. Current Page Information for file page ID **47639472** lists `Upload: Allow all users (infinite)` inside the **Page protection** table; Scriptorium treats that only as protection metadata and does not infer overwrite capability from it. The current rendered file page separately states **`You cannot overwrite this file.`** Neither operational observation identifies the PDF contents. A later freeze must therefore retrieve one specific PDF byte stream and record its exact byte count plus SHA-256 in source-free metadata before Scriptorium can claim that binary as frozen.

This unit deliberately remains at **source-edition tracing**. Scriptorium has not yet recorded a PDF snapshot digest, selected literary pages, or a deterministic OCR/extraction contract, and FantLab does not disclose which Petersburg edition or byte stream it analyzed. The 1916 first book edition is also kept distinct from Bely's materially revised 1922 edition. Therefore `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and the M2 reproduction gate remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/bely-petersburg-1916-ru.json` — FantLab counts, explicit 1916 facsimile identity, public-domain evidence, Commons description-vs-binary identity boundary, Wikisource provenance warning, edition-family boundary and next evidence required before diagnostics.

## Hyperboloid of Engineer Garin revision-frozen early-Soviet SF candidate

`tolstoy-hyperboloid-garin-wikisource-ru` adds a new author and an early Soviet science-fiction/adventure work to the retained diversity set. FantLab's 18 September 2022 linguistic analysis reports **495,539 characters** and **69,126 words**, so it clears the >=300,000-character calibration threshold.

Russian Wikisource publishes a stable reviewed full-work transcription, explicitly marks the literary work public domain and cites `az.lib.ru` as its source. The source-free manifest now pins permanent revision **`oldid=5014458`** as page ID **1022517**, timestamp **`2023-08-30T20:13:01Z`**, MediaWiki SHA-1 **`605afeabc38e4f5948371afdf976f586edbf1955`**, **502,280 wikitext characters / 934,455 UTF-8 bytes**, and wikitext SHA-256 **`fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`**. No source prose is committed.

This is intentionally a **revision-wikitext identity**, not a frozen literary body. No deterministic literary-body extraction contract or raw/`scriptorium-text-v1` normalized literary digest exists yet. Freezing the MediaWiki revision also does not establish which print edition the `az.lib.ru` transcription represents and does not identify FantLab's analyzer input.

Revision-family evidence remains fail-closed. The Wikisource text states that the novel was written in 1926–1927 and revised with new chapters in 1937. FantLab separately records that Tolstoy reworked the novel four times, notes a new ending published in 1927, and identifies the 1939 `Советский писатель` edition as the last lifetime edition. Scriptorium therefore does **not** infer that the Wikisource/az.lib transcription matches a particular 1927, 1937 or 1939 print edition.

A stronger **bibliographic lead** is recorded, but deliberately not promoted to source identity. Two sibling A. N. Tolstoy pages in the Russian Wikisource/az.lib source ecosystem — *Союз пяти* and *Случай на Бассейной улице* — identify their text source as **A. N. Tolstoy, Collected Works in ten volumes, vol. 4, *Emigrants. Hyperboloid of Engineer Garin*, Moscow: Goslitizdat, 1958**. Independent FantLab bibliographic commentary identifies the same 1958 volume as a real Hyperboloid edition context. This makes the Moscow volume a concrete edition family to test, not proof: the Hyperboloid Wikisource page itself still cites only `az.lib.ru`, and no direct evidence says that its exact transcription was made from that volume.

The textological classification is narrower still. FantLab-hosted Yu. A. Krestinsky commentary distinguishes four book editions — **1927, 1934, 1936, and 1939** — identifies the 1939 `Советский писатель` text as the fourth book edition, and states under the Moscow Goslitizdat 1958 collected-works volume-4 heading that its Hyperboloid text is printed from the **1939 edition with checking against preceding editions**. Scriptorium therefore classifies the Moscow 1958 lead as a **1939-fourth-edition-derived editorial/textual-family witness**, still with no source-identity or parity weight.

Same-year bibliography prevents shortcut matching. Russian State Library record `01006486636` catalogs a distinct **Kyiv: Goslitizdat Ukrainy, 1958, 393-page _Hyperboloid of Engineer Garin; Aelita_ edition**. Consequently `1958` alone is not an edition identifier and cannot be used to equate the Wikisource/az.lib transcription, the Moscow collected-works volume, that Kyiv edition, or FantLab's undisclosed analyzer input.

Accordingly `source_identity_status=revision_wikitext_frozen_body_unfrozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and the M2 reproduction gate remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.json` — FantLab counts, legal/source boundary, revision-family ambiguity, the Moscow-1958 textual-family classification and independent same-year disambiguation.
- `source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.revision.json` — exact source-free MediaWiki revision-wikitext identity.
- `../../scriptorium/single_page_revision.py` — generic fail-closed exact-revision capture/replay implementation.

## Shining World traced 1920s romantic-fantastic candidate

`grin-shining-world-ru` adds Alexander Grin and a different 1920s prose tradition to the retained diversity set. FantLab's 18 September 2022 linguistic analysis reports **306,240 characters** and **43,678 words**, so the novel clears the >=300,000-character calibration threshold, though only narrowly.

Russian Wikisource exposes a reviewed work index whose stable version was checked on 4 May 2024. The index cites **A. S. Grin, Collected Works in six volumes, Moscow: Pravda, 1965, volume 3, pp. 66–214 (`lib.web`)** and links **34 chapter subpages** arranged as 16 + 11 + 7 chapters across three parts; sampled chapter pages repeat the same bibliographic source. The index exposes permanent revision **`oldid=4186047`**, but that locator freezes only the navigation/index page, not the 34 literary chapter revisions. No source prose is committed.

The legal boundary is explicit rather than inferred from mere web access. Wikisource identifies Grin as 1880–1932, lists *Shining World* as a 1923 lifetime publication, and its author rights notice says works published during his lifetime are approximately in the public domain in the country of origin while warning that translations and later revisions may carry independent rights. Scriptorium retains only the original Russian literary work body as the candidate scope and excludes later editorial apparatus unless separately justified. Wikisource page content is also exposed under CC BY-SA subject to its terms.

Russian Virtual Library independently identifies *Shining World* as a 1921–1923 Grin text and exposes the same three-part / 34-chapter structure. That is a useful bibliographic/text-family cross-check, not byte identity. Scriptorium therefore does **not** equate RVB, the 1965-source Wikisource transcription, any alternate Grin transcription, or FantLab's undisclosed analyzer input merely from title, chronology, structure, or count proximity.

Accordingly `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and the M2 reproduction gate remains **0/5 source-matched works**. A later freeze unit must pin every chapter revision plus deterministic extraction/composition and raw/normalized composite digests before diagnostics are allowed.

Canonical evidence:

- `source-edition-traces/grin-shining-world-ru.json` — FantLab counts, 1965-source Wikisource transcription family, legal/source boundary, immutable index locator, independent RVB cross-check, diversity rationale, and exact evidence required before diagnostic promotion.

## Road to Nowhere traced Grin candidate

`grin-road-nowhere-ru` adds a second long Alexander Grin work and creates a future same-author comparison pair without weakening the source gate. FantLab's 18 September 2022 linguistic analysis reports **438,439 characters** and **61,299 words**, comfortably above the >=300,000-character calibration threshold.

The primary Russian Wikisource work index cites **A. S. Grin, Collected Works, volume 6, Moscow: Pravda, 1965, pp. 3–227 (`lib.web`)** and exposes permanent index revision **`oldid=4715367`**. FantLab's independent bibliography for the 1965 six-volume collected works lists *Road to Nowhere* on exactly **pp. 3–227**, which strongly corroborates the bibliographic transcription family. It still does not prove that the electronic literary bytes exactly reproduce that printing, and it says nothing about FantLab's undisclosed analyzer upload.

A second Wikisource route makes that distinction concrete rather than theoretical. `Дорога в никуда (Грин)` is a separate single-page `az.lib.ru`-derived transcription at permanent revision **`oldid=5585836`**; its source-free manifest freezes page ID **1003775**, revision timestamp **`2025-07-30T20:33:01Z`**, MediaWiki SHA-1 **`135933c3b9155bddb0356d0eb9644d11f55ba870`** and wikitext SHA-256 **`f47b9b05d06dc2f5c6e2642d0822e6db68128386e4f1374b9188206a69fef11b`** without storing source prose. That freezes the alternate revision wikitext only; deterministic literary-body extraction/body digests remain unfrozen.

The alternate route labels the 1930 original Russian work public domain in Russia under Article 1281 and shows a two-part, 24-chapter structure. It is **not** collapsed with the source-cited 1965 family merely because both represent the same novel. The 1965-source index still does not freeze the linked literary-page revisions, deterministic extraction/composition, or raw/normalized composite digests.

Accordingly the primary family remains trace-only while the alternate route has `revision_wikitext_identity_frozen=true`; `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and the M2 reproduction gate remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/grin-road-nowhere-ru.json` — FantLab counts, source-cited 1965 Wikisource family, independent bibliography match, alternate az.lib transcription/legal evidence and fail-closed identity boundary.
- `source-edition-traces/grin-road-nowhere-ru.alternate-revision.json` — source-free exact revision-wikitext identity for the alternate route.

## Running on Waves traced Grin candidate

`grin-running-on-waves-ru` adds a third long Alexander Grin work and strengthens future same-author voice-profile coverage without treating repeated-author availability as source parity. FantLab's 18 September 2022 linguistic analysis reports **360,987 characters** and **52,985 words**, clearing the >=300,000-character calibration threshold.

Russian Wikisource identifies the original work as **1928**, explicitly marks it public domain, and cites **A. Grin, _Scarlet Sails. Running on Waves. The Golden Chain_, Moscow: Detskaya literatura, 1965 (Biblioteka priklyucheniy)**. The work index exposes **35 numbered chapters plus an epilogue** and permanent revision **`oldid=2595407`**. FantLab's independent edition record `12637` catalogs the same publisher/year/volume and places *Running on Waves* on **pp. 77–276**. This independently corroborates the bibliographic transcription family, not electronic bytes or FantLab's analyzer input.

The identity boundary remains fail-closed. The work-index permanent revision freezes navigation and bibliography only: the 35 chapter pages and epilogue have not been revision-pinned, no deterministic extraction/composition contract is recorded, and there are no raw or `scriptorium-text-v1` normalized composite digests. No source prose is committed. Translations, derivative works and later editorial apparatus remain separate rights and text identities.

Accordingly `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and the M2 reproduction gate remains **0/5 source-matched works**. A later freeze must pin all 36 literary subpages and define fail-closed extraction/composition before diagnostics can be enabled.

Canonical evidence:

- `source-edition-traces/grin-running-on-waves-ru.json` — FantLab counts, source-cited 1965 Wikisource family, work-index permanent locator, independent FantLab bibliography cross-check, public-domain boundary, and next evidence required before diagnostic promotion.

## The White Guard traced mixed-source candidate

`bulgakov-white-guard-ru` adds Mikhail Bulgakov and another long 1920s prose tradition while making an unusually important provenance caveat visible. FantLab's 18 September 2022 linguistic analysis reports **487,807 characters** and **70,307 words**, comfortably above the >=300,000-character calibration threshold.

Russian Wikisource explicitly marks the original Russian literary work public domain and exposes permanent work-index revision **`oldid=4715350`**. The index links 20 chapters across three parts, but it also explicitly declares that the current transcription is **mixed-source**: chapters **1–11** cite *M. Bulgakov. Days of the Turbins (The White Guard), Paris: Concorde, 1927*, while chapters **12–20** cite *Bulgakov M. A. The White Guard. The Life of Monsieur de Molière. Stories, Moscow: Pravda, 1989*. Scriptorium therefore does not represent this Wikisource work as one edition identity.

The permanent work-index revision freezes the navigation/index declaration only. None of the 20 literary chapter pages is revision-pinned by this unit, no chapter-to-source partition manifest is bound to exact page identities, no deterministic extraction/composition contract exists, and no raw or `scriptorium-text-v1` normalized composite digest is recorded. No source prose is committed.

A separate 1927 *Days of the Turbins (The White Guard)* DJVU is retained only as a facsimile lead for the first source family. Its current rendered file surface reports 189 pages and 8.01 MB and names `torrents` as the source. That is not enough to identify the mixed Wikisource chapter bytes, establish a reliable full-work single-edition witness, or connect the scan to FantLab's undisclosed analyzer input.

Accordingly `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and the M2 reproduction gate remains **0/5 source-matched works**. A later freeze must preserve the explicit 1–11 / 12–20 source partition while pinning all chapter revisions and computing deterministic source-free identities; any legally usable single-edition full-work witness must remain a distinct text identity rather than silently replacing this mixed transcription.

Canonical evidence:

- `source-edition-traces/bulgakov-white-guard-ru.json` — FantLab counts, permanent Wikisource index locator, explicit two-source chapter partition, legal boundary, separate 1927 facsimile lead, fail-closed identity status, and next evidence required before diagnostics.

## The Twelve Chairs traced coauthored multi-edition candidate

`ilf-petrov-twelve-chairs-ru` adds Ilf and Petrov, a long coauthored early-Soviet satire, and a concrete edition-family split relevant to both future source matching and author-voice modeling. FantLab's 17 September 2022 linguistic analysis reports **572,654 characters** and **80,203 words**, comfortably above the >=300,000-character calibration threshold.

Russian Wikisource exposes two public routes that Scriptorium keeps distinct. The current family cites **I. Ilf, E. Petrov, Collected Works, Moscow: GIKhL, 1961, vol. 1, pp. 25–382** and says that publication reproduces the 1938 Soviet Writer four-volume text checked against earlier publications; permanent revision **`oldid=5706136`** exposes **40 chapters**. A separate route identifies the **Zemlya i Fabrika 1928 first standalone edition**, permanent revision **`oldid=5706135`**, and exposes **41 chapters**. The 40-versus-41 structural difference is enough to require separate edition/transcription identities, but it is not treated as a byte-level diff, proof of every textual change, or evidence that either route was FantLab's analyzer input.

The retained Wikisource surfaces explicitly mark the original Russian work public domain. A 1928 facsimile is also available through the Wikisource/Commons file surface, currently shown as **424 pages / 74.37 MB** with its source field pointing to the Russian National Electronic Library. Scriptorium has not frozen that binary, so it remains a facsimile lead rather than a content identity. No literary prose or scan bytes are committed.

FantLab itself warns on this work's author-recognition surface that the text has two authors and their mixed styles prevent exact recognition results. Scriptorium records that as a future **VOICE-model requirement**: the work must not silently become an individual Ilf or Petrov author profile.

Accordingly `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and the M2 reproduction gate remains **0/5 source-matched works**. A later freeze must choose one text family, pin exact literary-page identities, define deterministic fail-closed extraction/composition, and record raw plus `scriptorium-text-v1` normalized composite digests. If the 1928 scan is used, its exact byte snapshot and OCR/page-extraction provenance must also be frozen before source-bound diagnostics.

Canonical evidence:

- [`ilf-petrov-twelve-chairs-ru.md`](ilf-petrov-twelve-chairs-ru.md) — public source-free candidate note.
- `source-edition-traces/ilf-petrov-twelve-chairs-ru.json` — FantLab counts, dual edition-family trace, public-domain/legal boundary, facsimile lead, coauthorship caveat and fail-closed admissibility.
