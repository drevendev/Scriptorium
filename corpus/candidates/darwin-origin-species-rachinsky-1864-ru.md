# On the Origin of Species — Rachinsky 1864 Russian translation

This candidate records **Sergey A. Rachinsky's 1864 Russian translation** of Charles Darwin's *On the Origin of Species* as its own translation/source identity. It must not be collapsed with Darwin's English original, K. A. Timiryazev's Russian translation, other Russian translations, or rendered orthography transformations without an explicit transform/identity contract.

## Public-source witness

Russian Wikisource identifies the edition as **Ч. Дарвин. О происхождении видов**, translated by **Сергей Александрович Рачинский**, Saint Petersburg: **Издание книгопродавца А. И. Глазунова**, **1864**, **399 pages**.

Retained source-free anchors are:

- rendered edition-family page `О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)`, permanent revision **`oldid=5628021`**;
- ProofreadPage index `Индекс:Дарвин - О происхождении видов, 1864.djvu`, permanent revision **`oldid=4494408`**;
- shared route template, permanent revision **`oldid=3775868`**;
- parent topology witness, permanent revision **`oldid=5712882`** with `include="8-21,423-427"`.

The ProofreadPage index reports **`Закончено — Все страницы вычитаны и проверены`**. This is provenance/quality evidence for the transcription family; it is not by itself a literary-body freeze.

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

This is deliberately a composition/input freeze, **not yet a literary-body identity freeze**. The candidate-specific rendering decision profile is now frozen separately below, but unresolved provider/template/reference/math semantics and composite separator semantics still prevent a rendered literary-body identity.

## Source-free rendering-surface inventory

**SCRIP-CORPUS-036 / merged PR #160** freezes the bounded prerequisite needed before a renderer can be specified without guessing at MediaWiki/template behavior. The hosted audit replays the exact **388 already-frozen literary Page revisions**, verifies each title/revision/timestamp/MediaWiki SHA-1 identity before inspecting content, and reduces the transient wikitext to a source-free construct inventory.

The durable freeze contains **38 template name/arity shapes** and **18 HTML/ProofreadPage tag name/kind shapes**. Aggregate observations include **1,069 comments**, **776 `<noinclude>` blocks**, **8 wikilinks**, no external links, no headings, no table opens/closes, and no triple-brace template-parameter constructs on this exact literary surface. The inventory records construct identities/counts and cryptographic digests only; template arguments, lexical snippets, Page wikitext and rendered prose are not committed.

The full hosted audit covered all **388/388** literary dependencies with `identity_replay_match=true`. Its per-Page source-free receipt list is represented durably by SHA-256 `7c170f513bf21f2c9e0d7736bc9fc20b4c9a40fdfe942a7b1dd1b0ac048ba09b`; the compact deterministic freeze has SHA-256 `e5ae625fef6afb2e890de990e1ef3b9e108a409a2e0ea2136947c2c3e1cea44d`.

Independent exact-head review re-read all settled CI on `ee97e29af7225131002b6e0922c731536d903d13`, independently downloaded the exact-head artifact, recomputed its audit/receipt/freeze digests, and found no blocker before squash merge `1d9a7795724a68747ea1bb6e1fe1e7ea8b590519`.

## Fail-closed rendering decision profile

**SCRIP-CORPUS-045 / Draft PR #178** adds `scriptorium-darwin-page-render-profile-v1`, bound cryptographically to the reviewed exact-388 source-free surface freeze before any shape classification is accepted. The profile covers all **18 tag shapes / 5,164 tag tokens** and all **38 template shapes / 4,583 template invocations**. Its canonical profile SHA-256 is **`2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`**.

The decision table defines only conservative local markup handling: ordinary `big`, `div`, `small`, `sub` and `sup` wrappers preserve inner text; `<noinclude>` is excluded from transcluded content; ProofreadPage `pagequality` metadata is dropped. It intentionally leaves **5 tag shapes / 518 tokens** unresolved for provider semantics: `<math>` open/close, `<ref>` open/close and self-closing `<references/>`. All **38 template shapes / 4,583 invocations** remain unresolved rather than inferring expansion from names; `nop` is additionally marked as inter-page-sensitive.

This is a **frozen decision boundary, not a renderer**. `rendering_profile_frozen=true` coexists deliberately with `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `rendering_equivalence_claimed=false`, and `inter_page_composition_frozen=false`. Any changed count, new/missing shape, stale surface digest or wrong candidate identity fails closed. No Page wikitext, template argument values, rendered prose, OCR, DjVu/PDF bytes or literary text are committed.

## Independent scan binary identity

**SCRIP-CORPUS-037 / merged PR #162** independently retrieved the exact Wikimedia Commons DjVu backing this ProofreadPage family and streamed it through Scriptorium without writing the binary into the repository. The hosted capture observed **27,368,263 bytes** and SHA-1 `75ef508588194ae74874272ce290f3ec1043ea9b`, exactly matching the provider metadata that had already been frozen from the source surface.

The same transient byte stream produced Scriptorium-computed SHA-256 **`7f3ae1aadd4a844b193783a0c350e23815a76e7bb14a92bae7fa1c077354a2c8`**. This source-free identity is frozen in [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.scan-identity.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.scan-identity.json). The first hosted capture was run `35492937897`, job `106030871176`; its source-free artifact `10599691841` has ZIP SHA-256 `95cece9716e721b2fc2f98ecdc8bb10e4ba1ed2a27db514572d30cea186f1592`.

Independent exact-head review on `9d78a8a447b89d82e88f91c8c9d2d4d38d2ea167` found all **15/15** pull-request workflows successful. Dedicated run `35493249103`, job `106031676386`, replayed the exact original and reproduced the byte count/SHA-1/SHA-256. Review independently downloaded artifact `10600065977`, recomputed its ZIP SHA-256 as `54f11622eb549847118ed06555294dd97f84c9ba1d110a11ec9e7d9eb719a51d`, and confirmed it contains only the committed source-free receipt plus verification JSON. PR #162 was then squash-merged as `102c64a3e9c8149ac43c6d58ab044860fad511c2`.

The provider surface also reports MIME `image/vnd.djvu`, dimensions **3744 × 5616**, **432 pages**, current file-history display `11:45, 8 March 2016` by `Nonexyst`, and Archive.org locator `https://archive.org/details/oproiskhozhdenii00darw`. Those descriptive fields remain provider metadata; the byte count/SHA-1/SHA-256 identity above is the independently verified binary boundary. **No scan bytes are committed.**

This binary freeze does not define Page-wikitext rendering, does not prove the literary body is >=300,000 characters, and does not establish FantLab analyzer-input identity.

## Rights evidence

The retained Wikisource work surface explicitly states that the work is in the public domain in Russia and jurisdictions with a life-plus-70-or-shorter term; its translation-specific notice says exclusive rights have expired for all authors of the original and translation. This page records that source declaration as provenance evidence, not independent legal advice. Wikisource site text licensing remains separate from the public-domain status asserted for the work/translation.

## Corpus boundary

This candidate is still **not admitted** to the >=300,000-character calibration/profile corpus. The source family, route graph, 418-dependency topology, exact 418 Page revision identities, the 388/30 literary-versus-apparatus composition boundary, the exact 388-Page source-free markup-surface inventory, fail-closed render decision profile, and backing DjVu byte identity are now frozen, but the actual literary prose has not yet been deterministically rendered or counted.

Still required before corpus admission:

- independently resolve/freeze the provider/template/reference/math semantics explicitly left unresolved by the render profile and separately freeze inter-page composition/separator semantics;
- implement deterministic exact-revision rendering under those frozen semantics without persisting source prose;
- freeze the rendered literary-body character count including spaces plus raw/normalized digests;
- verify that the frozen body itself, not nominal page count, topology, construct counts or scan byte size, clears **300,000 characters**.

Accordingly `admitted_for_calibration=false` remains mandatory.

## FantLab boundary

FantLab work **`work969964`** identifies Darwin's 1859 English monograph. The currently exposed Russian translation there is **K. Timiryazev**, not Rachinsky's 1864 translation. No `/lp` result attributable to this exact Rachinsky source edition has been established. Keep `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.

## Canonical evidence

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json) — retained translation/source identity and gate boundary.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json) — exact route/topology evidence and apparatus roles.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.page-revisions.index.json) — authoritative source-free index for all 418 exact Page revision identities and four committed shards.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-surface.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-surface.json) — deterministic source-free 388-Page construct inventory with no source payload.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-surface.source-graph.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-surface.source-graph.json) — provenance edges from frozen Page identities through literary composition and hosted markup audit to the durable inventory and frozen decision profile.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.render-profile.json) — deterministic fail-closed source-free rendering decision profile with explicit unresolved semantics and closed downstream gates.
- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.scan-identity.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.scan-identity.json) — independently verified source-free DjVu byte count, SHA-1 cross-check and SHA-256; scan bytes are not stored.
- [`../../scriptorium/darwin_body_contract.py`](../../scriptorium/darwin_body_contract.py) — deterministic source-free 388/30 composition contract generator and fail-closed validator.
- [`../../scriptorium/darwin_render_surface.py`](../../scriptorium/darwin_render_surface.py) — exact-revision identity-verifying hosted construct audit.
- [`../../scriptorium/darwin_render_surface_freeze.py`](../../scriptorium/darwin_render_surface_freeze.py) — deterministic compact freeze reducer/validator.
- [`../../scriptorium/darwin_render_profile.py`](../../scriptorium/darwin_render_profile.py) — deterministic fail-closed source-free decision-profile builder/validator.
- [`../../scriptorium/darwin_scan_identity.py`](../../scriptorium/darwin_scan_identity.py) — streaming scan-identity capture/replay with provider cross-checks and no binary persistence.

## Next evidence

A later bounded unit should resolve and independently freeze the provider/template/reference/math semantics explicitly left unresolved by `scriptorium-darwin-page-render-profile-v1`; inter-page separator/composition semantics should remain a separately reviewable decision. Only after deterministic rendering exists should a separate identity/admission unit compute source-free counts/digests and independently prove the >=300,000-character threshold. FantLab parity remains a separate, stricter source-matching problem.
