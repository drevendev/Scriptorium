# Running on Waves — route-frozen corpus candidate

`grin-running-on-waves-ru` is a source-free provenance candidate for Alexander Grin's 1928 novel *Running on Waves* (`Бегущая по волнам`). FantLab's 18 September 2022 linguistic analysis reports **360,987 characters** and **52,985 words**, so the work clears Scriptorium's >=300,000-character calibration threshold.

## Retained public route

Russian Wikisource identifies the retained transcription family with **A. Grin, _Алые паруса. Бегущая по волнам. Золотая цепь_, Moscow: Detskaya literatura, 1965 (Biblioteka priklyucheniy)**. The work-index permanent revision is `oldid=2595407`.

A second immutable witness now freezes the **route topology** without storing prose: category permanent revision `oldid=4715419` lists exactly 37 pages — the main work page plus `/1` through `/35` and `/Эпилог`. The committed route manifest records those 36 literary titles exactly.

This is **not** a literary-page revision freeze. The 36 subpages' own revision IDs, timestamps and MediaWiki SHA-1 values are not yet pinned; no deterministic literary-body extraction/composition contract or composite digest is claimed.

## Distinct route boundary

Russian Wikisource also exposes `/Версия 2`, observed at permanent revision `oldid=5655654`. That page declares `az.lib.ru` and identifies **A. S. Grin, Collected Works, Pravda, Moscow, 1980**. Scriptorium treats it as a **distinct transcription/edition route** and does not splice it into the retained 1965-source family.

## FantLab boundary

FantLab edition record `12637` independently corroborates the same 1965 Detskaya literatura volume and places *Running on Waves* on pp. 77–276. This is useful bibliographic-family evidence, not proof that Wikisource reproduces those print bytes exactly and not evidence that FantLab analyzed this public transcription.

Therefore:

- `source_identity_status=route_inventory_frozen_subpage_revisions_unfrozen`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**.

## Canonical source-free evidence

- `source-edition-traces/grin-running-on-waves-ru.json` — structured provenance and admissibility boundary.
- `source-edition-traces/grin-running-on-waves-ru.route-inventory.json` — exact 36-title route witness and excluded 1980 route.
- `../../scriptorium/running_waves_inventory.py` — deterministic fail-closed route-manifest builder/validator.

No literary source text is committed by this candidate surface.
