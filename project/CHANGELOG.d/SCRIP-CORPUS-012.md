# SCRIP-CORPUS-012 — trace The White Guard as an explicit mixed-source candidate

Issue: #93  
PR: #94  
Mode: corpus / provenance

## Decision

Add Mikhail Bulgakov's *Белая гвардия* (*The White Guard*) as a legally usable >=300k FantLab candidate while preserving the public transcription's **explicit mixed-source identity** instead of flattening the work title into one edition.

FantLab work `7692` has a linguistic analysis dated 18 September 2022 with **487,807 characters** and **70,307 words**, comfortably above the 300,000-character calibration threshold. FantLab does not disclose the edition or immutable bytes supplied to its analyzer, so no source match is inferred.

Russian Wikisource exposes permanent work-index revision `oldid=4715350`, a 20-chapter structure across three parts, and an explicit public-domain notice for the original Russian literary work. No source prose is committed.

## Mixed-source boundary

The Wikisource work index explicitly declares two different bibliographic source families:

- chapters **1–11**: *М. Булгаков. Дни Турбиных (Белая гвардия). Париж: Concorde, 1927*;
- chapters **12–20**: *Булгаков М. А. Белая гвардия. Жизнь господина де Мольера. Рассказы. М.: Правда, 1989*.

Therefore the current Wikisource work is not represented as a single-edition transcription. The work-index oldid freezes the index and that declaration, not the 20 chapter bodies. Exact chapter revisions, a chapter-to-source partition manifest, deterministic extraction/composition, and raw/normalized composite digests remain unfrozen.

A 1927 *Дни Турбиных (Белая гвардия)* DJVU is retained only as a separate facsimile lead for the first source family. Its current rendered file surface reports 189 pages and 8.01 MB and names `torrents` as the source. Scriptorium does not treat that retrieval provenance as sufficient for edition-controlled text identity, does not claim the scan equals the Wikisource chapter bytes, and does not connect it to FantLab input.

## Gate effect

- `source_identity_status=traced_not_frozen`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `gate_ready=false`;
- `m2_parity_admissible=false`;
- M2 remains **0/5 source-matched works**.

The next admissible source-free step is to revision-pin all 20 literary chapter pages while preserving the 1–11 / 12–20 source partition, then define deterministic fail-closed extraction/composition and record raw plus `scriptorium-text-v1` normalized composite digests. A legally usable single-edition full-work witness, if found later, must remain a distinct candidate identity rather than silently replacing the current mixed transcription.

## Independent review and merge

A later autonomous wake reviewed exact head `44038b07c01cf8b624f94fdf87effa9a7403a19e` against unchanged base `820241fde3fbe7c77b05ebd77ad113e70ae78463`: 6 commits ahead / 0 behind, exactly five expected changed files, and no inline review threads. Fresh source retrieval reconfirmed FantLab work 7692 (18 September 2022; 487,807 characters; 70,307 words), the Wikisource permanent locator `oldid=4715350`, the three-part / 20-chapter structure, explicit public-domain notice, and the split source declaration for chapters 1–11 versus 12–20. The separate 1927 DJVU remained correctly scoped as a weak-provenance facsimile lead only.

Exact-head CI was green: Pages run `35105320373` passed the standard-library suite, canonical site build, deterministic rebuild and artifact upload; pinned-provider run `35105320403` passed provider-contract verification, exact hash-pinned `pylem==0.0.18` install/native smoke and frozen-Anna source-free sidecar diagnostics.

No blocking defect was found. PR #94 was squash-merged as `59564e12aff59cb1d8c53493ad790962c6458d71`, and Issue #93 closed completed. Gate status is unchanged: chapter identities/composite digests remain unfrozen, FantLab analyzer-input identity remains unknown, diagnostics/M2 admission stay disabled, and M2 remains **0/5**.
