# The Twelve Chairs — corpus candidate

**Candidate ID:** `ilf-petrov-twelve-chairs-ru`  
**Authors:** Ilya Ilf and Evgeny Petrov  
**Language:** Russian  
**Current status:** 1928 route graph frozen / literary body unfrozen / not M2-admissible

This candidate is retained because FantLab's 17 September 2022 linguistic analysis reports **572,654 characters** and **80,203 words**, comfortably above Scriptorium's 300,000-character corpus threshold. FantLab does not disclose the edition or immutable bytes uploaded for that analysis, so the numbers are a public reference surface rather than source-match evidence.

## Why edition identity matters here

Russian Wikisource exposes at least two materially distinct public text families that must not be collapsed under the work title:

- the current work family cites *Collected Works*, Moscow: GIKhL, 1961, vol. 1, pp. 25–382, and says that publication reproduces the 1938 Soviet Writer four-volume text checked against earlier publications; its visible structure has **40 chapters** and the work-index revision is pinned as `oldid=5706136`;
- a separate page identifies the **first standalone Zemlya i Fabrika 1928 edition** and exposes **41 chapters**; its work-index revision is pinned as `oldid=5706135`.

The 40-versus-41 chapter difference is enough to require distinct edition/transcription identities in Scriptorium. It is **not** treated as a byte-level diff, proof of every textual change, or evidence that either route was FantLab's analyzer input.

A 1928 facsimile is also available through the Wikisource/Commons file surface (currently shown as 424 pages / 74.37 MB, with its source field pointing to the Russian National Electronic Library). Scriptorium has not frozen the scan bytes, so the file page remains a facsimile lead rather than a binary identity.

## 1928 source graph freeze

The first-edition route is now more precisely bounded without committing literary prose. The ProofreadPage index is pinned at `oldid=5702510` and identifies the same 1928 *Zemlya i Fabrika* family. Three exact part-parent revisions transclude the same ProofreadPage index:

- Part 1: `oldid=5702507`, scan-page range **8–149** (**142** referenced Page-namespace pages);
- Part 2: `oldid=5704332`, scan-page range **152–313** (**162** pages);
- Part 3: `oldid=5702508`, scan-page range **316–421** (**106** pages).

Together these routes reference **410 Page-namespace dependencies**. Scan-index gaps **150–151** and **314–315** are deliberately recorded as unclassified and non-transcluded; Scriptorium does not silently assume that they are either literary text or disposable separators.

This is a **route/source-graph freeze, not a literary-body freeze**. The exact revisions of the 410 referenced Page-namespace pages are not yet pinned, the PDF bytes are not frozen, and no extraction/composition profile, body count or body digest is claimed. The source-free graph manifest is [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json).

## Legal and publication boundary

The retained Wikisource surfaces mark the original Russian work public domain. Scriptorium stores only provenance, metadata and derived evidence here; no literary source text or scan bytes are committed.

## Coauthorship caveat

FantLab itself warns on the work's author-recognition surface that the text has two authors and that their mixed styles prevent exact recognition results. Scriptorium records that as a future **VOICE-model requirement**: this coauthored work must not silently become an individual Ilf or Petrov author profile. No author-profile result is claimed by this candidate record.

## What is still required

The next source-identity unit must capture exact source-free revision identities for all **410** Page-namespace dependencies referenced by the frozen 1928 routes. Only after that can Scriptorium define and verify a fail-closed literary-body extraction/composition contract and raw plus `scriptorium-text-v1` normalized composite digests. The two explicit scan-index gaps must be inspected independently rather than inferred into or out of the body. If the 1928 facsimile is used as a binary witness, Scriptorium also needs an exact byte snapshot hash and documented OCR/page-extraction provenance.

FantLab still does not disclose which edition or immutable byte stream it analyzed. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; the M2 reproduction gate remains **0/5 source-matched works**.

Machine-readable provenance: [`source-edition-traces/ilf-petrov-twelve-chairs-ru.json`](source-edition-traces/ilf-petrov-twelve-chairs-ru.json).
