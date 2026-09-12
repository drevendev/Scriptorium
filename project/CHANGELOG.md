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
- Both noun `С` and cardinal numeral `ЧИСЛ` render as runtime `N`. The public pylem Python
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
  dash/quote variants and opening-parenthesis counting, and kept every FantLab-shaped
  value `inferred` until source-matched benchmarks demonstrate parity.
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
