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

The recovery patch synchronizes the public corpus navigation with the canonical provenance record. The Hyperboloid section explicitly exposes the Moscow 1958 lead as a 1939-fourth-edition-derived editorial/textual-family witness, records Russian State Library record `01006486636` as a distinct Kyiv 1958 edition, and preserves the rule that year-only matching has no identity weight. This repair changes documentation only; it does not add source bytes or weaken any source/parity gate.

## Independent review and merge

A later autonomous run independently reviewed repaired exact head `f33e3cb5861294f9b4389ded10cc2c35302401c9`. The branch was 7 commits ahead / 0 behind unchanged base `9d695174e83a4c63dc6a966898f9bf91815916ba` and changed exactly the four expected files: public corpus navigation, the Hyperboloid source-edition trace, this unit changelog, and durable state.

Fresh source verification reconfirmed the classification: Krestinsky distinguishes the 1927/1934/1936/1939 book editions and states that the Moscow Goslitizdat 1958 volume prints from the 1939 `Sovetsky pisatel` text with checking against preceding editions; Russian State Library record `01006486636` independently catalogs a distinct Kyiv 1958, 393-page *Hyperboloid of Engineer Garin; Aelita* edition.

Exact-head workflow runs `35045718867` (Scriptorium Pages) and `35045718851` (Scriptorium pinned pylem provider) both completed successfully. Their jobs passed the complete standard-library test suite, canonical Pages build plus deterministic rebuild, provider-contract suite, exact hash-pinned `pylem==0.0.18` native smoke, frozen Anna sidecar replay, and all source-free diagnostic builds/uploads. No blocking defect remained, so PR #84 was squash-merged as `86a98f14ca110981d32677446210db4b376a197c`; Issue #83 closed `completed`.

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
