# SCRIP-CORPUS-047 — Darwin/Rachinsky `{{ё}}` documentation evidence boundary

- Selected from the reviewed SCRIP-CORPUS-046 semantic backlog because template `ё` is the mechanically highest-impact unresolved row: arity 0/0, 2,227 invocations, priority rank 1.
- Current official Russian Wikisource documentation (`Шаблон:ЕЁ/Документация`, permanent revision `oldid=5090323`, dated 2024-01-11) documents zero-argument `{{ё}}` as a conditional single-character shorthand: `ё` under forced yoification, `е` otherwise. Current proofread help also describes `{{ё}}` / `{{ё!}}` as the mechanism supporting yoified and non-yoified finished-text variants.
- Added `scriptorium/darwin_template_yo_evidence.py` and a deterministic source-free evidence record with canonical SHA-256 `3c0af5dfe8d23cd6d47ce2f92b30c58b83e352df692c18e6d4f59a14928eb06a`.
- The evidence deliberately records a historical-gap witness: retained Page sequence 11 is revision `3358032` from `2018-08-13T19:18:33Z`, predating the 2024 documentation revision. Current documentation therefore narrows the semantics but does not prove the historical template/dependency state used by retained Page revisions.
- Kept the render profile and semantic backlog unchanged: all 43 shapes remain unresolved and `ё` remains `semantic_status=unresolved`. A later bounded unit must freeze historical `Шаблон:ЕЁ` / `Шаблон:ё` revision/dependency identity at retained Page-save anchors before renderer promotion is considered.
- Added regression tests plus a dedicated deterministic rebuild workflow and updated the public semantic-backlog companion page.
- Renderer implementation/equivalence, inter-page composition, literary-body counts/digests, >=300k admission, FantLab source match, diagnostics and M2 parity remain closed; M2 remains 0/5.
