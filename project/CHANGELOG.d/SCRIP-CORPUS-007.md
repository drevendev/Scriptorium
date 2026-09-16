# SCRIP-CORPUS-007 — Hyperboloid textual-family provenance classification

Issue: #83  
PR: #84  
Mode: corpus / provenance

## Decision

Strengthen the concrete Moscow Goslitizdat 1958 volume-4 lead for `tolstoy-hyperboloid-garin-wikisource-ru` by classifying its textual family, while keeping the lead explicitly non-identifying for the Wikisource/az.lib transcription.

FantLab-hosted Yu. A. Krestinsky commentary distinguishes four book editions of *Hyperboloid of Engineer Garin* (1927, 1934, 1936, 1939). It describes the 1939 `Sovetsky pisatel` edition as the fourth book edition, based on the 1936 text with further stylistic corrections and restoration of passages that had been adapted for younger readers. Crucially, under the bibliographic heading for A. N. Tolstoy, *Collected Works in ten volumes*, volume 4, Moscow: Goslitizdat, 1958, the commentary states that the text is printed from the 1939 edition with checking against preceding editions.

That is stronger than the previous bare edition-family lead: the Moscow 1958 volume can now be classified as a **1939-fourth-edition-derived editorial/textual-family witness**. It is still not evidence that the retained Wikisource/az.lib transcription came from that volume.

Independent same-year disambiguation makes that distinction operationally important. The Russian State Library catalogs a separate Kyiv: Goslitizdat Ukrainy, 1958, 393-page edition containing *Hyperboloid of Engineer Garin* and *Aelita*. Therefore `1958` by itself is not an edition identifier and must never be used to equate the Wikisource transcription, the Moscow collected-works volume, or another same-year edition.

## Review recovery

The first independent exact-head review found one blocking completeness defect: the machine-readable trace and durable state contained the new classification, but `corpus/candidates/README.md` still exposed the older SCRIP-CORPUS-006 wording. PR #84 was therefore returned to draft rather than merged.

The recovery patch now synchronizes the public corpus navigation with the canonical provenance record. The Hyperboloid section explicitly exposes the Moscow 1958 lead as a 1939-fourth-edition-derived editorial/textual-family witness, records Russian State Library record `01006486636` as a distinct Kyiv 1958 edition, and preserves the rule that year-only matching has no identity weight. This repair changes documentation only; it does not add source bytes or weaken any source/parity gate.

## Gate effect

No source/parity gate advances:

- `bibliographic_source_identity` remains unset;
- `source_identity_status=traced_not_frozen`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `gate_ready=false`;
- `m2_parity_admissible=false`;
- M2 remains **0/5 source-matched works**.

No source prose is committed. The next evidence path remains exact public-revision freezing plus a direct bibliographic statement tying the Hyperboloid Wikisource/az.lib transcription itself to the specific Moscow Goslitizdat 1958 volume, not merely to a compatible late-lifetime textual family.
