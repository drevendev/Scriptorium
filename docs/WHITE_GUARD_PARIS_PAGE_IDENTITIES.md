# White Guard Paris 1927 Page: revision identity capture

The 11 exact historical chapter revisions replayed by PR #430 describe 185 contiguous
ProofreadPage dependencies (scan pages 5–189). They **do not** pin the content or
revision of any transcluded Page: page.

Run from the repository root:

    python -m scriptorium.white_guard_page_identities > /tmp/paris-page-identities.json

This tool first replays the 20 frozen parent oldids through the existing
source-free preflight. It requires all 11 Paris ranges to match the exact
reviewed topology, then requests **current Page: metadata only** in batches
of 25, including page ID, revision ID, timestamp and MediaWiki SHA-1. It
replays all 185 captured oldids with the existing strict revision-identity
provider before issuing its source-free receipt. It never fetches Page:
wikitext, renders transclusion, stores book prose or publishes a manuscript.

The current metadata capture is **not atomic across API batches** and is **not
a historical rendering at the parent oldids**. A successful replay proves
those individual captured revisions can be addressed again by oldid. It does
not establish how the content was rendered, which page revision was active
when the parent was captured, whether the print pages are complete or how
chapter-boundary headers/footers should be selected. A final reviewed
immutable Page: identity manifest still needs to be adopted from the
validated receipt; the seven-day Actions artifact is a candidate, not an
automatically committed corpus artifact.

Hosted verification:
.github/workflows/white-guard-paris-page-identities.yml runs deterministic
positive/negative tests, captures exact metadata on the hosted runner and
validates a strict no-prose schema before uploading a seven-day artifact.
Provider errors, unexpected namespace/title redirects, missing pages,
malformed revision identities, duplicate IDs or replay drift abort without
a partial receipt. Failed hosted execution is **NOT_RUN**, never zero pages.

Separate next step: review and retain exact Page oldids, replay those
independently, then implement a **separate, versioned** bounded transclusion
renderer. The 1927/1989 split is preserved. A frozen literary body, the
300,000-character corpus threshold, matching FantLab input identity and M2
parity remain **UNKNOWN / 0 of 5** until their independent gates pass.

Source contracts: [ProofreadPage pages tag](https://www.mediawiki.org/wiki/Help:Extension:ProofreadPage/Pages_tag/en),
[MediaWiki revisions API](https://www.mediawiki.org/wiki/API:Revisions),
[Paris 1927 index](https://ru.wikisource.org/wiki/Индекс:Дни_Турбиных_(Белая_гвардия)_(Булгаков,_1927).djvu).
