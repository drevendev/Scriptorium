## SCRIP-CORPUS-035 — structured-provenance review repair

- Independent exact-head review of Draft PR #158 found one blocking consistency defect: the canonical structured source-edition trace still described literary-body composition as unfrozen even though the branch had already frozen the 388 literary / 30 apparatus selection contract.
- Reconciled `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json` with `scriptorium-darwin-literary-body-contract-v1`.
- The structured trace now records 418 frozen Page identities, the 388 numbered-route literary dependencies, 30 apparatus dependencies, and no-text 114/411 as explicit non-dependencies.
- The repair deliberately keeps Page-wikitext-to-prose rendering, composite separator/body-rendering semantics, literary-body counts/digests, >=300k admission, independent scan SHA-256, FantLab source identity and M2 parity unfrozen/false.
- Added a regression test that fails if the structured trace later loses the frozen composition boundary or silently promotes downstream gates.
- PR #158 remains Draft after this authored repair. A later run must independently review the new exact head and settled CI before Ready/merge.
