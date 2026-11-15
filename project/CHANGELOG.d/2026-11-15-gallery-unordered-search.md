# 2026-11-15 — Evidence gallery unordered search (#283)

- Match all nonempty title/author search terms in any order in the allow-listed evidence gallery; ignore repeated whitespace and preserve Russian case and `ё/е` folding.
- Exercise the actual emitted gallery JavaScript with a Node DOM stub for positive, negative, evidence-type, no-match and reset paths.
- Search remains local to heading/byline metadata; no manuscript text, tracking, new metric claims, or changed M2 gate.
- Proposed in a separate branch; exact-head CI and later-run independent acceptance are required before merge.
