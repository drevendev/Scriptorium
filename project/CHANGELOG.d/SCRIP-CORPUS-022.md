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

## Review remediation

The later independent review found one acceptance blocker before merge: the top-level public `corpus/candidates/README.md` still described this candidate as `traced_not_frozen` and did not expose the frozen route witness or the excluded `/Версия 2` boundary. The PR branch now reconciles that navigation surface with the structured trace and candidate page: it names category `oldid=4715419`, states the exact 36-title route topology, records `/Версия 2` / `oldid=5655654` as a separate 1980/az.lib route, and uses `route_inventory_frozen_subpage_revisions_unfrozen` without implying a literary-body freeze.

The authoring head `fa5fd0b038f7d269d38260624ed7a6fcab61009a` had all 13 pull-request workflow runs green. Because the review remediation changes the PR head, merge remains blocked until fresh exact-head checks complete and a later run independently reviews that final head.

## Evidence boundary

The category witness freezes **route topology, not literary-page contents**. Exact revision IDs/timestamps/MediaWiki SHA-1 values for the 36 literary pages, deterministic extraction/composition and composite hashes remain unfrozen. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains **0/5**.
