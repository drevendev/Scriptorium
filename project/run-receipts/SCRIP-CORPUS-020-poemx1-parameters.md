# Run receipt — SCRIP-CORPUS-020 `poemx1` literal parameter surface

- Date: 2026-09-17
- Issue: #109
- PR: #114 (draft; independent review pending)
- Branch: `scrip-corpus-020-poemx1-frame`
- Base at selection: `41b7effb148247164398e063e55795855e68b436`
- Result: `POEMX1_PARAMETER_SURFACE_AUTHORED_REVIEW_PENDING`

## Bounded unit

Advance only the next evidenced historical MediaWiki prerequisite after merged PR #113: freeze the literal triple-brace template-parameter reference/default surface of pinned inferred `Шаблон:Poemx1` oldid `5142743` after the already-frozen inclusion-control selection.

Do **not** bind the six real `poemx1` invocations in this unit. Do not recursively expand inserted argument wikitext, execute parser functions, render `#tag:poem`, claim historical render equivalence, resolve Part 2 bytes, or produce a literary-body digest.

## Implementation

`scriptorium/mediawiki_template_frame.py` adds a bounded fail-closed profile for literal triple-brace parameter references. It distinguishes missing parameters from parameters explicitly defined as an empty string, applies defaults only to missing parameters, supports nested literal parameter defaults, and preserves a missing no-default reference as its original triple-brace spelling. Dynamic/unsupported parameter-name shapes fail closed. Inserted argument values are deliberately not recursively parsed by this layer.

The source-free manifest records only revision identity, the post-inclusion input digest, literal parameter names/counts/default classes, evidence URLs and capture-scope booleans. It does not store template source text or expanded argument payloads.

Focused tests cover defined/non-empty values, defined-empty values, missing defaults, missing bare parameters, nested literal defaults, non-recursive inserted values, dynamic/malformed fail-closed behavior, source-free inventory and manifest boundaries.

## Official semantics evidence

The bounded behavior is tied to current official MediaWiki documentation:

- `https://www.mediawiki.org/wiki/Help:Templates` — triple-brace template parameters, omitted/default behavior, and the distinction between omitted and explicitly empty arguments.
- `https://www.mediawiki.org/wiki/Help:Parser_functions_in_templates` — undefined versus defined-empty parameters and empty defaults.
- `https://www.mediawiki.org/wiki/Manual:Template_expansion_process` — template expansion context; this Scriptorium profile intentionally supports only literal parameter names and stops before the broader expansion process.

## Exact-source observation

Dedicated workflow `35249215580` checked out authored head `99031deb1ecf10358e8b94bbd65a4b5be7de138b`, passed **205** standard-library tests, re-resolved exact historical `poemx1` oldid `5142743`, regenerated the existing raw-shape and post-inclusion evidence, and generated the source-free parameter manifest before failing at the intentionally absent expected artifact.

The generated evidence established:

- post-inclusion input SHA-256: `86ad628a9d8fc3d904fd513a1b4335f4e9f816ceedfa2af736e8e3a94e32ffbf`
- total literal parameter references: **21**
- counts: `1` x2, `2` x1, `3` x2, `fixed` x6, `poem` x1, `small` x6, `width` x3
- exactly one bare no-default reference: `fixed` x1
- empty-default references: `1` x2, `2` x1, `3` x2, `fixed` x1, `poem` x1, `width` x1

The generated artifact is committed as `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-template.parameters.json`, and the dedicated workflow now requires a byte-for-byte replay match.

## Fail-closed correction during authoring

The first authored-head CI run `35249020020` ran **205** tests and had one failure in the new dynamic-parameter test. The implementation did fail closed as intended, but the test over-specified that rejection must occur at the literal-name validator. The structurally ambiguous input was rejected earlier by the brace parser as `unclosed MediaWiki brace construct`. The test was repaired to assert the actual contract—`ValueError` fail-closed behavior—without broadening accepted syntax. The subsequent 205-test run was green.

## Public representation

`corpus/candidates/gorky-klim-samgin-ru.md` now exposes the source-free post-inclusion input digest and exact literal parameter inventory, while stating that concrete invocation binding, recursive inserted-value expansion, parser functions, `#tag:poem`, historical render equivalence and resolved Part 2 remain unresolved.

The machine-readable provenance trace references the new parameter manifest and keeps `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`.

No source prose is committed.

## Evidence boundary / next action

PR #114 remains Draft because this run authored the substantive change. A later independent run must review the exact final head and required checks before merge judgement.

If merged, the next bounded Issue #109 layer is source-free binding of the six concrete `poemx1` invocation argument shapes to the frozen literal parameter surface, followed by only the required `#expr`, `#if`, `#ifeq`, `#iferror` and `#tag:poem` behavior. Resolved Part 2 and four-part literary-body digests remain prohibited until the complete target-only expansion layer replays deterministically.

M2 remains **0/5 source-matched works**.
