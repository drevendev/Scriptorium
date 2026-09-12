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

## 2026-09-11 — AOT/pylem compatibility candidate

- Pinned `pylem==0.0.18` by package version and published sdist SHA-256, plus the
  repository revision that declares 0.0.18 and its exact `morph_dict` and `pybind11`
  submodule revisions.
- Recorded the distinction between an immutable PyPI artifact hash and the weaker
  repository-version match because PyPI metadata does not encode the Git commit used to
  build the uploaded sdist.
- Added a machine-readable AOT POS mapping with 17 direct semantic counterparts on the
  observed `fantlab-2022-v1` work surface.
- Required unresolved overrides before direct mapping for `ИНФИНИТИВ`, short adjectives
  (`П + кр`) and short participles (`ПРИЧАСТИЕ + кр`); postpositions and phrasal verbs
  remain unresolved derived categories.
- Refused to invent a FantLab homonym/disambiguation policy: pylem can return multiple
  analyses, so the future adapter must preserve ambiguity until benchmarks justify a
  deterministic selection rule.
- Kept pylem/AOT dictionary equivalence to FantLab 2022 explicitly unproven.
- Native build verification remains pending because the execution container could not
  resolve external package hosts; this was recorded as an environment limitation, not a
  pylem failure.
