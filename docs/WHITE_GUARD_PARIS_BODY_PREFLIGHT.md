# White Guard Paris 1927 — pinned Page body candidate preflight

The reviewed CSV in `corpus/candidates/white_guard_paris_1927_pages.csv`
permanently pins 185 *current-at-capture* Page oldids for scan pages 5–189.
This experiment fetches **exactly those revisions**, using the existing
`wikisource_replay.fetch_pinned_chapter_revisions` checks for title, Page ID,
revision ID, timestamp and MediaWiki SHA-1. All raw Page text remains in memory.

Run the offline synthetic regression suite:

```sh
python -m unittest discover -s tests -p 'test_white_guard_paris_body_preflight.py' -v
```

Run a **real network** preflight (185 pinned oldids, not current Page state):

```sh
python -m scriptorium.white_guard_paris_body_preflight > paris-body-receipt.json
```

Do not save or print upstream Page contents or full exception messages.
A provider/identity failure aborts without a receipt; each parsed Page emits
only a fixed status, page/chapter number, revision oldid and optional
candidate length/SHA-256. The GitHub Actions workflow
`white-guard-paris-body-preflight.yml` validates a fixed, source-free schema,
reports coverage and retains only that report for seven days.

This **v1 conservative candidate projection is NOT ProofreadPage rendering**.
It removes at most three balanced outer `<noinclude>` regions, while refusing
interior noinclude, templates, HTML, wiki links, headings, apostrophe styling,
line-start lists/indents and horizontal rules, oversized or empty pages. An accepted plain-text Page is a **candidate**, not a verified historical
render: page headers/footers and text joining (a provisional newline), scan
collation, historical parent revision, section semantics and source edition
matching still need independent evidence. No unsupported markup is silently
stripped. Per-chapter candidate length/hash is null if **any** Page fails;
all 11 chapters remain part of the distinct 1927 source family, never stitched
to the unrelated 1989 chapters.

An experiment that produces `CANDIDATE_ONLY` for all 185 pages is *still not*
an admissible frozen literary body or a proof of historical transclusion. No
book text is committed or uploaded, no `>=300,000` corpus admission is
declared, FantLab input remains UNKNOWN and M2 remains **0/5**.

Primary reference for `<pages />` and Page inclusion semantics:
https://www.mediawiki.org/wiki/Help:Extension:ProofreadPage/Pages_tag/en .
