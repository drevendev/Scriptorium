# 2026-10-23 — SCRIP-REPRO-010 readiness matrix (authored)

- Add deterministic source-free Markdown, JSON and CSV readiness reporting for
  five independently frozen public candidates. Validate cross-file FantLab URL,
  work ID, analysis date, displayed count, source rights, frozen length and
  SHA-256 witnesses; conflicting or duplicate-key evidence fails closed.
- Compare displayed character counts diagnostically while preserving unknown
  FantLab analyzer-input identity, no other metric runs and M2 0/5. Explicitly
  surface the stale Running on Waves catalog status alongside its newer frozen
  literary-body witness.
- Add negative/tamper, deterministic-output and create-only CLI tests. This is
  a partial executable slice of #281, not its scientific acceptance or a live
  Pages deployment. Independent later-run review and CI are required.
