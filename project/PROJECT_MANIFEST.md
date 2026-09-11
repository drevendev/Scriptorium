# PROJECT_MANIFEST — Scriptorium

Created: 2026-09-11
Profile: engineering + research
Status: ACTIVE
CONTROL_FORMAT_VERSION: SCRIPTORIUM-1 (EndlessZen-derived)

## Outcome

A reproducible open-source literary-analysis system exists that can analyze arbitrary
Russian text, demonstrates field-by-field parity with the public FantLab linguistic
analyzer on a legally usable benchmark set, and then extends that foundation with
versioned author-voice profiles, profile comparison, richer literary metrics, work
metadata/tags and tag profiles. Published derived results are browsable on GitHub
Pages.

## Deliverable

The public repository `drevendev/Scriptorium` contains:

- a Python library and CLI for deterministic text analysis;
- a FantLab-compatibility profile with documented metric definitions;
- pluggable morphology with an AOT-lineage compatibility backend;
- a benchmark harness and machine-readable comparison artifacts;
- a provenance/licensing catalog for analyzed works;
- author-voice and tag-profile models;
- derived analysis records for admitted works;
- tests and CI;
- a static GitHub Pages site for browsing works, authors, tags and comparisons.

## Consumer

Humans use the CLI/library and GitHub Pages. Future autonomous runs consume repository
state, issues, PRs and benchmark artifacts and must be able to resume without chat
memory.

## Canonical project state

The repository is the durable project state for this deployment. `project/` owns the
manifest, queue and changelog. GitHub issues/PRs own repository-facing discussion and
review evidence. This is an intentional repository-native adaptation of EndlessZen;
there is no separate Drive project unless the user later requests one.

## Canonical write ownership

Normal semantic changes use issue -> branch -> PR. GitHub branch refs and expected PR
head SHAs provide conflict detection at merge. The hourly task is the intended single
worker, but provider-level scheduler serialization has not been independently proven;
therefore runs must re-read current refs/state immediately before mutation and must not
overwrite a newer state revision. Substantial PRs are authored and judged in different
runs.

## Mode selection

The authorized hourly task prompt supplies the current deterministic selection policy:

1. recover interrupted or review-ready work;
2. fix a failing required check or benchmark regression;
3. satisfy the current milestone gate;
4. execute the highest-priority unblocked queue unit;
5. perform a consumer/corpus/provenance review when its trigger is due;
6. report no executable work.

This deployment does **not** yet have an independent external EndlessZen mode controller
that persists a selection receipt before each run. Until one is bound and verified, the
worker applies the user-authorized deterministic ladder above and records this as a
known conformance gap rather than claiming mechanical mode selection. The worker may
propose a policy change, but it may not silently change this ladder; goal or gate changes
require a manifest amendment with a reason.

## Liveness

```text
CADENCE:           hourly
OBSERVER:          user / ChatGPT task UI
TOLERATED_SILENCE: 3 hours
```

A stopped worker cannot self-report liveness. Repository state records only committed
runs, never claims that the scheduler itself is healthy.

## Constraints

- Calibration, parity-benchmark and author-profile corpus works must be at least
  300,000 characters including spaces.
- The analyzer must accept shorter stories/excerpts and mark profile confidence or
  representativeness limits rather than rejecting them.
- Corpus texts require public-domain status, an explicit compatible open license, or
  explicit permission. Accessibility alone is insufficient.
- Full copyrighted texts are not stored in the public repository by default; derived
  analysis, provenance, source references and digests are.
- Different translations are distinct works and never share a text identity.
- FantLab parity is evidence-based. Public methodology is authoritative evidence for
  what is described, but unpublished know-how must not be guessed into a claim of
  exact reproduction.
- GitHub Pages must remain static/public-safe and must not expose secrets or unlicensed
  source text.

## Required sources

- https://fantlab.ru/article374 — public description of the analyzer and author-profile
  method.
- https://fantlab.ru/work488/lp — first concrete published metric reference.
- https://fantlab.ru/rating/work/lingvo — public metric/ranking surface.
- http://aot.ru/history.html and the maintained AOT code lineage.
- https://github.com/sokirko74/aot — original/open AOT implementation lineage.
- https://pypi.org/project/pylem/ and its source — Python wrapper candidate for the
  AOT compatibility backend.
- Legally usable text sources selected and recorded per corpus entry.

## Mandatory subsystems

Initial identifier areas are frozen as:

```text
SETUP   project control and repository process
INGEST  local/source metadata ingestion and provenance
TEXT    normalization, tokenization, sentence/dialogue segmentation
MORPH   morphology and FantLab POS-category mapping
METRIC  metric extraction and schemas
REPRO   FantLab benchmark/parity harness
VOICE   author-voice profiles and comparison
TAG     work tags and tag profiles
CORPUS  legally admitted work catalog and derived analyses
SITE    GitHub Pages publication
QA      tests, reproducibility, performance and release gates
```

Adding an area is a manifest amendment.

## Milestones and gates

### M0 — Recoverable project

Gate: a fresh worker can orient from repository state, find the queue, understand the
legal boundary and identify the next executable unit without chat history.

### M1 — Deterministic FantLab surface

Implement and document deterministic/public metrics first: character/word/sentence
statistics, sentence lengths, dialogue measures, vocabulary windows, punctuation,
POS distributions, POS bigrams and POS-by-sentence-position. Each metric has a schema,
unit, test and compatibility status.

Gate: the benchmark harness can compare expected vs actual values field-by-field and
preserve text/configuration provenance.

### M2 — Morphology compatibility and parity corpus

Use the AOT lineage as the first compatibility target, reverse-engineering only what
public evidence and benchmark behavior justify.

Gate: at least five independent legally usable works of at least 300,000 characters,
with matching FantLab analysis and a traceable source edition, reproduce all published
compatibility metrics exactly after FantLab's displayed rounding. A work whose source
edition is not established cannot satisfy this gate. Any unexplained delta keeps the
gate open; the user may explicitly change this requirement if public information makes
exact parity impossible.

### M3 — Author voice

Implement author profiles from multiple works using word-count-weighted means and
weighted standard deviations as publicly described by FantLab, feature weighting,
comparison and short-text uncertainty reporting.

Gate: profile construction is reproducible, cross-validation is recorded, and
translation identity is preserved.

### M4 — Extended literary analytics and tags

Add versioned extension metrics and multi-label work tags, then aggregate tag profiles
without mixing them into FantLab-compatible fields.

Gate: extension metrics are documented and tested; tags have provenance/confidence;
tag profiles are reproducible from work artifacts.

### M5 — Public corpus and Pages

Publish derived analyses and comparison views. Diversify beyond 19th-century classics
and genre fiction toward modernism/postmodernism, translated works, nonfiction
(especially popular science), and contemporary/online fiction where rights permit.

Gate: GitHub Pages builds from repository artifacts; corpus/license checks are clean;
at least 30 works meet the >=300,000-character corpus rule and diversity is explicitly
reported rather than implied.

## Quality rules

- Same input bytes + same compatibility profile + same dependency versions produce the
  same normalized artifacts.
- Every published result names analyzer/config version and source digest.
- Compatibility metrics never silently change definition.
- No benchmark is called passing without source-edition confidence and recorded deltas.
- Tests distinguish parser logic, morphology behavior, metric formulas and rendering.
- Extensions cannot alter compatibility output unless the compatibility profile itself
  is deliberately versioned.

## Simplification principles

Prefer a small deterministic Python core and machine-readable JSON artifacts. Keep the
web layer static and downstream of analysis. Avoid a database until corpus size or
query requirements prove that flat/versioned artifacts are insufficient. Do not add ML
to reproduce a metric that can be expressed deterministically.

## Prohibitions

- No unlicensed corpus scraping or repository redistribution.
- No bypassing access controls, paywalls or platform terms.
- No claiming hidden FantLab coefficients were recovered without evidence.
- No training/profile corpus entry below 300,000 characters.
- No treating two translations as the same text/work.
- No publishing private/user-supplied text without explicit authorization.

## Completion

`v1` is complete when M0-M5 gates are all satisfied, there are no critical blockers,
CLI/library/site documentation is sufficient for a new user, and CI/release artifacts
are reproducible. After v1, corpus expansion and research may continue as an ongoing
curation programme until the user stops or changes scope.

## Amendments

| Date | What changed | Why |
| --- | --- | --- |
| 2026-09-11 | Initial manifest | User commissioned the project and hourly autonomous development. |
| 2026-09-11 | Record mode-controller conformance gap | Bootstrap review found that the deployment has an authorized deterministic ladder but no independently verified external selection receipt mechanism. |
