## SCRIP-CORPUS-046 — Darwin/Rachinsky unresolved-semantic priority backlog

- Added `scriptorium-darwin-render-semantic-backlog-v1`, derived only after the independently reviewed render profile validates against its frozen exact-388 source surface.
- Preserved all unresolved rendering shapes without promoting semantics: 5 tag shapes / 518 tag tokens and 38 template shapes / 4,583 invocations.
- Grouped the unresolved surface into provider-template (37 shapes / 4,579 occurrences), provider-reference (3 / 466), provider-math (2 / 52), and inter-page (1 / 4) tracks.
- Made future renderer research selection deterministic: the highest-impact unresolved row is template `ё` with arity 0/0 and 2,227 observed invocations. This is a priority decision only; `semantic_status=unresolved` remains frozen.
- Added a canonical source-free backlog artifact with SHA-256 `4ec4f84566f5f3f8dccd1945906d1a782f4532547a13cadc8570cb5b682bdcb2`, regression coverage, deterministic rebuild CI, and a public companion page.
- Independent review COMMENT `5262708679` found two acceptance/recoverability blockers on the authored head: canonical state had not recorded SCRIP-CORPUS-046, and the canonical Darwin candidate page still described merged PR #178 as Draft while omitting the semantic backlog.
- Repaired both review blockers on Draft PR #180: `project/STATE_AND_QUEUE.md` now records SCRIP-CORPUS-046 / #179 / #180 as `REVIEW_PENDING`, and the canonical Darwin candidate page links/summarizes the source-free backlog and corrects PR #178 to merged status.
- Kept renderer semantics/implementation/equivalence, inter-page composition, literary-body identity, >=300k admission, FantLab source match, diagnostics, and M2 parity closed. M2 remains 0/5.
- Draft PR #180 remains intentionally unmerged after the recovery repair; the changed exact head requires fresh settled checks and a later independent review before Ready/merge.
