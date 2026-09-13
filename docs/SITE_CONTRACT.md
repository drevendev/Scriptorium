# Static publication contract

Status: `scriptorium-publication-manifest-v1` merged; `scriptorium-static-site-v1`
renderer is an implementation candidate under review.

This contract defines the boundary between Scriptorium's durable analysis artifacts and
the future GitHub Pages user interface. It does **not** enable Pages or claim that a
public site is already deployed.

## Architecture decision

The repository remains the source of truth. Analysis/showcase/benchmark JSON lives in
its existing versioned locations; generated HTML is a disposable build product.

When deployment is enabled, Scriptorium will use GitHub Pages with a custom GitHub
Actions build/deploy flow from the default branch rather than committing generated site
output to a `gh-pages` branch or `docs/` directory. The intended flow follows GitHub's
current Pages guidance:

1. check out the repository;
2. build a static site from the allow-listed public artifacts;
3. upload the generated directory with `actions/upload-pages-artifact`;
4. deploy it with `actions/deploy-pages` to the `github-pages` environment.

The deployment job needs only the permissions required by GitHub Pages (`pages: write`
and `id-token: write`, with repository contents read-only for the build). Enabling that
workflow, repository Pages settings, environment protection, and pinning exact action
revisions are separate reviewed units.

Official references:

- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://github.com/actions/deploy-pages

## Publication manifest

`site/publication-manifest.json` is an explicit allow-list of repository artifacts that
may enter the public site build. Merely adding JSON elsewhere in the repository does not
publish it.

The manifest is validated against
`schemas/scriptorium-publication-manifest-v1.schema.json` and freezes these concepts:

- `entry_id` — stable machine identity for the publication entry;
- `kind` — one of `work_showcase`, `benchmark`, `author_profile`, or `tag_profile`;
- `slug` — stable URL-safe page identity;
- `title` — human-facing label only, never the machine identity;
- `artifact_path` — repository-relative path to the canonical JSON artifact;
- `artifact_schema` — version/profile identity expected from that artifact;
- publication, benchmark-admissibility and corpus-admissibility labels;
- `compatibility_claim` — `inferred`, `reproduced`, `extension`, or `mixed`;
- `source_text_included` — fixed to `false` in v1.

The seed manifest indexes the two existing *Anna Karenina* showcase slices. Their
historical metric artifacts are not rewritten merely to fit a newer analyzer version.

## Stable routes

The site generator derives routes from `kind` + `slug`:

| Kind | Route |
| --- | --- |
| `work_showcase` | `/works/<slug>/` |
| `benchmark` | `/benchmarks/<slug>/` |
| `author_profile` | `/authors/<slug>/` |
| `tag_profile` | `/tags/<slug>/` |

The current `scriptorium-static-site-v1` candidate implements only `work_showcase`.
Reserved future kinds fail closed instead of being rendered through guessed generic
semantics. A title change must not change a slug. If a published slug ever needs
replacement, a later contract version must define redirect/alias semantics rather than
silently moving an existing page.

## Safety boundary

The Pages dataset contains derived/public metadata only. The builder must fail closed
rather than publish an entry when any of these invariants are violated:

- the entry is absent from the publication manifest;
- the artifact path is absolute, escapes the repository, or does not exist;
- `source_text_included` is not exactly `false`;
- an indexed showcase artifact says `source.source_text_committed` is not exactly
  `false`;
- the manifest's publication/admissibility labels contradict the canonical artifact;
- the manifest's `compatibility_claim` contradicts the claim derived from the canonical
  artifact's per-metric compatibility statuses;
- the renderer encounters an artifact family whose publication semantics are not yet
  implemented;
- a provenance URL is not HTTP(S) or embeds URL credentials;
- a renderer would need to fetch a remote book or embed source prose in order to build.

External source URLs may be rendered as provenance links. They are never a build-time
license to fetch or redistribute the referenced text. Artifact-controlled strings are
HTML-escaped before insertion into generated pages.

## Claim rendering

Pages is a presentation layer and may not upgrade evidence. Per-metric compatibility
status from the canonical artifact remains authoritative. For artifacts exposing a
non-empty `analysis.metrics` object, `scriptorium-publication-manifest-v1` derives the
manifest-level claim deterministically from every metric row's `compatibility_status`:

- if every metric has the same supported status, the manifest claim is that status;
- if two or more supported statuses are present, the manifest claim is `mixed`;
- missing/empty metric surfaces or unknown compatibility statuses are not publishable
  under this derivation rule and must fail closed until an explicit contract is added.

The supported per-metric statuses for this v1 derivation are `inferred`, `reproduced`
and `extension`. Therefore a manifest entry may claim `reproduced` only when **every**
canonical metric row is `reproduced`; combining reproduced metrics with inferred or
extension metrics yields `mixed`. The executable check lives in
`scriptorium.publication.validate_compatibility_claim`, and the renderer calls that
validation rather than trusting the manifest string by itself.

The current showcase artifacts contain inferred FantLab-shaped metrics plus the
Scriptorium sentence-count extension, so their derived manifest claim is `mixed`. The UI
still shows the finer per-metric labels.

`benchmark_admissibility=not_admissible` and
`corpus_admissibility=not_admissible` are visible to users for illustrative excerpts. A
pretty page must never turn a showcase slice into parity evidence.

## Renderer contract

`scriptorium-static-site-v1` is a standard-library renderer whose only publication
inputs are the manifest and canonical artifacts named by it. It never scans directories
for publishable JSON and never dereferences provenance URLs.

The renderer emits a deterministic root index, stable work pages, shared CSS and a
non-canonical `build.json` receipt containing the publication-manifest SHA-256, each
allow-listed artifact SHA-256 and the route generated for it. No timestamps or absolute
local paths enter the output.

Only explicitly selected derived/provenance fields are rendered. In particular, source
selection fields such as excerpt boundary text are not copied into HTML simply because
they exist in a canonical artifact. Numeric metric values must be finite JSON numbers or
`null`, units must be present, and per-metric compatibility status must remain one of the
supported evidence classes.

Before replacing an existing output directory, the builder validates and renders the
entire requested site in memory. A failing entry therefore leaves the previous output
tree untouched instead of producing a partially refreshed publication. A successful
build replaces the tree completely so stale pages cannot survive a manifest removal.
Output symlinks, the repository root, and repository ancestors are rejected as build
targets.

See [`SITE_RENDERER.md`](SITE_RENDERER.md) for the local command and generated layout.

## Build determinism

A site build is determined by:

- the repository commit being built;
- the publication manifest version and bytes;
- the canonical artifact bytes referenced by the manifest;
- the site generator version and its pinned build dependencies.

The generated directory is not canonical state and should not be committed. This avoids
a second mutable copy of analysis results and keeps review focused on source artifacts,
the allow-list, and renderer code.

## Next implementation boundary

After independent review of the renderer candidate, a later `SITE` unit may add and
enable the GitHub Pages workflow. That unit must call the renderer against the canonical
manifest, upload only the generated directory, pin reviewed action revisions, preserve
the fail-closed legal/evidence boundary, and keep generated HTML out of repository state.
Repository Pages settings and deployment are still disabled at this stage.
