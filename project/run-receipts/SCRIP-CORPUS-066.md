# Run receipt — SCRIP-CORPUS-066

- **Unit:** SCRIP-CORPUS-066 — freeze dependency revision-selection policy for Darwin `{{ё}}` replay
- **Issue:** #219 (closed completed)
- **Pull request:** #220 (independently reviewed; squash-merged as `32b0cb0d4cd1e682b8a8f77cf97b41d30bd4b63d`)
- **Authoring base:** `master@9c874256d5e6d30ecc9c018241b3f97ef94e5b4d`
- **Reviewed head:** `4494f97a3efba0efd290daafb5fa1af9ec420131`
- **Branch:** `scrip-corpus-066-darwin-dependency-selection-policy`
- **Scope:** `drevendev/Scriptorium` only

## Produced

The bounded unit resolves a provenance question before the next recursive replay step: how an exact `Модуль:String` dependency revision may be selected. Reviewed v4 binds the two root templates and discovers the module, but deliberately leaves that child exact-identity-unbound.

Current official MediaWiki evidence does not support backdating the child from a caller/root timestamp. `Help:Templates` describes ordinary calls as dynamic transclusion; `API:Expandtemplates` documents `revid` as revision context for `REVISIONID` and similar variables rather than a recursive dependency-version pin; Wikimedia Phabricator T31051 records the lack of normal versioned-transclusion support, with T70399 closed as its duplicate on 2026-08-14.

Added source-free `scriptorium-darwin-dependency-revision-selection-policy-v1`, bound to reviewed v4 SHA-256 `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64`. Canonical policy SHA-256 is `4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855`.

The policy requires the next child binding to record canonical title, exact revision ID, revision timestamp, MediaWiki SHA-1 and a controlled observation context together. It explicitly sets caller-timestamp selection, `expandtemplates revid` recursive pinning and historical child inference to false.

## Verification

- Independent review `5287014474` re-read all 8 changed files at exact head `4494f97a3efba0efd290daafb5fa1af9ec420131` against unchanged `master@9c874256d5e6d30ecc9c018241b3f97ef94e5b4d` and found no merge blocker or open review thread.
- Fresh evidence review confirmed MediaWiki `Help:Templates` still documents ordinary dynamic transclusion, `API:Expandtemplates` still documents `revid` as context for `REVISIONID` and similar variables, T31051 remains open for versioned transclusion, and T70399 was closed as its duplicate on 2026-08-14.
- All 21 PR-triggered workflow runs on the exact reviewed SHA settled `success`.
- Dedicated Darwin run `35816344164` explicitly checked out `4494f97a3efba0efd290daafb5fa1af9ec420131`, ran 27 focused regressions, rebuilt/compared v4 byte-for-byte, validated policy SHA-256 `4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855`, and re-queried the exact historical roots.
- PR #220 was marked Ready and squash-merged with expected-head protection as `32b0cb0d4cd1e682b8a8f77cf97b41d30bd4b63d`; Issue #219 automatically closed `completed`.

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

SCRIP-CORPUS-066 is complete. Resume normal-flow queue selection. A later Darwin replay unit may bind `Модуль:String` only through a controlled explicit revision observation/binding and then recursively freeze its descendants before output/renderer/body/FantLab promotion.
