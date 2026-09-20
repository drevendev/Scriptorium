# Run receipt — SCRIP-CORPUS-041

Date: 2026-09-20  
Issue: #169 (open)  
Pull request: #170 (Draft; independent exact-head review pending)  
Base at selection: `363004d58abe7908ee82a8c1ae9a29498e2a54e7`

## Unit

Inspect the four explicit scan-index gaps outside the frozen 410-Page dependency set for the retained 1928 *Zemlya i Fabrika* first-standalone edition of Ilf and Petrov's *The Twelve Chairs*. Freeze only exact Page identities plus source-free structural/body-presence evidence; do not compose the gap pages into a literary body.

## Evidence captured

Hosted capture workflow run `35515025304`, job `106089401762`, checked out authored PR head `b5ed51c576e1bb022579020d7d5db8a29d6da93d`, passed the standard-library suite and source-free boundary assertions, and read exact Page revisions 150, 151, 314 and 315 transiently. Artifact `10606587097` is a 1,576-byte source-free ZIP with GitHub/recomputed SHA-256 `8171ce8c0dcd6d9f20a117e22cc35d0cee4a04d30b4a24c3d8d9befeaf55daa6`; its single 4,670-byte JSON capture has SHA-256 `f1ca4fb4b0ac475be548c0b51efc08b7c1acbbdca3484101de128501862386ad`.

The frozen Page evidence is:

- page 150: revision `5702065`, MediaWiki SHA-1 `ec8cf1e4be633102be57d24e7f92ce5b8f5b2a09`, `nonempty_body_unclassified`;
- page 151: revision `5702062`, MediaWiki SHA-1 `a5e9448c366881761d9792d458c8e33ec4653999`, `no_transcluded_body`;
- page 314: revision `5702066`, MediaWiki SHA-1 `db7f57fc08df092cbed2ce31da776404ba5ed329`, `nonempty_body_unclassified`;
- page 315: revision `5701572`, MediaWiki SHA-1 `667deafe474f3fac76671c04a2ba3d2be40a2bb5`, `no_transcluded_body`.

For the two empty-body pages, the transcluded-body SHA-256 is the standard empty digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Page 150's source-free transcluded-body counts are 22 codepoints / 40 UTF-8 bytes / 18 letters; page 314's are 40 codepoints / 74 UTF-8 bytes / 34 letters. These counts are evidence of nonempty bodies only, not semantic or literary classification.

## Boundary and durable artifacts

The committed `ilf-petrov-twelve-chairs-zif-1928.gap-audit.json` contains no Page wikitext or prose. The 410 frozen dependency identities remain unchanged. The source graph and public candidate page now distinguish exact gap inspection from literary-body composition: pages 150/314 are nonempty but unclassified, pages 151/315 have no transcluded body, and all four remain outside the 410 dependency set for this unit.

No Page wikitext, OCR, rendered prose, PDF/image bytes, scan payload, or literary source text is committed.

## Gates

`literary_membership_frozen=false`, `literary_body_frozen=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `m2_parity_admissible=false`. Benchmark movement: none; M2 remains 0/5.

## Handoff

SCRIP-CORPUS-041 authored production is complete in Draft PR #170. The next wake must re-read the current exact PR head, wait for/inspect all exact-head checks, inspect the hosted source-free replay artifact, review the complete diff and threads, and only then decide Ready/merge. Do not self-approve this authored change. If merged later, reconcile this receipt with the reviewed exact head, replay IDs/artifact digest, merge SHA, closed Issue #169, and the post-merge state revision.
