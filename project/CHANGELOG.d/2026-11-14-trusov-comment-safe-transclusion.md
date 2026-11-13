# 2026-11-14 — Trusov Page inclusion directives inside comments (PR candidate)

- Correct `transclusion_input` to treat `<noinclude>`, `<includeonly>`, and `<onlyinclude>` written inside a balanced HTML comment as literal source, not live transclusion directives. Previously the scanner could silently drop commented text or reject a harmless example as an unbalanced inclusion tag.
- Preserve genuine outside inclusion tags and explicitly refuse unclosed/nested HTML comments instead of assigning speculative historical rendering semantics. Include LF, CRLF and CR positive/negative regressions.
- All pinned Page, projection, and excerpt receipts remain subject to exact-head CI replay: this change is NOT evidence of complete Trusov narrative extraction, historical rendering equivalence, legal admission or FantLab input identity. Eleven full measured editions and M2=0/5 are unchanged; no historical prose is committed.
