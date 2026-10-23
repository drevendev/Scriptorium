# 2026-10-22 — Reader 0.4 delivery batch

- Accepted and merged earlier Reader 0.3 PR #278 as `5c03ee428df6cc36ebdeff2443d35ac9f7e72dca`; #277 closed by native GitHub. Exact-head baseline: 775 tests and installed-wheel checks passed. Pages deployment is still interlocked.
- Opened #288 on the reused `scrip-compare-003-local-cli` branch. Adopted #279: 29 canonical metrics, strict input/cross-report consistency, exact decimal deltas, offline HTML/JSON/CSV and private create-only output.
- Replaced legacy fixture-runtime mean tests with real `build_local_analysis()` reports. First full CI: 809 tests passed; an old hardcoded 0.2.0a1 smoke expectation then failed. Fixed it by requiring pyproject, installed metadata and exact CLI version agreement, retaining all installed tests and adding `-I` isolation. All six workflows passed at `dab93b3143ee8f494b2f2761bb21d25bf8153ad7`.
- Adopted #286's repin-aware source-unit guard without a second metric registry. Eight negative/positive tests plus one actual frozen-record check passed locally (43 local tests with the comparator). Full canonical CI must revalidate this successor before acceptance.
- Improved two-work navigation/export touch targets to a minimum of 44 pixels, retaining focus and reduced-motion styles. This is partial #283, not a claim of full browser/accessibility acceptance.
- Updated product-first README and existing compact queue; version is `0.4.0a1`. No external registry publication, new branch or access/administration change.
- Recovered distinct unpublished POS benchmark-join debt as #287 after deduplicating open and closed records. Existing #279-#286 remain their canonical scopes.
- New implementation remains pending later fresh acceptance. Browser HTTP navigation was blocked by the runtime: VISUAL_NOT_VERIFIED, no live-publication claim. Source data, scientific thresholds and M2 0/5 are unchanged.
