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
