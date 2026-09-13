# Static site renderer

Status: `scriptorium-static-site-v1` implementation candidate.

`scriptorium.site_renderer` turns the explicit publication allow-list into disposable
static output. It is deliberately downstream of the analysis artifacts: the renderer
cannot create or upgrade evidence, does not discover JSON by globbing, and never fetches
book text at build time.

## Build locally

From the repository root:

```bash
python -m scriptorium.site_renderer --output build/site
```

The publication input is always the canonical
`site/publication-manifest.json`; there is deliberately no CLI override that can substitute
another manifest. Relative output paths are resolved under the repository root. For
deletion safety, every output target must resolve inside the repository's `build/`
subtree; output elsewhere, including `.git`, is rejected. Generated output is ignored by
Git and is not canonical project state.

The current renderer writes:

- `build/site/index.html` — the publication index;
- `build/site/works/<slug>/index.html` — one page per supported work showcase;
- `build/site/assets/site.css` — deterministic shared styling;
- `build/site/build.json` — a non-canonical build receipt containing the generator
  profile, publication-manifest SHA-256, each allow-listed artifact SHA-256 and its route.

No timestamps or environment-specific paths are written into the generated tree. Given
the same manifest bytes, canonical artifact bytes and renderer revision, the output bytes
are deterministic.

## Renderer v1 scope

`scriptorium-static-site-v1` renders only `work_showcase` entries. Other kinds already
reserved by the publication schema (`benchmark`, `author_profile`, `tag_profile`) fail
closed until their canonical artifact contracts and presentation rules are implemented.
This is intentional: a generic renderer must not guess how evidence or admissibility
should be interpreted for a future artifact family.

Stable work routes follow the merged publication contract:

```text
/works/<slug>/
```

The index and work pages expose only selected derived/public metadata:

- manifest title and stable slug;
- author/work metadata;
- publication status;
- benchmark and corpus admissibility;
- manifest-level compatibility claim after canonical re-validation;
- metric ID, numeric/null value, unit and per-metric compatibility status;
- provenance provider/page, edition note, legal basis and immutable HTTP(S) source link;
- the canonical representativeness warning.

Fields such as source selections or excerpt boundary text are not copied into HTML merely
because they exist in the JSON artifact.

## Fail-closed validation

Before replacing any output, the renderer validates and renders every page in memory.
If any entry fails, the previous output tree is left untouched rather than being replaced
with a partially refreshed site.

The build is rejected when, among other cases:

- the canonical publication manifest is missing, unreadable, or traverses a symlink;
- the manifest profile, repository identity or deployment boundary is unexpected;
- an entry ID or slug is duplicate or unsafe;
- an artifact path is absolute, contains a traversal/double-separator shape, traverses a
  symlink, resolves outside the repository, is missing, or is not JSON;
- `source_text_included` is not exactly `false`;
- a showcase says `source.source_text_committed` is not exactly `false`;
- manifest schema/status/admissibility labels contradict the canonical showcase;
- the manifest compatibility claim does not equal the claim derived from canonical
  per-metric compatibility statuses;
- the renderer encounters an unsupported entry kind;
- a rendered metric has an unsupported evidence status, invalid unit, non-numeric value
  or non-finite number;
- a provenance link is not HTTP(S) or embeds URL credentials;
- the output target is a symlink or resolves outside the repository `build/` subtree,
  including through a symlinked parent.

All artifact-controlled strings are HTML-escaped. Remote provenance URLs are rendered as
links only; the builder never dereferences them.

## Deployment boundary

This unit does **not** enable GitHub Pages and does not add a deployment workflow. A
later reviewed unit may execute this renderer in GitHub Actions, upload `build/site` with
the Pages artifact action, and deploy it to the `github-pages` environment. Generated
HTML remains disposable output; the publication manifest and canonical JSON artifacts
remain the only repository publication inputs.
