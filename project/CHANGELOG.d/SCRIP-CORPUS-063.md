# SCRIP-CORPUS-063 — Darwin `{{ё}}` canonical replay root

- Corrected the Darwin/Rachinsky replay contract before dependency binding: invocation spelling `{{ё}}` resolves to canonical MediaWiki page title `Шаблон:Ё`, so the exact dependency roots are now `Шаблон:Ё` and `Шаблон:ЕЁ` rather than the non-canonical alias spelling `Шаблон:ё` plus `Шаблон:ЕЁ`.
- Upgraded the machine-readable contract to `scriptorium-darwin-template-yo-replay-contract-v2`, preserving the source-free fail-closed boundary while adding revision-pinned title-canonicalization evidence from MediaWiki `Manual:Page naming/en@8270202` and Russian Wikisource canonical root observations `Шаблон:Ё@5687302` / `Шаблон:ЕЁ@3684646`.
- The new root observations explicitly set `mediawiki_sha1_bound=false`: they establish canonical title/revision observations only and do not masquerade as complete dependency identities.
- Regenerated the canonical replay contract with SHA-256 `9b2e8914a5b4c3518ef331c27dc09a6a30d4d6433e90169c677348048f3dcd52`.
- Strengthened regression coverage so lowercase alias `Шаблон:ё` cannot satisfy a complete dependency closure. Focused local standard-library verification passes **19/19** tests.
- Updated the public Darwin semantic-backlog page so future replay work binds canonical titles and still requires revision timestamp, MediaWiki content SHA-1, recursive direct-dependency discovery evidence, closed graph edges and deterministic output verification.
- Opened Draft PR #214 for independent later review. No template source prose, renderer implementation, body admission, FantLab source match or M2 gate changed; M2 remains 0/5.
