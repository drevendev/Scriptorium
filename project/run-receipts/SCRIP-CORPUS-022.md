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

## Evidence boundary / next trigger

This unit freezes route topology only. It does not freeze the 36 literary pages' own revision IDs/timestamps/MediaWiki SHA-1 values, define literary extraction/composition, create a composite digest, or identify FantLab's analyzer input. M2 remains **0/5**.

Next wake: independently review the final exact head of #132, inspect all required checks and the public provenance wording, repair any blocking defect if necessary, and merge only when evidence supports it.
