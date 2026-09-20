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

**SCRIP-CORPUS-034** freezes the revision identity of every one of those 418 included Page dependencies without committing Page prose. Hosted capture requested only MediaWiki `ids|timestamp|sha1`; it returned exactly 418 distinct included sequences, excluded 114 and 411, and contained no wikitext/OCR/source-text field.

The capture is committed as four digest-pinned source-free shards plus one index:

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json) — topology contract, capture provenance, shard digests and gate boundary;
- `.page-revisions.01.json` through `.page-revisions.04.json` — compact tuples of **Page sequence, exact revision ID, revision timestamp and MediaWiki SHA-1** only.

Hosted replay re-queries the exact revision IDs and fails closed if title, timestamp or MediaWiki SHA-1 differs. No literary prose, Page-namespace payload, DjVu/PDF bytes, OCR or screenshots are committed.

## Literary-body composition contract

**SCRIP-CORPUS-035 / PR #158** freezes `scriptorium-darwin-literary-body-contract-v1`, a source-free composition contract bound to the frozen 418-Page identity inventory.

The contract selects only rendered numbered routes **`/1` through `/14`** as the literary input surface. That is **388 exact Page dependencies**, kept in frozen route/Page-sequence order. It intentionally excludes **30 frozen apparatus dependencies**:

- parent-only Page sequences **8–21** and **423–427** (19 dependencies total);
- alphabetical-index route **`/Указатель`**, Page sequences **412–422** (11 dependencies).

Source-declared no-text positions **114** and **411** remain explicit non-dependencies and therefore never enter either the 388 literary set or the 30 frozen-apparatus set.

The boundary is evidence-based rather than inferred from nominal page count. The frozen source graph already labels `/1` as introduction + chapter 1, `/2`–`/14` as chapter routes, and `/Указатель` as the alphabetical index. Fresh public-source inspection also shows Page 419 carrying alphabetical-index entries and Pages 425–426 carrying publisher-advertising/back-matter material. This supports excluding the index and parent-only framing surfaces from the literary composition without copying their prose into repository artifacts.

The implementation fails closed if the 418-Page identity inventory, identity-row shape, topology partition or generated contract drifts. It may later permit **transient exact-revision MediaWiki main-slot fetches only after identity verification**, but it does not serialize Page wikitext or rendered prose.

This is deliberately a composition/input freeze, **not yet a literary-body identity freeze**. The Page-wikitext-to-prose rendering profile and composite separator semantics remain unfrozen, so no body count or body digest is claimed by this unit.

## Source-free rendering-surface inventory

**SCRIP-CORPUS-036 / merged PR #160** freezes the bounded prerequisite needed before a renderer can be specified without guessing at MediaWiki/template behavior. The hosted audit replays the exact **388 already-frozen literary Page revisions**, verifies each title/revision/timestamp/MediaWiki SHA-1 identity before inspecting content, and reduces the transient wikitext to a source-free construct inventory.

The durable freeze contains **38 template name/arity shapes** and **18 HTML/ProofreadPage tag name/kind shapes**. Aggregate observations include **1,069 comments**, **776 `<noinclude>` blocks**, **8 wikilinks**, no external links, no headings, no table opens/closes, and no triple-brace template-parameter constructs on this exact literary surface. The inventory records construct identities/counts and cryptographic digests only; template arguments, lexical snippets, Page wikitext and rendered prose are not committed.

The full hosted audit covered all **388/388** literary dependencies with `identity_replay_match=true`. Its per-Page source-free receipt list is represented durably by SHA-256 `7c170f513bf21f2c9e0d7736bc9fc20b4c9a40fdfe942a7b1dd1b0ac048ba09b`; the compact deterministic freeze has SHA-256 `e5ae625fef6afb2e890de990e1ef3b9e108a409a2e0ea2136947c2c3e1cea44d`.

Independent exact-head review re-read all settled CI on `ee97e29af7225131002b6e0922c731536d903d13`, independently downloaded the exact-head artifact, recomputed its audit/receipt/freeze digests, and found no blocker before squash merge `1d9a7795724a68747ea1bb6e1fe1e7ea8b590519`.

This **does not freeze the renderer**. It freezes only the set of markup constructs the future candidate-specific renderer must handle or explicitly reject. `rendering_profile_frozen=false` remains mandatory until a separate implementation proves deterministic semantics for this exact inventory.

## Provider-reported scan-file metadata

The retained source surface reports **27,368,263 bytes**, MIME `image/vnd.djvu`, dimensions **3744 × 5616**, **432 pages**, SHA-1 `75ef508588194ae74874272ce290f3ec1043ea9b`, current file-history display `11:45, 8 March 2016` by `Nonexyst`, and Archive.org locator `https://archive.org/details/oproiskhozhdenii00darw`.

That is deliberately only **provider-reported remote metadata**. Scriptorium has not independently frozen the DjVu byte stream or computed a local SHA-256 over it.

## Rights evidence

The retained Wikisource work surface explicitly states that the work is in the public domain in Russia and jurisdictions with a life-plus-70-or-shorter term; its translation-specific notice says exclusive rights have expired for all authors of the original and translation. This page records that source declaration as provenance evidence, not independent legal advice. Wikisource site text licensing remains separate from the public-domain status asserted for the work/translation.

## Corpus boundary

This candidate is still **not admitted** to the >=300,000-character calibration/profile corpus. The source family, route graph, 418-dependency topology, exact 418 Page revision identities, the 388/30 literary-versus-apparatus composition boundary, and the exact 388-Page source-free markup-surface inventory are now frozen, but the actual literary prose has not yet been deterministically rendered or counted.

Still required before corpus admission:

- define and verify a candidate-specific fail-closed Page-wikitext-to-prose rendering profile that covers the frozen construct inventory;
- freeze the rendered literary-body character count including spaces plus raw/normalized digests;
- verify that the frozen body itself, not nominal page count, topology or construct counts, clears **300,000 characters**.

Accordingly `admitted_for_calibration=false` remains mandatory.

## FantLab boundary

FantLab work **`work969964`** identifies Darwin's 1859 English monograph. The currently exposed Russian translation there is **K. Timiryazev**, not Rachinsky's 1864 translation. No `/lp` result attributable to this exact Rachinsky source edition has been established. Keep `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.

## Canonical evidence

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json) — retained translation/source identity and gate boundary from the earlier provenance stages.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json) — exact route/topology evidence and apparatus roles.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json) — authoritative source-free index for all 418 exact Page revision identities and four committed shards.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-surface.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-surface.json) — deterministic source-free 388-Page construct inventory with no source payload.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-surface.source-graph.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-surface.source-graph.json) — provenance edges from frozen Page identities through literary composition and hosted markup audit to the durable inventory.
- [`../../scriptorium/darwin_body_contract.py`](../../scriptorium/darwin_body_contract.py) — deterministic source-free 388/30 composition contract generator and fail-closed validator.
- [`../../scriptorium/darwin_render_surface.py`](../../scriptorium/darwin_render_surface.py) — exact-revision identity-verifying hosted construct audit.
- [`../../scriptorium/darwin_render_surface_freeze.py`](../../scriptorium/darwin_render_surface_freeze.py) — deterministic compact freeze reducer/validator.

## Next evidence

A later bounded unit should use the now-frozen template/tag surface to define and verify a candidate-specific fail-closed rendering profile for the 388 literary dependencies without persisting source prose. Only then should a separate identity/admission unit compute source-free counts/digests and independently prove the >=300,000-character threshold. FantLab parity remains a separate, stricter source-matching problem.
