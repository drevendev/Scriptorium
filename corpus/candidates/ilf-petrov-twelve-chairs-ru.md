# The Twelve Chairs — corpus candidate

**Candidate ID:** `ilf-petrov-twelve-chairs-ru`  
**Authors:** Ilya Ilf and Evgeny Petrov  
**Language:** Russian  
**Current status:** 1928 route graph + 410 exact Page revision identities frozen / literary body unfrozen / not M2-admissible

This candidate is retained because FantLab's 17 September 2022 linguistic analysis reports **572,654 characters** and **80,203 words**, comfortably above Scriptorium's 300,000-character corpus threshold. FantLab does not disclose the edition or immutable bytes uploaded for that analysis, so the numbers are a public reference surface rather than source-match evidence.

## Why edition identity matters here

Russian Wikisource exposes at least two materially distinct public text families that must not be collapsed under the work title:

- the current work family cites *Collected Works*, Moscow: GIKhL, 1961, vol. 1, pp. 25–382, and says that publication reproduces the 1938 Soviet Writer four-volume text checked against earlier publications; its visible structure has **40 chapters** and the work-index revision is pinned as `oldid=5706136`;
- a separate page identifies the **first standalone Zemlya i Fabrika 1928 edition** and exposes **41 chapters**; its work-index revision is pinned as `oldid=5706135`.

The 40-versus-41 chapter difference is enough to require distinct edition/transcription identities in Scriptorium. It is **not** treated as a byte-level diff, proof of every textual change, or evidence that either route was FantLab's analyzer input.

A 1928 facsimile is also available through the Wikisource/Commons file surface (currently shown as 424 pages / 74.37 MB, with its source field pointing to the Russian National Electronic Library). Scriptorium has not frozen the scan bytes, so the file page remains a facsimile lead rather than a binary identity.

## 1928 route and Page-identity freeze

The first-edition route is bounded without committing literary prose. The ProofreadPage index is pinned at `oldid=5702510` and identifies the same 1928 *Zemlya i Fabrika* family. Three exact part-parent revisions transclude the same ProofreadPage index:

- Part 1: `oldid=5702507`, scan-page range **8–149** (**142** referenced Page-namespace pages);
- Part 2: `oldid=5704332`, scan-page range **152–313** (**162** pages);
- Part 3: `oldid=5702508`, scan-page range **316–421** (**106** pages).

Together these routes reference **410 Page-namespace dependencies**. Scriptorium now also freezes the exact source-free identity of every one of those dependencies: Page sequence, revision ID, revision timestamp and MediaWiki SHA-1. The deterministic identity set is stored as three source-free shards behind [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json). The initial hosted capture is recorded as workflow run `35503562530`, artifact `10603441105`, artifact ZIP SHA-256 `431558255b168e99f26ac7f5567bda7bb30d69288120b34f918ad3d0e50062c9`, with capture JSON SHA-256 `e5182724d8188fca48807c58720d17f1e40e55b121d1b172fa414e317859420c`.

Scan-index gaps **150–151** and **314–315** remain deliberately outside the 410 dependency set and unclassified. Scriptorium does not silently assume that they are either literary text or disposable separators.

This is still **not a literary-body freeze**. Exact Page revisions are pinned, but no Page-markup rendering/extraction contract, body composition, body character count, raw/normalized digest, or PDF byte identity is claimed. The source-free graph manifest is [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json).

## Legal and publication boundary

The retained Wikisource surfaces mark the original Russian work public domain. Scriptorium stores only provenance, metadata and derived evidence here; no literary source text, Page wikitext, OCR, rendered prose or scan bytes are committed.

## Coauthorship caveat

FantLab itself warns on the work's author-recognition surface that the text has two authors and that their mixed styles prevent exact recognition results. Scriptorium records that as a future **VOICE-model requirement**: this coauthored work must not silently become an individual Ilf or Petrov author profile. No author-profile result is claimed by this candidate record.

## What is still required

A later unit may inspect the two explicit two-page gaps independently, then define and verify a candidate-specific fail-closed literary-body extraction/composition contract over the **410 pinned Page revisions**. Only after that can Scriptorium record raw plus `scriptorium-text-v1` normalized composite counts/digests and determine whether its own frozen body satisfies the >=300k corpus rule. If the 1928 facsimile is used as a binary witness, Scriptorium also needs an exact byte snapshot hash and documented OCR/page-extraction provenance.

FantLab still does not disclose which edition or immutable byte stream it analyzed. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; the M2 reproduction gate remains **0/5 source-matched works**.

Machine-readable provenance: [`source-edition-traces/ilf-petrov-twelve-chairs-ru.json`](source-edition-traces/ilf-petrov-twelve-chairs-ru.json).
