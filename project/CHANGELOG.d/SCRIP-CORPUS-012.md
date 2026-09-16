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
