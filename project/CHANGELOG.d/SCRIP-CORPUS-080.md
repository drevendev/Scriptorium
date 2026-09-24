# SCRIP-CORPUS-080 — Darwin `<references/>` candidate-local promotion

- Base: exact `master@51c38fbeed3f7583df74c814f7b3580be0628153`.
- Issue: #249.
- Branch: `scrip-corpus-080-darwin-references-promotion`.
- PR: #250.
- Consumes only the independently reviewed SCRIP-CORPUS-079 source-free containment contract (`3dde2e1ea259ccc4f855ad20dc8df588f9546a9ec181f84155175a86c3b139e3`): 388/388 observed self-closing `<references/>` tokens are inside already-stripped `<noinclude>` regions, with 0 outside.
- Adds a fail-closed promotion builder/validator and six focused regressions.
- Promotes exactly that candidate-local shape to `drop_via_existing_strip_nontranscluded_region`; provider Cite semantics remain unreplayed.
- Effective unresolved tag surface falls from 5 shapes / 518 tokens to 4 / 130. Provider-reference backlog falls from 3 shapes / 466 occurrences to 2 / 78.
- Template surface remains 37 shapes / 2,356 invocations. The deterministic next research slice becomes template `ВАР` (2 positional / 0 named), observed 388 times.
- Promotion SHA-256: `4052973abc6c413503f26c27419770a2214bf3253ecb31ec9d4cf3c1276dec39`.
- Semantic-backlog v3 SHA-256: `4b68de749eec8bbacf0e07cb9f87e2c5c2db0c81d438a191fadd15f4dffbda18`.
- Historical transclusion, offline/version-pinned MediaWiki runtime, complete renderer/inter-page/body, >=300k, FantLab analyzer-input identity and M2 parity remain closed.
- Independent later-run review re-read all 8 changed files on exact final head `3832167289da2f90d4149c86e79807d95ed84de2` against unchanged `master@51c38fbeed3f7583df74c814f7b3580be0628153`; review `5300795617` found no merge blocker or open review thread.
- All 23 PR-triggered workflow runs returned for the exact head completed successfully. Frozen diagnostic run `35962074234` was bound to that SHA and both replay jobs passed their standard-library and frozen-source steps.
- PR #250 was marked Ready and squash-merged with expected-head protection as `07339c174be870237345851042e8515d11dc6adf`; Issue #249 closed `completed`.
