# 2026-11-12 — Trusov historical VAR preview line-break guard

- In `scriptorium.robinson_trusov_projection`, count **logical** line breaks in bounded `{{ВАР}}` previews: LF, CRLF and bare CR all count; CRLF is one break. The prior v3 preview counted LF only, permitting more than twelve bare-CR breaks.
- Version the inferred preview policy as `bounded_flat_and_multiline_VAR_orthography_branch_only_inferred_v4`; keep the report schema and honest `PARTIAL_TEMPLATE_PROJECTION_NOT_BODY` state. No historical renderer or source-text equivalence is claimed.
- Add explicit 12-accepted / 13-refused regression cases for all three line-ending forms; refused call evidence retains SHA-256 and reason only, never branch contents.
- Pinned 150-Page graph, rights, corpus membership, analyzed editions and FantLab M2 parity remain unchanged. This is a small correctness dependency for #511, not body extraction or a completed translation pair.
