# Original EPUB report replay proposal — 2026-11-06

Extend the accepted private `scriptorium verify` command with `--epub` to
re-extract an owner's original unencrypted EPUB in memory and verify its saved
29-metric JSON report against the same extracted UTF-8 bytes and profiles.
Optional `--provenance` cross-checks the source-free sidecar from
`scriptorium epub --provenance-output`, including exact archive SHA-256 and
extraction identity, so a different ZIP containing identical body text cannot
masquerade as the original archive. Fail closed on malformed sidecars, EPUB
structural/size violations, changed body and symlink input; never publish prose.

Reader/FantLab parity and literary admission do not advance (M2 0/5).
Exact-head CI and later independent acceptance are required before merging.
