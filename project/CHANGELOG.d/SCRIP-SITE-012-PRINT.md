## 2026-10-23 — Reader comparison print readability (#283 partial)

- Identified a concrete paper-output regression in the live Comparison Desk markup:
  print previously cleared the 64rem table minimum but retained 17rem/10rem
  column minimums, clipping eight metric columns on normal printed pages.
- Render all 29 rows as labelled two-column cards in print media, preserving
  metric name, left/right values, units, difference, status and reason.
  The original on-screen semantic table, focusable scroll and privacy behavior
  are unchanged. Desktop input controls are omitted from paper.
- Added a canonical-source regression checking every HTML column's print label,
  minimum-width overrides, row wrapping and retention of meaningful values.
- Isolated local Chromium (A4) print fixture: computed row display `grid`,
  metric header min width `0px`, all seven data labels present; printed PDF
  rendered and inspected without horizontal clipping. **This was not a built
  canonical Pages route or a live deployment test.**
- Source/corpus/benchmark parity unaffected; M2 remains 0/5. Full #283
  desktop/mobile/keyboard/real-route acceptance remains open.
- Authored on dedicated branch from master `e60738b74ec25d9bda2a95eaeb7648750ca3a695`;
  hosted exact-head tests and later independent PR acceptance remain mandatory.
