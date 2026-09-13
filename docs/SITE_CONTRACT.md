# Static publication contract

Status: `scriptorium-publication-manifest-v1` architecture candidate.

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

The future site generator derives routes from `kind` + `slug`:

| Kind | Route |
| --- | --- |
| `work_showcase` | `/works/<slug>/` |
| `benchmark` | `/benchmarks/<slug>/` |
| `author_profile` | `/authors/<slug>/` |
| `tag_profile` | `/tags/<slug>/` |

A title change must not change a slug. If a published slug ever needs replacement, a
later contract version must define redirect/alias semantics rather than silently moving
an existing page.

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
- a renderer would need to fetch a remote book or embed source prose in order to build.

External source URLs may be rendered as provenance links. They are never a build-time
license to fetch or redistribute the referenced text.

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
`scriptorium.publication.validate_compatibility_claim`, and a future renderer must call
that validation rather than trusting the manifest string by itself.

The current showcase artifacts contain inferred FantLab-shaped metrics plus the
Scriptorium sentence-count extension, so their derived manifest claim is `mixed`. The UI
must still show the finer per-metric labels.

`benchmark_admissibility=not_admissible` and
`corpus_admissibility=not_admissible` must be visible to users for illustrative excerpts.
A pretty page must never turn a showcase slice into parity evidence.

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

A later `SITE` implementation unit may add the generator, static HTML/CSS/JavaScript and
Pages workflow. That unit must consume this manifest rather than rediscovering files by
directory glob, must test the fail-closed safety rules above, and must not weaken the
repository's legal/provenance gates.
