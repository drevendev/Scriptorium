# CHANGELOG — Scriptorium project meaning

This log records changes to project meaning, gates and durable control state. Normal
code changes remain in Git history and their issues/PRs.

## 2026-09-11 — Bootstrap contract

- Created the repository-native EndlessZen project contract.
- Set the first milestone to public FantLab metric reproduction before extensions.
- Set the parity corpus minimum at 300,000 characters including spaces.
- Required explicit legal provenance for corpus admission and prohibited assuming that
  web availability grants reuse rights.
- Made every translation a separate work identity.
- Chose Python as the analysis core direction and the AOT/pylem lineage as the first
  FantLab-morphology compatibility candidate.
- Defined exact-after-display-rounding parity on at least five source-matched,
  legally usable works as the M2 gate.
- Reserved modernism/postmodernism, translations, nonfiction/popular science and
  permission-compatible online fiction as required diversification directions for the
  public corpus rather than allowing the corpus to collapse into 19th-century classics
  and genre fiction.
- Required derived analysis/provenance rather than full copyrighted text in the public
  repository.
- Bootstrap review corrected the mode-selection claim: the hourly task currently uses
  the user-authorized deterministic ladder, while an independently verified external
  controller/selection receipt remains an explicit EndlessZen conformance gap.

## 2026-09-11 — Repository scope boundary

- Made `drevendev/Scriptorium` the sole development target of this autonomous worker.
- Kept `drevendev/EndlessZen` as a read-only operating-model reference for Scriptorium.
- Allowed reusable EndlessZen findings to be reported as Issues for its own maintainers
  after contributor and duplicate checks, without turning framework maintenance into a
  Scriptorium work unit.
- Kept other repositories read-only unless inspection is necessary for Scriptorium
  research, provenance, dependency evaluation or comparison.

## 2026-09-11 — FantLab metric contract

- Froze `fantlab-2022-v1` metric identifiers for the first deterministic/public
  compatibility surface.
- Separated public definitions, public-only surfaces, inferred candidates and unresolved
  definition edges so undocumented FantLab behavior cannot silently become a claim of
  reproduction.
- Defined stable scalar IDs plus generated POS, POS-bigram, sentence-position POS and
  punctuation families from the public 2022 analysis surface.
- Recorded the discrepancy between the article's broader POS vocabulary and the 17
  buckets observed on a 2022 work page as a morphology research question rather than a
  guessed mapping.
- Added a versioned field-by-field benchmark comparison schema with exact reference
  surface, edition/legal/hash provenance, expected display text, actual raw value,
  deltas and `pass | fail | unresolved | not_run` outcomes.
- After independent review, made the metrics object key the sole metric identity so a
  schema-valid row cannot carry a contradictory nested identifier.
- After independent review, stopped deriving decimal precision from rendered text.
  `display_places` must come from independent field/surface evidence; otherwise decimal
  comparison remains `unresolved_precision` rather than widening the match interval.
- Required exact source-edition match plus legal basis and immutable digest before a
  numeric match can count as parity evidence.

## 2026-09-11 — FantLab parity-corpus seed

- Added a machine-readable candidate catalog with five full Russian novels whose public
  FantLab analyses each exceed the 300,000-character corpus threshold and whose source
  work pages carry explicit public-domain notices.
- Recorded source-transcription provenance where available instead of treating a generic
  work title as an edition identity; `Идиот` is deliberately marked weak because its
  current Wikisource transcription warns that the source edition is unidentified.
- Kept all five candidates `gate_ready: false`: FantLab's `/lp` surfaces do not identify
  the exact source edition or immutable bytes used for the published analyses.
- Recorded held leads separately, including a volume-level `Война и мир` analysis whose
  independence for the five-work M2 gate is not yet defined.
- M2 parity progress remains 0/5 source-matched works; candidate availability must not be
  confused with benchmark admissibility.

## 2026-09-12 — AOT/pylem compatibility candidate

- Pinned `pylem==0.0.18` by package version and published sdist SHA-256, plus the
  repository revision that declares 0.0.18 and its exact `morph_dict` and `pybind11`
  submodule revisions.
- Recorded the distinction between an immutable PyPI artifact hash and the weaker
  repository-version match because PyPI metadata does not encode the Git commit used to
  build the uploaded sdist.
- Independent review found that the first mapping used documentation-facing Cyrillic AOT
  labels instead of the actual runtime strings returned by pinned pylem. The contract was
  repaired around `SetUseNationalConstants(false)` and `LemmaInfo.part_of_speech`.
- The repaired machine contract enumerates all 22 pinned AOT source POS slots and the 21
  unique Latin runtime strings they render to.
- Fifteen runtime strings have unambiguous semantic counterparts on the observed
  `fantlab-2022-v1` surface and may be mapped directly as inferred candidates.
- Both noun `С` and cardinal numeral `ЧИСЛ` both render as runtime `N`. The public pylem Python
  result does not expose the original AOT POS enum/ancode, so noun/cardinal remains an
  explicit unresolved collision instead of two false direct mappings.
- `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT` and `INFINITIVE` are distinct runtime
  categories in the pinned backend; their folding onto the 17 displayed FantLab buckets
  remains unresolved.
- Refused to invent either a FantLab homonym-selection policy or a runtime-collision
  recovery heuristic. Future adapter work must preserve uncertainty until a discriminator
  and source-matched benchmark evidence justify it.
- Kept pylem/AOT dictionary equivalence to FantLab 2022 explicitly unproven.
- Native build verification remains pending; the original execution environment could
  not resolve external package hosts, which is an environment limitation rather than a
  pylem failure.

## 2026-09-12 — Deterministic text model candidate

- Added the first executable Python analysis layer under `scriptorium/`.
- Defined `scriptorium-text-v1` normalization as newline canonicalization plus Unicode
  NFC while preserving all other whitespace, punctuation, case and quote style.
- Added deterministic word candidates and sentence candidates with half-open offsets
  into normalized text.
- Kept tokenization and sentence-boundary behavior explicitly `inferred`; no abbreviation
  heuristic or undocumented FantLab rule is guessed into the implementation.
- Added golden tests for Cyrillic/mixed tokens, internal hyphen/apostrophe behavior,
  exact normalized-text offsets, punctuation/ellipsis/closing quotes, blank input,
  unterminated tails and deterministic replay.
- Exposed the first executable capability in the public README and documented that the
  next verified metric slice should publish derived analysis for real legally usable
  books rather than waiting for the complete analyzer.
- Independent review found a bootstrap architecture drift: the repository still named
  `pytest` while this slice deliberately uses standard-library `unittest`. The
  architecture now makes `unittest` the initial unit/golden/benchmark runner and defers
  `pytest` until a concrete fixture, parametrization or plugin need justifies adding it.

## 2026-09-12 — First deterministic metric profile

- Added `scriptorium-metrics-v1` for character count, word count, mean word/sentence
  length and a Scriptorium sentence-count diagnostic on top of `scriptorium-text-v1`.
- Added all 14 observed FantLab punctuation-per-1000-word fields under an explicit
  `scriptorium-punctuation-v1` candidate policy.
- Made compound punctuation greedy/non-overlapping, documented Unicode ellipsis,
  dash/quote/ellipsis handling, and kept every FantLab-shaped value `inferred` until
  source-matched benchmarks demonstrate parity.
- Added `scriptorium-deterministic-metrics-v1` JSON Schema with stable metric IDs, units,
  evidence class, compatibility status and normalized-text digest.
- Added standard-library golden tests covering formulas, zero denominators, punctuation
  overlap, diagnostic raw counts, deterministic digests and schema/profile identity.
- Added the first real-source derived showcase from an exact Russian Wikisource revision
  of *Anna Karenina*, Part I, Chapter I. Only provenance, selection hashes and derived
  metrics are stored; the selected prose is not committed.
- The showcase is explicitly an illustrative 1,298-character excerpt, below the
  300,000-character corpus threshold and inadmissible as FantLab parity evidence.

## 2026-09-12 — Executable FantLab benchmark harness candidate

- Added `scriptorium-benchmark-v1` as a standard-library local-text comparison CLI over
  the existing `fantlab-benchmark-comparison-v1` schema.
- Bound every run to raw and normalized SHA-256 plus explicit edition-match, source and
  legal provenance instead of treating a local filename as source identity.
- Made exact integer equality eligible for `pass` only when the source edition is exact,
  legal basis is recorded and immutable raw bytes are hashed; otherwise the result stays
  `unresolved` even when numbers match.
- Kept mean-length and punctuation decimal fields at `unresolved_precision` because
  FantLab display precision and tie-breaking are not independently established.
- Preserved captured JSON numeric lexemes as display evidence, so values such as `10.30`
  are not silently rewritten to `10.3` while still refusing to infer precision from them.
- Limited the first executable comparison to the 18 FantLab metrics actually implemented
  today; unimplemented page/dialogue/vocabulary/POS fields are omitted rather than
  manufactured as zero or `not_run`.
- Added CLI/gate tests and public documentation. The existing `Шутиха` reference remains
  source-unmatched, so M2 parity progress remains 0/5.
- Independent review found that the first admission gate trusted `edition_match=exact`
  without requiring the artifact to identify the edition/transcription or its source.
  The repaired gate now also requires non-empty `edition_label` and `source_reference`
  alongside exact match, legal basis and the harness-computed raw digest.
- Added regression coverage proving that either missing identity field keeps exact
  integer comparisons `unresolved`; lexical-display preservation and decimal
  `unresolved_precision` behavior are unchanged.

## 2026-09-12 — Deterministic dialogue profile candidate

- Added `scriptorium-dialogue-v1`, classifying LF-delimited paragraphs as dialogue only
  when their first content is an explicit dash marker followed by whitespace.
- Added normalized-text dialogue/narration spans and inspectable candidate author-remark
  spans based on alternating internal whitespace-dash-whitespace separators.
- Versioned the metric artifact as `scriptorium-metrics-v2` /
  `scriptorium-deterministic-metrics-v2` and added the four FantLab dialogue scalars.
- Made dialogue share and author-text-inside-dialogue denominators explicit as
  non-whitespace character ratios; all four FantLab-shaped fields remain `inferred`.
- Extended the benchmark harness from 18 to 22 implemented FantLab fields; dialogue
  decimal comparisons remain `unresolved_precision` until display precision is proven.
- Added golden coverage for offsets, marker handling, author remarks, empty denominators,
  schema identity and benchmark exposure; the authored reconstructed suite passed 33/33.
- Added a second public derived showcase from two dialogue paragraphs of *Anna Karenina*,
  Part I, Chapter II, bound to Russian Wikisource `oldid=4929731` and the cited Nauka
  1970 edition. Source prose is not committed; the 250-character slice is explicitly
  non-corpus and non-parity evidence.

## 2026-09-13 — Deterministic vocabulary profile candidate

- Added `scriptorium-vocabulary-v1` with case-folded lexical identities over the existing
  deterministic word-token stream; no lemmatization or undocumented `ё` folding is
  guessed into compatibility behavior.
- Added six FantLab-shaped vocabulary rows and versioned the aggregate artifact as
  `scriptorium-metrics-v3` / `scriptorium-deterministic-metrics-v3`; the artifact now
  contains 29 rows total, including the Scriptorium sentence-count extension.
- Kept unique vocabulary available without external dependencies while making active
  dictionary, active non-dictionary and UASZ values `null` unless an explicit dictionary
  lexeme collection and profile identity are supplied together.
- Bound supplied dictionaries to a canonical normalized-lexeme SHA-256 and lexeme count,
  preventing a reused profile label from silently hiding different dependency contents.
- Implemented inferred UASZ-3000/10000/100000 scalars as arithmetic means over every
  complete contiguous N-token window at one-token step, using an O(words) rolling
  frequency counter and excluding incomplete tails.
- Extended the benchmark mapping from 22 to 28 FantLab metric IDs. Dictionary-free unique
  vocabulary can use the source-provenance gate; dictionary-dependent rows remain
  `unresolved` even with a supplied dictionary because FantLab's production dictionary
  identity/version is still unproven.
- Preserved the frozen comparison-v1 rule that missing UASZ values remain
  `unresolved_precision`/`unresolved`, while missing integer dictionary counts are
  `not_run`.
- Added vocabulary/window/dependency and benchmark-admission tests plus public docs and
  README navigation. A local reconstruction covering the branch's existing regression
  surface plus the new vocabulary cases passed 44/44 checks, and the v3 schema validated
  artifacts both with and without an explicit dictionary dependency.
- Existing public showcase artifacts remain versioned historical outputs; no vocabulary
  values were fabricated from their hashes without re-reading the provenance-bound
  source selection.

## 2026-09-13 — Provider-neutral POS metric candidate

- Added `scriptorium-pos-v1` / `scriptorium-pos-metrics-v1` as a deterministic aggregation
  layer over one externally supplied pylem-style runtime-analysis sequence per
  `scriptorium-text-v1` word token.
- Bound every POS artifact to a non-empty runtime profile, the pinned
  `aot-pylem-0.0.18-to-fantlab-2022-v1` mapping contract and a SHA-256 of the canonical
  runtime-candidate matrix; this makes the aggregation input reproducible without
  pretending native pylem execution was verified in this unit.
- Resolve a token only when every supplied analysis belongs to the 15 direct runtime
  mappings and every mapped analysis agrees on one displayed FantLab bucket. Empty
  analyses, runtime `N`, the five unresolved extra AOT categories, unknown codes and
  cross-bucket homonyms stay undefined.
- Added defined/undefined counts and rates plus all 17 displayed bucket counts and
  percentages of defined words. FantLab's service-word aggregation remains explicit
  `unresolved` null data because its exact POS-to-service folding is not public.
- Added a complete 17×17 ordered POS-bigram matrix. The v1 candidate counts only resolved
  adjacent tokens inside the same Scriptorium sentence candidate and normalizes raw
  pair counts per 1000 total Scriptorium word tokens; an undefined token breaks a pair.
- Added positions 1..20. Based on FantLab's public “randomly selected sentence” wording,
  every position uses all Scriptorium sentence candidates as its denominator; sentences
  that are too short or undefined at that position add zero to bucket numerators.
- Kept the bigram adjacency and sentence-position denominator choices visibly inferred;
  source-matched benchmarks, not plausibility, must decide whether they match FantLab.
- Added focused tests for conservative mapping, empty input, ambiguity/unresolved cases,
  sentence-bounded bigrams, per-1000 normalization, all-sentence position denominators,
  alignment and the 20-position boundary. The reconstructed focused suite passed 9/9.
- Draft 2020-12 validation accepted both the POS schema itself and a generated artifact.
  A full branch suite is left for independent exact-head review because the execution
  container could not DNS-resolve GitHub for a repository checkout; GitHub connector
  reads and writes remained healthy.
- No source-matched benchmark or public analyzed-work showcase moved in this slice: M2
  remains 0/5, and no POS values were invented without provenance-bound source text and
  provider execution evidence.
- Independent review found that the runtime-candidate digest was not sufficient artifact
  provenance: identical candidate matrices and identical word/sentence counts can still
  correspond to different sentence segmentation and therefore different bigram/position
  metrics.
- Repaired the artifact contract by binding it to `scriptorium-text-v1` and SHA-256 of the
  exact normalized UTF-8 text, and froze both fields in the Draft 2020-12 schema while
  retaining the existing runtime profile/mapping/candidate identities.
- Added a segmentation-collision regression using `А Б. В Г.` versus `А. Б В Г.`: both
  inputs have the same runtime-candidate digest and counts but distinct normalized-text
  identities and distinct POS bigrams. The repaired focused morphology suite passes
  10/10 and a generated artifact validates against the repaired schema; independent
  exact-head/full-suite review remains required before merge.

## 2026-09-13 — Static GitHub Pages publication contract candidate

- Re-checked `SCRIP-MORPH-003` before selecting new work. Native/provider verification
  remains `not_run` because the current execution environment still cannot resolve
  GitHub/PyPI package hosts; this is a scoped environment blocker, not a pylem failure.
- Added `scriptorium-publication-manifest-v1` as an explicit allow-list between canonical
  repository artifacts and the future public Pages renderer. JSON elsewhere in the
  repository is not implicitly public just because it exists.
- Seeded the manifest with the two existing *Anna Karenina* showcase slices, preserving
  their historical metric schema versions and explicit non-corpus/non-benchmark status.
- Froze stable URL slugs, repository-relative artifact references, publication status,
  benchmark/corpus admissibility, compatibility claim, and `source_text_included=false`
  in a Draft 2020-12 schema.
- Defined fail-closed publication rules: paths may not escape the repository, an indexed
  showcase must say source text is not committed, and build-time remote book fetching is
  forbidden. Pages remains a renderer of derived/public metadata, not a redistribution
  channel for source prose.
- Chose a future custom GitHub Actions Pages flow based on current official GitHub
  guidance: checkout/build, upload the generated static directory as a Pages artifact,
  then deploy with the Pages deployment action. Generated HTML is disposable output and
  will not be committed as a second source of truth.
- Deliberately did not enable Pages or add a deployment workflow in this architecture
  unit. Deployment settings, action pinning and environment protection remain later
  reviewed work.
- Added standard-library contract checks for unique IDs/slugs, repo-relative paths,
  canonical showcase label agreement and the no-source-prose boundary. The seed manifest
  and schema also pass Draft 2020-12 validation locally.
- Independent review found that `compatibility_claim` was only schema-checked, so a
  manifest-only `mixed -> reproduced` edit could upgrade public evidence without changing
  the canonical showcase artifact.
- Repaired the boundary with executable fail-closed derivation from canonical per-metric
  `compatibility_status`: one uniform supported status remains that status, multiple
  supported statuses become `mixed`, and missing/unknown metric surfaces are rejected.
- Added a regression proving the current mixed Anna Karenina showcase cannot be relabeled
  `reproduced`, and documented compatibility-claim contradiction as a build-stopping
  safety failure. A future renderer must call this validation rather than trust the
  manifest string alone.

## 2026-09-13 — Deterministic static site renderer candidate

- Re-checked `SCRIP-MORPH-003` before selection. Native pylem/provider execution remains
  `not_run`: the execution container still cannot resolve GitHub or PyPI package hosts,
  while the connected GitHub API path remains healthy. The next dependency-satisfied
  unit was therefore `SCRIP-SITE-002`.
- Added `scriptorium-static-site-v1`, a standard-library renderer whose publication inputs
  are only `site/publication-manifest.json` and the canonical artifacts explicitly named
  by that manifest. Directory scanning and build-time remote fetching are absent by
  design.
- Implemented a deterministic root index plus stable `/works/<slug>/` work-showcase
  pages, shared CSS and a disposable `build.json` receipt containing the manifest and
  allow-listed artifact SHA-256 identities. No timestamps or local absolute paths enter
  generated output.
- Kept v1 deliberately narrow: reserved benchmark/author/tag kinds fail closed until
  their own canonical rendering contracts exist rather than inheriting guessed showcase
  semantics.
- Rendered only selected derived metrics and provenance metadata. Source-selection fields
  and source prose are not copied into HTML; artifact-controlled strings are escaped and
  provenance links are accepted only as credential-free HTTP(S) URLs.
- Revalidated canonical publication/admissibility labels and compatibility claims at
  build time and added runtime path containment, finite-number/unit/evidence checks, and
  output-target guards.
- Made refresh atomic at the validation boundary: all pages are validated/rendered before
  the previous output tree is replaced, while successful rebuilds replace the tree
  completely so stale pages cannot survive manifest removals.
- Added eight focused standard-library regressions covering deterministic bytes/routes,
  manifest-only selection, escaping, evidence/admissibility contradictions, source-text
  flags, traversal/unsupported-kind/URL rejection, non-finite values, symlink protection,
  failed-build preservation and stale-output cleanup. The authored focused suite passed
  8/8; full exact-head repository review remains for a later independent wake.
- Added public renderer documentation and ignored `/build/` output. GitHub Pages remains
  disabled; workflow/deployment/action pinning are a separate reviewed unit.
- Independent review found a fail-open contract gap: the renderer validated selected
  fields manually but accepted unexpected top-level/entry properties and an invented
  `artifact_schema` whenever the artifact repeated the same invented string.
- Repaired `scriptorium-static-site-v1` to enforce the exact manifest and entry key sets
  defined by `scriptorium-publication-manifest-v1` and to allow only the currently
  supported showcase profiles `scriptorium-deterministic-metrics-v1` and
  `scriptorium-deterministic-metrics-v2`. Future artifact schemas now require an explicit
  renderer-contract change rather than becoming publishable by string agreement alone.
- Added regressions for unexpected top-level manifest keys, unexpected entry keys and a
  synchronized `scriptorium-unknown-v999` manifest/artifact schema. The repaired focused
  renderer suite passes 11/11 plus `py_compile`; a later independent exact-head review is
  still required before merge.
- Independent repaired-head review reconstructed the full standard-library execution
  surface from the GitHub-published head and passed **74/74** tests. The canonical
  publication manifest and both showcase artifacts were used byte-for-byte for the real
  seed build.
- The real seed site was built twice with byte-identical output: one root page, two stable
  `/works/<slug>/` pages, shared CSS and `build.json`. A direct scan confirmed that none
  of the source-selection prose stored as provenance boundaries in either showcase was
  copied into generated HTML, while `mixed` compatibility and `not_admissible` labels
  remained visible.
- GitHub reported the reviewed head mergeable and strictly ahead of `master`; hosted
  statuses/workflow runs remained absent, so CI is still not configured rather than
  green. PR #29 was squash-merged as `73d4b8316f4b0a7fee94248b978732d0f5c1d4b5`
  and Issue #28 closed completed.
- GitHub Pages itself remains disabled. The next public-site unit is the separately
  reviewed Pages build/upload/deploy workflow; generated HTML must remain disposable and
  the merged fail-closed publication boundary must not be weakened.

## 2026-09-13 — Gated GitHub Pages workflow candidate

- Re-checked `SCRIP-MORPH-003` before selection. Native/provider provenance remains
  `not_run`: pylem is not installed in the execution environment and DNS resolution for
  GitHub/PyPI package hosts is still unavailable, while the connected GitHub API path is
  healthy. `SCRIP-SITE-003` was therefore the next dependency-satisfied queue unit.
- Opened Issue #30 and PR #31 for the first executable publication workflow over the
  merged `scriptorium-static-site-v1` renderer. This authoring run deliberately does not
  merge the workflow.
- Added a pull-request/relevant-master build job that uses Python 3.13, runs the complete
  standard-library test suite, builds only through `scriptorium.site_renderer`, rebuilds
  into a second disposable directory and requires byte-identical output before upload.
- Upload scope is exactly `build/site`; canonical JSON artifacts and source-selection
  provenance remain repository inputs and are not packed as a broader directory tree.
- Kept workflow-level and build-job permissions at `contents: read`, disabled persisted
  checkout credentials, and isolated `pages: write` plus `id-token: write` to the deploy
  job.
- Pinned all GitHub-owned actions to reviewed full release-tag commits:
  `checkout` v7.0.1, `setup-python` v7.0.0, `upload-pages-artifact` v5.0.0,
  `configure-pages` v6.0.0 and `deploy-pages` v5.0.1. Current configure/deploy releases
  use the Node 24 action runtime.
- Made deployment depend on the successful build, target the `github-pages` environment,
  run only for `refs/heads/master` outside pull-request events, and require the explicit
  repository variable `SCRIPTORIUM_PAGES_DEPLOY_ENABLED=true`.
- The workflow does not call privileged Pages enablement and does not use a secret/PAT.
  Repository Pages source/settings and activation of the deploy interlock remain a
  separate administrator effect after independent code/workflow review.
- Added five standard-library workflow-contract regressions covering full-SHA action
  pinning, read-only build permissions/canonical renderer invocation, deploy gating,
  absence of secrets/privileged enablement, and upload scope. Focused authoring checks
  pass 5/5; hosted exact-head workflow execution remains required in the independent
  review before merge.
- Independent exact-head review inspected hosted run `34761422729`: Python 3.13.15 passed
  the complete **79/79** standard-library inventory, canonical build and byte-identical
  rebuild succeeded, the Pages artifact uploaded successfully, and deployment was skipped
  on the pull-request event as required.
- The downloaded Pages artifact matched GitHub's recorded SHA-256
  `ff1b3a1e1096ae97eb199a03f628ffa8ec66b983806658f3b626c44913c17a7b` and contained
  only generated `build.json`, the root index, two allow-listed work pages and shared CSS.
  Canonical showcase JSON was not packaged and explicit source-selection prose remained
  absent from the generated site; `mixed` compatibility plus `not_admissible` benchmark/
  corpus labels remained visible.
- Independently resolved every action pin to its stated official release tag and verified
  that the pinned configure-pages/deploy-pages actions declare Node 24. Current GitHub
  Pages guidance still matches the workflow's build artifact -> `needs` -> deploy shape,
  required `pages: write` / `id-token: write` permissions and `github-pages` environment.
- PR #31 was squash-merged as `cb2dbfff22cec99e2063f208916680eac8da3d4d` and Issue #30
  closed completed. The resulting master push run `34763894163` also completed successfully;
  build/upload passed and deployment stayed skipped because the explicit activation
  variable remains unset. Pages settings were not changed.
- Post-merge review identified a latent publication-freshness gap: the workflow path
  filters watch `showcase/**` but omit renderer-supported `benchmarks/**` and
  `public-artifacts/**`. The current seed manifest references only showcase artifacts, so
  no current page is stale, but Issue #33 / `SCRIP-SITE-004` now blocks Pages activation
  or publication-root expansion until trigger coverage is synchronized and regression-tested.

## 2026-09-13 — Pages publication-root trigger repair

- Repaired the publication freshness contract in `SCRIP-SITE-004`: both pull-request and
  `master` push filters now include every canonical renderer artifact root —
  `showcase/**`, `benchmarks/**` and `public-artifacts/**`.
- Added a regression that derives required trigger paths directly from the renderer's
  `_ALLOWED_ARTIFACT_ROOTS`, so adding renderer support for another canonical root without
  updating the workflow fails the test instead of silently creating a stale-deployment path.
- Independent exact-head review of PR #34 head
  `647f35fac3e895f5a3258949e87cc8d8195176ba` confirmed the branch was strictly ahead of
  `master`, permissions/action pins/upload scope/deploy interlock were unchanged, and
  hosted run `34766996476` passed **80/80** tests, canonical build, byte-identical rebuild
  and artifact upload while deployment remained skipped on the PR event.
- Independently downloaded artifact `10320628444`; the ZIP SHA-256 matched GitHub's
  `a86fd5da51bba2c857f79680c7d08f0bf780d46fec5096cfd74b0159942c5395` and its tar
  contained only generated `build.json`, root index, the two allow-listed Anna Karenina
  pages and shared CSS.
- PR #34 was squash-merged as `1c740d1cd4e5149b3ce7d6b270becce2cc4ade31` and Issue #33
  closed completed. The resulting master push run `34769895595` also completed
  successfully with build/upload green and deploy skipped because Pages activation remains
  unset.
- The trigger-repair blocker is closed. GitHub Pages activation is still a separate
  administrator effect; the next normal-flow bias returns to morphology/provider work
  when executable, otherwise source-edition/benchmark work. M2 remains 0/5 source-matched
  works.

## 2026-09-13 — Anna Karenina source-edition trace candidate

- Re-checked `SCRIP-MORPH-003` before selection. `pylem` is still not installed and the
  execution container still cannot resolve GitHub/PyPI package hosts, so native provider
  execution remains `not_run`; connected GitHub repository access is healthy.
- Selected `SCRIP-REPRO-003` and opened Issue #35 / PR #36 for the retained
  `tolstoy-anna-karenina-ru` candidate.
- Reconfirmed the FantLab 19 September 2022 target at 1,692,647 characters and 253,275
  words, while its public analysis surface still discloses neither source edition nor
  immutable analyzer-input bytes.
- Recorded FantLab creator evidence that the analyzer operates on works uploaded to the
  database. This makes the site's bibliographic edition list insufficient evidence for
  analyzer-input identity and prevents a false source match by edition resemblance.
- Inspected the current work-page TXT excerpt link and found that it redirects to a LitRes
  trial endpoint. The trace therefore marks its relationship to the 2022 analysis text
  as unproven and excludes it from source-edition evidence.
- Strengthened the legal/public transcription side: Russian Wikisource identifies the
  transcription via FEB as `Толстой Л. Н. Анна Каренина. М.: Наука, 1970. С. 5–684`,
  explicitly marks the literary work public domain, and exposes permanent work-index
  revision `3829834`.
- Identified the remaining immutable-identity gap precisely: the work index composes 239
  separately stored chapter subpages across eight parts, so pinning index revision
  `3829834` does not freeze the chapter text bytes. The new machine-readable trace records
  source identity as `partial`, not exact.
- Kept the reproduction gate fail-closed: `fantlab_source_edition_match=unknown`,
  diagnostic comparison inadmissible, M2 parity inadmissible, and M2 remains 0/5.
- The next evidence step is bounded and mechanical: revision-pin all 239 chapter
  subpages, freeze extraction/concatenation order, acquire those exact public-domain
  revisions and compute raw/normalized SHA-256 plus character count. Only then should a
  field-by-field diagnostic run; it remains diagnostic until independent evidence ties
  FantLab's uploaded analysis text to the same frozen source.

## 2026-09-13 — Independent review and merge: Anna Karenina source-edition trace

- Independently reviewed repaired PR #36 exact head
  `6ccdf1c4fbbd67622bdf8bcfa591d745cb9100ac`. The branch was strictly ahead of
  `master` by 8 commits and behind by 0; the five changed paths contain only candidate/
  provenance metadata plus project documentation/state, with no committed novel prose.
- Parsed both machine-readable JSON files successfully and reconfirmed the fail-closed
  state: `source_identity_status=partial`, `fantlab_source_edition_match=unknown`,
  `gate_ready=false`, `diagnostic_comparison_admissible=false`, and
  `m2_parity_admissible=false`.
- Fresh evidence checks on 2026-09-13 reconfirmed FantLab's 19 September 2022 analysis at
  1,692,647 characters / 253,275 words and re-followed the work-page TXT link through
  `getwork74152506.txt.zip` to the LitRes trial endpoint with `art=74152506`. The repaired
  trace correctly treats that redirect as a dated point-in-time observation, not stable
  analyzer-input identity.
- Rechecked the creator discussion supporting the uploaded-text-corpus distinction from
  bibliographic listings. Rechecked Russian Wikisource's FEB/Nauka 1970 source statement,
  explicit public-domain notice, permanent work-index `oldid=3829834`, and 239 chapter
  subpages across eight parts; the index revision still does not freeze those subpage
  text revisions.
- The exact head has no pull-request workflow run. That is expected for this
  corpus/docs/project-only change under publication-scoped CI and is not a green-CI claim.
- PR #36 was squash-merged as `26df4eb31455ade653f3cd5331213537cf1acd4f` and Issue #35
  closed completed. M2 remains 0/5 source-matched works.
- The next normal-flow ladder rechecks `SCRIP-MORPH-003` first. If native provider
  execution is still unavailable, `SCRIP-REPRO-004` freezes the 239 Wikisource chapter
  revisions plus canonical extraction/concatenation and candidate digests before any
  diagnostic comparison is allowed.

## 2026-09-13 — Independent review and merge: frozen Anna Karenina candidate

- Independently reviewed PR #38 exact final head
  `cf8ba3ee96ef8a0ffc267d8f848000ceee28e09b` after the prior version-contract blocker
  had been repaired. The branch was strictly ahead of `master` by 19 commits and behind
  by 0, and GitHub reported it mergeable.
- Verified that the expanded capture receipt remains
  `scriptorium-source-revision-manifest-v1` while the canonical source-free artifact is
  `scriptorium-source-revision-packed-manifest-v1`; the checked-in deterministic
  pack/decode path round-trips all 239 ordered chapter identities and validates captured
  identity SHA-256 `fea96e084c769dfdec3a5fd55cbce34b061336441ba6edec70ebc830f5f83779`.
- Exact-head hosted run `34788532663` used Python 3.13.15 and passed **92/92**
  standard-library tests, canonical Pages build, byte-identical rebuild and artifact
  upload; deployment was skipped on the pull-request event.
- Independently downloaded artifact `10327113653`; the ZIP SHA-256 matched GitHub's
  `c72670a56a1279895221524cc7ef9f22c805660232b1a210d1d4e1aa6661e6f6`. Its tar contains
  only generated `build.json`, root index, the two existing Anna Karenina work pages and
  CSS; neither the research receipt nor novel prose is published.
- The frozen public candidate identity is 1,705,605 characters / 3,072,993 UTF-8 bytes
  with raw and `scriptorium-text-v1` normalized SHA-256
  `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`.
  `fantlab_source_edition_match` remains `unknown`; diagnostic comparison is permitted
  only as diagnostic evidence, `m2_parity_admissible=false`, and M2 remains 0/5.
- PR #38 was squash-merged as `9790057ad6cc56d7dbe092099d6bd11fd84a8baa`; Issue #37
  closed completed.
- Post-merge selection recheck still finds no installed `pylem` and the execution
  container still cannot resolve `github.com`, so `SCRIP-MORPH-003` remains `not_run`
  rather than failed. The next dependency-satisfied unit is `SCRIP-REPRO-005`, which may
  run deterministic metrics against the frozen candidate only as diagnostic evidence.

## 2026-09-14 — Frozen Anna Karenina full-work diagnostic candidate

- Re-checked `SCRIP-MORPH-003` first. The execution container still has no installed
  `pylem`, and direct DNS resolution for GitHub/PyPI package hosts still fails, so native
  provider execution remains infrastructure `not_run`; the connected GitHub API path is
  healthy.
- Opened Issue #39 / PR #40 for `SCRIP-REPRO-005`. Added the 19 September 2022 FantLab
  work-270306 reference, exact pinned-revision replay, a fail-closed diagnostic runner,
  mocked/local regressions and a bounded hosted integration workflow.
- The replay path requests the 239 revision IDs already frozen in the canonical packed
  manifest and verifies each returned title, timestamp and MediaWiki SHA-1 before source
  prose is accepted. It then reconstructs the text in memory and requires the committed
  1,705,605-character / SHA-256
  `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205`
  composite identity before analysis.
- Hosted frozen-diagnostic run `34794221625` on authored analysis head
  `9ba8f36440b15fc41374209437048ae2e486d579` used Python 3.13.15, passed **95/95**
  standard-library tests, replayed the exact frozen source successfully and emitted only
  derived diagnostic evidence. No novel prose was committed or uploaded by that workflow.
- The same analysis head passed Pages run `34794221544`: tests, canonical build,
  byte-identical rebuild and artifact upload succeeded; deployment remained skipped.
- The first full-work diagnostic records 1,705,605 Scriptorium characters versus
  FantLab's 1,692,647 (+12,958 / +0.766%) and 269,358 Scriptorium words versus 253,275
  (+16,083 / +6.350%). This demonstrates that the observed gap is not only a displayed
  character-count difference, while still leaving source-edition mismatch as a live
  alternative explanation.
- Several values are numerically close — mean sentence length differs by -0.174
  characters and dialogue share by -0.145 percentage points — but these remain
  diagnostic resemblance, not parity.
- The highest-value deterministic gaps are author text inside dialogue (+21.372
  percentage points) and dash frequency (+20.894 per 1000 Scriptorium words). These now
  justify explicit follow-up units for dialogue-author-remark and token/dash semantics
  rather than heuristic tuning to a single unmatched text.
- Surface-form unique vocabulary is 33,373 versus FantLab's 12,770 (+20,603).
  Dictionary-dependent vocabulary metrics remain not-run/unresolved because FantLab's
  production dictionary identity is unknown and no substitute dictionary was supplied.
- Native POS actuals were deliberately omitted because pinned pylem/provider execution
  remains `not_run`; no values were manufactured from the provider-neutral contract.
- The committed diagnostic artifact keeps `status=diagnostic_only`,
  `fantlab_source_edition_match=unknown`, `m2_parity_admissible=false`, and M2 at 0/5.
  PR #40 remains open for a later independent exact-head review before any merge.

## 2026-09-14 — Independent review and merge: frozen Anna Karenina full-work diagnostic

- Independently reviewed PR #40 exact final head
  `e0337c05ba73f146c6aeee1cff1792cf27a1a261`; the branch was 12 commits ahead of
  `master`, 0 behind, mergeable, and contained only the diagnostic workflow, source-free
  benchmark artifacts, replay/diagnostic code, tests and repository-facing documentation.
- Freshly rechecked FantLab work 270306 and confirmed the 19 September 2022 public values
  used by the implemented general, dialogue, vocabulary and punctuation comparison.
- Exact-head hosted diagnostic run `34794669740` on Python 3.13.15 passed **95/95** tests,
  replayed all 239 pinned revisions and reproduced frozen SHA-256
  `1dcf2af815f6288099f77a038d873690fb0dc72edf81d2094fd29f3d5a30c205` while keeping
  `fantlab_source_edition_match=unknown`, `status=diagnostic_only` and
  `m2_parity_admissible=false`.
- The committed source-free summary remains explicitly bound to authored analysis head
  `9ba8f36440b15fc41374209437048ae2e486d579`; the exact final head independently
  reproduced the same numeric surface after normalization-profile validation was tightened
  to the actual `scriptorium-text-v1` constant, rather than trusting the manifest value.
- Exact-head Pages run `34794669749` succeeded with deployment skipped. After merge, the
  `master` push Pages run `34797281911` also completed successfully; Pages activation
  remains deliberately disabled.
- PR #40 was squash-merged as `46fdbf04a246f327cebe40e36816d1ee63c0c31e`; Issue #39
  closed completed.
- The merged diagnostic records +12,958 characters, +16,083 words, +21.372 percentage
  points author-text-inside-dialogue, +20.894 dashes per 1000 Scriptorium words and
  +20,603 unique surface vocabulary. Dictionary-dependent vocabulary remains
  not-run/unresolved and POS remains omitted because native pinned pylem execution is
  still `not_run`.
- M2 remains **0/5 source-matched works**. Post-merge runtime recheck still finds no
  installed `pylem`, and DNS resolution for `github.com`, `pypi.org` and
  `files.pythonhosted.org` still fails. The next dependency-satisfied unit after the
  mandatory provider recheck is `SCRIP-TEXT-004`.
