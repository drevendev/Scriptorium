# Running on Waves — frozen corpus candidate

`grin-running-on-waves-ru` is a source-free provenance candidate for Alexander Grin's 1928 novel *Running on Waves* (`Бегущая по волнам`). FantLab's 18 September 2022 linguistic analysis reports **360,987 characters** and **52,985 words**. Scriptorium's independently frozen public candidate contains **363,819 characters including spaces** and therefore clears the >=300,000-character calibration threshold.

## Retained public route

Russian Wikisource identifies the retained transcription family with **A. Grin, _Алые паруса. Бегущая по волнам. Золотая цепь_, Moscow: Detskaya literatura, 1965 (Biblioteka priklyucheniy)**. The work-index permanent revision is `oldid=2595407`.

A second immutable witness freezes the **route topology** without storing prose: category permanent revision `oldid=4715419` lists exactly 37 pages — the main work page plus `/1` through `/35` and `/Эпилог`. The committed route manifest records those 36 literary titles exactly.

The 36 literary subpages are **revision-frozen**. `grin-running-on-waves-ru.source-revisions.json` records, in route order `/1` through `/35` then `/Эпилог`, each page ID, exact revision ID, UTC revision timestamp and MediaWiki SHA-1. Candidate-specific CI captures the same source-free identities and replays every pinned revision without storing literary prose.

## Frozen literary body

`scriptorium-running-waves-wikisource-body-v1` defines a candidate-specific, fail-closed extraction contract over those exact 36 revisions. It resolves only the formatting/template shapes observed in the frozen source set, preserves visible literary content, strips only observed layout-only wrappers, and leaves unknown or unobserved shapes to fail closed. The bodies are composed in frozen route order with `\n\n` between pages under `scriptorium-wikisource-composite-v1`.

The resulting source-free composite identity is:

- **363,819 characters including spaces**;
- **656,239 UTF-8 bytes**;
- raw SHA-256 **`41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`**;
- `scriptorium-text-v1` normalized SHA-256 **`41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`**.

This identity clears Scriptorium's >=300k rule for **general calibration/profile use**. No literary source text is committed.

## Distinct route boundary

Russian Wikisource also exposes `/Версия 2`, observed at permanent revision `oldid=5655654`. That page declares `az.lib.ru` and identifies **A. S. Grin, Collected Works, Pravda, Moscow, 1980**. Scriptorium treats it as a **distinct transcription/edition route** and does not splice it into the retained 1965-source family.

## FantLab boundary

FantLab edition record `12637` independently corroborates the same 1965 Detskaya literatura volume and places *Running on Waves* on pp. 77–276. This is useful bibliographic-family evidence, not proof that Wikisource reproduces those print bytes exactly and not evidence that FantLab analyzed this public transcription.

The frozen public composite is **2,832 characters larger** than FantLab's displayed count (363,819 vs 360,987). That delta is diagnostic evidence only; it cannot establish or reject source identity by itself because FantLab does not disclose the uploaded analyzer bytes or complete counting/extraction rules.

Therefore:

- `source_identity_status=literary_body_frozen_public_candidate`
- `general_calibration_profile_admissible=true`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**.

## Canonical source-free evidence

- `source-edition-traces/grin-running-on-waves-ru.json` — structured provenance and admissibility boundary.
- `source-edition-traces/grin-running-on-waves-ru.route-inventory.json` — exact 36-title route witness and excluded 1980 route.
- `source-edition-traces/grin-running-on-waves-ru.source-revisions.json` — exact source-free identities for all 36 retained literary pages.
- `source-edition-traces/grin-running-on-waves-ru.literary-body.json` — exact per-page and composite literary-body counts/digests.
- `../../scriptorium/running_waves_inventory.py` — deterministic fail-closed route-manifest builder/validator.
- `../../scriptorium/running_waves_revisions.py` — deterministic source-free revision capture/validation/replay.
- `../../scriptorium/running_waves_body.py` — candidate-specific fail-closed literary-body extraction/composition/replay.

No literary source text is committed by this candidate surface.
