# SCRIP-CORPUS-006 — Hyperboloid bibliographic provenance strengthening

Issue: #81  
PR: #82  
Mode: corpus / provenance

## Decision

Strengthen `tolstoy-hyperboloid-garin-wikisource-ru` with a concrete 1958 Goslitizdat volume-4 bibliographic lead while keeping it explicitly non-identifying.

Direct evidence for the retained public candidate is unchanged: Russian Wikisource permanent revision `oldid=5014458` is a stable reviewed public-domain locator, cites `az.lib.ru`, and the work text says the novel was written in 1926–1927 and revised with new chapters in 1937. FantLab reports the 18 September 2022 linguistic analysis at 495,539 characters / 69,126 words, but does not disclose analyzer-input edition or bytes.

New collateral evidence narrows the next research target without crossing the source-identity gate:

- Russian Wikisource `Союз пяти (Толстой)`, a sibling A. N. Tolstoy page citing `az.lib.ru`, identifies its text source as A. N. Tolstoy, *Collected Works in ten volumes*, vol. 4, *Emigrants. Hyperboloid of Engineer Garin*, Moscow: Goslitizdat, 1958.
- Russian Wikisource `Случай на Бассейной улице (Толстой)`, another sibling Tolstoy page in the az.lib.ru import lineage, cites the same 1958 volume 4.
- FantLab bibliographic commentary on the novel independently identifies the same 1958 volume as a real *Hyperboloid of Engineer Garin* edition context.

These facts make the 1958 volume a testable edition-family lead. They do not prove that the Hyperboloid Wikisource/az.lib transcription was produced from that volume: the Hyperboloid page itself still names only `az.lib.ru`, and sibling-page provenance cannot establish the bytes or exact text identity of another page. They also say nothing about FantLab's undisclosed analyzer input.

## Gate effect

No parity or diagnostic gate advances:

- `bibliographic_source_identity` remains unset;
- `source_identity_status=traced_not_frozen`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `gate_ready=false`;
- `m2_parity_admissible=false`;
- M2 remains **0/5 source-matched works**.

No source prose is committed. The next evidence path is to freeze the exact Wikisource revision/body identity and independently test the 1958 volume lead with a direct source statement rather than infer it from sibling metadata.
