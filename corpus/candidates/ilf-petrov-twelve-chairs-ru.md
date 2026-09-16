# The Twelve Chairs — corpus candidate

**Candidate ID:** `ilf-petrov-twelve-chairs-ru`  
**Authors:** Ilya Ilf and Evgeny Petrov  
**Language:** Russian  
**Current status:** `traced_not_frozen` / not M2-admissible

This candidate is retained because FantLab's 17 September 2022 linguistic analysis reports **572,654 characters** and **80,203 words**, comfortably above Scriptorium's 300,000-character corpus threshold. FantLab does not disclose the edition or immutable bytes uploaded for that analysis, so the numbers are a public reference surface rather than source-match evidence.

## Why edition identity matters here

Russian Wikisource exposes at least two materially distinct public text families that must not be collapsed under the work title:

- the current work family cites *Collected Works*, Moscow: GIKhL, 1961, vol. 1, pp. 25–382, and says that publication reproduces the 1938 Soviet Writer four-volume text checked against earlier publications; its visible structure has **40 chapters** and the work-index revision is pinned as `oldid=5706136`;
- a separate page identifies the **first standalone Zemlya i Fabrika 1928 edition** and exposes **41 chapters**; its work-index revision is pinned as `oldid=5706135`.

The 40-versus-41 chapter difference is enough to require distinct edition/transcription identities in Scriptorium. It is **not** treated as a byte-level diff, proof of every textual change, or evidence that either route was FantLab's analyzer input.

A 1928 facsimile is also available through the Wikisource/Commons file surface (currently shown as 424 pages / 74.37 MB, with its source field pointing to the Russian National Electronic Library). Scriptorium has not frozen the scan bytes, so the file page remains a facsimile lead rather than a binary identity.

## Legal and publication boundary

The retained Wikisource surfaces mark the original Russian work public domain. Scriptorium stores only provenance, metadata and derived evidence here; no literary source text or scan bytes are committed.

## Coauthorship caveat

FantLab itself warns on the work's author-recognition surface that the text has two authors and that their mixed styles prevent exact recognition results. Scriptorium records that as a future **VOICE-model requirement**: this coauthored work must not silently become an individual Ilf or Petrov author profile. No author-profile result is claimed by this candidate record.

## What is still required

Before source-bound diagnostics, one chosen public text family needs exact literary-page identities, deterministic fail-closed extraction/composition, and raw plus `scriptorium-text-v1` normalized composite digests. If the 1928 scan is used, Scriptorium also needs an exact binary snapshot hash and a documented OCR/page-extraction route. M2 can advance only if independent evidence also establishes which edition/transcription FantLab analyzed.

Machine-readable provenance: [`source-edition-traces/ilf-petrov-twelve-chairs-ru.json`](source-edition-traces/ilf-petrov-twelve-chairs-ru.json).
