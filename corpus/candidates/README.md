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

This unit deliberately stops at **source-edition tracing**. Scriptorium has not yet frozen the PDF byte digest, selected literary pages, or a deterministic OCR/extraction contract, and FantLab does not disclose which Petersburg edition or byte stream it analyzed. The 1916 first book edition is also kept distinct from Bely's materially revised 1922 edition. Therefore `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and the M2 reproduction gate remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/bely-petersburg-1916-ru.json` — FantLab counts, explicit 1916 facsimile identity, public-domain evidence, Wikisource provenance warning, edition-family boundary and next evidence required before diagnostics.

## Hyperboloid of Engineer Garin traced early-Soviet SF candidate

`tolstoy-hyperboloid-garin-wikisource-ru` adds a new author and an early Soviet science-fiction/adventure work to the retained diversity set. FantLab's 18 September 2022 linguistic analysis reports **495,539 characters** and **69,126 words**, so it clears the >=300,000-character calibration threshold.

Russian Wikisource publishes a stable reviewed full-work transcription, explicitly marks the literary work public domain, cites `az.lib.ru` as its source, and exposes permanent revision **`oldid=5014458`** from 30 August 2023. That is a useful immutable locator but not yet a Scriptorium-frozen literary-text identity: this unit does not record the MediaWiki revision SHA-1/wikitext digest, define a deterministic body extractor, or compute raw/normalized text digests. No source prose is committed.

Revision identity is deliberately fail-closed. The Wikisource text states that the novel was written in 1926–1927 and revised with new chapters in 1937. FantLab separately records that Tolstoy reworked the novel four times, notes a new ending published in 1927, and identifies the 1939 `Советский писатель` edition as the last lifetime edition. Scriptorium therefore does **not** infer that the Wikisource/az.lib transcription matches a particular 1927, 1937 or 1939 print edition, and it does not infer that FantLab analyzed the same text.

A stronger **bibliographic lead** is now recorded, but deliberately not promoted to source identity. Two sibling A. N. Tolstoy pages in the Russian Wikisource/az.lib source ecosystem — *Союз пяти* and *Случай на Бассейной улице* — identify their text source as **A. N. Tolstoy, Collected Works in ten volumes, vol. 4, *Emigrants. Hyperboloid of Engineer Garin*, Moscow: Goslitizdat, 1958**. Independent FantLab bibliographic commentary identifies the same 1958 volume as a real Hyperboloid edition context. This makes the 1958 volume a concrete edition family to test, not proof: the Hyperboloid Wikisource page itself still cites only `az.lib.ru`, and no direct evidence yet says that its exact transcription was made from that volume. Sibling import metadata and edition availability cannot establish textual identity.

Accordingly `bibliographic_source_identity` remains unset, `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and the M2 reproduction gate remains **0/5 source-matched works**.

Canonical evidence:

- `source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.json` — FantLab counts, permanent Wikisource revision, public-domain evidence, revision-family ambiguity, collateral 1958-volume bibliographic leads with explicit identity weight, and the evidence required before any diagnostic promotion.
