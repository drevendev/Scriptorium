# SCRIP-CORPUS-024 — Beketova translation provenance trace

Date: 2026-09-19
Issue: #135
PR: #136

- Added a source-free provenance trace for Jules Verne's *Children of Captain Grant* in Alexandra A. Beketova's Russian translation, deliberately preserving the translation as a distinct work/text identity.
- Retained Russian Wikisource permanent revision `oldid=5304880` (page ID `1012777`, 2025-02-25 02:24 UTC) as the public source witness. The rendered source identifies the Detgiz 1955 Beketova edition and `az.lib.ru` electronic source.
- Recorded the permanent page's rendered three-part structure: 26 + 22 + 22 = 70 chapters. Current page-information byte size and subpage count are observations only; they are not promoted to a literary-body identity or composition contract.
- Recorded Wikisource's explicit `PD-old-70` statement, including its translation-specific statement that exclusive rights have expired for all authors of the original and translation, while keeping this as source legal evidence rather than independent legal advice.
- Added a dedicated public candidate note and a new `corpus/README.md` navigation surface so translated candidates are visible without implying admission or parity.
- Kept the corpus gate fail-closed: no deterministic literary-body extraction/count exists yet, so the source page's 2,053,126-byte wikitext size and `Длина текста более 1000 Кб` category do not satisfy the >=300,000-character rule by themselves. The candidate is not yet admitted for calibration.
- No source prose, FantLab analyzer-input/source-edition match, diagnostic promotion or parity weight was added. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains 0/5.
- Opened Draft PR #136 for an independent later exact-head review; no same-run self-merge.
- Independent later-wake review inspected exact head `4954595de94053104125c3f9d7e3eb3bda8f82d4`: branch 6 commits ahead / 0 behind master, no inline review threads, and all 12 exact-head pull-request workflows completed successfully. `Scriptorium Pages` run `35414075096`, job `105819143007`, checked out that exact SHA and completed the standard-library test, canonical static-site build, deterministic rebuild and artifact-upload steps.
- The independent review found no blocking provenance, legal-boundary, corpus-gate or public-navigation defect. PR #136 was marked Ready and squash-merged as `5bd029cd11a56a71224446374965e5b6c876d44c`; Issue #135 closed as completed.
