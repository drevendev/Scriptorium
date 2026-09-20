# Run receipt — SCRIP-CORPUS-040

Date: 2026-09-20  
Issue: #167 (closed completed)  
Pull request: #168 (squash-merged as `eae276fd01774ef3ed094a1ef5b4dad353359a33`)  
Base at selection: `ea69d44b5bd15802dee10dc2f3188093a53eb69a`

## Unit

Freeze the exact source-free binary identity of the Wikimedia Commons PDF backing the already retained 1928 *Zemlya i Fabrika* first-standalone edition route for Ilf and Petrov's *The Twelve Chairs*.

## Evidence captured

Official Commons metadata reports a 424-page original of 77,978,350 bytes with SHA-1 `4ab6aa42c3517169e99c1177b6fb6412cfe9187d`. Hosted capture run `35509143401`, job `106073891876`, checked out authored head `79fbc45d2056aea1adcb0f4b65da965b30b555c2`, passed the source-free identity tests, streamed the exact original transiently, reproduced that byte count and SHA-1 and independently computed SHA-256 `5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4`.

Capture artifact `10603893998` contains only the JSON identity receipt: 875-byte archive, GitHub digest `sha256:0807a0489aacc6d10ab752d6e3e1ec240d0eede1344f3271f0206f179d3c4cdb`. The PDF itself, page images, OCR, Page wikitext, rendered prose and literary source text are not committed.

## Independent exact-head review

A later run re-read PR #168 at exact head `820269e512928e1b38b2c99dd00643e21ee08128` against unchanged base `ea69d44b5bd15802dee10dc2f3188093a53eb69a`. The branch was 13 commits ahead / 0 behind, mergeable, with no inline review threads. All 15 PR-triggered workflows on that exact head settled `success`.

Dedicated replay run `35509447298`, job `106074688049`, ran on the exact reviewed SHA and completed scan/provenance tests, exact Commons-original replay, gate-boundary assertions and source-free artifact upload. Independent artifact inspection downloaded `10604853582`, recomputed its 1,439-byte ZIP as SHA-256 `9e8f319bf0de47c385eb0ae885e31ad15aab6413d4e1aa96942b5e3c2cdbb61e`, and confirmed that it contains only the committed source-free receipt plus verification JSON. The receipt records 77,978,350 bytes, SHA-1 `4ab6aa42c3517169e99c1177b6fb6412cfe9187d`, SHA-256 `5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4`, while preserving `page_dependency_set_changed=false`, `gap_pages_classified=false`, and all body/admission/FantLab/M2 gates closed.

The changed-file set contains only workflow, code, tests, control documents and source-free provenance artifacts. No PDF/image bytes, OCR, Page wikitext, rendered prose or literary payload entered the diff. Review was recorded as COMMENT rather than self-approval. With no blocker found, PR #168 was marked Ready and squash-merged as `eae276fd01774ef3ed094a1ef5b4dad353359a33`, automatically closing Issue #167 completed.

## Durable result

Master now binds the retained 1928 family to an independently reviewed exact scan binary identity while retaining the already reviewed 410 Page revision identities. The scan-identity receipt explicitly records that the Page dependency set did not change and gaps 150–151 and 314–315 remain unclassified.

## Gates

`literary_body_count_and_digests_frozen=false`, `minimum_300k_proved_from_frozen_body=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `m2_parity_admissible=false`. Binary identity is edition-witness provenance only; it is not a literary-body extraction contract or FantLab source match. Benchmark movement: none; M2 remains 0/5.

## Handoff

SCRIP-CORPUS-040 is complete. Resume normal-flow selection from the queue. A later bounded unit may inspect the four explicit scan-index gap pages or define a fail-closed candidate-specific literary-body extraction/composition contract over the frozen 410 Page revisions, but body/admission/FantLab/M2 gates must remain closed until independently verified.
