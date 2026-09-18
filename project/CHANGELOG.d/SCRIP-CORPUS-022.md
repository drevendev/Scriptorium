# SCRIP-CORPUS-022 — Running on Waves route-inventory witness

- Issue: #131
- Draft PR: #132
- Scope: corpus/provenance strengthening for `grin-running-on-waves-ru`; no literary-page revision freeze, literary-body freeze, FantLab source-match claim or M2 promotion.

## Finding

Russian Wikisource's permanent category revision `oldid=4715419` lists exactly **37 pages** in the `Бегущая по волнам (Грин)` category: the main work page plus the expected **35 numbered literary subpages and `/Эпилог`**. This supplies an immutable, source-free witness that all 36 expected routes existed in that captured category topology.

A separate Wikisource page, `/Версия 2`, is not part of that retained 1965-source route. Its current permanent locator observed during this unit is `oldid=5655654`; the page declares `az.lib.ru` and identifies `А.С. Грин. Собрание сочинений: Правда; Москва; 1980`. That is a distinct transcription/edition route and must not be silently composed with the 1965 Detskaya literatura family.

## Implementation

`scriptorium/running_waves_inventory.py` defines the exact `/1` through `/35` plus `/Эпилог` title contract, emits the deterministic source-free route manifest, validates the permanent category witness and excluded-route boundary, and fails closed if a future artifact drifts or overclaims literary-page revision/body freeze.

The committed `corpus/candidates/source-edition-traces/grin-running-on-waves-ru.route-inventory.json` records only route/provenance identity. Unit coverage verifies exact ordering/count, source-free scope, the distinct 1980 route boundary, and deterministic equality between the builder and committed artifact.

## Evidence boundary

The category witness freezes **route topology, not literary-page contents**. Exact revision IDs/timestamps/MediaWiki SHA-1 values for the 36 literary pages, deterministic extraction/composition and composite hashes remain unfrozen. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains **0/5**.
