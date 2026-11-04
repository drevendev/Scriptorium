# White Guard pinned literary-body preflight (candidate only)

The existing reviewed 20-revision manifest pins the page/revision identities of
*Белая гвардия* but deliberately mixes **11 Paris/Concorde 1927** and **9
Moscow/Pravda 1989** chapter source families. It is **not** an admitted
single-edition text or a FantLab analyzer-input identity.

After installing the repository, from its root:

    python -m scriptorium.white_guard_delivery --offline
    python -m scriptorium.white_guard_body_preflight > white-guard-preflight.json

The first command validates the exact committed manifest **without fetching
prose**. The second performs a network request for only those 20 recorded
revisions, checks provider-reported identities, then tries the existing
scriptorium-wikisource-body-v1 extractor on each chapter in memory. It emits
a **source-free JSON** report to stdout: source family, chapter/revision,
wikitext character count/SHA-256, safe extraction status and candidate
body length/SHA-256 where the extractor can handle the actual markup.

CANDIDATE_ONLY means a parser produced nonempty text; it does **not** prove
complete narrative selection, historical print edition, copyright clearance
for a new source, or FantLab parity. UNSUPPORTED_MARKUP means the current
parser cannot safely extract that pinned page, not that the page is empty or
that its body has zero characters. No parser exception details or book prose
are printed. A missing, malformed or drifted pinned provider identity fails
the entire operation before issuing any receipt.

Candidate composite length/hash are supplied **only if all 20 chapters**
extract; otherwise they are null, not zero. Even a complete candidate keeps
literary_body_extraction_frozen=false, single_edition_identity=false,
fantlab_input_identity=unknown, m2_parity_admissible=false.
The 300,000-character threshold is a *separate* tentative size check and
never automatically admits this mixed-source work.

**Verification:** injected test fetchers are marked INJECTED_FIXTURE, not
VERIFIED_IDENTITIES. tests/test_white_guard_body_preflight.py uses synthetic,
source-free fixtures for all 20 chapters, source partition, partial failures,
provider inventory integrity and privacy. It does **not** prove the live
historical content has been extracted. Real provider execution and literary/
edition collation must be recorded separately after a successful run. Never
commit a raw wikitext response or full novel to GitHub or Pages.

## Hosted live evidence (independent of synthetic tests)

The read-only [White Guard pinned literary-body preflight workflow](../.github/workflows/white-guard-body-preflight.yml)
runs on a relevant pull request and supports manual `workflow_dispatch` once
the workflow is present on the default branch. It runs the existing synthetic
negative tests, then queries **only** the 20 recorded historical revision IDs
on a hosted runner. The job checks an explicit source-free JSON schema,
chapter ordering, 11/9 source-family partition, extraction statuses and all
non-admission flags before uploading a seven-day derived-only artifact named
`white-guard-body-preflight`. Its logs show chapter numbers and status
counts, not the manuscript or raw MediaWiki responses.

A workflow **failure** (including network/API throttling) means no validated
hosted receipt; it does not prove any chapter is unsupported. A successful run
distinguishes `CANDIDATE_ONLY` from `UNSUPPORTED_MARKUP` for each chapter,
but even 20 candidates do not prove narrative completeness, single-edition
identity, rights for a new source or FantLab parity. Inspect the actual run,
exact commit and receipt before recording a measured body claim. Local code
and fixture tests alone remain `REAL_PROVIDER_NOT_RUN`.
