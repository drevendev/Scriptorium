# 2026-11-06 — Conditional FantLab word-density gap

- Reuse the validated six-work retained metric matrix to quantify word-count drift **per 1,000 characters including spaces**, explicitly modelling only a hypothetical proportional-length adjustment. The raw counts and provenance remain immutable.
- For frozen Anna Karenina: 253,275 / 1,692,647 reference words/characters versus 269,358 / 1,705,605 inferred; signed density difference +8.292695 words per 1,000 characters, hypothetical residual +14,144.062082 words. These numbers prioritize segmentation/input-edition investigation, not a corrected value.
- A new source-free `scriptorium word-gap` CLI supports Markdown/CSV/JSON, fail-closed identity/count tests and explicit NOT_RUN. No manuscript read or new parity claim. M2 remains 0/5; later acceptance/CI required.
