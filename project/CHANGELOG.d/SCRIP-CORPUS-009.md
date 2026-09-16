# SCRIP-CORPUS-009 — trace Alexander Grin's Road to Nowhere

Issue: #87  
PR: #88  
Mode: corpus / provenance

## Decision

Add Alexander Grin's *Дорога никуда* (*Road to Nowhere*) as a legally usable >=300,000-character diversity candidate while keeping literary-source identity and FantLab parity fail-closed.

FantLab work `27346` has a linguistic analysis dated 18 September 2022 with **438,439 characters** and **61,299 words**, comfortably clearing the repository's calibration threshold.

The primary Russian Wikisource work index cites **A. S. Grin, Collected Works, volume 6, Moscow: Pravda, 1965, pp. 3–227 (`lib.web`)** and exposes permanent index revision `oldid=4715367`. FantLab's independent bibliography for the 1965 six-volume collected works lists *Road to Nowhere* on the same pp. 3–227. That agreement strengthens the bibliographic transcription-family trace but is not byte identity for the electronic text and is not evidence about FantLab's uploaded analyzer input.

A distinct Wikisource route, *Дорога в никуда*, exposes an `az.lib.ru`-derived single-page transcription at permanent revision `oldid=5585836`, records the work as a 1930 publication, and explicitly marks the original Russian work public domain in Russia under Article 1281 and in life-plus-70-or-less jurisdictions. Its visible structure is two parts with 7 + 17 = 24 chapters. Scriptorium records this page as alternate-transcription and legal evidence only; it is deliberately not collapsed with the source-cited 1965 family merely because both represent the same novel.

The retained rights scope is the original Russian literary work body only. No source prose is committed. Translations, later creative revisions and editorial apparatus require separate provenance/rights review.

## Identity boundary

The primary work-index revision is an immutable locator, not a frozen full-work literary identity. The linked literary-page revisions are not pinned, and this unit does not define deterministic extraction/composition or record raw / `scriptorium-text-v1` normalized composite digests.

Bibliographic agreement between Wikisource and FantLab's edition catalog does not establish that the Wikisource literary bytes exactly reproduce the 1965 printing, does not establish equivalence to the alternate az.lib transcription, and does not establish FantLab analyzer-input identity.

## Gate effect

- `source_identity_status=traced_not_frozen`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `gate_ready=false`;
- `m2_parity_admissible=false`;
- M2 remains **0/5 source-matched works**.

Public corpus navigation and the machine-readable parity catalog now expose this second long Grin candidate and its exact evidence boundary. The dedicated trace records the next admissible steps: pin the primary literary-page inventory, define fail-closed extraction/composition, compute source-free composite digests, and seek independent evidence for FantLab's actual analyzer input.

This authoring run leaves PR #88 for a later independent exact-head review rather than self-merging it.
