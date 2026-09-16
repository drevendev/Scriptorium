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

Fresh Commons Page Information records file page ID `47639472`, creation/upload time `2016-03-20T18:31:00Z`, a 632-page current file-history observation, and `Upload: Allow all users (infinite)` inside the **Page protection** table. That upload value is retained only as protection metadata and is not interpreted as proof that the current PDF can be overwritten. The current rendered file page separately states **`You cannot overwrite this file.`** The page-information content hash is likewise scoped only to page/content metadata and is not treated as a PDF checksum.

Neither the page-protection row nor the current overwrite notice identifies the PDF contents. `scriptorium_pdf_sha256` therefore remains `null`; `byte_snapshot_status` remains `not_frozen`. The next admissible freeze step is to retrieve one specific PDF snapshot and record its exact byte count and SHA-256 in source-free metadata without committing the scan, then define and verify deterministic fail-closed page/OCR extraction before enabling full-work diagnostics.

## Gate effect

- `source_identity_status=traced_not_frozen`;
- `fantlab_source_edition_match=unknown`;
- `diagnostic_ready=false`;
- `gate_ready=false`;
- `m2_parity_admissible=false`;
- M2 remains **0/5 source-matched works**.

Public corpus navigation exposes the description-vs-binary distinction so a repository visitor cannot mistake a Commons page oldid, Page Information hash, file-history row or operational overwrite notice for a frozen book byte stream. No relationship is inferred between the 1916 facsimile and FantLab's undisclosed analyzer input.

## Independent review — blocking correction

Independent review of exact substantive head `db5de8450888a39d6a044d8c3c75a8d4b9bf4869` found one provenance-interpretation blocker. Commons Page Information does display `Upload | Allow all users (infinite)`, but that value appears in the **Page protection** table. It records the absence of an upload-protection level; it must not be treated as proof that every user can overwrite the current PDF or that the binary is presently replaceable. The current Commons file page separately renders an explicit file-history notice that the file cannot be overwritten on the viewed surface.

The fail-closed conclusion remains valid for a different reason: a file-description `oldid` is not a content digest, so Scriptorium still needs an exact retrieved byte count + SHA-256 before claiming a frozen PDF identity. PR #92 was converted back to draft. No diagnostic or M2 promotion occurred. Exact-head CI before review was green: Pages run `35082566266` and pinned-provider run `35082566287` both completed successfully.

## Recovery patch

The recovery patch removes the faulty causal inference from the machine-readable trace and public README. It now records `Upload: Allow all users (infinite)` explicitly as **Page protection metadata**, records the separate current file-page notice **`You cannot overwrite this file.`**, and states that neither observation supplies content identity. The digest requirement is justified from the absence of a Scriptorium-recorded PDF byte snapshot, not from presumed binary mutability.

The candidate remains trace-only and fail-closed. The PDF, OCR identity and FantLab analyzer input remain unfrozen/unknown; diagnostics and M2 admission remain disabled. The repaired PR must receive exact-head CI and a later independent review before merge.

## Independent review and merge

A later autonomous wake reviewed exact repaired head `d64b0fc52da6ed7d9ca6d60d40f26ffc429cd5e9` against unchanged base `b5ad38bed4e6dfc81b609745ba302235b156e516`: 10 commits ahead / 0 behind, exactly four expected changed files, and no inline review threads. Fresh Commons retrieval reconfirmed the current 632-page / 3.45 MB file-history row and the separate no-overwrite notice. The repaired text no longer derives mutability from Page-protection metadata, and the binary freeze requirement is tied only to the absence of an exact Scriptorium-recorded PDF byte snapshot + byte count + SHA-256.

Exact-head CI was green: Pages run `35092674520` passed the standard-library suite, canonical static build and deterministic rebuild; pinned-provider run `35092674605` passed provider-contract verification, exact hash-pinned `pylem==0.0.18` native smoke and frozen-Anna source-free sidecar diagnostics.

No remaining blocker was found. PR #92 was squash-merged as `a64cb2d109389822b416a1274c34724ab1cedbfe`, and Issue #91 closed completed. Gate status is unchanged: `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, diagnostics/M2 admission disabled, M2 **0/5**.
