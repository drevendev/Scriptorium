# 2026-09-19 — SCRIP-CORPUS-027 Running on Waves page revisions

- Opened Issue #141 and Draft PR #142 to strengthen the retained 1965-source Russian Wikisource candidate for Alexander Grin's *Running on Waves*.
- Reused the already frozen route witness (`oldid=4715419`) and captured exactly 36 literary-page identities in route order `/1` through `/35` then `/Эпилог`.
- Each committed source-free row records page ID, exact revision ID, UTC revision timestamp and MediaWiki SHA-1; no literary prose is committed.
- Added fail-closed capture/validation/replay code and candidate-specific CI. Bootstrap run `35430448437`, job `105863933461`, completed successfully and uploaded source-free artifact `10581001332` with digest `sha256:a0c58c00b0e5a1ea0a6649815ef7489b06ca7eecb129cf7f19bd1729bf288572`.
- Kept the evidence boundary explicit: page-revision identity is frozen, but literary-body extraction/composition, composite counts/digests and FantLab analyzer-input/source-edition identity remain unresolved. M2 stays 0/5.
- The separate `/Версия 2` (`oldid=5655654`, az.lib.ru / Pravda 1980) remains a distinct non-composable route.
- PR #142 remains Draft because this run authored the substantive change; independent exact-head review is the next recovery unit.
