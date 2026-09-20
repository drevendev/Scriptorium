# Run receipt — SCRIP-CORPUS-040

Date: 2026-09-20  
Issue: #167  
Pull request: #168 (Draft; authored in this run)  
Base at selection: `ea69d44b5bd15802dee10dc2f3188093a53eb69a`

## Unit

Freeze the exact source-free binary identity of the Wikimedia Commons PDF backing the already retained 1928 *Zemlya i Fabrika* first-standalone edition route for Ilf and Petrov's *The Twelve Chairs*.

## Evidence captured

Official Commons metadata reports a 424-page original of 77,978,350 bytes with SHA-1 `4ab6aa42c3517169e99c1177b6fb6412cfe9187d`. Hosted capture run `35509143401`, job `106073891876`, checked out PR head `79fbc45d2056aea1adcb0f4b65da965b30b555c2`, passed the source-free identity tests, streamed the exact original transiently, reproduced that byte count and SHA-1 and independently computed SHA-256 `5a82f8101f9c17dfafcf8b45dc9ed5a7cdfa12a3e88d18bd0f0987e4fcd51eb4`.

Capture artifact `10603893998` contains only the JSON identity receipt: 875-byte archive, GitHub digest `sha256:0807a0489aacc6d10ab752d6e3e1ec240d0eede1344f3271f0206f179d3c4cdb`. The PDF itself, page images, OCR, Page wikitext, rendered prose and literary source text are not committed.

## Durable result

The branch commits a strict source-free receipt plus a replay workflow. The canonical structured trace, route graph and public candidate page now bind the retained 1928 family to the exact scan binary while retaining the independently reviewed 410 Page revision identities. The scan-identity receipt explicitly records that the Page dependency set did not change and that gaps 150–151 and 314–315 remain unclassified.

## Gates

`literary_body_count_and_digests_frozen=false`, `minimum_300k_proved_from_frozen_body=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `m2_parity_admissible=false`. Binary identity is edition-witness provenance only; it is not a literary-body extraction contract or FantLab source match. M2 remains 0/5.

## Handoff

PR #168 must remain Draft after this authored run. A later wake must independently re-read the then-current exact PR head against its base, inspect settled exact-head CI including the dedicated scan replay, verify that no source payload entered the diff and only then decide whether to mark Ready/merge.
