# 2026-11-13 — Trusov Page standalone-template context guard (PR candidate)

- Preserve literal `{{nop}}` and `{{heading|...}}` lines when they occur inside a multiline comment, wikilink or enclosing template. A line-shaped call was previously projected despite belonging to an outer construct; that could alter source-free projected Page digests and the already-incomplete interior diagnostic.
- Reuse the existing conservative enclosing-markup check from the optional VAR preview; malformed enclosing context fails closed rather than being silently rewritten. Add positive/negative regressions over LF, CRLF and bare CR, including calls after a closed comment/link/template.
- No new historical renderer, body extraction, rights approval or FantLab source identity is claimed. The 145-Page excerpt remains **incomplete**; 11 complete measured editions and M2=0/5 remain unchanged. Exact-head pinned-source replay and independent later-run acceptance are required before merge.
