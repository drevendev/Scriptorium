# Scriptorium agent instructions

These rules govern autonomous work in this repository.

## Mission

Build Scriptorium end to end: first reproduce the publicly observable FantLab
linguistic analysis as faithfully as evidence permits, then extend it with author-voice
profiles, profile comparison, additional literary metrics, tagging and tag profiles,
and a browsable GitHub Pages publication.

The project uses `drevendev/EndlessZen` as its operating discipline. Every wake is
stateless: orient from repository state, perform one bounded unit, verify it, and leave
a recoverable durable result.

## Repository scope

`drevendev/Scriptorium` is this worker's development target. A bounded run advances
Scriptorium; it does not become a maintenance run for the framework or another project.

`drevendev/EndlessZen` is a read-only operating-model reference for this worker. Do not
patch it, create branches or pull requests there, review or merge its pull requests, or
otherwise maintain it from the Scriptorium task. If Scriptorium work exposes a genuine
EndlessZen defect or reusable framework improvement, check that repository's current
contributor rules and open/closed issues, then report the finding as an Issue for its own
maintainers. Reporting that finding does not replace the Scriptorium unit for the run.

Other repositories may be inspected read-only when needed for Scriptorium research,
source provenance, dependency evaluation, or comparison. Do not turn that inspection
into unrelated repository development.

## Durable state

Read these before selecting work:

1. `project/PROJECT_MANIFEST.md`
2. `project/STATE_AND_QUEUE.md`
3. `project/CHANGELOG.md`
4. the issue or PR named by the selected unit

Repository files, issues, pull requests, checks, benchmark artifacts and comments are
project memory. Chat memory is never authoritative.

## Authority and workflow

The user authorized end-to-end repository development. You may research, create and
update issues, create branches and commits, open and review pull requests, refactor,
merge safe pull requests, maintain CI and GitHub Pages, and update project state.

Normal mutation path after bootstrap:

```text
issue -> branch -> pull request -> independent later review -> merge
```

Do not merge a substantial PR in the same run that authored its substantive changes.
A later run may review and merge it when evidence and checks support doing so. Small
mechanical recovery/bookkeeping fixes may be handled directly only when the current
repository policy makes a PR disproportionate and the change cannot alter analyzer
semantics.

Never force-push a shared branch, weaken a security gate, change repository visibility
or administration, spend money, or access credentials that were not explicitly made
available. Use the connected GitHub identity as itself; never impersonate another user.

Repository-facing prose, issue bodies, PRs and commits are written in English.

## One run, one bounded unit

A run must finish one named unit that is small enough to verify. Recover interrupted
work before selecting new work. Prefer the highest-priority executable unit in
`STATE_AND_QUEUE.md`; do not invent a different priority because it is more interesting.

Research is work only when it changes a requirement, decision, test, benchmark, source
record or queued unit. A list of links is not a completed research unit.

A blocked run records the precise blocker and the evidence or event that would reopen
the unit. Never turn unknown into zero or not-run into passed.

## FantLab fidelity rules

Keep three classes distinct in code, docs and Pages output:

- **reproduced** — behavior is demonstrated against a FantLab benchmark;
- **inferred** — behavior is a documented reconstruction from public evidence;
- **extension** — Scriptorium behavior that is not claimed to match FantLab.

FantLab states that some corrective coefficients and implementation details are
unpublished. Therefore resemblance is not parity. A compatibility metric closes only
when benchmark evidence satisfies its declared equality/tolerance rule.

The first compatibility target is the 19 September 2022 FantLab analysis of Henry Lion
Oldie, `Шутиха`, recorded in `benchmarks/fantlab/work488.json`. It is a public numeric
reference, not a licensed corpus text.

For FantLab compatibility, prefer the AOT lineage for morphology. `pylem` is the first
implementation candidate because it wraps the original AOT C++ morphology family. A
newer tagger may be used for Scriptorium extensions, but must not silently replace the
compatibility backend.

## Corpus and copyright boundary

Calibration, benchmark and author-profile corpus entries must contain at least 300,000
characters including spaces. The analyzer itself must accept shorter works and excerpts
and report that short-input author/profile estimates are less representative.

Admit a corpus text only when provenance and legal use are clear: public domain, an
explicit open license, or explicit permission from the rightsholder/site for the use we
perform. Web accessibility is not permission.

Treat every translation as a distinct work with its own translator, edition/provenance,
text digest and analysis result. Do not collapse translations into the source work.

Do not commit copyrighted full text by default. Store metadata, license/provenance,
source references, immutable digests, analyzer version and derived analysis artifacts.
Local user-supplied text may be analyzed without becoming part of the public corpus.

Author.Today and fanfiction sources are candidates only when their specific text/license
or permission supports the intended processing/publication. Do not scrape around access
controls or assume a platform-wide license.

## Verification

Analyzer changes require tests for the behavior changed. Compatibility changes also
update or run the relevant benchmark comparison. A benchmark records:

- source/edition identity and legal basis;
- raw and normalized text digests;
- character count including spaces;
- analyzer version/configuration;
- FantLab reference URL/date;
- expected value, actual value and delta per metric.

If the exact text edition behind a FantLab result is not established, the comparison is
diagnostic, not a parity proof.

GitHub Pages contains derived analysis and provenance, not unlicensed book text.

## Design bias

Keep the core deterministic and testable. Separate ingestion, normalization,
tokenization, dialogue detection, morphology, metric extraction, profile modeling,
benchmarking and presentation so a FantLab-compatibility decision can be changed
without rewriting unrelated layers.

Prefer explicit schemas and versioned compatibility profiles over hidden heuristics.
When evidence is insufficient, make uncertainty visible in the artifact rather than
burying it in code.
