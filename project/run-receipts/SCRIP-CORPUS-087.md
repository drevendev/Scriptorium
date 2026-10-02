# Run receipt — SCRIP-CORPUS-087

Status: COMPLETE

## Recovery state

- Canonical recovery base: `master@27f54858d20000244bb8e80342038d80ea510b45`.
- Issue: #263.
- PR: #264, squash-merged as `a9df79ec04664011f6dddf3593031424b15c1073`.
- Fresh recovery branch: `scrip-corpus-087-petersburg-preflight-current`.
- Exact stale Petersburg handoff used only as a five-file source: `a24bbaeff4054762640694b8025500815853d4a5`.
- Recovery semantic head before bookkeeping: `e6e93a4639f5986a85f87b5341f684ba6808dda7`.
- The stale branch itself was not merged and its old `STATE_AND_QUEUE.md` was not copied.

## Recovered evidence

- Source-free preflight physical SHA-256: `093f251cb8d03846a5158a1ac29d4b66e1796a7cc2bc65a77ade3d9e3cebcff1`.
- Exact frozen carrier: 632 pages / 3,621,459 bytes / SHA-1 `682476934dd6ed49c6bbcdb0720127c1812ff477` / SHA-256 `b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`.
- Existing OCR/body promotion contract SHA-256 remains `d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2`.
- Embedded text-layer status remains `unverified`; neither direct PDF text extraction nor raster OCR is selected.
- No PDF bytes, page images, extracted text or literary source text are committed.

## Gate boundary

Literary-page selection, extraction profile, body identity, >=300k admission, FantLab analyzer-input identity, diagnostics, M2 admission and parity remain closed. M2 remains 0/5.

## Completion

- Independently reviewed exact final head: `950404bb86c191b7eacdf21eb34c231f1d906fc4`.
- Hosted evidence at review time: 24/24 pull-request-triggered workflow runs completed successfully; no submitted reviews; no unresolved review threads.
- PR #264 was squash-merged with expected-head protection as `a9df79ec04664011f6dddf3593031424b15c1073`.
- Issue #263 closed completed.
- Recovery evidence boundaries remain unchanged: `embedded_text_layer_status=unverified`; direct PDF extraction, raster OCR, literary-body, >=300k admission, FantLab-input identity, diagnostics, M2 and parity remain closed.
