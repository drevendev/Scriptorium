# White Guard: immutable revision inventory, not an analyzed book

The retained `bulgakov-white-guard-ru` candidate now has a provider-verified inventory
of all **20 chapter revisions**. Chapters 1–11 belong to the Paris Concorde 1927
source family; chapters 12–20 to Moscow Pravda 1989. The split is intentional and
must not be represented as one verified print edition.

## Reproduce the identity check

From a checkout, with Python and no optional morphology dependencies:

```sh
# Local byte/structure verification; provider replay explicitly stays NOT_RUN.
python -m scriptorium.white_guard_delivery --offline

# One metadata-only request for the exact committed revision IDs.
python -m scriptorium.white_guard_delivery
```

Both commands emit source-free JSON. Live mode emits `provider_replay: VERIFIED`
only after every requested page ID, title, revision ID, timestamp and MediaWiki
SHA-1 matches. Offline mode is `NOT_RUN`, never a substitute for that provider
check. A missing/modified manifest or failed provider request yields a nonzero
exit code and **no receipt**; it never recaptures current page revisions.

The artifact is pinned by SHA-256:
`094fddd834667be7a0e03eda141efc2d68235506351a421681e6c6e80353836c`.
Its exact 11,705 bytes are retained at
`corpus/candidates/source-edition-traces/bulgakov-white-guard-ru.source-revisions.json`.
Whitespace changes also require explicit re-admission rather than silently
changing the reviewed evidence.

## Capture and adoption evidence

The one-time draft bootstrap used existing `white_guard_revisions` primitives.
It requested only `rvprop=ids|timestamp|sha1`, captured the current 20 identities,
and immediately replayed those exact identities. No content/slot/body request
was made. The reviewed artifact was downloaded and checked before adoption.

- Capture commit: `e05eaee1903c58e95ca1007cf3be4b92502349ae`.
- Successful capture/replay workflow: [41853192167](https://github.com/drevendev/Scriptorium/actions/runs/41853192167).
- Artifact ID: `13336482763`, `white-guard-source-identities`.
- ZIP SHA-256: `1cdc4e1b0b268a60f9ee328c946ade16311a9a63b9cd42cc2bea231a450e08e4`.
- Bootstrap receipt SHA-256: `d7caca44791138542e2a6d06b9f04fb911dfc4921fe167b1214a1b1ec1edec7d`.

The final workflow has **no bootstrap branch or current-title capture**. It
runs the standard-library suite, verifies the committed byte pin, replays the
exact oldids, and uploads only a successful source-free receipt. The working
checkout and Actions token are read-only; no provider edits or repository writes
occur in CI. A future source update needs an explicit reviewed change to both
the manifest and its pin, with a new capture/replay provenance record.

## Validation and scope

The adapter reuses the canonical revision schema, rejects duplicate JSON keys,
nonfinite values, unbounded/nonregular inputs, symlinks and source-prose fields,
and verifies the immutable byte hash. The canonical validator now checks exact
JSON scalar types: Boolean/floating values cannot impersonate integer chapter
numbers, and numbers cannot impersonate scientific gate flags.

The manifest establishes only **revision identity and the declared partition**.
Literary-body extraction, completeness, normalized hashes, character count,
rights for any new downstream use, print collation and FantLab analyzer-input
identity require their own evidence. No full book is retained here, no Reader
book is added, and **M2 remains 0/5**.

## Earlier outbox reconciliation

The substantive SCRIP-CORPUS-087 private outbox design dated 2026-09-29 is adopted
through existing issue #408, not duplicated. Its separate pending-patch document
was empty and was not treated as executable code. The unrelated 2026-10-05 POS
comparison handoff already exists in `benchmark_pos.py` and its tests; it is not
new work for this delivery. Private storage IDs and links are intentionally absent.
