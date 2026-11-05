# White Guard Paris 1927 — retained Page revision identities

The metadata-only GitHub Actions capture from [run #41959859796](https://github.com/drevendev/Scriptorium/actions/runs/41959859796), artifact `13383909900`, commit `1eb66bc069a02c3997b65330930931e29aacf88b`, was downloaded and independently inspected. Its source-free `paris-page-identities.json` is SHA-256 `baf64a30cad23740dd0a6a1d51599f6bb7343f99922cf87efcd658f08042dc0f`, with 185 distinct Page identities covering scan pages 5–189, grouped by the eleven pinned Paris chapters.

The durable, reviewable `corpus/candidates/white_guard_paris_1927_pages.csv` retains the exact page number, Page ID, current-at-capture revision oldid, UTC timestamp, and MediaWiki SHA-1 for each of those 185 dependencies. Its UTF-8 byte SHA-256 is `f2f2ea90a65ffb99b5cd12e64f20c15f16f6a2d7ca600cd7084488f311f81c02`. Page titles are derived deterministically from the **existing** `PAGE_PREFIX`; chapter ranges from the reviewed `EXPECTED_RANGES`.

Offline verification (no network):

    python -m scriptorium.white_guard_paris_manifest

Online recheck of the *same* captured oldids and SHA-1 (metadata only; fail closed):

    python -m scriptorium.white_guard_paris_manifest --verify-provider

The receipt explicitly reports `NOT_RUN` for offline replay; passing offline validation never implies successful fresh provider replay. Errors issue no partial receipt and suppress potentially sensitive exception text.

**Scientific boundary:** The 185 individual page revisions were collected as *current* revisions in separate MediaWiki batches; that collection is not an atomic historical transclusion. Historical revision selection, ProofreadPage rendering, header/footer selection, book-body extraction, the >=300,000-character gate, and FantLab source identity remain unresolved. This is metadata only; it is neither a measured 1927 text nor M2 progress (still 0/5). The 1989 edition is not combined with it.
