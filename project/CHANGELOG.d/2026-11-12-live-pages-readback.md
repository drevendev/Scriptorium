# Live branch Pages readback — 2026-11-12

Issue #285. Based on merged master `ecf0e4c809428bd83d9ca265916fe0bb275532d5`.
This change is for later independent review; **LIVE_VERIFIED is not claimed by the PR**.

- Preserve the existing GitHub-managed `master / (root)` publisher and the separate, gated Actions artifact deployment. No administration or Pages-source change.
- On later `master` pushes, the Pages workflow runs a separately reported Chromium probe of the public `https://drevendev.github.io/Scriptorium/` site; pull-request builds still use staged local pages only.
- Before and after live interactions, compare eight public HTML/CSS/JS/JSON/CSV assets with **exact SHA-256 hashes of the checked-out master files**. A 200 response with stale content, a changed path/host, HTTP error or DNS failure is not deployment proof.
- Exercise real public desktop/mobile comparisons, mobile horizontal overflow, keyboard skip link, 29 glossary entries, author page, CSV and A4 PDF. Archive screenshots, PDF and explicit `LIVE_VERIFIED` / `LIVE_NOT_VERIFIED` JSON with the checked-out SHA.
- Allow a bounded delay for asynchronous branch Pages publication; a failed live probe is visible in a separate step/receipt and is non-blocking for static build/artifact preservation. A green build alone never implies live deployment.
- Offline guard smoke covers exact data, stale data, HTTP 404, cross-origin redirect, invalid base URL and path rejection.
- No changes to the 11 measured editions, source/provenance records, FantLab reference metrics, M2=0/5 or scientific profiles.

Local verification in the authoring environment: Node syntax and the new guard smoke passed. The real hosted Chromium and remote HTTP readback remain NOT_RUN until GitHub Actions executes them; this environment cannot resolve the Pages host.
