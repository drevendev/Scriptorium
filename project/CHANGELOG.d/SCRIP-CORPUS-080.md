# SCRIP-CORPUS-080 — Darwin `<references/>` candidate-local promotion

- Base: exact `master@51c38fbeed3f7583df74c814f7b3580be0628153`.
- Issue: #249.
- Branch: `scrip-corpus-080-darwin-references-promotion`.
- Draft PR: #250.
- Consumes only the independently reviewed SCRIP-CORPUS-079 source-free containment contract (`3dde2e1ea259ccc4f855ad20dc8df588f9546a9ec181f84155175a86c3b139e3`): 388/388 observed self-closing `<references/>` tokens are inside already-stripped `<noinclude>` regions, with 0 outside.
- Adds a fail-closed promotion builder/validator and six focused regressions.
- Promotes exactly that candidate-local shape to `drop_via_existing_strip_nontranscluded_region`; provider Cite semantics remain unreplayed.
- Effective unresolved tag surface falls from 5 shapes / 518 tokens to 4 / 130. Provider-reference backlog falls from 3 shapes / 466 occurrences to 2 / 78.
- Template surface remains 37 shapes / 2,356 invocations. The deterministic next research slice becomes template `ВАР` (2 positional / 0 named), observed 388 times.
- Promotion SHA-256: `4052973abc6c413503f26c27419770a2214bf3253ecb31ec9d4cf3c1276dec39`.
- Semantic-backlog v3 SHA-256: `4b68de749eec8bbacf0e07cb9f87e2c5c2db0c81d438a191fadd15f4dffbda18`.
- Historical transclusion, offline/version-pinned MediaWiki runtime, complete renderer/inter-page/body, >=300k, FantLab analyzer-input identity and M2 parity remain closed.
- Authoring run leaves PR #250 Draft for independent later judgement; it must not self-approve or self-merge this substantive change.
