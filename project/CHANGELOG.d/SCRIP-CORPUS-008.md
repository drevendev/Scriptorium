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

## Independent review and merge

A later run independently reviewed exact PR head `35061e829d5b279aa45a29f32ff255516c45961a` against unchanged base `c7da33834dd6df8017bc59d86b39b0d07ea480ab`. GitHub compare reported **7 commits ahead / 0 behind**, and the PR changed exactly the five expected corpus/provenance/public-navigation/state files. No blocking review defect or pre-existing review thread was present.

Fresh evidence checks reconfirmed FantLab work `27340` at 306,240 characters / 43,678 words on 18 September 2022; the reviewed Wikisource work-index source citation, permanent locator `oldid=4186047`, and 16+11+7 chapter structure; sampled chapter pages carrying the same Pravda 1965 volume-3 source citation; and RVB as a 1921–1923 / three-part text-family cross-check only. A statutory cross-check also confirmed the Russian general life-plus-70 term and the transition rule that the newer term applies only where the former 50-year term had not expired by 1 January 1993, consistent with the retained public-domain treatment for Grin's 1923 lifetime work while preserving the repository's translation/later-revision caveat.

Exact-head workflow runs `35053939844` (Scriptorium Pages) and `35053939843` (Scriptorium pinned pylem provider) both completed successfully. Pages passed the standard-library suite, canonical static-site build, deterministic rebuild and artifact upload; live deployment was skipped on the pull-request event. The provider workflow passed its contract suite, exact hash-pinned `pylem==0.0.18` native smoke and frozen-Anna source-free diagnostic replay.

PR #86 was squash-merged as `84f4f4cea73a53d8ff01fe45000e6655e9f4cb5a`; Issue #85 closed `completed`. The source identity boundary is unchanged: the index locator does not freeze the 34 literary chapter revisions, extraction/composition contract or composite digests, FantLab input identity remains unknown, and **M2 remains 0/5 source-matched works**.
