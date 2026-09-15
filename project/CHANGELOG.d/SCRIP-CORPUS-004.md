# SCRIP-CORPUS-004 — trace a source-explicit Petersburg modernist candidate

- Issue: #77
- PR: #78
- Scope: corpus / provenance; no FantLab parity promotion and no source-text publication.
- Added `bely-petersburg-1916-ru` as a legally usable >=300,000-character candidate. FantLab's 19 September 2022 analysis reports 944,182 characters and 130,217 words.
- Selected Wikimedia Commons' 632-page facsimile of Andrei Bely's first 1916 book publication as the source-edition lead. Commons describes the volume as a mechanical reproduction of the novel parts published in three *Sirin* collections in 1913–1914 and explicitly marks the work public domain.
- Kept the 1916 first-book edition as a distinct text identity from Bely's materially revised 1922 edition. No equivalence across edition families is inferred.
- The generic Russian Wikisource landing page is recorded only as a legal/bibliographic cross-check: it explicitly sits in the `Тексты без ссылок на источники` category and therefore is not promoted as the candidate source identity.
- The candidate remains `traced_not_frozen`: Scriptorium has not yet frozen the Commons PDF byte digest, a deterministic page/OCR extraction contract, or raw/normalized literary-text digests. No scan pages, OCR, or source prose are committed.
- FantLab does not disclose which Petersburg edition or immutable byte stream was uploaded for its 2022 analysis. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`; M2 remains 0/5 source-matched works.
- Generalized the catalog-level legal-policy wording from a Russian-Wikisource-specific sentence to the repository's candidate-specific public-domain/open-license/permission rule so non-Wikisource legal sources cannot inherit a false provenance claim.
- Public corpus navigation now explains why the Commons facsimile is retained and what evidence is still required before full-work diagnostics.
- Authored head `2ec01e45bdc3e2ac69092e0cb3bfefd5ac2483be` was independently reviewed in a later run against unchanged base `6ddb25aec005c80628aa74278582e01c3d2a49a0`: it was 6 commits ahead / 0 behind and changed exactly the five expected corpus/provenance/state files.
- Exact-head Pages run `35004623316` completed successfully, including the complete standard-library test suite, canonical static-site build and deterministic rebuild. Pinned-provider run `35004623349` also completed successfully: provider-contract tests, exact hash-pinned `pylem==0.0.18` native smoke on Python 3.9, and the frozen Anna sidecar replay all passed.
- PR #78 had no pre-existing conversation comments, submitted reviews or inline review threads. Fresh external review reconfirmed FantLab's 944,182-character / 130,217-word reference, Commons' 632-page first-1916-book facsimile description and public-domain notice, and Wikisource's `Тексты без ссылок на источники` warning plus separate 1913/1922 edition navigation.
- No blocking defect was found. PR #78 was squash-merged as `22911929228b127e721f0607d0d1c97cf5dd6823`; Issue #77 closed completed. The merge does not freeze PDF/OCR bytes, enable diagnostics, establish FantLab source identity, publish source text, or advance M2 beyond 0/5.
