# The Twelve Chairs — corpus candidate

**Candidate ID:** `ilf-petrov-twelve-chairs-ru`  
**Authors:** Ilya Ilf and Evgeny Petrov  
**Language:** Russian  
**Current status:** 1928 route graph + 410 exact Page revision identities + exact scan binary identity + source-free four-gap audit frozen / literary body unfrozen / not M2-admissible

This candidate is retained because FantLab's 17 September 2022 linguistic analysis reports **572,654 characters** and **80,203 words**, comfortably above Scriptorium's 300,000-character corpus threshold. FantLab does not disclose the edition or immutable bytes uploaded for that analysis, so the numbers are a public reference surface rather than source-match evidence.

## Why edition identity matters here

Russian Wikisource exposes at least two materially distinct public text families that must not be collapsed under the work title:

- the current work family cites *Collected Works*, Moscow: GIKhL, 1961, vol. 1, pp. 25–382, and says that publication reproduces the 1938 Soviet Writer four-volume text checked against earlier publications; its visible structure has **40 chapters** and the work-index revision is pinned as `oldid=5706136`;
- a separate page identifies the **first standalone Zemlya i Fabrika 1928 edition** and exposes **41 chapters**; its work-index revision is pinned as `oldid=5706135`.

The 40-versus-41 chapter difference is enough to require distinct edition/transcription identities in Scriptorium. It is **not** treated as a byte-level diff, proof of every textual change, or evidence that either route was FantLab's analyzer input.

The 1928 facsimile behind the retained Wikisource ProofreadPage family is frozen as an exact source-free binary identity. Hosted Scriptorium capture streamed the Wikimedia Commons original transiently and reproduced the provider's **77,978,350 bytes** and SHA-1 `4ab6aa42c3517169e99c1177b6fb6412cfe9187d`; Scriptorium independently computed SHA-256 `5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4`. The PDF itself is not committed. The canonical source-free receipt is [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.scan-identity.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.scan-identity.json).

## 1928 route and Page-identity freeze

The first-edition route is bounded without committing literary prose. The ProofreadPage index is pinned at `oldid=5702510` and identifies the same 1928 *Zemlya i Fabrika* family. Three exact part-parent revisions transclude the same ProofreadPage index:

- Part 1: `oldid=5702507`, scan-page range **8–149** (**142** referenced Page-namespace pages);
- Part 2: `oldid=5704332`, scan-page range **152–313** (**162** pages);
- Part 3: `oldid=5702508`, scan-page range **316–421** (**106** pages).

Together these routes reference **410 Page-namespace dependencies**. Scriptorium freezes the exact source-free identity of every one of those dependencies: Page sequence, revision ID, revision timestamp and MediaWiki SHA-1. The deterministic identity set is stored as three source-free shards behind [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.page-revisions.index.json). The initial hosted capture is recorded as workflow run `35503562530`, artifact `10603441105`, artifact ZIP SHA-256 `431558255b168e99f26ac7f5567bda7bb30d69288120b34f918ad3d0e50062c9`, with capture JSON SHA-256 `e5182724d8188fca48807c58720d17f1e40e55b121d1b172fa414e317859420c`.

## Non-transcluded gap audit

Scan-index pages **150–151** and **314–315** remain outside the frozen 410 dependency set, but they are no longer an entirely uninspected hole. Scriptorium transiently read the four exact Page revisions and committed only source-free identity, digest/count and body-presence evidence in [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.gap-audit.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.gap-audit.json). Hosted capture run `35515025304` produced artifact `10606587097`; its ZIP SHA-256 is `8171ce8c0dcd6d9f20a117e22cc35d0cee4a04d30b4a24c3d8d9befeaf55daa6`, and the exact capture JSON SHA-256 is `f1ca4fb4b0ac475be548c0b51efc08b7c1acbbdca3484101de128501862386ad`.

The result is deliberately conservative: page **150** (`oldid=5702065`) and page **314** (`oldid=5702066`) have nonempty transcluded bodies at their frozen revisions, so they are classified only as `nonempty_body_unclassified`; page **151** (`oldid=5702062`) and page **315** (`oldid=5701572`) have `no_transcluded_body` after removing comments and `<noinclude>` regions. This does **not** add any of the four pages to the 410 dependency set and does not decide that the nonempty pages are literary prose. That membership decision belongs to the later candidate-specific composition contract.

This is still **not a literary-body freeze**. Exact Page revisions, the backing PDF bytes and the gap body-presence surface are identified, but no Page-markup rendering/extraction contract, OCR/page-to-literary-text profile, body composition, body character count, or raw/normalized literary-body digest is claimed. The source-free graph manifest is [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json).

## Legal and publication boundary

The retained Wikisource and Commons surfaces mark the original Russian work/facsimile public domain. Scriptorium stores only provenance, metadata and derived evidence here; no literary source text, Page wikitext, OCR, rendered prose, PDF/image bytes or scan payload is committed.

## Coauthorship caveat

FantLab itself warns on the work's author-recognition surface that the text has two authors and that their mixed styles prevent exact recognition results. Scriptorium records that as a future **VOICE-model requirement**: this coauthored work must not silently become an individual Ilf or Petrov author profile. No author-profile result is claimed by this candidate record.

## What is still required

A later unit must define and verify a candidate-specific fail-closed literary-body extraction/composition contract over the **410 pinned Page revisions** and explicitly decide whether the nonempty gap pages **150** and **314** belong to the literary body; pages **151** and **315** are frozen with no transcluded body. Only after that can Scriptorium record raw plus `scriptorium-text-v1` normalized composite counts/digests and determine whether its own frozen body satisfies the >=300k corpus rule. If scan OCR is used to cross-check the public transcription, its OCR/page-extraction provenance must be frozen separately; exact PDF identity alone is not a literary-body extraction contract.

FantLab still does not disclose which edition or immutable byte stream it analyzed. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; the M2 reproduction gate remains **0/5 source-matched works**.

Machine-readable provenance: [`source-edition-traces/ilf-petrov-twelve-chairs-ru.json`](source-edition-traces/ilf-petrov-twelve-chairs-ru.json).
