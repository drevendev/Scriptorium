# Reader release repair and owner-requested cleanup

Refs #275, #269 and #273. This is a new successor PR, not a same-run merge acceptance.

- Independently accepted #268 at 50fbb9b9c0da59a5eb78c6826381b8acd3dd8aae and merged as 6338bedbeaf94b00374a95423bba5dd82368e593; #267 closed. Accepted #272 at 610dc8044c0f03a70c646eb48db51e6bd8ce19c7 after retargeting to the identical master base tree, merged as 9412ee54ab1a56c7c81f6ff4d290e39d83f49630; #271 closed. Both exact heads had 22 successful workflow runs.
- Adopt #274 at 62e6c078cb70ec77775007a1668fa0c3ede4f5fa, including its bounded/path-private local analyzer, formats, labels, package and tests. Correct only the staged-site body indentation in the complete renderer (original blob 74a79963b06777ab4b15145b541b7b06a59d7aed).
- Recover the pending crash-safe publisher patch against exact original blob f99fb10f4f19b3b363a3accbe68212feacf66c44. Keep a stable regular-file inode and nonblocking Linux flock released on process death; reject symlinks/special files. Retain atomic exchange/no-replace behavior. New subprocess tests have deadlines; original six plus new five pass locally (11/11). Baseline reproduced two crash errors before the fix.
- Reuse existing gallery branch c411e29030e7e778f99cd9689441d348f75a7715 and preserve its source-free two-work module/tests. Clarify offline status, digest-based registration and shell-redirection semantics. Add installed-gallery/deterministic-output CI checks and an early syntax check without changing existing test coverage or workflow permissions.
- Expand build/cache ignores, synchronize README examples, refresh the single compact queue and add roadmap/assessment. Reconcile the owner's 2026-10-02 delivery correction into AGENTS and manifest mode selection/liveness; M0-M5 scientific criteria are unchanged.

The complete corrected renderer compiled locally and its uploaded blob matches the tested
bytes. Full checkout was unavailable locally because Git DNS failed; the focused publisher
suite is not the full repository suite. Hosted exact-head CI/installed-wheel/canonical build
outcomes are native provider facts and remain pending at authoring. Real-route visual
acceptance is not inferred from earlier in-memory previews.

No frozen corpus/benchmark/showcase JSON, publication allow-list, dependency/dictionary pin,
external registry, Pages activation, repository administration, visibility or scheduler
change. M2 remains 0/5; no new corpus admission or FantLab parity claim.
