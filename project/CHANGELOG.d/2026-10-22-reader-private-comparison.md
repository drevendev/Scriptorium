# 2026-10-22 — Reader private comparison delivery

- Accepted and merged earlier Reader 0.3 PR #278 as `5c03ee428df6cc36ebdeff2443d35ac9f7e72dca`; #277 closed by native GitHub. Exact-head baseline: 775 tests and installed-wheel checks passed. Pages deployment is still interlocked.
- Adopted the previously unpublished #279 comparator into the existing `scrip-compare-003-local-cli` branch: 29 canonical metrics, strict input and cross-report consistency, exact decimal deltas, HTML/JSON/CSV and private create-only output.
- Replaced old fixture-runtime mean tests with real canonical analyzer reports. Local actual-source subset: 34 tests passed; actual installed execution-closure wheel smoke passed outside the checkout. Full repository CI belongs to the resulting PR, not to that local subset.
- Reader package version becomes `0.4.0a1`; no external registry publication or access/administration changes.
- Recovered distinct unpublished POS benchmark-join debt as #287 after deduplicating open and closed records. Existing #279-#286 remain their canonical scopes.
- New code requires later fresh acceptance before merge. Local HTTP browser navigation was blocked by the runtime; VISUAL_NOT_VERIFIED, no live-publication claim. M2 remains 0/5 and scientific gates are unchanged.
