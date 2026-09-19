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
- Added this run receipt and semantic changelog fragment; canonical state was advanced in the authored PR for stateless recovery.

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

## Independent review and completion

Independent review was performed on exact authored head **`241bc6ce0ce0ae1715bd44c8b06f40bd1f1d3806`** against unchanged base `f61586ec9ab03f9ccc1668c66a416b8895392cf6`.

Fresh source checks independently verified the route-template ranges/exclusion, parent `include="8-21,423-427"`, and Page 114 / Page 411 no-text permanent revisions. The ProofreadPage index source provided an additional direct mapping witness: `22=1`, `114="—"`, `115="схема"`, `116=93`, with no later label reset before 423. Consequently Page sequence 411 carries displayed print label 388, independently supporting the source-declared no-text p.388 classification rather than relying on continuity alone.

All six changed paths were reviewed and contain only provenance/control metadata; no literary prose payload, Page-namespace source payload, OCR, DjVu/PDF bytes, or screenshots were introduced. The complete 418 referenced Page revision set, independently retrieved scan bytes/SHA-256, literary-body extraction/composition, body count/digests, >=300k admission, FantLab source match and M2 status remain explicitly closed.

All **13** pull-request-triggered workflows completed successfully on the exact reviewed head. `Scriptorium Pages` run **`35465902112`**, job **`105958057742`**, checked out the exact head and completed the standard-library test suite, canonical Pages build, deterministic rebuild and artifact upload. Artifact **`10590908696`** has digest **`sha256:e038fb9f7bbcdc84e0ee4d7b3699d58987b97e2a38a03245e08790c42f40e45d`**.

No blocking finding remained. PR #154 was marked Ready and squash-merged as **`6ec86ee09a0c4c8a2d80d3cfafeabbe1cc302d08`**; Issue #153 closed as completed. The next stateless wake should resume normal-flow P2 corpus/provenance work from canonical state.