# 2026-11-13 — Trusov VAR same-line CR isolation (PR candidate)

- Correct a distinct v4 diagnostic error: the logical-newline count already recognized bare CR, but same-line context for literal `{{ВАР}}` calls still searched only LF. Two separate CR-delimited safe calls could be falsely classified as multiple templates on one line.
- Version the conservative preview as v5 and use either CR or LF for before/after context boundaries. Preserve the <=12 logical-break bound, <=4096 invocation size, nesting, markup, inline, and comment refusal gates.
- Add paired LF/CRLF/CR positive previews and negative inline/enclosing-comment regressions. This changes only an inferred source-free preview, not a historical renderer or complete Trusov body.
- Prior #515 is merged; the existing 145-Page incomplete metric diagnostic remains valid, 11 full measured editions and M2=0/5. New exact-head CI and independent later-run acceptance are required.
