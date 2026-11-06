# 2026-11-06 — Strict FantLab reference calendar validation

- Source-free five-work benchmark readiness now checks that each dated FantLab
  reference is a real ISO calendar day, not merely a matching YYYY-MM-DD string.
- Mirrored invalid dates in the catalog, source trace and reference cannot
  make fictitious dated evidence pass. Valid leap days remain accepted.
- This strengthens #281 reference provenance integrity without changing any
  observed metric, source identity, edition/legal gate, or M2 0/5.
