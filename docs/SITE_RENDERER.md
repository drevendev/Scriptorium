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

Within `work_showcase`, renderer v1 explicitly supports only the two canonical profiles
already present in the merged publication manifest:

- `scriptorium-deterministic-metrics-v1`;
- `scriptorium-deterministic-metrics-v2`.

A newer or otherwise unknown artifact schema fails closed even when the manifest and
artifact repeat the same schema string. Supporting another profile is a reviewed
renderer-contract change, not an implicit consequence of compatible-looking JSON.

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
- top-level manifest or entry properties differ from the frozen
  `scriptorium-publication-manifest-v1` key sets;
- an entry ID or slug is duplicate or unsafe;
- an artifact path is absolute, contains a traversal/double-separator shape, traverses a
  symlink, resolves outside the repository, is missing, or is not JSON;
- a work-showcase `artifact_schema` is not one of the explicitly supported renderer-v1
  profiles above;
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

## GitHub Actions publication path

`.github/workflows/pages.yml` is the candidate publication workflow for the merged
renderer. Pull requests and relevant pushes run the standard-library test suite under
Python 3.13, build the site only through `scriptorium.site_renderer`, rebuild it into a
second disposable directory and require the two trees to be byte-identical before the
first `build/site` tree is uploaded as the Pages artifact.

The build job has only `contents: read`, checkout credentials are not persisted, and
GitHub-owned actions are pinned to reviewed full commit SHAs. The workflow currently
pins `actions/checkout` v7.0.1, `actions/setup-python` v7.0.0,
`actions/upload-pages-artifact` v5.0.0, `actions/configure-pages` v6.0.0 and
`actions/deploy-pages` v5.0.1. The current configure/deploy generations use the Node 24
action runtime.

Deployment is intentionally narrower than build verification. The deploy job:

- depends on the successful build job;
- runs only for `refs/heads/master`, never for pull-request events;
- additionally requires the repository variable
  `SCRIPTORIUM_PAGES_DEPLOY_ENABLED` to equal the literal string `true`;
- is the only job granted `pages: write` and `id-token: write`;
- targets the `github-pages` environment;
- runs `configure-pages` without its privileged `enablement` option before deploying the
  already-built Pages artifact.

The repository variable is a deliberate activation interlock, not evidence that Pages is
configured. This workflow does **not** enable Pages, change repository Pages source
settings, or use a secret/PAT to do so. An administrator must separately configure the
repository to use GitHub Actions as its Pages source and then set the activation variable
only after this workflow is independently reviewed. Until that happens, builds can prove
the publication artifact while the deploy job remains skipped.

Generated HTML remains disposable output; the publication manifest and canonical JSON
artifacts remain the only repository publication inputs.
