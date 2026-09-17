# Run receipt — SCRIP-CORPUS-020 `poemx1` control review

- Date: 2026-09-17
- Issue: #109
- PR: #116 (merged)
- Base at review: `master@3f2312675aca5d1fe60a716c818b45110d874761`
- Reviewed exact head: `fcc31b5163d56e6405a646fa88cad95d46e2432a`
- Merged commit: `440765ce082fb6857804dd2bddbeff0b96b7e819`
- Mode: independent review / provenance

## Selected bounded unit

Perform the required later-run judgement of PR #116, independently verify its candidate-specific historical MediaWiki control-flow evidence, and merge only if the exact reviewed head and checks remain clean.

## Review evidence

1. PR #116 was mergeable, 9 commits ahead / 0 behind current `master`, changed 9 expected files and had no inline review threads.
2. Exact-head workflows all completed successfully:
   - `35274153400` — Klim Samgin poemx1 control flow
   - `35274153394` — Klim Samgin poemx1 invocation bindings
   - `35274153427` — Klim Samgin historical template dependency
   - `35274153403` — Klim Samgin source revisions
   - `35274153406` — Scriptorium Pages
   - `35274153398` — Scriptorium frozen diagnostic
   - `35274153412` — Scriptorium pinned pylem provider
3. The dedicated control-flow job checked out exact head `fcc31b5163d56e6405a646fa88cad95d46e2432a`, ran 217 standard-library tests successfully, regenerated the source-free control manifest and byte-compared it to the committed artifact.
4. Independent inspection of Russian Wikisource `Шаблон:Poemx1` revision `oldid=5142743` confirmed the frozen frame decisions: empty parameter `1` skips the title block; omitted `fixed` selects the unequal branches of both fixed `#ifeq` calls; omitted `width` leaves the nested `#iferror` / `#expr` path unreachable; omitted `poem` selects the default-font branch; omitted `small` leaves its live `#ifeq` unequal; omitted parameter `3` skips the signature block.
5. Therefore the source structure independently supports reachable `#if` x4, `#ifeq` x3 and `#tag:poem` x1, with `#expr` x2, `#iferror` x1, one `#if` and two `#ifeq` occurrences unreachable for all six frozen calls.

## Result / boundary

No blocking defect was found. A COMMENT review was submitted against the exact head, PR #116 was marked Ready, and it was squash-merged as `440765ce082fb6857804dd2bddbeff0b96b7e819` without closing Issue #109.

The merged evidence does not reproduce recursive expansion of parameter `2`, the historical `#tag:poem` / poem-extension behavior, resolved Part 2 bytes, historical render equivalence, the four-part literary-body composite or FantLab analyzer-input identity. Those boundaries remain explicit, and M2 remains 0/5 source-matched works.

Next action: continue Issue #109 with only the live historical expansion path—recursive parameter-2 expansion as required by `#tag:poem` plus the evidenced historical poem-extension behavior—before any resolved Part 2 or four-part extraction/composition claim.
