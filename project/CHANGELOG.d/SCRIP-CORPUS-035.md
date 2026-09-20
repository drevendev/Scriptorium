## SCRIP-CORPUS-035 — Darwin/Rachinsky literary-body composition contract

- Opened Issue #157 and Draft PR #158 from `master` `c885600f528e2883396d58e14f229824c61b0902`.
- Added `scriptorium-darwin-literary-body-contract-v1`, bound to the existing SHA-256-pinned 418-Page revision inventory.
- The contract selects only rendered numbered routes `/1` through `/14` as literary dependencies: 388 exact Page revisions in frozen route order.
- It excludes 30 frozen apparatus dependencies: parent-only sequences 8–21 and 423–427 plus alphabetical-index route `/Указатель` sequences 412–422. Source-declared no-text 114 and 411 remain explicit non-dependencies.
- The implementation fails closed on Page identity row-shape drift, topology drift, partition drift and contract drift. It emits only source-free contract metadata; no Page wikitext, OCR, rendered prose, scan bytes, body counts or body digests are serialized.
- Added dedicated CI to materialize and validate a source-free contract receipt. Page-wikitext rendering semantics, literary-body count/digests, >=300k proof, independent scan SHA-256 and FantLab source matching remain deferred gates.
- Fresh source inspection corroborated the apparatus boundary: Russian Wikisource Page 419 is alphabetical-index content, while Pages 425–426 are publisher-advertising/back-matter content. This evidence informed the contract but no source prose was copied into repository artifacts.
- This authored PR remains Draft for a later independent exact-head review; no self-approval or merge is performed in this run.
