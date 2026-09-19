# Run receipt — SCRIP-CORPUS-033

Date: 2026-09-19
Issue: #153
Pull request: #154 (`scrip-corpus-033-darwin-transclusion-topology`)
Mode: normal-flow P2 corpus/provenance strengthening

## Selected bounded unit

Strengthen the retained Darwin/Rachinsky 1864 candidate by freezing the exact source-free ProofreadPage transclusion topology beneath the already retained rendered family, resolving the two explicit no-text omissions that matter to composition, while keeping the complete Page revision set, scan bytes and literary body fail-closed.

## Evidence captured

Fresh official Russian Wikisource evidence establishes:

- shared route template `Шаблон:О происхождении видов (Дарвин; Рачинский)/1864`, permanent revision **`oldid=3775868`**;
- exact route Page-sequence expressions `/1` 22–56, `/2` 57–69, `/3` 70–85, `/4` 86–131 with `exclude=114`, `/5` 132–161, `/6` 162–190, `/7` 191–219, `/8` 220–245, `/9` 246–269, `/10` 270–297, `/11` 298–326, `/12` 327–348, `/13` 349–384, `/14` 385–410, `/Указатель` 412–422;
- current parent topology witness **`oldid=5712882`** with exact parent include expression `8-21,423-427`;
- **399** route dependencies plus **19** parent dependencies = **418 distinct referenced Page-sequence numbers**;
- Page sequence **114**, exact revision **`oldid=3364724`**, source-declared `Эта страница не требует вычитки` and hidden category `Без текста`; this is the page explicitly excluded by route `/4`;
- Page sequence **411**, exact revision **`oldid=3364733`**, carries the same source-declared no-text classification and is the sole omitted sequence between `/14` and `/Указатель`.

The route/display spans 362–387 ↔ 385–410 and 389–399 ↔ 412–422 have equal cardinality. The single one-page gap therefore uniquely aligns displayed print page **388** with Page sequence **411**; because exact Page revision `oldid=3364733` is source-declared no-text, the repository can resolve the prior p.388 unknown without OCR or scan-image interpretation.

## Durable result

- Updated `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json` with exact template/parent topology witnesses, route ranges, dependency counts and exact no-text Page evidence.
- Updated `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json` to synchronize the stronger topology and freeze boundary.
- Updated `corpus/candidates/darwin-origin-species-rachinsky-1864-ru.md` so public repository visitors can inspect the topology and p.388 resolution without seeing source prose.
- Added this run receipt and semantic changelog fragment; canonical state is advanced in the same Draft PR for later stateless recovery.

## Freeze boundary

Frozen at this stage:

- prior parent/index/rendered-route anchors and provider-reported scan metadata;
- current parent topology witness `oldid=5712882` and `include="8-21,423-427"`;
- shared route-template revision `oldid=3775868` and exact Page-sequence ranges/exclusion;
- topology counts: 399 route dependencies, 19 parent dependencies, 418 distinct referenced Page-sequence numbers;
- exact source-free no-text identities/classifications for Page sequences 114 (`oldid=3364724`) and 411 (`oldid=3364733`);
- displayed print page 388 as the uniquely aligned Page-411 source-declared no-text gap.

Still unfrozen:

- exact revision IDs/timestamps/MediaWiki SHA-1 identities for the 418 included Page dependencies;
- a full print-page ↔ Page-sequence map outside the uniquely resolved p.388 gap;
- independently retrieved DjVu bytes and Scriptorium-computed binary SHA-256;
- Page-markup extraction semantics and literary-body composition for included source pages;
- literary-body character count/raw-normalized digests and >=300k admission;
- FantLab analyzer-input/source-edition identity.

## Corpus and gate status

The stronger transclusion topology is provenance, not the literary-body threshold proof. Therefore:

- `admitted_for_calibration=false`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**

## Handoff

Draft PR #154 must be reviewed on its exact final head by a later run. The review should independently re-check the official template revision/ranges, parent include topology, Page-114/Page-411 no-text classifications, inspect changed files for source-prose/binary leakage or boundary promotion, and require exact-head CI before any Ready/merge decision.