# SCRIP-CORPUS-010 — trace Alexander Grin's Running on Waves

Issue: #89  
PR: #90  
Mode: corpus / provenance

## Decision

Add Alexander Grin's *Бегущая по волнам* (*Running on Waves*) as a legally usable >=300,000-character trace-only diversity candidate while keeping literary-source identity and FantLab parity fail-closed.

FantLab work `27344` has a linguistic analysis dated 18 September 2022 with **360,987 characters** and **52,985 words**, clearing the repository calibration threshold.

Russian Wikisource identifies the original Russian work as created in 1928, explicitly marks it public domain in Russia under Article 1281 and in life-plus-70-or-less jurisdictions, and cites **A. Grin, _Scarlet Sails. Running on Waves. The Golden Chain_, Moscow: Detskaya literatura, 1965 (Biblioteka priklyucheniy)**. Its work index exposes permanent revision `oldid=2595407` and links 35 numbered chapters plus an epilogue.

FantLab edition `12637` independently catalogs the same Detskaya literatura 1965 volume and places *Running on Waves* on pp. 77–276. This corroborates a bibliographic transcription family but does not establish exact electronic bytes, equivalence to the printed volume, or FantLab analyzer-input identity.

The retained rights scope is the original Russian literary work body only. No source prose is committed. Translations, derivative works and later editorial apparatus remain distinct rights/text identities.

## Identity boundary

The work-index permanent revision freezes navigation and bibliography only. The 35 chapter revisions and epilogue revision are not pinned, and this unit does not define deterministic extraction/composition or record raw / `scriptorium-text-v1` normalized composite digests.

Bibliographic agreement between Wikisource and FantLab's edition catalog does not establish that the Wikisource literary bytes exactly reproduce the 1965 printing and does not establish FantLab analyzer-input identity.

## Gate effect

- `source_identity_status=traced_not_frozen`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `gate_ready=false`;
- `m2_parity_admissible=false`;
- M2 remains **0/5 source-matched works**.

Public corpus navigation and the machine-readable parity catalog now expose this third long Grin candidate and its exact evidence boundary. The dedicated trace records the next admissible steps: pin all 36 literary subpages, define fail-closed extraction/composition, compute source-free composite digests, and seek independent evidence for FantLab's actual analyzer input.

This authoring run leaves PR #90 for a later independent exact-head review rather than self-merging it.

## Independent review and merge

A later run independently reviewed exact head `a6c779aa208bc01d8581de151b75f618d5cc87ab` against unchanged base `19e32ee1a6d27c290cd52e085b790ae24719d019`. The branch was 6 commits ahead / 0 behind and changed exactly the intended five files: the parity catalog, public corpus README, the dedicated Running-on-Waves source-edition trace, this changelog fragment, and durable state. No prior submitted reviews or inline review threads were present.

Fresh source checks reconfirmed FantLab's 18 September 2022 analysis at 360,987 characters / 52,985 words; the Russian Wikisource work page's 1928 date, Detskaya literatura 1965 source citation, 35 numbered chapters plus epilogue, public-domain notice and permanent locator `oldid=2595407`; and FantLab edition `12637` listing the same 1965 volume with *Running on Waves* on pp. 77–276. These findings support only the recorded bibliographic transcription-family trace and do not establish electronic-byte identity or FantLab analyzer-input identity.

Exact-head workflows were independently inspected at job level. Scriptorium Pages run `35071053751` completed successfully with the standard-library suite, canonical site build, deterministic rebuild and artifact upload; PR deployment was skipped as designed. Pinned-provider run `35071053786` completed successfully with the provider-contract suite, exact hash-pinned `pylem==0.0.18` install/native smoke and frozen-Anna source-free sidecar diagnostics.

No blocking defect was found. PR #90 was squash-merged as `2df3e90328e487a57798e0a13e485a580585b0c9`; Issue #89 closed completed. The merge does not advance M2: the 36 literary subpages remain unfrozen, FantLab analyzer-input identity remains undisclosed, diagnostics/gate remain disabled, and the reproduction gate stays at **0/5 source-matched works**.
