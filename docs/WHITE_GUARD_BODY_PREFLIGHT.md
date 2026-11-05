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

## Structural failure diagnostics (receipt v2)

The previous hosted replay identified 5 tentative candidates and 15 unsupported
chapters, but the v1 receipt could not distinguish *why* the 15 were rejected.
The v2 receipt adds `extraction_failure_code` to each chapter (null when
`CANDIDATE_ONLY`). Known, source-free codes are:

- `BODY_CONTAINER_ABSENT`: no recognized transcription div.
- `BODY_CONTAINER_MULTIPLE`: more than one recognized transcription div.
- `UNSUPPORTED_TEMPLATE`: at least one template remains after conservative transforms.
- `TABLE_OR_HEADING`: unhandled table/heading syntax remains.
- `UNSUPPORTED_INLINE_MARKUP`: unhandled HTML or wiki-link syntax remains.
- `PROOFREADPAGE_UNPINNED`: `<pages />` transcludes Page-namespace text whose
  revisions have not been frozen as part of this literary body.
- `EMPTY_BODY`: recognized body yields no selected text.
- `UNCLASSIFIED_ERROR`: any other parser error, invalid result, or unknown
  injected diagnostic code; never serialize exception messages.

## Source-free ProofreadPage route plan (receipt v3)

On 2026-11-05, the **current** Wikisource edit-source view of Paris chapter 1
shows a `<pages index="Дни Турбиных (Белая гвардия) (Булгаков, 1927).djvu"
from=5 to=9 />` transclusion inside its transcription div. This view is **not**
evidence that pinned `oldid=2423390` has identical content; the pinned
provider replay must establish that independently. See the [live page edit
source](https://ru.wikisource.org/w/index.php?title=Белая_гвардия_(Булгаков)/Глава_1&action=edit)
and the [official ProofreadPage `pages` tag contract](https://www.mediawiki.org/wiki/Help:Extension:ProofreadPage/Pages_tag/en).

The extractor must **never** drop `<pages />` and count the empty parent as
literary prose. Receipt v3 reports `PROOFREADPAGE_UNPINNED`, plus an optional
`proofreadpage_page_plan` only when the *pinned* Paris source has exactly one
recognized text div containing exactly one whitelisted, unmodified `<pages />`
route (index title, positive numeric `from`/`to`, at most 100 Page numbers).
Other indexes, steps, section selectors, excludes, multiple routes, mixed body
text and malformed ranges stay unsupported with a **null** plan. All plans
remain **UNFROZEN** topology hints, never actual Page revision identities,
verified page content, a render-equivalent body or copyright clearance.
The v2 synthetic and hosted receipts remain historical evidence, not updated
in place. A new exact-head hosted replay must establish observed v3 plan counts.

### Verified pinned-range replay — 2026-11-05

The [exact-revision hosted run #41945016706](https://github.com/drevendev/Scriptorium/actions/runs/41945016706)
on initial PR #430 head `5da7380692f114805cb531f40eabd3cc8fb417c0`
completed successfully, including 12 focused synthetic tests and all 20
pinned-revision identity/readback and source-free schema validations.
All **11/11 Paris chapter parents** have the exact whitelisted tag shape.
The Page-number ranges in chapter order are:

`5–9; 10–32; 33–52; 53–61; 62–80; 81–112; 113–124; 125–138; 139–148; 149–164; 165–189`.

These are **185 contiguous Page-number dependencies** in the declared 1927
index, with no gaps or overlaps in this *syntactic* topology. The other nine
1989 chapters remain five tentative bodies and four unsupported templates.
Overall candidate-body coverage remains **5/20** and the composite stays
null. No Page: revision IDs, immutable Page: content, Index: revision, complete
rendering, text/body size or FantLab source identity are established. This
source-free evidence is not a frozen or analyzed edition; M2 remains **0/5**.
The original run supports the code at its original head; later documentation
commits require their own current-head CI before merge.

The independent next task is to resolve every Page-namespace dependency at
its own immutable revision/MediaWiki SHA-1 and decide page-boundary/section
semantics before experimenting with a *separate*, versioned transclusion
renderer. Historic parent oldids alone cannot freeze the content transcluded
from Page namespace; current render output is not automatically deterministic.

This classifies parser *rejection*, not the correct literary body or print
edition. No raw wikitext, exception string, prose fragments, or manuscript
content are emitted. It does not loosen the v1 parser or admission rules.
The pre-existing v1 receipt remains historical evidence; new category counts
require a successful **new exact-revision hosted run** and are NOT_RUN at PR
creation. Use the category counts to select a reviewed, source-specific fix
rather than guessing whether every chapter shares the same structure.


## Paris Page revision identity capture (separate, source-free unit)

The 11 **historically pinned parent chapters** have already yielded a
ProofreadPage route plan covering exactly 185 Page numbers, 5–189. The
`scriptorium.white_guard_page_freeze` module captures a **new snapshot
of current Page-namespace revision identities**, not the state of the
transcluded pages when the parent chapters were edited. The source
family is strictly Paris/Concorde 1927; none of the Moscow/Pravda 1989
chapters enters this inventory.

To capture and immediately replay current Page identities:

    python -m scriptorium.white_guard_page_freeze capture --manifest paris-page-identities.json
    python -m scriptorium.white_guard_page_freeze replay --manifest paris-page-identities.json --receipt paris-page-replay.json

The capture records exactly one Page title, revision ID, UTC timestamp,
MediaWiki SHA-1, and permanent oldid URL per scan-page dependency.
It records the capture time and explicit current-revision basis, and
rejects missing, extra, duplicate, malformed and untrusted identities.
The replay verifies that all 185 historical revision IDs still resolve
to the exact recorded titles, timestamps and SHA-1 hashes. No page
content, OCR, transclusion output or full prose is requested by these
metadata calls or written into either JSON artifact.

The [Paris Page identity workflow](../.github/workflows/white-guard-paris-page-revisions.yml)
first revalidates the exact 20 pinned parent sources and the 11 expected
routes; only then does it capture/replay Page identities and retain a
seven-day metadata-only artifact. A successful workflow creates an
**ephemeral, source-free frozen-identity candidate**. It does not on
its own commit a stable manifest, freeze a complete literary body,
establish the Paris book/scan collation, establish the source version
FantLab analyzed, or satisfy the >=300,000-character admission gate.
Any failed historical route validation stops the capture rather than
silently switching to current parent markup.

After a successful hosted capture, independently validate the artifact,
commit the verified identities through a later PR, and implement a
separate versioned Page-content renderer with page-boundary and header/
footer treatment backed by explicit reproducible tests. Never reuse the
current rendered parent HTML as if it were oldid-pinned source text.
