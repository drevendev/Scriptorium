# 2026-10-23 — Private batch Reader (#290)

- Added explicit bounded manifest processing through the canonical installed Reader analyzer, with no source upload or corpus enrollment.
- Delivered create-only, deterministic SHA-bound JSON/HTML reports and complete HTML/JSON/CSV batch indexes, including explicit failures and duplicate reuse.
- Protected input/output directory components with POSIX no-follow directory handles, and made complete JSON indexes publish last for safe retry.
- Added real-core CLI, privacy, collision, symlink, input-limit and interrupted-write regressions.
- M2 remains 0/5; public Pages deployment is unchanged.
