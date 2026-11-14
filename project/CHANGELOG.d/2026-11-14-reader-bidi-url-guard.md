# 2026-11-14 — Reader catalogue URL direction-control guard (#283)

- Reject invisible bidirectional formatting and C1 control characters in shareable/deep-linked Reader catalogue search queries. Previously the share link could contain Unicode direction overrides that visually misrepresent a public search URL.
- Keep verified in-page filtering local and preserve ordinary Cyrillic names, search facets, source hashes and the no-JavaScript catalogue.
- Add negative Node regressions for bidi override/isolate and C1/Arabic marks, a deep-link rejection case and positive Cyrillic control. No text or metric changes; M2 remains 0/5.
- Exact-head CI, independent later-run acceptance and actual Pages deployment are separate gates.
