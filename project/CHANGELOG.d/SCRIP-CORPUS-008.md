# SCRIP-CORPUS-008 — trace Alexander Grin's Shining World

Issue: #85  
PR: #86  
Mode: corpus / provenance

## Decision

Add Alexander Grin's *Блистающий мир* (*Shining World*) as a legally usable >=300,000-character diversity candidate while keeping source identity and FantLab parity fail-closed.

FantLab work `27340` has a linguistic analysis dated 18 September 2022 with **306,240 characters** and **43,678 words**, so the novel clears the repository's calibration threshold by 6,240 characters.

Russian Wikisource exposes a reviewed work index that cites **A. S. Grin, Collected Works in six volumes, Moscow: Pravda, 1965, volume 3, pp. 66–214 (`lib.web`)**. The index exposes permanent revision `oldid=4186047` and a three-part structure of **16 + 11 + 7 = 34 chapter subpages**; sampled chapter pages repeat the same bibliographic source. Russian Virtual Library independently identifies the work as Grin's 1921–1923 novel and exposes the same three-part / 34-chapter structure. RVB is retained only as bibliographic/text-family corroboration, not byte identity.

The legal boundary is explicit. Wikisource records Grin as 1880–1932, lists *Shining World* as a 1923 lifetime publication, and its author rights notice says works published during his lifetime are approximately public domain in the source country while warning that translations and later revisions may have independent rights. The retained scope is the original Russian literary body only; no source prose or later editorial apparatus is committed. Wikisource page content is additionally exposed under CC BY-SA subject to its terms.

## Identity boundary

The permanent work-index revision is an immutable locator, not a frozen full-work identity. The literary prose is distributed across 34 chapter pages, so a later freeze must pin every admitted chapter revision plus timestamps and MediaWiki SHA-1 identities, define deterministic fail-closed extraction/composition, and record raw plus `scriptorium-text-v1` normalized composite digests.

No identity is inferred between the 1965-source Wikisource transcription, RVB, any alternate Grin transcription, or FantLab's undisclosed analyzer upload merely from title, chronology, chapter structure or character-count proximity.

## Gate effect

- `source_identity_status=traced_not_frozen`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `gate_ready=false`;
- `m2_parity_admissible=false`;
- M2 remains **0/5 source-matched works**.

Public corpus navigation now exposes the candidate and its exact evidence boundary. The machine-readable trace records the next admissible evidence steps without publishing book text. This authoring run leaves PR #86 for a later independent exact-head review rather than self-merging it.
