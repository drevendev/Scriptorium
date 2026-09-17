# SCRIP-CORPUS-020 — merge poemx1 control-flow evidence

- Independently reviewed PR #116 exact head `fcc31b5163d56e6405a646fa88cad95d46e2432a` in a later run, separate from the authoring run.
- Re-checked exact Russian Wikisource `Шаблон:Poemx1` revision `oldid=5142743`; under the frozen shared frame (`1` defined empty, `2` defined non-empty, `3/fixed/poem/small/width` omitted), its source structure yields reachable `#if` x4, `#ifeq` x3 and `#tag:poem` x1 while both `#expr` calls and the single `#iferror` call remain unreachable.
- Verified all seven pull-request workflows on the exact reviewed head completed successfully. The dedicated control-flow job checked out that exact SHA, ran 217 standard-library tests, regenerated the source-free control artifact and byte-compared it with the committed evidence.
- Marked PR #116 Ready and squash-merged it as `440765ce082fb6857804dd2bddbeff0b96b7e819`.
- Issue #109 remains open. The next live historical expansion prerequisite is recursive parameter-2 expansion plus the evidenced `#tag:poem` / historical poem-extension behavior. Dead `#expr` / `#iferror` paths are not implementation prerequisites for these six frozen calls.
- No resolved Part 2 identity, historical render equivalence or FantLab source match was promoted. M2 remains 0/5 source-matched works.
