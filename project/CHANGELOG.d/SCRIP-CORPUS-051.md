# SCRIP-CORPUS-051 — freeze Perelman 1913 scan byte identity

- Selected the next P2 corpus/provenance continuation after SCRIP-CORPUS-050 completed, keeping the diversity focus on Yakov Perelman's 1913 first edition of *Entertaining Physics, Book 1*.
- Opened Issue #189 and Draft PR #190 from `master@5262067b7fda3d7cb2b3aa898f719fbf588c705d`.
- Added a source-free transient streaming verifier for the exact current Wikimedia Commons original. The automation runtime could not resolve `upload.wikimedia.org`, so the initial PR workflow was intentionally used as the hosted capture surface rather than treating the provider metadata as independently verified.
- Hosted run `35641285926`, job `106470938299`, checked out exact authored head `1e7e41821d98f770887ffabcc1dd57866e899de0`, passed 7 focused fail-closed tests, streamed the exact current Commons PDF, and reproduced the provider-observed **28,168,847-byte** size and SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`.
- The independent stream established Scriptorium SHA-256 **`3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`**. Source-free capture artifact `10658576419` was 941 bytes as a ZIP with SHA-256 `a2814db9f4755db8dff262c171502a903c329977bfbf9e8b47716d40c37341b5`.
- Committed the source-free byte-identity receipt and changed the dedicated workflow from one-time capture to exact receipt replay/verification. The permanent Commons description `oldid=1045983412` remains bibliographic/legal provenance only; it is not claimed to version-pin the PDF binary.
- Updated the public candidate page and machine trace to distinguish **scan-binary frozen** from **OCR/literary-body frozen**. No PDF bytes, page images, OCR or source prose are committed or uploaded as project evidence.
- Kept page selection/OCR, literary-body character count and digests, the >=300,000-character admission gate, work-specific FantLab linguistic-analysis/input identity, diagnostics and M2 parity closed. M2 remains **0/5**.
- PR #190 remains Draft for independent later exact-head review and merge judgement after final hosted checks settle.
