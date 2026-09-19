# SCRIP-CORPUS-029 — Twelve Chairs 1928 Wikisource source graph

- Selected the already retained 1928 Zemlya i Fabrika *Twelve Chairs* transcription as the next P2 corpus/provenance strengthening unit; the distinct later 1938/1961 editorial family remains separate.
- Pinned the ProofreadPage source index at `oldid=5702510` and the three part-parent revisions at `oldid=5702507`, `5704332`, and `5702508`.
- Recorded the exact parent-page transclusion topology over the common ProofreadPage index: scan pages **8–149**, **152–313**, and **316–421**, totaling **410 Page-namespace dependencies**.
- Kept scan-index gaps **150–151** and **314–315** explicit and unclassified rather than silently composing or discarding them.
- Added `corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json` as a source-free route-graph manifest; no literary prose, Page-namespace content, or scan bytes are committed.
- Reconciled the public candidate page and structured provenance so `route_graph_frozen_underlying_pages_unfrozen` cannot be mistaken for a frozen literary body.
- The exact revisions of the 410 referenced Page-namespace pages, facsimile PDF bytes, literary extraction/composition contract, body counts, and body digests remain unfrozen.
- FantLab analyzer-input/source-edition identity remains unknown; `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains **0/5 source-matched works**.
- Independent exact-head review verified authored head `4976172850b375ce34357fdf0e0c860188258d35` against unchanged base `8a1195878757126511902625ffbdbbc38a178156`: 7 commits ahead / 0 behind, mergeable, no inline review threads, and all 13 pull-request-triggered workflows successful.
- Official Russian Wikisource source views independently confirmed the three `<pages>` ranges 8–149, 152–313, and 316–421 against the same 1928 Zemlya i Fabrika ProofreadPage index; inclusive arithmetic is 142 + 162 + 106 = 410. The two two-page gaps remain explicit and unclassified.
- `Scriptorium Pages` run `35441912697`, job `105894074343`, checked out the exact authored head, ran 287 tests successfully, built the canonical site, verified a deterministic rebuild, and uploaded artifact `10583813114` (`sha256:efed0b1a23842e721bb04e9a824703a6f3e64a53e8ba8c522b9e9372b4690789`).
- Review found no blocking defect. PR #146 was marked Ready and squash-merged as `a9abd3c01134683a0bc50aea204d2a2c05de9f93`; Issue #145 closed completed. The route graph is now canonical in `master`, while the 410 Page revision identities, PDF bytes, literary body and FantLab input remain unfrozen/unmatched.
