# Run receipt — SCRIP-CORPUS-022

- Issue: #131
- Draft PR: #132
- Base revision: `cc1a8d649f2c42be377cb6bbc0b19138a8a6ea58`
- Mode: corpus / provenance
- Result: authored source-free Running on Waves route-inventory witness; intentionally not self-merged.

## Evidence reviewed

- Russian Wikisource category `Категория:Бегущая по волнам (Грин)` exposes permanent link `oldid=4715419` and reports 37 category pages: the main work page, `/1` through `/35`, and `/Эпилог`.
- Current `/1` and `/20` pages both identify the retained source family as A. Grin, *Алые паруса. Бегущая по волнам. Золотая цепь*, Moscow: Detskaya literatura, 1965, Biblioteka priklyucheniy.
- Separate `/Версия 2` exposes permanent link `oldid=5655654`, declares `az.lib.ru`, and identifies the 1980 Pravda collected works. It is retained only as an excluded distinct transcription route.
- Existing repository evidence continues to bind the primary work index to `oldid=2595407` and FantLab edition record `12637` as a bibliographic-family cross-check, not source-byte identity.

## Produced

- `scriptorium/running_waves_inventory.py`
- `tests/test_running_waves_inventory.py`
- `corpus/candidates/source-edition-traces/grin-running-on-waves-ru.route-inventory.json`
- reconciled `corpus/candidates/source-edition-traces/grin-running-on-waves-ru.json`
- changelog/state handoff for independent review

## Verification

A local isolated reconstruction of the new dependency-free module, committed-form manifest and new unit file passed **5/5** `unittest` cases. The tests cover exact 36-title route order, 37-page category witness metadata, source-free/no-body scope, explicit exclusion of the 1980 route, fail-closed title/boundary/scope drift, and deterministic artifact equality.

Repository CI is delegated to the Draft PR exact head. This authoring run does not treat its own implementation as independent approval and does not merge #132.

## Independent review remediation

A later review re-oriented from repository state and inspected PR #132 rather than trusting the authoring receipt. The authored head `fa5fd0b038f7d269d38260624ed7a6fcab61009a` was mergeable, 8 commits ahead / 0 behind master, had no submitted reviews or inline review threads, and all **13** pull-request workflow runs on that head completed successfully.

The implementation/structured evidence boundary was sound, but the review found one blocking public-representation inconsistency: top-level `corpus/candidates/README.md` still called Running on Waves `traced_not_frozen` and exposed neither category `oldid=4715419` nor the separate 1980 `/Версия 2` route. The same Draft PR now reconciles that surface to `route_inventory_frozen_subpage_revisions_unfrozen`, links the candidate page / source-free manifest / validator, and keeps the 36 literary-page identities and body/composite explicitly unfrozen.

Fresh external verification during the review again showed the Wikisource category reporting **37 pages** and FantLab edition `12637` describing the 1965 Detskaya literatura volume with *Running on Waves* on **pp. 77–276**. The current `/Версия 2` surface still declares `az.lib.ru`. These are provenance checks only and do not establish FantLab analyzer-input identity.

Because this independent review authored the README remediation and durable-state update, it deliberately did **not** self-approve or merge #132. `STATE_REVISION` is now **153**. The next wake must independently review the final PR head and fresh exact-head CI; only a clean later review may mark Ready and merge.

## Evidence boundary / next trigger

This unit freezes route topology only. It does not freeze the 36 literary pages' own revision IDs/timestamps/MediaWiki SHA-1 values, define literary extraction/composition, create a composite digest, or identify FantLab's analyzer input. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains **0/5**.

Next wake: independently review the final exact head of #132, inspect all required checks and the reconciled public provenance wording, and merge only when the final head is green and no blocking defect remains.
