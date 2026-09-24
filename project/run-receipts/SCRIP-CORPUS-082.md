# Run receipt — SCRIP-CORPUS-082

- Unit: SCRIP-CORPUS-082
- Issue: #253
- Draft PR: #254
- Base: `master@bd291227733155672f8dd6d9d3a634348615cdbe`
- Status: `REVIEW_PENDING`
- Stream: corpus / provenance / renderer evidence
- Benchmark movement: none; M2 remains `0/5`

## Bounded result

Fresh Russian Wikisource research materially changed the replay-selection decision for the unresolved Darwin/Rachinsky `{{ВАР}}` shape. The already reviewed VAR implementation module is pinned at `Модуль:Дореформенная орфография@5721277` (2026-06-08). Current provider evidence observed `Модуль:Header@5746249` (2026-09-10), and a Wikisource forum discussion dated 2026-09-08 explicitly raised whether `{{ВАР}}` had broken after Header-related changes. This run records the discussion only as provider-drift risk; it does not assert a proven production failure.

The source-free evidence contract `scriptorium-darwin-var-provider-drift-evidence-v1` has SHA-256 `6126adbc966c7120ca487fb940bd0e01aafa0d7350d332e6422edbf8b3846cb8`. It links prior evidence SHA-256 `321ced32bb7ffc75829b6fbb5255bce3243641a80c21ad4e2b7bb7a25138502d` to the observed Header revision and deterministically replays only the title-classification rule needed by retained mainspace title `О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)`. The edition segment `1864 (ВТ:Ё)` yields `isPRS=false`, so `Модуль:Дореформенная орфография@5721277` would select its second/modern argument if its non-Page branch is reached under that observed Header rule.

## Evidence boundary

Not frozen/proven in this unit:
- live `Шаблон:ВАР` root revision identity;
- `Module:Header` MediaWiki SHA-1;
- execution-relevant nested dependency closure;
- complete `{{ВАР}}` invocation replay;
- historical transclusion identity;
- offline/version-pinned MediaWiki runtime;
- renderer promotion, literary-body identity, >=300k admission, FantLab analyzer-input identity or parity.

The effective unresolved counts remain 4 tag shapes / 130 tokens and 37 template shapes / 2,356 invocations; `ВАР` remains unresolved at 388 invocations.

## Verification authored in this unit

Focused regressions rebuild the committed evidence deterministically, verify the retained title classifies as `isPRS=false`, cover positive ДО cases, assert all full-replay/promotion gates remain false, and ensure the community warning is retained as risk evidence rather than upgraded to a runtime-failure claim.

Local deterministic builder/validator checks passed before commit. GitHub exact-head workflow evidence is intentionally left for CI and the next independent-review wake; PR #254 remains Draft.

## Next trigger

Independently review the exact final PR #254 head and CI. If clean, mark Ready and merge with expected-head protection. A subsequent VAR replay unit must choose one explicit coherent snapshot, freeze exact `Шаблон:ВАР`, `Модуль:Дореформенная орфография`, `Module:Header` identities including MediaWiki SHA-1 and execution-relevant nested closure, then replay the candidate invocation without silently substituting a later live descendant.
