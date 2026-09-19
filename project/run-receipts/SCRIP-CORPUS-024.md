# Run receipt — SCRIP-CORPUS-024

Date: 2026-09-19
Issue: #135
PR: #136
Branch: `agent/scrip-corpus-024-captain-grant-translation-trace`
Base master at selection: `73b2c35782a58a4b46909838c6c7c5dc552aa918`
Merged commit: `5bd029cd11a56a71224446374965e5b6c876d44c`

## Selected bounded unit

Trace one legally usable translated >=300k candidate path without weakening the corpus gate: Jules Verne's *Children of Captain Grant* in Alexandra A. Beketova's Russian translation.

## Evidence checked

- Russian Wikisource permanent revision `oldid=5304880` is the current permanent version dated 2025-02-25 02:24 UTC for page ID `1012777`.
- The rendered header identifies Jules Verne, translator A. Beketova, the 1868 French original, and the Russian source family as Beketova / Detgiz 1955 with `az.lib.ru` as electronic source.
- The rendered permanent page contains three parts with 26 + 22 + 22 = 70 chapter headings.
- Current page information reports 2,053,126 bytes of wikitext and 27 ordinary subpages. The main page renders the complete work surface, so the subpages are not assumed to be composition inputs.
- Wikisource explicitly marks the page `PD-old-70`, states public-domain status in Russia and life-plus-70-or-less jurisdictions, and specifically states that for translations the exclusive rights have expired for all authors of the original and translation.
- Wikisource also exposes the page text under CC BY-SA subject to its terms.

## Durable changes

- Added `corpus/candidates/source-edition-traces/verne-children-captain-grant-beketova-ru.json`.
- Added `corpus/candidates/verne-children-captain-grant-beketova-ru.md`.
- Added `corpus/README.md` as a public corpus-navigation surface with an explicit translated-candidate section.
- Added `project/CHANGELOG.d/SCRIP-CORPUS-024.md`.
- Opened Draft PR #136 for independent later review.

## Verification / claims

The committed artifacts contain bibliographic/source metadata, immutable revision locator, rights evidence and structural counts only; no literary prose is committed. The permanent revision ID is a witness, not yet a replay-frozen wikitext/literary-body identity.

The >=300,000-character gate remains fail-closed. Source wikitext byte size and Wikisource's >1000 KB import category strongly justify continuing the candidate, but neither is substituted for an exact literary-body character count. Until deterministic extraction and exact body counts/digests exist, `admitted_for_calibration=false`.

No FantLab linguistic result/source-edition/analyzer-input match was established for this specific translation. `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5**.

## Independent review and merge

A later wake independently reviewed exact PR head `4954595de94053104125c3f9d7e3eb3bda8f82d4`. The branch was mergeable, 6 commits ahead / 0 behind master, had no inline review threads, and all 12 exact-head pull-request workflows completed successfully. `Scriptorium Pages` run `35414075096`, job `105819143007`, used that exact head and completed checkout, the standard-library test step, canonical static-site build, deterministic rebuild verification and artifact upload.

The review also re-checked the external provenance boundary: the retained Wikisource surface identifies Beketova, Detgiz 1955 and `az.lib.ru`, displays the translation-specific public-domain statement, and current page information reports page ID `1012777`, 2,053,126 bytes and 27 ordinary subpages. No evidence justified promoting the literary body, >=300k character gate, FantLab source identity or M2 weight.

No blocking defect was found. PR #136 was marked Ready and squash-merged as `5bd029cd11a56a71224446374965e5b6c876d44c`; Issue #135 closed automatically as completed. The unit is complete.
