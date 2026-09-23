# Run receipt — SCRIP-CORPUS-066

- **Unit:** SCRIP-CORPUS-066 — freeze dependency revision-selection policy for Darwin `{{ё}}` replay
- **Issue:** #219 (open)
- **Pull request:** #220 (Draft; authoring wake)
- **Base:** `master@9c874256d5e6d30ecc9c018241b3f97ef94e5b4d`
- **Branch:** `scrip-corpus-066-darwin-dependency-selection-policy`
- **Scope:** `drevendev/Scriptorium` only

## Produced

The bounded unit resolves a provenance question before the next recursive replay step: how an exact `Модуль:String` dependency revision may be selected. Reviewed v4 binds the two root templates and discovers the module, but deliberately leaves that child exact-identity-unbound.

Current official MediaWiki evidence does not support backdating the child from a caller/root timestamp. `Help:Templates` describes ordinary calls as dynamic transclusion; `API:Expandtemplates` documents `revid` as revision context for `REVISIONID` and similar variables rather than a recursive dependency-version pin; Wikimedia Phabricator T31051 records the lack of normal versioned-transclusion support, with T70399 closed as its duplicate on 2026-08-14.

Added source-free `scriptorium-darwin-dependency-revision-selection-policy-v1`, bound to reviewed v4 SHA-256 `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64`. Canonical policy SHA-256 is `4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855`.

The policy requires the next child binding to record canonical title, exact revision ID, revision timestamp, MediaWiki SHA-1 and a controlled observation context together. It explicitly sets caller-timestamp selection, `expandtemplates revid` recursive pinning and historical child inference to false.

## Verification

- Added `scriptorium/darwin_dependency_revision_policy.py`, which recomputes the canonical policy digest, binds it to the reviewed v4 predecessor, confirms `Модуль:String` is still the only discovered unbound dependency, validates the official evidence URLs and fails closed if downstream gates move.
- Added four focused `unittest` regressions covering committed-policy validation/digest stability, rejection of caller-timestamp selection, rejection of recursive `expandtemplates revid` pinning and unchanged downstream gates.
- Extended `.github/workflows/darwin-template-yo-direct-dependency-probe.yml` so PR heads run the new regression and validator while retaining deterministic v4 rebuild/compare and exact-root re-query verification.
- Public companion `corpus/candidates/darwin-origin-species-rachinsky-1864-ru-template-yo-direct-dependencies.md` now exposes the selection boundary and policy artifact without source prose.

The exact PR head and hosted workflow settlement must be re-read from PR #220 after this receipt commit; this authoring wake does not self-approve the change.

## Gates / handoff

- `Модуль:String` exact identity remains unbound.
- Caller/root timestamps are not allowed as dependency revision selectors.
- `expandtemplates revid` is not treated as a recursive dependency revision pin.
- `dependency_closure_complete=false`.
- forced/non-forced output verification remains open.
- renderer rule promotion remains false.
- literary-body / >=300k admission remains false.
- `fantlab_source_edition_match=unknown`.
- `m2_parity_admissible=false`.
- M2 remains **0/5**.

Next action is independent exact-head review of Draft PR #220 after all PR-triggered checks settle. If merged, the next Darwin replay unit may bind `Модуль:String` only through a controlled explicit revision observation/binding and then recursively freeze its descendants.
