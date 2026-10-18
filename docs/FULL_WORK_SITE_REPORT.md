# Full-work reports in the canonical static site

`scriptorium-static-site-v2` extends the existing publication-manifest-v1 renderer with
one reviewed, source-free historical diagnostic. It also adds a reader-first homepage
with a real report action, explicit page types, shared keyboard focus/skip links and a
responsive card grid. Existing four routes and their scientific labels are retained.

```bash
python -m scriptorium.site_renderer --repo-root . --output build/site
```

The generated homepage links to `works/anna-karenina-full-work-diagnostic/`. That page
reuses `frozen_diagnostic_report` from SCRIP-SITE-007: 28 historical fields, 23 numeric
actuals, five missing actuals, expected/actual/raw deltas, correct mean-length denominators
and replay identities. A backlink returns to the work list. No metric is recalculated.

## Publication boundary

The manifest must explicitly include the frozen report. Directory discovery is not
supported. `scriptorium/site_frozen_diagnostic.py` registers the exact existing JSON path,
entry ID, slug, publication/compatibility/source-text flags and SHA-256 of the reviewed
snapshot. The standard schema validator runs even after the byte digest matches; the
parsed object must agree with the verified bytes. This narrow registration intentionally
rejects unreviewed new snapshots, changed observations, altered labels and path aliases.
A new snapshot requires scientific/security review and an explicit registration change.

The registration does not grant corpus admission or identify FantLab's input. The entry
remains diagnostic-only, inferred, with `corpus_admissibility=not_admissible`; the original
source-free JSON is not rewritten. M2 remains 0/5. The four existing artifacts keep their
own previously reviewed corpus and compatibility flags.

All entries are validated and rendered before the existing disposable output is replaced.
A broken input, unapproved digest or report-integration mismatch leaves the previous
valid build intact. `build.json` records the exact consumed input hashes and five routes.
The existing workflow performs the full suite and a byte-identical canonical rebuild.

## Acceptance and delivery

Tests exercise the canonical five-entry manifest, all internal links/fragments, historical
row counts, source-free output, digest/flag tampering, missing/aliased files, output
preservation, title escaping and deterministic builds. Shared navigation/card/action links
have minimum 44px targets; tables are named, focusable scrolling regions with scoped
headers. The full report retains its own standalone stylesheet and historical labels.

A successful build is not a live deployment. The existing Pages deployment variable,
repository configuration and later fresh PR acceptance gates are unchanged. No workflow
permissions or external services are added. Visual screenshots require an environment
where browser navigation is allowed; structural tests are not visual verification.
