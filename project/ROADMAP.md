# Scriptorium roadmap and repository assessment

Updated by the owner-requested cleanup on 2026-10-18. This document defines strategic
acceptance; `STATE_AND_QUEUE.md` alone owns execution order. PR/check/merge/deployment
status is always native GitHub evidence, not a manually maintained duplicate ledger.

## Assessment

**The main bottleneck is delivery convergence, not a missing analyzer foundation.**
The repository already has deterministic metric families, pinned morphology research,
source-free evidence and tested rendering primitives. #268 and #272 were accepted on
their unchanged exact heads (22 successful workflow runs each) and merged into master.
The offline frozen report and its canonical route no longer need another implementation.

The useful local analyzer in #270 was not mergeable as-is: its latest review identifies
unbounded special-file reads and path-disclosing errors. #274 already incorporates fixes,
CSV, readable labels and wheel packaging, but its newer atomic-publisher change left a
syntax error in `site_renderer.py`. Its observed head had 8 successful and 15 failed
workflow runs. The successor #275 adopts that existing implementation rather than replacing
the public API with an isolated subset. It also preserves the three unique files from the
un-PR'd two-work gallery branch.

The publisher's mkdir lock survived process death and could block all later builds.
A reproduced crash test now motivates a persistent regular-file/kernel lock; replacement
remains atomic and first publication remains no-clobber. Linux support is explicit rather
than claiming cross-platform site publication. Orphaned old staging directories and legacy
directory locks are not automatically deleted while ownership could be ambiguous.

**Public presentation and scientific completion are separate gaps.** The canonical site
has five evidence routes; the two-work gallery is still offline. Repository metadata reports
`has_pages=false`, so building a site is not a live deployment. M2 is still 0/5 because no
retained work establishes the required FantLab analyzer-input identity. More polished UI,
large legal source texts or approximate numeric matches do not close that gate.

**Repository hygiene needs focused follow-through.** Master is protected by a PR/no-force/
no-delete ruleset, but the observed ruleset does not require named CI checks or resolved
threads. #265 owns that administration/deletion scope. The root has no LICENSE file and
repository metadata reports no detected license; settle an explicit code/data licensing
and attribution policy before advertising a broadly reusable release. Do not infer a
license from public visibility or silently relicense contributors/dependencies.

## 1. Reader 0.2 — finish one release path

Scope: #275, #269 and #273. Preserve #268/#272's landed work; adopt #274's Reader and the
unfinished gallery, repair syntax/crash recovery and maintain one active successor branch.
Do not keep adding disconnected ZIP-only features.

Acceptance: all applicable exact-head CI passes; the complete canonical suite and
syntax check run; a built wheel is installed in a clean environment outside checkout;
`scriptorium analyze` produces valid JSON/HTML/CSV with all 29 rows, bounded private input
and create-only reports; diagnostic and five-route site commands work; canonical builds
are byte-identical; the installed gallery produces deterministic HTML/CSV. Negative tests
must retain private-path, special-file, tampered-evidence and publication-failure behavior.

A later fresh acceptance may merge the successor and then close superseded #270/#274 only
with preservation proof. Do not self-approve or merge freshly authored repairs. Verify the
new master checks separately. This preview does not authorize package-registry publication.

## 2. Public full-work results — a useful real showcase

Integrate the already-frozen Grin and Beketova results into the canonical publication path,
not a decorative dashboard or corpus-candidate research page. Keep translation identity,
source JSON/body hashes, scientific labels and exact units visible. Publish only supported
metric rows; absolute totals are not normalized style scores.

Acceptance: explicit digest-pinned allow-list and route registration, working homepage/list/
detail/back links, HTML plus source-free machine-readable download, labeled charts and exact
tables, no arbitrary artifact discovery. Exercise real desktop/mobile/keyboard flows and
inspect screenshots in a permitted browser. Malformed data/build failure preserves the last
valid site. Distinguish local build, CI artifact, deployment and live verification. A Pages
configuration blocker affects only the last two stages, not implementation.

## 3. Trustworthy comparison — one shared contract

Selectively adopt the pending comparison CLI/Comparison Desk work after checking canonical
Reader compatibility. Avoid independently hand-maintained Python/JavaScript registries.
A shared versioned declaration should define metric IDs, methods, units, dictionary-dependent
fields and valid status transitions. Imported declarations are untrusted input, not proof.

Acceptance: actual Reader JSON -> comparison -> browser -> CSV/JSON round trip; unknown,
unavailable, unregistered and incompatible fields remain distinct; no delta for an
incomparable row. Test decimal arithmetic, stale import races, strict UTF-8, size limits,
dictionary identity, method/unit/status tampering, formula-like text and data privacy.
Keep benchmark diagnostics separate from author-profile claims. No external manuscript
transmission or new service is needed.

## 4. Morphology and benchmark evidence — resolve a measured uncertainty

Use the pinned AOT/pylem lineage for a bounded noun/cardinal ambiguity experiment, then
expose the affected POS distribution/bigram/sentence-position deltas. Reuse existing primary
source/provenance research; do not silently substitute another backend or invent FantLab's
unpublished coefficients. Add a new experimental consequence, not another link inventory.

Acceptance: pinned toolchain/dictionary/source identities, positive and ambiguous fixtures,
expected/actual/delta output and an explicit mapping/version decision or narrowly actionable
remaining question. The experiment remains diagnostic until compatible behavior and source
identity are independently demonstrated.

Build one inspectable cross-work readiness report from existing admitted/frozen evidence:
rights, >=300k size, source-edition identity, input identity, reference date, required fields,
rounding rules, NOT_RUN and unresolved deltas. Tests must prove source-unmatched works cannot
be promoted to parity. Use this to choose the next genuinely executable corpus/source task;
do not repeat unchanged Perelman/Darwin metadata investigations.

## 5. Reproducibility, release hygiene and later profiles

Keep the deterministic library/CLI separate from evidence ingestion and presentation.
Add measured performance/installation regressions before architectural rewrites. Consolidate
repeated broad CI execution only after mapping every old assertion to retained coverage;
research-specific triggers and a clear core/package/site acceptance check should reduce
noise without weakening gates. Required-check settings remain #265's administration scope.

Resolve explicit code license, data attribution and dependency notices before a broad public
release. Inspect legacy branches for unique content and active stack dependencies; supported
deletion needs fresh exact-head proof, never ref overwrites or forced history changes.

Author-voice and tag-profile work follows its own M3/M4 acceptance: multiple sufficiently
large legal works, reproducible weighting/uncertainty/cross-validation and distinct translator
identities. Any earlier extension preview must be labeled and independently validated.
M5 still needs at least 30 eligible diverse works plus its publication/license gates.

## Definition of progress

A working command, tested defect fix, accepted earlier PR, reproducible evidence delta or
usable real-work page is progress. Repeated unchanged reviews, wake counters, administrative
waiting and more unintegrated prototypes are not. No item above changes the mission,
corpus floor, M2 equality/rounding requirements, privacy boundary or perpetual hourly job.
