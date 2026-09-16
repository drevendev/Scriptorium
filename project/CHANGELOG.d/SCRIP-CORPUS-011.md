# SCRIP-CORPUS-011 — harden Petersburg Commons provenance boundary

Issue: #91  
PR: #92  
Mode: corpus / provenance

## Decision

Strengthen the existing `bely-petersburg-1916-ru` source trace by explicitly separating a permanent Wikimedia Commons **file-description revision** from the still-unfrozen **PDF binary identity**.

FantLab work `293513` remains the benchmark reference: its linguistic analysis dated 19 September 2022 reports **944,182 characters** and **130,217 words**. The retained public edition remains the Wikimedia Commons **632-page facsimile of the first 1916 book publication**, described as a mechanical reproduction of the three *Sirin* installments from 1913–1914 and explicitly marked public domain.

The facsimile's title page was independently inspected and identifies *Петербург*, Andrei Bely, and 1916. No scan bytes, OCR, or source prose are committed.

## Binary-identity boundary

The previously recorded Commons permanent description locator `oldid=1046280975` freezes descriptive page wikitext; it does **not** by itself freeze the PDF bytes served for the file.

Fresh Commons page-information evidence records file page ID `47639472`, creation/upload time `2016-03-20T18:31:00Z`, a 632-page current file-history observation, and page-level upload permission reported as **Allow all users**. The page-information content hash is recorded only as page/content metadata and is explicitly **not** treated as a PDF checksum.

Consequently the current file-history row and direct `upload.wikimedia.org` URL are retrieval evidence, not immutable Scriptorium binary identity. `scriptorium_pdf_sha256` remains `null`; `byte_snapshot_status` remains `not_frozen`.

The next admissible freeze step is to retrieve one specific PDF snapshot and record its exact byte count and SHA-256 in source-free metadata without committing the scan, then define and verify deterministic fail-closed page/OCR extraction before enabling full-work diagnostics.

## Gate effect

- `source_identity_status=traced_not_frozen`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `gate_ready=false`;
- `m2_parity_admissible=false`;
- M2 remains **0/5 source-matched works**.

Public corpus navigation now exposes the description-vs-binary distinction so a repository visitor cannot mistake a Commons page oldid for a frozen book byte stream. No relationship is inferred between the 1916 facsimile and FantLab's undisclosed analyzer input.

This authoring run leaves PR #92 for a later independent exact-head review rather than self-merging it.

## Independent review — blocking correction

Independent review of exact substantive head `db5de8450888a39d6a044d8c3c75a8d4b9bf4869` found one provenance-interpretation blocker. Commons Page Information does display `Upload | Allow all users (infinite)`, but that value appears in the **Page protection** table. It records the absence of an upload-protection level; it must not be treated as proof that every user can overwrite the current PDF or that the binary is presently replaceable. The current Commons file page separately renders an explicit file-history notice that the file cannot be overwritten on the viewed surface.

The fail-closed conclusion remains valid for a different reason: a file-description `oldid` is not a content digest, so Scriptorium still needs an exact retrieved byte count + SHA-256 before claiming a frozen PDF identity. Recovery must revise the trace, public README, state and this changelog to distinguish page-protection metadata from binary overwrite capability, record the explicit current no-overwrite observation, and justify the digest requirement independently of inferred mutability.

PR #92 was converted back to draft. No diagnostic or M2 promotion occurred. Exact-head CI before review was green: Pages run `35082566266` and pinned-provider run `35082566287` both completed successfully.
