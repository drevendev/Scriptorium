# The Twelve Chairs — corpus candidate

**Candidate ID:** `ilf-petrov-twelve-chairs-ru`  
**Authors:** Ilya Ilf and Evgeny Petrov  
**Language:** Russian  
**Current status:** 1928 route graph + 410 exact Page revision identities + exact scan binary identity + source-free four-gap audit + gap composition-membership decision + exact-410 source-free markup-surface inventory + fail-closed rendering decision profile frozen / renderer semantics and literary body incomplete / not M2-admissible

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

## Non-transcluded gap audit and membership decision

Scan-index pages **150–151** and **314–315** remain outside the frozen 410 dependency set, but they are no longer an uninspected or composition-ambiguous hole. Scriptorium transiently read the four exact Page revisions and committed only source-free identity, digest/count and body-presence evidence in [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.gap-audit.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.gap-audit.json). Hosted capture run `35515025304` produced artifact `10606587097`; its ZIP SHA-256 is `8171ce8c0dcd6d9f20a117e22cc35d0cee4a04d30b4a24c3d8d9befeaf55daa6`, and the exact capture JSON SHA-256 is `f1ca4fb4b0ac475be548c0b51efc08b7c1acbbdca3484101de128501862386ad`.

The audit remains deliberately conservative: page **150** (`oldid=5702065`) and page **314** (`oldid=5702066`) have nonempty transcluded bodies at their frozen revisions and remain `nonempty_body_unclassified`; page **151** (`oldid=5702062`) and page **315** (`oldid=5701572`) have `no_transcluded_body` after removing comments and `<noinclude>` regions.

The source-free [`gap-membership.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.gap-membership.json) freezes the **composition-membership** decision separately from semantic classification: all four pages stay excluded because the three frozen canonical part routes do not transclude them. For nonempty pages 150 and 314 this is explicitly **not** a claim that the printed-page content is non-literary; body presence alone is insufficient to override the canonical route topology. The frozen literary dependency surface therefore remains exactly **410 pages**.

## Exact-410 Page markup surface

Scriptorium now has a source-free structural inventory over those same **410 exact pinned Page revisions**. The hosted auditor replays each pinned revision, verifies title, timestamp and MediaWiki SHA-1 before reading the exact Page wikitext transiently, then reduces it to construct shapes/counts and cryptographic per-Page receipts. It never serializes wikitext, template argument values, OCR, rendered prose, scan bytes or literary text.

The compact durable freeze is [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.render-surface.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.render-surface.json). It binds the inventory to the existing page-revision index SHA-256 `c1e3280984e640b8fe739a752ff49a3327633f49b52a635bd2d2d1e6a09f538f` and to a digest over all 410 transient source-free Page receipts. The observed surface includes ProofreadPage `noinclude`/`pagequality` wrappers plus a bounded set of tags/templates such as `poem`, `section`, `references`, `nop`, `razr2`, `heading`, `опечатка2`, accents and layout helpers. This is evidence about the exact markup surface that a future renderer must support; it is **not** a claim that those constructs are already rendered with Wikisource-equivalent semantics.

## Fail-closed rendering profile boundary

[`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.render-profile.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.render-profile.json) now freezes a candidate-specific decision table over that exact reviewed surface. It is bound to the 410-page index SHA-256 `c1e3280984e640b8fe739a752ff49a3327633f49b52a635bd2d2d1e6a09f538f` and render-surface freeze SHA-256 `8a4f04238c68c40e59464e76a7911f0bee9488e09daab9f8772b1af970768d23`; the profile's canonical SHA-256 is `88e410311435ab6bcfbd70ab0a2cea73ffe304e3ce2876d241d25ea38cc5d5cd`.

The contract classifies **all 12 observed tag shapes / 3,488 tag tokens** and **all 30 observed template shapes / 602 template invocations**, and it fails closed if any shape is added, removed or changed. Local structural decisions are frozen for comments, `<noinclude>`, `pagequality`, `section`, simple containers and `<br>`. Scriptorium deliberately does **not** infer template expansion from template names: all 30 template shapes / 602 invocations remain `unresolved`, as do the 410 `<references/>` tokens. `nop` is explicitly marked inter-page-sensitive rather than silently dropped.

Therefore `rendering_profile_frozen=true` means the fail-closed **decision boundary** is frozen, not that a complete renderer exists. `renderer_semantics_complete=false`, `renderer_implementation_ready=false` and `rendering_equivalence_claimed=false` remain explicit. The next renderer unit must freeze or otherwise evidence the unresolved Wikisource template/reference semantics before any Page prose can be composed.

This is still **not a literary-body freeze**. Exact Page revisions, the backing PDF bytes, the gap body-presence/membership surface, source-free markup inventory and fail-closed decision profile are identified, but inter-page composition/separator rules, unresolved template/reference expansion, body character count, and raw/normalized literary-body digests are not claimed. The route/source manifest remains [`source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json`](source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json).

## Legal and publication boundary

The retained Wikisource and Commons surfaces mark the original Russian work/facsimile public domain. Scriptorium stores only provenance, metadata and derived evidence here; no literary source text, Page wikitext, OCR, rendered prose, PDF/image bytes or scan payload is committed.

## Coauthorship caveat

FantLab itself warns on the work's author-recognition surface that the text has two authors and that their mixed styles prevent exact recognition results. Scriptorium records that as a future **VOICE-model requirement**: this coauthored work must not silently become an individual Ilf or Petrov author profile. No author-profile result is claimed by this candidate record.

## What is still required

A later unit must resolve and independently freeze the remaining template/reference semantics identified by the fail-closed profile, then implement/verify rendering against that contract. Inter-page composition/separator behavior over the **410 pinned Page revisions** remains a separate decision; the audited gap pages **150/151/314/315** stay outside that canonical composition surface unless new evidence explicitly revises the route contract. Only after renderer and composition semantics are independently reviewed can Scriptorium record raw plus `scriptorium-text-v1` normalized composite counts/digests and determine whether its own frozen body satisfies the >=300k corpus rule. If scan OCR is used to cross-check the public transcription, its OCR/page-extraction provenance must be frozen separately; exact PDF identity alone is not a literary-body extraction contract.

FantLab still does not disclose which edition or immutable byte stream it analyzed. Therefore `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; the M2 reproduction gate remains **0/5 source-matched works**.

Machine-readable provenance: [`source-edition-traces/ilf-petrov-twelve-chairs-ru.json`](source-edition-traces/ilf-petrov-twelve-chairs-ru.json).
